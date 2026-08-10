#!/usr/bin/env python3
"""Exact low-weight trade-off for a 4-divisible [121,18,44] residual code.

Using the same degree-five polynomial as the residual-48 abundance certificate,
P(44)=14/3 and P(48)=1 while P(w)<=0 for all 4-divisible w>=52. Hence

  70 A44 + 15 A48 >= 51708.

Consequences checked here:
  * if A44>=15, incidence forces two 44-words to meet in at least 16;
  * if A44<=14, then A48>=3382, and incidence forces two 48-words to meet
    in at least 20.
In either case a 2D low-weight subcode has all three nonzero weights in
{44,48,52,56}.
"""
from fractions import Fraction
from math import comb, ceil

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


def convex_pair_lower(m,k,n=N):
    total=m*k
    q,r=divmod(total,n)
    return (n-r)*comb(q,2)+r*comb(q+1,2)


def main():
    coeff=[Fraction(953,40960),Fraction(407,40960),Fraction(241,122880),
           Fraction(21,40960),Fraction(9,163840),Fraction(1,98304)]
    for w in range(122):
        assert sum(coeff[j]*kraw(N,j,w) for j in range(6))==P(w)
    assert P(44)==Fraction(14,3)
    assert P(48)==1
    for w in range(52,121,4):
        assert P(w)<=0
    base=SIZE*coeff[0]-P(0)
    assert base==Fraction(17236,5)
    # (14/3) A44 + A48 >= 17236/5; multiply by 15.
    assert 15*base==51708

    # Case A44 >= 15: force a 44/44 pair with intersection >=16.
    m44=15
    low44=convex_pair_lower(m44,44)
    assert low44==1485
    assert low44>14*comb(m44,2)

    # Case A44 <=14: force A48 >=3382.
    rhs=Fraction(51708-70*14,15)
    assert rhs==Fraction(50728,15)
    assert ceil(rhs)==3382
    m48=3382
    low48=convex_pair_lower(m48,48)
    assert low48==108815445
    assert low48>18*comb(m48,2)

    print('Exact residual-44 low-weight trade-off OK')
    print('  70 A44 + 15 A48 >= 51708')
    print('  A44>=15 -> a 44/44 pair meets in >=16')
    print('  A44<=14 -> A48>=3382 -> a 48/48 pair meets in >=20')
    print('  hence a 2D subcode has nonzero weights in {44,48,52,56}')

if __name__=='__main__':
    main()
