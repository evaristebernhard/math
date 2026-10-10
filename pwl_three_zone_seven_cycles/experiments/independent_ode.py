"""Independent IVP integration check, not based on interval witness flight code."""
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import numpy as np
A=9.; B=1.5; mu=1.81363
P=2*np.pi

def eval_f(t,x):
    g=np.where(x<-1,9*x+10.5,np.where(x>1,9*x-10.5,-1.5*x))
    return mu*np.sin(t)-g

def integrate(y, ending=P, tol=3e-13):
    def rhs(t,v):
        x,m=v
        gc=9 if abs(x)>1 else -1.5
        return [eval_f(t,x),-gc*m]
    sol=solve_ivp(rhs,(0,ending),[y,1.],rtol=tol,atol=tol*0.02,max_step=.003,method='DOP853',dense_output=True)
    assert sol.success
    t=np.linspace(0,ending,10001)
    xx=sol.sol(t)[0]
    lower=np.flatnonzero(np.diff(np.sign(xx+1)))
    upper=np.flatnonzero(np.diff(np.sign(xx-1)))
    return sol.y[0,-1]-y,sol.y[1,-1],t[lower],t[upper],(t,xx),sol.y[0,-1]

if __name__=='__main__':
    seeds=[-.571,-.567,-.55677,-.55675,-.5552,-.5545]
    for y in seeds:
        d,m,lo,up,*_=integrate(y)
        print('witness',y,'disp',f'{d:+.14e}','mult',f'{m:.10f}','lower',lo,'upper',up)
    for a,b in [(-.571,-.567),(-.55677,-.55675),(-.5552,-.5545)]:
        y=brentq(lambda w:integrate(w)[0],a,b,xtol=1e-14)
        disp,m,lo,up,(ts,xx),end=integrate(y)
        xi=np.trapezoid(xx,ts)/P
        print('ROOT',f'{y:.13f}','disp',f'{disp:+.3e}','xi',f'{xi:.9f}','multiplier',f'{m:.8f}','crossings',lo,up,'range',min(xx),max(xx))
    for y in [-.585,-.58,-.579,-.578,-.571,-.567]:
        d,*_=integrate(y,ending=np.pi)
        print('Q sign',y,d+2*y)