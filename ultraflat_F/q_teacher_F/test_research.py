import unittest
import numpy as np
from certified_symmetry_obstruction import run, alpha, jackson_cutoff
from train_F_pilot import p2_support
from train_spreading_factor import bump
class Tests(unittest.TestCase):
 def test_obstruction(self):
  r=run()
  self.assertGreater(r['necessary_relative_squared_balance_error_eta'],.975)
  self.assertLess(r['necessary_relative_squared_balance_error_eta'],.977)
  self.assertEqual(jackson_cutoff(1),2041028)
 def test_jackson(self):
  self.assertGreater(alpha(2041028,1),0)
  self.assertLess(alpha(2041028,2),alpha(2041028,1))
 def test_p2(self):
  a,b=p2_support()
  self.assertEqual(len(a),6)
  self.assertAlmostEqual(2*np.sum(b*b),.56854248046875)
 def test_cutoff(self):
  self.assertTrue(np.array_equal(bump(np.array([-.5,-.4,0.,.4,.5])),np.array([0.,1.,1.,1.,0.])))
if __name__=='__main__':unittest.main()
