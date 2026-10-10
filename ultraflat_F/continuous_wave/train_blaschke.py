#!/usr/bin/env python3
"""Differentiable real Blaschke continuous-waveform baseline.
No claim of an effective ultraflat Littlewood algorithm.
Requires numpy, torch; CPU only. The Fourier diagnostics are numerical.
"""
import argparse
import json
import numpy as np
import torch

def build(logits, angles, z, n):
    m=len(logits)
    budget=np.log(n)/4
    floor=min(.01,.5*budget/m)
    alpha=floor+(budget-m*floor)*torch.softmax(logits,dim=0)
    rho=torch.exp(-alpha)
    rc=(rho*torch.cos(angles))[None,:]
    r2=(rho*rho)[None,:]
    Z=z[:,None]
    B=torch.prod((Z*Z-2*rc*Z+r2)/(1-2*rc*Z+r2*Z*Z),dim=1)
    return B,rho

def experiment(n, pairs, mesh, steps, restarts, seed, lr):
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    z=torch.exp(2j*np.pi*torch.arange(mesh,dtype=torch.float64)/mesh)
    records=[]
    best=None
    for run in range(restarts):
        r=torch.nn.Parameter(.03*torch.randn(pairs,dtype=torch.float64))
        ph=torch.nn.Parameter(2*np.pi*torch.rand(pairs,dtype=torch.float64))
        optimizer=torch.optim.Adam([r,ph],lr=lr)
        low=None
        for step in range(steps):
            optimizer.zero_grad()
            B,rho=build(r,ph,z,n)
            hat=torch.fft.fft(B)/mesh
            y=np.sqrt(n)*hat[:n].real
            err=torch.sqrt((y*y-1)**2+1e-6)
            cap=torch.logsumexp(8*err,dim=0)/8-np.log(n)/8
            tail=torch.sum(hat[n:].abs()**2)
            loss=torch.mean((y*y-1)**2)+.2*cap+tail
            if step%25==0 or step==steps-1:
                with torch.no_grad():
                    val=float(loss)
                    if low is None or val<low['loss']:
                        low={'loss':val,'step':step,
                             'radii':rho.detach().numpy().tolist(),
                             'angles':ph.detach().numpy().tolist()}
            loss.backward()
            torch.nn.utils.clip_grad_norm_([r,ph],10)
            optimizer.step()
        print('restart',run,'best_loss',low['loss'],flush=True)
        records.append({'run':run,'loss':low['loss']})
        if best is None or low['loss']<best['loss']:best=low
    return {'n':n,'pairs':pairs,'mesh':mesh,'steps':steps,'restarts':restarts,
            'seed':seed,'best':best,'restarts_summary':records}

def diagnose(model, mesh=32768):
    n=model['n'];d=model['best']
    radii=np.asarray(d['radii']); angles=np.asarray(d['angles'])
    z=np.exp(2j*np.pi*np.arange(mesh)/mesh)
    B=np.ones(mesh,dtype=complex)
    speed=np.zeros(mesh)
    for r,a in zip(radii,angles):
        c=np.cos(a)
        B*=(z*z-2*r*c*z+r*r)/(1-2*r*c*z+r*r*z*z)
        alpha=r*np.exp(1j*a)
        speed+=(1-r*r)/np.abs(z-alpha)**2
        speed+=(1-r*r)/np.abs(z-alpha.conjugate())**2
    coef=np.fft.fft(B)/mesh
    y=np.sqrt(n)*coef[:n]
    cap=max(0,float(np.abs(y.real).max())-1)
    tau2=float(np.sum(np.abs(coef[n:])**2))
    return {'max_unit_modulus_error_grid':float(np.max(abs(abs(B)-1))),
            'max_imag_y_grid':float(np.max(abs(y.imag))),
            'y0':float(y[0].real),
            'min_abs_y':float(np.min(abs(y.real))),
            'max_abs_y':float(np.max(abs(y.real))),
            'tau2_grid':tau2,'tau1_grid':float(np.sum(abs(coef[n:]))),
            'phase_speed_min_over_N_grid':float(speed.min()/n),
            'phase_speed_max_over_N_grid':float(speed.max()/n),
            'rounding_q_bound_from_grid':.5*(1-(1-tau2)/(1+cap)**2),
            'note':'Floating-point sampled diagnostics, not mathematical certification.'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name,default in [('n',200),('pairs',24),('mesh',2048),
                          ('steps',700),('restarts',2),('seed',77)]:
        p.add_argument('--'+name,type=int,default=default)
    p.add_argument('--lr',type=float,default=.035)
    p.add_argument('--out',default='blaschke_results.json')
    args=p.parse_args()
    kw={k:v for k,v in vars(args).items() if k!='out'}
    result=experiment(**kw)
    result['diagnostic']=diagnose(result)
    with open(args.out,'w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result['diagnostic'],indent=2))
