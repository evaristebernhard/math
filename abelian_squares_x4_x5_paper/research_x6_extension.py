from itertools import combinations
from collections import defaultdict
from math import floor


def words_with_x_a(n, x=6):
    for pos in combinations(range(n), x):
        s=['b']*n
        for p in pos: s[p]='a'
        yield ''.join(s)


def AS(w):
    n=len(w); pa=[0]*(n+1)
    for i,c in enumerate(w): pa[i+1]=pa[i]+(c=='a')
    out=set()
    for i in range(n):
        for j in range(i+2,n+1,2):
            h=(j-i)//2
            if pa[i+h]-pa[i]==pa[j]-pa[i+h]: out.add(w[i:j])
    return out


def gaps(w):
    p=[i for i,c in enumerate(w) if c=='a']
    return (p[0],)+tuple(y-x-1 for x,y in zip(p,p[1:]))+(len(w)-1-p[-1],)


def T6(B): return 2+floor((B+2)/4)
def T5(Y): return floor((Y+6)/4)


def main():
    stats=defaultdict(lambda:[10**9,None])
    by_d=defaultdict(lambda:[10**9,None])
    fail_escape=[]
    fail_strong=[]
    for n in range(10,25):
        B=n-6
        for w0 in words_with_x_a(n):
            g0=gaps(w0)
            w=w0 if g0[0] <= g0[-1] else w0[::-1]
            g=gaps(w)
            d=g[0]
            Q=w[d+1:]
            AQ=AS(Q); AW=AS(w)
            y=Q.count('b')
            base=T5(y)
            e=len(AQ)-base
            new=len(AW-AQ)
            deficit=T6(B)-base
            key=(d,e,deficit)
            if new<stats[key][0]: stats[key]=[new,w]
            if new+e < by_d[d][0]: by_d[d]=[new+e,w]
            if new+e < deficit:
                fail_escape.append((w,d,e,new,deficit,len(AW),T6(B)))
            strong=(d+1)//2 + 1
            if new+e < strong:
                fail_strong.append((w,d,e,new,strong,new+e))
    print('fail potential count',len(fail_escape))
    if fail_escape: print('first',fail_escape[:10])
    print('fail strong count',len(fail_strong))
    if fail_strong: print('first strong',fail_strong[:10])
    print('min (e+new) by d:', {d:(v[0],v[1]) for d,v in sorted(by_d.items())})
    print('\nmin new by (d,e,deficit):')
    for key,(new,w) in sorted(stats.items()):
        d,e,defi=key
        if d<=8 and e<=4:
            print(key,'min_new',new,'need_after_surplus',max(0,defi-e),'witness',w)

if __name__=='__main__': main()
