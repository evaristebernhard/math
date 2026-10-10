#!/usr/bin/env python3
"""Exactly balanced F + differentiable stationary phase samples (OpenAI §4, (5.12)).
This meets |c_{±a}|²=|a.v| and sum_{a} |a.v|=1 exactly by parameterization.
It does NOT establish ||F||inf<=1+delta or the signed interval packing lemma.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
import torch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from train128 import endpoint_project,metrics,swap_anneal
ROOT=Path(__file__).resolve().parent

def primitive_support(radius):
    modes=[]
    for a in range(-radius,radius+1):
        for b in range(-radius,radius+1):
            if (a>0 or (a==0 and b>0)) and math.gcd(abs(a),abs(b))==1:
                modes.append((a,b))
    return np.asarray(modes,dtype=np.int64)

def evaluate(coeff_phase, theta, angle, modes, k, n, H, mesh=None, mass=0.995):
    # shared common v and coefficient weights fixed by exact balancing
    direction=torch.stack((torch.cos(angle),torch.sin(angle)))
    proj=torch.abs(modes@direction)
    # prevent exactly zero projections; don't smuggle a zero coefficient into support
    v=mass*direction/(2*torch.sum(proj))
    w=mass*proj/(2*torch.sum(proj))
    c=torch.sqrt(w)
    # F(y) = 2 sum_j sqrt(|a.v|) cos(2pi a.y + phi_j)
    if mesh is None:
        h=torch.minimum(torch.div(k*H,n,rounding_mode='floor').long(),torch.tensor(H-1))
        midpoint=(h+.5)/H
        Q=.5*(k/n-midpoint)**2
        point=k[:,None]*theta[h]+(n*Q)[:,None]*v[None,:]
    else:
        point=mesh
    arg=2*math.pi*point@modes.T + coeff_phase
    y=2*torch.cos(arg)@c
    return y, v, w

def run(args):
    torch.set_num_threads(1)
    torch.manual_seed(args.seed)
    n=128;H=args.blocks
    A=torch.tensor(primitive_support(args.radius),dtype=torch.float64)
    D=len(A)
    k=torch.arange(n,dtype=torch.float64)
    g=torch.arange(args.grid,dtype=torch.float64)/args.grid
    torus=torch.stack(torch.meshgrid(g,g,indexing='ij'),-1).reshape(-1,2)
    t=np.arange(args.swap_mesh)
    ang=2*np.pi*np.arange(n)[:,None]*t[None,:]/args.swap_mesh
    er=np.cos(ang); ei=-np.sin(ang)
    base=np.loadtxt(ROOT/'best_signs_N128.csv',delimiter=',')
    baseline=metrics(base)
    records=[]; winner=(float('inf'),None,None)
    for trial in range(args.restarts):
        torch.manual_seed(args.seed+100*trial)
        phi=torch.nn.Parameter(torch.randn(D,dtype=torch.float64)*2.3)
        theta=torch.nn.Parameter(torch.rand((H,2),dtype=torch.float64))
        angle=torch.nn.Parameter(torch.tensor(.575 + .05*trial,dtype=torch.float64))
        opt=torch.optim.Adam([{'params':[phi,theta],'lr':args.lr},{'params':[angle],'lr':args.lr/12}])
        bestsign=None;bestloss=float('inf')
        for step in range(args.steps):
            opt.zero_grad(set_to_none=True)
            y,v,w=evaluate(phi,theta,angle,A,k,n,H,mass=args.mass)
            ytorus,_,_=evaluate(phi,theta,angle,A,k,n,H,mesh=torus,mass=args.mass)
            F4=torch.mean((ytorus**2-1)**2)
            hard=torch.tensor(endpoint_project(y.detach().numpy()),dtype=torch.float64)
            signal=hard+y-y.detach()
            amp=torch.abs(torch.fft.fft(signal,n=args.sign_mesh))/math.sqrt(n)
            err=torch.abs(amp-1)
            loss=args.f_weight*F4+torch.logsumexp(24*err,dim=0)/24-math.log(args.sign_mesh)/24 + .10*torch.mean(err**2)
            loss.backward()
            torch.nn.utils.clip_grad_norm_([phi,theta,angle],10.)
            opt.step()
            if (step+1)%max(1,args.steps//10)==0:
                candidate=endpoint_project(y.detach().numpy())
                score=metrics(candidate,16384)['epsilon_bound']
                if score<bestloss:bestloss=score;bestsign=candidate.copy()
        with torch.no_grad():
            y,v,w=evaluate(phi,theta,angle,A,k,n,H,mass=args.mass)
            u,_,_=evaluate(phi,theta,angle,A,k,n,H,mesh=torus,mass=args.mass)
            j=float(torch.mean((u*u-1)**2))
            supsample=float(torch.max(torch.abs(u)))
            coefferr=float(torch.max(torch.abs(w-torch.abs(A@v))))
        sign=bestsign.copy() if bestsign is not None else endpoint_project(y.numpy())
        start=metrics(sign)['epsilon_bound']
        for jstage in range(args.refine_stages):
            new,_,_=swap_anneal(sign.copy(),er,ei,args.swaps,24+20*jstage,.02,.00015,args.seed+trial*13+jstage*111)
            if metrics(new,16384)['epsilon_bound']<metrics(sign,16384)['epsilon_bound']:
                sign=new.copy()
        final=metrics(sign)
        rec={'trial':trial,'D':D,'H':H,'fourth_moment_defect':j,'sup_sample_lower_bound':supsample,
             'max_weight_mismatch':coefferr,'initial_epsilon':start,'refined_epsilon':final['epsilon_bound'],
             'grid_min':final['grid_min'],'grid_max':final['grid_max']}
        records.append(rec);print(rec,flush=True)
        if final['epsilon_bound']<winner[0]: winner=(final['epsilon_bound'],sign.copy(),rec)
    np.savetxt(ROOT/'balanced_coherent_signs_N128.csv',winner[1],fmt='%d',delimiter=',')
    (ROOT/'balanced_coherent_results.json').write_text(json.dumps({'model':'F exact coefficient balance + coherent stationary phase Fourier coefficients','limitation':'2D primitive modes, no uniform sup norm bound, no proven B_N','baseline':baseline,'f_weight':args.f_weight,'mass':args.mass,'runs':records,'best':winner[2]},indent=2))
    print('BASELINE',baseline['epsilon_bound'],'BEST',winner[0],flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--radius',type=int,default=3)
 p.add_argument('--f-weight',type=float,default=.18)
 p.add_argument('--mass',type=float,default=.995)
 p.add_argument('--blocks',type=int,default=4)
 p.add_argument('--grid',type=int,default=32)
 p.add_argument('--sign-mesh',type=int,default=1024)
 p.add_argument('--steps',type=int,default=450)
 p.add_argument('--restarts',type=int,default=2)
 p.add_argument('--lr',type=float,default=.025)
 p.add_argument('--swap-mesh',type=int,default=512)
 p.add_argument('--swaps',type=int,default=3500)
 p.add_argument('--refine-stages',type=int,default=1)
 p.add_argument('--seed',type=int,default=20261011)
 run(p.parse_args())
