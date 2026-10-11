#!/usr/bin/env python3
"""Exact rank audit for two-sum relations of tuned p2 (requires sympy)."""
from collections import defaultdict
from itertools import combinations_with_replacement
import sympy as sp
from exact_lift import BASE

def rank_audit():
    reps=list(BASE);freq=[]
    for j,a in enumerate(reps):
        freq.extend([(a,j,1),(tuple(-x for x in a),j,-1)])
    sums=defaultdict(list)
    for i,j in combinations_with_replacement(range(len(freq)),2):
        a,ai,asgn=freq[i];b,bi,bsgn=freq[j]
        row=[0]*len(reps);row[ai]+=asgn;row[bi]+=bsgn
        sums[tuple(x+y for x,y in zip(a,b))].append(row)
    rows=[]
    for group in sums.values():
        for row in group[1:]:
            diff=[x-y for x,y in zip(row,group[0])]
            if any(diff):rows.append(diff)
    A=sp.Matrix(rows)
    X=sp.Matrix([[a[0],a[1]] for a in reps])
    assert A*X==sp.zeros(len(rows),2)
    assert A.rank()==len(reps)-2 and X.rank()==2
    return {'sign_pairs':len(reps),'nontrivial_relations':len(rows),
            'relation_rank':A.rank(),'kernel_dimension':2,
            'theorem':'all lifts preserving these relations are linear k_s=alpha*s1+beta*s2'}

if __name__=='__main__':print(rank_audit())
