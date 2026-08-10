#!/usr/bin/env python3
"""步骤 01: 并行、原子、可断点续跑的 Arb 零点生产线。"""
from __future__ import annotations

import argparse
import multiprocessing
import os
import time
from pathlib import Path

import config
import util


def shard_path(work_dir: str, lo: int, hi: int) -> str:
    return os.path.join(work_dir, f"zpart_{lo}_{hi}.txt")


def validate_shard(path: str, lo: int, hi: int) -> list[str]:
    with open(path, encoding="utf-8") as handle:
        return util.validate_arb_rows(handle, lo, hi, require_ball=True)


def make_shard(task):
    lo, hi, bits, work_dir, resume = task
    from flint import acb, ctx

    ctx.prec = bits
    output = shard_path(work_dir, lo, hi)
    if resume and os.path.exists(output):
        try:
            validate_shard(output, lo, hi)
            return output, True
        except (OSError, ValueError):
            pass

    with util.atomic_text_writer(output) as handle:
        k = lo
        while k <= hi:
            count = min(50, hi - k + 1)
            zeros = acb.zeta_zeros(k, count)
            if len(zeros) != count:
                raise RuntimeError(f"Arb 返回 {len(zeros)}/{count} 个零点")
            for offset, zero in enumerate(zeros):
                # str(arb) 是含半径的严格球；去空格后仍可由 arb(text) 解析。
                text = str(zero.imag).replace(" ", "")
                util.parse_arb_ball_line(f"{k + offset} {text}")
                handle.write(f"{k + offset} {text}\n")
            k += count

    validate_shard(output, lo, hi)
    return output, False


def merge_shards(parts, output: str, total: int) -> None:
    rows = {}
    for path, lo, hi in parts:
        for row in validate_shard(path, lo, hi):
            k, _ = util.parse_arb_ball_line(row)
            if k in rows:
                raise ValueError(f"合并时发现重复索引 {k}")
            rows[k] = row
    missing = [k for k in range(1, total + 1) if k not in rows]
    if missing:
        raise ValueError(f"合并缺少 {len(missing)} 个索引，首个 {missing[0]}")
    with util.atomic_text_writer(output) as handle:
        for k in range(1, total + 1):
            handle.write(rows[k] + "\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=config.NPROC)
    parser.add_argument("--chunk-size", type=int)
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--count", type=int, default=config.NEV + 1,
                        help="测试时可生成较小前缀；正式默认 NEV+1")
    parser.add_argument("--bits", type=int, default=config.ARB_PREC_BITS)
    parser.add_argument("--output", default=config.ZEROS_ARB)
    parser.add_argument("--skip-kn-check", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.jobs < 1 or args.count < 1 or args.bits < 64:
        raise SystemExit("--jobs/--count 必须为正，--bits 至少 64")
    os.makedirs(config.WORK_DIR, exist_ok=True)
    jobs = min(args.jobs, len(util.physical_cpu_ids(reserve=0)))
    step = args.chunk_size or max(200, args.count // max(1, jobs * 4))
    if step < 1:
        raise SystemExit("--chunk-size 必须为正")
    ranges = [(lo, min(lo + step - 1, args.count))
              for lo in range(1, args.count + 1, step)]
    started = time.time()
    print(f"[01] {args.count} zeros @ {args.bits} bits, "
          f"{len(ranges)} chunks, {jobs} jobs, resume={args.resume}")
    tasks = [(lo, hi, args.bits, config.WORK_DIR, args.resume)
             for lo, hi in ranges]
    if jobs == 1:
        results = list(map(make_shard, tasks))
    else:
        context = multiprocessing.get_context("fork")
        with context.Pool(jobs) as pool:
            results = list(pool.map(make_shard, tasks))
    merge_shards(
        [(path, lo, hi) for (lo, hi), (path, _) in zip(ranges, results)],
        args.output,
        args.count,
    )
    reused = sum(was_reused for _, was_reused in results)
    print(f"[01] done: {args.output} ({time.time()-started:.1f}s; "
          f"reused {reused}/{len(results)} shards)")

    if not args.skip_kn_check and args.count >= 1:
        kn_path = os.path.join(config.DATA_DIR, "zeroes.txt")
        kn = open(kn_path, encoding="utf-8").readline().strip()[:60]
        first = open(args.output, encoding="utf-8").readline()
        _, mid = util.parse_arb_line(first)
        if mid[:55] != kn[:55]:
            raise RuntimeError("gamma_1 与 K-N 数据不符")
        print("[01] self-check vs K-N gamma_1: OK")


if __name__ == "__main__":
    main()
