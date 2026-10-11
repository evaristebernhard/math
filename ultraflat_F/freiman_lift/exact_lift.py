#!/usr/bin/env python3
"""Exact rational fourth-moment audit for integer Fourier lifts of tuned p2.
Uses only Python stdlib. Not an ultraflat F constructor.
"""
from fractions import Fraction as Q
from collections import defaultdict
from random import Random
import json, argparse, math

BASE={(1,0):Q(1,2), (0,1):Q(19,128), (2,1):Q(-5,64),
      (-2,1):Q(-5,64), (4,1):Q(1,256), (-4,1):Q(1,256)}

def full_coeffs(kmap=None):
    coeff={}
    for a,b in BASE.items():
        k=0 if kmap is None else kmap[a]
        f=a+(k,)
        coeff[f]=b
        coeff[tuple(-x for x in f)]=b
    return coeff

def conv(coeff):
    out=defaultdict(Q)
    for a,ca in coeff.items():
        for b,cb in coeff.items():
            h=tuple(i+j for i,j in zip(a,b))
            out[h]+=ca*cb
    return {h:c for h,c in out.items() if c}

def sums(coeff):
    M=sum((x*x for x in coeff.values()),Q(0))
    r=conv(coeff)
    corr=sum((c*c for h,c in r.items() if any(h)),Q(0))
    fourth=sum((c*c for c in r.values()),Q(0))
    return dict(M=float(M),fourth=float(fourth),corr=float(corr),
                J=float((1-M)**2+corr),
                unit_energy_sup_lower=float(math.sqrt(float(fourth))/float(M)),
                M_exact=str(M),fourth_exact=str(fourth))

def lifted_energy(kmap):
    return sums(full_coeffs(kmap))

def kmap_linear(w1,w2):
    return {s:w1*s[0]+w2*s[1] for s in BASE}

def integer_balance(nu):
    return {s:int(round(float(b*b)/float(nu))) for s,b in BASE.items()}

def audit(nu=Q(1,10000000),trials=80,seed=41):
    base=sums(full_coeffs())
    linear=lifted_energy(kmap_linear(2,1))
    k=integer_balance(nu)
    balanced=lifted_energy(k)
    maxerr=max(abs(float(Q(v)*nu/b**2)-1) for s,b in BASE.items() for v in [k[s]])
    mass=sum(2*float(nu)*abs(k[s]) for s in BASE)
    rng=Random(seed)
    fourth=[]
    for trial in range(trials):
        rand={s:rng.randint(-20,20) for s in BASE}
        fourth.append(lifted_energy(rand)['fourth'])
    return dict(seed=seed,trials=trials,base=base,linear=linear,balanced_lift=balanced,
                balance_k={str(s):k[s] for s in BASE},nu=str(nu),
                max_relative_balance_error=maxerr,weight_mass=mass,
                random_F4_min=min(fourth) if fourth else None,
                random_F4_median=sorted(fourth)[len(fourth)//2] if fourth else None,
                random_F4_max=max(fourth) if fourth else None,
                caveat='No supremum guarantee for the non-linear balance lift.')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--trials',type=int,default=80)
    p.add_argument('--nu-denom',type=int,default=10000000)
    p.add_argument('--output',default='')
    args=p.parse_args()
    result=audit(Q(1,args.nu_denom),args.trials)
    print(json.dumps(result,indent=2))
    if args.output:
        with open(args.output,'w') as f:json.dump(result,f,indent=2)
