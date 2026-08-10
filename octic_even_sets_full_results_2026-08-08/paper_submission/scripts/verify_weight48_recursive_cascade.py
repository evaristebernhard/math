#!/usr/bin/env python3
"""Exact verifier for the coding-only recursive residual cascade in the d(K)=48 branch.

This script verifies three new ingredients.

(1) Master first-residual trade-off.  For a 4-divisible [121,18] first residual R
coming from a weight-48 word, the degree-five polynomial

  P(w)=-(w-52)(w-60)(w-64)(w-68)(w-72)/368640

has positive Krawtchouk coefficients and is nonpositive on all allowed weights >=52.
Hence

  3465 A24 + 1050 A32 + 504 A36 + 210 A40 + 70 A44 + 15 A48 >= 51708.

A short incidence threshold argument then forces two equal-weight words among
weights 24,32,36,40,44,48 whose sum has weight <=56.  Thus all first-residual
outlets admit a low 2-dimensional subcode before any geometry is used.

(2) If the recursive branch reaches a general binary [45,16,16] code T, an exact
degree-seven certificate gives A16(T)>=6572.  Incidence forces two 16-words to
meet in at least 6 coordinates.  Residualizing one gives [29,15] with d>=8 and
a word of weight <=10; Griesmer excludes d>=9, hence the residual has d=8.

(3) For a binary [29,15,8] code U, an exact degree-eight certificate gives
A8(U)>=188.  Incidence forces two 8-words to meet in at least 3 coordinates.
Residualizing gives [21,14] with d in {4,5}; the Hamming bound excludes d=5,
so the next residual has d=4.
"""
from fractions import Fraction
from math import comb, ceil


def kraw(n,j,w):
    if j==0: return 1
    a=1; b=n-2*w
    if j==1: return b
    for t in range(1,j):
        num=(n-2*w)*b-(n-t+1)*a
        assert num%(t+1)==0
        a,b=b,num//(t+1)
    return b


def balanced_pair_lower(n,M,w):
    total=M*w
    q,r=divmod(total,n)
    return (n-r)*comb(q,2)+r*comb(q+1,2)


def griesmer(k,d):
    return sum(ceil(d/(2**i)) for i in range(k))


def verify_master_121():
    N=121; SIZE=2**18
    coeff=[
        Fraction(953,40960),
        Fraction(407,40960),
        Fraction(241,122880),
        Fraction(21,40960),
        Fraction(9,163840),
        Fraction(1,98304),
    ]
    def P(w):
        return Fraction(-(w-52)*(w-60)*(w-64)*(w-68)*(w-72),368640)
    assert all(c>0 for c in coeff)
    for w in range(N+1):
        assert sum(coeff[j]*kraw(N,j,w) for j in range(6))==P(w)
    vals={24:Fraction(231),32:Fraction(70),36:Fraction(168,5),
          40:Fraction(14),44:Fraction(14,3),48:Fraction(1)}
    for w,v in vals.items(): assert P(w)==v
    for w in range(52,121,4): assert P(w)<=0
    base=SIZE*coeff[0]-P(0)
    assert base==Fraction(17236,5)
    # Multiply by 15.
    assert 15*base==51708

    # Thresholds sufficient to force an equal-weight pair whose sum has weight <=56.
    # For 4-divisible R, intersections of two codewords are even.
    thresholds={24:2,32:5,36:6,40:10,44:15,48:29}
    target_intersection={24:0,32:4,36:8,40:12,44:16,48:20}
    for w,M in thresholds.items():
        if w==24:
            continue
        lower=balanced_pair_lower(N,M,w)
        pairs=comb(M,2)
        # Average exceeds target-2; even intersections force some pair >= target.
        assert lower > (target_intersection[w]-2)*pairs
    # If none of the thresholds is reached, the master LHS is far too small.
    max_below=(3465*(2-1)+1050*(5-1)+504*(6-1)+210*(10-1)
               +70*(15-1)+15*(29-1))
    assert max_below==13475
    assert max_below<51708
    return vals,thresholds


def verify_45_16():
    N=45; SIZE=2**16
    coeff=[
        Fraction(1863,9350),
        Fraction(28197,299200),
        Fraction(44853,1196800),
        Fraction(1509,108800),
        Fraction(1313,299200),
        Fraction(37,29920),
        Fraction(123,478720),
        Fraction(21,478720),
    ]
    assert all(c>0 for c in coeff)
    def P(w): return sum(coeff[j]*kraw(N,j,w) for j in range(8))
    assert P(16)==1
    for w in range(17,N+1): assert P(w)<=0
    assert P(0)==Fraction(162162,25)
    base=SIZE*coeff[0]-P(0)
    assert base==Fraction(6144498,935)
    assert 6571<base<6572
    M=6572
    lower=balanced_pair_lower(N,M,16)
    assert lower>5*comb(M,2)  # some intersection >=6
    # Residual of a 16-word in a [45,16,16] code has [29,15], d>=8;
    # the neighbour gives a word of weight <=10.  Griesmer excludes d>=9.
    assert griesmer(15,9)==30>29
    return base


def verify_29_8():
    N=29; SIZE=2**15
    coeff=[
        Fraction(1073,29952),
        Fraction(43,1664),
        Fraction(5813,419328),
        Fraction(155,19968),
        Fraction(61,17472),
        Fraction(1,624),
        Fraction(461,838656),
        Fraction(7,39936),
        Fraction(1,29952),
    ]
    assert all(c>0 for c in coeff)
    def P(w): return sum(coeff[j]*kraw(N,j,w) for j in range(9))
    assert P(8)==1
    for w in range(9,N+1): assert P(w)<=0
    assert P(0)==986
    base=SIZE*coeff[0]-P(0)
    assert base==Fraction(21982,117)
    assert 187<base<188
    M=188
    lower=balanced_pair_lower(N,M,8)
    assert lower>2*comb(M,2)  # some intersection >=3
    # Residual is [21,14], d>=4 and the neighbour gives weight <=5.
    # If d>=5, radius-2 Hamming spheres already exceed the ambient space.
    volume=1+21+comb(21,2)
    assert volume==232
    assert (2**14)*volume > 2**21
    return base


def main():
    vals,thresholds=verify_master_121()
    b45=verify_45_16()
    b29=verify_29_8()
    print('Recursive coding cascade certificates OK')
    print('  master: 3465 A24 + 1050 A32 + 504 A36 + 210 A40 + 70 A44 + 15 A48 >= 51708')
    print('  thresholds forcing equal-weight pair with sum <=56:',thresholds)
    print('  [45,16,16]: A16 >= 6572; next residual [29,15,8]')
    print('  [29,15,8]: A8 >= 188; next residual [21,14,4]')


if __name__=='__main__':
    main()
