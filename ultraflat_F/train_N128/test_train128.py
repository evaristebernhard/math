"""Simple tests for feasibility, analytical relations, and certificate persistence."""
import unittest
import numpy as np
from train128 import endpoint_project, metrics, loss_grid, pair_loss

class Train128Tests(unittest.TestCase):
    def test_parity_endpoints(self):
        rng=np.random.default_rng(9)
        for i in range(20):
            s=endpoint_project(rng.standard_normal(128))
            self.assertTrue(np.all(np.isin(s,(-1,1))))
            self.assertEqual(int(s.sum()),12)
            self.assertEqual(int(s @ ((-1)**np.arange(128))),12)

    def test_swap_grid_loss(self):
        rng=np.random.default_rng(5)
        n=128;m=256
        s=endpoint_project(rng.normal(size=128))
        z=np.fft.fft(s.astype(float),n=m)
        ii=int(np.flatnonzero((np.arange(n)%2==0)&(s==1))[0])
        jj=int(np.flatnonzero((np.arange(n)%2==0)&(s==-1))[0])
        basis=np.exp(-2j*np.pi*np.arange(n)[:,None]*np.arange(m)[None,:]/m)
        v=pair_loss(z.real,z.imag,basis.real,basis.imag,ii,jj,float(s[ii]),n,22.)
        s[ii],s[jj]=s[jj],s[ii]
        z2=np.fft.fft(s.astype(float),n=m)
        expected=loss_grid(z2.real,z2.imag,n,22.)
        self.assertAlmostEqual(v,expected,places=10)

    def test_certificate_margin(self):
        import pathlib
        s=np.loadtxt(pathlib.Path(__file__).parent/'best_signs_N128.csv',dtype=int,delimiter=',')
        d=metrics(s,m=65536)
        self.assertLess(d['epsilon_bound'],0.77)
        self.assertEqual(d['endpoint_1'],12)

if __name__ == '__main__':unittest.main()
