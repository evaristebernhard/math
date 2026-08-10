#!/usr/bin/env python3
"""原始行序/旧范数排序的 MPFR-384 Babai 并排审计。"""
from __future__ import annotations

import argparse
import json
import os

import audit_core
import config
import util


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=sorted(config.STAGES))
    parser.add_argument("checkpoints", nargs="+")
    parser.add_argument("--meta")
    parser.add_argument("--mpfr-bits", type=int, default=384)
    parser.add_argument("--scorer-dps", default="100,160")
    parser.add_argument("--output")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(os.path.join(config.WORK_DIR, "audit"), exist_ok=True)
    meta_path = args.meta or f"{config.WORK_DIR}/{args.stage}_meta.json"
    meta = json.load(open(meta_path, encoding="utf-8"))
    dps = tuple(int(x) for x in args.scorer_dps.split(",") if x)
    if len(dps) != 2:
        raise SystemExit("--scorer-dps 必须给两个精度，例如 100,160")
    dim = int(meta["mH"]) + 1
    if any(not util.validate_fplll_matrix(path, dim) for path in args.checkpoints):
        raise SystemExit("checkpoint 不完整或与 meta 维度不符")
    audits = [
        audit_core.audit_checkpoint(args.stage, path, meta, args.mpfr_bits, dps)
        for path in args.checkpoints
    ]
    paired = []
    for audit in audits:
        rows = {(r["order"], r["backend"]): r for r in audit["candidates"]}
        raw = rows.get(("original", f"mpfr-{args.mpfr_bits}"))
        old = rows.get(("norm", f"mpfr-{args.mpfr_bits}"))
        if raw and old and raw.get("metrics") and old.get("metrics"):
            paired.append(float(raw["metrics"]["h_H"])
                          - float(old["metrics"]["h_H"]))
    # 小样本只报告保守的“一致胜出”，不强行做完整维度拟合。
    significant = bool(paired and min(paired) > 0)
    selected = "original" if significant else "original_default_unresolved"
    payload = {
        "schema": 1, "stage": args.stage, "meta": meta_path,
        "meta_sha256": util.sha256_file(meta_path),
        "mpfr_bits": args.mpfr_bits, "scorer_dps": list(dps),
        "audits": audits,
        "order_comparison": {
            "paired_h_H_delta_original_minus_norm": paired,
            "original_consistently_better": significant,
            "model_decoder_order": selected,
        },
    }
    output = args.output or os.path.join(config.WORK_DIR, "audit",
                                         f"{args.stage}_decoder.json")
    util.atomic_write_json(output, payload)
    print(f"[AUDIT] checkpoints={len(audits)} order={selected} -> {output}")


if __name__ == "__main__":
    main()
