#!/usr/bin/env python3
"""Exploratory frequency multipliers: keep distinct rational directions, allow nonprimitive modes."""
import argparse
import json
import numpy as np
from balanced_f import support, BalancedF

def run(radius=4, attempts=100, seed=143, restarts=2, maxiter=450):
    rng = np.random.default_rng(seed)
    primitive = support(radius)
    reports = []
    best = None
    for trial in range(attempts + 1):
        if trial == 0:
            multipliers = np.ones(len(primitive), dtype=int)
        elif trial == 1:
            multipliers = np.full(len(primitive), 2, dtype=int)
        else:
            multipliers = rng.choice([1, 2, 3], len(primitive), p=[.55, .30, .15])
        freq = primitive * multipliers[:, None]
        model = BalancedF(freq, v=(1, .6180339887498949))
        ans = model.optimize(restarts=restarts, seed=seed + trial, maxiter=maxiter)
        result = {
            "trial": trial, "radius": radius, "D": len(freq),
            "max_frequency": int(np.max(np.abs(freq))),
            "nonprimitive_count": int(np.count_nonzero(multipliers > 1)),
            "J": ans["J"], "sampled_sup_lower": ans["sup_grid"],
            "moment_sup_lower": float(np.sqrt(1 + ans["J"])),
            "factors": multipliers.tolist(), "phases": ans["phase"],
        }
        reports.append({k: v for k, v in result.items() if k not in ("factors", "phases")})
        if best is None or result["J"] < best["J"]:
            best = result
    return {"best": best, "trials": reports}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius", type=int, default=4)
    parser.add_argument("--attempts", type=int, default=100)
    parser.add_argument("--seed", type=int, default=143)
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    report = run(args.radius, args.attempts, args.seed)
    print({k: v for k, v in report["best"].items() if k not in ("factors", "phases")})
    if args.output:
        with open(args.output, "w") as fp:
            json.dump(report, fp, indent=2)
