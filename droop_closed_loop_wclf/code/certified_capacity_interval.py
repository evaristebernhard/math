"""Quadratic sufficient safety certificate for *fixed gain* load hosting.

Mathematical guarantee requires externally verified uniform Hessian bounds
over the entire load domain and full disturbance set. Python float results
are demonstrations, not formal directed-rounding certificates.

Run: python3 code/certified_capacity_interval.py
"""
from math import sqrt


def support(a, b, c):
    if c < 0:
        raise ValueError("nonnegative half-disc radius required")
    return c * sqrt(a*a+b*b) if a >= 0 else c * abs(b)


def quadratic_safe_interval(constant, slope, curvature, lo, hi):
    """Intersection of [lo,hi] with {s: c+a*s+M*s^2/2 <= 0}."""
    if curvature < 0 or lo > hi:
        raise ValueError("curvature must be nonnegative and lo<=hi")
    if curvature == 0:
        if slope == 0:
            return (lo, hi) if constant <= 0 else None
        cutoff = -constant / slope
        if slope > 0:
            hi = min(hi, cutoff)
        else:
            lo = max(lo, cutoff)
        return (lo, hi) if lo <= hi else None
    discriminant = slope*slope-2*curvature*constant
    if discriminant < 0:
        return None
    root = sqrt(discriminant)
    low = max(lo, (-slope-root)/curvature)
    high = min(hi, (-slope+root)/curvature)
    return (low, high) if low <= high else None


def certified_hosting_interval(lambda0, domain, constraints):
    """Intersect explicit Taylor/Hessian sufficient conditions.

    Each constraint (a violation <= 0) is a dictionary with:
      value0, d_lambda, grad_w_blocks=[(a,b),...], radii=[C_j,...], M.
    The Hessian M is with respect to joint (lambda,w) variables.
    lambda0 and domain are in the same normalized units.
    """
    lower, upper = domain
    if lower > upper:
        raise ValueError("Invalid domain")
    for item in constraints:
        M, radii = item["M"], item["radii"]
        if M < 0 or len(radii) != len(item["grad_w_blocks"]):
            raise ValueError("Invalid uniform Hessian bound or blocks")
        constant = item["value0"] + sum(
            support(a, b, c) for (a, b), c in zip(item["grad_w_blocks"], radii)
        ) + 0.5*M*sum(c*c for c in radii)
        interval = quadratic_safe_interval(
            constant, item["d_lambda"], M, lower-lambda0, upper-lambda0
        )
        if interval is None:
            return None
        lower = max(lower, lambda0+interval[0])
        upper = min(upper, lambda0+interval[1])
        if lower > upper:
            return None
    return lower, upper


def toy_exact_worst_current_sq(lam, pv=0.30, radius=0.05):
    """Fixed sending voltage, lossless: p=lam-pv-wp, q=wq."""
    a = lam-pv
    return (a-radius)**2 if a < 0 else a*a+radius*radius


def demo():
    pv, radius, current_max = 0.30, 0.05, 0.20
    # phi=(lambda-pv-wp)^2+wq^2-Imax^2, Hessian spectral norm = 4.
    constraint = {
        "value0": -current_max**2,
        "d_lambda": 0.,
        "grad_w_blocks": [(0., 0.)],
        "radii": [radius],
        "M": 4.0,
    }
    safe = certified_hosting_interval(pv, (0, 0.70), [constraint])
    exact = (pv+radius-current_max,
             pv+sqrt(current_max**2-radius**2))
    assert safe is not None
    assert exact[0] <= safe[0] and safe[1] <= exact[1]
    assert toy_exact_worst_current_sq(0, pv, radius) > current_max**2
    for k in range(301):
        lam = safe[0] + (safe[1]-safe[0])*k/300
        assert toy_exact_worst_current_sq(lam,pv,radius) <= current_max**2+1e-12
    print("Quadratic inner safe interval:", safe)
    print("Exact robust toy safe interval:", exact)
    print("All sampled cross-checks passed (sampling is not the proof).")


if __name__ == "__main__":
    demo()
