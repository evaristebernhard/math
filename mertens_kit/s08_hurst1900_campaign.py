#!/usr/bin/env python3
"""Single-core NU=1900 Hurst campaign with exact NU=900 warm starts."""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict

import audit_core
import config
import lift_structured_lattice
import model_core
import reduction
import s05_certify
import util
from s06_probe import backend_command, reduction_available_memory


TARGET = model_core.HURST_TARGET
PROGRESS_INTERVAL = 60.0


def remaining(deadline):
    return max(0.0, deadline-time.time())


def require_time(deadline, operation):
    value = remaining(deadline)
    if value <= 0:
        raise TimeoutError(f"wall deadline before {operation}")
    return value


def h_fingerprint(meta):
    return hashlib.sha256(
        json.dumps(meta["H"], separators=(",", ":")).encode()
    ).hexdigest()


def wait_for_memory(deadline, reserve_bytes):
    while reduction_available_memory() < reserve_bytes + 256*2**20:
        if remaining(deadline) <= 0:
            raise TimeoutError("memory reserve wait reached wall deadline")
        time.sleep(2)


def _load_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _next_number(directory, stem, suffix):
    expression = re.compile(
        rf"^{re.escape(stem)}(\d{{3}}){re.escape(suffix)}"
        rf"(?:\.run\.json|\.progress\.jsonl)?$"
    )
    temporary = re.compile(
        rf"^\.{re.escape(stem)}(\d{{3}}){re.escape(suffix)}\..*\.tmp"
        rf"(?:\.err)?$"
    )
    numbers = []
    for name in os.listdir(directory):
        match = expression.match(name) or temporary.match(name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=-1)+1


def _new_numbered_path(directory, stem, suffix):
    number = _next_number(directory, stem, suffix)
    return os.path.join(directory, f"{stem}{number:03d}{suffix}")


def _valid_hashed_file(path, digest, dim=None):
    if not path or not os.path.exists(path):
        return False
    if dim is not None and not util.validate_fplll_matrix(path, dim):
        return False
    return util.sha256_file(path) == digest


def prepare_base(root, mH, nu, deadline, resume):
    """Build or reuse a raw-order structured basis; never shuffle it."""
    directory = os.path.join(root, f"m{mH}_n{nu}")
    os.makedirs(directory, exist_ok=True)
    prefix = os.path.join(directory, "base")
    raw_basis, meta_path = prefix+"_basis.txt", prefix+"_meta.json"
    dim = mH+1
    if not (resume and util.validate_fplll_matrix(raw_basis, dim)
            and os.path.exists(meta_path)):
        subprocess.run([
            sys.executable, "s02_build_lattice.py", "hurst",
            "--mH", str(mH), "--nu", str(nu), "--output-prefix", prefix,
        ], check=True, timeout=require_time(deadline, "lattice build"),
           env={**os.environ, **reduction.THREAD_ENV})
    meta = _load_json(meta_path)
    if (meta.get("stage") != "hurst" or int(meta["mH"]) != mH
            or int(meta["NU"]) != nu):
        raise RuntimeError("resumed meta does not match campaign parameters")
    return {
        "mH": mH, "NU": nu, "dimension": dim, "directory": directory,
        "basis": raw_basis, "meta": meta_path,
        "basis_sha256": util.sha256_file(raw_basis),
        "meta_sha256": util.sha256_file(meta_path),
        "H_sha256": h_fingerprint(meta),
        "raw_order": True,
    }


def _reusable_attempt(directory, stem, dim, metadata):
    """Find an accepted immutable attempt whose parent metadata still matches."""
    for sidecar in sorted(
            glob.glob(os.path.join(directory, f"{stem}[0-9][0-9][0-9].txt.run.json")),
            reverse=True):
        try:
            payload = _load_json(sidecar)
            attempt_meta = payload.get("metadata", {})
            checkpoint = sidecar[:-len(".run.json")]
            if (payload.get("accepted")
                    and all(attempt_meta.get(k) == v
                            for k, v in metadata.items())
                    and util.validate_fplll_matrix(checkpoint, dim)):
                return checkpoint, payload
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            continue
    return None, None


def run_raw_parent_lll(instance, deadline, resume, reserve_bytes, cap_hours):
    """Produce the NU=900 parent LLL directly from raw B900."""
    metadata = {
        "campaign": "hurst1900_warm",
        "step": "warm_parent_lll",
        "mH": instance["mH"], "NU": instance["NU"],
        "input_sha256": instance["basis_sha256"], "raw_order": True,
    }
    if resume:
        checkpoint, payload = _reusable_attempt(
            instance["directory"], "parent_lll_attempt",
            instance["dimension"], metadata,
        )
        if checkpoint:
            return checkpoint, [{"resumed": True, **payload}]
    wait_for_memory(deadline, reserve_bytes)
    output = _new_numbered_path(
        instance["directory"], "parent_lll_attempt", ".txt"
    )
    result = reduction.run_fplll(
        ["fplll", "-a", "lll", "-m", "wrapper"],
        instance["basis"], output, instance["dimension"],
        timeout=min(require_time(deadline, "NU900 parent LLL"),
                    cap_hours*3600),
        metadata=metadata,
        progress_interval=PROGRESS_INTERVAL,
        progress_label=f"m{instance['mH']} NU{instance['NU']} parent wrapper",
    )
    record = asdict(result)
    if not result.accepted:
        raise RuntimeError(f"NU900 parent LLL failed: {result.status}")
    return output, [record]


