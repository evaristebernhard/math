#!/usr/bin/env python3
"""
Exact split-MacWilliams certificate excluding the d(R)=32 branch.

CONDITIONAL AUDIT ONLY.

Extra hypothesis used by this legacy certificate:
  * A_88=A_96=A_104=A_112=0.

Endrass, Minimal even sets of nodes, Cor. 1.11 does NOT provide this
vanishing for octic surfaces: in degree 8 it excludes strict weight 56;
88,96,104,112 occur in the degree-10 column.  Therefore this script does
not prove unconditional exclusion of d(R)=32 for octics.

Coding setup after shortening:
  * C is a binary [169,19] code;
  * every codeword weight is divisible by 8;
  * the minimum nonzero weight is 64;
  * C contains H=<c1,c2> whose three nonzero words all have weight 64.

The program:
  1. partitions the 169 coordinates into the four (c1_i,c2_i)-blocks;
  2. enumerates every possible H-coset split-weight state using the
     Endrass-forbidden weights;
  3. evaluates an exact nonnegative split-MacWilliams certificate;
  4. verifies the contradiction using only Python integers.
"""

from __future__ import annotations

from itertools import product
from math import comb
from typing import Dict, Tuple

Index = Tuple[int, int, int, int]
Counts = Tuple[int, int, int, int]
Weights = Tuple[int, int, int, int]

BLOCK_SIZES: Counts = (73, 32, 32, 32)
ZERO_ORBIT_WEIGHTS: Weights = (0, 64, 64, 64)

# For a strict even-node code on an octic, 88,96,104,112 are excluded by
# Endrass, Minimal even sets of nodes, Corollary 1.11.
ALLOWED_WEIGHTS = (
    0, 64, 72, 80, 120, 128, 136, 144, 152, 160, 168
)

KLEIN_PERMUTATIONS = (
    (0, 1, 2, 3),
    (1, 0, 3, 2),
    (2, 3, 0, 1),
    (3, 2, 1, 0),
)

CONSTANT = 1_000_000_000

COEFFICIENTS: Dict[Index, int] = {
    (0, 0, 0, 2): 68_106_614,
    (0, 0, 0, 4): 3_213_888,
    (0, 0, 2, 0): 56_003_971,
    (0, 0, 2, 4): 9_153,
    (0, 0, 4, 0): 5_724_406,
    (0, 0, 4, 2): 43_973,
    (0, 1, 1, 3): 199_398,
    (0, 1, 3, 1): 386_029,
    (0, 2, 0, 0): 38_428_042,
    (0, 2, 0, 4): 49_913,
    (0, 2, 4, 0): 51_055,
    (0, 3, 1, 1): 410_502,
    (0, 4, 0, 0): 3_180_934,
    (0, 4, 0, 2): 17_857,
    (0, 4, 2, 0): 38_767,
    (0, 6, 0, 0): 19_244,
    (1, 0, 2, 2): 150_706,
    (1, 1, 3, 1): 4_894,
    (1, 2, 0, 2): 116_444,
    (1, 2, 2, 0): 163_968,
    (2, 0, 0, 2): 64_206,
    (2, 2, 0, 0): 140_431,
    (3, 0, 2, 0): 22_877,
    (3, 1, 1, 1): 4_566,
    (3, 2, 0, 0): 5_656,
    (5, 0, 0, 0): 4_619,
    (6, 0, 0, 0): 358,
}


def krawtchouk(n: int, degree: int, weight: int) -> int:
    total = 0
    lower = max(0, degree - (n - weight))
    upper = min(degree, weight)
    for i in range(lower, upper + 1):
        total += (
            (-1) ** i
            * comb(weight, i)
            * comb(n - weight, degree - i)
        )
    return total


def canonical_weights(weights: Weights) -> Weights:
    return min(
        tuple(weights[index] for index in permutation)
        for permutation in KLEIN_PERMUTATIONS
    )


def recover_counts(weights: Weights, sizes: Counts) -> Counts | None:
    """Invert the four H-orbit weight equations."""
    n00, n10, n01, n11 = sizes
    w0, w1, w2, w3 = weights

    rhs = (
        w0,
        w1 - n10 - n11,
        w2 - n01 - n11,
        w3 - n10 - n01,
    )

    numerators = (
        rhs[0] + rhs[1] + rhs[2] + rhs[3],
        rhs[0] - rhs[1] + rhs[2] - rhs[3],
        rhs[0] + rhs[1] - rhs[2] - rhs[3],
        rhs[0] - rhs[1] - rhs[2] + rhs[3],
    )

    if any(value % 4 for value in numerators):
        return None

    counts = tuple(value // 4 for value in numerators)
    if not all(0 <= value <= size for value, size in zip(counts, sizes)):
        return None
    return counts  # type: ignore[return-value]


def orbit_counts(counts: Counts, sizes: Counts) -> tuple[Counts, ...]:
    x00, x10, x01, x11 = counts
    n00, n10, n01, n11 = sizes
    return (
        (x00, x10, x01, x11),
        (x00, n10 - x10, x01, n11 - x11),
        (x00, x10, n01 - x01, n11 - x11),
        (x00, n10 - x10, n01 - x01, x11),
    )


def orbit_feature(counts: Counts, sizes: Counts, index: Index) -> int:
    total = 0
    for state in orbit_counts(counts, sizes):
        term = 1
        for size, degree, weight in zip(sizes, index, state):
            term *= krawtchouk(size, degree, weight)
        total += term
    return total


def enumerate_coset_states() -> tuple[list[Counts], Counts]:
    representatives: dict[Weights, Counts] = {}

    for weights in product(ALLOWED_WEIGHTS, repeat=4):
        counts = recover_counts(weights, BLOCK_SIZES)
        if counts is None:
            continue

        canonical = canonical_weights(weights)
        canonical_counts = recover_counts(canonical, BLOCK_SIZES)
        if canonical_counts is None:
            raise AssertionError("canonical state failed to invert")

        representatives.setdefault(canonical, canonical_counts)

    zero_key = canonical_weights(ZERO_ORBIT_WEIGHTS)
    zero_counts = representatives.pop(zero_key)
    return list(representatives.values()), zero_counts


def certificate_value(counts: Counts) -> int:
    return CONSTANT + sum(
        coefficient * orbit_feature(counts, BLOCK_SIZES, index)
        for index, coefficient in COEFFICIENTS.items()
    )


def main() -> None:
    nonzero_states, zero_counts = enumerate_coset_states()

    assert len(nonzero_states) == 122

    values = [certificate_value(state) for state in nonzero_states]
    maximum = max(values)
    minimum = min(values)
    zero_value = certificate_value(zero_counts)

    assert maximum == -597_428_248
    assert minimum == -36_199_536_078_392
    assert zero_value == 117_963_660_093_832
    assert maximum < 0

    quotient_size = 2**17
    threshold = CONSTANT * quotient_size
    assert zero_value < threshold
    assert threshold == 131_072_000_000_000

    print("d(R)=32 exact split-MacWilliams certificate")
    print("  nonzero H-coset states :", len(nonzero_states))
    print("  maximum certificate    :", maximum)
    print("  minimum certificate    :", minimum)
    print("  certificate at H       :", zero_value)
    print("  constant * 2^17        :", threshold)
    print("  gap                    :", threshold - zero_value)
    print()
    print("All exact checks passed.")


if __name__ == "__main__":
    main()
