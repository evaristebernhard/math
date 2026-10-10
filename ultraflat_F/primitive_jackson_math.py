#!/usr/bin/env python3
"""Exact finite-support combinatorics and high precision L2 formulas for primitive-frequency sign-product polynomials.
No Fourier tensor is formed.
"""
import numpy as np, math
from functools import lru_cache

@lru_cache(None)
def mobius(t:int)->int:
    if t==1:return 1
    n=t; mu=1; p=2
    while p*p<=n:
        if n%p==0:
            n//=p;mu=-mu
            if n%p==0:return 0
            while n%p==0:n//=p
        p+=1
    if n>1:mu=-mu
    return mu

def jackson_profile(n:int):
    # Fejer_n normalized to have integral 1. Jackson kernel is Fejer_n squared normalized.
    k=np.arange(-n+1,n, dtype=float)
    a=1-np.abs(k)/n
    w=np.convolve(a,a)
    w=w/w[len(w)//2]
    pos=np.arange(1,2*n-1,2)
    b2=8/(np.pi*np.pi)/pos**2*w[len(w)//2+pos]**2
    return pos,b2

def model(n,r):
    pos,b2=jackson_profile(n)
    Et=np.zeros(pos[-1]+1)
    for t in range(1,len(Et),2):
        Et[t]=b2[pos%t==0].sum()
    energy=sum(mobius(t)*(Et[t]**r) for t in range(1,len(Et),2))
    ss=sum(abs(mobius(t))/t**r for t in range(1,len(Et),2))
    # Finite support count (signed primitive tuples) /2
    count=sum(mobius(t)*(2*((((2*n-2)//t)+1)//2))**r for t in range(1,2*n-1,2))//2
    return b2.sum(),energy,ss,energy/ss**2,count

if __name__=='__main__':
    for r in [2,3,4,5,6]:
      print('r=',r)
      for n in [6,11,21,41,81,161,321,641,1281]:
        e,m,s,rho,d=model(n,r)
        print(' n=%5d oneD=%.6f primitive=%.6f S=%.6f cert M>=%.6f D=%d'%(n,e,m,s,rho,d),flush=True)
