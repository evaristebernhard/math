#!/usr/bin/env python3
"""Exact rational Fourier coefficients for the bounded degree-2 recursion.

p1=cos(y1), pj=p_{j-1}+(1-p_{j-1}^2)/2*cos(yj).

It shows why L2-energy compression alone cannot preserve the L-infinity
bound used by OpenAI. Do not run beyond d=5 without reworking convolution.
"""
import argparse
from collections import defaultdict
from fractions import Fraction


def square(s):
    out=defaultdict(Fraction)
    x=list(s.items())
    for i,(a,v) in enumerate(x):
        for b,w in x[i:]:
            h=tuple(u+z for u,z in zip(a,b))
            out[h]+=v*w*(1 if a==b else 2)
    return {k:v for k,v in out.items() if v}


def generate(d):
    if not 1<=d<=5:raise ValueError('1<=d<=5 for this exact audit')
    z={(1,):Fraction(1,2),(-1,):Fraction(1,2)}
    for j in range(2,d+1):
        sq=square(z)
        sq[(0,)*(j-1)]=sq.get((0,)*(j-1),Fraction(0))-1
        out={k+(0,):v for k,v in z.items()}
        for k,v in sq.items():
            if v:
                out[k+(1,)]=-v/4
                out[k+(-1,)]=-v/4
        z=out
    return z

def main():
    a=argparse.ArgumentParser();a.add_argument('--depth',type=int,default=5)
    x=a.parse_args()
    s=generate(x.depth)
    mags=sorted((float(abs(v)) for v in s.values()),reverse=True)
    e=sum(v*v for v in mags);l1=sum(mags)
    print(f'd={x.depth} nonzero={len(s)} sign_pairs={len(s)//2} energy={e:.12g} L1={l1:.12g}')
    for keep in (50,100,108,200,500,1000,2000,5000,10000):
        if keep>len(mags):continue
        got=sum(v*v for v in mags[:keep])/e
        tail=l1-sum(mags[:keep])
        print(f'keep={keep:6d} L2_fraction={got:.9f} deleted_L1={tail:.9f}')
    print('The deleted L1 is the guaranteed sup-norm error bound; L2 pruning alone is not sufficient.')

if __name__=='__main__':main()
