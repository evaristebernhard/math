"""Decoder/Babai 审计的共享实现。

生产路径保持 fplll 的原始行序；范数排序只在显式审计中复现旧行为。
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass

import mpmath as mp

import config
import util


@dataclass
class BabaiCandidate:
    order: str
    backend: str
    cy: int | None
    error: str | None = None


def ordered_basis(path: str, dim: int, order: str = "original") -> list[list[int]]:
    rows = util.read_fplll_matrix(path, dim)
    if order == "norm":
        rows.sort(key=lambda row: sum(x*x for x in row))
    elif order != "original":
        raise ValueError(f"unknown basis order: {order}")
    return rows


def _cy(coefficients, rows, y_column):
    return sum(int(coefficients[i]) * rows[i][y_column]
               for i in range(len(rows)))


def mpfr_babai(path, meta, order="original", bits=384) -> BabaiCandidate:
    try:
        from fpylll import FPLLL, GSO, IntegerMatrix

        dim = int(meta["mH"]) + 1
        rows = ordered_basis(path, dim, order)
        FPLLL.set_precision(bits)
        FPLLL.set_threads(1)
        matrix = IntegerMatrix.from_matrix(rows)
        gso = GSO.Mat(matrix, float_type="mpfr")
        if not gso.update_gso():
            raise ArithmeticError("MPFR GSO update failed")
        coefficients = [int(x) for x in gso.babai(
            tuple(int(x) for x in meta["tvec"])
        )]
        return BabaiCandidate(order, f"mpfr-{bits}",
                              _cy(coefficients, rows, dim-1))
    except Exception as exc:
        return BabaiCandidate(order, f"mpfr-{bits}", None,
                              f"{type(exc).__name__}: {exc}")


def float64_babai(path, meta, order="original") -> BabaiCandidate:
    """诊断用的经典 GS/Babai；结果不得用于 gate。"""
    try:
        import numpy as np

        dim = int(meta["mH"]) + 1
        rows = ordered_basis(path, dim, order)
        target = [int(x) for x in meta["tvec"]]
        top = max(max(abs(x).bit_length() for row in rows for x in row),
                  int(meta["NU"]) + 10)
        scale = 2.0 ** -(top - 40)
        bf = np.asarray([[float(x)*scale for x in row] for row in rows])
        tf = np.asarray([float(x)*scale for x in target])
        gs = np.zeros_like(bf)
        for i in range(dim):
            vector = bf[i].copy()
            for j in range(i):
                denominator = float(np.dot(gs[j], gs[j]))
                if not np.isfinite(denominator) or denominator == 0:
                    raise ArithmeticError(f"float64 GS breakdown {i}/{j}")
                vector -= float(np.dot(bf[i], gs[j])) / denominator * gs[j]
            gs[i] = vector
        residual = tf.copy()
        coefficients = [0] * dim
        for i in range(dim-1, -1, -1):
            denominator = float(np.dot(gs[i], gs[i]))
            if not np.isfinite(denominator) or denominator == 0:
                raise ArithmeticError(f"float64 Babai breakdown {i}")
            coefficients[i] = round(float(np.dot(residual, gs[i])
                                          / denominator))
            residual -= coefficients[i] * bf[i]
        return BabaiCandidate(order, "float64-diagnostic",
                              _cy(coefficients, rows, dim-1))
    except Exception as exc:
        return BabaiCandidate(order, "float64-diagnostic", None,
                              f"{type(exc).__name__}: {exc}")


def load_scoring_inputs(stage: str, meta: dict):
    cfg = dict(config.STAGES[stage])
    gstr = util.load_gamma_strings(cfg, stage)
    alpha = util.read_lines(os.path.join(config.DATA_DIR, "alpha.txt"))
    phase = util.read_lines(os.path.join(config.DATA_DIR, "beta.txt"))
    return gstr, alpha, phase


def canonical_heavy_metrics(cy: int, meta: dict, scoring_inputs, dps: int):
    """从十进制源独立重建权重，并返回重块真余弦与二次损失。"""
    gstr, alpha_text, phase_text = scoring_inputs
    nev, nuy = int(meta["NEV"]), int(meta["NUY"])
    # y≈10^260 时，直接用 100/160 dps 做 gamma*y mod 2π 会把小数相位
    # 全部吃掉。canonical scorer 的“100/160 位”指结果精度；参数约简必须
    # 加上 y 的十进制数量级作为 guard digits。两个 scorer 各自从十进制源
    # 重建并独立约简，不能共享低精度 theta。
    guard_dps = dps + len(str(abs(cy))) + 40
    with mp.workdps(guard_dps):
        gamma = [mp.mpf(value) for value in gstr]
        alpha = [mp.mpf(value) for value in alpha_text]
        phase = [mp.mpf(value) for value in phase_text]
        T = gamma[nev]
        y = mp.mpf(cy) / mp.power(2, nuy)
        h_h = mp.mpf("0")
        a_h = mp.mpf("0")
        q = mp.mpf("0")
        for k in meta["H"]:
            u = gamma[k] / T
            kernel = (1-u)*mp.cos(mp.pi*u) + mp.sin(mp.pi*u)/mp.pi
            weight = 2*alpha[k]*kernel
            theta = mp.fmod(gamma[k]*y-phase[k]+mp.pi, 2*mp.pi)
            if theta < 0:
                theta += 2*mp.pi
            theta -= mp.pi
            a_h += weight
            h_h += weight*mp.cos(theta)
            q += weight*theta*theta/2
        ideal_loss = a_h - mp.mpf(str(meta["LH_pred"]))
        true_loss = a_h - h_h
        rho = mp.sqrt(true_loss/ideal_loss) if ideal_loss > 0 else mp.nan
        return {
            "result_dps": dps, "argument_reduction_dps": guard_dps,
            "h_H": mp.nstr(h_h, dps),
            "A_H": mp.nstr(a_h, dps),
            "efficiency": mp.nstr(h_h/a_h, dps),
            "Q": mp.nstr(q, dps),
            "true_cosine_loss": mp.nstr(true_loss, dps),
            "proxy_error_Q_minus_true": mp.nstr(q-true_loss, dps),
            "rho": mp.nstr(rho, dps),
        }


def audit_candidate(candidate, meta, scoring_inputs, dps_values=(100, 160)):
    row = {
        "order": candidate.order, "backend": candidate.backend,
        "diagnostic_only": candidate.backend.startswith("float64"),
        "error": candidate.error,
    }
    if candidate.cy is None:
        row.update({"cy": None, "parity": "UNVERIFIED"})
        return row
    nuy = int(meta["NUY"])
    scores = [
        canonical_heavy_metrics(candidate.cy, meta, scoring_inputs, dps)
        for dps in dps_values
    ]
    with mp.workdps(max(dps_values)+20):
        difference = abs(mp.mpf(scores[-1]["h_H"])
                         - mp.mpf(scores[-2]["h_H"]))
    row.update({
        "cy": str(candidate.cy),
        "y_exact": {"numerator": str(candidate.cy),
                    "denominator": str(1 << nuy)},
        "y_decimal": mp.nstr(mp.mpf(candidate.cy)/(1 << nuy), 50),
        "scorer": {"dps": list(dps_values), "runs": scores,
                   "h_H_difference": mp.nstr(difference, 30)},
        "metrics": scores[-1],
        "parity": "VERIFIED" if difference < mp.mpf("1e-20") else "BROKEN",
    })
    return row


def canonical_full_score(cy, meta, scoring_inputs, dps):
    """独立十进制源的全 NEV scorer，带大 y 参数约简 guard。"""
    gstr, alpha_text, phase_text = scoring_inputs
    nev, nuy = int(meta["NEV"]), int(meta["NUY"])
    guard_dps = dps + len(str(abs(int(cy)))) + 40
    with mp.workdps(guard_dps):
        gamma = [mp.mpf(value) for value in gstr]
        alpha = [mp.mpf(value) for value in alpha_text]
        phase = [mp.mpf(value) for value in phase_text]
        T = gamma[nev]
        y = mp.mpf(cy)/mp.power(2, nuy)
        total = mp.mpf("0")
        for k in range(nev):
            u = gamma[k]/T
            kernel = (1-u)*mp.cos(mp.pi*u) + mp.sin(mp.pi*u)/mp.pi
            total += 2*alpha[k]*kernel*mp.cos(gamma[k]*y-phase[k])
        return {
            "result_dps": dps, "argument_reduction_dps": guard_dps,
            "h": mp.nstr(total, dps),
        }


def canonical_full_parity(cy, meta, scoring_inputs, dps_values=(100, 160)):
    runs = [
        canonical_full_score(cy, meta, scoring_inputs, dps)
        for dps in dps_values
    ]
    with mp.workdps(max(dps_values)+20):
        difference = abs(mp.mpf(runs[-1]["h"])-mp.mpf(runs[-2]["h"]))
    return {
        "cy": str(cy), "NUY": int(meta["NUY"]),
        "dps": list(dps_values), "runs": runs,
        "difference": mp.nstr(difference, 30),
        "parity": "VERIFIED" if difference < mp.mpf("1e-20") else "BROKEN",
    }


def audit_checkpoint(stage, path, meta, bits=384, dps_values=(100, 160)):
    scoring = load_scoring_inputs(stage, meta)
    candidates = []
    for order in ("original", "norm"):
        candidates.append(mpfr_babai(path, meta, order, bits))
        candidates.append(float64_babai(path, meta, order))
    return {
        "stage": stage, "checkpoint": path,
        "checkpoint_sha256": util.sha256_file(path),
        "meta_mH": int(meta["mH"]), "meta_NU": int(meta["NU"]),
        "NUY": int(meta["NUY"]), "LH_ideal": str(meta["LH_pred"]),
        "candidates": [
            audit_candidate(candidate, meta, scoring, dps_values)
            for candidate in candidates
        ],
    }
