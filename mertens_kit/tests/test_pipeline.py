import json
import os
import sys
import tempfile
import textwrap
import time
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

import reduction
import util
import audit_core
import lift_structured_lattice
import model_core
import s05_certify
from s01_make_zeros import merge_shards, validate_shard
import s04_search
from s04_search import ordered_map
from s06_probe import backend_command, fit_q
import s08_hurst1900_campaign
from s08_hurst1900_campaign import budget_eta, main_budget_action


def delayed_square(value):
    time.sleep((5 - value) * 0.002)
    return value * value


class ArbShardTests(unittest.TestCase):
    def test_radius_preserved_and_duplicate_rejected(self):
        index, ball = util.parse_arb_ball_line("7 [12.5+/-3e-40]")
        self.assertEqual(index, 7)
        self.assertEqual(ball, "[12.5+/-3e-40]")
        with self.assertRaises(ValueError):
            util.validate_arb_rows(
                ["1 [1.0+/-1e-20]", "1 [1.0+/-1e-20]"], 1, 2
            )

    def test_merge_requires_complete_disjoint_indices(self):
        with tempfile.TemporaryDirectory() as directory:
            left = os.path.join(directory, "left")
            right = os.path.join(directory, "right")
            output = os.path.join(directory, "merged")
            with open(left, "w") as handle:
                handle.write("1 [1.0+/-1e-20]\n2 [2.0+/-1e-20]\n")
            with open(right, "w") as handle:
                handle.write("3 [3.0+/-1e-20]\n")
            merge_shards([(left, 1, 2), (right, 3, 3)], output, 3)
            with open(output) as handle:
                rows = handle.read().splitlines()
            self.assertEqual([util.parse_arb_line(row)[0] for row in rows],
                             [1, 2, 3])
            self.assertTrue(all("+/-" in row for row in rows))


