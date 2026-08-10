#!/usr/bin/env python3
"""Exact arithmetic checks for the third-stage coding descent in weight 48."""
from fractions import Fraction
from math import comb


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
    q,r=divmod(M*w,n)
    return (n-r)*comb(q,2)+r*comb(q+1,2)


def verify_47():
    n=47; size=2**16
    coeff=[
        Fraction(1835147,32288256),
        Fraction(68149,2935296),
        Fraction(264611,32288256),
        Fraction(601,225792),
        Fraction(2167,2935296),
        Fraction(5585,32288256),
        Fraction(335,10762752),
        Fraction(5,1537536),
    ]
    assert all(c>0 for c in coeff)
    def P(w): return sum(coeff[j]*kraw(n,j,w) for j in range(8))
    assert P(16)==1
    assert P(17)==Fraction(5,13)
    assert P(18)==Fraction(2375,22932)
    assert all(P(w)<=0 for w in range(19,n+1))
    base=size*coeff[0]-P(0)
    assert base==Fraction(57511661,21021)
    assert 2735<base<2736
    # 2736 low words -> one of 16,17,18 occurs at least 912 times.
    M=912
    assert balanced_pair_lower(n,M,16)>5*comb(M,2)  # t>=6
    assert balanced_pair_lower(n,M,17)>6*comb(M,2)  # t>=7
    assert balanced_pair_lower(n,M,18)>6*comb(M,2)  # t>=7


def verify_49():
    n=49; size=2**16
    coeff=[
        Fraction(6515,267904),
        Fraction(9151,803712),
        Fraction(81737,19289088),
        Fraction(9337,6429696),
        Fraction(63,153088),
        Fraction(2845,28933632),
        Fraction(5,279552),
        Fraction(5,2755584),
    ]
    assert all(c>0 for c in coeff)
    def P(w): return sum(coeff[j]*kraw(n,j,w) for j in range(8))
    assert P(16)==1
    assert P(17)==Fraction(11,27)
    assert P(18)==Fraction(847,7176)
    assert all(P(w)<=0 for w in range(19,n+1))
    base=size*coeff[0]-P(0)
    assert base==Fraction(5530165,6279)
    assert 880<base<881
    # 881 low words -> one of 16,17,18 occurs at least 294 times.
    M=294
    assert balanced_pair_lower(n,M,16)>5*comb(M,2)  # t>=6
    assert balanced_pair_lower(n,M,17)>5*comb(M,2)  # t>=6
    assert balanced_pair_lower(n,M,18)>6*comb(M,2)  # t>=7


def verify_sidon_count():
    # A hypothetical [22,14,5] parity-check matrix has 22 columns in F_2^8.
    # There are C(22,2)=231 distinct pair sums, while the complement of
    # {0} union A has 256-1-22=233 elements, leaving exactly two holes.
    assert comb(22,2)==231
    assert 2**8-1-22==233
    assert 233-231==2
    # XOR count: each column occurs 21 times among pair sums, hence xor(pair sums)=xor(A).
    assert 21%2==1


def main():
    verify_47(); verify_49(); verify_sidon_count()
    print('weight48 small-code descent certificates OK')
    print('  [47,16,16]: A16+A17+A18 >= 2736')
    print('  [49,16,16]: A16+A17+A18 >= 881')
    print('  [22,14,5] Sidon-count obstruction checked')


if __name__=='__main__':
    main()
