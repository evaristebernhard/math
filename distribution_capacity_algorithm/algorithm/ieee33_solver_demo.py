"""IEEE 33-bus nonlinear physical-clipping power-flow curve reproduction.

Uses the case33bw exact-decimal feeder data already committed in the sibling
'droop_closed_loop_wclf/code/exact_design_upper.py'. Requires numpy and scipy.
This script reproduces Figure 'voltage' for ONE SPECIFIED feasible disturbance.
It does not search over the full PV uncertainty set.
Run at repo root: python3 distribution_capacity_algorithm/algorithm/ieee33_solver_demo.py
"""
from pathlib import Path
import csv
import sys
import numpy as np
from scipy.optimize import root

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
sys.path.insert(0,str(ROOT / "droop_closed_loop_wclf" / "code"))
import exact_design_upper as dat

N = 32
PV = np.array([7,16,22,31],dtype=int)
D = np.array(dat.D,dtype=float)
r = np.array([float(x) for x in dat.r])
x = np.array([float(x) for x in dat.x])
R = D.T @ np.diag(r) @ D
X = D.T @ np.diag(x) @ D
M = D.T @ np.diag(r) @ (np.eye(N)-2*D) @ np.diag(r) + D.T @ np.diag(x) @ (np.eye(N)-2*D) @ np.diag(x)
Hr = (D-np.eye(N)) @ np.diag(r)
Hx = (D-np.eye(N)) @ np.diag(x)
P0 = -np.array([float(t) for t in dat.base_p])
Q0 = -np.array([float(t) for t in dat.base_q])
P0[PV] += .025
QV = np.sqrt(.1*.1-.025*.025)

LOADS = [0,.2,.4,.6,.8,1,1.05,1.1,1.15,1.187]
CONTROLS = {
    "uniform": (1.92,1.92,1.92,1.92),
    "coordinated": (3.80105,1.89598,2.39520,4.0),
}
EXPECTED_AT_110 = {"uniform":.94970338,"coordinated":.95312898}


def solve(load_mw,gains):
    gain = np.zeros(N)
    gain[PV] = gains
    p = P0.copy()
    p[16] -= load_mw/10.
    qbase = Q0.copy()
    wq = np.full(len(PV),-.0125)

    def state(z):
        nu,ell=z[:N],z[N:]
        if np.any(nu<=0):
            raise ValueError("Nonpositive squared voltage")
        volts = np.sqrt(nu)
        raw=wq-gain[PV]*(volts[PV]-1)
        actual=np.clip(raw,-QV,QV)
        q=qbase.copy();q[PV]+=actual
        active=np.zeros(N); active[PV]=gain[PV]*((raw>-QV)&(raw<QV))
        a=D@p-Hr@ell
        b=D@q-Hx@ell
        return nu,ell,volts,a,b,raw,active,q

    def fun(z):
        try: nu,ell,v,a,b,raw,active,q=state(z)
        except ValueError: return np.ones(N*2)*1e3
        return np.r_[nu-1-2*R@p-2*X@q-M@ell,
                     ell-(a*a+b*b)/nu]

    def jac(z):
        try: nu,ell,v,a,b,raw,active,q=state(z)
        except ValueError: return np.eye(N*2)
        t=active/v
        j11=np.eye(N)+X@np.diag(t)
        j12=-M
        j21=np.diag((a*a+b*b)/nu**2)+np.diag(b/nu)@D@np.diag(t)
        j22=np.eye(N)+2*np.diag(a/nu)@Hr+2*np.diag(b/nu)@Hx
        return np.block([[j11,j12],[j21,j22]])

    guess=np.r_[np.ones(N)*.96,np.ones(N)*.03]
    result=root(fun,guess,jac=jac,tol=1e-11)
    residual=float(np.max(np.abs(fun(result.x))))
    if residual>1e-9 or min(result.x[:N])<=0:raise RuntimeError(f"power flow failure: {result.message}, residual {residual}")
    nu,ell,v,a,b,raw,active,q=state(result.x)
    return dict(v18=float(v[16]),vmin=float(np.min(v)),
                imax=float(np.max(np.sqrt(np.maximum(ell,0)))),
                residual=residual,
                saturated=int(np.sum(active[PV]==0)))


def run():
    rows=[]
    for lam in LOADS:
        u=solve(lam,CONTROLS["uniform"])
        c=solve(lam,CONTROLS["coordinated"])
        rows.append([lam,u["v18"],c["v18"],u["imax"],c["imax"]])
    ix=LOADS.index(1.1)
    assert abs(rows[ix][1]-EXPECTED_AT_110["uniform"])<2e-7
    assert abs(rows[ix][2]-EXPECTED_AT_110["coordinated"])<2e-7
    target=ROOT/"distribution_capacity_algorithm"/"results"/"ieee33_fixed_disturbance_voltage.csv"
    target.parent.mkdir(exist_ok=True,parents=True)
    with target.open("w",newline="",encoding="utf-8") as file:
        writer=csv.writer(file)
        writer.writerow(["load_mw","v18_uniform_pu","v18_coordinated_pu","imax_uniform_pu","imax_coordinated_pu"])
        writer.writerows(rows)
    print(f"Verified solver curve and wrote {target}")
    print("At 1.10 MW: V18 uniform",round(rows[ix][1],8),"coordinated",round(rows[ix][2],8))


if __name__=="__main__":
    run()
