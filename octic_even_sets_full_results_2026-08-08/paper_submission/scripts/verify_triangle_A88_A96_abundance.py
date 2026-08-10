#!/usr/bin/env python3
"""Exact split-MacWilliams certificate for a residual 32 triangle.

Theorem verified by this script.

Let C be a binary 8-divisible [169,19,64] code containing a two-dimensional
subcode H=<c1,c2> whose three nonzero words all have weight 64.  Then

    A_88(C) + A_96(C) >= 65.

No deletion of weights 88,96,104,112 is assumed.  The proof uses the full
allowed weight set for an 8-divisible minimum-64 length-169 code.

The four H-block sizes are (73,32,32,32).  We enumerate every possible
nonzero H-coset state, use split Krawtchouk moments of total degree <= 8,
and verify an exact rational dual certificate using Python integers only.
"""

from itertools import product
from math import comb

SIZES = (73, 32, 32, 32)
ALLOWED = tuple(range(64, 169, 8)) + (0,)
ALLOWED = tuple(sorted(ALLOWED))
KLEIN = (
    (0, 1, 2, 3),
    (1, 0, 3, 2),
    (2, 3, 0, 1),
    (3, 2, 1, 0),
)
ZERO_WEIGHTS = (0, 64, 64, 64)

# Common denominator of the exact dual coefficients.
D = 10**16
MU_NUM = 84_772_048_819_120

# Nonnegative multipliers lambda_j = numerator / D.
# Here Phi_j is the H-orbit sum of the four-block split Krawtchouk feature.
LAMBDA_NUM = {
    (0, 0, 2, 0): 149_988_053_449,
    (0, 2, 0, 0): 698_300_216_164,
    (1, 0, 0, 2): 114_662_497_219,
    (1, 0, 2, 0): 144_129_577_275,
    (1, 2, 0, 0): 94_463_478_607,
    (0, 1, 1, 3): 11_279_143_111,
    (0, 1, 3, 1): 12_756_879_943,
    (0, 3, 1, 1): 9_954_364_697,
    (1, 0, 0, 4): 5_631_015_494,
    (1, 0, 2, 2): 6_284_432_149,
    (1, 0, 4, 0): 10_479_118_786,
    (1, 2, 0, 2): 2_719_611_181,
    (1, 2, 2, 0): 4_645_827_081,
    (1, 4, 0, 0): 4_921_422_999,
    (5, 0, 0, 0): 68_395_254,
    (0, 2, 4, 0): 99_554_863,
    (1, 1, 1, 3): 127_702_386,
    (1, 1, 3, 1): 71_123_616,
    (2, 2, 0, 2): 136_127_903,
    (2, 2, 2, 0): 165_658_430,
    (3, 1, 1, 1): 87_230_736,
    (4, 0, 0, 2): 39_583_467,
    (4, 0, 2, 0): 7_979_578,
    (4, 2, 0, 0): 11_407_528,
    (0, 1, 3, 3): 134_414_767,
    (0, 1, 5, 1): 168_816_124,
    (0, 3, 1, 3): 34_510_033,
    (0, 3, 3, 1): 156_584_290,
    (1, 0, 4, 2): 223_339_482,
    (1, 2, 0, 4): 171_084_251,
    (1, 2, 4, 0): 102_097_798,
    (1, 4, 2, 0): 174_490_564,
    (4, 1, 1, 1): 7_889_904,
    (5, 0, 0, 2): 1_132_966,
    (5, 2, 0, 0): 564_853,
    (7, 0, 0, 0): 2_339_681,
    (1, 1, 5, 1): 7_038_413,
    (1, 5, 1, 1): 5_428_326,
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


def bad_weight_count(weights):
    return sum(1 for w in weights if w in (88, 96))


def main():
    states, zero_counts = enumerate_states()
    assert len(states) == 1594
    assert len(LAMBDA_NUM) == 38
    assert all(a >= 0 for a in LAMBDA_NUM.values())

    # Pointwise dual inequality on every possible nonzero H-coset:
    # D*b(s) - sum_j lambda_num[j] Phi_j(s) >= MU_NUM.
    min_slack = None
    min_state = None
    for weights, counts in states.items():
        lhs = D * bad_weight_count(weights)
        lhs -= sum(a * phi(counts, j) for j, a in LAMBDA_NUM.items())
        slack = lhs - MU_NUM
        if min_slack is None or slack < min_slack:
            min_slack = slack
            min_state = weights
    assert min_slack is not None and min_slack >= 0

    # Split MacWilliams gives sum_all_cosets Phi_j >= 0, hence
    # sum_nonzero Phi_j >= -Phi_j(H).  There are 2^17-1 nonzero H-cosets.
    zero_penalty = sum(a * phi(zero_counts, j) for j, a in LAMBDA_NUM.items())
    lower_num = (2**17 - 1) * MU_NUM - zero_penalty

    # Exact rational lower bound is lower_num / D, strictly above 64.
    assert lower_num > 64 * D
    # A_88+A_96 is an integer, hence it is at least 65.

    print("Residual-32 triangle A88+A96 exact split-MacWilliams certificate")
    print("  nonzero H-coset states :", len(states))
    print("  active moments          :", len(LAMBDA_NUM))
    print("  minimum pointwise slack :", min_slack)
    print("  state attaining min     :", min_state)
    print("  exact lower numerator   :", lower_num)
    print("  denominator             :", D)
    print("  lower bound             :", lower_num / D)
    print("  margin above 64         :", (lower_num - 64 * D) / D)
    print()
    print("Therefore A_88 + A_96 >= 65.")
    print("All checks used exact Python integers.")


if __name__ == "__main__":
    main()