def _find_lift_manifest(directory, source, target, dim):
    for path in sorted(
            glob.glob(os.path.join(directory, "lift[0-9][0-9][0-9].json")),
            reverse=True):
        try:
            payload = _load_json(path)
            inputs, outputs = payload["inputs"], payload["outputs"]
            expected = {
                "source_basis": source["basis"],
                "source_meta": source["meta"],
                "source_reduced": source["lll"],
                "target_basis": target["basis"],
                "target_meta": target["meta"],
            }
            if payload.get("parity") != "VERIFIED":
                continue
            if any(inputs[name]["sha256"] != util.sha256_file(value)
                   for name, value in expected.items()):
                continue
            transform = outputs["transform"]["path"]
            warm = outputs["warm_basis"]["path"]
            if (_valid_hashed_file(transform, outputs["transform"]["sha256"], dim)
                    and _valid_hashed_file(
                        warm, outputs["warm_basis"]["sha256"], dim)):
                return path, payload
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            continue
    return None, None


def lift_instance(source, target, resume):
    """Create or reuse an immutable U/B1900/manifest bundle."""
    source = dict(source)
    source["lll_sha256"] = util.sha256_file(source["lll"])
    if resume:
        manifest_path, manifest = _find_lift_manifest(
            target["directory"], source, target, target["dimension"]
        )
        if manifest_path:
            return {
                "manifest": manifest_path, "manifest_payload": manifest,
                "transform": manifest["outputs"]["transform"]["path"],
                "warm_basis": manifest["outputs"]["warm_basis"]["path"],
                "warm_basis_sha256":
                    manifest["outputs"]["warm_basis"]["sha256"],
                "parity": manifest["parity"], "resumed": True,
            }
    occupied = []
    patterns = (
        re.compile(r"^lift(\d{3})\.json$"),
        re.compile(r"^lift_transform(\d{3})\.txt$"),
        re.compile(r"^warm_basis(\d{3})\.txt$"),
    )
    for name in os.listdir(target["directory"]):
        for pattern in patterns:
            match = pattern.match(name)
            if match:
                occupied.append(int(match.group(1)))
                break
    number = max(occupied, default=-1)+1
    transform = os.path.join(
        target["directory"], f"lift_transform{number:03d}.txt"
    )
    warm = os.path.join(
        target["directory"], f"warm_basis{number:03d}.txt"
    )
    manifest_path = os.path.join(
        target["directory"], f"lift{number:03d}.json"
    )
    manifest = lift_structured_lattice.lift(
        source["basis"], source["meta"], source["lll"],
        target["basis"], target["meta"], transform, warm, manifest_path,
    )
    return {
        "manifest": manifest_path, "manifest_payload": manifest,
        "transform": transform, "warm_basis": warm,
        "warm_basis_sha256": manifest["outputs"]["warm_basis"]["sha256"],
        "parity": manifest["parity"], "resumed": False,
    }


def _find_cleanup_manifest(instance, lift):
    dim = instance["dimension"]
    for path in sorted(glob.glob(os.path.join(
            instance["directory"], "cleanup[0-9][0-9][0-9].json")),
            reverse=True):
        try:
            payload = _load_json(path)
            checkpoint = payload["wrapper_checkpoint"]
            if (payload.get("warm_basis_sha256") == lift["warm_basis_sha256"]
                    and payload.get("wrapper_completed") is True
                    and _valid_hashed_file(
                        checkpoint, payload["wrapper_checkpoint_sha256"], dim)):
                return path, payload
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            continue
    return None, None


def lll_complexity_estimate(dimension, source_nu, target_nu,
                            measured_source_seconds,
                            reference_dimension=None):
    """Return a transparent scaling envelope, not a completion guarantee.

    Classical LLL bit-complexity is polynomial in dimension and input bit
    length.  Floating implementations and swap counts make the exact exponent
    instance-dependent, so the campaign reports b^2/b^3/b^4 envelopes and
    uses d^5 only when extrapolating across dimensions.
    """
    reference_dimension = reference_dimension or dimension
    dimension_ratio = dimension/reference_dimension
    bit_ratio = target_nu/source_nu
    estimates = {
        f"bit_power_{power}_seconds":
            measured_source_seconds*(dimension_ratio**5)*(bit_ratio**power)
        for power in (2, 3, 4)
    }
    return {
        "model": "T ~= T0*(d/d0)^5*(target_NU/source_NU)^p",
        "warning": (
            "complexity envelope only; backend precision, LLL swaps and "
            "conditioning determine the actual completion time"
        ),
        "dimension": dimension,
        "reference_dimension": reference_dimension,
        "source_NU": source_nu, "target_NU": target_nu,
        "measured_source_seconds": measured_source_seconds,
        **estimates,
    }


