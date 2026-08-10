#!/usr/bin/env python3
"""Small exact prototype for bounded zero-relation certificates and dual CVP filters.

This is deliberately a low-dimensional verifier.  It uses real Riemann-zero balls
already present in ``work/zeros_arb.txt``, rounds K*gamma to integers p_i, keeps
the rounding/ball error in the certified radius, and compares:

1. exhaustive exact primal SVP/CVP decisions;
2. one- and multi-character lower bounds from short dual vectors.

The prototype is not a full Hurst certificate.  Its purpose is to validate the
mathematical reduction and measure how much a small number of dual characters
can filter before exact CVP enumeration is needed.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
from fractions import Fraction

import config
import util


def parse_ball_fraction(line: str) -> tuple[int, Fraction, Fraction]:
    index, text = util.parse_arb_ball_line(line)
    body = text[1:-1]
    mid_text, rad_text = body.split("+/-", 1)
    return index, Fraction(mid_text), Fraction(rad_text)


def nearest_integer(x: Fraction) -> int:
    q, r = divmod(x.numerator, x.denominator)
    return q + (2 * r >= x.denominator)


def centered_mod(value: int, modulus: int) -> int:
    residue = value % modulus
    if 2 * residue > modulus:
        residue -= modulus
    return residue


def integer_points_ball(dimension: int, radius_sq: int):
    """Yield every integer vector with Euclidean square <= radius_sq."""
    vector = [0] * dimension

    def visit(position: int, remaining: int):
        if position == dimension:
            yield tuple(vector)
            return
        limit = math.isqrt(remaining)
        for value in range(-limit, limit + 1):
            vector[position] = value
            yield from visit(position + 1, remaining - value * value)

    yield from visit(0, radius_sq)


def dot(left, right) -> int:
    return sum(int(a) * int(b) for a, b in zip(left, right))


def row_norm_sq(row) -> int:
    return dot(row, row)


def gram_schmidt_exact(basis: list[list[int]]):
    """Exact Gram--Schmidt data for a small integer row basis."""
    dimension = len(basis)
    width = len(basis[0])
    stars: list[list[Fraction]] = []
    norms: list[Fraction] = []
    mu = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    for i in range(dimension):
        vector = [Fraction(value) for value in basis[i]]
        for j in range(i):
            coefficient = sum(
                Fraction(basis[i][t]) * stars[j][t] for t in range(width)
            ) / norms[j]
            mu[i][j] = coefficient
            for t in range(width):
                vector[t] -= coefficient * stars[j][t]
        norm = sum(value * value for value in vector)
        if norm == 0:
            raise RuntimeError("linearly dependent basis in exact LLL")
        stars.append(vector)
        norms.append(norm)
    return mu, norms


def exact_lll(rows: list[list[int]], lovasz: Fraction = Fraction(3, 4)):
    """Slow exact LLL, suitable for the prototype dimensions only."""
    basis = [row[:] for row in rows]
    dimension = len(basis)
    transform = [[int(i == j) for j in range(dimension)] for i in range(dimension)]
    k = 1
    while k < dimension:
        mu, norms = gram_schmidt_exact(basis)
        for j in range(k - 1, -1, -1):
            quotient = int(round(mu[k][j]))
            if quotient:
                basis[k] = [
                    basis[k][t] - quotient * basis[j][t]
                    for t in range(len(basis[k]))
                ]
                transform[k] = [
                    transform[k][t] - quotient * transform[j][t]
                    for t in range(dimension)
                ]
                mu, norms = gram_schmidt_exact(basis)
        if norms[k] >= (lovasz - mu[k][k - 1] ** 2) * norms[k - 1]:
            k += 1
        else:
            basis[k], basis[k - 1] = basis[k - 1], basis[k]
            transform[k], transform[k - 1] = transform[k - 1], transform[k]
            k = max(1, k - 1)
    return basis, transform


def lll_short_dual_rows(p: list[int]) -> tuple[int, list[list[int]]]:
    """Return Delta and an exactly LLL-reduced basis of Delta * L^*."""
    m = len(p)
    delta = 1 + sum(value * value for value in p)
    rows = []
    for i, pi in enumerate(p):
        row = [(-pi * pj) for pj in p] + [pi]
        row[i] += delta
        rows.append(row)

    reduced, transform = exact_lll(rows)
    for i in range(m):
        reconstructed = [
            sum(transform[i][k] * rows[k][j] for k in range(m))
            for j in range(m + 1)
        ]
        if reconstructed != reduced[i]:
            raise RuntimeError("dual LLL transform reconstruction failed")

    reduced.sort(key=row_norm_sq)
    return delta, reduced


def gram(rows: list[list[int]]) -> list[list[int]]:
    return [[dot(a, b) for b in rows] for a in rows]


def determinant_int(matrix: list[list[int]]) -> int:
    """Exact determinant by cofactor expansion; only used for k<=3 by default."""
    n = len(matrix)
    if n == 0:
        return 1
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    total = 0
    for column, value in enumerate(matrix[0]):
        minor = [row[:column] + row[column + 1 :] for row in matrix[1:]]
        total += (-1 if column % 2 else 1) * value * determinant_int(minor)
    return total


def adjugate_int(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)
    if n == 1:
        return [[1]]
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [
                row[:i] + row[i + 1 :]
                for row_index, row in enumerate(matrix)
                if row_index != j
            ]
            result[i][j] = (-1 if (i + j) % 2 else 1) * determinant_int(minor)
    return result


def quadratic_numerator(vector: tuple[int, ...], adjugate: list[list[int]]) -> int:
    return sum(
        vector[i] * adjugate[i][j] * vector[j]
        for i in range(len(vector))
        for j in range(len(vector))
    )


def exact_torus_lower_bound(
    rows: list[list[int]],
    delta: int,
    target_p: int,
    max_window: int,
) -> tuple[Fraction | None, dict]:
    """Certify a projected CVP lower bound from selected dual rows.

    For z_j = rows[j]/Delta, let M=(rows_i . rows_j).  The projected
    lower bound is

        min_n (f + Delta*n)^T M^{-1} (f + Delta*n),

    where f_j is the centered residue of rows[j][-1]*target_p modulo Delta.
    We enumerate an expanding integer cube.  A global outside-cube bound uses
    lambda_max(M) <= max row-sum(M):

        q >= ||w||^2/lambda_max(M).
    """
    matrix = gram(rows)
    determinant = determinant_int(matrix)
    if determinant <= 0:
        raise RuntimeError("dual Gram matrix is not positive definite")
    adj = adjugate_int(matrix)
    lambda_upper = max(sum(abs(value) for value in row) for row in matrix)
    residues = tuple(centered_mod(row[-1] * target_p, delta) for row in rows)

    best_num = None
    best_shift = None
    certified_window = None
    k = len(rows)

    for window in range(max_window + 1):
        ranges = [range(-window, window + 1)] * k
        for shift in itertools.product(*ranges):
            if window and max(abs(value) for value in shift) != window:
                continue
            vector = tuple(residues[i] + delta * shift[i] for i in range(k))
            numerator = quadratic_numerator(vector, adj)
            if best_num is None or numerator < best_num:
                best_num = numerator
                best_shift = shift

        # Any shift outside [-window,window]^k has one coordinate whose
        # magnitude is at least (window+1/2)*Delta after centering.
        outside_num = (2 * window + 1) ** 2 * delta * delta
        # outside lower bound = outside_num / (4*lambda_upper)
        if best_num * 4 * lambda_upper < outside_num * determinant:
            certified_window = window
            break

    metadata = {
        "dimension": k,
        "det_gram": str(determinant),
        "lambda_max_upper": str(lambda_upper),
        "best_shift": list(best_shift) if best_shift is not None else None,
        "certified_window": certified_window,
        "max_window": max_window,
    }
    if certified_window is None:
        return None, metadata
    return Fraction(best_num, determinant), metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=5)
    parser.add_argument("--N", type=int, default=2)
    parser.add_argument("--bits", type=int, default=160)
    parser.add_argument("--external", type=int, default=12)
    parser.add_argument("--dual-k", type=int, default=3)
    parser.add_argument("--dual-window", type=int, default=16)
    parser.add_argument(
        "--zeros-arb", default=config.ZEROS_ARB,
        help="strict Arb-ball zero file",
    )
    parser.add_argument(
        "--output", default="work/probes/dual_filter_prototype.json"
    )
    args = parser.parse_args()
    if args.m < 2 or args.N < 1 or args.bits < 12 or args.external < 1:
        raise SystemExit("require m>=2, N>=1, bits>=12, external>=1")

    lines = util.read_lines(args.zeros_arb)
    needed = args.m + args.external
    if len(lines) < needed:
        raise SystemExit(f"need at least {needed} zero balls")
    balls = [parse_ball_fraction(line) for line in lines[:needed]]

    scale = 1 << args.bits
    rounded = []
    for index, midpoint, radius in balls:
        p = nearest_integer(scale * midpoint)
        error = abs(Fraction(p) - scale * midpoint) + scale * radius
        rounded.append({"index": index, "p": p, "error": error})

    selected = rounded[: args.m]
    external = rounded[args.m :]
    p = [row["p"] for row in selected]
    errors = [row["error"] for row in selected]

    base_error = sum(args.N * error for error in errors)
    weak_radii = []
    for j, error in enumerate(errors):
        coordinate_sq = (args.N + 1) ** 2 + (args.m - 1) * args.N**2
        relation_error = base_error + error
        weak_radii.append((j, Fraction(coordinate_sq) + relation_error**2))
    internal_radius_sq = max(radius for _, radius in weak_radii)

    external_rows = []
    for row in external:
        radius_sq = Fraction(args.m * args.N**2) + (base_error + row["error"]) ** 2
        external_rows.append({**row, "radius_sq": radius_sq})

    max_radius_sq = max([internal_radius_sq] + [row["radius_sq"] for row in external_rows])
    coefficient_radius_sq = math.floor(max_radius_sq)
    points = []
    for coefficients in integer_points_ball(args.m, coefficient_radius_sq):
        norm_sq = sum(value * value for value in coefficients)
        points.append((coefficients, norm_sq, dot(coefficients, p)))

    internal_min = None
    internal_arg = None
    for coefficients, norm_sq, relation in points:
        if not any(coefficients):
            continue
        value = norm_sq + relation * relation
        if internal_min is None or value < internal_min:
            internal_min = value
            internal_arg = coefficients

    delta, dual_rows = lll_short_dual_rows(p)
    dual_k = min(args.dual_k, args.m)

    filter_counts = {str(k): 0 for k in range(1, dual_k + 1)}
    results = []
    for row in external_rows:
        target_p = row["p"]
        radius_sq = row["radius_sq"]
        exact_min = None
        exact_arg = None
        for coefficients, norm_sq, relation in points:
            if norm_sq > radius_sq:
                continue
            value = norm_sq + (relation - target_p) ** 2
            if exact_min is None or value < exact_min:
                exact_min = value
                exact_arg = coefficients

        perpendicular_sq = Fraction(target_p * target_p, delta)
        dual_bounds = []
        for k in range(1, dual_k + 1):
            projected, metadata = exact_torus_lower_bound(
                dual_rows[:k], delta, target_p, args.dual_window
            )
            total = None if projected is None else perpendicular_sq + projected
            filtered = total is not None and total > radius_sq
            if filtered:
                filter_counts[str(k)] += 1
            if total is not None and exact_min is not None and total > exact_min:
                raise RuntimeError("dual lower bound exceeds exact primal distance")
            dual_bounds.append({
                "k": k,
                "projected_lower_sq": None if projected is None else str(projected),
                "total_lower_sq": None if total is None else str(total),
                "filtered": filtered,
                **metadata,
            })

        results.append({
            "index": row["index"],
            "radius_sq": str(radius_sq),
            "exact_cvp_min_sq": str(exact_min),
            "exact_cvp_arg": list(exact_arg) if exact_arg is not None else None,
            "exact_cvp_certifies": exact_min is not None and exact_min > radius_sq,
            "perpendicular_sq": str(perpendicular_sq),
            "dual_bounds": dual_bounds,
        })

    payload = {
        "schema": 1,
        "parameters": {
            "m": args.m,
            "N": args.N,
            "bits": args.bits,
            "external": args.external,
            "dual_k": dual_k,
            "dual_window": args.dual_window,
        },
        "selected_indices": [row["index"] for row in selected],
        "rounding_errors": [str(error) for error in errors],
        "internal_radius_sq": str(internal_radius_sq),
        "internal_exact_min_sq": str(internal_min),
        "internal_exact_arg": list(internal_arg) if internal_arg is not None else None,
        "internal_svp_certifies": internal_min is not None and internal_min > internal_radius_sq,
        "enumerated_primal_points": len(points),
        "dual_delta": str(delta),
        "dual_row_norm_squares": [str(row_norm_sq(row)) for row in dual_rows],
        "filter_counts": filter_counts,
        "external_results": results,
    }
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    util.atomic_write_json(args.output, payload)
    print(
        f"[DUAL-PROTOTYPE] m={args.m} N={args.N} bits={args.bits} "
        f"points={len(points)} internal={payload['internal_svp_certifies']}"
    )
    print(f"[DUAL-PROTOTYPE] filtered by k={filter_counts}")
    print(f"[DUAL-PROTOTYPE] wrote {args.output}")


if __name__ == "__main__":
    main()
