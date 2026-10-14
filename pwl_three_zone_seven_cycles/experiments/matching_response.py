"""Approximate periodic response profiles by explicit affine matching.

Reproduces the illustrative CSV and checks the construction values.
The matching equations and mean integral are given in the manuscript.
"""
from decimal import Decimal as D, getcontext
from functools import lru_cache
from pathlib import Path
import csv,json
getcontext().prec=70
PI=D('3.141592653589793238462643383279502884197169399375105820974944592307816406')
A=D(9);B=D('1.5');MU=D('1.81363');PER=2*PI;RHO=PER*A/(A+B)

@lru_cache(maxsize=200000)
def sc(t):
    s=ts=t;c=tc=D(1);tt=-t*t
    for k in range(1,150):
        ts=ts*tt/((2*k)*(2*k+1));tc=tc*tt/((2*k-1)*(2*k))
        s+=ts;c+=tc
        if max(abs(ts),abs(tc))<D('1e-75'):break
    return s,c

def linear(mat,rhs):
    a=[list(row)+[val] for row,val in zip(mat,rhs)];n=len(a)
    for k in range(n):
        j=max(range(k,n),key=lambda j:abs(a[j][k]));a[j],a[k]=a[k],a[j]
        if not a[k][k]:raise ValueError('singular')
        for j in range(k+1,n):
            q=a[j][k]/a[k][k]
            for l in range(k,n+1):a[j][l]-=q*a[k][l]
    x=[D(0)]*n
    for j in range(n-1,-1,-1):x[j]=(a[j][n]-sum(a[j][k]*x[k] for k in range(j+1,n)))/a[j][j]
    return x

def newton(fun,x,tol=D('1e-42'),iterations=25):
    x=list(map(D,x));h=D('1e-18');n=len(x)
    for it in range(iterations):
        f=fun(x)
        if max(map(abs,f))<tol:return x
        cols=[]
        for j in range(n):
            xp=x.copy();xm=x.copy();xp[j]+=h;xm[j]-=h
            cols.append([(p-m)/(2*h) for p,m in zip(fun(xp),fun(xm))])
        dx=linear(list(zip(*cols)),[-v for v in f])
        scale=D(1)
        for k in range(12):
            nxt=[u+scale*v for u,v in zip(x,dx)]
            if max(map(abs,fun(nxt)))<max(map(abs,f)):break
            scale/=2
        x=nxt
    raise ValueError(('no convergence',x,f))

def flow(t0,t1,x0,c,d,lam=0):
    s0,c0=sc(t0);s1,c1=sc(t1);q0=(lam-d)/c+MU*(c*s0-c0)/(1+c*c);q1=(lam-d)/c+MU*(c*s1-c1)/(1+c*c)
    return (-c*(t1-t0)).exp()*(x0-q0)+q1

def profile(vals,xi=None,four=True,unbiased=False):
    if unbiased:y=vals[0];lam=D(0);times=vals[1:]
    else:y,lam=vals[:2];times=vals[2:]
    ts=[D(0)]+times+[PER]
    levels=[y,D(-1),D(-1),D(1),D(1),y] if four else [y,D(1),D(1),y]
    zones=[(-B,D(0)),(A,A+B),(-B,D(0)),(A,-A-B),(-B,D(0))] if four else [(-B,D(0)),(A,-A-B),(-B,D(0))]
    errors=[];integ=D(0)
    for j,(c,d) in enumerate(zones):
        errors.append(flow(ts[j],ts[j+1],levels[j],c,d,lam)-levels[j+1])
        integ+=((lam-d)*(ts[j+1]-ts[j])+MU*(sc(ts[j])[1]-sc(ts[j+1])[1])-(levels[j+1]-levels[j]))/c
    if xi is not None:errors.append(integ-PER*xi)
    return errors,integ/PER

