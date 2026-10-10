"""Deterministic structural checks for three OpenAI-inspired trainable families."""
import unittest, math
import numpy as np
import torch
from train128 import endpoint_project
from packed_wave_train import prepare_mesh,phase_grid,diagnose
from coherent_F_train import p_tuned
from balanced_coherent_train import primitive_support,evaluate

class Tests(unittest.TestCase):
 def setUp(self):
  torch.set_num_threads(1)
  torch.manual_seed(5)
 def test_piecewise_chirp_symmetry_and_band(self):
  K=8; N=128; mesh=prepare_mesh(512,K)
  raw=torch.randn(K+1,dtype=torch.float64)
  phi,x=phase_grid(raw,mesh,K,N)
  B=torch.exp(2j*math.pi*N*phi)
  self.assertLess(float(torch.max(abs(abs(B)-1))),1.e-13)
  self.assertTrue(float(x.min())>.029)
  self.assertTrue(float(x.max())<.971)
  self.assertAlmostEqual(float(phi[256]),.25,places=12)
  self.assertLess(float(torch.max(torch.abs(B[1:256]-torch.conj(torch.flip(B[257:],dims=(0,)))))),1e-12)
  self.assertLess(float(torch.max(torch.abs(torch.fft.fft(B).imag))),1e-9)
 def test_no_spurious_balance_loss(self):
  A=torch.tensor(primitive_support(3),dtype=torch.float64)
  phi=torch.randn(len(A),dtype=torch.float64,requires_grad=True)
  theta=torch.rand((2,2),dtype=torch.float64)
  ang=torch.tensor(.58,dtype=torch.float64,requires_grad=True)
  k=torch.arange(128,dtype=torch.float64)
  y,v,w=evaluate(phi,theta,ang,A,k,128,2,mass=.995)
  self.assertTrue(torch.all(torch.abs(A@v)>1e-9))
  self.assertLess(float(torch.max(torch.abs(torch.abs(A@v)-w)).detach()),1e-14)
  self.assertAlmostEqual(float((2*w.sum()).detach()),.995,places=13)
  self.assertTrue(bool(torch.isfinite(y).all()))
  ((y*y).mean()).backward()
  self.assertTrue(torch.isfinite(phi.grad).all())
  self.assertTrue(torch.isfinite(ang.grad))
 def test_p_d_bounded(self):
  x=torch.rand((100,18),dtype=torch.float64)
  y=p_tuned(x)
  self.assertTrue(float(y.abs().max())<=1.000000000001)
 def test_endpoints(self):
  s=endpoint_project(np.random.default_rng(6).normal(size=128))
  self.assertEqual(int(s.sum()),12)
  self.assertEqual(int(s@((-1)**np.arange(128))),12)
 def test_piecewise_wave_autodiff(self):
  raw=torch.nn.Parameter(torch.randn(17,dtype=torch.float64))
  mesh=prepare_mesh(256,16)
  loss,*_=diagnose(raw,mesh,16,128)
  loss.backward()
  self.assertTrue(torch.isfinite(raw.grad).all())

if __name__=='__main__':unittest.main()
