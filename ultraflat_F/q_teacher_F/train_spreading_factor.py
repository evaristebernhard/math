#!/usr/bin/env python3
"""OpenAI Lemma 4.2 spreading factor pilot: equal Fourier coefficient magnitudes exactly.
For finite T, sampled-error diagnostics only, not a theorem-level alpha guarantee.
"""
import argparse,json
import numpy as np
import torch

def bump(z,edge=.025):
    a=np.abs(z);t=(a-(.5-edge))/edge
    out=np.ones_like(a);m=(t>0)&(t<1);tt=t[m]
    l=np.exp(-1/tt);r=np.exp(-1/(1-tt))
    out[m]=r/(l+r);out[a>=.5]=0
    return out

def train(T=63,beta=1.0,steps=650,seed=31,mesh=768,edge=.025):
    torch.set_num_threads(1);torch.manual_seed(seed)
    L=2*int(T*abs(beta)/2)+1
    u=torch.arange(-(L//2),L//2+1,dtype=torch.float64)
    z=np.arange(mesh,dtype=float)/mesh-.5
    g=bump(z,edge)
    target=torch.tensor(g*np.exp(1j*np.pi*T*beta*z*z))
    E=torch.exp(2j*np.pi*torch.tensor(z,dtype=torch.float64)[:,None]*u[None,:])/np.sqrt(L)
    phase=torch.nn.Parameter((np.sign(beta)*np.pi/4-np.pi*u*u/(T*beta)).clone())
    opt=torch.optim.Adam([phase],lr=.04)
    logs=[]
    for step in range(steps+1):
        if step<steps: opt.zero_grad()
        f=E@torch.exp(1j*phase)
        err=torch.abs(f-target)
        loss=.6*torch.mean(err*err)+.4*torch.logsumexp(12*err,0)/12
        if step in (0,steps):
            logs.append({'step':step,'sampled_max_error':float(err.max().detach()),
                         'mse':float(torch.mean(err*err).detach()),
                         'sampled_max_f':float(f.abs().max().detach())})
        if step<steps:loss.backward();opt.step()
    return {'T':T,'L':L,'beta':beta,'edge_width':edge,'target_L2_grid':float(np.mean(g*g)),
            'logs':logs,'theta':phase.detach().cpu().numpy().tolist(),
            'exact_coefficient_modulus':1/np.sqrt(L),
            'warning':'Grid diagnostics only; NOT an F or rigorous Lemma 4.2 approximation.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--T',type=int,default=63)
    p.add_argument('--steps',type=int,default=650);p.add_argument('--out',default='factor_result.json')
    a=p.parse_args();z=train(T=a.T,steps=a.steps)
    print(json.dumps({k:v for k,v in z.items() if k!='theta'},indent=2))
    open(a.out,'w').write(json.dumps(z,indent=2))