def critical(r,s):
    qs=[D(0),r,r+s,RHO+s,PER];levels=[D(1),D(-1),D(-1),D(1),D(1)]
    zones=[(-B,D(0)),(A,A+B),(-B,D(0)),(A,-A-B)]
    rows=[];rhs=[]
    for j,(c,d) in enumerate(zones):
        q0=qs[j];q1=qs[j+1];e=(-c*(q1-q0)).exp();s0,c0=sc(q0);s1,c1=sc(q1)
        alpha=(1-e)/c;beta=(c*c1+s1-e*(c*c0+s0))/(1+c*c);gamma=(c*s1-c1-e*(c*s0-c0))/(1+c*c)
        rows.append([alpha,beta,gamma]);rhs.append(levels[j+1]-e*levels[j]+d*alpha)
    lam,u,v=linear(rows[:3],rhs[:3]);res=sum(a*b for a,b in zip(rows[3],[lam,u,v]))-rhs[3]
    mu=(u*u+v*v).sqrt();w=[B*b+lam+u*sc(q)[1]+v*sc(q)[0] for b,q in zip(levels[:4],qs[:4])]
    H=1/w[0]-(B*r).exp()/w[1]+(B*r-A*s).exp()/w[2]-(B*RHO-A*s).exp()/w[3]
    integ=D(0)
    for j,(c,d) in enumerate(zones):
        mu_cos0=v*sc(qs[j])[1]-u*sc(qs[j])[0];mu_cos1=v*sc(qs[j+1])[1]-u*sc(qs[j+1])[0]
        integ+=((lam-d)*(qs[j+1]-qs[j])+mu_cos0-mu_cos1-(levels[j+1]-levels[j]))/c
    return res,mu,lam,H,integ/PER

def main():
    out={}
    for name,r,s in [('first','2.73100378','.40448498'),('second','2.90517603','.18921685')]:
        sol=newton(lambda z:[critical(*z)[0],critical(*z)[1]-MU],[r,s])
        values=critical(*sol);out[name]={'r':str(sol[0]),'s':str(sol[1]),'mu':str(values[1]),'bias':str(values[2]),'H':str(values[3]),'mean':str(values[4])}
    sym=critical(RHO/2,(PER-RHO)/2);out['symmetric_amplitude']=str(sym[1])
    root_seeds=[['-.5692039544','.706','1.076','3.700','4.229'],['-.5567601961','.944','0.999','3.431','4.234'],['-.5551559903','3.233','4.235']]
    for i,seed in enumerate(root_seeds):
        four=i<2;sol=newton(lambda z:profile(z,four=four,unbiased=True)[0],seed)
        out['root'+str(i+1)]={'initial':str(sol[0]),'mean':str(profile(sol,four=four,unbiased=True)[1])}
    print(json.dumps(out,indent=2),flush=True)
    result=[];vals=[D('-.5790224707'),D(0),D('.63458'),D('1.08317'),PI+D('.63458'),PI+D('1.08317')]
    for k in range(161):
        xi=D(k)/2000;four=k<=77
        if k==78:vals=vals[:2]+vals[-2:]
        vals=newton(lambda z:profile(z,xi,four)[0],vals)
        if four:
            exterior=(vals[3]-vals[2])+(vals[5]-vals[4])
            assert D(0)<vals[2]<vals[3]<PI/2 and PI<vals[4]<vals[5]<3*PI/2
            assert all((B*level+vals[1]+MU*sc(t)[0])*direction>D(0) for t,level,direction in zip(vals[2:],[-1,-1,1,1],[-1,1,1,-1]))
        else:
            exterior=vals[3]-vals[2]
            assert PI<vals[2]<vals[3]<3*PI/2
            assert B+vals[1]+MU*sc(vals[2])[0]>0 and B+vals[1]+MU*sc(vals[3])[0]<0
        # Minimum near the lower tangency phase, obtained from the relevant affine flight.
        t0=D(0) if not four else vals[2];x0=vals[0] if not four else D(-1);c,d=(-B,D(0)) if not four else (A,A+B)
        tm=newton(lambda z:[-c*flow(t0,z[0],x0,c,d,vals[1])-d+vals[1]+MU*sc(z[0])[0]],['.973'])
        minimum=flow(t0,tm[0],x0,c,d,vals[1])
        if four:assert vals[2]<tm[0]<vals[3] and minimum<-1
        else:assert 0<tm[0]<PI/2 and minimum>-1
        result.append([f'{xi:.6f}',f'{D(0) if k==0 else 100000*vals[1]:.10f}',f'{PER-exterior-RHO:.10f}',f'{minimum:.10f}'])
        if k%20==0:print('sample',k,result[-1],flush=True)
    outpath=Path(__file__).resolve().parents[1]/'paper/figures/response_data.csv'
    with outpath.open('w') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['xi','scaled_lambda','T_minus_rho','minimum']);w.writerows(result)

if __name__=='__main__':main()
