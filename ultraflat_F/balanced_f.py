#!/usr/bin/env python3
"""Experiments with directly balanced auxiliary F, WITHOUT d-fold spreading.

For nonparallel integer a_j and v=(rho,1)*scale:
  c_{+a_j}=sqrt(w_j)*exp(1j*phi_j), c_{-a_j}=conjugate,
  w_j=|a_j.v|, 2*sum w_j=1.

F(x)=2 sum sqrt(w_j) cos(2pi a_j*x+phi_j).
Squared L2 norm is exactly 1. Minimize ||F^2 - 1||_2^2 using FFT with
4*maxdegree +1 grid so quartic integration is unaliased.
"""
import argparse
import json
import math
import numpy as np
from scipy.optimize import minimize


def support(radius, limit=None, family='primitive'):
    pts=[]
    for a in range(0, radius+1):
        for b in range(-radius,radius+1):
            if a==0 and b<=0: continue
            if a==0 and b!=1 and family=='primitive': continue
            if family=='primitive' and math.gcd(a,abs(b)) != 1: continue
            if family=='nonparallel' and math.gcd(a,abs(b)) != 1:continue
            if family=='diagonal' and a!=b and a!=-b: continue
            if a==0 and b==0: continue
            pts.append((a,b))
    pts.sort(key=lambda p:(max(abs(p[0]),abs(p[1])),abs(p[0])+abs(p[1]),p[0],p[1]))
    if limit: pts=pts[:limit]
    return np.asarray(pts,dtype=np.int64)

class BalancedF:
    def __init__(self, a, v=(1,0.3),oversampling=1):
        self.a=np.asarray(a,dtype=int)
        weights=np.abs(self.a @ np.array(v,dtype=float))
        if np.min(weights)<=1e-12: raise ValueError('zero weight')
        self.w=weights/(2*weights.sum())
        ax=int(np.abs(self.a[:,0]).max()); ay=int(np.abs(self.a[:,1]).max());
        self.nx=oversampling*(4*ax+1);self.ny=oversampling*(4*ay+1)
        self.num=self.nx*self.ny
        self.ix=self.a[:,0]%self.nx
        self.iy=self.a[:,1]%self.ny
        self.jx=(-self.a[:,0])%self.nx
        self.jy=(-self.a[:,1])%self.ny

    def fft_poly(self, phases):
        C=np.zeros((self.nx,self.ny),complex)
        ca=np.sqrt(self.w)*np.exp(1j*phases)
        C[self.ix,self.iy]=ca
        C[self.jx,self.jy]=np.conj(ca)
        f=np.fft.ifft2(C).real*self.num
        return f

    def fun_grad(self,phases):
        f=self.fft_poly(phases)
        g=(f*f-1)*f
        cost=np.mean((f*f-1)**2)
        ghat=np.fft.fft2(g)/self.num
        grad=-8*np.sqrt(self.w)*np.imag(np.exp(1j*phases)*np.conj(ghat[self.ix,self.iy]))
        return float(cost),grad

    def optimize(self,restarts=3,seed=17,maxiter=600):
        rng=np.random.default_rng(seed)
        best=None
        for k in range(restarts):
            init=rng.uniform(-np.pi,np.pi,size=len(self.w))
            opt=minimize(self.fun_grad,init,jac=True,method='L-BFGS-B',
                   options={'maxiter':maxiter,'ftol':1e-13,'gtol':1e-8})
            f=self.fft_poly(opt.x)
            record={'J':float(opt.fun),'min':float(np.min(f)),'max':float(np.max(f)),'sup_grid':float(np.max(np.abs(f))),
               'range_abs_grid':[float(np.min(np.abs(f))),float(np.max(np.abs(f)))],
               'nit':int(opt.nit),'success':bool(opt.success),'phase':opt.x.tolist()}
            if best is None or record['J']<best['J']: best=record
        return best


def main():
    p=argparse.ArgumentParser();p.add_argument('--radius',type=int,default=4);p.add_argument('--limit',type=int,default=0)
    p.add_argument('--rho',type=float,default=.3);p.add_argument('--restarts',type=int,default=3)
    p.add_argument('--maxiter',type=int,default=600);p.add_argument('--seed',type=int,default=17)
    p.add_argument('--output',default='')
    args=p.parse_args()
    a=support(args.radius,args.limit or None)
    prob=BalancedF(a,v=(1,args.rho))
    ans=prob.optimize(args.restarts,args.seed,args.maxiter)
    report={'model':'exactly_balanced_2d','radius':args.radius,'D':len(a),'v_direction':[1,args.rho],
       'grid':[prob.nx,prob.ny], 'weights':prob.w.tolist(),'freq':a.tolist(), **ans}
    print(json.dumps({k:v for k,v in report.items() if k not in ('weights','freq','phase')},indent=2))
    if args.output:
        with open(args.output,'w') as w:json.dump(report,w,indent=2)
if __name__=='__main__':main()
