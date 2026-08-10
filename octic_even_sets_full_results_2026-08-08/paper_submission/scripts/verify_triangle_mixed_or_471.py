#!/usr/bin/env python3
"""Exact split-MacWilliams dichotomy for a residual-32 triangle.

Let C be a binary 8-divisible [169,19,64] code containing a two-dimensional
subcode H whose three nonzero words all have weight 64. Then either

  (i) some nonzero H-coset contains both a weight-64 word and a word of
      weight 88 or 96; or
  (ii) A_88(C)+A_96(C) >= 471.

No weight is deleted. The second alternative is certified on the full allowed
weight set by exact integer arithmetic. The certificate assumes the negation
of (i), i.e. excludes only mixed H-coset states, not any global codeword weight.
"""

from itertools import product
from math import comb

SIZES = (73, 32, 32, 32)
ALLOWED = tuple(sorted((0,) + tuple(range(64, 169, 8))))
KLEIN = (
    (0, 1, 2, 3),
    (1, 0, 3, 2),
    (2, 3, 0, 1),
    (3, 2, 1, 0),
)
ZERO_WEIGHTS = (0, 64, 64, 64)

D = 10**15
MU_NUM = 62_570_151_493_496

LAMBDA_NUM = {
    (0, 0, 0, 2): 239_188_970_348,
    (0, 0, 2, 0): 393_521_057_799,
    (0, 1, 1, 3): 7_822_312_249,
    (0, 1, 3, 1): 11_909_341_539,
    (0, 1, 3, 3): 155_425_635,
    (0, 1, 5, 1): 121_890_155,
    (0, 2, 4, 0): 69_359_801,
    (0, 3, 1, 1): 5_484_331_486,
    (0, 3, 1, 3): 84_254_240,
    (1, 0, 0, 2): 83_644_993_311,
    (1, 0, 0, 4): 3_279_921_679,
    (1, 0, 2, 0): 95_926_800_008,
    (1, 0, 2, 2): 5_223_809_989,
    (1, 0, 4, 0): 10_156_802_889,
    (1, 0, 4, 2): 251_262_915,
    (1, 1, 1, 3): 78_528_909,
    (1, 1, 1, 5): 233_964,
    (1, 1, 5, 1): 9_084_503,
    (1, 2, 0, 0): 80_833_424_766,
    (1, 2, 0, 2): 1_655_431_012,
    (1, 2, 0, 4): 144_169_563,
    (1, 2, 2, 0): 3_229_302_554,
    (1, 2, 4, 0): 18_104_635,
    (1, 3, 1, 1): 64_313_103,
    (1, 4, 0, 0): 2_087_537_968,
    (1, 4, 0, 2): 44_652_491,
    (1, 4, 2, 0): 37_943_886,
    (2, 0, 2, 2): 61_294_329,
    (2, 2, 0, 2): 99_854_332,
    (2, 2, 2, 0): 58_260_004,
    (3, 1, 1, 1): 65_515_104,
    (4, 0, 0, 2): 17_339_777,
    (4, 0, 2, 0): 21_889_737,
    (4, 1, 1, 1): 5_711_268,
    (4, 2, 0, 0): 3_710_366,
    (5, 0, 0, 0): 54_200_121,
    (5, 0, 2, 0): 1_646_755,
    (7, 0, 0, 0): 1_808_265,
}


def krawtchouk(n: int, degree: int, weight: int) -> int:
    lo = max(0, degree - (n - weight))
    hi = min(degree, weight)
    return sum(
        (-1) ** i * comb(weight, i) * comb(n - weight, degree - i)
        for i in range(lo, hi + 1)
    )


def canonical_weights(weights):
    return min(tuple(weights[i] for i in p) for p in KLEIN)


def recover_counts(weights):
    n00, n10, n01, n11 = SIZES
    w0, w1, w2, w3 = weights
    rhs = (
        w0,
        w1 - n10 - n11,
        w2 - n01 - n11,
        w3 - n10 - n01,
    )
    nums = (
        rhs[0] + rhs[1] + rhs[2] + rhs[3],
        rhs[0] - rhs[1] + rhs[2] - rhs[3],
        rhs[0] + rhs[1] - rhs[2] - rhs[3],
        rhs[0] - rhs[1] - rhs[2] + rhs[3],
    )
    if any(v % 4 for v in nums):
        return None
    counts = tuple(v // 4 for v in nums)
    if not all(0 <= x <= n for x, n in zip(counts, SIZES)):
        return None
    return counts


def orbit_counts(counts):
    x00, x10, x01, x11 = counts
    n00, n10, n01, n11 = SIZES
    return (
        (x00, x10, x01, x11),
        (x00, n10 - x10, x01, n11 - x11),
        (x00, x10, n01 - x01, n11 - x11),
        (x00, n10 - x10, n01 - x01, x11),
    )


def phi(counts, index):
    total = 0
    for state in orbit_counts(counts):
        term = 1
        for n, j, w in zip(SIZES, index, state):
            term *= krawtchouk(n, j, w)
        total += term
    return total


def enumerate_states():
    reps = {}
    for weights in product(ALLOWED, repeat=4):
        counts = recover_counts(weights)
        if counts is None:
            continue
        key = canonical_weights(weights)
        reps.setdefault(key, recover_counts(key))
    zero_counts = reps.pop(canonical_weights(ZERO_WEIGHTS))
    return reps, zero_counts


def is_mixed(weights):
    return any(w == 64 for w in weights) and any(w in (88, 96) for w in weights)


def high_count(weights):
    return sum(1 for w in weights if w in (88, 96))


def main():
    states, zero_counts = enumerate_states()
    assert len(states) == 1594
    allowed_states = [(w, c) for w, c in states.items() if not is_mixed(w)]
    assert len(allowed_states) == 1395
    assert len(LAMBDA_NUM) == 38
    assert all(a >= 0 for a in LAMBDA_NUM.values())

    min_slack = None
    min_state = None
    for weights, counts in allowed_states:
        lhs = D * high_count(weights)
        lhs -= sum(a * phi(counts, j) for j, a in LAMBDA_NUM.items())
        slack = lhs - MU_NUM
        if min_slack is None or slack < min_slack:
            min_slack = slack
            min_state = weights
    assert min_slack is not None and min_slack >= 0

    zero_penalty = sum(a * phi(zero_counts, j) for j, a in LAMBDA_NUM.items())
    lower_num = (2**17 - 1) * MU_NUM - zero_penalty
    assert lower_num > 470 * D

    print("Residual-32 triangle mixed-coset / high-weight dichotomy")
    print("  all nonzero H-coset states :", len(states))
    print("  non-mixed states           :", len(allowed_states))
    print("  active moments             :", len(LAMBDA_NUM))
    print("  minimum pointwise slack    :", min_slack)
    print("  state attaining min        :", min_state)
    print("  exact lower numerator      :", lower_num)
    print("  denominator                :", D)
    print("  lower bound                :", lower_num / D)
    print("  margin above 470           :", (lower_num - 470 * D) / D)
    print()
    print("Hence, if no H-coset mixes weight 64 with weight 88/96,")
    print("then A_88 + A_96 >= 471.")
    print("Equivalently: a triangle forces a mixed coset or >=471 high words.")
    print("All checks used exact Python integers.")


if __name__ == "__main__":
    main()
