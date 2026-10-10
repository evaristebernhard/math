import unittest
import numpy as np
from balanced_f import BalancedF, support
from seed_fourier import generate

class BalancedFTests(unittest.TestCase):
    def test_nonparallel(self):
        a=support(5)
        for i,p in enumerate(a):
            for q in a[i+1:]:
                self.assertNotEqual(int(p[0]*q[1]-p[1]*q[0]),0)
    def test_weight_and_energy(self):
        m=BalancedF(support(3), v=(1,0.31))
        x=np.linspace(0,2*np.pi,len(m.w),endpoint=False)
        f=m.fft_poly(x)
        self.assertAlmostEqual(2*sum(m.w),1.)
        self.assertAlmostEqual(np.mean(f*f),1.,places=12)
    def test_exact_quartic_fft(self):
        m=BalancedF(support(2),v=(1,0.31))
        x=np.linspace(0,1,len(m.w))
        obj,_=m.fun_grad(x)
        spec={}
        for a,w,p in zip(m.a,m.w,x):
            coeff=np.sqrt(w)*np.exp(1j*p)
            key=tuple(map(int,a))
            spec[key]=coeff
            spec[(-key[0],-key[1])]=np.conj(coeff)
        conv={}
        for a,ca in spec.items():
            for b,cb in spec.items():
                k=(a[0]+b[0],a[1]+b[1]);conv[k]=conv.get(k,0)+ca*cb
        exact=sum(abs(v-(1 if k==(0,0) else 0))**2 for k,v in conv.items())
        self.assertAlmostEqual(exact,obj,places=11)
    def test_gradient(self):
        m=BalancedF(support(3),v=(1,.31))
        x=np.random.default_rng(7).normal(size=len(m.w))
        o,g=m.fun_grad(x)
        for j in range(min(8,len(g))):
            y=x.copy();y[j]+=1e-6
            self.assertAlmostEqual((m.fun_grad(y)[0]-o)/1e-6,g[j],delta=3e-5)
    def test_seed_pairs(self):
        for d,expected in [(2,4),(3,27),(4,350)]:
            s=generate(d)
            self.assertEqual(len(s)//2,expected)

if __name__=='__main__':unittest.main()
