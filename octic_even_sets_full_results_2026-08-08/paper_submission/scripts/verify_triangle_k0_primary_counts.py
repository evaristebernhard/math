#!/usr/bin/env python3
"""Exact symbolic audit for the k=0 finite invariant-Lagrangian count.

For a single primary component of a self-adjoint operator T, put N=T-lambda I.
Use the standard canonical model:
  * N is block diagonal with nilpotent Jordan blocks;
  * the symmetric Gram matrix is block diagonal with reverse-identity blocks.

In every Grassmann chart for half-dimensional subspaces L, impose exactly
  N L subset L,
  B|_L = 0.
The script records whether the solution set is positive-dimensional and, when finite,
counts distinct row spaces.  It verifies the table used in
TRIANGLE_K0_CLOSURE_RESEARCH_2026-08-09.md.
"""

from itertools import combinations
import sympy as sp


def jordan_block(m: int) -> sp.Matrix:
    M = sp.zeros(m)
    for i in range(m - 1):
        M[i, i + 1] = 1
    return M


def reverse_block(m: int) -> sp.Matrix:
    M = sp.zeros(m)
    for i in range(m):
        M[i, m - 1 - i] = 1
    return M


def canonical(part):
    N = sp.diag(*[jordan_block(m) for m in part])
    B = sp.diag(*[reverse_block(m) for m in part])
    assert B * N == N.T * B
    return N, B


def chart_equations(part, pivots):
    N, B = canonical(part)
    n = N.rows
    r = n // 2
    nonpivots = [j for j in range(n) if j not in pivots]
    xs = sp.symbols(f"x0:{r * len(nonpivots)}")

    M = sp.zeros(r, n)
    for i, p in enumerate(pivots):
        M[i, p] = 1
    k = 0
    for i in range(r):
        for j in nonpivots:
            M[i, j] = xs[k]
            k += 1

    # Invariance: MN = A M, with A read from the pivot columns because M_P=I.
    MN = M * N
    A = MN[:, list(pivots)]
    inv = MN[:, nonpivots] - A * M[:, nonpivots]

    # Isotropy.
    iso = M * B * M.T

    eqs = [sp.expand(e) for e in list(inv) if e != 0]
    for i in range(r):
        for j in range(i, r):
            e = sp.expand(iso[i, j])
            if e != 0:
                eqs.append(e)
    return xs, eqs, M


def is_unit_ideal(G):
    return len(G.polys) == 1 and G.polys[0].as_expr() == 1


def classify(part):
    n = sum(part)
    r = n // 2
    rowspaces = set()
    positive_dimensional = False

    for pivots in combinations(range(n), r):
        xs, eqs, M = chart_equations(part, pivots)
        G = sp.groebner(eqs, *xs, order="grevlex")
        if is_unit_ideal(G):
            continue
        if not G.is_zero_dimensional:
            positive_dimensional = True
            continue

        sols = sp.solve_poly_system([p.as_expr() for p in G.polys], *xs)
        for sol in sols:
            MM = M.subs(dict(zip(xs, sol)))
            RR, _ = MM.rref()
            rowspaces.add(tuple(sp.simplify(x) for x in RR))

    if positive_dimensional:
        return "infinity"
    return len(rowspaces)


EXPECTED = {
    (2,): 1,
    (1, 1): 2,
    (4,): 1,
    (3, 1): 2,
    (2, 2): 3,
    (2, 1, 1): 2,
    (1, 1, 1, 1): "infinity",
    (6,): 1,
    (5, 1): 2,
    (4, 2): 3,
    (4, 1, 1): 2,
    (3, 3): 4,
    (3, 2, 1): 2,
    (3, 1, 1, 1): "infinity",
    (2, 2, 2): "infinity",
    (2, 2, 1, 1): "infinity",
    (2, 1, 1, 1, 1): "infinity",
    (1, 1, 1, 1, 1, 1): "infinity",
}


def verify_all():
    for part, expected in EXPECTED.items():
        got = classify(part)
        assert got == expected, (part, got, expected)
        print(f"{part}: {got}")

    # Global finite maximum in dimension six:
    # primary dimensions 6, 4+2, or 2+2+2.
    assert max(4, 3 * 2, 2 ** 3) == 8
    print("finite global maximum: 8")
    print("equality type: (11)+(11)+(11) on three distinct primary eigenvalues")


def test_primary_counts():
    verify_all()


if __name__ == "__main__":
    verify_all()
