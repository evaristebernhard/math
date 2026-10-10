#!/usr/bin/env python3
"""Exploratory log-factorization test for lower-rank spreading (NOT a certificate).

For a seed p_d with b_s, gamma fixed, fit
log(|b_s|^2/|s.gamma|) ~= c + sum_j log|s.W_j|.
"""
import sys,json,argparse
import numpy as np
from scipy.optimize import minimize
from pathlib import Path
# More portable: load old source if present; else below in release use local seed module.
from seed_fourier import generate

def source(d):
 s=generate(d)
 out=sorted((tuple(map(int,k)),float(abs(v))) for k,v in s.items() if next((u for u in k[::-1] if u!=0),0)>0)
 return np.asarray([x for x,v in out],dtype=float),np.asarray([v for x,v in out],dtype=float)

def test(d,r,restarts=12,seed=7):
 a,b=source(d)
 gamma=np.sqrt(np.array([2,3,5,7,11][:d],float))
 rho=np.abs(a@gamma)
 t=2*np.log(b)-np.log(rho)
 t=t-np.mean(t)
 rng=np.random.default_rng(seed)
 best=None
 def fg(x):
  W=x.reshape((r,d))
  dot=a@W.T
  # Square-root smoothing avoids numerical infinities; avoid fitting values near zero.
  eps=1e-15
  logs=.5*np.log(dot*dot+eps**2)
  z=logs.sum(axis=1)
  res=(z-z.mean())-t
  loss=float(np.mean(res**2))
  raw=2*res[:,None]*dot/(dot*dot+eps**2)/len(a)
  grad=raw.T@a
  return loss,grad.flatten()
 for k in range(restarts):
  W=rng.normal(size=(r,d))
  opt=minimize(fg,W.flatten(),jac=True,method='L-BFGS-B',options={'maxiter':550,'maxls':35})
  val=opt.x.reshape(r,d)
  dot=a@val.T
  z=np.log(np.abs(dot)+1e-300).sum(axis=1)
  dif=(z-z.mean())-t
  item={'d':d,'D':len(a),'r':r,'log_rms':float(np.sqrt(np.mean(dif**2))),
      'log_max':float(np.max(np.abs(dif))), 'factor_worst':float(np.exp(min(100,np.max(np.abs(dif))))),
      'median_factor':float(np.exp(np.median(np.abs(dif)))),'W':val.tolist(), 'nit':int(opt.nit)}
  if best is None or item['log_rms']<best['log_rms']:best=item
 return best

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',default='');p.add_argument('--restarts',type=int,default=10);args=p.parse_args()
 report=[]
 for d in [3,4]:
  for r in [1,2,3,4,6]:
   ans=test(d,r,args.restarts)
   print({k:round(v,4) if isinstance(v,float) else v for k,v in ans.items() if k!='W'},flush=True)
   report.append(ans)
 if args.output:Path(args.output).write_text(json.dumps(report,indent=2))
