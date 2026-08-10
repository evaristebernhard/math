#!/usr/bin/env python3
"""Scan extremal-polynomial finite-independence designs.

The script uses the current Hurst-stage kernel weights and compares:

* uniform designs: top m weights with a common N;
* greedy anisotropic designs: each selected coordinate receives its own N_i.

The principal bounded-box complexity proxy is

    H_box = sum_i log10(2*N_i + 1),

which is the base-10 logarithm of the coefficient-box cardinality.  This is
closer to the actual bounded-CVP statement than a spherical SVP volume proxy.
"""
from __future__ import annotations

import argparse
import heapq
import json
import math
import os
from collections import Counter

import config
import util


def load_weights(cutoff_count: int) -> list[float]:
    # Planning scans may use the full K--N 301-digit table.  Final certificates
    # must replace these values by independently generated strict Arb balls.
    gamma_rows = util.read_lines(os.path.join(config.DATA_DIR, "zeroes.txt"))
    alpha_rows = util.read_lines(os.path.join(config.DATA_DIR, "alpha.txt"))
    gammas = [float(value) for value in gamma_rows]
    alphas = [float(value) for value in alpha_rows]
    maximum = min(len(gammas), len(alphas)) - 1
    if not 1 <= cutoff_count <= maximum:
        raise ValueError(f"cutoff_count must lie in [1,{maximum}]")
    cutoff = gammas[cutoff_count]
    weights = []
    for gamma, alpha in zip(gammas[:cutoff_count], alphas[:cutoff_count]):
        u = gamma / cutoff
        kernel = (1.0 - u) * math.cos(math.pi * u) + math.sin(math.pi * u) / math.pi
        weights.append(2.0 * alpha * kernel)
    return sorted(weights, reverse=True)


def factor(n: int) -> float:
    if n <= 0:
        return 0.0
    return math.cos(math.pi / (n + 2))


def uniform_scan(weights: list[float], target: float, max_n: int, max_m: int):
    prefix = [0.0]
    for value in weights[:max_m]:
        prefix.append(prefix[-1] + value)
    rows = []
    for n in range(1, max_n + 1):
        f = factor(n)
        required = target / f
        lo, hi = 1, min(max_m, len(weights))
        if prefix[hi] < required:
            continue
        while lo < hi:
            mid = (lo + hi) // 2
            if prefix[mid] >= required:
                hi = mid
            else:
                lo = mid + 1
        m = lo
        bound = prefix[m] * f
        h_box = m * math.log10(2 * n + 1)
        l2_n = n * math.sqrt(m)
        rms_n = float(n)
        gh_digits = m * math.log10(rms_n * math.sqrt(2.0 * math.pi * math.e))
        rows.append({
            "m": m,
            "N": n,
            "A_m": prefix[m],
            "bound": bound,
            "margin": bound - target,
            "H_box_digits": h_box,
            "GH_sphere_digits": gh_digits,
            "sum_N": m * n,
            "l2_N": l2_n,
            "rms_N": rms_n,
            "balanced_last_to_coeff_ratio": 2.0 / math.sqrt(m * (m - 1)),
            "dimension": m,
            "runtime_proxy_p2": (m ** 5) * (h_box ** 2),
            "runtime_proxy_p3": (m ** 5) * (h_box ** 3),
            "sphere_runtime_proxy_p2": (m ** 5) * (gh_digits ** 2),
            "sphere_runtime_proxy_p3": (m ** 5) * (gh_digits ** 3),
        })
    rows.sort(key=lambda row: row["H_box_digits"])
    return rows


def marginal(weight: float, n: int):
    """Increment N=n -> n+1, returning contribution gain and box-log cost."""
    gain = weight * (factor(n + 1) - factor(n))
    cost = math.log10(2 * (n + 1) + 1) - (math.log10(2 * n + 1) if n else 0.0)
    return gain, cost


