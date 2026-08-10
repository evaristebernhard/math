#!/usr/bin/env python3
"""隔离变量的 BKZ q(d,beta) 标定。

每个 m 只做一次确定性 LLL；BKZ-20 与 BKZ-40 都直接从同一个 LLL
checkpoint 起跑、各单 tour，避免把维度税、档次收益和累计 tour 混在一起。
"""
from __future__ import annotations

import argparse
import json
import math
import multiprocessing
import os
import random
import subprocess
import sys
import time
from dataclasses import asdict

import numpy as np

import audit_core
import config
import model_core
import reduction
import util


def backend_command(beta, backend, no_lll=False):
    command = ["fplll", "-a", "bkz", "-b", str(beta), "-f", backend,
               "-bkzmaxloops", "1"]
    if backend == "mpfr":
        command += ["-p", "256"]
    if no_lll:
        command.append("-nolll")
    return command


def remaining(deadline):
    return max(0.0, deadline-time.time())


def reduction_available_memory():
    try:
        for line in open("/proc/meminfo", encoding="utf-8"):
            if line.startswith("MemAvailable:"):
                return int(line.split()[1])*1024
    except OSError:
        pass
    return 2**63-1


def prepare_instance(root, stage, mH, nu, seed, deadline, resume):
    directory = os.path.join(root, f"m{mH}_n{nu}")
    os.makedirs(directory, exist_ok=True)
    prefix = os.path.join(directory, "base")
    raw_basis, meta_path = prefix+"_basis.txt", prefix+"_meta.json"
    dim = mH+1
    if not (resume and util.validate_fplll_matrix(raw_basis, dim)
            and os.path.exists(meta_path)):
        if remaining(deadline) <= 0:
            raise TimeoutError("wall-clock deadline before lattice build")
        subprocess.run([
            sys.executable, "s02_build_lattice.py", stage,
            "--mH", str(mH), "--nu", str(nu), "--output-prefix", prefix,
        ], check=True, env={**os.environ, **reduction.THREAD_ENV},
           timeout=remaining(deadline))
    meta = json.load(open(meta_path, encoding="utf-8"))
    seeded_basis = os.path.join(directory, "basis_seeded.txt")
    if not (resume and util.validate_fplll_matrix(seeded_basis, dim)):
        rows = util.read_fplll_matrix(raw_basis, dim)
        random.Random(seed).shuffle(rows)
        util.write_fplll_matrix(seeded_basis, rows)
    lll = os.path.join(directory, "lll.txt")
    if not (resume and util.validate_fplll_matrix(lll, dim)):
        result = reduction.run_fplll(
            ["fplll", "-a", "lll", "-m", "wrapper"],
            seeded_basis, lll, dim, timeout=remaining(deadline),
            metadata={"probe": "qcal", "mH": mH, "NU": nu,
                      "seed": seed, "step": "lll"},
        )
        if not result.accepted:
            raise RuntimeError(f"m={mH} LLL failed: {result.status}")
    return {
        "mH": mH, "NU": nu, "seed": seed, "directory": directory,
        "meta": meta_path, "lll": lll,
        "lll_sha256": util.sha256_file(lll),
    }


