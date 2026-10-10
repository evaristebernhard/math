#!/usr/bin/env python3
"""Train a piecewise inverse-curvature unit-modulus wave B_N, inspired by
OpenAI (2026) Proposition 5.1, then project/round to real Littlewood signs.

This is deliberately *not* the paper's full F / signed interval packing.
Its differentiable main arcs have constant inverse curvature; arcs are joined
in C1 via a continuous frequency profile. The phase is odd and has integer
endpoint winding, so B(-t)=conj B(t), hence Fourier coefficients are real.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import torch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from train128 import endpoint_project, swap_anneal, metrics

ROOT = Path(__file__).resolve().parent

def prepare_mesh(M, K, device='cpu'):
    t = torch.arange(M,dtype=torch.float64,device=device)/M
    u = torch.where(t<=.5, t, t-1.)
    a = torch.abs(u)
    seg = torch.minimum(torch.floor(a*2*K).long(),torch.tensor(K-1,device=device))
    frac = torch.clamp(a*2*K-seg,0.,1.)
    return t, u, seg, frac

def phase_grid(raw, mesh, K, N):
    _, u, seg, frac = mesh
    z = torch.tanh(raw)
    avg = (.5*z[0]+torch.sum(z[1:-1])+.5*z[-1])/K
    centered=z-avg
    scale=.47/torch.clamp(torch.max(torch.abs(centered)),min=1.)
    x=.5+scale*centered # 0.03 < phase derivative < 0.97
    h=.5/K
    integrals = h*(x[:-1]+x[1:])*.5
    prefix=torch.cat((torch.zeros(1,dtype=torch.float64),torch.cumsum(integrals,dim=0)))
    z_int = prefix[seg]+h*(x[seg]*frac+.5*(x[seg+1]-x[seg])*frac**2)
    phi=torch.sign(u)*z_int
    return phi, x

def diagnose(raw,mesh,K,N):
    phi,x=phase_grid(raw,mesh,K,N)
    B=torch.exp((2j*math.pi*N)*phi)
    f=torch.fft.fft(B)/len(B)
    Y=(N**.5)*f[:N].real
    outside=torch.sum(torch.abs(f[N:])**2)
    # L2 spectrum flatness, fourth-moment soft max, energy leakage
    defect=(torch.abs(Y)-1)
    obj=torch.mean(defect**2)+.25*torch.mean(defect**4)+.8*outside
    # penalize significant imaginary error if numerical symmetry breaks
    obj=obj+10*torch.mean(f[:N].imag**2)
    return obj, Y, outside, x, f, B

def run(args):
    torch.set_num_threads(1)
    torch.manual_seed(args.seed)
    K=args.pieces; N=128
    mesh=prepare_mesh(args.mesh,K)
    ang=2*np.pi*np.arange(N)[:,None]*np.arange(args.swap_mesh)[None,:]/args.swap_mesh
    er=np.cos(ang);ei=-np.sin(ang)
    baseline=np.loadtxt(ROOT/'best_signs_N128.csv',delimiter=',')
    base=metrics(baseline,131072)
    print('baseline',json.dumps(base),flush=True)
    records=[]; winners=[]
    for trial in range(args.restarts):
        idx=torch.arange(K+1,dtype=torch.float64)
        if trial%3==0:
            initial=1.8*torch.where(idx.long()%2==0, 1., -1.) + .3*torch.randn(K+1,dtype=torch.float64)
        elif trial%3==1:
            initial=.8*torch.sin(2*math.pi*(trial+1)*idx/K)+.5*torch.randn(K+1,dtype=torch.float64)
        else:
            initial=1.7*torch.randn(K+1,dtype=torch.float64)
        raw=torch.nn.Parameter(initial)
        opt=torch.optim.Adam([raw],lr=args.lr)
        checkpoint=None
        for step in range(args.steps):
            opt.zero_grad(set_to_none=True)
            loss,Y,tail,x,F,B=diagnose(raw,mesh,K,N)
            loss.backward()
            torch.nn.utils.clip_grad_norm_([raw],10.)
            opt.step()
            if (step+1)%max(1,args.steps//4)==0 or step==0:
                current=float(loss.detach())
                if checkpoint is None or current<checkpoint[0]:
                    checkpoint=(current,raw.detach().clone())
        with torch.no_grad():
            raw.copy_(checkpoint[1]); loss,Y,tail,x,F,B=diagnose(raw,mesh,K,N)
        yr=Y.detach().numpy()
        signs=endpoint_project(yr)
        projected=metrics(signs,131072)
        best=signs.copy(); accepted=None
        for s in range(args.refine_stages):
            new,score,acc=swap_anneal(best,er,ei,args.swaps,16.+24*s,.03/(s+1),.00015/(s+1),args.seed+trial*101+s*7000)
            m=metrics(new,131072)
            if m['epsilon_bound']<metrics(best,131072)['epsilon_bound']:
                best=new.copy()
            accepted=acc
        outcome=metrics(best,131072)
        record={'trial':trial,'K':K,'steps':args.steps,'wave_loss':float(loss.detach()),
                'spectral_tail_energy':float(tail.detach()),'min_abs_Y':float(np.min(np.abs(yr))),
                'max_abs_Y':float(np.max(np.abs(yr))), 'wave_fourier_imag_max':float(torch.max(torch.abs(F[:N].imag))),
                'endpoint_phase_error':float(abs(128*float(.5/K*torch.sum(x[:-1]+x[1:])*.5)-32)),
                'projection_epsilon_bound':projected['epsilon_bound'],
                'refined_epsilon_bound':outcome['epsilon_bound'],
                'refined_min':outcome['grid_min'],'refined_max':outcome['grid_max'],'accepted_last':accepted}
        print('trial',json.dumps(record),flush=True)
        records.append(record);winners.append((outcome['epsilon_bound'],best,yr,x.detach().numpy(),raw.detach().numpy()))
    winners.sort(key=lambda w:w[0]); eps,s,yr,x,raw=winners[0]
    np.savetxt(ROOT/'trained_wave_signs_N128.csv',s.astype(int),fmt='%d',delimiter=',')
    np.savetxt(ROOT/'trained_wave_fourier_N128.csv',yr,fmt='%.16g',delimiter=',')
    Path(ROOT/'trained_wave_control.json').write_text(json.dumps({'pieces':K,'raw':raw.tolist(),'derivative_knots':x.tolist(),'N':N},indent=2))
    result={'architecture':'OpenAI-inspired C1 joined quadratic inverse-curvature wave packets','warning':'Not full Proposition 5.1: no F or lemma 5.2 packing',
            'baseline':base,'trials':records,'best':metrics(s,131072),'best_vs_prior':float(eps-base['epsilon_bound'])}
    (ROOT/'wave_training_results.json').write_text(json.dumps(result,indent=2))
    print('BEST',json.dumps(result['best']),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--pieces',type=int,default=24)
    p.add_argument('--mesh',type=int,default=2048)
    p.add_argument('--steps',type=int,default=2000)
    p.add_argument('--lr',type=float,default=.06)
    p.add_argument('--restarts',type=int,default=4)
    p.add_argument('--swap-mesh',type=int,default=512)
    p.add_argument('--swaps',type=int,default=12000)
    p.add_argument('--refine-stages',type=int,default=2)
    p.add_argument('--seed',type=int,default=20261011)
    run(p.parse_args())
