"""Exact scalar inverter lag tracking under a moving flexible-load setpoint.

Checks a conditional contraction tracking formula. This is an illustrative
linear feeder, not a certified nonlinear IEEE 33-bus controller.
"""
from math import exp

def run():
    a,b,g,tau=.1,.08,2.,1.
    alpha=(1+g*b)/tau
    S=g*a/(1+g*b)
    E=.02
    v=alpha*E/S
    print(f"alpha={alpha:.8f}, dq*/dlambda={S:.8f}")
    print(f"Sufficient ramp speed for E={E:g}: {v:.8f} pu/s")
    for t in (0,1,2,5,10):
        lam=v*t
        qstar=S*lam
        e=-S*v/alpha*(1-exp(-alpha*t))
        q=qstar+e
        assert abs(e)<=E+1e-12
        # Verify formula against exact constant-ramp ODE solution:
        direct= (g*a*v/alpha)*(t-(1-exp(-alpha*t))/alpha)
        assert abs(q-direct)<1e-12
    print("Scalar exact transient formula agrees with bound.")


if __name__=="__main__":
    run()
