#!/usr/bin/env python3
"""RETRACTED / INVALID FOR OCTICS.

This exploratory script was built under a misreading of Endrass Cor. 1.11:
it deletes strict weights 88,96,104,112.  Those weights belong to the
degree-10 forbidden column, not degree 8.  For octics the corollary excludes
strict weight 56 only.  Consequently the d(R)<=44, A_48>=24, and incidence
reduction produced below are NOT valid octic theorems and this file is not
run by the submission test suite.

The code is retained only to document the retracted experiment.

Assumptions used by this invalid experiment:
  * weight 48 is minimal and is cut by a reduced contact quadric;
  * extra unsupported vanishing of 88,96,104,112.

Coding setup after shortening:
  * C is an 8-divisible binary [169,19] code with d(C)=48;
  * fix a weight-48 word c;
  * R=Res(C;c) is a 4-divisible [121,18] code.

The script verifies two claims exactly:
  (I)  the refined first-residual bound d(R) <= 44;
  (II) a split-MacWilliams dual certificate giving A_48(C) > 23,
       hence A_48(C) >= 24.
It then verifies the elementary incidence step forcing a pair of weight-48
words meeting in 16 or 24 coordinates, hence a base word with residual
minimum distance 24 or 32.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations_with_replacement
from math import comb

N = 169
DIM = 19
C_SIZE = 2**DIM
R_N = 121
R_DIM = 18
R_SIZE = 2**R_DIM

GLOBAL_ALLOWED = (0, 48, 64, 72, 80, 120, 128, 136, 144, 152, 160, 168)


def krawtchouk(n: int, degree: int, weight: int) -> int:
    """Binary Krawtchouk polynomial, via exact three-term recurrence."""
    if degree == 0:
        return 1
    k0 = 1
    k1 = n - 2 * weight
    if degree == 1:
        return k1
    a, b = k0, k1
    for j in range(1, degree):
        numerator = (n - 2 * weight) * b - (n - j + 1) * a
        assert numerator % (j + 1) == 0
        a, b = b, numerator // (j + 1)
    return b


def residual_states() -> list[tuple[int, int, int, int]]:
    """Return canonical H=<c> coset states (r,a;u,v), with a<=24 and u<=v."""
    out: list[tuple[int, int, int, int]] = []
    for u, v in combinations_with_replacement(GLOBAL_ALLOWED, 2):
        s = u + v - 48
        d = u - v + 48
        if s % 2 or d % 2:
            continue
        r = s // 2
        a = d // 2
        if 0 <= r <= 121 and 0 <= a <= 24:
            out.append((r, a, u, v))
    return sorted(out)


def verify_refined_residual_bound(states: list[tuple[int, int, int, int]]) -> None:
    allowed_r = sorted({r for r, _a, _u, _v in states})
    expected = [0, 24, 32, 36, 40, 44, 48, 52, 56, 72, 76, 80,
                96, 100, 104, 108, 112, 116, 120]
    assert allowed_r == expected

    # Exact nonnegative Krawtchouk certificate on length 121:
    # P = 19,923,960 K0 + 127,704 K3 + 31,905 K4 + 4,835 K5.
    coeff = {0: 19_923_960, 3: 127_704, 4: 31_905, 5: 4_835}

    def P(w: int) -> int:
        return sum(a * krawtchouk(R_N, j, w) for j, a in coeff.items())

    nonzero_if_d_ge_48 = [w for w in allowed_r if w >= 48]
    vals = {w: P(w) for w in nonzero_if_d_ge_48}
    assert all(v <= 0 for v in vals.values())
    assert vals[48] == vals[56] == vals[76] == 0

    p0 = P(0)
    threshold = coeff[0] * R_SIZE
    assert p0 == 1_269_004_369_920
    assert threshold == 5_222_946_570_240
    assert p0 < threshold

    print("Refined weight-48 first residual certificate")
    print("  allowed residual weights:", allowed_r)
    print("  P(0):", p0)
    print("  K0 * 2^18:", threshold)
    print("  conclusion: d(R) <= 44")


def split_feature(state: tuple[int, int, int, int], i: int, j: int) -> int:
    r, a, _u, _v = state
    return krawtchouk(121, i, r) * (
        krawtchouk(48, j, a) + krawtchouk(48, j, 48 - a)
    )


def verify_A48_lower_bound(states: list[tuple[int, int, int, int]]) -> None:
    assert len(states) == 30
    zero = (0, 0, 0, 48)
    assert zero in states

    # The nine split MacWilliams moments used in the exact dual certificate.
    moments = ((0, 2), (0, 4), (0, 6), (1, 4), (1, 6),
               (3, 2), (4, 2), (6, 0), (7, 0))

    # Exact dual coefficients lambda_m >= 0.
    lam = (
        Fraction(65239429292188417201, 2834529949256729839534080),
        Fraction(3170499391738143997, 1181054145523637433139200),
        Fraction(770756836106435039, 4724216582094549732556800),
        Fraction(3282915304170671, 49210589396818226380800),
        Fraction(4710389538806263, 590527072761818716569600),
        Fraction(483894212214413, 885790609142728074854400),
        Fraction(2987876555989, 39368471517454581104640),
        Fraction(7072896059273, 44289530457136403742720),
        Fraction(3900761177663, 221447652285682018713600),
    )
    assert all(x >= 0 for x in lam)

    alpha = Fraction(33677326469941958183, 147631768190454679142400)
    beta = Fraction(-27176298587580376598, 750894003247348425)

    # For every canonical H-coset state s, let c48(s) be the number (0,1,2)
    # of representatives of that coset having global weight 48.  Verify
    #   c48(s) >= alpha + beta*1_{s=zero} + sum lambda_m Phi_m(s).
    # Summing over all 2^18 cosets and using split MacWilliams positivity gives
    #   A48 >= alpha*2^18 + beta > 23.
    for state in states:
        _r, _a, u, v = state
        c48 = int(u == 48) + int(v == 48)
        rhs = alpha + (beta if state == zero else 0)
        rhs += sum(
            l * split_feature(state, i, j)
            for l, (i, j) in zip(lam, moments)
        )
        assert Fraction(c48, 1) >= rhs

    lower = alpha * R_SIZE + beta
    expected = Fraction(53180410117026702938, 2252682009742045275)
    assert lower == expected
    assert lower > 23
    assert lower < 24

    print("Split-MacWilliams lower bound for A_48")
    print("  canonical H-coset states:", len(states))
    print("  exact lower bound:", lower)
    print("  decimal lower bound:", float(lower))
    print("  conclusion: A_48 >= 24")


def verify_incidence_reduction() -> None:
    m = 24
    total_incidence = 48 * m
    q, r = divmod(total_incidence, 169)
    convex_lower = (169 - r) * comb(q, 2) + r * comb(q + 1, 2)
    pair_count = comb(m, 2)
    if_all_intersections_at_most_12 = 12 * pair_count

    assert (q, r) == (6, 138)
    assert convex_lower == 3363
    assert pair_count == 276
    assert if_all_intersections_at_most_12 == 3312
    assert convex_lower > if_all_intersections_at_most_12

    # For two distinct 48-words c,x, wt(c+x)=96-2t.  Among allowed nonzero
    # strict weights <=96 only 48,64,72,80 occur, hence t in {24,16,12,8}.
    intersections = sorted({(96 - w) // 2 for w in (48, 64, 72, 80)})
    assert intersections == [8, 12, 16, 24]

    print("Incidence reduction")
    print("  convex lower pair-incidence:", convex_lower)
    print("  bound if all intersections <=12:", if_all_intersections_at_most_12)
    print("  allowed intersections:", intersections)
    print("  conclusion: some pair meets in 16 or 24 coordinates")
    print("  hence one may choose c with d(Res(C;c)) in {24,32}")


def main() -> None:
    states = residual_states()
    verify_refined_residual_bound(states)
    print()
    verify_A48_lower_bound(states)
    print()
    verify_incidence_reduction()
    print("\nAll exact weight-48 global-reduction checks passed.")


if __name__ == "__main__":
    main()
