#!/usr/bin/env python3
"""Exact low-weight trade-off for an even [73,17] second residual.

For any binary even [73,17] code with d>=24, the degree-six polynomial

 Q(w)=(w-30)(w-36)(w-38)(w-44)(w-46)(w-72)/2027520

has positive Krawtchouk coefficients, is nonpositive on every even weight >=30,
and takes Q(24)=21/2, Q(26)=345/88, Q(28)=1.  MacWilliams gives

  924 A24 + 345 A26 + 88 A28 >= 522758.

Hence A24+A26+A28 >=566.  If d=28, then A28>=5941.
"""
from fractions import Fraction

N=73
SIZE=2**17


def kraw(n,j,w):
    if j==0: return 1
    a=1; b=n-2*w
    if j==1: return b
    for t in range(1,j):
        num=(n-2*w)*b-(n-t+1)*a
        assert num%(t+1)==0
        a,b=b,num//(t+1)
    return b


def Q(w):
    return Fraction((w-30)*(w-36)*(w-38)*(w-44)*(w-46)*(w-72),2027520)


def main():
    coeff=[
        Fraction(191,2816),
        Fraction(179,5632),
        Fraction(19,2112),
        Fraction(1357,540672),
        Fraction(257,540672),
        Fraction(47,540672),
        Fraction(1,180224),
    ]
    assert all(c>0 for c in coeff)
    for w in range(74):
        assert sum(coeff[j]*kraw(N,j,w) for j in range(7))==Q(w)
    assert Q(24)==Fraction(21,2)
    assert Q(26)==Fraction(345,88)
    assert Q(28)==1
    for w in range(30,73,2):
        assert Q(w)<=0
    assert Q(0)==Fraction(11799,4)
    base=SIZE*coeff[0]-Q(0)
    assert base==Fraction(261379,44)
    # Multiply by 88:
    # 924 A24 + 345 A26 + 88 A28 >= 522758.
    assert 88*base==522758
    # Since every coefficient on the left is at most 924:
    assert Fraction(522758,924)>565
    # If d=28, only the A28 term remains among the positive-weight terms.
    assert base>5940
    print('Exact [73,17] second-residual trade-off OK')
    print('  924 A24 + 345 A26 + 88 A28 >= 522758')
    print('  hence A24+A26+A28 >= 566')
    print('  if d=28, then A28 >= 5941')

if __name__=='__main__':
    main()
