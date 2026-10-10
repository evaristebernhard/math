#!/usr/bin/env python3
"""Finite-N differentiable surrogate for OpenAI's coherent stationary phase formula (5.12).
Y_k ~ F(k*theta_h + N*v*Q_h(k/N)), with F replaced by a compact p_d recursion.
This does NOT construct balanced F and does NOT inherit Proposition 5.1 guarantees.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
import torch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from train128 import endpoint_project,metrics,swap_anneal
HERE=Path(__file__).resolve().parent

def p_tuned(y):
    p=torch.cos(2*math.pi*y[...,0])
    for j in range(1,y.shape[-1]):
        u=1-p*p
        b=(15/32)*u+(29/128)*u*u
        p=p+b*torch.cos(2*math.pi*y[...,j])
    return p

def p_original(y):
    p=torch.cos(2*math.pi*y[...,0])
    for j in range(1,y.shape[-1]):
        p=p+.5*(1-p*p)*torch.cos(2*math.pi*y[...,j])
    return p

def forward(rawtheta,rawv,k,H,N,variant):
    j=torch.minimum((k*H//N).long(),torch.tensor(H-1))
    mid=(j+.5)/H
    q=.5*(k/N-mid)**2
    theta=torch.sigmoid(rawtheta)
    v=torch.tanh(rawv)*.16
    y=k[:,None]*theta[j] + N*q[:,None]*v[None,:]
    return p_tuned(y) if variant=='tuned' else p_original(y)

def run(args):
    torch.set_num_threads(1)
    n=128;d=args.dimension;H=args.blocks
    k=torch.arange(n,dtype=torch.float64)
    mm=args.mesh
    t=np.arange(mm)
    ang=2*np.pi*np.arange(n)[:,None]*t[None,:]/mm
    er=np.cos(ang);ei=-np.sin(ang)
    base=np.loadtxt(HERE/'best_signs_N128.csv',delimiter=',')
    baseinfo=metrics(base)
    report=[];winner=(1e9,None,None)
    for trial in range(args.restarts):
        torch.manual_seed(args.seed+trial)
        theta=torch.nn.Parameter(torch.randn((H,d),dtype=torch.float64)*.8)
        v=torch.nn.Parameter(torch.randn((d,),dtype=torch.float64)*.5)
        opt=torch.optim.Adam([theta,v],lr=args.lr)
        bestloss=float('inf');bestvec=None
        for step in range(args.steps):
            opt.zero_grad(set_to_none=True)
            y=forward(theta,v,k,H,n,args.variant)
            # Straight-through endpoint projection: hard signs forward, smooth p_d backward
            h=torch.tensor(endpoint_project(y.detach().numpy()),dtype=torch.float64)
            s=h+(y-y.detach())
            spectrum=torch.fft.fft(s,n=args.mesh)/np.sqrt(n)
            err=(torch.abs(spectrum)-1).abs()
            softpeak=torch.logsumexp(25*err,dim=0)/25-math.log(args.mesh)/25
            loss=.9*softpeak + .25*torch.mean(err**2)+.03*torch.mean((1-y*y)**2)
            loss.backward()
            torch.nn.utils.clip_grad_norm_([theta,v],5.)
            opt.step()
            if (step+1)%100==0:
                with torch.no_grad():
                    sign=endpoint_project(y.detach().numpy())
                    empirical=metrics(sign,32768)['epsilon_bound']
                    if empirical<bestloss:
                        bestloss=empirical;bestvec=sign.copy()
        with torch.no_grad():
            y=forward(theta,v,k,H,n,args.variant).numpy()
        candidate=bestvec if bestvec is not None else endpoint_project(y)
        first=metrics(candidate)
        improved=candidate.copy()
        for s in range(args.refine_stages):
            other,score,accepted=swap_anneal(improved.copy(),er,ei,args.swaps,28+20*s,.012,.00009,args.seed+trial*17+s*123)
            if metrics(other,32768)['epsilon_bound']<metrics(improved,32768)['epsilon_bound']:
                improved=other
        result=metrics(improved)
        item={'trial':trial,'blocks':H,'d':d,'best_during_training':bestloss,
             'initial_eps':first['epsilon_bound'],'polish_eps':result['epsilon_bound'],
             'grid_min':result['grid_min'],'grid_max':result['grid_max'],
             'raw_p_d_mean_sq':float(np.mean(y*y))}
        report.append(item)
        print(item,flush=True)
        if result['epsilon_bound']<winner[0]:winner=(result['epsilon_bound'],improved.copy(),item)
    np.savetxt(HERE/'coherent_F_signs_N128.csv',winner[1],fmt='%d',delimiter=',')
    out={'model':'OpenAI (5.12) coherent stationary-phase F sampled on torus, F surrogate=p_d, STE endpoint projection',
         'not_proved':'Does not satisfy F coefficient balancing or signed packing; no theorem guarantee',
         'baseline':baseinfo,'runs':report,'best':winner[2]}
    (HERE/'coherent_F_results.json').write_text(json.dumps(out,indent=2))
    print('BASELINE',baseinfo['epsilon_bound'],'WINNER',winner[0],flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--dimension',type=int,default=24)
 p.add_argument('--blocks',type=int,default=2)
 p.add_argument('--steps',type=int,default=900)
 p.add_argument('--restarts',type=int,default=3)
 p.add_argument('--lr',type=float,default=.008)
 p.add_argument('--mesh',type=int,default=1024)
 p.add_argument('--swaps',type=int,default=5000)
 p.add_argument('--refine-stages',type=int,default=1)
 p.add_argument('--variant',choices=['tuned','original'],default='tuned')
 p.add_argument('--seed',type=int,default=20261010)
 run(p.parse_args())
