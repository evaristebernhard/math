#!/usr/bin/env python3
"""p2 teacher training of six EXACTLY balanced frequency sign pairs.
Exploratory only; p2 has energy 0.5685, not suitable for Proposition 4.1.
"""
import json,argparse
import numpy as np
import torch

def p2_support():
    return np.array([(1,0),(0,1),(2,1),(2,-1),(4,1),(4,-1)],int),np.array([.5,19/128,-5/64,-5/64,1/256,1/256],float)

def train(seed=11,steps=1200,lambda_teacher=1.,lambda_quartic=.6,lambda_sup=2.):
    torch.set_num_threads(1);torch.manual_seed(seed)
    a,b=p2_support()
    t=torch.arange(65,dtype=torch.float64)/65*2*np.pi
    x,y=torch.meshgrid(t,t,indexing='ij')
    xyz=torch.stack([x.ravel(),y.ravel()],dim=-1)
    angle=xyz@torch.tensor(a,dtype=torch.float64).T
    q=torch.cos(xyz[:,0]);u=1-q*q;q=q+(.5*u+.125*u*u)*torch.cos(xyz[:,1])
    mass=float(2*np.sum(b*b))
    phase=torch.nn.Parameter(torch.tensor(np.where(b<0,np.pi,0.),dtype=torch.float64))
    rho=torch.nn.Parameter(torch.tensor(.23,dtype=torch.float64))
    optim=torch.optim.Adam([phase,rho],lr=.025);history=[]
    for step in range(steps+1):
        if step<steps:optim.zero_grad()
        v=torch.stack([torch.ones_like(rho),rho])
        w0=torch.abs(torch.tensor(a,dtype=torch.float64)@v)+1e-12
        w=mass*w0/(2*w0.sum())
        F=2*(torch.sqrt(w)[None,:]*torch.cos(angle+phase)).sum(1)
        lt=torch.mean((F-q)**2);lq=torch.mean((F*F-mass)**2)
        ls=torch.mean(torch.relu(torch.abs(F)-1)**2)
        loss=lambda_teacher*lt+lambda_quartic*lq+lambda_sup*ls
        if step in (0,steps):
            history.append({'step':step,'loss':float(loss.detach()),'teacher_mse':float(lt.detach()),'quartic_error':float(lq.detach()),
               'sampled_sup':float(F.abs().max().detach()),'rho':float(rho.detach()),'mass':mass})
        if step<steps:loss.backward();optim.step()
    return {'history':history,'frequencies':a.tolist(),'mass':mass,'phase':phase.detach().numpy().tolist(),
            'warning':'sampled data only, not compliant F'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--steps',type=int,default=1200);p.add_argument('--out',default='pilot.json')
    a=p.parse_args();result=train(steps=a.steps);print(json.dumps(result['history'],indent=2))
    open(a.out,'w').write(json.dumps(result,indent=2))
