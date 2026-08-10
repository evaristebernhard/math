#!/usr/bin/env python3
"""有效预算扫描：``h_real = L_ideal(B_eff)``，不再外推固定 q。"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

import config
import model_core
import util


def load_budget_points(path, weights):
    payload = json.load(open(path, encoding="utf-8"))
    points = []
    for row in payload.get("rows", []):
        if row.get("parity") != "VERIFIED" or row.get("h_H") is None:
            continue
        metrics = model_core.budget_metrics(
            weights, int(row["mH"]), int(row["NU"]), float(row["h_H"])
        )
        points.append({
            "mH": int(row["mH"]), "NU": int(row["NU"]),
            "beta": int(row["beta"]), "h_H": float(row["h_H"]),
            "q_efficiency": float(row["q_efficiency"]), **metrics,
        })
    return points


def forecast_with_tax(weights, mH, nu, tax, target):
    ideal = model_core.ideal_row(weights, mH, nu, target)
    effective = max(0.0, model_core.raw_budget(nu)-tax)
    _, h_h = util.tilt_prediction(
        model_core.active_weights(weights, mH), effective
    )
    harvest = ideal["ideal_harvest"]["1000"]["q10"]
    return {
        "mH": mH, "dimension": mH+1, "NU": nu,
        "assumed_budget_tax_nats": tax,
        "effective_budget_nats": effective,
        "A_H": ideal["A_H"], "h_H": h_h,
        "harvest_Meff1000_q10": harvest,
        "total_q10": h_h+harvest,
        "target": target, "passes_target": h_h+harvest > target,
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", default="hurst",
                        choices=sorted(config.STAGES))
    parser.add_argument(
        "--qcal", default="work/probes/qcal_seed20260726/qcal_results.json"
    )
    parser.add_argument("--nu", type=int, default=1900)
    parser.add_argument("--target", type=float,
                        default=model_core.HURST_TARGET)
    parser.add_argument("--output", default="work/model/effective_budget.json")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    weights = model_core.scan_inputs(args.stage)
    points = load_budget_points(args.qcal, weights)
    taxes_by_beta = {}
    for beta in (20, 40):
        values = [row["budget_tax_nats"] for row in points
                  if row["beta"] == beta]
        if values:
            taxes_by_beta[str(beta)] = {
                "min": min(values), "median": float(np.median(values)),
                "max": max(values), "count": len(values),
            }

    # 不把 m<=460 的趋势外推成维度曲线；使用最坏已观测税作为保守包络。
    conservative_tax = max(
        row["budget_tax_nats"] for row in points if row["beta"] == 20
    )
    rows = [
        forecast_with_tax(weights, mH, args.nu, conservative_tax, args.target)
        for mH in range(600, 901, 20)
    ]
    passing = [row for row in rows if row["passes_target"]]
    payload = {
        "schema": 2, "stage": args.stage, "NU": args.nu,
        "target": args.target,
        "actual_model": "h_H_real=L_H_ideal(B_eff)",
        "raw_budget_nats": model_core.raw_budget(args.nu),
        "calibration": args.qcal,
        "budget_points": points,
        "budget_tax_by_beta": taxes_by_beta,
        "forecast_policy": "worst observed BKZ20 additive nats tax",
        "conservative_tax_nats": conservative_tax,
        "first_passing_mH": passing[0]["mH"] if passing else None,
        "rows": rows,
    }
    util.atomic_write_json(args.output, payload)
    print(f"[MODEL] B={payload['raw_budget_nats']:.3f} "
          f"tax={conservative_tax:.3f} first_pass="
          f"{payload['first_passing_mH']} -> {args.output}")


if __name__ == "__main__":
    main()