def empirical_dimension_fit(samples, target_dimension):
    """Fit T=c*d^q to same-NU wrapper observations in log space."""
    if len(samples) < 2:
        raise ValueError("at least two dimension timing samples are required")
    logs = [(math.log(float(d)), math.log(float(seconds)))
            for d, seconds in samples]
    x_mean = sum(x for x, _ in logs)/len(logs)
    y_mean = sum(y for _, y in logs)/len(logs)
    denominator = sum((x-x_mean)**2 for x, _ in logs)
    if denominator == 0:
        raise ValueError("dimension timing samples must have distinct dimensions")
    exponent = (
        sum((x-x_mean)*(y-y_mean) for x, y in logs)/denominator
    )
    coefficient = math.exp(y_mean-exponent*x_mean)
    return {
        "model": "T=c*d^q (empirical, same NU/backend)",
        "samples": [
            {"dimension": int(d), "seconds": float(seconds)}
            for d, seconds in samples
        ],
        "dimension_exponent_q": exponent,
        "coefficient_c": coefficient,
        "target_dimension": int(target_dimension),
        "predicted_seconds": coefficient*target_dimension**exponent,
    }


def campaign_complexity_plan(baseline_path, main_m, source_nu, target_nu):
    """Use q-calibration sidecars to plan m800 before starting it."""
    root = os.path.dirname(baseline_path)
    samples = []
    for mH in (260, 360, 460):
        sidecar = os.path.join(
            root, f"m{mH}_n{source_nu}", "lll.txt.run.json"
        )
        if os.path.exists(sidecar):
            payload = _load_json(sidecar)
            if payload.get("accepted"):
                samples.append((mH+1, float(payload["seconds"])))
    fit = empirical_dimension_fit(samples, main_m+1)
    target = lll_complexity_estimate(
        main_m+1, source_nu, target_nu, fit["predicted_seconds"]
    )
    return {"parent_dimension_fit": fit, "target_bit_envelope": target}


def _reusable_cleanup_parent(instance, lift):
    """Resume from the newest complete heuristic output, accepted or partial."""
    candidates = sorted(glob.glob(os.path.join(
        instance["directory"], "lll_attempt[0-9][0-9][0-9].txt.run.json"
    )), reverse=True)
    for sidecar in candidates:
        try:
            payload = _load_json(sidecar)
            metadata = payload.get("metadata", {})
            checkpoint = sidecar[:-len(".run.json")]
            command = payload.get("command", [])
            if (metadata.get("warm_basis_sha256")
                    != lift["warm_basis_sha256"]
                    or metadata.get("step") != "heuristic_cleanup"
                    or not payload.get("output_valid")
                    or not util.validate_fplll_matrix(
                        checkpoint, instance["dimension"])):
                continue
            backend = (
                command[command.index("-f")+1] if "-f" in command else None
            )
            return checkpoint, backend, payload
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            continue
    return None, None, None


def run_warm_cleanup(instance, lift, deadline, resume, reserve_bytes,
                     cap_hours):
    """Heuristic LD -> heuristic MPFR-256 fallback -> mandatory wrapper."""
    if resume:
        manifest_path, manifest = _find_cleanup_manifest(instance, lift)
        if manifest_path:
            return manifest["wrapper_checkpoint"], manifest_path, manifest

    dim = instance["dimension"]
    parent = lift["warm_basis"]
    runs = []
    cleanup_budget = min(remaining(deadline), cap_hours*3600)
    cleanup_deadline = time.time()+cleanup_budget
    resumed_backend = None
    if resume:
        reusable, resumed_backend, payload = _reusable_cleanup_parent(
            instance, lift
        )
        if reusable:
            parent = reusable
            runs.append({"resumed": True, **payload})
            print(
                f"[H1900-WARM] resume cleanup from {reusable} "
                f"backend={resumed_backend}",
                flush=True,
            )
    heuristic_commands = [
        (["fplll", "-a", "lll", "-m", "heuristic", "-f", "longdouble"],
         min(12*60, cleanup_budget*0.20)),
        (["fplll", "-a", "lll", "-m", "heuristic",
          "-f", "mpfr", "-p", "256"], min(10*60, cleanup_budget*0.20)),
    ]
    for command, attempt_budget in heuristic_commands:
        backend = command[command.index("-f")+1]
        if resumed_backend == "mpfr":
            continue
        if resumed_backend == "longdouble" and backend == "longdouble":
            continue
        wait_for_memory(deadline, reserve_bytes)
        output = _new_numbered_path(
            instance["directory"], "lll_attempt", ".txt"
        )
        result = reduction.run_fplll(
            command, parent, output, dim,
            timeout=min(
                require_time(deadline, "warm heuristic cleanup"),
                max(0.1, attempt_budget),
            ),
            metadata={
                "campaign": "hurst1900_warm", "step": "heuristic_cleanup",
                "mH": instance["mH"], "NU": instance["NU"],
                "input_sha256": util.sha256_file(parent),
                "warm_basis_sha256": lift["warm_basis_sha256"],
            },
            retain_valid_failure=True,
            progress_interval=PROGRESS_INTERVAL,
            progress_label=(
                f"m{instance['mH']} NU{instance['NU']} "
                f"heuristic-{backend}"
            ),
        )
        runs.append(asdict(result))
        if result.accepted:
            parent = output
            break
        if result.output_valid and result.output:
            # fplll can report "infinite loop in babai" after printing a
            # complete, partially reduced matrix.  It is not accepted as the
            # final checkpoint, but it is strictly better evidence and the
            # next backend/wrapper must continue from it rather than restart.
            parent = output
            print(
                f"[H1900-WARM] retained complete provisional matrix "
                f"from {backend}: {output}",
                flush=True,
            )

    # A failed heuristic is only an optimization failure.  Wrapper is always
    # attempted, from the last complete matrix (or the exact warm basis).
    wrapper_parent_sha256 = util.sha256_file(parent)
    wait_for_memory(deadline, reserve_bytes)
    wrapper_output = _new_numbered_path(
        instance["directory"], "lll_attempt", ".txt"
    )
    wrapper = reduction.run_fplll(
        ["fplll", "-a", "lll", "-m", "wrapper"],
        parent, wrapper_output, dim,
        timeout=min(
            require_time(deadline, "mandatory wrapper LLL"),
            max(0.1, cleanup_deadline-time.time()),
        ),
        metadata={
            "campaign": "hurst1900_warm", "step": "wrapper_cleanup",
            "mH": instance["mH"], "NU": instance["NU"],
            "input_sha256": wrapper_parent_sha256,
            "warm_basis_sha256": lift["warm_basis_sha256"],
        },
        progress_interval=PROGRESS_INTERVAL,
        progress_label=f"m{instance['mH']} NU{instance['NU']} wrapper",
    )
    runs.append(asdict(wrapper))
    manifest_path = _new_numbered_path(
        instance["directory"], "cleanup", ".json"
    )
    manifest = {
        "schema": 1, "campaign": "hurst1900_warm",
        "mH": instance["mH"], "NU": instance["NU"],
        "lift_manifest": lift["manifest"],
        "lift_manifest_sha256": util.sha256_file(lift["manifest"]),
        "warm_basis": lift["warm_basis"],
        "warm_basis_sha256": lift["warm_basis_sha256"],
        "cleanup_parent": parent,
        "cleanup_parent_sha256": wrapper_parent_sha256,
        "wrapper_command": ["fplll", "-a", "lll", "-m", "wrapper"],
        "wrapper_completed": wrapper.accepted,
        "wrapper_checkpoint": wrapper_output if wrapper.accepted else None,
        "wrapper_checkpoint_sha256":
            util.sha256_file(wrapper_output) if wrapper.accepted else None,
        "total_seconds": sum(run["seconds"] for run in runs),
        "peak_rss_kib": max(run["peak_rss_kib"] for run in runs),
        "runs": runs,
    }
    util.atomic_write_json(manifest_path, manifest)
    if not wrapper.accepted:
        raise RuntimeError(
            "mandatory wrapper did not commit a complete matrix; "
            "NU1900 cold fallback is disabled"
        )
    return wrapper_output, manifest_path, manifest


