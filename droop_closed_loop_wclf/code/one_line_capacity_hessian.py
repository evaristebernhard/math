"""Two-node nonlinear DistFlow: explicit residual Hessian and load sensitivity.

Uses Python standard library only. Finite differences are numerical checks,
NOT rigorous interval-arithmetic power-flow certification.
"""
from math import sqrt

R, X, G = 0.05, 0.03, 2.0
P0, Q0 = -0.1, -0.04
D, E = 1.0, 0.3


def power(nu, w, lam):
    return (P0-lam*D+w[0], Q0-lam*E+w[1]-G*(sqrt(nu)-1))


def residual(z, w, lam):
    nu, ell = z
    p, q = power(nu, w, lam)
    return (nu-1-2*R*p-2*X*q+(R*R+X*X)*ell,
            ell-(p*p+q*q)/nu)


def jacobians(z, w, lam):
    nu, _ = z
    p, q = power(nu, w, lam)
    t = G/(2*sqrt(nu))
    Fz = ((1+2*X*t, R*R+X*X),
          ((p*p+q*q)/nu**2+2*q*t/nu, 1.0))
    Fw = ((-2*R, -2*X), (-2*p/nu, -2*q/nu))
    Flam = (2*(R*D+X*E), 2*(p*D+q*E)/nu)
    return Fz, Fw, Flam


def second_residual(z, w, lam, u, v):
    """D²F along u,v ordered as (nu,ell,wp,wq,lambda)."""
    nu, _ = z
    p, q = power(nu, w, lam)
    dp_u, dp_v = u[2]-D*u[4], v[2]-D*v[4]
    dq_u = u[3]-E*u[4]-G*u[0]/(2*sqrt(nu))
    dq_v = v[3]-E*v[4]-G*v[0]/(2*sqrt(nu))
    dq_uv = G*u[0]*v[0]/(4*nu**1.5)
    first = -2*X*dq_uv
    second = -(2*dp_u*dp_v+2*dq_u*dq_v+2*q*dq_uv)/nu
    second += 2*((p*dp_u+q*dq_u)*v[0]+
                 (p*dp_v+q*dq_v)*u[0])/nu**2
    second -= 2*(p*p+q*q)*u[0]*v[0]/nu**3
    return first, second


def solve2(a, b):
    det = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    if abs(det) < 1e-12:
        raise ArithmeticError("Near-singular Jacobian")
    return ((a[1][1]*b[0]-a[0][1]*b[1])/det,
            (-a[1][0]*b[0]+a[0][0]*b[1])/det)


def power_flow(w, lam):
    z = [0.98, 0.02]
    for _ in range(30):
        f = residual(z, w, lam)
        J, _, _ = jacobians(z, w, lam)
        step = solve2(J, f)
        z = [z[0]-step[0], z[1]-step[1]]
        if z[0] <= 0:
            raise ArithmeticError("Off positive-voltage branch")
        if max(map(abs, step)) < 1e-14:
            break
    assert max(map(abs, residual(z, w, lam))) < 1e-11
    return tuple(z)


def sensitivity_and_current_hessian(w, lam):
    z = power_flow(w, lam)
    J, W, Flam = jacobians(z, w, lam)
    derivatives = [solve2(J, (-W[0][k], -W[1][k]))
                   for k in range(2)]
    capacity_derivative = solve2(J, (-Flam[0], -Flam[1]))
    hessian = []
    for k in range(2):
        row = []
        for j in range(2):
            uk = (derivatives[k][0], derivatives[k][1],
                  float(k == 0), float(k == 1), 0.0)
            vj = (derivatives[j][0], derivatives[j][1],
                  float(j == 0), float(j == 1), 0.0)
            f2 = second_residual(z, w, lam, uk, vj)
            row.append(solve2(J, (-f2[0], -f2[1]))[1])
        hessian.append(tuple(row))
    return z, capacity_derivative, tuple(hessian)


def check():
    w, lam, eps = (0.02, -0.01), 0.05, 1e-4
    _, dlam, H = sensitivity_and_current_hessian(w, lam)
    cap_fd = [(power_flow(w, lam+eps)[i]-
               power_flow(w, lam-eps)[i])/(2*eps) for i in range(2)]
    assert max(abs(a-b) for a, b in zip(cap_fd, dlam)) < 1e-6

    def ell(u): return power_flow(u, lam)[1]
    for i in range(2):
        for j in range(2):
            def shifted(s, t):
                v = list(w)
                v[i] += eps*s
                v[j] += eps*t
                return ell(v)
            fd = (shifted(1, 1)-shifted(1, -1)-
                  shifted(-1, 1)+shifted(-1, -1))/(4*eps**2)
            assert abs(fd-H[i][j]) < 5e-6, (fd, H[i][j])
    assert abs(H[0][1]-H[1][0]) < 1e-10
    print("d(nu,ell)/d(lambda):", dlam)
    print("Hessian of ell wrt (wp,wq):", H)
    print("Numerical derivative checks passed.")


if __name__ == "__main__":
    check()