def greedy_anisotropic(weights: list[float], target: float, max_active: int, max_n: int,
                       activation_penalty: float = 0.0):
    """Greedy separable design by marginal gain per effective cost.

    activation_penalty is added only when a coordinate changes 0 -> 1.  Scanning
    it produces a Pareto family trading coefficient entropy against dimension.
    """
    count = min(max_active, len(weights))
    levels = [0] * count
    contribution = 0.0
    h_box = 0.0
    effective_cost = 0.0
    heap = []

    def push(i: int):
        n = levels[i]
        if n >= max_n:
            return
        gain, cost = marginal(weights[i], n)
        charged = cost + (activation_penalty if n == 0 else 0.0)
        if gain > 0 and charged > 0:
            heapq.heappush(heap, (-gain / charged, i, n, gain, cost, charged))

    for i in range(count):
        push(i)

    steps = 0
    while contribution < target and heap:
        _, i, expected_n, gain, cost, charged = heapq.heappop(heap)
        if levels[i] != expected_n:
            continue
        levels[i] += 1
        contribution += gain
        h_box += cost
        effective_cost += charged
        steps += 1
        push(i)

    active = [n for n in levels if n > 0]
    if contribution < target:
        return None
    distribution = Counter(active)
    m_active = len(active)
    sum_n = sum(active)
    l2_n = math.sqrt(sum(n * n for n in active))
    rms_n = l2_n / math.sqrt(m_active)
    gh_digits = m_active * math.log10(rms_n * math.sqrt(2.0 * math.pi * math.e))
    balanced_ratio = l2_n / (0.5 * sum_n * math.sqrt(m_active - 1)) if m_active > 1 else 1.0
    return {
        "target": target,
        "bound": contribution,
        "margin": contribution - target,
        "m": m_active,
        "max_N": max(active),
        "mean_N": sum_n / m_active,
        "sum_N": sum_n,
        "l2_N": l2_n,
        "rms_N": rms_n,
        "H_box_digits": h_box,
        "GH_sphere_digits": gh_digits,
        "balanced_last_to_coeff_ratio": balanced_ratio,
        "activation_penalty": activation_penalty,
        "effective_cost": effective_cost,
        "steps": steps,
        "N_distribution": {str(key): value for key, value in sorted(distribution.items())},
        "runtime_proxy_p2": (m_active ** 5) * (h_box ** 2),
        "runtime_proxy_p3": (m_active ** 5) * (h_box ** 3),
        "sphere_runtime_proxy_p2": (m_active ** 5) * (gh_digits ** 2),
        "sphere_runtime_proxy_p3": (m_active ** 5) * (gh_digits ** 3),
    }