def audit_reduced(instance, checkpoint, weights):
    """Original-row MPFR-384 Babai followed by independent 100/160 scoring."""
    path = checkpoint + ".audit.json"
    checkpoint_hash = util.sha256_file(checkpoint)
    if os.path.exists(path):
        payload = _load_json(path)
        if payload.get("checkpoint_sha256") == checkpoint_hash:
            raw = payload["candidates"][0]
        else:
            raise RuntimeError(f"immutable audit hash mismatch: {path}")
    else:
        meta = _load_json(instance["meta"])
        candidate = audit_core.mpfr_babai(checkpoint, meta, "original", 384)
        scoring = audit_core.load_scoring_inputs("hurst", meta)
        raw = audit_core.audit_candidate(candidate, meta, scoring, (100, 160))
        payload = {
            "stage": "hurst", "campaign": "hurst1900_warm",
            "decoder": {"backend": "mpfr", "bits": 384,
                        "row_order": "original"},
            "checkpoint": checkpoint,
            "checkpoint_sha256": checkpoint_hash,
            "meta": instance["meta"],
            "meta_sha256": util.sha256_file(instance["meta"]),
            "meta_mH": instance["mH"], "meta_NU": instance["NU"],
            "H_sha256": instance["H_sha256"], "candidates": [raw],
        }
        if raw.get("metrics"):
            payload["budget"] = model_core.budget_metrics(
                weights, instance["mH"], instance["NU"],
                float(raw["metrics"]["h_H"]),
            )
        util.atomic_write_json(path, payload)
    return {
        "audit": path, "parity": raw.get("parity"), "cy": raw.get("cy"),
        "scorer_h_H_difference":
            raw.get("scorer", {}).get("h_H_difference"),
        "h_H": float(raw["metrics"]["h_H"]) if raw.get("metrics") else None,
        "rho": float(raw["metrics"]["rho"]) if raw.get("metrics") else None,
        "budget": payload.get("budget"),
        "checkpoint": checkpoint, "checkpoint_sha256": checkpoint_hash,
    }


def _reusable_bkz(instance, beta):
    metadata = {
        "campaign": "hurst1900_warm",
        "beta": beta,
        "parent_lll_sha256": instance["lll_sha256"],
        "single_tour": True, "no_lll": True,
    }
    return _reusable_attempt(
        instance["directory"], f"bkz{beta}_attempt",
        instance["dimension"], metadata,
    )


