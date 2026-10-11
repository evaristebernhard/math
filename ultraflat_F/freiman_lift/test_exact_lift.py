#!/usr/bin/env python3
"""Exact rational test suite: python -m unittest discover -s . -p 'test_*.py'."""
import unittest
from fractions import Fraction as Q
from exact_lift import BASE,full_coeffs,sums,integer_balance,kmap_linear,lifted_energy
class TestLift(unittest.TestCase):
    def test_seed_energy(self):
        self.assertEqual(sums(full_coeffs())['M_exact'],'9315/16384')
    def test_linear_relation_preserves_fourth_moment(self):
        self.assertEqual(sums(full_coeffs())['fourth_exact'],
                         lifted_energy(kmap_linear(2,1))['fourth_exact'])
    def test_balance_and_quartic_defect(self):
        nu=Q(1,10000000); k=integer_balance(nu)
        self.assertTrue(all(k[a]>0 for a in BASE))
        self.assertLess(max(abs(float(Q(v)*nu/b**2)-1) for a,b in BASE.items()
                            for v in [k[a]]),.003)
        self.assertEqual(lifted_energy(k)['fourth_exact'],'634969809/1073741824')
    def test_three_mode_obstruction(self):
        A=Q(1,4);B=Q(25,4096)
        self.assertEqual((2*A-B)/(2*A+B),Q(2023,2073))
    def test_real_symmetry(self):
        coeff=full_coeffs(integer_balance(Q(1,10000000)))
        for a,b in coeff.items():
            self.assertEqual(coeff[tuple(-x for x in a)],b)
if __name__=='__main__':unittest.main()