class ReductionCheckpointTests(unittest.TestCase):
    MATRIX = "[[1 0]\\n[0 1]\\n]\\n"

    def make_fake(self, directory):
        path = os.path.join(directory, "fake.py")
        with open(path, "w") as handle:
            handle.write(textwrap.dedent("""
            import sys, time
            mode = sys.argv[1]
            data = sys.stdin.read()
            if mode == "timeout":
                time.sleep(5)
            elif mode == "truncated":
                print("[[1 0]")
            else:
                print(data, end="")
            if mode == "limit":
                print("loops limit exceeded", file=sys.stderr)
                raise SystemExit(8)
            if mode == "babai":
                print("infinite loop in babai", file=sys.stderr)
                raise SystemExit(1)
            if mode == "crash":
                raise SystemExit(3)
            """))
        return path

    def run_mode(self, mode, timeout=2):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        source = os.path.join(directory.name, "in.txt")
        output = os.path.join(directory.name, "out.txt")
        with open(source, "w") as handle:
            handle.write(self.MATRIX)
        fake = self.make_fake(directory.name)
        result = reduction.run_fplll(
            [sys.executable, fake, mode], source, output, 2, timeout=timeout
        )
        return result, output

    def test_normal_and_loop_limit_are_committed(self):
        for mode, status in (("ok", "completed"),
                             ("limit", "completed_by_limit")):
            result, output = self.run_mode(mode)
            self.assertTrue(result.accepted)
            self.assertEqual(result.status, status)
            self.assertTrue(os.path.exists(output))

    def test_bad_outputs_never_commit(self):
        for mode, status in (
            ("truncated", "truncated_or_invalid_matrix"),
            ("babai", "infinite_loop_in_babai"),
            ("crash", "failed_rc_3"),
            ("timeout", "timeout"),
        ):
            result, output = self.run_mode(mode, timeout=0.05)
            self.assertFalse(result.accepted, mode)
            self.assertEqual(result.status, status, mode)
            self.assertFalse(os.path.exists(output), mode)

    def test_valid_failure_can_be_retained_as_provisional_parent(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        source = os.path.join(directory.name, "in.txt")
        output = os.path.join(directory.name, "out.txt")
        with open(source, "w") as handle:
            handle.write(self.MATRIX)
        fake = self.make_fake(directory.name)
        result = reduction.run_fplll(
            [sys.executable, fake, "babai"], source, output, 2,
            retain_valid_failure=True, progress_interval=0.001,
            progress_label="test-provisional",
        )
        self.assertFalse(result.accepted)
        self.assertTrue(result.output_valid)
        self.assertTrue(result.retained_valid_failure)
        self.assertEqual(result.output, output)
        self.assertTrue(util.validate_fplll_matrix(output, 2))
        with open(output+".progress.jsonl") as handle:
            events = [json.loads(line)["event"] for line in handle]
        self.assertEqual(events[0], "started")
        self.assertEqual(events[-1], "completed")


class StructuredLiftTests(unittest.TestCase):
    def make_bundle(self, directory, transform=None):
        source_meta = {
            "stage": "hurst", "mH": 2, "NU": 20, "NUY": 8,
            "H": [3, 9],
        }
        target_meta = {**source_meta, "NU": 40}
        source = [[3, 5, 1], [7, 0, 0], [0, 11, 0]]
        target = [[13, 17, 1], [19, 0, 0], [0, 23, 0]]
        transform = transform or [[1, 1, 0], [0, 1, 1], [0, 0, 1]]
        reduced_basis = lift_structured_lattice.StructuredBasis(
            source, source[0][:-1], [7, 11], 3
        )
        reduced = lift_structured_lattice.multiply_transform(
            transform, reduced_basis
        )
        paths = {
            name: os.path.join(directory, name)
            for name in (
                "source.txt", "source.json", "reduced.txt",
                "target.txt", "target.json", "transform.txt",
                "warm.txt", "manifest.json",
            )
        }
        util.write_fplll_matrix(paths["source.txt"], source)
        util.write_fplll_matrix(paths["reduced.txt"], reduced)
        util.write_fplll_matrix(paths["target.txt"], target)
        util.atomic_write_json(paths["source.json"], source_meta)
        util.atomic_write_json(paths["target.json"], target_meta)
        return paths, source_meta, target_meta

    def run_lift(self, paths):
        return lift_structured_lattice.lift(
            paths["source.txt"], paths["source.json"],
            paths["reduced.txt"], paths["target.txt"], paths["target.json"],
            paths["transform.txt"], paths["warm.txt"],
            paths["manifest.json"],
        )

    def test_known_unimodular_transform_and_cross_nu_lift(self):
        with tempfile.TemporaryDirectory() as directory:
            paths, _, _ = self.make_bundle(directory)
            manifest = self.run_lift(paths)
            self.assertEqual(manifest["determinant"], "1")
            self.assertEqual(manifest["exact_division_remainders"], 0)
            self.assertEqual(manifest["parity"], "VERIFIED")
            self.assertEqual(
                util.read_fplll_matrix(paths["transform.txt"], 3),
                [[1, 1, 0], [0, 1, 1], [0, 0, 1]],
            )

    def test_non_exact_division_is_rejected_before_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            paths, _, _ = self.make_bundle(directory)
            rows = util.read_fplll_matrix(paths["reduced.txt"], 3)
            rows[0][0] += 1
            util.write_fplll_matrix(paths["reduced.txt"], rows)
            with self.assertRaisesRegex(ValueError, "non-exact"):
                self.run_lift(paths)
            self.assertFalse(os.path.exists(paths["manifest.json"]))

    def test_non_unimodular_transform_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            paths, _, _ = self.make_bundle(
                directory, [[2, 0, 0], [0, 1, 0], [0, 0, 1]]
            )
            with self.assertRaisesRegex(ValueError, "not unimodular"):
                self.run_lift(paths)

    def test_active_set_and_stage_mismatch_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            paths, _, target = self.make_bundle(directory)
            util.atomic_write_json(
                paths["target.json"], {**target, "H": [3, 10]}
            )
            with self.assertRaisesRegex(ValueError, "H"):
                self.run_lift(paths)

    def test_complete_reconstruction_guard_is_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            paths, _, _ = self.make_bundle(directory)
            original = lift_structured_lattice.multiply_transform
            calls = 0

            def corrupt_second(transform, basis):
                nonlocal calls
                calls += 1
                result = original(transform, basis)
                if calls == 2:
                    result[0][0] += 1
                return result

            with mock.patch.object(
                    lift_structured_lattice, "multiply_transform",
                    side_effect=corrupt_second):
                with self.assertRaisesRegex(
                        ValueError, "source reconstruction"):
                    self.run_lift(paths)


class WarmCampaignCommandTests(unittest.TestCase):
    MATRIX = [[1, 0], [0, 1]]

    def result(self, command, output, accepted, status):
        return reduction.RunResult(
            command=command, returncode=0 if accepted else 1,
            status=status, accepted=accepted, seconds=0.1,
            peak_rss_kib=10, output_valid=accepted,
            stderr_tail="", output=output if accepted else None,
        )

    def test_cleanup_fallback_order_and_wrapper_has_no_float_flag(self):
        with tempfile.TemporaryDirectory() as directory:
            warm = os.path.join(directory, "warm.txt")
            util.write_fplll_matrix(warm, self.MATRIX)
            commands = []

            def fake_run(command, input_path, output_path, dim, **kwargs):
                commands.append(command)
                accepted = len(commands) > 1
                if accepted:
                    util.write_fplll_matrix(output_path, self.MATRIX)
                else:
                    util.atomic_write_json(output_path+".run.json", {})
                return self.result(
                    command, output_path, accepted,
                    "completed" if accepted else "failed_rc_1",
                )

            instance = {
                "dimension": 2, "directory": directory, "mH": 1, "NU": 40,
            }
            lift = {
                "warm_basis": warm,
                "warm_basis_sha256": util.sha256_file(warm),
                "manifest": os.path.join(directory, "lift.json"),
            }
            util.atomic_write_json(lift["manifest"], {"parity": "VERIFIED"})
            with mock.patch.object(
                    s08_hurst1900_campaign.reduction, "run_fplll",
                    side_effect=fake_run), mock.patch.object(
                    s08_hurst1900_campaign, "wait_for_memory"):
                checkpoint, _, manifest = (
                    s08_hurst1900_campaign.run_warm_cleanup(
                        instance, lift, time.time()+10, False, 0, 1
                    )
                )
            self.assertTrue(os.path.exists(checkpoint))
            self.assertEqual(commands[0][-2:], ["-f", "longdouble"])
            self.assertIn("mpfr", commands[1])
            self.assertIn("256", commands[1])
            self.assertEqual(
                commands[2], ["fplll", "-a", "lll", "-m", "wrapper"]
            )
            self.assertNotIn("-f", commands[2])
            self.assertTrue(manifest["wrapper_completed"])
            self.assertEqual(len(set(run["output"] for run in manifest["runs"]
                                     if run["output"])), 2)

    def test_bkz_builder_supports_nolll_after_precision_options(self):
        for backend in ("dpe", "longdouble", "mpfr"):
            command = backend_command(40, backend, no_lll=True)
            self.assertIn("-nolll", command)
            self.assertEqual(command.count("-bkzmaxloops"), 1)
            self.assertEqual(command[command.index("-bkzmaxloops")+1], "1")
        mpfr = backend_command(20, "mpfr", no_lll=True)
        self.assertEqual(mpfr[mpfr.index("-p")+1], "256")

    def test_wrapper_failure_stops_without_cold_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            warm = os.path.join(directory, "warm.txt")
            util.write_fplll_matrix(warm, self.MATRIX)
            commands = []

            def fail(command, input_path, output_path, dim, **kwargs):
                commands.append(command)
                util.atomic_write_json(output_path+".run.json", {})
                return self.result(command, output_path, False, "failed_rc_1")

            instance = {
                "dimension": 2, "directory": directory, "mH": 1, "NU": 40,
            }
            lift = {
                "warm_basis": warm,
                "warm_basis_sha256": util.sha256_file(warm),
                "manifest": os.path.join(directory, "lift.json"),
            }
            util.atomic_write_json(lift["manifest"], {"parity": "VERIFIED"})
            with mock.patch.object(
                    s08_hurst1900_campaign.reduction, "run_fplll",
                    side_effect=fail), mock.patch.object(
                    s08_hurst1900_campaign, "wait_for_memory"):
                with self.assertRaisesRegex(
                        RuntimeError, "cold fallback is disabled"):
                    s08_hurst1900_campaign.run_warm_cleanup(
                        instance, lift, time.time()+10, False, 0, 1
                    )
            self.assertEqual(len(commands), 3)
            self.assertEqual(
                commands[-1], ["fplll", "-a", "lll", "-m", "wrapper"]
            )
            self.assertFalse(any("cold" in " ".join(command)
                                 for command in commands))

    def test_raw_parent_lll_reads_unshuffled_basis_and_attempts_are_immutable(self):
        with tempfile.TemporaryDirectory() as directory:
            basis = os.path.join(directory, "base.txt")
            util.write_fplll_matrix(basis, self.MATRIX)
            seen = []

            def fake_run(command, input_path, output_path, dim, **kwargs):
                seen.append((input_path, output_path))
                util.write_fplll_matrix(output_path, self.MATRIX)
                return self.result(command, output_path, True, "completed")

            instance = {
                "dimension": 2, "directory": directory, "mH": 1, "NU": 20,
                "basis": basis, "basis_sha256": util.sha256_file(basis),
            }
            with mock.patch.object(
                    s08_hurst1900_campaign.reduction, "run_fplll",
                    side_effect=fake_run), mock.patch.object(
                    s08_hurst1900_campaign, "wait_for_memory"):
                s08_hurst1900_campaign.run_raw_parent_lll(
                    instance, time.time()+10, False, 0, 1
                )
                s08_hurst1900_campaign.run_raw_parent_lll(
                    instance, time.time()+10, False, 0, 1
                )
            self.assertEqual([item[0] for item in seen], [basis, basis])
            self.assertNotEqual(seen[0][1], seen[1][1])
            self.assertFalse(os.path.exists(
                os.path.join(directory, "basis_seeded.txt")
            ))


class OrderedParallelTests(unittest.TestCase):
    def test_parallel_map_keeps_score_candidate_alignment(self):
        values = list(range(6))
        serial = ordered_map(delayed_square, values, jobs=1)
        parallel = ordered_map(delayed_square, values, jobs=4)
        self.assertEqual(serial, parallel)
        self.assertEqual(parallel, [value*value for value in values])


class DecoderAuditTests(unittest.TestCase):
    def test_production_loader_preserves_fplll_row_order(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "basis.txt")
            util.write_fplll_matrix(path, [[9, 0], [1, 0]])
            old = dict(s04_search.G)
            self.addCleanup(lambda: (s04_search.G.clear(),
                                     s04_search.G.update(old)))
            s04_search.G["d"] = 2
            self.assertEqual(s04_search.load_basis(path), [[9, 0], [1, 0]])

    def test_large_y_scorer_uses_argument_reduction_guard(self):
        meta = {
            "NEV": 1, "NUY": 8, "H": [0],
            "LH_pred": 0.1,
        }
        inputs = (
            ["14.134725141734693790457251983562470270784257115699",
             "21.022039638771554992628479593896902777334340524903"],
            ["0.0891415", "0.01"],
            ["1.25", "0.5"],
        )
        cy = 10**270 + 123456789
        low = audit_core.canonical_heavy_metrics(cy, meta, inputs, 100)
        high = audit_core.canonical_heavy_metrics(cy, meta, inputs, 160)
        self.assertLess(
            abs(float(low["h_H"])-float(high["h_H"])), 1e-20
        )
        self.assertGreater(low["argument_reduction_dps"], 300)


class QFitTests(unittest.TestCase):
    def test_fit_keeps_same_m_beta_pairs(self):
        rows = []
        for mH, q20, q40 in (
            (260, .85, .86), (360, .80, .83), (460, .76, .81)
        ):
            for beta, q in ((20, q20), (40, q40)):
                rows.append({"mH": mH, "beta": beta,
                             "status": "completed", "q_efficiency": q})
        fit = fit_q(rows, bootstrap_samples=20, seed=1)
        self.assertEqual(fit["status"], "fitted")
        self.assertEqual(len(fit["direct_slopes"]), 3)
        self.assertAlmostEqual(
            fit["direct_slopes"][1]["delta_q_per_10_beta"], .015
        )


class EffectiveBudgetTests(unittest.TestCase):
    def test_inverse_tilt_recovers_budget(self):
        active = [0.18, 0.12, 0.08, 0.05]
        _, score = util.tilt_prediction(active, 5.0)
        recovered = model_core.effective_budget_for_score(active, score)
        self.assertAlmostEqual(recovered, 5.0, places=5)

    def test_eta_and_main_gate(self):
        baseline = {"raw_budget_nats": 600,
                    "effective_budget_nats": 150}
        new = {"raw_budget_nats": 1300,
               "effective_budget_nats": 780}
        self.assertAlmostEqual(budget_eta(baseline, new), 0.9)
        self.assertEqual(main_budget_action(780, 771), "search")
        self.assertEqual(main_budget_action(750, 771), "bkz40")
        self.assertEqual(main_budget_action(700, 771), "stop")

    def test_lll_complexity_envelope_matches_measured_bit_scaling(self):
        estimate = s08_hurst1900_campaign.lll_complexity_estimate(
            461, 900, 1900, 148.2671201810008
        )
        self.assertAlmostEqual(
            estimate["bit_power_2_seconds"], 660.7954368560653
        )
        self.assertAlmostEqual(
            estimate["bit_power_3_seconds"], 1395.01258891836
        )
        self.assertAlmostEqual(
            estimate["bit_power_4_seconds"], 2945.0265766054267
        )
        fit = s08_hurst1900_campaign.empirical_dimension_fit(
            [(261, 60.40539120700123),
             (361, 94.4963083640032),
             (461, 148.2671201810008)],
            801,
        )
        self.assertAlmostEqual(fit["dimension_exponent_q"],
                               1.567898230318205)
        self.assertAlmostEqual(fit["predicted_seconds"],
                               344.07698941211976)

    def test_full_reuse_precision_report_checks_every_index(self):
        balls = {1: "[14.0+/-1e-100]", 2: "[21.0+/-1e-100]"}
        report = s05_certify.strict_ball_precision_report(
            balls, range(1, 3), 300
        )
        self.assertTrue(report["complete"])
        self.assertTrue(report["sufficient"])
        missing = s05_certify.strict_ball_precision_report(
            balls, range(1, 4), 300
        )
        self.assertFalse(missing["complete"])
        self.assertEqual(missing["minimum_index"], 3)

    def test_certificate_fingerprint_binds_custom_meta(self):
        left = s05_certify.candidate_id(
            "hurst", 123, 8, 2000, "strict:x", "meta-a"
        )
        right = s05_certify.candidate_id(
            "hurst", 123, 8, 2000, "strict:x", "meta-b"
        )
        self.assertNotEqual(left, right)


if __name__ == "__main__":
    unittest.main()
