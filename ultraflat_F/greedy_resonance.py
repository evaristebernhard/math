#!/usr/bin/env python3
"""Greedy resonance-directed addition of balanced Fourier frequency pairs.

Exploratory numerical optimization; makes no globally certified flatness claim.
"""
import argparse
import json
import numpy as np
from scipy.optimize import minimize
from balanced_f import BalancedF, support


def canonical(k):
    x, y = map(int,k)
    if x < 0 or (x == 0 and y < 0): return (-x,-y)
    return (x,y)

def candidates(model, phases, max_frequency, top_h=12, max_candidates=36):
    f = model.fft_poly(phases)
    r = np.fft.fft2(f*f)/model.num
    frequencies = []
    # Valid Fourier support of F² (unaliased, as nx>4max |a_x|, likewise y).
    Rx, Ry = 2*np.abs(model.a).max(axis=0)
    for x in range(-Rx,Rx+1):
        for y in range(-Ry,Ry+1):
            if x == 0 and y == 0: continue
            frequencies.append((float(abs(r[x%model.nx,y%model.ny])),(x,y)))
    frequencies.sort(reverse=True)
    existing = [tuple(map(int,z)) for z in model.a]
    all_old = existing + [(-a,-b) for a,b in existing]
    out = {}
    for mass,h in frequencies[:top_h]:
        for a in all_old:
            b = canonical((h[0]-a[0],h[1]-a[1]))
            if b==(0,0) or max(map(abs,b))>max_frequency: continue
            if any(b[0]*q[1]-b[1]*q[0]==0 for q in existing):continue
            out[b]=max(mass,out.get(b,0))
    return [x for x,score in sorted(out.items(),key=lambda el:-el[1])[:max_candidates]]

def local_optim(model,init,maxiter):
    o=minimize(model.fun_grad, init,jac=True,method='L-BFGS-B',
               options={'maxiter':maxiter,'ftol':1e-13,'gtol':1e-8})
    return {'J':float(o.fun),'phases':o.x,'sup_grid':float(np.max(np.abs(model.fft_poly(o.x))))}

def run(start_radius=2,steps=12,max_frequency=8,seed=93,rho=.6180339887498949):
    rng=np.random.default_rng(seed)
    freq=support(start_radius)
    model=BalancedF(freq,v=(1,rho))
    best=model.optimize(restarts=12,seed=seed,maxiter=700)
    current={'J':best['J'],'phases':np.array(best['phase']),'sup_grid':best['sup_grid']}
    history=[{'step':0,'D':len(freq),'J':current['J'],'sampled_sup_lower':current['sup_grid']}]
    for step in range(1,steps+1):
        choices=candidates(model,current['phases'],max_frequency)
        selected=None
        for b in choices:
            nm=BalancedF(np.vstack((freq,np.array(b))),v=(1,rho))
            for phase in (0.,np.pi/2,np.pi,3*np.pi/2):
                init=np.r_[current['phases'],phase]
                sol=local_optim(nm,init,200)
                if selected is None or sol['J']<selected['fit']['J']:
                    selected={'freq':b,'fit':sol}
        if selected is None or selected['fit']['J']>=current['J']-1e-9:
            history.append({'step':step,'status':'no_improvement','candidate_count':len(choices)})
            break
        freq=np.vstack((freq,np.array(selected['freq'])))
        model=BalancedF(freq,v=(1,rho))
        current=selected['fit']
        history.append({'step':step,'new_frequency':selected['freq'],'D':len(freq),
                        'J':current['J'],'sampled_sup_lower':current['sup_grid'],
                        'moment_sup_lower':float(np.sqrt(1+current['J'])),
                        'candidate_count':len(choices)})
        print(history[-1],flush=True)
    return {'settings':{'radius':start_radius,'steps':steps,'max_frequency':max_frequency,'rho':rho,'seed':seed},
            'history':history,'freq':freq.tolist(),'phases':current['phases'].tolist(),
            'final_J':current['J'],'final_sampled_sup_lower':current['sup_grid']}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--steps',type=int,default=12)
    parser.add_argument('--max-frequency',type=int,default=8)
    parser.add_argument('--output',default='')
    args=parser.parse_args()
    o=run(steps=args.steps,max_frequency=args.max_frequency)
    if args.output:
        with open(args.output,'w') as f:json.dump(o,f,indent=2)
