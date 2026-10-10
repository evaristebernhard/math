"""Exploratory high-precision four-flight critical-fold computation. NOT a global proof.
Run: python3 research/discriminant_scan.py (requires mpmath and numpy)."""
import mpmath as m
import numpy as np
m.mp.dps=38

def chart(A,B,r,s):
    A=m.mpf(A);B=m.mpf(B)
    rho=2*m.pi*A/(A+B);L=2*m.pi-rho
    z=m.exp(1j*r);w=m.exp(1j*s);R=m.exp(B*r);S=m.exp(A*s)
    alpha=m.exp(-B*rho);beta=m.exp(A*L);p=m.exp(1j*rho)
    cm=-B/(-B+1j);cp=A/(A+1j)
    Z1=cm*(z-R)/(1-R);Z2=cp*z*(S*w-1)/(S-1)
    Z3=cm*w*(alpha*p*R-z)/(alpha*R-1)
    Z4=cp*(beta-p*S*w)/(beta-S)
    U=Z1-Z3;V=Z1-Z4;Q=Z1-Z2
    d2=2*B*R/(1-R);d3=2*B*R*(1-alpha)/((1-R)*(1-alpha*R));d4=2*B/(1-R)
    br=lambda a,b:m.im(a*m.conj(b))
    delta=br(U,V)
    F=d2*delta-d3*br(Q,V)+d4*br(Q,U)
    W=(d3*m.conj(V)-d4*m.conj(U))/delta
    M=m.re(W*m.conj(W))
    lam=B*(1+R)/(1-R)-m.im(W*Z1)
    return F,M,W,lam,rho

def F(A,B,r,s):return chart(A,B,r,s)[0]
def M(A,B,r,s):return chart(A,B,r,s)[1]
def pd(fun,A,B,r,s,j):
    return m.diff(lambda x:fun(A,B,x,s) if j==0 else fun(A,B,r,x),r if j==0 else s)
def K(A,B,r,s):
    return pd(M,A,B,r,s,0)*pd(F,A,B,r,s,1)-pd(M,A,B,r,s,1)*pd(F,A,B,r,s,0)

def find_fold(A,B,r0,s0):
    A=m.mpf(str(A));B=m.mpf(str(B))
    r,s=m.findroot((lambda r,s:F(A,B,r,s),lambda r,s:K(A,B,r,s)),(m.mpf(str(r0)),m.mpf(str(s0))),tol=m.mpf('1e-26'),maxsteps=30)
    f,mm,w,lam,rho=chart(A,B,r,s)
    fr=pd(F,A,B,r,s,0);fs=pd(F,A,B,r,s,1)
    kr=pd(K,A,B,r,s,0);ks=pd(K,A,B,r,s,1)
    return A,B,r,s,m.sqrt(mm),lam,m.arg(w),rho,(kr*fs-ks*fr)/(2*m.sqrt(mm)*fs**2)

def physical_check(A,B,r,s,mu,lam,t0,rho):
    u=rho-r;v=2*m.pi-rho-s;area=m.mpf(0);maxerr=m.mpf(0)
    flights=[(r,-B,0,1,-1),(s,A,A+B,-1,-1),(u,-B,0,-1,1),(v,A,-A-B,1,1)]
    ranges=[]
    for dt,c,d,y0,y1 in flights:
        def exact(h):
            e=m.exp(-c*h);t=t0+h
            return e*y0-(d-lam)*(1-e)/c+mu/(1+c*c)*(c*m.sin(t)-m.cos(t)-e*(c*m.sin(t0)-m.cos(t0)))
        ys=[float(exact(dt*j/300)) for j in range(301)]
        ranges.append((min(ys),max(ys)))
        area+=m.quad(exact,[0,dt])
        maxerr=max(maxerr,abs(exact(dt)-y1))
        t0+=dt
    ok=(ranges[0][0]>=-1-1e-8 and ranges[0][1]<=1+1e-8 and ranges[1][1]<=-1+1e-8 and
        ranges[2][0]>=-1-1e-8 and ranges[2][1]<=1+1e-8 and ranges[3][0]>=1-1e-8 and maxerr<m.mpf('1e-22'))
    return area/(2*m.pi),ok,maxerr

if __name__=="__main__":
    for a,b,r0,s0 in [(9,1.5,2.855,.255),(8,1.5,2.72,.408),(9,4,2.933,.137),(16,3,3.072,.011)]:
        A,B,r,s,mu,lam,t0,rho,curv=find_fold(a,b,r0,s0)
        xi,firsthit,err=physical_check(A,B,r,s,mu,lam,t0,rho)
        assert xi>0 and curv>0 and firsthit, (a,b,xi,curv,firsthit)
        print('A=',a,'B=',b,'r=',m.nstr(r,15),'s=',m.nstr(s,15),
              'mu=',m.nstr(mu,15),'xi=',m.nstr(xi,13),
              'd2mu/dr2=',m.nstr(curv,14),'sample_first_hit=',firsthit,
              'endpoint_err=',m.nstr(err,3))
    print('Numerical minima only: global uniqueness / L<=7 remains OPEN')
