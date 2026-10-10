#!/usr/bin/env python3
"""Genuine q49-guided Fourier student pilot.
Train on p49, a rigorous L2 proxy for Jackson q49 (not pointwise exact).
This STUDENT does NOT enforce OpenAI coefficient balance and is NOT an F certificate.
Dictionary: first 16 singleton cosines and four resonant odd-parity (2,1) products.
24 Fourier sign pairs total, no parallel sign pairs.
"""
import argparse,json
import numpy as np
import torch

def data(n,seed,d=49):
  rng=np.random.default_rng(seed)
  c=np.cos(rng.uniform(-np.pi,np.pi,(n,d)))
  p=c[:,0].copy()
  for j in range(1,d):
    u=1-p*p
    p += (.5*u+.125*u*u)*c[:,j]
  features=[np.sqrt(2)*c[:,i] for i in range(16)]
  features += [2*(2*c[:,0]**2-1)*c[:,j] for j in range(1,5)]
  return np.stack(features,axis=1).astype('float64'),p

def run(steps=600,seed=202610,train_n=24000,test_n=12000):
    torch.set_num_threads(1);torch.manual_seed(seed)
    X,Y=data(train_n,seed);Xt,Yt=data(test_n,seed+3)
    xt=torch.tensor(X); yt=torch.tensor(Y)
    w=torch.nn.Parameter(torch.zeros(X.shape[1],dtype=torch.float64))
    opt=torch.optim.Adam([w],lr=.04)
    history=[]
    for step in range(steps):
        idx=torch.randint(train_n,(3072,))
        fit=xt[idx]@w
        loss=torch.mean((fit-yt[idx])**2)
        opt.zero_grad();loss.backward();opt.step()
        if step%150==0 or step==steps-1:
            v=Xt@w.detach().numpy()
            history.append({'step':step,'heldout_mse_to_p49':float(np.mean((v-Yt)**2)),
               'heldout_F_energy':float(np.mean(v*v)),
               'heldout_sup_lower':float(np.max(np.abs(v)))})
    v=Xt@w.detach().numpy()
    return {'model':'q49 p49 teacher + 24 sign-pair Fourier student',
        'q49_proxy_L2_error_upper':0.004994448565542868**.5,
        'train_n':train_n,'test_n':test_n,'training_steps':steps,'history':history,
        'final_weights':w.detach().numpy().tolist(),
        'warning':'No coefficient balance, uniform norm, or 99%-energy certificate. Diagnostics only.'}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--steps',type=int,default=600);a.add_argument('--out',default='q49_distillation.json');r=a.parse_args()
    z=run(steps=r.steps);print(json.dumps(z['history'],indent=2));open(r.out,'w').write(json.dumps(z,indent=2))