def run_branch(task):
    instance, beta, stage, deadline, resume = task
    mH, nu = instance["mH"], instance["NU"]
    directory = instance["directory"]
    meta = json.load(open(instance["meta"], encoding="utf-8"))
    dim = mH+1
    checkpoint = os.path.join(directory, f"bkz{beta}.txt")
    records = []
    if not (resume and util.validate_fplll_matrix(checkpoint, dim)):
        accepted = None
        for backend in ("dpe", "longdouble", "mpfr"):
            if remaining(deadline) <= 0:
                break
            result = reduction.run_fplll(
                backend_command(beta, backend), instance["lll"], checkpoint,
                dim, timeout=remaining(deadline),
                metadata={"probe": "qcal", "mH": mH, "NU": nu,
                          "seed": instance["seed"], "beta": beta,
                          "parent_lll_sha256": instance["lll_sha256"],
                          "backend": backend, "single_tour": True},
            )
            records.append({"backend": backend, **asdict(result)})
            if result.accepted:
                accepted = result
                break
        if accepted is None:
            return {
                "mH": mH, "NU": nu, "beta": beta, "status": "failed",
                "parent_lll_sha256": instance["lll_sha256"],
                "runs": records,
            }
    # 完整 checkpoint 提交后立即做原始行序 MPFR-384。旧排序/float64
    # 属 decoder 专项审计，不混入这组 q(d,beta) 计时。
    candidate = audit_core.mpfr_babai(checkpoint, meta, "original", 384)
    scoring = audit_core.load_scoring_inputs(stage, meta)
    raw = audit_core.audit_candidate(candidate, meta, scoring, (100, 160))
    audit = {
        "stage": stage, "checkpoint": checkpoint,
        "checkpoint_sha256": util.sha256_file(checkpoint),
        "meta_mH": mH, "meta_NU": nu, "NUY": int(meta["NUY"]),
        "LH_ideal": str(meta["LH_pred"]), "candidates": [raw],
    }
    audit_path = os.path.join(directory, f"bkz{beta}_audit.json")
    util.atomic_write_json(audit_path, audit)
    return {
        "mH": mH, "dimension": dim, "NU": nu, "beta": beta,
        "status": "completed" if raw.get("parity") == "VERIFIED"
                  else "audit_failed",
        "parent_lll": instance["lll"],
        "parent_lll_sha256": instance["lll_sha256"],
        "checkpoint": checkpoint,
        "checkpoint_sha256": util.sha256_file(checkpoint),
        "audit": audit_path, "runs": records,
        "parity": raw.get("parity"), "cy": raw.get("cy"),
        "h_H": float(raw["metrics"]["h_H"]) if raw.get("metrics") else None,
        "A_H": float(raw["metrics"]["A_H"]) if raw.get("metrics") else None,
        # 用户表中的 q：真实重块效率；另存相对理想天花板的兑现率。
        "q_efficiency": (
            float(raw["metrics"]["efficiency"]) if raw.get("metrics") else None
        ),
        "q_vs_ideal_ceiling": (
            float(raw["metrics"]["h_H"])/float(meta["LH_pred"])
            if raw.get("metrics") else None
        ),
        "rho": float(raw["metrics"]["rho"]) if raw.get("metrics") else None,
    }


def fit_q(rows, bootstrap_samples=2000, seed=20260726):
    good = [row for row in rows
            if row.get("status") == "completed"
            and row.get("q_efficiency") is not None]
    paired = {}
    for row in good:
        paired.setdefault(row["mH"], {})[row["beta"]] = row
    direct = []
    for mH in sorted(paired):
        if 20 in paired[mH] and 40 in paired[mH]:
            q20 = paired[mH][20]["q_efficiency"]
            q40 = paired[mH][40]["q_efficiency"]
            direct.append({
                "mH": mH, "dimension": mH+1, "q20": q20, "q40": q40,
                "delta_q_20_to_40": q40-q20,
                "delta_q_per_beta": (q40-q20)/20,
                "delta_q_per_10_beta": (q40-q20)/2,
            })
    if len(good) < 4:
        return {"direct_slopes": direct, "status": "insufficient"}
    # q = a + b log(m/360) + c ((beta-20)/20)
    #     + d log(m/360)((beta-20)/20)
    X = np.asarray([
        [1, math.log(row["mH"]/360), (row["beta"]-20)/20,
         math.log(row["mH"]/360)*(row["beta"]-20)/20]
        for row in good
    ], dtype=float)
    y = np.asarray([row["q_efficiency"] for row in good])
    coefficients, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    residuals = y-X@coefficients
    boot = []
    rng = random.Random(seed)
    # 按 m 成对 bootstrap，保持“同一 LLL 分叉”实验结构。
    pair_groups = [[row for row in good if row["mH"] == mH]
                   for mH in sorted(paired)]
    for _ in range(bootstrap_samples):
        sample = [row for _ in pair_groups
                  for row in rng.choice(pair_groups)]
        xb = np.asarray([
            [1, math.log(row["mH"]/360), (row["beta"]-20)/20,
             math.log(row["mH"]/360)*(row["beta"]-20)/20]
            for row in sample
        ])
        yb = np.asarray([row["q_efficiency"] for row in sample])
        cb, _, rb, _ = np.linalg.lstsq(xb, yb, rcond=None)
        if rb == 4:
            boot.append(cb.tolist())
    return {
        "status": "fitted", "formula":
            "q=a+b*log(m/360)+c*((beta-20)/20)+d*interaction",
        "coefficients": coefficients.tolist(), "rank": int(rank),
        "residuals": [
            {"mH": row["mH"], "beta": row["beta"],
             "residual": float(value)}
            for row, value in zip(good, residuals)
        ],
        "rmse": float(math.sqrt(np.mean(residuals*residuals))),
        "direct_slopes": direct,
        "bootstrap_valid": len(boot),
        "bootstrap_coefficients": boot,
        "coefficient_interval_95": (
            np.quantile(np.asarray(boot), [0.025, 0.975], axis=0).T.tolist()
            if boot else None
        ),
    }


