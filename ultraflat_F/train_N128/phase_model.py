#!/usr/bin/env python3
"""Bounded-phase (unit-modulus) waveform trained by autograd, inspired by OpenAI's B_N.
Research prototype: no effective ultraflat proof.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import torch
from train128 import endpoint_project,metrics,swap_anneal

def run(args):
 torch.set_num_threads(1)
 torch.manual_seed(args.seed)
 n=128;M=args.mesh
 t=torch.arange(M,dtype=torch.float64)/M
 j=torch.arange(1,args.harmonics+1,dtype=torch.float64)
 sx=torch.sin(2*np.pi*t[:,None]*j[None,:])/(2*np.pi*j[None,:])
 records=[]
 for trial in range(args.restarts):
  theta=torch.nn.Parameter(.25*torch.randn(args.harmonics,dtype=torch.float64))
  optimizer=torch.optim.Adam([theta],lr=args.lr)
  bestloss=1e50;bestphase=None
  for step in range(args.steps):
   optimizer.zero_grad()
   a=torch.tanh(theta)
   a=.49*a/(1.+a.abs().sum())
   phase=t*.5+ sx@a
   B=torch.exp(2j*np.pi*n*phase)
   F=torch.fft.fft(B)/M
   y=(n**.5)*F[:n].real
   # Square-amplitude defect and sup-safe regularizer on the prescribed frequencies
   e=(y*y-1)
   v=torch.logsumexp(12*e.abs(),dim=0)/12-np.log(n)/12
   loss=torch.mean(e*e)+.4*v+.6*torch.sum(F[n:].abs()**2)
   loss.backward()
   optimizer.step()
   if float(loss.detach())<bestloss:
    bestloss=float(loss);bestphase=y.detach().cpu().numpy().copy()
  signs=endpoint_project(bestphase)
  before=metrics(signs,m=16384)
  # same parity swaps refine the projection; phase training never changes sign constraints
  er=np.cos(2*np.pi*np.arange(n)[:,None]*np.arange(1024)[None,:]/1024)
  ei=-np.sin(2*np.pi*np.arange(n)[:,None]*np.arange(1024)[None,:]/1024)
  signs,_,_=swap_anneal(signs.copy(),er,ei,args.swaps,24.,.018,.0002,args.seed+trial)
  after=metrics(signs,m=16384)
  record={'trial':trial,'phase_loss':bestloss,'before_epsilon_bound':before['epsilon_bound'],
          'after_epsilon_bound':after['epsilon_bound'],'after_grid_min':after['grid_min'],'after_grid_max':after['grid_max']}
  records.append(record)
  print(record,flush=True)
  if trial==0 or after['epsilon_bound']<best['epsilon_bound']:
   best=after;best_sign=signs.copy()
 np.savetxt(args.out,best_sign,fmt='%d')
 Path(args.report).write_text(json.dumps({'method':'periodic real-coefficient chirp with bounded derivative; differentiable phase regression',
                                          'trials':records,'best':best},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--harmonics',type=int,default=16)
 p.add_argument('--steps',type=int,default=2500)
 p.add_argument('--restarts',type=int,default=4)
 p.add_argument('--swaps',type=int,default=13000)
 p.add_argument('--mesh',type=int,default=2048)
 p.add_argument('--lr',type=float,default=.08)
 p.add_argument('--seed',type=int,default=44)
 p.add_argument('--out',default=str(Path(__file__).parent/'phase_signs_N128.csv'))
 p.add_argument('--report',default=str(Path(__file__).parent/'phase_results.json'))
 run(p.parse_args())