def run_bkz(instance, beta, deadline, resume, reserve_bytes, cap_hours):
    """One tour, no initial LLL, and immutable DPE/LD/MPFR-256 attempts."""
    if resume:
        checkpoint, payload = _reusable_bkz(instance, beta)
        if checkpoint:
            return checkpoint, [{"resumed": True, **payload}]
    records = []
    for backend in ("dpe", "longdouble", "mpfr"):
        wait_for_memory(deadline, reserve_bytes)
        if remaining(deadline) <= 0:
            break
        output = _new_numbered_path(
            instance["directory"], f"bkz{beta}_attempt", ".txt"
        )
        result = reduction.run_fplll(
            backend_command(beta, backend, no_lll=True),
            instance["lll"], output, instance["dimension"],
            timeout=min(remaining(deadline), cap_hours*3600),
            metadata={
                "campaign": "hurst1900_warm",
                "mH": instance["mH"], "NU": instance["NU"],
                "beta": beta,
                "parent_lll_sha256": instance["lll_sha256"],
                "backend": backend, "single_tour": True, "no_lll": True,
            },
            progress_interval=PROGRESS_INTERVAL,
            progress_label=(
                f"m{instance['mH']} NU{instance['NU']} "
                f"BKZ-{beta}-{backend}"
            ),
        )
        records.append({"backend": backend, **asdict(result)})
        if result.accepted:
            return output, records
    raise RuntimeError(f"BKZ-{beta} exhausted fallback chain")


def search_checkpoint(instance, checkpoint, label, mode, deadline, resume):
    output = os.path.join(instance["directory"], f"{label}_{mode}.json")
    log_path = output+".log"
    if not (resume and os.path.exists(output)):
        command = [
            sys.executable, "s04_search.py", "hurst", checkpoint,
            "--meta", instance["meta"], "--mode", mode, "--jobs", "1",
            "--seed", str(instance["seed"]), "--output", output,
        ]
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, timeout=require_time(deadline, f"{mode} search"),
                env={**os.environ, **reduction.THREAD_ENV},
            )
        except subprocess.TimeoutExpired as exc:
            with util.atomic_text_writer(log_path) as handle:
                handle.write(str(exc.stdout or ""))
            return {"status": "timeout", "log": log_path}
        with util.atomic_text_writer(log_path) as handle:
            handle.write(result.stdout)
        if result.returncode != 0 or not os.path.exists(output):
            return {"status": "failed", "returncode": result.returncode,
                    "log": log_path}
    result_payload = _load_json(output)
    meta = _load_json(instance["meta"])
    scoring = audit_core.load_scoring_inputs("hurst", meta)
    parity = audit_core.canonical_full_parity(
        int(result_payload["y_exact_num"]), meta, scoring, (100, 160)
    )
    parity_path = output+".parity.json"
    util.atomic_write_json(parity_path, parity)
    return {
        "status": "completed" if parity["parity"] == "VERIFIED"
                  else "parity_failed",
        "result": output, "parity": parity_path,
        "h": float(parity["runs"][-1]["h"]),
        "cy": parity["cy"], "mode": mode,
    }


def certify(instance, search, deadline, resume, precision):
    output = os.path.join(
        instance["directory"],
        os.path.basename(search["result"]).replace(".json", "_certificate.json"),
    )
    if resume and os.path.exists(output):
        return _load_json(output)
    command = [
        sys.executable, "s05_certify.py", "hurst", "--jobs", "1",
        "--meta", instance["meta"], "--results", search["result"],
        "--output", output, "--precision", str(precision),
        "--zero-source", "reuse", "--resume",
    ]
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, timeout=require_time(deadline, "Arb certification"),
            env={**os.environ, **reduction.THREAD_ENV},
        )
    except subprocess.TimeoutExpired as exc:
        with util.atomic_text_writer(output+".log") as handle:
            handle.write(str(exc.stdout or ""))
        return {"surpassed": False, "status": "timeout", "log": output+".log"}
    with util.atomic_text_writer(output+".log") as handle:
        handle.write(result.stdout)
    if result.returncode != 0 or not os.path.exists(output):
        return {"surpassed": False, "status": "certification_failed",
                "returncode": result.returncode, "log": output+".log"}
    return _load_json(output)


def strict_zero_preflight(path, total, precision):
    balls = s05_certify.load_strict_balls(path, total)
    report = s05_certify.strict_ball_precision_report(
        balls, range(1, total+1), precision
    )
    report.update({
        "path": path, "sha256": util.sha256_file(path), "count": len(balls),
    })
    return report


def baseline_row(path):
    payload = _load_json(path)
    return next(
        row for row in payload["rows"]
        if int(row["mH"]) == 460 and int(row["NU"]) == 900
        and int(row["beta"]) == 20 and row.get("parity") == "VERIFIED"
    )


def budget_eta(baseline_budget, new_budget):
    raw_delta = new_budget["raw_budget_nats"]-baseline_budget["raw_budget_nats"]
    if raw_delta <= 0:
        raise ValueError("new raw budget must exceed baseline")
    return (
        new_budget["effective_budget_nats"]
        - baseline_budget["effective_budget_nats"]
    )/raw_delta


def main_budget_action(effective, required, window=40):
    if effective >= required:
        return "search"
    if effective >= required-window:
        return "bkz40"
    return "stop"