def fixed_m_greedy(weights: list[float], target: float, m: int, max_n: int):
    """Greedy anisotropic design with exactly the top m weights active."""
    if m < 1 or m > len(weights):
        return None
    active_weights = weights[:m]
    levels = [1] * m
    contribution = sum(weight * factor(1) for weight in active_weights)
    h_box = m * math.log10(3)
    heap = []

    def push(i: int):
        n = levels[i]
        if n >= max_n:
            return
        gain, cost = marginal(active_weights[i], n)
        if gain > 0 and cost > 0:
            heapq.heappush(heap, (-gain / cost, i, n, gain, cost))

    for i in range(m):
        push(i)
    while contribution < target and heap:
        _, i, expected_n, gain, cost = heapq.heappop(heap)
        if levels[i] != expected_n:
            continue
        levels[i] += 1
        contribution += gain
        h_box += cost
        push(i)
    if contribution < target:
        return None
    sum_n = sum(levels)
    l2_n = math.sqrt(sum(n * n for n in levels))
    rms_n = l2_n / math.sqrt(m)
    gh_digits = m * math.log10(rms_n * math.sqrt(2.0 * math.pi * math.e))
    distribution = Counter(levels)
    return {
        "m": m,
        "bound": contribution,
        "margin": contribution - target,
        "max_N": max(levels),
        "mean_N": sum_n / m,
        "sum_N": sum_n,
        "l2_N": l2_n,
        "rms_N": rms_n,
        "H_box_digits": h_box,
        "GH_sphere_digits": gh_digits,
        "balanced_last_to_coeff_ratio": l2_n / (0.5 * sum_n * math.sqrt(m - 1)) if m > 1 else 1.0,
        "N_distribution": {str(key): value for key, value in sorted(distribution.items())},
        "runtime_proxy_p2": (m ** 5) * (h_box ** 2),
        "runtime_proxy_p3": (m ** 5) * (h_box ** 3),
        "sphere_runtime_proxy_p2": (m ** 5) * (gh_digits ** 2),
        "sphere_runtime_proxy_p3": (m ** 5) * (gh_digits ** 3),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=float, default=1.826054)
    parser.add_argument("--margin", type=float, default=0.0)
    parser.add_argument("--max-m", type=int, default=1500)
    parser.add_argument("--max-n", type=int, default=128)
    parser.add_argument("--cutoff-count", type=int, default=config.NEV,
                        help="use gamma_(cutoff_count+1) as kernel cutoff")
    parser.add_argument("--output", default="work/model/extremal_design_scan.json")
    args = parser.parse_args()
    target = args.target + args.margin
    weights = load_weights(args.cutoff_count)

    uniform = uniform_scan(weights, target, args.max_n, args.max_m)
    penalties = [0.0] + [0.025 * i for i in range(1, 41)] + [1.25, 1.5, 2.0, 3.0, 4.0]
    anisotropic = []
    for penalty in penalties:
        row = greedy_anisotropic(weights, target, args.max_m, args.max_n, penalty)
        if row is not None:
            anisotropic.append(row)

    fixed_m = []
    for m in range(580, min(args.max_m, 1000) + 1):
        row = fixed_m_greedy(weights, target, m, args.max_n)
        if row is not None:
            fixed_m.append(row)

    payload = {
        "schema": 1,
        "target_base": args.target,
        "target_used": target,
        "margin_requested": args.margin,
        "cutoff_count": args.cutoff_count,
        "weights_count": len(weights),
        "weight_sum": sum(weights),
        "uniform_best_by_box": uniform[:20],
        "uniform_best_by_gh_sphere": sorted(uniform, key=lambda row: row["GH_sphere_digits"])[:20],
        "uniform_best_by_runtime_p2": sorted(uniform, key=lambda row: row["runtime_proxy_p2"])[:20],
        "uniform_best_by_runtime_p3": sorted(uniform, key=lambda row: row["runtime_proxy_p3"])[:20],
        "uniform_best_by_sphere_runtime_p2": sorted(uniform, key=lambda row: row["sphere_runtime_proxy_p2"])[:20],
        "uniform_best_by_sphere_runtime_p3": sorted(uniform, key=lambda row: row["sphere_runtime_proxy_p3"])[:20],
        "anisotropic_pareto_samples": anisotropic,
        "anisotropic_best_by_box": sorted(anisotropic, key=lambda row: row["H_box_digits"])[:20],
        "anisotropic_best_by_runtime_p2": sorted(anisotropic, key=lambda row: row["runtime_proxy_p2"])[:20],
        "anisotropic_best_by_sphere_runtime_p2": sorted(anisotropic, key=lambda row: row["sphere_runtime_proxy_p2"])[:20],
        "fixed_m_best_by_box": sorted(fixed_m, key=lambda row: row["H_box_digits"])[:30],
        "fixed_m_best_by_runtime_p2": sorted(fixed_m, key=lambda row: row["runtime_proxy_p2"])[:30],
        "fixed_m_best_by_sphere_runtime_p2": sorted(fixed_m, key=lambda row: row["sphere_runtime_proxy_p2"])[:30],
    }
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    util.atomic_write_json(args.output, payload)

    print(f"[EXTREMAL-SCAN] target={target:.9f} total_weight={sum(weights):.9f}")
    if uniform:
        best = uniform[0]
        runtime_best = min(uniform, key=lambda row: row["runtime_proxy_p2"])
        sphere_best = min(uniform, key=lambda row: row["sphere_runtime_proxy_p2"])
        print(
            "[EXTREMAL-SCAN] uniform box-opt "
            f"m={best['m']} N={best['N']} H={best['H_box_digits']:.2f} "
            f"GH={best['GH_sphere_digits']:.2f} bound={best['bound']:.9f}"
        )
        print(
            "[EXTREMAL-SCAN] uniform runtime-opt "
            f"box:m={runtime_best['m']} N={runtime_best['N']} H={runtime_best['H_box_digits']:.2f}; "
            f"sphere:m={sphere_best['m']} N={sphere_best['N']} GH={sphere_best['GH_sphere_digits']:.2f}"
        )
    if anisotropic:
        for label, row in (
            ("box", min(anisotropic, key=lambda item: item["H_box_digits"])),
            ("runtime", min(anisotropic, key=lambda item: item["runtime_proxy_p2"])),
            ("sphere", min(anisotropic, key=lambda item: item["sphere_runtime_proxy_p2"])),
        ):
            print(
                f"[EXTREMAL-SCAN] anisotropic-{label} m={row['m']} "
                f"H={row['H_box_digits']:.2f} GH={row['GH_sphere_digits']:.2f} "
                f"rmsN={row['rms_N']:.2f} maxN={row['max_N']}"
            )
    if fixed_m:
        for label, row in (
            ("box", min(fixed_m, key=lambda item: item["H_box_digits"])),
            ("runtime", min(fixed_m, key=lambda item: item["runtime_proxy_p2"])),
            ("sphere", min(fixed_m, key=lambda item: item["sphere_runtime_proxy_p2"])),
        ):
            print(
                f"[EXTREMAL-SCAN] fixed-m-{label} m={row['m']} "
                f"H={row['H_box_digits']:.2f} GH={row['GH_sphere_digits']:.2f} "
                f"rmsN={row['rms_N']:.2f} maxN={row['max_N']} "
                f"bound={row['bound']:.9f} margin={row['margin']:.2e} "
                f"dist={row['N_distribution']}"
            )
    print(f"[EXTREMAL-SCAN] wrote {args.output}")


if __name__ == "__main__":
    main()
