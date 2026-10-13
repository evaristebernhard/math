"""Regression tests for the reusable continuous-prefix admission driver.

No power-flow model is imported. These tests check endpoint/gap semantics only.
Run: python3 -m unittest discover -s algorithm/tests -v
"""
import pathlib
import sys
import unittest
from fractions import Fraction as Q

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from connected_prefix import cover_prefix, choose_tested_gains


class PrefixTests(unittest.TestCase):
    def test_whole_interval_must_pass(self):
        def oracle(_g, lo, hi):
            return (hi + Q(1, 10)) ** 2 <= Q(4, 5) ** 2
        self.assertTrue(cover_prefix((Q(1),), Q(7,10), oracle).passed)
        cert = cover_prefix((Q(1),), Q(4,5), oracle)
        self.assertFalse(cert.passed)
        self.assertIsNotNone(cert.unresolved)

    def test_no_jumping_over_unknown_gap(self):
        # Even if a higher load cell itself passes, a gap blocks acceptance.
        def oracle(_g, lo, hi):
            return hi <= Q(1, 5) or lo >= Q(1, 4)
        cert = cover_prefix((Q(1),), Q(2, 5), oracle,
                            initial_width=Q(1,10), min_width=Q(1,10000))
        self.assertFalse(cert.passed)

    def test_no_fabricated_global_optimum(self):
        def oracle(g, lo, hi):
            return hi <= Q(g[0],10)
        design, target, record = choose_tested_gains(
            [(Q(3),), (Q(5),)],
            [Q(1,5), Q(2,5), Q(3,5)],
            oracle)
        self.assertEqual(design,(Q(5),))
        self.assertEqual(target,Q(2,5))
        self.assertTrue(record.passed)

if __name__ == "__main__":
    unittest.main()