def predict_q(coefficients, mH, beta):
    x = np.asarray([
        1, math.log(mH/360), (beta-20)/20,
        math.log(mH/360)*(beta-20)/20,
    ])
    return float(x@np.asarray(coefficients))


def recommendations(fit, weights, target=1.6383):
    if fit.get("status") != "fitted":
        return []
    candidates = []
    for mH in range(260, 461, 20):  # 只在实测维度包络内插值。
        for beta in (20, 30, 40, 50):
            ideal = model_core.ideal_row(weights, mH, 900, target)
            q = predict_q(fit["coefficients"], mH, beta)
            hH = q*ideal["A_H"]
            harvest = ideal["ideal_harvest"]["1000"]["q10"]
            total = hH+harvest
            candidates.append({
                "mH": mH, "dimension": mH+1, "beta": beta,
                "q_pred": q, "A_H": ideal["A_H"], "h_H_pred": hH,
                "harvest_Meff1000_q10": harvest,
                "total_conservative": total,
                "surpasses_1_6383": total > target,
                "beta_extrapolated": beta > 40,
            })
            if fit.get("bootstrap_coefficients"):
                totals = [
                    predict_q(coefficients, mH, beta)*ideal["A_H"]+harvest
                    for coefficients in fit["bootstrap_coefficients"]
                ]
                candidates[-1]["bootstrap_total_interval_95"] = [
                    float(np.quantile(totals, 0.025)),
                    float(np.quantile(totals, 0.975)),
                ]
    candidates.sort(key=lambda row: (
        not row["surpasses_1_6383"], row["beta"],
        -row["total_conservative"]
    ))
    passing = [row for row in candidates if row["surpasses_1_6383"]]
    return (passing[:2] if passing else
            sorted(candidates, key=lambda row: -row["total_conservative"])[:2])


def required_beta_table(fit, weights, target=1.6383):
    result = []
    for row in fit.get("direct_slopes", []):
        ideal = model_core.ideal_row(weights, row["mH"], 900, target)
        harvest = ideal["ideal_harvest"]["1000"]["q10"]
        required_q = (target-harvest)/ideal["A_H"]
        slope = row["delta_q_per_beta"]
        beta_required = (
            20+(required_q-row["q20"])/slope if slope > 0 else None
        )
        result.append({
            **row, "A_H": ideal["A_H"],
            "harvest_Meff1000_q10": harvest,
            "observed_total_b20": row["q20"]*ideal["A_H"]+harvest,
            "observed_total_b40": row["q40"]*ideal["A_H"]+harvest,
            "required_q": required_q,
            "required_q_exceeds_one": required_q > 1,
            "linear_beta_required": beta_required,
            "within_measured_beta_range": (
                beta_required is not None and beta_required <= 40
            ),
            "within_beta50": (
                beta_required is not None and beta_required <= 50
            ),
        })
    return result


