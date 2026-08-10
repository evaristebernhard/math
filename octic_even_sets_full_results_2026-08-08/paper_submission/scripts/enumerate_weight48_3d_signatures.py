#!/usr/bin/env python3
"""Enumerate 3-dimensional subcode signatures forced by the coding-only
master 2D compression in the d(K)=48 branch.

Fix e0=c of weight 48.  Two equal-weight residual words y,z in the first
residual have weight r in {24,32,36,40,44,48} and y+z has residual weight
s<=56.  The two lifts of each residual word have one of the canonical global
weight pairs below.  For every choice of lift orientations we compute the eight
column-type multiplicities of H=<c,x1,x2> by Walsh inversion.

Results:
  * 697 labeled realizable signatures;
  * 165 orbits under GL(3,2) basis changes fixing c;
  * all seven nonzero weights lie in {48,64,72,80,88,96}.
"""
from itertools import product

GLOBAL={0,48,64,72,80,88,96,104,112,120,128,136,144,152,160,168}
PAIRS={
    24:[(48,48)],
    32:[(48,64)],
    36:[(48,72)],
    40:[(48,80),(64,64)],
    44:[(48,88),(64,72)],
    48:[(48,96),(64,80),(72,72)],
    52:[(64,88),(72,80)],
    56:[(64,96),(72,88),(80,80)],
}


def dot(a,b):
    return ((a & b).bit_count()) & 1


def orientations(p):
    a,b=p
    return [(a,b)] if a==b else [(a,b),(b,a)]


def multiplicities(w):
    # w[v] is the weight of v in F_2^3, with w[0]=0.
    out=[]
    for alpha in range(8):
        s=sum((169-2*w[v]) * (-1 if dot(alpha,v) else 1) for v in range(8))
        if s%8:
            return None
        out.append(s//8)
    return tuple(out) if min(out)>=0 else None


def rank3(vs):
    basis=[]
    for x in vs:
        y=x
        for b in basis:
            y=min(y,y^b)
        if y:
            hb=1<<(y.bit_length()-1)
            basis=[b^y if b&hb else b for b in basis]
            basis.append(y)
            basis.sort(reverse=True)
    return len(basis)


def stabilizer_of_c():
    maps=set()
    for a in range(1,8):
        for b in range(1,8):
            if rank3([1,a,b])!=3:
                continue
            T=[]
            for v in range(8):
                T.append((1 if v&1 else 0) ^ (a if v&2 else 0) ^ (b if v&4 else 0))
            maps.add(tuple(T))
    assert len(maps)==24
    return sorted(maps)


def canonical(weight_tuple,stab):
    return min(tuple(weight_tuple[T[v]] for v in range(8)) for T in stab)


def main():
    labeled=set()
    for r in (24,32,36,40,44,48):
        for s in (24,32,36,40,44,48,52,56):
            if s>56 or s>2*r:
                continue
            inter=r-s//2
            if inter<0 or inter>r or inter%2:
                continue
            for p1 in PAIRS[r]:
                for p2 in PAIRS[r]:
                    for ps in PAIRS[s]:
                        for o1,o2,os in product(orientations(p1),orientations(p2),orientations(ps)):
                            w=(0,48,o1[0],o1[1],o2[0],o2[1],os[0],os[1])
                            if not set(w).issubset(GLOBAL):
                                continue
                            m=multiplicities(w)
                            if m is not None:
                                labeled.add((w,m))
    assert len(labeled)==697
    stab=stabilizer_of_c()
    reps={canonical(w,stab) for w,m in labeled}
    assert len(reps)==165
    assert all(set(w[1:]).issubset({48,64,72,80,88,96}) for w in reps)
    supports=[]
    for w in reps:
        m=multiplicities(w)
        supports.append(169-m[0])
    assert min(supports)==84 and max(supports)==124
    print('labeled signatures:',len(labeled))
    print('orbits fixing c:',len(reps))
    print('support range:',min(supports),max(supports))


if __name__=='__main__':
    main()
