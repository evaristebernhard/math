"""理想大偏差、尾部 harvest 与有效预算模型。"""
from __future__ import annotations

import math

import mpmath as mp
import numpy as np

import config
import util


TARGET = 1.6383
HURST_TARGET = 1.826054


def raw_budget(nu):
    return (int(nu)-16)*math.log(2)


def scan_inputs(stage="bt2015"):
    cfg = dict(config.STAGES[stage])
    gstr = util.load_gamma_strings(cfg, stage)
    alpha = util.read_lines(f"{config.DATA_DIR}/alpha.txt")
    gf = np.asarray([float(x) for x in gstr])
    af = np.asarray([float(x) for x in alpha[:config.NEV+1]])
    weights, _ = util.build_weights(gf, af, config.NEV)
    return weights


def normal_max_quantile(sigma, effective_count, probability):
    # P(max <= x)=Phi(x/sigma)^M.
    p_single = mp.power(mp.mpf(str(probability)),
                        mp.mpf(1)/effective_count)
    return float(sigma*mp.sqrt(2)*mp.erfinv(2*p_single-1))


def harvest_summary(tail_variance):
    sigma = math.sqrt(max(0.0, tail_variance))
    result = {}
    for count in (100, 1000, 10000):
        result[str(count)] = {
            "M_eff": count,
            "q10": normal_max_quantile(sigma, count, 0.10),
            "median": normal_max_quantile(sigma, count, 0.50),
            "q90": normal_max_quantile(sigma, count, 0.90),
        }
    return result


def ideal_row(weights, mH, nu, target=TARGET):
    order = np.argsort(-weights)
    H = order[:mH]
    AH = float(weights[H].sum())
    _, LH = util.tilt_prediction([float(weights[k]) for k in H],
                                 raw_budget(nu))
    ideal_loss = AH-LH
    mask = np.ones(len(weights), dtype=bool)
    mask[H] = False
    tail_variance = float(0.5*np.square(weights[mask]).sum())
    harvest = harvest_summary(tail_variance)
    conservative = harvest["1000"]["q10"]
    required_hH = target-conservative
    required_efficiency = required_hH/AH
    rho_required = (
        math.sqrt(max(0.0, (AH-required_hH)/ideal_loss))
        if ideal_loss > 0 and required_hH <= AH else None
    )
    return {
        "mH": mH, "dimension": mH+1, "NU": nu,
        "A_H": AH, "L_H_ideal_pred": LH, "ideal_loss": ideal_loss,
        "tail_variance": tail_variance, "tail_sigma": math.sqrt(tail_variance),
        "ideal_harvest": harvest,
        "target": target, "required_h_H_at_Meff_1000_q10": required_hH,
        "required_efficiency": required_efficiency,
        "max_allowed_rho": rho_required,
    }


def active_weights(weights, mH):
    order = np.argsort(-weights)
    return [float(weights[k]) for k in order[:int(mH)]]


def effective_budget_for_score(active, score):
    """反解 ``L_H^ideal(B_eff)=score``。

    这是相对于当前 KL 倾斜模型的定义，不把 q 当作与 NU 无关的乘法税。
    """
    active = [float(value) for value in active]
    amplitude = sum(active)
    score = float(score)
    if score <= 0:
        return 0.0
    if score >= amplitude:
        return math.inf
    lo, hi = 1e-8, 1e9
    for _ in range(100):
        lam = math.sqrt(lo*hi)
        value = sum(weight*util.R1(lam*weight) for weight in active)
        if value < score:
            lo = lam
        else:
            hi = lam
    lam = math.sqrt(lo*hi)
    return float(sum(util.dKL(lam*weight) for weight in active))


def budget_metrics(weights, mH, nu, score):
    active = active_weights(weights, mH)
    budget = raw_budget(nu)
    effective = effective_budget_for_score(active, score)
    return {
        "raw_budget_nats": budget,
        "effective_budget_nats": effective,
        "budget_tax_nats": budget-effective,
        "effective_budget_per_coordinate": effective/int(mH),
    }


def required_effective_budget(weights, mH, required_score):
    return effective_budget_for_score(
        active_weights(weights, mH), required_score
    )


def fit_design(mH, nu):
    return [1.0, mH/nu, math.log(mH/400.0)]


def predict_rho(coefficients, mH, nu):
    return math.exp(float(np.dot(coefficients, fit_design(mH, nu))))