def write_report(path, rows, fit, required_rows, recommendations_rows):
    lines = [
        "# BKZ q(d,β) 隔离变量短探针", "",
        "| mH | dim | q20=hH/AH | q40=hH/AH | Δq/10β |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in fit.get("direct_slopes", []):
        lines.append(
            f"| {row['mH']} | {row['dimension']} | {row['q20']:.6f} | "
            f"{row['q40']:.6f} | {row['delta_q_per_10_beta']:+.6f} |"
        )
    lines += ["", "## 过 1.6383 所需线性外推", "",
              "| mH | required q | linear β_required | ≤50? |",
              "|---:|---:|---:|:---:|"]
    for row in required_rows:
        beta = row["linear_beta_required"]
        lines.append(
            f"| {row['mH']} | {row['required_q']:.6f} | "
            f"{beta:.1f} | {'yes' if row['within_beta50'] else 'no'} |"
        )
    lines += ["", f"fit RMSE: `{fit.get('rmse')}`", "",
              "## 推荐（仅 m=260..460 内插；β=50 明确为外推）", "",
              "| mH | β | q_pred | conservative h | pass |",
              "|---:|---:|---:|---:|:---:|"]
    for row in recommendations_rows:
        lines.append(
            f"| {row['mH']} | {row['beta']} | {row['q_pred']:.6f} | "
            f"{row['total_conservative']:.6f} | "
            f"{'yes' if row['surpasses_1_6383'] else 'no'} |"
        )
    with util.atomic_text_writer(path) as handle:
        handle.write("\n".join(lines)+"\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", default="bt2015",
                        choices=sorted(config.STAGES))
    parser.add_argument("--m", default="260,360,460")
    parser.add_argument("--nu", type=int, default=900)
    parser.add_argument("--betas", default="20,40")
    parser.add_argument("--seed", type=int, default=20260726)
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--wall-hours", type=float, default=4)
    parser.add_argument("--reserve-gib", type=float, default=1.2)
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction,
                        default=True)
    parser.add_argument("--output-dir",
                        default="work/probes/qcal_seed20260726")
    return parser.parse_args()


def main():
    args = parse_args()
    started = time.time()
    deadline = started+args.wall_hours*3600
    m_values = [int(x) for x in args.m.split(",") if x]
    betas = [int(x) for x in args.betas.split(",") if x]
    if betas != [20, 40]:
        raise SystemExit("隔离协议固定要求 --betas 20,40")
    os.makedirs(args.output_dir, exist_ok=True)
    instances = [
        prepare_instance(args.output_dir, args.stage, mH, args.nu,
                         args.seed, deadline, args.resume)
        for mH in m_values
    ]
    tasks = [(instance, beta, args.stage, deadline, args.resume)
             for instance in instances for beta in betas]
    reserve = int(args.reserve_gib*2**30)
    available = reduction_available_memory()
    memory_jobs = max(1, int(max(0, available-reserve)/(1536*2**20)))
    jobs = max(1, min(args.jobs, len(tasks), memory_jobs))
    print(f"[PROBE] branches={len(tasks)} jobs={jobs} deadline="
          f"{args.wall_hours:.2f}h", flush=True)
    with multiprocessing.get_context("fork").Pool(jobs) as pool:
        rows = list(pool.map(run_branch, tasks))
    fit = fit_q(rows)
    weights = model_core.scan_inputs(args.stage)
    required = required_beta_table(fit, weights)
    picks = recommendations(fit, weights)
    payload = {
        "schema": 1, "protocol": "same-LLL independent single-tour BKZ",
        "stage": args.stage, "mH": m_values, "NU": args.nu,
        "betas": betas, "seed": args.seed,
        "wall_seconds": time.time()-started,
        "rows": rows, "fit": fit, "required_beta": required,
        "recommendations": picks,
    }
    output = os.path.join(args.output_dir, "qcal_results.json")
    util.atomic_write_json(output, payload)
    write_report(os.path.join(args.output_dir, "qcal_report.md"),
                 rows, fit, required, picks)
    print(f"[PROBE] -> {output}", flush=True)


if __name__ == "__main__":
    main()
