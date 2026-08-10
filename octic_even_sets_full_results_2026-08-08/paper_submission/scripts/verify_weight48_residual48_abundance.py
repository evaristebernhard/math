#!/usr/bin/env python3
"""Exact certificate for the d(R)=48 outlet in the minimum-weight-48 branch.

If R is a 4-divisible [121,18,48] residual code, the degree-five polynomial

  P(w)=-(w-52)(w-60)(w-64)(w-68)(w-72)/368640

has nonnegative Krawtchouk coefficients, P(48)=1, and P(w)<=0 on every
other nonzero 4-divisible weight 52,...,120.  Hence A_48(R)>=3448.
The script also verifies the incidence step forcing two minimum words to meet
in 20,22,or24 coordinates, so a second residual [73,17] has minimum distance
24,26,or28.
"""
from fractions import Fraction
from math import comb

N=121
SIZE=2**18


def kraw(n,j,w):
    if j==0: return 1
    a=1; b=n-2*w
    if j==1: return b
    for t in range(1,j):
        num=(n-2*w)*b-(n-t+1)*a
        assert num%(t+1)==0
        a,b=b,num//(t+1)
    return b


def P(w):
    return Fraction(-(w-52)*(w-60)*(w-64)*(w-68)*(w-72),368640)


def main():
    coeff=[
        Fraction(953,40960),
        Fraction(407,40960),
        Fraction(241,122880),
        Fraction(21,40960),
        Fraction(9,163840),
        Fraction(1,98304),
    ]
    assert all(c>0 for c in coeff)
    for w in range(0,122):
        lhs=sum(coeff[j]*kraw(N,j,w) for j in range(6))
        assert lhs==P(w)
    assert P(48)==1
    for w in range(52,121,4):
        assert P(w)<=0
    assert P(0)==2652
    lower=SIZE*coeff[0]-P(0)
    assert lower==Fraction(17236,5)
    assert lower>3447
    # Integrality gives A_48(R)>=3448.
    M=3448
    total=M*48
    q,r=divmod(total,N)
    assert (q,r)==(1367,97)
    pair_lower=(N-r)*comb(q,2)+r*comb(q+1,2)
    assert pair_lower==113105580
    pairs=comb(M,2)
    assert pair_lower>19*pairs
    # Pair intersections are even because R is 4-divisible; minimum 48 gives t<=24.
    # Hence some pair has t in {20,22,24}, giving a second residual word of
    # weight 48-t in {28,26,24}.
    print('Exact residual-48 abundance certificate OK')
    print('  A_48(R) >= 3448')
    print('  pair-intersection lower average =', float(Fraction(pair_lower,pairs)))
    print('  some pair meets in 20,22,or24 coordinates')
    print('  therefore second residual minimum lies in {24,26,28}')

if __name__=='__main__':
    main()
