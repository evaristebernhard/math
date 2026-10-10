#!/usr/bin/env python3
"""N=128, endpoint-constrained signed Littlewood learning.

Main step: softmax loss on complex Fourier samples and parity-preserving
opposite-sign swaps. This learns a discrete sign vector, not a proof of the
OpenAI asymptotic construction. Optional STE torch stage for initialization.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
from numba import njit

@njit(cache=True)
def loss_grid(pr,pi,n,kappa):
    mx=-1e20
    for h in range(len(pr)):
        a=math.sqrt(pr[h]*pr[h]+pi[h]*pi[h])/math.sqrt(n)
        v=kappa*abs(a-1.0)
        if v>mx: mx=v
    ss=0.
    for h in range(len(pr)):
        a=math.sqrt(pr[h]*pr[h]+pi[h]*pi[h])/math.sqrt(n)
        ss+=math.exp(kappa*abs(a-1.0)-mx)
    return (mx+math.log(ss/len(pr)))/kappa

@njit(cache=True)
def pair_loss(pr,pi,er,ei,i,j,signi,n,kappa):
    mx=-1e20
    for h in range(len(pr)):
        xr=pr[h]-2*signi*(er[i,h]-er[j,h]);xi=pi[h]-2*signi*(ei[i,h]-ei[j,h])
        a=math.sqrt(xr*xr+xi*xi)/math.sqrt(n)
        val=kappa*abs(a-1.0)
        if val>mx:mx=val
    ss=0.
    for h in range(len(pr)):
        xr=pr[h]-2*signi*(er[i,h]-er[j,h]);xi=pi[h]-2*signi*(ei[i,h]-ei[j,h])
        a=math.sqrt(xr*xr+xi*xi)/math.sqrt(n)
        ss+=math.exp(kappa*abs(a-1.0)-mx)
    return (mx+math.log(ss/len(pr)))/kappa

@njit(cache=True)
def do_swap(sign,pr,pi,er,ei,i,j):
    si=sign[i]
    for h in range(len(pr)):
        pr[h]-=2*si*(er[i,h]-er[j,h]);pi[h]-=2*si*(ei[i,h]-ei[j,h])
    sign[i]=-si;sign[j]=si

@njit(cache=True)
def swap_anneal(sign,er,ei,steps,kappa,temp0,temp1,seed):
    np.random.seed(seed)
    n=len(sign);m=er.shape[1]
    pr=np.zeros(m);pi=np.zeros(m)
    for k in range(n):
        for h in range(m):
            pr[h]+=sign[k]*er[k,h];pi[h]+=sign[k]*ei[k,h]
    value=loss_grid(pr,pi,n,kappa)
    best=value;best_sign=sign.copy();accepted=0
    for step in range(steps):
        parity=np.random.randint(2)
        i=2*np.random.randint(n//2)+parity
        j=2*np.random.randint(n//2)+parity
        if sign[i]==sign[j]:continue
        v=pair_loss(pr,pi,er,ei,i,j,sign[i],n,kappa)
        temp=temp0*(temp1/temp0)**(step/max(steps-1,1))
        if v<value or np.random.random()<math.exp(min(0.,(value-v)/temp)):
            do_swap(sign,pr,pi,er,ei,i,j)
            value=v;accepted+=1
            if value<best:
                best=value;best_sign=sign.copy()
    return best_sign,best,accepted

def endpoint_project(v,n=128,plus_even=38,plus_odd=32):
    v=np.asarray(v).reshape(n)
    x=-np.ones(n,dtype=np.int8)
    for parity,plus in ((0,plus_even),(1,plus_odd)):
        ids=np.arange(parity,n,2)
        x[ids[np.argsort(v[ids])[-plus:]]]=1
    assert x.sum()==12 and (x*np.where(np.arange(n)%2==0,1,-1)).sum()==12
    return x

def metrics(s,m=131072):
    z=np.fft.fft(s.astype(float),n=m)
    amp=np.abs(z)/np.sqrt(len(s))
    # Grid + uniform Bernstein first derivative based on sup norm itself.
    eta=np.pi*(len(s)-1)/m
    max_s=float(np.max(amp)/(1-eta))
    min_s=float(max(0,np.min(amp)-eta*max_s))
    return dict(grid_min=float(amp.min()),grid_max=float(amp.max()),
                circle_lower_conservative=min_s,circle_upper_conservative=max_s,
                epsilon_bound=max(1-min_s,max_s-1),
                endpoint_1=int(s.sum()),endpoint_minus1=int(np.dot(s,(-1)**np.arange(len(s)))),grid=m)

def get_initials(rng,folder,random_count):
    base=[]
    names=['optimized_wave_signs_N128.csv','refined_signs_N128.csv','pd_tuned_N128_d30_signs.csv',
           'pd_original_N128_d30_signs.csv']
    for f in names:
        path=Path(folder)/f
        if path.exists():
            v=np.loadtxt(path,delimiter=',').reshape(-1)
            if v.size==128:base.append((f,endpoint_project(v)))
    for i in range(random_count):
        base.append((f'random_{i}',endpoint_project(rng.standard_normal(128))))
    return base

def train_ste(seed=14,steps=800,batches=3,m=1024):
    """Straight-through differentiable projection; purely heuristic initialization."""
    import torch
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    results=[]
    for b in range(batches):
        raw=torch.nn.Parameter(0.5*torch.randn(128,dtype=torch.float64))
        optim=torch.optim.Adam([raw],lr=0.08)
        for it in range(steps):
            optim.zero_grad()
            hard=torch.tensor(endpoint_project(raw.detach().numpy()),dtype=torch.float64)
            soft=torch.tanh(raw/1.2)
            s=hard+soft-soft.detach()
            ampl=torch.abs(torch.fft.fft(s,n=m))/np.sqrt(128)
            err=torch.abs(ampl-1.0)
            temperature=12.+28.*it/max(1,steps-1)
            objective=torch.logsumexp(err*temperature,dim=0)/temperature-math.log(m)/temperature
            objective.backward()
            torch.nn.utils.clip_grad_norm_([raw],2.)
            optim.step()
        result=endpoint_project(raw.detach().numpy())
        results.append((f'ste_{b}',result))
    return results

def run(args):
    rng=np.random.default_rng(args.seed)
    m=args.mesh;n=128
    t=np.arange(m)
    angle=2*np.pi*np.arange(n)[:,None]*t[None,:]/m
    er=np.cos(angle);ei=-np.sin(angle)
    candidates=get_initials(rng,args.seed_dir,args.restarts)
    if args.ste_steps:
        candidates+=train_ste(seed=args.seed,steps=args.ste_steps,batches=args.ste_restarts,m=m)
    history=[];best=None;best_score=float('inf')
    for idx,(name,signs) in enumerate(candidates):
        cur=signs.copy()
        for stage,kappa,temp0,temp1,steps in [('anneal',args.kappa,.025,.0003,args.steps),
                                               ('polish',args.polish_kappa,.004,.00004,args.polish_steps)]:
            cur,score,accepted=swap_anneal(cur,er,ei,steps,kappa,temp0,temp1,args.seed+idx*137+(stage=='polish')*100000)
        z=np.fft.fft(cur.astype(float),n=m)
        a=np.abs(z)/np.sqrt(n)
        maxerr=float(np.max(np.abs(a-1)))
        item=dict(seed=name,loss=float(score),sample_error=maxerr,sample_min=float(a.min()),sample_max=float(a.max()))
        history.append(item)
        if maxerr<best_score:
            best_score=maxerr;best=cur.copy()
        print(json.dumps(item),flush=True)
    Path(args.out).parent.mkdir(exist_ok=True,parents=True)
    np.savetxt(args.out,best,fmt='%d',delimiter=',')
    cert=metrics(best)
    record=dict(mode='endpoint-constrained swap annealing with optional STE',
                n=n,restarts=len(candidates),train_mesh=m,best_train_grid_error=best_score,
                results=history,certification=cert)
    Path(args.report).write_text(json.dumps(record,indent=2))
    print('FINAL',json.dumps(cert))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--seed',type=int,default=20261010)
    p.add_argument('--seed-dir',default=str(HERE / 'seeds'))
    p.add_argument('--steps',type=int,default=14000)
    p.add_argument('--polish-steps',type=int,default=5000)
    p.add_argument('--restarts',type=int,default=8)
    p.add_argument('--mesh',type=int,default=2048)
    p.add_argument('--kappa',type=float,default=22)
    p.add_argument('--polish-kappa',type=float,default=65)
    p.add_argument('--ste-steps',type=int,default=0)
    p.add_argument('--ste-restarts',type=int,default=0)
    p.add_argument('--out',default=str(HERE / 'best_signs_N128.csv'))
    p.add_argument('--report',default=str(HERE / 'results.json'))
    run(p.parse_args())
