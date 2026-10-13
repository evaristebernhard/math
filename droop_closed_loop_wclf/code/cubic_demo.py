"""Reproduce the cubic gap of the analytical theorem on a nonzero-baseline model.

Only math stdlib; a dense boundary grid approximates the test maximum.
This is not an IEEE-33-bus DistFlow experiment or a computer proof.
"""
from math import cos, sin, hypot, pi, sqrt
from half_disc_support import candidate_and_lambda

G = (1.0, 2.0)
H = ((0.8, 0.2), (0.2, -0.2))
C = 1.0
HESSIAN_FROBENIUS = sqrt(sum(h*h for row in H for h in row))
U_STAR, LAMBDA = candidate_and_lambda(*G, C)
KAPPA = LAMBDA / (2*C)
R_U = C


def f(p, q):
    return 0.5 + G[0]*p + G[1]*q + 0.5*(H[0][0]*p*p
                                          + 2*H[0][1]*p*q
                                          + H[1][1]*q*q)


def boundary_grid_max(epsilon, samples=65536):
    # The gradient's p-coordinate is >0 in these toy cases; thus maxima
    # lie on the arc for these epsilon values. Dense samples are merely a diagnostic.
    best = -1e300
    for k in range(samples+1):
        theta = -pi/2 + pi*k/samples
        best = max(best, f(epsilon*C*cos(theta), epsilon*C*sin(theta)))
    return best


def run():
    assert KAPPA > 0
    print("Cubic gap demo: nonzero nominal f(0)=0.5")
    print("epsilon   observed grid gap   rigorous real-arithmetic cubic allowance   gap/eps^3")
    for eps in (0.30, 0.15, 0.075, 0.0375):
        candidate = f(eps*U_STAR[0], eps*U_STAR[1])
        observed_gap = max(0.0, boundary_grid_max(eps) - candidate)
        cubic_allowance = (HESSIAN_FROBENIUS**2 * R_U**2 /
                           (4*KAPPA)) * eps**3
        print(f"{eps:7.4f}   {observed_gap:18.11g}   {cubic_allowance:18.11g}   {observed_gap/eps**3:.9g}")
        assert observed_gap <= cubic_allowance + 1e-12


if __name__ == "__main__":
    run()
