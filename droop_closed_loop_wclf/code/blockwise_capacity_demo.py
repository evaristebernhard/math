"""Blockwise Hessian hosting-capacity demo with an exactly solved thermal toy.

No external packages. All statements of computer-assisted certification for
actual nonlinear DistFlow additionally require interval-verifiable derivatives.
"""
from math import sqrt


def quadratic_sublevel(c,a,m,lo,hi):
    if m<0 or lo>hi:
        raise ValueError("m>=0 and lo<=hi required")
    if m==0:
        if a==0: return (lo,hi) if c<=0 else None
        cutoff=-c/a
        lo,hi=(lo,min(hi,cutoff)) if a>0 else (max(lo,cutoff),hi)
        return (lo,hi) if lo<=hi else None
    disc=a*a-2*m*c
    if disc<0:return None
    root=sqrt(disc)
    lo,hi=max(lo,(-a-root)/m),min(hi,(-a+root)/m)
    return (lo,hi) if lo<=hi else None


def abs_quadratic_sublevel(c,a,m,k,lo,hi):
    """Sublevel of c+a*s+m*s²/2+k*abs(s) over a compact domain."""
    if k<0:raise ValueError("k>=0 required")
    parts=[]
    for left,right,slope in ((lo,min(hi,0.),a-k),
                             (max(lo,0.),hi,a+k)):
        if left>right:continue
        seg=quadratic_sublevel(c,slope,m,left,right)
        if seg is not None:parts.append(seg)
    return ((min(p[0] for p in parts),max(p[1] for p in parts))
            if parts else None)


def exact_worst_current_sq(lam,pv=.30,c=.05):
    a=lam-pv
    return (a-c)**2 if a<0 else a*a+c*c


def demo():
    pv,c,imax=.30,.05,.20
    # f=(s-wp)^2+wq^2-imax^2; Hessian blocks 2, (-2,0), 2I.
    lams=abs_quadratic_sublevel(-imax**2+c*c,0.,2.,2*c,-pv,.7-pv)
    assert lams is not None
    cert=(pv+lams[0],pv+lams[1])
    exact=(pv+c-imax,pv+sqrt(imax**2-c*c))
    assert abs(cert[0]-.15)<1e-12 and abs(cert[1]-.45)<1e-12
    assert exact[0] <= cert[0] and cert[1] <= exact[1]
    assert exact_worst_current_sq(0,pv,c)>imax**2
    for i in range(1001):
        lam=cert[0]+(cert[1]-cert[0])*i/1000
        assert exact_worst_current_sq(lam,pv,c)<=imax**2+1e-12
    print("Exact toy robust feasible interval:",exact)
    print("Block-Hessian certified inner interval:",cert)
    print("Original isotropic-Hessian inner interval:",
          (pv-sqrt(.035/2),pv+sqrt(.035/2)))


if __name__=="__main__":
    demo()
