#!/usr/bin/env python3
"""Exact split-MacWilliams certificate for a residual 32 triangle.

Theorem verified by this script.

Let C be a binary 8-divisible [169,19,64] code containing a two-dimensional
subcode H=<c1,c2> whose three nonzero words all have weight 64.  Then

    A_88(C) + 3 A_96(C) >= 185.

Together with the companion certificate A_88+A_96>=65 this gives useful
geometric dichotomies; in particular max(A_88,A_96)>=47, and either
A_96>=41 or A_88>=65.

No deletion of weights 88,96,104,112 is assumed.  The proof uses the full
allowed weight set and split Krawtchouk moments of total degree <= 8.
All verification below is exact integer arithmetic.
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
MU_NUM = 28_837_497_163_480

# Nonnegative multipliers lambda_j = numerator / D.
LAMBDA_NUM = {
    (0, 0, 0, 2): 13_486_589_098,
    (0, 1, 1, 3): 4_003_258_172,
    (0, 1, 1, 5): 4_411_699,
    (0, 1, 3, 1): 3_820_121_750,
    (0, 2, 0, 0): 370_550_144_496,
    (0, 3, 1, 1): 5_823_913_063,
    (0, 3, 1, 3): 21_535_610,
    (0, 3, 3, 1): 76_274_091,
    (0, 5, 1, 1): 8_574_316,
    (1, 0, 0, 2): 38_361_707_195,
    (1, 0, 0, 4): 2_071_178_796,
    (1, 0, 2, 0): 42_421_876_403,
    (1, 0, 2, 2): 1_058_830_502,
    (1, 0, 2, 4): 41_623_179,
    (1, 0, 4, 0): 1_444_053_789,
    (1, 1, 1, 5): 1_904_618,
    (1, 1, 3, 1): 7_150_755,
    (1, 1, 5, 1): 1_301_415,
    (1, 2, 0, 0): 35_235_502_394,
    (1, 2, 0, 2): 2_053_931_892,
    (1, 2, 0, 4): 22_219_795,
    (1, 2, 2, 0): 2_056_035_699,
    (1, 2, 4, 0): 69_263_976,
    (1, 4, 0, 0): 3_660_962_332,
    (1, 4, 0, 2): 31_205_794,
    (1, 4, 2, 0): 73_250_552,
    (1, 5, 1, 1): 3_182_153,
    (2, 0, 2, 2): 4_543_657,
    (2, 2, 2, 0): 48_175_277,
    (3, 1, 1, 1): 47_530_589,
    (4, 0, 0, 2): 7_259_765,
    (4, 0, 2, 0): 4_053_556,
    (4, 1, 1, 1): 956_788,
    (5, 0, 0, 0): 82_103_315,
    (5, 2, 0, 0): 6_706_195,
    (7, 0, 0, 0): 2_044_762,
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


def weighted_count(weights):
    return sum(1 if w == 88 else 3 if w == 96 else 0 for w in weights)


def main():
    states, zero_counts = enumerate_states()
    assert len(states) == 1594
    assert len(LAMBDA_NUM) == 36
    assert all(a >= 0 for a in LAMBDA_NUM.values())

    min_slack = None
    min_state = None
    for weights, counts in states.items():
        lhs = D * weighted_count(weights)
        lhs -= sum(a * phi(counts, j) for j, a in LAMBDA_NUM.items())
        slack = lhs - MU_NUM
        if min_slack is None or slack < min_slack:
            min_slack = slack
            min_state = weights
    assert min_slack is not None and min_slack >= 0

    zero_penalty = sum(a * phi(zero_counts, j) for j, a in LAMBDA_NUM.items())
    lower_num = (2**17 - 1) * MU_NUM - zero_penalty

    assert lower_num > 184 * D

    print("Residual-32 triangle A88+3A96 exact split-MacWilliams certificate")
    print("  nonzero H-coset states :", len(states))
    print("  active moments          :", len(LAMBDA_NUM))
    print("  minimum pointwise slack :", min_slack)
    print("  state attaining min     :", min_state)
    print("  exact lower numerator   :", lower_num)
    print("  denominator             :", D)
    print("  lower bound             :", lower_num / D)
    print("  margin above 184        :", (lower_num - 184 * D) / D)
    print()
    print("Therefore A_88 + 3 A_96 >= 185.")
    print("Hence max(A_88,A_96) >= 47.")
    print("Also, either A_96 >= 41 or A_88 >= 65.")
    print("All checks used exact Python integers.")


if __name__ == "__main__":
    main()
