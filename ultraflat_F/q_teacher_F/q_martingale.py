"""Teacher p49 diagnostics. p_j is a martingale in new torus coordinate.
Monte-Carlo only; confidence intervals are NOT rigorous certificates.
"""
from __future__ import annotations
import argparse,json
import numpy as np

def trace(n=65536,d=49,seed=0):
    rng=np.random.default_rng(seed)
    p=np.cos(rng.uniform(-np.pi,np.pi,n))
    energy=[float(np.mean(p*p))]
    single=[float(np.mean(p*np.cos(np.zeros(n))))]  # overwritten
    single=[float(np.mean(p*p))] # 2*b_{e1}=E[p cos t1]=1/2
    for j in range(2,d+1):
        z=1-p*p
        inc=(.5*z+.125*z*z)
        phase=np.cos(rng.uniform(-np.pi,np.pi,n))
        single.append(float(np.mean(inc))/2)
        p+=inc*phase
        energy.append(float(np.mean(p*p)))
    return {'M':energy,'singleton_cos_correlation':single}

def run(n=65536,repeats=4,d=49):
    runs=[trace(n,d,seed+443) for seed in range(repeats)]
    energies=np.asarray([r['M'] for r in runs]); corr=np.asarray([r['singleton_cos_correlation'] for r in runs]);
    out={'d':d,'sample_size_per_run':n,'repeats':repeats,
         'energy_mean':energies.mean(0).tolist(),'energy_sd':energies.std(0,ddof=1).tolist(),
         'singleton_correlation_mean':corr.mean(0).tolist(),
         'singleton_energy_proxy':float(2*np.sum(corr.mean(0)**2))}
    return out

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--samples',type=int,default=65536);a.add_argument('--repeats',type=int,default=4);a.add_argument('--out',default='teacher_moments.json');args=a.parse_args()
    z=run(args.samples,args.repeats);open(args.out,'w').write(json.dumps(z,indent=2));
    for j in [2,3,4,8,12,16,24,32,40,49]:print('d=',j,'M=',round(z['energy_mean'][j-1],6),'std=',round(z['energy_sd'][j-1],6),'unseen floor to q>=.990225=',round(max(0,.9902251996-z['energy_mean'][j-1]),6))
    print('singleton Fourier energy proxy',z['singleton_energy_proxy'])
