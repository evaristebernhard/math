#!/usr/bin/env python3
"""步骤 04: 多 checkpoint、多核、确定性的柱候选搜索。"""
from __future__ import annotations

import argparse
import json
import math
import multiprocessing
import os
import random
import time
from dataclasses import asdict, dataclass

import mpmath as mp
import numpy as np

import config
import reduction
import util


# fork worker 共享的只读状态；所有 map 都保持输入顺序。
G = {}


@dataclass
class DecodeResult:
    path: str
    f64_cy: int | None
    hp_cy: int | None
    enum_cys: list[int]
    directions: list[int]
    float_type: str | None
    messages: list[str]
    seconds: float


def ordered_map(function, values, jobs, chunksize=1):
    values = list(values)
    if jobs == 1 or len(values) <= 1:
        return [function(value) for value in values]
    with multiprocessing.get_context("fork").Pool(min(jobs, len(values))) as pool:
        return list(pool.imap(function, values, chunksize=max(1, chunksize)))


def load_basis(path):
    d = G["d"]
    # fplll 输出的行序就是 Babai/GSO 的生产顺序。范数排序会破坏约化基的
    # 三角结构，只允许由 s06_decoder_audit.py 显式复现。
    return util.read_fplll_matrix(path, d)


def cy_from_coefficients(coefficients, basis):
    n = G["n"]
    return sum(int(coefficients[i]) * basis[i][n] for i in range(G["d"]))


def f64_babai(basis):
    d, nu, target = G["d"], G["NU"], G["target"]
    top = max(max(abs(x).bit_length() for x in basis[-1]), nu + 10)
    scale = 2.0 ** -(top - 40)
    bf = np.array([[float(x) * scale for x in row] for row in basis])
    tf = np.array([float(x) * scale for x in target])
    gs = np.zeros_like(bf)
    for i in range(d):
        vector = bf[i].copy()
        for j in range(i):
            denominator = np.dot(gs[j], gs[j])
            if not np.isfinite(denominator) or denominator == 0:
                raise ArithmeticError(f"float64 GS breakdown {i}/{j}")
            vector -= np.dot(bf[i], gs[j]) / denominator * gs[j]
        gs[i] = vector
    residual = tf.copy()
    coefficients = [0] * d
    for i in range(d - 1, -1, -1):
        denominator = np.dot(gs[i], gs[i])
        if not np.isfinite(denominator) or denominator == 0:
            raise ArithmeticError(f"float64 Babai breakdown {i}")
        coefficient = round(float(np.dot(residual, gs[i]) / denominator))
        coefficients[i] = coefficient
        residual -= coefficient * bf[i]
    return coefficients


def normalised_radius(diff, inflate=1.01):
    radius = sum(x * x for x in diff)
    exponent = max(0, radius.bit_length() - 50)
    return float(radius / (1 << exponent)) * inflate, exponent


