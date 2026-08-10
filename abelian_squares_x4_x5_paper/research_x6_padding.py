from itertools import combinations, product


def words(n,x=6):
    for pos in combinations(range(n),x):
        s=['b']*n
        for p in pos:s[p]='a'
        yield ''.join(s)


def AS(w):
    n=len(w); pa=[0]*(n+1)
    for i,c in enumerate(w):pa[i+1]=pa[i]+(c=='a')
    out=set()
    for i in range(n):
        for j in range(i+2,n+1,2):
            h=(j-i)//2
            if pa[i+h]-pa[i]==pa[j]-pa[i+h]:out.add(w[i:j])
    return out


def main():
    for pad in (1,2):
        minnew=999; witness=None; fails=0
        for n in range(6,21):
            for u in words(n):
                w='b'*pad+u+'b'*pad
                new=len(AS(w)-AS(u))
                if new<minnew:minnew,witness=new,(u,w)
                need=1 if pad==2 else 0
                if new<need:fails+=1
        print('x6 pad',pad,'minnew',minnew,'witness',witness,'fails_need',fails)

    bad=[]
    for n in range(1,13):
        for tup in product('ab', repeat=n):
            u=''.join(tup)
            if 'a' not in u:
                continue
            w='bb'+u+'bb'
            new=len(AS(w)-AS(u))
            if new<1:
                bad.append((u,w))
                if len(bad)>=10:
                    break
        if bad:
            break
    print('general pad2 bad count shown',len(bad),'examples',bad[:10])

if __name__=='__main__':main()
