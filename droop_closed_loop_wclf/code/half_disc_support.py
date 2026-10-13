"""Exact half-disc support and a certified-angle outer bound for affine phasors.

All returned analytic inequalities are exact-real mathematics. Python float
calculations do NOT carry directed-rounding computer-assisted certification.
"""
from math import cos, sin, hypot, pi, sqrt


def support(a, b, radius):
    """max_{x>=0,x*x+y*y<=radius**2} (a*x+b*y), for radius>=0."""
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    return radius * (hypot(a, b) if a >= 0 else abs(b))


def candidate_and_lambda(a, b, radius):
    """Linear maximizer u*, with lambda for quadratic growth.

    lambda==0 marks a degenerate first-order exposed face. A cubic gap
    theorem cannot be invoked there without additional hypotheses.
    """
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    if radius == 0:
        return (0.0, 0.0), 0.0
    if a >= 0 and hypot(a, b) > 0:
        norm = hypot(a, b)
        return (radius*a/norm, radius*b/norm), norm
    if a < 0 and b != 0:
        return (0.0, radius * (1 if b > 0 else -1)), abs(b)
    return (0.0, 0.0), 0.0


def affine_phasor_norm_angle_bounds(base, matrices, radii, grid_size=4096):
    """Lower/upper bounds for max ||base+sum_j T_j*u_j||_2 over half-discs.

    matrices[j] is a 2x2 map from (active,reactive) to a phasor (Re,Im).
    The upper value includes a global Lipschitz angular interpolation
    term pi/grid_size * (||base|| + sum radius*||T_j||_F).
    Thus the mathematical upper bound is valid without asserting that
    the largest angle-grid sample is the true global maximum.
    """
    if grid_size < 4 or len(matrices) != len(radii):
        raise ValueError("bad grid size or block count")
    lipschitz = hypot(*base)
    for t, c in zip(matrices, radii):
        if c < 0:
            raise ValueError("radius must be nonnegative")
        lipschitz += c * sqrt(sum(v*v for row in t for v in row))
    grid_max = float("-inf")
    for k in range(grid_size):
        angle = (2*pi*k) / grid_size
        sx, sy = cos(angle), sin(angle)
        phi = base[0]*sx + base[1]*sy
        for t, c in zip(matrices, radii):
            # T^T * s
            ap = t[0][0]*sx+t[1][0]*sy
            aq = t[0][1]*sx+t[1][1]*sy
            phi += support(ap, aq, c)
        grid_max = max(grid_max, phi)
    return grid_max, grid_max + pi*lipschitz/grid_size