def decode_basis(path):
    started = time.time()
    basis = load_basis(path)
    d, n, target = G["d"], G["n"], G["target"]
    directions = [row[n] for row in basis if row[n] != 0][:G["direction_pool"]]
    messages, enum_cys = [], []
    try:
        f64_cy = cy_from_coefficients(f64_babai(basis), basis)
    except Exception as exc:
        f64_cy = None
        messages.append(f"float64={type(exc).__name__}: {exc}")
    hp_cy, float_type = None, None
    try:
        from fpylll import Enumeration, FPLLL, GSO, IntegerMatrix

        FPLLL.set_precision(G["mpfr_bits"])
        FPLLL.set_threads(1)
        integer_matrix = IntegerMatrix.from_matrix(basis)
        errors, matrix = [], None
        # canonical target is always passed directly to MatGSO.babai.
        for candidate_type in ("mpfr", "dpe", "long double", "double"):
            try:
                candidate = GSO.Mat(integer_matrix, float_type=candidate_type)
                candidate.update_gso()
                matrix, float_type = candidate, candidate_type
                break
            except Exception as exc:
                errors.append(f"{candidate_type}:{type(exc).__name__}")
        if matrix is None:
            raise RuntimeError("GSO fallback chain failed: " + ", ".join(errors))
        if errors:
            messages.append("GSO fallbacks: " + ", ".join(errors))
        coefficients = [int(x) for x in matrix.babai(tuple(target))]
        hp_cy = cy_from_coefficients(coefficients, basis)

        tail_dim = min(G["tail_dim"], d)
        if tail_dim > 0 and G["tail_solutions"] > 0:
            # 所有维度都只枚举尾块；全维 Enumeration 会给 validate 也
            # 带来不可控长尾，且违背固定 12 维尾枚举的吞吐约束。
            first = d - tail_dim
            head = coefficients[:first] + [0] * (d - first)
            head_point = [
                sum(head[i] * basis[i][j] for i in range(d)) for j in range(d)
            ]
            residual = [target[j] - head_point[j] for j in range(d)]
            block_coefficients = [
                int(x) for x in matrix.babai(
                    tuple(residual), start=first, dimension=d - first
                )
            ]
            block_point = [
                sum(block_coefficients[i] * basis[first + i][j]
                    for i in range(d - first))
                for j in range(d)
            ]
            mantissa, exponent = normalised_radius(
                [residual[j] - block_point[j] for j in range(d)], 1.01
            )
            target_gso = matrix.from_canonical(tuple(residual))
            enumeration = Enumeration(matrix, nr_solutions=G["tail_solutions"])
            for _, solution in enumeration.enumerate(
                first, d, mantissa, exponent, target=target_gso
            ):
                full = head[:]
                full[first:] = [int(round(x)) for x in solution]
                enum_cys.append(cy_from_coefficients(full, basis))
    except Exception as exc:
        messages.append(f"high-precision={type(exc).__name__}: {exc}")
    return DecodeResult(path, f64_cy, hp_cy, enum_cys, directions, float_type,
                        messages, time.time() - started)


def heavy_score(cy):
    y = mp.mpf(cy) / G["two_nuy"]
    return sum(
        weight * math.cos(float(mp.fmod(gamma * y - phase, G["twopi"])))
        for gamma, phase, weight in zip(G["gH"], G["pH"], G["wH"])
    )


def full_score(cy):
    y = mp.mpf(cy) / G["two_nuy"]
    return sum(
        G["w"][k] * math.cos(float(mp.fmod(
            G["gAll"][k] * y - float(G["bf"][k]), G["twopi"]
        )))
        for k in range(G["NEV"])
    )


def direction_gain(task):
    anchor, dcy = task
    base = heavy_score(anchor)
    return max(heavy_score(anchor + dcy), heavy_score(anchor - dcy)) - base


def ap_scan(task):
    cy, dcy, keep = task
    y, dy = mp.mpf(cy) / G["two_nuy"], mp.mpf(dcy) / G["two_nuy"]
    theta = np.array(
        [float(mp.fmod(gamma * y, G["twopi"])) for gamma in G["gM"]]
    ) - G["pM"]
    delta = np.array(
        [float(mp.fmod(gamma * dy, G["twopi"])) for gamma in G["gM"]]
    )
    grid = G["J"]
    values = (
        G["wM"][:, None]
        * np.cos(theta[:, None] + delta[:, None] * grid[None, :])
    ).sum(axis=0)
    keep = min(keep, len(values))
    indices = np.argpartition(values, -keep)[-keep:]
    indices = indices[np.argsort(-values[indices])]
    return [(float(values[i]), cy + int(grid[i]) * dcy) for i in indices]


def exact_full_score(cy, dps):
    """独立 dps 重算；不复用 float64 权重或相位。"""
    # 结果精度为 dps；gamma*y 的约简还必须覆盖 y 的整数数量级。
    with mp.workdps(dps + len(str(abs(int(cy)))) + 40):
        y = mp.mpf(cy) / mp.power(2, G["NUY"])
        gamma = [mp.mpf(value) for value in G["gstr"]]
        alpha = [mp.mpf(value) for value in G["A"]]
        phase = [mp.mpf(value) for value in G["Bt"]]
        T = gamma[G["NEV"]]
        total = mp.mpf("0")
        for k in range(G["NEV"]):
            u = gamma[k] / T
            kernel = (1-u) * mp.cos(mp.pi*u) + mp.sin(mp.pi*u) / mp.pi
            total += 2 * alpha[k] * kernel * mp.cos(gamma[k]*y-phase[k])
        return +total


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=sorted(config.STAGES))
    parser.add_argument("basis", nargs="*")
    parser.add_argument("--mode", choices=("anchor", "pilot", "full"), default="full")
    parser.add_argument("--jobs", type=int, default=config.NPROC)
    parser.add_argument("--seed", type=int, default=97)
    parser.add_argument("--output")
    parser.add_argument("--meta")
    parser.add_argument("--mpfr-bits", type=int, default=384)
    parser.add_argument("--tail-dim", type=int, default=12)
    parser.add_argument("--tail-solutions", type=int, default=128)
    parser.add_argument("--verify-dps", default="100,160")
    return parser.parse_args()


