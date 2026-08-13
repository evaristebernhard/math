#!/usr/bin/env python3
"""Regenerate and exactly check the Laurent--BKK certificate.

SciPy/Qhull is used only to propose hull vertices and a triangulation of the
boundary. Facet support and every determinant entering a volume are checked
over the integers or :class:`fractions.Fraction` before a value is accepted.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple

try:
    import numpy as np
    from scipy.spatial import ConvexHull
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "SciPy is required for convex-hull enumeration; install python3-scipy "
        "or `python3 -m pip install scipy`."
    ) from exc


Exponent = Tuple[int, int, int, int]
ParamExponent = Tuple[int, int, int, int, int, int, int, int]


@dataclass(frozen=True)
class Gaussian:
    re: Fraction = Fraction(0)
    im: Fraction = Fraction(0)

    @staticmethod
    def coerce(value: object) -> "Gaussian":
        if isinstance(value, Gaussian):
            return value
        return Gaussian(Fraction(value))

    def __add__(self, other: object) -> "Gaussian":
        other = self.coerce(other)
        return Gaussian(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self) -> "Gaussian":
        return Gaussian(-self.re, -self.im)

    def __sub__(self, other: object) -> "Gaussian":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "Gaussian":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "Gaussian":
        other = self.coerce(other)
        return Gaussian(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def conjugate(self) -> "Gaussian":
        return Gaussian(self.re, -self.im)

    def __bool__(self) -> bool:
        return bool(self.re or self.im)


ZERO_PARAM: ParamExponent = (0,) * 8


class Coefficient:
    """Laurent polynomial in (alpha,beta,p,cm,cmb,cp,cpb,m)."""

    def __init__(self, terms: Mapping[ParamExponent, Gaussian] | None = None):
        self.terms: Dict[ParamExponent, Gaussian] = {
            e: c for e, c in (terms or {}).items() if c
        }

    @staticmethod
    def scalar(value: object) -> "Coefficient":
        value = Gaussian.coerce(value)
        return Coefficient({ZERO_PARAM: value}) if value else Coefficient()

    @staticmethod
    def parameter(index: int) -> "Coefficient":
        exponent = [0] * 8
        exponent[index] = 1
        return Coefficient({tuple(exponent): Gaussian(1)})

    @staticmethod
    def coerce(value: object) -> "Coefficient":
        return value if isinstance(value, Coefficient) else Coefficient.scalar(value)

    def __add__(self, other: object) -> "Coefficient":
        other = self.coerce(other)
        result = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            result[exponent] = result.get(exponent, Gaussian()) + coefficient
            if not result[exponent]:
                del result[exponent]
        return Coefficient(result)

    __radd__ = __add__

    def __neg__(self) -> "Coefficient":
        return Coefficient({e: -c for e, c in self.terms.items()})

    def __sub__(self, other: object) -> "Coefficient":
        return self + (-self.coerce(other))

    def __rsub__(self, other: object) -> "Coefficient":
        return self.coerce(other) - self

    def __mul__(self, other: object) -> "Coefficient":
        other = self.coerce(other)
        result: Dict[ParamExponent, Gaussian] = {}
        for left_exp, left_coefficient in self.terms.items():
            for right_exp, right_coefficient in other.terms.items():
                exponent = tuple(a + b for a, b in zip(left_exp, right_exp))
                result[exponent] = result.get(exponent, Gaussian()) + left_coefficient * right_coefficient
                if not result[exponent]:
                    del result[exponent]
        return Coefficient(result)

    __rmul__ = __mul__

    def star(self) -> "Coefficient":
        result: Dict[ParamExponent, Gaussian] = {}
        for exponent, coefficient in self.terms.items():
            alpha, beta, p, cm, cmb, cp, cpb, amplitude = exponent
            starred = (alpha, beta, -p, cmb, cm, cpb, cp, amplitude)
            result[starred] = result.get(starred, Gaussian()) + coefficient.conjugate()
        return Coefficient(result)

    def __bool__(self) -> bool:
        return bool(self.terms)


ZERO: Exponent = (0, 0, 0, 0)
Laurent = Dict[Exponent, Coefficient]


def monomial(exponent: Exponent = ZERO, coefficient: object = 1) -> Laurent:
    coefficient = Coefficient.coerce(coefficient)
    return {exponent: coefficient} if coefficient else {}


def add(*polynomials: Laurent) -> Laurent:
    result: Laurent = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, Coefficient()) + coefficient
            if not result[exponent]:
                del result[exponent]
    return result


def scale(polynomial: Laurent, coefficient: object) -> Laurent:
    coefficient = Coefficient.coerce(coefficient)
    return {e: c * coefficient for e, c in polynomial.items() if c * coefficient}


def subtract(left: Laurent, right: Laurent) -> Laurent:
    return add(left, scale(right, -1))


def multiply(left: Laurent, right: Laurent) -> Laurent:
    result: Laurent = {}
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exp, right_exp))
            coefficient = left_coefficient * right_coefficient
            result[exponent] = result.get(exponent, Coefficient()) + coefficient
            if not result[exponent]:
                del result[exponent]
    return result


def power(polynomial: Laurent, exponent: int) -> Laurent:
    result = monomial()
    for _ in range(exponent):
        result = multiply(result, polynomial)
    return result


def power_coefficient(coefficient: Coefficient, exponent: int) -> Coefficient:
    result = Coefficient.scalar(1)
    for _ in range(exponent):
        result *= coefficient
    return result


def star(polynomial: Laurent) -> Laurent:
    return {(-a, -b, c, d): coefficient.star() for (a, b, c, d), coefficient in polynomial.items()}


def imaginary_pair(left: Laurent, right: Laurent) -> Laurent:
    return scale(
        subtract(multiply(left, star(right)), multiply(star(left), right)),
        Gaussian(0, Fraction(-1, 2)),
    )


def real_pair_twice(left: Laurent, right: Laurent) -> Laurent:
    return add(multiply(left, star(right)), multiply(star(left), right))


def divide_by_R_minus_one(polynomial: Laurent, multiplicity: int) -> Laurent:
    """Exact sparse division in the coefficient ring; assert zero remainder."""
    quotient = polynomial
    for _ in range(multiplicity):
        groups: Dict[Tuple[int, int, int], Dict[int, Coefficient]] = {}
        for (a, b, c, d), coefficient in quotient.items():
            groups.setdefault((a, b, d), {})[c] = coefficient
        next_quotient: Laurent = {}
        for (a, b, d), coefficients in groups.items():
            coefficients = dict(coefficients)
            group_quotient: Dict[int, Coefficient] = {}
            while coefficients and max(coefficients) >= 1:
                degree = max(coefficients)
                leading = coefficients.pop(degree)
                quotient_degree = degree - 1
                group_quotient[quotient_degree] = group_quotient.get(quotient_degree, Coefficient()) + leading
                coefficients[quotient_degree] = coefficients.get(quotient_degree, Coefficient()) + leading
                if not coefficients[quotient_degree]:
                    del coefficients[quotient_degree]
            if coefficients:
                raise AssertionError("nonzero remainder in division by R-1")
            for degree, coefficient in group_quotient.items():
                if coefficient:
                    next_quotient[(a, b, degree, d)] = coefficient
        quotient = next_quotient
    return quotient


def basic_supports() -> Tuple[Set[Exponent], Set[Exponent], dict]:
    one = monomial()
    z = monomial((1, 0, 0, 0))
    w = monomial((0, 1, 0, 0))
    R = monomial((0, 0, 1, 0))
    S = monomial((0, 0, 0, 1))
    alpha, beta, p, cm, _cmb, cp, _cpb, amplitude = [Coefficient.parameter(i) for i in range(8)]

    U = scale(
        subtract(
            multiply(subtract(z, R), subtract(scale(R, alpha), one)),
            multiply(w, multiply(subtract(scale(R, alpha * p), z), subtract(one, R))),
        ), cm,
    )
    V = add(
        scale(multiply(subtract(z, R), subtract(scale(one, beta), S)), cm),
        scale(multiply(subtract(scale(one, beta), scale(multiply(S, w), p)), subtract(one, R)), -cp),
    )
    Ahat = add(
        scale(multiply(subtract(z, R), subtract(S, one)), cm),
        scale(multiply(multiply(z, subtract(multiply(S, w), one)), subtract(one, R)), -cp),
    )
    D_A = multiply(subtract(one, R), subtract(S, one))
    D_V = multiply(subtract(one, R), subtract(scale(one, beta), S))
    F0 = add(
        multiply(multiply(R, D_A), imaginary_pair(U, V)),
        multiply(multiply(multiply(R, subtract(one, scale(one, alpha))), subtract(one, R)), imaginary_pair(Ahat, V)),
        multiply(D_V, imaginary_pair(Ahat, U)),
    )
    F = divide_by_R_minus_one(F0, 3)
    try:
        divide_by_R_minus_one(F0, 4)
    except AssertionError:
        fourth_power_divides = False
    else:
        fourth_power_divides = True

    pair_determinant = subtract(multiply(U, star(V)), multiply(star(U), V))
    G0 = add(
        scale(multiply(power(R, 2), multiply(V, star(V))), power_coefficient(1 - alpha, 2)),
        multiply(power(subtract(scale(one, beta), S), 2), multiply(U, star(U))),
        scale(multiply(multiply(R, subtract(scale(one, beta), S)), real_pair_twice(U, V)), 1 - alpha),
        scale(power(pair_determinant, 2), amplitude),
    )
    G = divide_by_R_minus_one(G0, 2)
    return set(F), set(G), {
        "F0_term_count": len(F0),
        "F0_divisible_by_R_minus_1_power": 3,
        "F0_divisible_by_fourth_power": fourth_power_divides,
        "G0_term_count": len(G0),
        "G0_divisible_by_R_minus_1_power": 2,
    }


def minkowski_support(*supports: Iterable[Exponent]) -> Set[Exponent]:
    result: Set[Exponent] = {ZERO}
    for support in supports:
        result = {tuple(a + b for a, b in zip(left, right)) for left in result for right in support}
    return result


def euler_support(support: Set[Exponent], angle: int, exponential: int) -> Set[Exponent]:
    return {point for point in support if point[angle] != 0 or point[exponential] != 0}


def partial_support(support: Set[Exponent], coordinate: int) -> Set[Exponent]:
    result = set()
    for point in support:
        if point[coordinate] != 0:
            shifted = list(point)
            shifted[coordinate] -= 1
            result.add(tuple(shifted))
    return result


def determinant3_support(rows: Sequence[Sequence[Set[Exponent]]]) -> Set[Exponent]:
    result: Set[Exponent] = set()
    for permutation in itertools.permutations(range(3)):
        result |= minkowski_support(*(rows[row][permutation[row]] for row in range(3)))
    return result


def contact_support(F: Set[Exponent], G: Set[Exponent], Q: Set[Exponent]) -> Set[Exponent]:
    derivatives = [[partial_support(P, coordinate) for coordinate in range(4)] for P in (F, G, Q)]
    z_w_S = determinant3_support([[row[0], row[1], row[3]] for row in derivatives])
    w_R_S = determinant3_support([[row[1], row[2], row[3]] for row in derivatives])
    return z_w_S | minkowski_support({(-1, 0, 1, 0)}, w_R_S)


def propagated_supports() -> Tuple[Dict[str, Set[Exponent]], dict]:
    F, G, algebra = basic_supports()
    H2 = minkowski_support(euler_support(F, 0, 2), euler_support(G, 1, 3))
    H2 |= minkowski_support(euler_support(F, 1, 3), euler_support(G, 0, 2))
    H1_raw = contact_support(F, G, H2)
    H1 = {(a, b, c, d - 1) for a, b, c, d in H1_raw}
    P = minkowski_support({(0, 0, 0, 0), (2, 0, 0, 0)}, {(0, 0, 0, 0), (0, 2, 0, 0)}, {(0, 0, 1, 1)})
    P |= minkowski_support(
        {(1, 1, 0, 0)},
        {(0, 0, 0, 0), (0, 0, 1, 0), (0, 0, 2, 0)},
        {(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, 2)},
    )
    Hc_raw = contact_support(F, G, P)
    Hc = {(a, b, c, d - 1) for a, b, c, d in Hc_raw}
    return {"F": F, "G": G, "H2": H2, "H1_tilde": H1, "P_epsilon": P, "Hc_tilde": Hc}, algebra


def determinant(matrix: Sequence[Sequence[object]]) -> object:
    if len(matrix) == 1:
        return matrix[0][0]
    result = 0
    for column in range(len(matrix)):
        minor = [list(row[:column]) + list(row[column + 1 :]) for row in matrix[1:]]
        result += ((-1) ** column) * matrix[0][column] * determinant(minor)
    return result


def affine_rank(points: Sequence[Exponent]) -> int:
    if len(points) <= 1:
        return 0
    matrix = [[Fraction(b - a) for a, b in zip(points[0], point)] for point in points[1:]]
    rank = 0
    for column in range(4):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column]:
                factor = matrix[row][column]
                matrix[row] = [value - factor * base for value, base in zip(matrix[row], matrix[rank])]
        rank += 1
    return rank


def hull_vertices(points: Iterable[Exponent]) -> List[Exponent]:
    points = sorted(set(points))
    if affine_rank(points) < 4:
        return points
    hull = ConvexHull(np.asarray(points, dtype=float))
    vertices = [points[index] for index in sorted(set(map(int, hull.vertices)))]
    # Recheck the proposed hull against every original lattice point.  This
    # keeps floating point out of the accepted face incidences.
    vertex_hull = ConvexHull(np.asarray(vertices, dtype=float))
    for simplex in vertex_hull.simplices:
        facet = [vertices[int(index)] for index in simplex]
        normal = primitive_normal(facet)
        if normal is None:
            continue
        offset = sum(normal[i] * facet[0][i] for i in range(4))
        signs = [sum(normal[i] * point[i] for i in range(4)) - offset for point in points]
        if not (all(value <= 0 for value in signs) or all(value >= 0 for value in signs)):
            raise AssertionError("Qhull vertex set fails exact support containment")
    return vertices


def primitive_normal(facet: Sequence[Exponent]) -> Tuple[int, int, int, int] | None:
    base = facet[0]
    edges = [[point[i] - base[i] for i in range(4)] for point in facet[1:]]
    normal = []
    for column in range(4):
        minor = [row[:column] + row[column + 1 :] for row in edges]
        normal.append(((-1) ** column) * int(determinant(minor)))
    divisor = math.gcd(*(abs(value) for value in normal))
    if divisor == 0:
        # Qhull may emit zero-volume simplices while triangulating a
        # nonsimplicial rational facet.  They make no volume contribution.
        return None
    return tuple(value // divisor for value in normal)


def exact_normalized_volume(points: Iterable[Exponent]) -> Tuple[Fraction, int, int]:
    vertices = hull_vertices(points)
    if affine_rank(vertices) < 4:
        return Fraction(0), len(vertices), 0
    hull = ConvexHull(np.asarray(vertices, dtype=float))
    centre = tuple(Fraction(sum(point[i] for point in vertices), len(vertices)) for i in range(4))
    total = Fraction(0)
    checked_facets = 0
    for simplex in hull.simplices:
        facet = [vertices[int(index)] for index in simplex]
        normal = primitive_normal(facet)
        if normal is None:
            continue
        offset = sum(normal[i] * facet[0][i] for i in range(4))
        signs = [sum(normal[i] * point[i] for i in range(4)) - offset for point in vertices]
        if not (all(value <= 0 for value in signs) or all(value >= 0 for value in signs)):
            raise AssertionError("Qhull facet fails exact supporting-hyperplane check")
        edge_matrix = [[Fraction(point[i]) - centre[i] for i in range(4)] for point in facet]
        simplex_determinant = determinant(edge_matrix)
        if simplex_determinant == 0:
            continue
        total += abs(simplex_determinant)
        checked_facets += 1
    if total.denominator != 1:
        raise AssertionError(f"normalized lattice volume is not integral: {total}")
    return total, len(vertices), checked_facets


def minkowski_vertices(polytopes: Sequence[Sequence[Exponent]]) -> List[Exponent]:
    vertices: List[Exponent] = [ZERO]
    for polytope in polytopes:
        candidates = {tuple(a + b for a, b in zip(left, right)) for left in vertices for right in polytope}
        vertices = hull_vertices(candidates)
    return vertices


def mixed_volume_certificate(names: Sequence[str], vertices: Mapping[str, Sequence[Exponent]]) -> dict:
    rows = []
    polarization = Fraction(0)
    for mask in range(1, 1 << 4):
        chosen = [names[index] for index in range(4) if mask & (1 << index)]
        sum_vertices = minkowski_vertices([vertices[name] for name in chosen])
        volume, vertex_count, facet_count = exact_normalized_volume(sum_vertices)
        polarization += ((-1) ** (4 - len(chosen))) * volume
        rows.append({
            "subset": chosen,
            "normalized_volume": int(volume),
            "vertex_count": vertex_count,
            "boundary_simplex_count": facet_count,
        })
    if polarization.denominator != 1 or int(polarization) % math.factorial(4):
        raise AssertionError(f"invalid polarization sum {polarization}")
    return {
        "polytopes": list(names),
        "minkowski_sums": rows,
        "normalized_polarization_sum": int(polarization),
        "mixed_volume": int(polarization) // math.factorial(4),
    }


EXPECTED_STATS = {
    "F": (36, 16), "G": (265, 24), "H2": (1154, 52),
    "H1_tilde": (12360, 54), "P_epsilon": (13, 8), "Hc_tilde": (2692, 74),
}
SYSTEMS = {
    "B0": ("F", "G", "H2", "H1_tilde"),
    "B1": ("F", "G", "P_epsilon", "Hc_tilde"),
    "B2": ("F", "G", "H2", "P_epsilon"),
}
EXPECTED_POLARIZATIONS = {"B0": 163392, "B1": 37632, "B2": 29952}
EXPECTED_MIXED_VOLUMES = {"B0": 6808, "B1": 1568, "B2": 1248}


def build_certificate() -> dict:
    supports, algebra = propagated_supports()
    vertices = {name: hull_vertices(support) for name, support in supports.items()}
    stats = {name: {"support_size": len(supports[name]), "vertex_count": len(vertices[name])} for name in supports}
    actual_stats = {name: (row["support_size"], row["vertex_count"]) for name, row in stats.items()}
    if actual_stats != EXPECTED_STATS:
        raise AssertionError(f"support statistics mismatch: {actual_stats!r}")
    systems = {name: mixed_volume_certificate(tuple_names, vertices) for name, tuple_names in SYSTEMS.items()}
    polarizations = {name: row["normalized_polarization_sum"] for name, row in systems.items()}
    mixed_volumes = {name: row["mixed_volume"] for name, row in systems.items()}
    if polarizations != EXPECTED_POLARIZATIONS:
        raise AssertionError(f"polarization mismatch: {polarizations!r}")
    if mixed_volumes != EXPECTED_MIXED_VOLUMES:
        raise AssertionError(f"mixed-volume mismatch: {mixed_volumes!r}")
    return {
        "schema": "pwl-three-zone-laurent-bkk-certificate-v1",
        "variables": ["z", "w", "R", "S"],
        "normalization": {
            "lattice_volume": "4! times Euclidean volume",
            "mixed_volume": "normalized polarization sum divided by 4!",
        },
        "algebra": algebra,
        "statistics": stats,
        "supports": {name: [list(point) for point in sorted(support)] for name, support in supports.items()},
        "vertices": {name: [list(point) for point in vertex_list] for name, vertex_list in vertices.items()},
        "systems": systems,
        "conclusion": {"regular_positive_three_zone_bound": 8216, "calculation": "6808 + (1568 + 1248)/2 = 8216"},
    }


def serialized(certificate: dict) -> bytes:
    return (json.dumps(certificate, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="regenerate and compare byte-for-byte with this JSON certificate")
    parser.add_argument("--output", type=Path, help="write the regenerated certificate")
    arguments = parser.parse_args()
    data = serialized(build_certificate())
    if arguments.check:
        if arguments.check.read_bytes() != data:
            raise SystemExit(f"certificate mismatch: regenerate with --output {arguments.check}")
        print(f"certificate verified byte-for-byte: {arguments.check}")
    elif arguments.output:
        arguments.output.write_bytes(data)
        print(f"certificate written: {arguments.output}")
    else:
        print(data.decode("utf-8"), end="")
    print("support/vertex counts: " + ", ".join(f"{n}={s}/{v}" for n, (s, v) in EXPECTED_STATS.items()))
    print("normalized polarization sums: 163392, 37632, 29952")
    print("mixed volumes: 6808, 1568, 1248")
    print("regular positive three-zone bound: 8216")


if __name__ == "__main__":
    main()
