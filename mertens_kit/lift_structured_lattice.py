#!/usr/bin/env python3
"""Recover an exact row transform from a structured lattice and lift it.

The Hurst bases have one dense row followed by diagonal rows::

    [a_0 ... a_(n-1) 1]
    [d_0 ...       0 0]
    [0   d_1 ...   0 0]
    ...

For a reduced row ``r = u B``, ``u[0]`` is therefore ``r[-1]`` and every
remaining coefficient is recovered by one exact division.  This avoids a
general rational matrix inversion and, more importantly, gives explicit
divisibility and reconstruction checks before a warm basis is committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass

import util


@dataclass(frozen=True)
class StructuredBasis:
    rows: list[list[int]]
    dense: list[int]
    diagonal: list[int]
    dimension: int


def _load_meta(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        meta = json.load(handle)
    for key in ("stage", "mH", "NU", "NUY", "H"):
        if key not in meta:
            raise ValueError(f"{path}: missing metadata field {key}")
    return meta


def _structured_basis(path: str, meta: dict) -> StructuredBasis:
    n = int(meta["mH"])
    dim = n + 1
    rows = util.read_fplll_matrix(path, dim)
    if rows[0][-1] != 1:
        raise ValueError(f"{path}: dense row must end in 1")
    dense = rows[0][:-1]
    if len(dense) != n or any(value == 0 for value in dense):
        raise ValueError(f"{path}: first row is not dense")
    diagonal: list[int] = []
    for index, row in enumerate(rows[1:]):
        if row[-1] != 0:
            raise ValueError(f"{path}: diagonal row {index + 1} has tail")
        value = row[index]
        if value == 0:
            raise ValueError(f"{path}: diagonal entry {index} is zero")
        if any(entry != 0 for column, entry in enumerate(row[:-1])
               if column != index):
            raise ValueError(
                f"{path}: row {index + 1} is not diagonal"
            )
        diagonal.append(value)
    return StructuredBasis(rows, dense, diagonal, dim)


def validate_metadata(source: dict, target: dict) -> None:
    """Require the same active lattice and a genuine upward-NU lift."""
    # The existing NU=900 q-calibration parent was deliberately built under
    # ``bt2015`` (the decimal zero source is sufficient at 900 bits), while
    # NU=1900 must use the Arb-backed ``hurst`` stage.  This is the only
    # cross-stage bridge accepted by the lift tool.
    stages = (source["stage"], target["stage"])
    if stages[0] != stages[1] and stages != ("bt2015", "hurst"):
        raise ValueError(
            f"source/target metadata mismatch: stage ({stages[0]}->{stages[1]})"
        )
    for key in ("mH", "NUY", "H"):
        if source[key] != target[key]:
            raise ValueError(f"source/target metadata mismatch: {key}")
    if int(target["NU"]) <= int(source["NU"]):
        raise ValueError("target NU must be greater than source NU")
    if len(source["H"]) != int(source["mH"]):
        raise ValueError("source active set length does not match mH")
    if len(set(source["H"])) != len(source["H"]):
        raise ValueError("source active set contains duplicates")


def recover_transform(source: StructuredBasis,
                      reduced_rows: list[list[int]]) -> list[list[int]]:
    """Recover U from R=U*B and verify every division and reconstructed cell."""
    if len(reduced_rows) != source.dimension:
        raise ValueError("reduced checkpoint has the wrong row count")
    transform: list[list[int]] = []
    for row_index, row in enumerate(reduced_rows):
        if len(row) != source.dimension:
            raise ValueError(
                f"reduced checkpoint row {row_index} has wrong dimension"
            )
        dense_coefficient = row[-1]
        coefficients = [dense_coefficient]
        for column, divisor in enumerate(source.diagonal):
            numerator = row[column] - dense_coefficient*source.dense[column]
            quotient, remainder = divmod(numerator, divisor)
            if remainder:
                raise ValueError(
                    "non-exact transform division at "
                    f"row={row_index}, column={column}, remainder={remainder}"
                )
            coefficients.append(quotient)
        reconstructed = multiply_transform_row(coefficients, source)
        if reconstructed != row:
            differences = sum(
                left != right for left, right in zip(reconstructed, row)
            )
            raise ValueError(
                f"source reconstruction mismatch in row {row_index}: "
                f"{differences} cells"
            )
        transform.append(coefficients)
    return transform


def multiply_transform_row(coefficients: list[int],
                           basis: StructuredBasis) -> list[int]:
    dense_coefficient = coefficients[0]
    return [
        dense_coefficient*basis.dense[column]
        + coefficients[column + 1]*basis.diagonal[column]
        for column in range(basis.dimension - 1)
    ] + [dense_coefficient]


def multiply_transform(transform: list[list[int]],
                       basis: StructuredBasis) -> list[list[int]]:
    return [multiply_transform_row(row, basis) for row in transform]


def exact_determinant(transform: list[list[int]]) -> int:
    """Compute det(U) with python-flint's exact fmpz implementation."""
    try:
        from flint import fmpz_mat
    except ImportError:
        dependency = os.path.join(os.path.dirname(__file__), ".deps", "pip")
        if dependency not in sys.path:
            sys.path.insert(0, dependency)
        try:
            from flint import fmpz_mat
        except ImportError as exc:
            raise RuntimeError(
                "python-flint is required for the exact determinant check"
            ) from exc
    return int(fmpz_mat(transform).det())