def main():
    args = parse_args()
    started = time.time()
    cfg = config.STAGES[args.stage]
    meta_path = args.meta or f"{config.WORK_DIR}/{args.stage}_meta.json"
    meta = json.load(open(meta_path, encoding="utf-8"))
    redpaths = args.basis or [f"{config.WORK_DIR}/{args.stage}_lll.txt"]
    mode = dict(config.SEARCH_MODES[args.mode])
    jobs = max(1, min(args.jobs, len(util.physical_cpu_ids(reserve=0))))
    n, d = int(meta["mH"]), int(meta["mH"]) + 1
    if any(not util.validate_fplll_matrix(path, d) for path in redpaths):
        raise SystemExit("至少一个 checkpoint 与 meta 维度不符或被截断")

    gstr = util.load_gamma_strings(cfg, args.stage)
    A = util.read_lines(os.path.join(config.DATA_DIR, "alpha.txt"))
    Bt = util.read_lines(os.path.join(config.DATA_DIR, "beta.txt"))
    NEV, NU, NUY = int(meta["NEV"]), int(meta["NU"]), int(meta["NUY"])
    gf = np.array([float(value) for value in gstr])
    af = np.array([float(value) for value in A[:NEV+1]])
    bf = np.array([float(value) for value in Bt[:NEV+1]])
    w, _ = util.build_weights(gf, af, NEV)
    order = np.argsort(-w)
    H = meta["H"]
    mid = np.sort(order[:config.N_MID])
    mp.mp.dps = int(NU * 0.302) + 60
    G.update({
        "n": n, "d": d, "NU": NU, "NUY": NUY, "NEV": NEV,
        "target": [int(x) for x in meta["tvec"]],
        "mpfr_bits": args.mpfr_bits, "tail_dim": args.tail_dim,
        "tail_solutions": 0 if args.mode == "anchor" else args.tail_solutions,
        "direction_pool": max(32, config.N_DELTA * 2),
        "two_nuy": mp.mpf(2) ** NUY, "twopi": 2 * mp.pi,
        "gH": [mp.mpf(gstr[k]) for k in H],
        "pH": [float(bf[k]) for k in H], "wH": [float(w[k]) for k in H],
        "gM": [mp.mpf(gstr[k]) for k in mid], "pM": bf[mid], "wM": w[mid],
        "gAll": [mp.mpf(value) for value in gstr[:NEV]],
        "w": w, "bf": bf, "gstr": gstr, "A": A, "Bt": Bt,
    })
    AH = float(meta["AH"])

    def log(*values):
        print(f"[04 {time.time()-started:7.1f}s]", *values, flush=True)

    log(f"stage={args.stage} mode={args.mode} dim={d} "
        f"checkpoints={len(redpaths)} jobs={jobs} seed={args.seed}")
    decoded = ordered_map(decode_basis, redpaths, min(jobs, len(redpaths)))
    by_source, candidates = {}, set()
    random_source = random.Random(args.seed)
    diagnostic = []
    for result in decoded:
        anchors = [cy for cy in (result.f64_cy, result.hp_cy) if cy not in (None, 0)]
        anchors += [cy for cy in result.enum_cys if cy]
        diagnostic += anchors[:2]
        local = set(anchors)
        if anchors and result.directions:
            for anchor in anchors[:2]:
                for dcy in result.directions[:16]:
                    for coefficient in (-6, -3, -1, 1, 3, 6):
                        local.add(anchor + coefficient*dcy)
            while len(local) < mode["n_bases"]:
                cy = random_source.choice(anchors[:2] or anchors)
                for _ in range(random_source.choice((1, 2, 2, 3, 4))):
                    cy += random_source.choice((-3, -2, -1, 1, 2, 3)) \
                          * random_source.choice(result.directions)
                if cy:
                    local.add(cy)
        candidates.update(local)
        by_source[result.path] = result.directions

    diagnostic_scores = dict(zip(
        diagnostic, ordered_map(heavy_score, diagnostic, jobs)
    ))
    for result in decoded:
        log(f"decoder {os.path.basename(result.path)}: "
            f"f64={diagnostic_scores.get(result.f64_cy, float('nan')):.4f} "
            f"hp={diagnostic_scores.get(result.hp_cy, float('nan')):.4f} "
            f"({result.float_type or 'FAILED'}) tail={len(result.enum_cys)}")
        for message in result.messages:
            log(" ", message)
    candidate_list = sorted(candidates)
    values = ordered_map(heavy_score, candidate_list, jobs,
                         max(1, len(candidate_list)//max(1, jobs*8)))
    scored = sorted(zip(values, candidate_list), reverse=True)
    if not scored:
        raise SystemExit("所有 checkpoint 解码均失败")
    log(f"heavy best={scored[0][0]:.6f}/A_H={AH:.6f}="
        f"{100*scored[0][0]/AH:.1f}%")

    # 方向按“来源多样性 + 对当前重块锚点的实际增益”选，不按 abs(dcy)。
    best_anchor = scored[0][1]
    per_source_ranked = []
    for source, source_directions in by_source.items():
        unique = list(dict.fromkeys(source_directions))
        gains = ordered_map(direction_gain, [(best_anchor, d) for d in unique], jobs)
        ranked = sorted(zip(gains, unique), reverse=True)
        per_source_ranked.append((source, ranked))
    chosen, seen = [], set()
    # 首先保留每个 checkpoint 的最佳方向，再按实际 gain 全局补足。
    for source, ranked in per_source_ranked:
        if ranked and ranked[0][1] not in seen:
            seen.add(ranked[0][1])
            chosen.append(ranked[0][1])
    remaining = [
        (gain, dcy, source)
        for source, ranked in per_source_ranked
        for gain, dcy in ranked[1:]
    ]
    for gain, dcy, source in sorted(remaining, reverse=True):
        if dcy and dcy not in seen:
            seen.add(dcy)
            chosen.append(dcy)
    directions = chosen[:max(config.N_DELTA, 16)]
    log(f"base candidates={len(candidate_list)} selected directions={len(directions)}")

    output_path = args.output or f"{config.WORK_DIR}/{args.stage}_results.json"
    common = {
        "stage": args.stage, "mode": args.mode, "seed": args.seed, "jobs": jobs,
        "meta": meta_path, "meta_sha256": util.sha256_file(meta_path),
        "checkpoints": [{"path": path, "sha256": util.sha256_file(path)}
                        for path in redpaths],
        "decoder": {"mpfr_bits": args.mpfr_bits, "tail_dim": args.tail_dim,
                    "tail_solutions": args.tail_solutions,
                    "basis_order": "fplll_original"},
        "h_H": float(scored[0][0]), "A_H": AH,
        "anchor_cy": str(scored[0][1]), "NUY": NUY,
        "decoders": [asdict(result) for result in decoded],
    }
    if args.mode == "anchor":
        common.update({"h": float(scored[0][0]),
                       "y_exact_num": str(scored[0][1]),
                       "y": mp.nstr(mp.mpf(scored[0][1])/G["two_nuy"], 40)})
        util.atomic_write_json(output_path, common)
        log(f"anchor -> {output_path}")
        return
    if not directions:
        raise SystemExit("没有非零 Y 方向可供 AP 搜索")

    top_count = min(mode["top_bases"], len(scored))
    direction_count = min(16, len(directions))
    projected_tasks = top_count * direction_count \
        + mode["ap2_seeds"] * direction_count
    ap_j = mode["ap_j"]
    if projected_tasks:
        required_width = math.ceil(mode["min_ap_evals"] / projected_tasks)
        ap_j = max(ap_j, math.ceil((required_width - 1) / 2))
    G["J"] = np.arange(-ap_j, ap_j + 1, dtype=np.int64)

    pass1_tasks = [
        (cy, dcy, 6) for _, cy in scored[:top_count]
        for dcy in directions[:direction_count]
    ]
    pass1 = [
        item for group in ordered_map(ap_scan, pass1_tasks, jobs)
        for item in group
    ]
    pass1.sort(reverse=True)
    seeds, seed_seen = [], set()
    for score, cy in pass1:
        if cy not in seed_seen:
            seed_seen.add(cy)
            seeds.append((score, cy))
            if len(seeds) >= mode["ap2_seeds"]:
                break
    pass2_tasks = [
        (cy, dcy, 3) for _, cy in seeds
        for dcy in directions[:direction_count]
    ]
    pass2 = [
        item for group in ordered_map(ap_scan, pass2_tasks, jobs)
        for item in group
    ]
    ap_candidates = sorted(pass1 + pass2, reverse=True)
    unique = {}
    for score, cy in ap_candidates:
        unique.setdefault(cy, score)
    tested = (len(pass1_tasks)+len(pass2_tasks)) * len(G["J"])
    if args.mode == "full" and tested < 4_000_000:
        raise RuntimeError(f"full AP 预算不足: {tested:,} < 4,000,000")
    log(f"2D AP best_mid={ap_candidates[0][0]:.6f} tested={tested:,} "
        f"unique={len(unique):,}")

    full_count = min(len(unique), max(mode["finalists"]*4, mode["finalists"]))
    full_input = list(unique)[:full_count]
    full_values = ordered_map(full_score, full_input, jobs,
                              max(1, full_count//max(1, jobs*4)))
    finalists = sorted(zip(full_values, full_input), reverse=True)
    polish_input = list(dict.fromkeys(
        cy+offset for _, cy in finalists[:mode["finalists"]]
        for offset in range(-2, 3)
    ))
    polish_values = ordered_map(full_score, polish_input, jobs,
                                max(1, len(polish_input)//max(1, jobs*4)))
    polished = sorted(zip(polish_values, polish_input), reverse=True)
    float_h, cy_best = polished[0]

    verification = None
    if args.mode == "full":
        dps_values = [int(value) for value in args.verify_dps.split(",") if value]
        if len(dps_values) < 2:
            raise SystemExit("--verify-dps 至少需要两个精度，例如 100,160")
        exact_values = [exact_full_score(cy_best, dps) for dps in dps_values]
        difference = abs(exact_values[-1] - exact_values[-2])
        verification = {
            "dps": dps_values,
            "values": [mp.nstr(value, dps) for value, dps in zip(exact_values, dps_values)],
            "difference": mp.nstr(difference, 30),
            "passed_1e_20": bool(difference < mp.mpf("1e-20")),
            "y_exact_num": str(cy_best),
            "NUY": NUY,
        }
        final_h = exact_values[-1]
    else:
        final_h = mp.mpf(float_h)
    hH = heavy_score(cy_best)
    y_best = mp.mpf(cy_best) / G["two_nuy"]
    log(f"full top5={[round(value, 6) for value, _ in polished[:5]]}")
    log(f"RESULT h={mp.nstr(final_h, 15)} h_H={hH:.6f} "
        f"harvest={float(final_h)-hH:+.6f}")
    common.update({
        "h": float(final_h), "h_float64": float(float_h),
        "y": mp.nstr(y_best, mp.mp.dps), "y_exact_num": str(cy_best),
        "h_H": float(hH), "M_tested": tested, "M_kept": len(unique),
        "verification": verification,
        "parity": (
            "VERIFIED" if verification and verification["passed_1e_20"]
            else "UNVERIFIED"
        ),
        "numerical_breakthrough": bool(final_h > mp.mpf(str(cfg["target"]))),
        "finalists": [
            [float(value), str(cy), mp.nstr(mp.mpf(cy)/G["two_nuy"], 40)]
            for value, cy in polished[:mode["finalists"]]
        ],
    })
    util.atomic_write_json(output_path, common)
    log(f"saved -> {output_path}")


if __name__ == "__main__":
    main()
