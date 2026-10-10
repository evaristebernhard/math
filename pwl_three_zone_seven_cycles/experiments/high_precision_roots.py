"""High precision *noncertifying* root approximations from analytic segments.
Works independently of ODE shooting (no scipy integration).
"""
import mpmath as m
m.mp.dps=70
A=m.mpf(9);B=m.mpf('1.5');MU=m.mpf('1.81363')
T=2*m.pi

def flow(t0,y0,t,c,d):
    h=t-t0;e=m.exp(-c*h)
    return e*y0-d*(1-e)/c + MU/(1+c*c)*(c*m.sin(t)-m.cos(t)-e*(c*m.sin(t0)-m.cos(t0)))

def period(y,four):
    # initial guesses for event times are only used for Newton iteration;
    # all exact analytic pieces are independently calculated here.
    guess=[m.mpf('0.72'),m.mpf('1.07'),m.mpf('3.70'),m.mpf('4.23')] if four else [m.mpf('3.23'),m.mpf('4.235')]
    levels=[-1,-1,1,1] if four else [1,1]
    cds=[(-B,0),(A,A+B),(-B,0),(A,-A-B),(-B,0)] if four else [(-B,0),(A,-A-B),(-B,0)]
    ti=m.mpf(0);yi=y;events=[]
    for j,level in enumerate(levels):
        c,d=cds[j]
        t=m.findroot(lambda xx:flow(ti,yi,xx,c,d)-level,(guess[j]-m.mpf('0.002'),guess[j]+m.mpf('0.002')))
        assert ti<t<T and abs(flow(ti,yi,t,c,d)-level)<m.mpf('1e-55')
        events.append(t);ti=t;yi=m.mpf(level)
    c,d=cds[-1]
    ending=flow(ti,yi,T,c,d)
    return ending-y,events

for a,b,four in [('-0.571','-0.567',True),('-0.55677','-0.55675',True),('-0.55517','-0.55514',False)]:
    root=m.findroot(lambda y:period(y,four)[0], (m.mpf(a),m.mpf(b)), tol=m.mpf('1e-55'),maxsteps=50)
    residual,ts=period(root,four)
    z=[m.mpf(0)]+ts+[T]
    if four:
        tm=(z[1]-z[0])+(z[3]-z[2])+(z[5]-z[4])
    else:
        tm=(z[1]-z[0])+(z[3]-z[2])
    mult=m.exp((A+B)*tm-A*T)
    print('ROOT',m.nstr(root,35),'P-y',m.nstr(residual,5),'T_middle',m.nstr(tm,27),'multiplier',m.nstr(mult,27))
    print('events',*[m.nstr(t,22) for t in ts])