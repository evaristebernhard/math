#!/usr/bin/env python3
"""Exploratory LP for the minimum-weight-48 branch using the correct octic spectrum.

Setup:
  * C is an 8-divisible binary [169,19,48] code;
  * c is a fixed weight-48 word;
  * R=Res(C;c) has 2^18 H=<c> cosets and length 121;
  * each H-coset is represented by a canonical state (r,a;u,v), a<=24, u<=v,
    where r is the residual weight and u,v are the two global lift weights.

Unlike the archived invalid experiment, this script keeps the full degree-8 strict
weight set, including 88,96,104,112.  It imposes:
  * exact coset count 2^18;
  * nonnegativity of normalized split-MacWilliams moments up to a chosen total degree;
  * the exact global trade-off A64 + 21 A48 >= 533;
  * optional lower bounds on residual minimum distance.

This is a floating-point feasibility/optimization diagnostic, not an exact certificate.
If a case is infeasible here, an exact dual certificate should be extracted separately.
"""

from __future__ import annotations

from itertools import combinations_with_replacement
from math import comb
import numpy as np
from scipy.optimize import linprog

GLOBAL_ALLOWED = (0,48,64,72,80,88,96,104,112,120,128,136,144,152,160,168)
R_SIZE = 2**18


def krawtchouk(n: int, degree: int, weight: int) -> int:
    if degree == 0:
        return 1
    k0 = 1
    k1 = n - 2*weight
    if degree == 1:
        return k1
    a,b = k0,k1
    for j in range(1,degree):
        num = (n-2*weight)*b - (n-j+1)*a
        assert num % (j+1) == 0
        a,b = b, num//(j+1)
    return b


def states():
    out=[]
    for u,v in combinations_with_replacement(GLOBAL_ALLOWED,2):
        s=u+v-48
        d=u-v+48
        if s%2 or d%2:
            continue
        r=s//2
        a=d//2
        if 0<=r<=121 and 0<=a<=24:
            out.append((r,a,u,v))
    return sorted(out)


def normK(n,j,w):
    return krawtchouk(n,j,w)/comb(n,j)


def feature(st,i,j):
    r,a,_u,_v=st
    return normK(121,i,r)*(normK(48,j,a)+normK(48,j,48-a))


def count_weight(st,w):
    _r,_a,u,v=st
    return int(u==w)+int(v==w)


def solve(min_residual: int, max_total_degree: int=10, objective: str='feas'):
    S=states(); m=len(S)
    zero=(0,0,0,48)
    zi=S.index(zero)

    Aeq=[np.ones(m)]
    beq=[float(R_SIZE)]
    Aub=[]; bub=[]

    # Split-MacWilliams positivity: sum_s n_s Phi_{i,j}(s) >= 0.
    moments=[]
    for i in range(max_total_degree+1):
        for j in range(max_total_degree+1-i):
            if i==0 and j==0:
                continue
            moments.append((i,j))
            row=np.array([-feature(st,i,j) for st in S],dtype=float)
            Aub.append(row); bub.append(0.0)

    # Exact global trade-off, used as a valid linear inequality.
    trade=np.array([count_weight(st,64)+21*count_weight(st,48) for st in S],dtype=float)
    Aub.append(-trade); bub.append(-533.0)

    bounds=[]
    for k,st in enumerate(S):
        r=st[0]
        if k==zi:
            bounds.append((1.0,1.0))
        elif r<min_residual:
            bounds.append((0.0,0.0))
        else:
            bounds.append((0.0,None))

    if objective=='feas':
        c=np.zeros(m)
    elif objective=='A48':
        c=np.array([count_weight(st,48) for st in S],dtype=float)
    elif objective=='A64':
        c=np.array([count_weight(st,64) for st in S],dtype=float)
    elif objective=='low44':
        c=np.array([1.0 if st[0]==44 else 0.0 for st in S],dtype=float)
    elif objective=='low48':
        c=np.array([1.0 if st[0]==48 else 0.0 for st in S],dtype=float)
    else:
        raise ValueError(objective)

    res=linprog(c,A_ub=np.array(Aub),b_ub=np.array(bub),A_eq=np.array(Aeq),b_eq=np.array(beq),
                bounds=bounds,method='highs',options={'presolve':True})
    return S,moments,res


def summarize(min_residual,deg):
    print(f'\n=== min residual >= {min_residual}, split total degree <= {deg} ===')
    S,mom,res=solve(min_residual,deg,'feas')
    print('states:',len(S),'moments:',len(mom),'feasible:',res.success, res.message)
    if not res.success:
        return
    x=res.x
    def A(w): return sum(x[k]*count_weight(st,w) for k,st in enumerate(S))
    print('one feasible point: A48=%.6f A64=%.6f trade=%.6f' % (A(48),A(64),A(64)+21*A(48)))
    used=[(x[k],st) for k,st in enumerate(S) if x[k]>1e-5]
    used.sort(reverse=True)
    print('largest active states:')
    for val,st in used[:12]: print('  %.3f'%val, st)
    for obj in ('A48','A64'):
        _,_,rr=solve(min_residual,deg,obj)
        print('min',obj,':', rr.fun if rr.success else 'infeasible')


def main():
    S=states()
    print('canonical states:',len(S))
    print('residual weights:',sorted({s[0] for s in S}))
    assert len(S)==72
    for deg in (6,8,10,12):
        summarize(48,deg)
    for deg in (8,10,12):
        summarize(44,deg)

if __name__=='__main__':
    main()