def _hashes(paths: dict[str, str]) -> dict[str, dict[str, str]]:
    return {
        name: {"path": path, "sha256": util.sha256_file(path)}
        for name, path in paths.items()
    }


def lift(source_basis_path: str, source_meta_path: str,
         reduced_path: str, target_basis_path: str, target_meta_path: str,
         transform_path: str, warm_basis_path: str,
         manifest_path: str) -> dict:
    """Validate, recover, lift, and atomically commit a warm-start bundle."""
    source_meta = _load_meta(source_meta_path)
    target_meta = _load_meta(target_meta_path)
    validate_metadata(source_meta, target_meta)
    source = _structured_basis(source_basis_path, source_meta)
    target = _structured_basis(target_basis_path, target_meta)
    if source.dimension != target.dimension:
        raise ValueError("source/target basis dimensions differ")
    reduced = util.read_fplll_matrix(reduced_path, source.dimension)
    transform = recover_transform(source, reduced)
    determinant = exact_determinant(transform)
    if abs(determinant) != 1:
        raise ValueError(f"recovered transform is not unimodular: det={determinant}")
    warm = multiply_transform(transform, target)

    # Re-run the cheap structural products after determinant construction so a
    # mutable/aliased caller cannot invalidate the proof immediately before IO.
    if multiply_transform(transform, source) != reduced:
        raise ValueError("complete source reconstruction failed")
    if multiply_transform(transform, target) != warm:
        raise ValueError("complete target reconstruction failed")

    for path in (transform_path, warm_basis_path, manifest_path):
        if os.path.exists(path):
            raise FileExistsError(f"refusing to overwrite lift artifact: {path}")
    util.write_fplll_matrix(transform_path, transform)
    util.write_fplll_matrix(warm_basis_path, warm)
    manifest = {
        "schema": 1,
        "operation": "structured_unimodular_lift",
        "source_stage": source_meta["stage"],
        "target_stage": target_meta["stage"],
        "mH": int(source_meta["mH"]),
        "dimension": source.dimension,
        "source_NU": int(source_meta["NU"]),
        "target_NU": int(target_meta["NU"]),
        "NUY": int(source_meta["NUY"]),
        "active_set_sha256": hashlib.sha256(
            json.dumps(source_meta["H"], separators=(",", ":")).encode()
        ).hexdigest(),
        "determinant": str(determinant),
        "exact_division_remainders": 0,
        "source_reconstruction_differences": 0,
        "target_reconstruction_differences": 0,
        "parity": "VERIFIED",
        "inputs": _hashes({
            "source_basis": source_basis_path,
            "source_meta": source_meta_path,
            "source_reduced": reduced_path,
            "target_basis": target_basis_path,
            "target_meta": target_meta_path,
        }),
        "outputs": _hashes({
            "transform": transform_path,
            "warm_basis": warm_basis_path,
        }),
    }
    util.atomic_write_json(manifest_path, manifest)
    return manifest


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recover U from a reduced structured basis and lift U*B."
    )
    parser.add_argument("--source-basis", required=True)
    parser.add_argument("--source-meta", required=True)
    parser.add_argument("--source-reduced", required=True)
    parser.add_argument("--target-basis", required=True)
    parser.add_argument("--target-meta", required=True)
    parser.add_argument("--output-transform", required=True)
    parser.add_argument("--output-basis", required=True)
    parser.add_argument("--manifest", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    manifest = lift(
        args.source_basis, args.source_meta, args.source_reduced,
        args.target_basis, args.target_meta, args.output_transform,
        args.output_basis, args.manifest,
    )
    print(
        "[LIFT] "
        f"det={manifest['determinant']} "
        f"NU={manifest['source_NU']}->{manifest['target_NU']} "
        f"[PARITY {manifest['parity']}]"
    )


if __name__ == "__main__":
    main()
