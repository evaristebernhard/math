"""Reproducible explanatory plots; numerical, not interval certified."""
import os,sys
sys.path.insert(0,os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from residence_experiment import central,shoot,residence
A,B,mu,N=9.,1.5,1.81363,16384
rho=2*np.pi*A/(A+B)
yc=central(A,B,mu,N)
xx=np.linspace(0,.08,161)
Lam=[];Diff=[];mins=[]
prev=yc;lam=0.
for xi in xx:
    prev,lam,u,ok=shoot(float(xi),prev,lam,A,B,mu,N)
    if not ok: raise RuntimeError('failed shooting')
    Lam.append(lam);Diff.append(residence(u)-rho);mins.append(float(u.min()))
crit=[.0042753017,.0261500219,.0496475006]
roots=[.007659607,.037207634,.065677289]
fig,ax=plt.subplots(figsize=(9,4.1))
ax.plot(xx,1e5*np.array(Lam),lw=1.7)
ax.axhline(0,lw=.9,ls='--')
for q in crit:ax.axvline(q,ls=':',lw=.8,alpha=.65)
ax.scatter(roots,np.zeros(3),marker='x',s=65,zorder=5)
ax.set(xlabel='Mean xi', ylabel='Response 1e5 * Lambda(xi)',title='Three positive zeros: A=9, B=1.5, mu=1.81363')
ax.grid(alpha=.25)
fig.tight_layout();fig.savefig('/mnt/data/seven_response_mechanism.png',dpi=165);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.1))
ax.plot(xx,Diff,lw=1.7)
ax.axhline(0,lw=.9,ls='--')
for q in crit:ax.axvline(q,ls=':',lw=.8,alpha=.65)
ax.set(xlabel='Mean xi', ylabel='T(xi)-rho',title='Residence time changes sign three times')
ax.grid(alpha=.25)
fig.tight_layout();fig.savefig('/mnt/data/seven_residence_mechanism.png',dpi=165);plt.close(fig)
print('saved plots',[(p,os.path.getsize(p)) for p in ['/mnt/data/seven_response_mechanism.png','/mnt/data/seven_residence_mechanism.png']])