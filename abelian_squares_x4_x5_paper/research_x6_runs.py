from itertools import combinations
from collections import defaultdict
from math import floor


def words_with_x_a(n, x=6):
    for pos in combinations(range(n), x):
        s=['b']*n
        for p in pos: s[p]='a'
        yield ''.join(s)


def abelian_squares(w):
    n=len(w); pa=[0]*(n+1)
    for i,c in enumerate(w): pa[i+1]=pa[i]+(c=='a')
    out=set()
    for i in range(n):
        for j in range(i+2,n+1,2):
            h=(j-i)//2
            if pa[i+h]-pa[i]==pa[j]-pa[i+h]: out.add(w[i:j])
    return out


def theta(w): return len(abelian_squares(w))

def target(n): return 2+floor((n-4)/4)


def a_comp(w):
    out=[]; i=0
    while i<len(w):
        if w[i]=='b': i+=1; continue
        j=i
        while j<len(w) and w[j]=='a': j+=1
        out.append(j-i); i=j
    return tuple(out)


def canon_comp(c): return min(c, tuple(reversed(c)))


def main():
    for n in range(10,25):
        by_r=defaultdict(lambda:[10**9,0,None])
        by_c=defaultdict(lambda:[10**9,0,None])
        for w in words_with_x_a(n):
            t=theta(w); c=a_comp(w); r=len(c); cc=canon_comp(c)
            if t<by_r[r][0]: by_r[r]=[t,1,w]
            elif t==by_r[r][0]: by_r[r][1]+=1
            if t<by_c[cc][0]: by_c[cc]=[t,1,w]
            elif t==by_c[cc][0]: by_c[cc][1]+=1
        print('\nN',n,'target',target(n))
        print(' by run count:', {r:(v[0],v[0]-target(n),v[1],v[2]) for r,v in sorted(by_r.items())})
        sharp=[]
        for c,v in sorted(by_c.items()):
            if v[0] <= target(n)+1:
                sharp.append((c,v[0],v[0]-target(n),v[1],v[2]))
        print(' compositions with min <= target+1:')
        for z in sharp: print('  ',z)

if __name__=='__main__': main()
