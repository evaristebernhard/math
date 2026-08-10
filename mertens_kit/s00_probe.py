#!/usr/bin/env python3
"""步骤 00: 主机/后端探测与目标 basis 单-tour 墙钟基准。"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time

import config
import reduction
import util


BACKENDS = ("dd", "qd", "dpe", "longdouble", "mpfr")


def version(command):
    try:
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=10)
        return result.stdout.splitlines()[0]
    except Exception as exc:
        return f"unavailable: {type(exc).__name__}: {exc}"


def memory_info():
    values = {}
    for line in open("/proc/meminfo", encoding="utf-8"):
        key, value = line.split(":", 1)
        values[key] = int(value.split()[0]) * 1024
    return {"total_bytes": values.get("MemTotal", 0),
            "available_bytes": values.get("MemAvailable", 0)}


def tiny_basis(path):
    util.write_fplll_matrix(path, [
        [105, 821, 404, 328],
        [881, 667, 644, 927],
        [181, 483, 87, 500],
        [893, 834, 732, 441],
    ])


def command_for(backend, beta, limit_seconds=None):
    command = ["fplll", "-a", "bkz", "-b", str(beta), "-f", backend,
               "-bkzmaxloops", "1"]
    if backend == "mpfr":
        command += ["-p", "256"]
    if limit_seconds:
        command += ["-bkzmaxtime", str(max(1, int(limit_seconds)))]
    return command


def probe_backend(backend, basis, dim, beta, timeout, output_dir, target=None):
    output = os.path.join(output_dir, f"probe_{backend}.txt")
    result = reduction.run_fplll(
        command_for(backend, beta, timeout),
        basis,
        output,
        dim,
        timeout=timeout,
        metadata={"backend": backend, "probe": True},
    )
    decode = (reduction.mpfr_decode_check(output, dim, target)
              if result.accepted else {"valid": False, "available": False})
    payload = result.__dict__.copy()
    payload["mpfr384_decode"] = decode
    # 支持性与速度分开：tiny probe 完成即支持；目标 benchmark 还要求解码。
    payload["usable"] = result.accepted and (
        decode.get("valid", False) or target is None
    )
    return payload


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--basis", help="目标 basis；省略时只做安全的 tiny probe")
    parser.add_argument("--meta", help="目标 meta，用于维度和 MPFR-384 Babai")
    parser.add_argument("--beta", type=int, default=20)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--backends", nargs="+", choices=BACKENDS,
                        default=list(BACKENDS))
    parser.add_argument("--output", default=f"{config.WORK_DIR}/s00_probe.json")
    parser.add_argument("--start-qd-build", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(config.WORK_DIR, exist_ok=True)
    cpus = util.physical_cpu_ids(reserve=0)
    report = {
        "time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "platform": platform.platform(),
        "logical_cpus": os.cpu_count(),
        "physical_cpu_ids": cpus,
        "recommended_cpu_ids": util.physical_cpu_ids(reserve=2),
        "memory": memory_info(),
        "fplll": version(["fplll", "--version"]),
        "python": sys.version.split()[0],
        "python_modules": {},
    }
    for module in ("fpylll", "flint", "numpy", "mpmath"):
        try:
            imported = __import__(module)
            report["python_modules"][module] = getattr(imported, "__version__", "present")
        except Exception as exc:
            report["python_modules"][module] = f"unavailable: {exc}"

    if args.start_qd_build:
        log = open(f"{config.WORK_DIR}/fplll_qd_build.log", "ab")
        process = subprocess.Popen(
            ["bash", "build_fplll_qd.sh"], stdout=log, stderr=subprocess.STDOUT,
            start_new_session=True, env={**os.environ, **reduction.THREAD_ENV},
        )
        report["qd_build"] = {"pid": process.pid,
                              "log": f"{config.WORK_DIR}/fplll_qd_build.log"}

    with tempfile.TemporaryDirectory(dir=config.WORK_DIR, prefix="s00.") as tmp:
        if args.basis:
            if not args.meta:
                raise SystemExit("--basis 需要 --meta 以确定维度和 target")
            meta = json.load(open(args.meta, encoding="utf-8"))
            dim = int(meta["mH"]) + 1
            if not util.validate_fplll_matrix(args.basis, dim):
                raise SystemExit("目标 basis 不是完整的方阵")
            basis = args.basis
            target = [int(x) for x in meta["tvec"]]
            beta = args.beta
            report["probe_kind"] = "target_single_tour"
        else:
            basis = os.path.join(tmp, "tiny.txt")
            tiny_basis(basis)
            dim, target, beta = 4, None, min(args.beta, 3)
            report["probe_kind"] = "tiny_support"
        report["basis"] = {"path": basis, "dim": dim, "beta": beta}
        report["backends"] = {}
        # 每个后端均是独立进程；unsupported 的 SIGABRT 不会带走探测器。
        for backend in args.backends:
            print(f"[00] probe {backend} ...", flush=True)
            report["backends"][backend] = probe_backend(
                backend, basis, dim, beta, args.timeout, tmp, target
            )
            item = report["backends"][backend]
            print(f"[00] {backend}: {item['status']}, "
                  f"{item['seconds']:.2f}s, RSS={item['peak_rss_kib']/1024:.1f} MiB")
    util.atomic_write_json(args.output, report)
    print(f"[00] report -> {args.output}")


if __name__ == "__main__":
    main()
