"""Smoke test for the self-contained sign/center certificate."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SevenCycleCertificateTest(unittest.TestCase):
    def test_full_interval_certificate(self):
        run = subprocess.run(
            [sys.executable, str(ROOT / "proof" / "certify_seven.py")],
            cwd=ROOT, capture_output=True, text=True, check=True, timeout=60,
        )
        self.assertIn("CERTIFIED SIGNS, center ordering, and nonunit center multiplier", run.stdout)
        self.assertIn("center Q bracket", run.stdout)
        self.assertEqual(run.stdout.count("D( "), 6)


if __name__ == "__main__":
    unittest.main()
