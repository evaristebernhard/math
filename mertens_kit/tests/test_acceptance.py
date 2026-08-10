"""使用现有 validate artifact 的可选慢回归。

运行：
  PYTHONPATH=.deps/pip:.localdeps/usr/lib/python3/dist-packages \
    python3 -m unittest tests.test_acceptance
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(__file__))
ENV = {
    **os.environ,
    "PYTHONPATH": (
        f"{os.path.join(ROOT, '.deps/pip')}:"
        f"{os.path.join(ROOT, '.localdeps/usr/lib/python3/dist-packages')}:"
        f"{ROOT}"
    ),
}


@unittest.skipUnless(
    os.path.exists(os.path.join(ROOT, "work", "validate_bkz20.txt")),
    "validate artifacts unavailable",
)
class ExistingValidateAcceptance(unittest.TestCase):
    def run_search(self, jobs, output):
        subprocess.run([
            sys.executable, "s04_search.py", "validate",
            "work/validate_bkz20.txt", "--mode", "pilot",
            "--jobs", str(jobs), "--seed", "123", "--tail-solutions", "16",
            "--output", output,
        ], cwd=ROOT, env=ENV, check=True, stdout=subprocess.DEVNULL)
        return json.load(open(output))

    @unittest.skipUnless(os.environ.get("MERTENS_SLOW_TESTS") == "1",
                         "set MERTENS_SLOW_TESTS=1 (~4 min)")
    def test_search_one_vs_fourteen(self):
        with tempfile.TemporaryDirectory() as directory:
            one = self.run_search(1, os.path.join(directory, "one.json"))
            many = self.run_search(14, os.path.join(directory, "many.json"))
            self.assertEqual(one["y_exact_num"], many["y_exact_num"])
            self.assertEqual(one["h"], many["h"])

    def test_serial_parallel_certificates_intersect(self):
        from flint import arb, ctx
        with tempfile.TemporaryDirectory() as directory:
            outputs = []
            for jobs in (1, 14):
                output = os.path.join(directory, f"cert{jobs}.json")
                subprocess.run([
                    sys.executable, "s05_certify.py", "validate",
                    "--jobs", str(jobs), "--output", output,
                ], cwd=ROOT, env=ENV, check=True, stdout=subprocess.DEVNULL)
                with open(output) as handle:
                    outputs.append(json.load(handle))
            ctx.prec = outputs[0]["precision"]
            left, right = (arb(item["h_ball"]) for item in outputs)
            self.assertFalse(left.upper() < right.lower())
            self.assertFalse(right.upper() < left.lower())
            self.assertGreater(float(left.lower()), 1.218)


@unittest.skipUnless(
    os.path.exists(os.path.join(
        ROOT, "work", "probes", "qcal_seed20260726",
        "m460_n900", "lll.txt",
    )) and os.path.exists(os.path.join(
        ROOT, "work", "probes", "hurst1900_seed20260726",
        "m460_n1900", "base_basis.txt",
    )),
    "NU900/NU1900 warm-start artifacts unavailable",
)
class ExistingWarmLiftAcceptance(unittest.TestCase):
    @unittest.skipUnless(
        os.environ.get("MERTENS_SLOW_TESTS") == "1",
        "set MERTENS_SLOW_TESTS=1 (~70 sec)",
    )
    def test_m460_exact_recovery_and_lift(self):
        import lift_structured_lattice
        source = os.path.join(
            ROOT, "work", "probes", "qcal_seed20260726", "m460_n900"
        )
        target = os.path.join(
            ROOT, "work", "probes", "hurst1900_seed20260726", "m460_n1900"
        )
        with tempfile.TemporaryDirectory() as directory:
            manifest = lift_structured_lattice.lift(
                os.path.join(source, "base_basis.txt"),
                os.path.join(source, "base_meta.json"),
                os.path.join(source, "lll.txt"),
                os.path.join(target, "base_basis.txt"),
                os.path.join(target, "base_meta.json"),
                os.path.join(directory, "U.txt"),
                os.path.join(directory, "warm.txt"),
                os.path.join(directory, "manifest.json"),
            )
            self.assertEqual(manifest["determinant"], "1")
            self.assertEqual(manifest["exact_division_remainders"], 0)
            self.assertEqual(
                manifest["source_reconstruction_differences"], 0
            )
            self.assertEqual(manifest["parity"], "VERIFIED")


if __name__ == "__main__":
    unittest.main()
