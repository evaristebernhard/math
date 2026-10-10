#!/usr/bin/env python3
"""Mathematically exact full-circle certificate for real Littlewood signs.

Uses rational unit circle z=(q+ip)^2/(p^2+q^2). Samples at t=p/q=j/M and
t=M/j to cover upper semicircle, max gap in angle <=2/M; for real signs
|P(conj z)|=|P(z)|. Normalized amplitude derivative is bounded by
L=(sum k)/sqrt(N), and for N perfect square this is rational.
All sampled inequalities are checked using arbitrary-size INTEGER arithmetic.
"""
import argparse, math, json
from pathlib import Path
import numpy as np

def exact_homogeneous_eval(signs,p,q):
    d=p*p+q*q; re=q*q-p*p; im=2*p*q
    u=int(signs[-1]);v=0
    t=1
    for k in range(len(signs)-2,-1,-1):
        t*=d
        uu=u*re-v*im+int(signs[k])*t
        vv=u*im+v*re
        u,v=uu,vv
    return u*u+v*v,d**(2*(len(signs)-1))

def certify(signs,M=8192,epsilon_num=47,epsilon_den=100):
    n=len(signs)
    h=math.isqrt(n)
    # sqrt(n)>=floor(sqrt(n)), so this gives a conservative rational derivative bound.
    # L=sum k /sqrt(n) <= n(n-1)/(2floor(sqrt(n)))
    L_num=n*(n-1);L_den=2*h
    # target R in [1-eps,1+eps] after extending grid by L/M
    # at sample R in [(1-eps) + L/M, (1+eps)-L/M]
    den=epsilon_den*L_den*M
    low_num=(epsilon_den-epsilon_num)*L_den*M+L_num*epsilon_den
    high_num=(epsilon_den+epsilon_num)*L_den*M-L_num*epsilon_den
    if low_num<=0 or high_num<=low_num:
        raise ValueError('grid too sparse for chosen epsilon')
    lower_ok=True;upper_ok=True;min_float=1e100;max_float=0;count=0
    for j in range(M+1):
        for p,q in ((j,M),(M,j)):
            if p==0 and q==0: continue
            numerator,den_power=exact_homogeneous_eval(signs,p,q)
            lhs=numerator*den*den
            if lhs < n*den_power*low_num*low_num: lower_ok=False
            if lhs > n*den_power*high_num*high_num: upper_ok=False
            val=math.sqrt(numerator/den_power/n)
            min_float=min(min_float,val);max_float=max(max_float,val)
            count+=1
    return dict(n=n,points=count,M=M,epsilon=f'{epsilon_num}/{epsilon_den}',
                verified_exactly=bool(lower_ok and upper_ok),
                lower_checked=lower_ok,upper_checked=upper_ok,
                sample_min_approx=min_float,sample_max_approx=max_float,
                circle_lower_consequence=float((epsilon_den-epsilon_num)/epsilon_den),
                circle_upper_consequence=float((epsilon_den+epsilon_num)/epsilon_den),
                sample_lower_threshold=float(low_num/den),sample_upper_threshold=float(high_num/den),
                geometry='two rational-slope coordinate grids; nearest angle <= 1/M; mirror uses real coefficients',
                derivative_lipschitz=float(L_num/L_den))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--file',required=True)
    p.add_argument('--M',type=int,default=8192)
    p.add_argument('--epsilon-num',type=int,default=47);p.add_argument('--epsilon-den',type=int,default=100)
    p.add_argument('--out',default='')
    a=p.parse_args()
    signs=np.loadtxt(a.file,dtype=np.int64).reshape(-1)
    if not np.all(np.isin(signs,[-1,1])):raise ValueError('Not real Littlewood signs')
    result=certify(signs,a.M,a.epsilon_num,a.epsilon_den)
    if a.out:Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if not result['verified_exactly']:raise SystemExit(2)
