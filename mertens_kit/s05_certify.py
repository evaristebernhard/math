#!/usr/bin/env python3
"""步骤 05: 分片、可续跑、保留零点半径的并行 Arb 认证。"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing
import os
import time

import config
import reduction
import util


CERT = {}


def candidate_id(stage, cy, nuy, prec, zero_source, meta_sha256=""):
    text = (
        f"{stage}:{cy}:{nuy}:{prec}:{zero_source}:{meta_sha256}"
    ).encode()
    return hashlib.sha256(text).hexdigest()[:20]


def shard_file(work_dir, stage, fingerprint, lo, hi):
    return os.path.join(work_dir, "cert_shards", stage, fingerprint,
                        f"{lo}_{hi}.json")


def valid_saved_shard(path, expected):
    try:
        payload = json.load(open(path, encoding="utf-8"))
        for key, value in expected.items():
            if payload.get(key) != value:
                return None
        from flint import arb
        arb(payload["sum_ball"])
        return payload
    except (OSError, ValueError, KeyError, TypeError):
        return None


def certify_shard(task):
    lo, hi, output, expected, resume = task
    from flint import acb, arb, ctx

    ctx.prec = CERT["prec"]
    if resume:
        saved = valid_saved_shard(output, expected)
        if saved is not None:
            return saved
    y = arb(CERT["cy"]) / arb(2) ** CERT["NUY"]
    T = arb(CERT["T_ball"])
    pi = arb.pi()
    total = arb(0)
    k = lo
    while k <= hi:
        count = min(200, hi - k + 1)
        texts = [CERT["zero_balls"].get(index)
                 for index in range(k, k + count)]
        if all(texts):
            zeros = [arb(text) for text in texts]
            source = "reused_strict_balls"
        else:
            zeros = [zero.imag for zero in acb.zeta_zeros(k, count)]
            source = "arb_recomputed"
        for offset, gamma in enumerate(zeros):
            index = k - 1 + offset
            alpha = arb(CERT["A"][index].strip())
            phase = arb(CERT["Bt"][index].strip())
            u = gamma / T
            kernel = (1-u) * (pi*u).cos() + (pi*u).sin()/pi
            total += 2 * alpha * kernel * (gamma*y-phase).cos()
        k += count
    payload = {
        **expected, "lo": lo, "hi": hi, "count": hi-lo+1,
        "sum_ball": str(total), "source": source,
    }
    util.atomic_write_json(output, payload)
    return payload


def load_strict_balls(path, total):
    rows = {}
    if not path or not os.path.exists(path):
        return rows
    for line in open(path, encoding="utf-8"):
        try:
            index, text = util.parse_arb_ball_line(line)
        except ValueError:
            continue
        if 1 <= index <= total:
            if index in rows:
                raise ValueError(f"严格零点文件重复索引 {index}")
            rows[index] = text
    return rows


def sufficient_ball_precision(zero_balls, indices, bits):
    from flint import arb, ctx
    ctx.prec = bits
    if not all(index in zero_balls for index in indices):
        return False
    return all(arb(zero_balls[index]).rel_accuracy_bits() >= bits - 16
               for index in indices)


def strict_ball_precision_report(zero_balls, indices, bits):
    """全量检查 reuse 输入；返回最小相对精度及其索引。"""
    from flint import arb, ctx
    ctx.prec = bits + 100
    minimum = None
    minimum_index = None
    for index in indices:
        if index not in zero_balls:
            return {"complete": False, "minimum_bits": None,
                    "minimum_index": index, "sufficient": False}
        accuracy = int(arb(zero_balls[index]).rel_accuracy_bits())
        if minimum is None or accuracy < minimum:
            minimum, minimum_index = accuracy, index
    return {
        "complete": True, "minimum_bits": minimum,
        "minimum_index": minimum_index,
        "required_bits": bits-16,
        "sufficient": minimum is not None and minimum >= bits-16,
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=sorted(config.STAGES))
    parser.add_argument("--jobs", type=int, default=config.NPROC)
    parser.add_argument("--chunk-size", type=int)
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--zeros-arb", default=config.ZEROS_ARB)
    parser.add_argument("--zero-source", choices=("auto", "reuse", "recompute"),
                        default="auto")
    parser.add_argument("--precision", type=int)
    parser.add_argument("--meta")
    parser.add_argument("--results")
    parser.add_argument("--output")
    return parser.parse_args()


def main():
    args = parse_args()
    started = time.time()
    cfg = config.STAGES[args.stage]
    meta_path = args.meta or f"{config.WORK_DIR}/{args.stage}_meta.json"
    result_path = args.results or f"{config.WORK_DIR}/{args.stage}_results.json"
    meta = json.load(open(meta_path, encoding="utf-8"))
    result = json.load(open(result_path, encoding="utf-8"))
    NEV, NU = int(meta["NEV"]), int(meta["NU"])
    NUY, cy = int(result["NUY"]), int(result["y_exact_num"])
    prec = args.precision or int((NU * 0.302 + 80) * 3.33)
    jobs = max(1, min(args.jobs, len(util.physical_cpu_ids(reserve=0))))
    zero_balls = {} if args.zero_source == "recompute" else \
        load_strict_balls(args.zeros_arb, NEV + 1)
    sample = sorted(set([1, NEV//2, NEV, NEV+1]))
    precision_report = (
        strict_ball_precision_report(
            zero_balls, range(1, NEV+2), prec
        )
        if args.zero_source == "reuse"
        else None
    )
    reusable = (
        precision_report["sufficient"] if precision_report is not None
        else sufficient_ball_precision(zero_balls, sample, prec)
    )
    if args.zero_source == "reuse" and (
        len(zero_balls) != NEV + 1 or not reusable
    ):
        raise SystemExit("--zero-source reuse 要求完整且精度足够的严格 Arb balls")
    if not reusable:
        zero_balls = {}
    zero_source = (
        f"strict:{util.sha256_file(args.zeros_arb)}"
        if zero_balls else "recompute:acb.zeta_zeros"
    )

    from flint import acb, ctx
    ctx.prec = prec
    if NEV + 1 in zero_balls:
        T_ball = zero_balls[NEV + 1]
    else:
        T_ball = str(acb.zeta_zeros(NEV + 1, 1)[0].imag)
    meta_sha256 = util.sha256_file(meta_path)
    fingerprint = candidate_id(
        args.stage, cy, NUY, prec, zero_source, meta_sha256
    )
    A = util.read_lines(os.path.join(config.DATA_DIR, "alpha.txt"))
    Bt = util.read_lines(os.path.join(config.DATA_DIR, "beta.txt"))
    CERT.update({
        "prec": prec, "cy": cy, "NUY": NUY, "T_ball": T_ball,
        "zero_balls": zero_balls, "A": A, "Bt": Bt,
    })
    step = args.chunk_size or max(1, math.ceil(NEV / max(1, jobs*4)))
    ranges = [(lo, min(NEV, lo+step-1)) for lo in range(1, NEV+1, step)]
    expected_base = {
        "fingerprint": fingerprint, "stage": args.stage,
        "cy": str(cy), "NUY": NUY, "precision": prec,
        "zero_source": zero_source, "meta_sha256": meta_sha256,
    }
    tasks = []
    for lo, hi in ranges:
        output = shard_file(config.WORK_DIR, args.stage, fingerprint, lo, hi)
        tasks.append((lo, hi, output, expected_base, args.resume))
    print(f"[05] stage={args.stage} jobs={jobs} shards={len(tasks)} "
          f"prec={prec} source={'strict balls' if zero_balls else 'recompute'}")
    if jobs == 1:
        shards = list(map(certify_shard, tasks))
    else:
        with multiprocessing.get_context("fork").Pool(jobs) as pool:
            # map 保留区间顺序；parent 也严格按 lo 递增求和。
            shards = list(pool.map(certify_shard, tasks))
    shards.sort(key=lambda item: item["lo"])

    from flint import arb
    ctx.prec = prec
    total = arb(0)
    for shard in shards:
        total += arb(shard["sum_ball"])
    err_data = arb(3) * arb(10) ** (-290)
    enclosure = total + arb(0, err_data)
    lo = float(enclosure.lower())
    hi = float(enclosure.upper())
    target = float(cfg["target"])
    output_path = args.output or f"{config.WORK_DIR}/{args.stage}_certificate.json"
    certificate = {
        "stage": args.stage, "h_lo": lo, "h_hi": hi,
        "h_ball": str(enclosure), "target": target,
        "surpassed": lo > target, "y": result.get("y"),
        "y_exact_num": str(cy), "NUY": NUY, "precision": prec,
        "zero_source": zero_source, "fingerprint": fingerprint,
        "meta": meta_path, "meta_sha256": meta_sha256,
        "strict_ball_precision": precision_report,
        "shards": [{"lo": item["lo"], "hi": item["hi"],
                    "sum_ball": item["sum_ball"], "source": item["source"]}
                   for item in shards],
    }
    util.atomic_write_json(output_path, certificate)
    print(f"[05] h(y,T) in [{lo:.16g}, {hi:.16g}]")
    print(f"[05] {'SURPASSED' if lo > target else 'not reached'} target {target}")
    print(f"[05] saved -> {output_path} ({time.time()-started:.1f}s)")


if __name__ == "__main__":
    main()
