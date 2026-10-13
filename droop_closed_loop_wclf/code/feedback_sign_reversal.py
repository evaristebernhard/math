"""Analytic two-line feeder counterexample (no dependencies)."""
r1,x1 = 0.01,0.08
r2,x2 = 0.08,0.02
gain = 8.0
critical = r1/(x1*r2-r1*x2)
closed_loop_sensitivity = (
    r1 + gain*(r1*x2-x1*r2)
)/(1+gain*(x1+x2))

if __name__ == "__main__":
    print(f"critical gain: {critical:.9f}")
    print(f"dV1/dp2 at gain {gain:g}: {closed_loop_sensitivity:.9f}")
    assert abs(critical-1.6129032258064515)<1e-12
    assert abs(closed_loop_sensitivity-(-0.022))<1e-12
