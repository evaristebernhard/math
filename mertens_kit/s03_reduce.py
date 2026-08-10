#!/usr/bin/env python3
"""步骤 03: 多条单核、独立 LLL/BKZ 链的吞吐赛马。"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import os
import random
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass

import config
import reduction
import util


@dataclass(frozen=True)
class Chain:
    index: int
    chain_id: str
    mH: int
    nu: int
    seed: int
    cpu: int
    basis: str
    meta: str
    directory: str


def expand_profile(stage: str, seed: int, cpus: list[int]) -> list[Chain]:
    entries = config.RACE_PROFILES.get(stage)
    if not entries:
        cfg = config.STAGES[stage]
        entries = [(cfg["mH"], cfg["NU"], 1)]
    result = []
    index = 0
    for mH, nu, count in entries:
        for _ in range(count):
            chain_seed = seed + 104729 * index
            chain_id = f"m{mH}_n{nu}_s{chain_seed}"
            directory = os.path.join(config.WORK_DIR, "races", stage, chain_id)
            prefix = os.path.join(directory, chain_id)
            result.append(Chain(
                index=index, chain_id=chain_id, mH=mH, nu=nu,
                seed=chain_seed, cpu=cpus[index % len(cpus)],
                basis=prefix + "_basis.txt", meta=prefix + "_meta.json",
                directory=directory,
            ))
            index += 1
    return result


def build_base(stage: str, mH: int, nu: int) -> tuple[str, str]:
    directory = os.path.join(config.WORK_DIR, "races", stage, "bases")
    prefix = os.path.join(directory, f"m{mH}_n{nu}")
    basis, meta = prefix + "_basis.txt", prefix + "_meta.json"
    dim = mH + 1
    if util.validate_fplll_matrix(basis, dim) and os.path.exists(meta):
        return basis, meta
    os.makedirs(directory, exist_ok=True)
    command = [
        sys.executable, "s02_build_lattice.py", stage,
        "--mH", str(mH), "--nu", str(nu), "--output-prefix", prefix,
    ]
    subprocess.run(command, check=True, env={**os.environ, **reduction.THREAD_ENV})
    if not util.validate_fplll_matrix(basis, dim):
        raise RuntimeError(f"构格输出无效: {basis}")
    return basis, meta


def prepare_chain(chain: Chain, base_basis: str, base_meta: str):
    os.makedirs(chain.directory, exist_ok=True)
    dim = chain.mH + 1
    if not util.validate_fplll_matrix(chain.basis, dim):
        rows = util.read_fplll_matrix(base_basis, dim)
        random.Random(chain.seed).shuffle(rows)
        util.write_fplll_matrix(chain.basis, rows)
    if not os.path.exists(chain.meta):
        with util.atomic_text_writer(chain.meta) as handle:
            handle.write(open(base_meta, encoding="utf-8").read())
    util.atomic_write_json(
        os.path.join(chain.directory, "chain.json"),
        {**asdict(chain), "base_basis": base_basis,
         "basis_sha256": util.sha256_file(chain.basis)},
    )


def backend_command(beta: int, backend: str):
    command = ["fplll", "-a", "bkz", "-b", str(beta), "-f", backend,
               "-bkzmaxloops", "1"]
    if backend == "mpfr":
        command += ["-p", "256"]
    return command


def available_memory():
    for line in open("/proc/meminfo", encoding="utf-8"):
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) * 1024
    return 0


def wait_for_memory(reserve_bytes: int):
    while available_memory() and available_memory() < reserve_bytes + 256 * 2**20:
        time.sleep(2)


def score_checkpoint(stage, chain: Chain, checkpoint: str, beta: int):
    output = os.path.join(chain.directory, f"anchor_b{beta}.json")
    command = [
        sys.executable, "s04_search.py", stage, checkpoint,
        "--meta", chain.meta, "--mode", "anchor", "--jobs", "1",
        "--seed", str(chain.seed), "--output", output,
    ]
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        env={**os.environ, **reduction.THREAD_ENV},
    )
    with util.atomic_text_writer(output + ".log") as handle:
        handle.write(result.stdout)
    return output if result.returncode == 0 and os.path.exists(output) else None


def run_chain(task):
    stage, chain, betas, timeout, resume, do_score, reserve_bytes = task
    dim = chain.mH + 1
    wait_for_memory(reserve_bytes)
    lll = os.path.join(chain.directory, "lll.txt")
    records = []
    if resume and util.validate_fplll_matrix(lll, dim):
        current = lll
        records.append({"step": "lll", "status": "resumed", "accepted": True})
    else:
        result = reduction.run_fplll(
            ["fplll", "-a", "lll", "-m", "wrapper"],
            chain.basis, lll, dim, timeout=timeout, cpu=chain.cpu,
            metadata={"chain": chain.chain_id, "step": "lll"},
        )
        records.append({"step": "lll", **asdict(result)})
        if not result.accepted:
            return chain.chain_id, records
        current = lll

    for level, beta in enumerate(betas):
        output = os.path.join(chain.directory, f"bkz{beta}.txt")
        if resume and util.validate_fplll_matrix(output, dim):
            current = output
            records.append({"step": f"bkz{beta}", "status": "resumed",
                            "accepted": True, "output": output})
        else:
            primary = "dpe" if (chain.index + level) % 2 == 0 else "longdouble"
            backends = [primary]
            if primary == "dpe":
                backends.append("longdouble")
            backends.append("mpfr")
            accepted = None
            for backend in dict.fromkeys(backends):
                wait_for_memory(reserve_bytes)
                result = reduction.run_fplll(
                    backend_command(beta, backend), current, output, dim,
                    timeout=timeout, cpu=chain.cpu,
                    metadata={"chain": chain.chain_id, "step": f"bkz{beta}",
                              "backend": backend},
                )
                records.append({"step": f"bkz{beta}", "backend": backend,
                                **asdict(result)})
                if result.accepted:
                    accepted = result
                    break
            if accepted is None:
                break
            current = output
        if do_score:
            score = score_checkpoint(stage, chain, current, beta)
            records[-1]["anchor_output"] = score
    util.atomic_write_json(os.path.join(chain.directory, "runs.json"), records)
    return chain.chain_id, records


def single_chain(args, betas):
    cfg = config.STAGES[args.stage]
    dim = cfg["mH"] + 1
    cpu = util.physical_cpu_ids(reserve=2)[0]
    basis = f"{config.WORK_DIR}/{args.stage}_basis.txt"
    meta = f"{config.WORK_DIR}/{args.stage}_meta.json"
    chain = Chain(0, args.stage, cfg["mH"], cfg["NU"], args.seed, cpu,
                  basis, meta, config.WORK_DIR)
    # 单链保持原有 checkpoint 命名。
    lll = f"{config.WORK_DIR}/{args.stage}_lll.txt"
    current = basis
    if not (args.resume and util.validate_fplll_matrix(lll, dim)):
        result = reduction.run_fplll(
            ["fplll", "-a", "lll", "-m", "wrapper"], basis, lll, dim,
            timeout=args.timeout, cpu=cpu,
        )
        if not result.accepted:
            raise SystemExit(f"LLL 失败: {result.status}")
    current = lll
    for level, beta in enumerate(betas):
        output = f"{config.WORK_DIR}/{args.stage}_bkz{beta}.txt"
        if args.resume and util.validate_fplll_matrix(output, dim):
            current = output
            continue
        primary = "dpe" if level % 2 == 0 else "longdouble"
        backends = [primary] + (["longdouble"] if primary == "dpe" else []) + ["mpfr"]
        for backend in dict.fromkeys(backends):
            result = reduction.run_fplll(
                backend_command(beta, backend), current, output, dim,
                timeout=args.timeout, cpu=cpu,
            )
            print(f"[03] BKZ-{beta}/{backend}: {result.status} "
                  f"{result.seconds:.1f}s", flush=True)
            if result.accepted:
                current = output
                break
        else:
            raise SystemExit(f"BKZ-{beta} 所有后端失败")
    print(f"[03] 最终约化基: {current}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=sorted(config.STAGES))
    parser.add_argument("betas", type=int, nargs="*")
    parser.add_argument("--jobs", type=int, default=config.NPROC)
    parser.add_argument("--seed", type=int, default=20260726)
    parser.add_argument("--timeout", type=float, default=8 * 3600)
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--single", action="store_true",
                        help="兼容参数；当前默认已经是单链")
    parser.add_argument("--score-checkpoints",
                        action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--reserve-gib", type=float, default=1.2)
    parser.add_argument(
        "--campaign", action="append", default=[],
        choices=("bt2015-14", "bkz50-escalation"),
        help=("长跑能力默认关闭；14 链和 BKZ-50 必须分别显式指定 campaign "
              "（可重复传参）"),
    )
    parser.add_argument("--escalate-bkz50", action="store_true",
                        help=argparse.SUPPRESS)  # 旧参数不再单独授权 escalation
    return parser.parse_args()


def main():
    args = parse_args()
    betas = args.betas or config.STAGES[args.stage]["beta_list"]
    race_enabled = "bt2015-14" in args.campaign
    if "bkz50-escalation" in args.campaign and not race_enabled:
        raise SystemExit("bkz50-escalation 必须与 --campaign bt2015-14 同时指定")
    if not race_enabled:
        single_chain(args, betas)
        return
    if args.stage != "bt2015":
        raise SystemExit("bt2015-14 campaign 只适用于 bt2015 stage")
    cpus = util.physical_cpu_ids(reserve=2)
    jobs = min(args.jobs, len(cpus))
    chains = expand_profile(args.stage, args.seed, cpus)
    # 每种参数只构造一次，再为每个 seed 做确定性行排列。
    bases = {}
    for chain in chains:
        key = chain.mH, chain.nu
        bases.setdefault(key, build_base(args.stage, *key))
        prepare_chain(chain, *bases[key])
    print(f"[03] race chains={len(chains)} jobs={jobs} physical CPUs={cpus[:jobs]}")
    tasks = [
        (args.stage, chain, betas, args.timeout, args.resume,
         args.score_checkpoints, int(args.reserve_gib * 2**30))
        for chain in chains
    ]
    context = multiprocessing.get_context("fork")
    with context.Pool(jobs) as pool:
        results = list(pool.imap(run_chain, tasks, chunksize=1))
    summary = {"stage": args.stage, "betas": betas, "chains": []}
    for chain_id, records in results:
        summary["chains"].append({
            "chain_id": chain_id,
            "accepted_steps": sum(bool(row.get("accepted")) for row in records),
            "last_status": records[-1].get("status") if records else "not_started",
        })

    # Gate: BKZ-40 pilot 未到 1.645 时，前四名各派生三个全新行排列。
    if "bkz50-escalation" in args.campaign and 40 in betas:
        ranked = []
        by_id = {chain.chain_id: chain for chain in chains}
        for chain in chains:
            anchor = os.path.join(chain.directory, "anchor_b40.json")
            checkpoint = os.path.join(chain.directory, "bkz40.txt")
            try:
                score = float(json.load(open(anchor, encoding="utf-8"))["h_H"])
            except (OSError, ValueError, KeyError):
                continue
            if util.validate_fplll_matrix(checkpoint, chain.mH + 1):
                ranked.append((score, chain, checkpoint))
        ranked.sort(reverse=True, key=lambda item: item[0])
        if ranked and ranked[0][0] < 1.645:
            branches = []
            for rank, (_, parent, checkpoint) in enumerate(ranked[:4]):
                for branch_index in range(3):
                    branch_seed = parent.seed + (branch_index + 1) * 1_000_003
                    chain_id = f"{parent.chain_id}_b50_{branch_index}"
                    directory = os.path.join(config.WORK_DIR, "races",
                                             args.stage, chain_id)
                    prefix = os.path.join(directory, chain_id)
                    branch = Chain(
                        index=rank*3+branch_index, chain_id=chain_id,
                        mH=parent.mH, nu=parent.nu, seed=branch_seed,
                        cpu=cpus[(rank*3+branch_index) % len(cpus)],
                        basis=prefix+"_basis.txt", meta=prefix+"_meta.json",
                        directory=directory,
                    )
                    prepare_chain(branch, checkpoint, parent.meta)
                    branches.append(branch)
            branch_tasks = [
                (args.stage, branch, [50], args.timeout, args.resume,
                 args.score_checkpoints, int(args.reserve_gib * 2**30))
                for branch in branches
            ]
            with context.Pool(min(jobs, len(branches))) as pool:
                branch_results = list(pool.imap(run_chain, branch_tasks, chunksize=1))
            summary["bkz50_gate"] = {
                "triggered": True, "pilot_best_h_H": ranked[0][0],
                "parents": [item[1].chain_id for item in ranked[:4]],
                "branches": [item[0] for item in branch_results],
            }
        else:
            summary["bkz50_gate"] = {
                "triggered": False,
                "pilot_best_h_H": ranked[0][0] if ranked else None,
                "reason": "pilot reached gate or no valid scored BKZ-40 checkpoint",
            }
    output = os.path.join(config.WORK_DIR, "races", args.stage, "summary.json")
    util.atomic_write_json(output, summary)
    print(f"[03] race summary -> {output}")


if __name__ == "__main__":
    main()
