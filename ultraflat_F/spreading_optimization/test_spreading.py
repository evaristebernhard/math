#!/usr/bin/env python3
import unittest
from hyperplane_groups import group_p3, construct_p3
from factor_gate import report
from seed_fourier import generate

class SpreadingAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=group_p3()
        cls.build=construct_p3(0.01)
    def test_support(self):
        self.assertEqual(self.base['D'],27)
        self.assertEqual(sum(map(len,self.base['group_frequencies'])),27)
    def test_grouped_factors(self):
        self.assertEqual(self.base['groups'],15)
        self.assertEqual(self.base['paired_groups'],12)
    def test_balance(self):
        self.assertLess(self.build['max_relative_product_error'],.00032)
    def test_anisotropic_scale(self):
        self.assertLess(self.build['log10_anisotropic_T_product'],self.build['log10_uniform_T_product'])
    def test_factor_necessary_lower(self):
        r=report(63,mesh=32768,edge=.025)
        self.assertTrue(.20<r['best_possible_L2_error']<.22)
        self.assertTrue(r['phase_projection_sup_grid']>=r['best_possible_L2_error'])
    def test_pruning_bound(self):
        c=generate(3)
        reps=sorted([abs(float(v)) for s,v in c.items() if next(x for x in s if x)>0],reverse=True)
        self.assertEqual(len(reps),27)
        self.assertLessEqual(2*sum(reps[-4:]),.01)

if __name__=='__main__': unittest.main()
