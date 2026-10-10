#!/usr/bin/env python3
"""Reproducible exact-rational (except certified rational enclosure of pi) calculations
for a finite, nonparallel-frequency, bounded real auxiliary polynomial.

Given Jackson order n and dimension r, no r-dimensional Fourier tensor is built.
"""
import argparse
from fractions import Fraction as Q
from math import gcd
from functools import lru_cache
from decimal import Decimal, localcontext

@lru_cache(None)
def mobius(n):
    result=1
    d=2
    while d*d<=n:
        if n%d==0:
            n//=d;result=-result
            if n%d==0:return 0
            while n%d==0:n//=d
        d+=1
    return -result if n>1 else result

def profile(n):
    a={i:Q(n-abs(i),n) for i in range(-n+1,n)}
    h={k:sum((a.get(j,Q(0))*a.get(k-j,Q(0)) for j in a),Q(0)) for k in range(-2*n+2,2*n-1)}
    return {k:h[k]/h[0] for k in range(1,2*n-1,2)}

def calc(n,r):
    t=profile(n)
    ks=list(t)
    A={u:sum((t[k]/k)**2 for k in ks if k%u==0) for u in range(1,2*n-1,2)}
    U=sum((mobius(u)*A[u]**r for u in A),Q(0))
    S=sum((Q(abs(mobius(u)),u**r) for u in A),Q(0))
    count=sum((mobius(u)*(2*(((2*n-2)//u+1)//2))**r for u in A))//2
    # M_raw=(8/pi^2)^r*U; M_normalized=M_raw/S^2
    # exact rational bracketing of pi to 15 decimal digits
    pi_lo=Q(3141592653589793,10**15)
    pi_hi=Q(3141592653589794,10**15)
    lower=(Q(8)/pi_hi**2)**r * U/S**2
    upper=(Q(8)/pi_lo**2)**r * U/S**2
    with localcontext() as ctx:
        ctx.prec=24
        lo=Decimal(lower.numerator)/Decimal(lower.denominator)
        up=Decimal(upper.numerator)/Decimal(upper.denominator)
    return dict(n=n,r=r,D=count,cutoff=2*n-2,pi_lower=str(pi_lo),pi_upper=str(pi_hi),
         S_as_rational=str(S),U_as_rational=str(U),normalised_energy_lower=str(lo),
         normalised_energy_upper=str(up),normalised_energy_bracket_width=str(up-lo),
         formula='M=(8/pi^2)^r * U / S^2',
         note='F constructed via a product of Jackson-convolved sign(cos) functions, followed by projection onto gcd=1 Fourier frequencies; the polynomial is divided by S to certify supnorm <=1. The Fourier coefficients are NOT balanced against |a dot v|.')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--n',type=int,default=8)
    ap.add_argument('--dimension',type=int,default=2)
    args=ap.parse_args()
    import json
    print(json.dumps(calc(args.n,args.dimension),ensure_ascii=False,indent=2))