def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260726)
    parser.add_argument("--wall-hours", type=float, default=12)
    parser.add_argument("--reserve-gib", type=float, default=1.2)
    parser.add_argument("--nu", type=int, default=1900)
    parser.add_argument("--warm-parent-nu", type=int, default=900)
    parser.add_argument("--calibration-m", type=int, default=460)
    parser.add_argument("--main-m", type=int, default=800)
    parser.add_argument("--eta-gate", type=float, default=0.90)
    parser.add_argument("--bkz40-window-nats", type=float, default=40)
    parser.add_argument("--precision", type=int, default=2000)
    parser.add_argument(
        "--progress-seconds", type=float, default=60,
        help="console/JSONL heartbeat interval for every fplll process",
    )
    parser.add_argument(
        "--baseline",
        default="work/probes/qcal_seed20260726/qcal_results.json",
    )
    parser.add_argument(
        "--baseline-meta",
        default="work/probes/qcal_seed20260726/m460_n900/base_meta.json",
    )
    parser.add_argument(
        "--calibration-parent",
        default="work/probes/qcal_seed20260726/m460_n900/lll.txt",
    )
    parser.add_argument(
        "--cold-baseline-run",
        default="work/probes/hurst1900_seed20260726/"
                "m460_n1900/lll.txt.run.json",
    )
    parser.add_argument("--output-dir")
    parser.add_argument(
        "--calibration-only", action="store_true",
        help="stop after the measured m460 lift/cleanup/BKZ-20 eta gate",
    )
    parser.add_argument("--resume", action=argparse.BooleanOptionalAction,
                        default=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def _external_parent(checkpoint, expected_m, expected_nu):
    directory = os.path.dirname(checkpoint)
    basis = os.path.join(directory, "base_basis.txt")
    meta_path = os.path.join(directory, "base_meta.json")
    meta = _load_json(meta_path)
    dim = expected_m+1
    if (int(meta["mH"]) != expected_m or int(meta["NU"]) != expected_nu
            or not util.validate_fplll_matrix(basis, dim)
            or not util.validate_fplll_matrix(checkpoint, dim)):
        raise RuntimeError("calibration parent/base/meta do not match")
    result = {
        "mH": expected_m, "NU": expected_nu, "dimension": dim,
        "directory": directory, "basis": basis, "meta": meta_path,
        "lll": checkpoint, "basis_sha256": util.sha256_file(basis),
        "meta_sha256": util.sha256_file(meta_path),
        "lll_sha256": util.sha256_file(checkpoint),
        "H_sha256": h_fingerprint(meta), "raw_order": True,
    }
    sidecar = checkpoint+".run.json"
    if os.path.exists(sidecar):
        result["lll_seconds"] = float(_load_json(sidecar)["seconds"])
    return result


def _warm_target(source, output_dir, mH, nu, seed, deadline, resume,
                 reserve_bytes, cleanup_cap_hours):
    target = prepare_base(output_dir, mH, nu, deadline, resume)
    target["seed"] = seed
    if source.get("lll_seconds"):
        estimate = lll_complexity_estimate(
            target["dimension"], source["NU"], target["NU"],
            source["lll_seconds"], source["dimension"],
        )
        target["lll_complexity_estimate"] = estimate
        low = estimate["bit_power_2_seconds"]/60
        central = estimate["bit_power_3_seconds"]/60
        high = estimate["bit_power_4_seconds"]/60
        print(
            f"[H1900-WARM] LLL complexity envelope m={mH}: "
            f"{low:.1f}/{central:.1f}/{high:.1f} min "
            f"(bit powers 2/3/4; not an ETA)",
            flush=True,
        )
    lift = lift_instance(source, target, resume)
    target["lift"] = {
        key: value for key, value in lift.items() if key != "manifest_payload"
    }
    target["lift"]["determinant"] = lift["manifest_payload"]["determinant"]
    checkpoint, cleanup_path, cleanup = run_warm_cleanup(
        target, lift, deadline, resume, reserve_bytes, cleanup_cap_hours
    )
    target["cleanup_manifest"] = cleanup_path
    target["cleanup"] = cleanup
    target["lll"] = checkpoint
    target["lll_sha256"] = util.sha256_file(checkpoint)
    return target


def main(argv=None):
    global PROGRESS_INTERVAL
    args = parse_args(argv)
    PROGRESS_INTERVAL = max(5.0, float(args.progress_seconds))
    started = time.time()
    deadline = started+args.wall_hours*3600
    output_dir = args.output_dir or (
        f"work/probes/hurst1900_warm_seed{args.seed}"
    )
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "campaign.json")
    summary = {
        "schema": 2, "campaign": "hurst1900_warm", "target": TARGET,
        "seed": args.seed, "NU": args.nu,
        "warm_parent_NU": args.warm_parent_nu,
        "wall_hours": args.wall_hours, "reserve_gib": args.reserve_gib,
        "single_core": True, "calibration_m": args.calibration_m,
        "main_m": args.main_m, "eta_gate": args.eta_gate,
        "status": "preflight", "started_unix": started,
        "cold_fallback": False,
    }
    if os.path.exists(args.cold_baseline_run):
        cold = _load_json(args.cold_baseline_run)
        summary["cold_baseline"] = {
            "source": args.cold_baseline_run,
            "status": cold.get("status"), "accepted": cold.get("accepted"),
            "seconds": cold.get("seconds"),
            "peak_rss_kib": cold.get("peak_rss_kib"),
        }

    if args.dry_run:
        summary["status"] = "dry_run"
        summary["steps"] = [
            "zero_preflight", "m460_exact_lift",
            "heuristic_longdouble_or_mpfr256", "mandatory_wrapper",
            "mpfr384_and_100_160_parity", "bkz20_nolll_eta",
            "eta_gate", "m800_raw_B900_wrapper", "m800_exact_lift",
            "mandatory_wrapper", "bkz20_or_bkz40_nolll",
            "pilot_or_full_search", "arb_certificate",
        ]
        util.atomic_write_json(summary_path, summary)
        print(f"[H1900-WARM] dry-run -> {summary_path}")
        return

    if args.nu != 1900:
        raise SystemExit("hurst1900 campaign requires NU=1900")
    if args.warm_parent_nu >= args.nu:
        raise SystemExit("warm parent NU must be smaller than target NU")
    reserve_bytes = int(args.reserve_gib*2**30)
    zeros = strict_zero_preflight(
        config.ZEROS_ARB, config.NEV+1, args.precision
    )
    summary["zero_preflight"] = zeros
    if not zeros["sufficient"]:
        summary["status"] = "zero_precision_failed"
        util.atomic_write_json(summary_path, summary)
        raise SystemExit("strict Arb balls do not satisfy precision gate")

    weights = model_core.scan_inputs("hurst")
    baseline = baseline_row(args.baseline)
    baseline_meta = _load_json(args.baseline_meta)
    baseline_budget = model_core.budget_metrics(
        weights, 460, args.warm_parent_nu, float(baseline["h_H"])
    )
    summary["baseline"] = {**baseline_budget, "source": args.baseline}
    try:
        complexity_plan = campaign_complexity_plan(
            args.baseline, args.main_m, args.warm_parent_nu, args.nu
        )
        summary["complexity_plan"] = complexity_plan
        parent_minutes = (
            complexity_plan["parent_dimension_fit"]["predicted_seconds"]/60
        )
        envelope = complexity_plan["target_bit_envelope"]
        target_minutes = [
            envelope[f"bit_power_{power}_seconds"]/60
            for power in (2, 3, 4)
        ]
        print(
            f"[H1900-WARM] empirical m{args.main_m} NU"
            f"{args.warm_parent_nu} parent estimate={parent_minutes:.1f} min; "
            f"NU{args.nu} bit envelope="
            f"{target_minutes[0]:.1f}/{target_minutes[1]:.1f}/"
            f"{target_minutes[2]:.1f} min",
            flush=True,
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        summary["complexity_plan"] = {
            "status": "unavailable",
            "error": f"{type(exc).__name__}: {exc}",
        }
    util.atomic_write_json(summary_path, summary)

    calibration_parent = _external_parent(
        args.calibration_parent, args.calibration_m, args.warm_parent_nu
    )
    if h_fingerprint(baseline_meta) != calibration_parent["H_sha256"]:
        summary["status"] = "calibration_parent_active_set_mismatch"
        util.atomic_write_json(summary_path, summary)
        raise SystemExit("baseline/calibration parent active sets differ")
    try:
        calibration = _warm_target(
            calibration_parent, output_dir, args.calibration_m, args.nu,
            args.seed, deadline, args.resume, reserve_bytes, 1.5,
        )
    except RuntimeError as exc:
        summary["status"] = "calibration_wrapper_failed"
        summary["blocker"] = str(exc)
        util.atomic_write_json(summary_path, summary)
        return
    calibration["lll_audit"] = audit_reduced(
        calibration, calibration["lll"], weights
    )
    calibration["parity"] = (
        "VERIFIED"
        if (calibration["lift"]["parity"] == "VERIFIED"
            and calibration["lll_audit"]["parity"] == "VERIFIED")
        else "BROKEN"
    )
    if calibration["parity"] != "VERIFIED":
        summary.update({
            "status": "calibration_parity_failed",
            "calibration": calibration,
        })
        util.atomic_write_json(summary_path, summary)
        return

    b20_path, b20_runs = run_bkz(
        calibration, 20, deadline, args.resume, reserve_bytes, cap_hours=0.5
    )
    calibration["bkz20"] = audit_reduced(calibration, b20_path, weights)
    calibration["bkz20"]["runs"] = b20_runs
    if calibration["bkz20"]["parity"] != "VERIFIED":
        summary.update({
            "status": "calibration_bkz20_parity_failed",
            "calibration": calibration,
        })
        util.atomic_write_json(summary_path, summary)
        return
    eta = budget_eta(baseline_budget, calibration["bkz20"]["budget"])
    calibration["eta"] = eta
    summary["calibration"] = calibration
    if summary.get("cold_baseline"):
        summary["warm_vs_cold"] = {
            "cold_incomplete_seconds":
                summary["cold_baseline"].get("seconds"),
            "warm_cleanup_seconds":
                calibration["cleanup"].get("total_seconds"),
            "cold_accepted": summary["cold_baseline"].get("accepted"),
        }
    if eta < args.eta_gate:
        summary["status"] = "eta_gate_no_go"
        summary["wall_seconds"] = time.time()-started
        util.atomic_write_json(summary_path, summary)
        print(f"[H1900-WARM] NO-GO eta={eta:.4f} < {args.eta_gate:.4f}")
        return
    if args.calibration_only:
        summary["status"] = "calibration_complete_eta_go"
        summary["wall_seconds"] = time.time()-started
        util.atomic_write_json(summary_path, summary)
        print(
            f"[H1900-WARM] calibration complete eta={eta:.4f}; "
            "m800 intentionally not started",
            flush=True,
        )
        return
    util.atomic_write_json(summary_path, summary)

    # The expensive m=800 parent is intentionally created only after eta GO.
    main_parent = prepare_base(
        output_dir, args.main_m, args.warm_parent_nu, deadline, args.resume
    )
    parent_lll, parent_runs = run_raw_parent_lll(
        main_parent, deadline, args.resume, reserve_bytes, cap_hours=4
    )
    main_parent["lll"] = parent_lll
    main_parent["lll_sha256"] = util.sha256_file(parent_lll)
    main_parent["lll_runs"] = parent_runs
    timed_runs = [run for run in parent_runs if run.get("seconds") is not None]
    if timed_runs:
        main_parent["lll_seconds"] = float(timed_runs[-1]["seconds"])
    try:
        main_instance = _warm_target(
            main_parent, output_dir, args.main_m, args.nu, args.seed,
            deadline, args.resume, reserve_bytes, 4,
        )
    except RuntimeError as exc:
        summary["status"] = "main_wrapper_failed"
        summary["blocker"] = str(exc)
        summary["main_parent"] = main_parent
        util.atomic_write_json(summary_path, summary)
        return
    main_instance["parent"] = main_parent
    main_instance["lll_audit"] = audit_reduced(
        main_instance, main_instance["lll"], weights
    )
    main_instance["parity"] = (
        "VERIFIED"
        if (main_instance["lift"]["parity"] == "VERIFIED"
            and main_instance["lll_audit"]["parity"] == "VERIFIED")
        else "BROKEN"
    )
    if main_instance["parity"] != "VERIFIED":
        summary.update({
            "status": "main_lll_parity_failed", "main": main_instance,
        })
        util.atomic_write_json(summary_path, summary)
        return

    ideal = model_core.ideal_row(weights, args.main_m, args.nu, TARGET)
    harvest = ideal["ideal_harvest"]["1000"]["q10"]
    required_h_h = TARGET-harvest
    required_budget = model_core.required_effective_budget(
        weights, args.main_m, required_h_h
    )
    summary["gate"] = {
        "harvest_Meff1000_q10": harvest, "required_h_H": required_h_h,
        "required_effective_budget_nats": required_budget,
        "bkz40_window_nats": args.bkz40_window_nats,
    }
    b20_path, b20_runs = run_bkz(
        main_instance, 20, deadline, args.resume, reserve_bytes, cap_hours=2
    )
    main_instance["bkz20"] = audit_reduced(main_instance, b20_path, weights)
    main_instance["bkz20"]["runs"] = b20_runs
    summary["main"] = main_instance
    util.atomic_write_json(summary_path, summary)
    if main_instance["bkz20"]["parity"] != "VERIFIED":
        summary["status"] = "main_bkz20_parity_failed"
        util.atomic_write_json(summary_path, summary)
        return

    b20_eff = main_instance["bkz20"]["budget"]["effective_budget_nats"]
    initial_action = main_budget_action(
        b20_eff, required_budget, args.bkz40_window_nats
    )
    summary["main"]["bkz20_gate_action"] = initial_action
    search = None
    if initial_action == "search":
        search = search_checkpoint(
            main_instance, b20_path, "bkz20", "pilot", deadline, args.resume
        )
        summary["main"]["bkz20_search"] = search
        if search.get("status") == "completed" and search["h"] > TARGET:
            certificate = certify(
                main_instance, search, deadline, args.resume, args.precision
            )
            summary["main"]["bkz20_certificate"] = certificate
            if certificate.get("surpassed"):
                summary["status"] = "certified_breakthrough"
                util.atomic_write_json(summary_path, summary)
                print(f"[H1900-WARM] CERTIFIED h_lo={certificate['h_lo']}")
                return

    needs_b40 = initial_action != "stop" and remaining(deadline) >= 2*3600
    if not needs_b40:
        summary["status"] = "main_bkz20_no_go"
        util.atomic_write_json(summary_path, summary)
        return

    # BKZ-20 and BKZ-40 both read main_instance["lll"], never each other.
    b40_path, b40_runs = run_bkz(
        main_instance, 40, deadline, args.resume, reserve_bytes, cap_hours=3
    )
    main_instance["bkz40"] = audit_reduced(main_instance, b40_path, weights)
    main_instance["bkz40"]["runs"] = b40_runs
    util.atomic_write_json(summary_path, summary)
    if (main_instance["bkz40"]["parity"] != "VERIFIED"
            or main_instance["bkz40"]["budget"]
            ["effective_budget_nats"] < required_budget):
        summary["status"] = "main_bkz40_no_go"
        util.atomic_write_json(summary_path, summary)
        return

    search = search_checkpoint(
        main_instance, b40_path, "bkz40", "pilot", deadline, args.resume
    )
    summary["main"]["bkz40_search"] = search
    if (search.get("status") == "completed" and search["h"] <= TARGET
            and TARGET-search["h"] <= 0.01
            and remaining(deadline) >= 2*3600):
        search = search_checkpoint(
            main_instance, b40_path, "bkz40", "full", deadline, args.resume
        )
        summary["main"]["bkz40_full_search"] = search
    if search.get("status") == "completed" and search["h"] > TARGET:
        certificate = certify(
            main_instance, search, deadline, args.resume, args.precision
        )
        summary["main"]["bkz40_certificate"] = certificate
        if certificate.get("surpassed"):
            summary["status"] = "certified_breakthrough"
            util.atomic_write_json(summary_path, summary)
            print(f"[H1900-WARM] CERTIFIED h_lo={certificate['h_lo']}")
            return
    summary["status"] = "search_no_go"
    summary["wall_seconds"] = time.time()-started
    util.atomic_write_json(summary_path, summary)
    print(f"[H1900-WARM] {summary['status']} -> {summary_path}")


if __name__ == "__main__":
    main()
