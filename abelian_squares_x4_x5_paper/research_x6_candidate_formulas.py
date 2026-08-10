from math import floor


def AS(w):
    n=len(w); pa=[0]*(n+1)
    for i,c in enumerate(w): pa[i+1]=pa[i]+(c=='a')
    out=set()
    for i in range(n):
        for j in range(i+2,n+1,2):
            h=(j-i)//2
            if pa[i+h]-pa[i]==pa[j]-pa[i+h]: out.add(w[i:j])
    return out


def theta(w): return len(AS(w))

def cpar(u,q): return sum(1 for x in range(u+1) if x%2==q%2)


def A_word(s,q,t): return 'b'*s+'a'+'b'*q+'a'*5+'b'*t

def A_formula(s,q,t):
    assert q>=1
    M=max(s,q,t); u=min(s,q)
    C6=0 if t<q else min(s,t-q)+1
    return 2+floor(M/2)+cpar(u,q)+C6


def B_word(q,r,t): return 'a'*2+'b'*q+'a'*3+'b'*r+'a'+'b'*t

def B_formula(q,r,t):
    assert q>=1 and r>=1
    M=max(q,r,t)
    ans=floor(M/2)+1  # pure b plus aa
    # rank 1 across q and across r
    ans += (q%2==0)
    ans += cpar(min(t,r),r)
    if q==r and q%2==0:
        ans -= 1  # ab^q a counted from both adjacent-pair locations
    # rank 2
    ans += (q%2==0)  # a^2 b^q a^2
    ans += (r>=q)    # a b^q a^3 b^q
    if q>=r:
        ans += min(t,q-r)+1  # b^{r+z} a^3 b^r a b^z
    # rank 3
    ans += (q>=r and t>=q-r)
    return ans


def D_word(s,q,t): return 'b'*s+'a'*2+'b'*q+'a'*4+'b'*t

def D_formula(s,q,t):
    assert q>=1
    M=max(s,q,t); u=min(s,q)
    C6=0 if t<q else min(s,t-q)+1
    return floor(M/2)+(u+1)+(q%2==0)+cpar(u,q)+(min(q,t)+1)+C6


def target(n): return 2+floor((n-4)/4)


def W114(s,p,q,t): return 'b'*s+'a'+'b'*p+'a'+'b'*q+'a'*4+'b'*t

def W222(s,p,q,t): return 'b'*s+'a'*2+'b'*p+'a'*2+'b'*q+'a'*2+'b'*t

def W141(s,p,q,t): return 'b'*s+'a'+'b'*p+'a'*4+'b'*q+'a'+'b'*t

def W123(s,p,q,t): return 'b'*s+'a'+'b'*p+'a'*2+'b'*q+'a'*3+'b'*t

def lower123(s,p,q,t):
    N=max(s,p,q,t); nu=min(p,q); v=min(s,p)
    G=cpar(v,p)-(1 if p==q and p%2==0 else 0)
    eps=q%2
    K=max(0,min(s,t-p+eps)+1)
    return floor(N/2)+nu+1+(q%2==0)+cpar(nu,q)+(t>=q)+G+K


def W213(s,p,q,t): return 'b'*s+'a'*2+'b'*p+'a'+'b'*q+'a'*3+'b'*t

def lower213(s,p,q,t):
    N=max(s,p,q,t); r=min(s,p); nu=min(p,q)
    cross=cpar(nu,p)+cpar(nu,q)-(1 if p==q and p%2==0 else 0)
    ans=floor(N/2)+(r+1)+cross
    if p<=q:
        eps=(p-q)%2
        K=0 if t<eps else min(s,t-eps)+1
        ans+=K
    return ans


def main():
    for s in range(7):
        for q in range(1,8):
            for t in range(7):
                w=A_word(s,q,t)
                f=A_formula(s,q,t)
                z=theta(w)
                assert f==z, ('A',s,q,t,f,z,w,AS(w))
    print('PASS A exact formula')

    for q in range(1,9):
        for r in range(1,9):
            for t in range(8):
                w=B_word(q,r,t)
                f=B_formula(q,r,t)
                z=theta(w)
                assert f==z, ('B',q,r,t,f,z,w,AS(w))
    print('PASS B exact formula')

    for s in range(8):
        for q in range(1,9):
            for t in range(8):
                w=D_word(s,q,t)
                f=D_formula(s,q,t)
                z=theta(w)
                assert f==z, ('D',s,q,t,f,z,w,AS(w))
                assert z >= floor((s+q+t)/2)+2, ('D coarse',s,q,t,z)
    print('PASS D=2+4 exact formula and coarse bound')

    for Bmass in range(4,25):
        T=2+floor((Bmass+2)/4)
        for s in range(Bmass+1):
            for p in range(1,Bmass-s+1):
                for q in range(1,Bmass-s-p+1):
                    t=Bmass-s-p-q
                    assert theta(W114(s,p,q,t)) >= T, ('114',Bmass,s,p,q,t)
                    assert theta(W222(s,p,q,t)) >= T, ('222',Bmass,s,p,q,t)
                    assert theta(W141(s,p,q,t)) >= T, ('141',Bmass,s,p,q,t)
    print('PASS three easy three-run families through B=24')

    for Bmass in range(2,35):
        T=2+floor((Bmass+2)/4)
        for s in range(Bmass+1):
            for p in range(1,Bmass-s+1):
                for q in range(1,Bmass-s-p+1):
                    t=Bmass-s-p-q
                    w=W123(s,p,q,t)
                    L=lower123(s,p,q,t)
                    assert L<=theta(w), ('123 selected overcount',s,p,q,t,L,theta(w))
                    assert L>=T, ('123 target',s,p,q,t,L,T)
                    w=W213(s,p,q,t)
                    L=lower213(s,p,q,t)
                    assert L<=theta(w), ('213 selected overcount',s,p,q,t,L,theta(w))
                    assert L>=T, ('213 target',s,p,q,t,L,T)
    print('PASS selected-family lower bounds for 1+2+3 and 2+1+3 through B=34')

    print('\nB equality triples by n (q,r,t), n=6+q+r+t:')
    for n in range(10,33):
        eq=[]
        N=n-6
        for q in range(1,N):
            for r in range(1,N-q+1):
                t=N-q-r
                if t>=0 and B_formula(q,r,t)==target(n): eq.append((q,r,t))
        if eq: print(n,eq)

if __name__=='__main__': main()
