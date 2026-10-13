"""Certified endpoint-sign persistence for a small parameter cube.

This is an analytic perturbation bound, NOT a second independent interval
backend. It imports the original exact-flow endpoint checker and uses an
elementary one-sided Gronwall bound to protect its strict signs.

Parameters: f(x,t) = -A*x+(A+B)*sat(x)+mu*sin(t).
For max(|A-9|, |B-3/2|, |mu-1.81363|) < 1e-12,
the difference from each BASE trajectory (same y) is < 1.5e-6 on [0,2*pi].
The six certified displacement margins all exceed that error.
This certifies seven distinct periodic solutions throughout the cube.
Isolation/stability on a (possibly smaller) open neighborhood additionally
use itinerary analyticity and continuity of the central multiplier.
"""
from decimal import Decimal
from fractions import Fraction

from certify_seven import PI, I, check, flow, regions

EPS = Decimal("1e-12")
MAX_DIFFERENCE = Decimal("0.0000015")
ENDPOINTS = (
    ("-0.571", "+"),
    ("-0.567", "-"),
    ("-0.55677", "-"),
    ("-0.55675", "+"),
    ("-0.55517", "+"),
    ("-0.55514", "-"),
)


def certify():
    # e < 11/4, pi < 13/4 imply e^(4*pi) < (11/4)^13 < 600000.
    assert Fraction(11, 4) ** 13 < 600000
    assert PI.r < Decimal(13) / Decimal(4)

    # |x_base(t;y)| <= 2 on [0,2pi] whenever |y| <= 2:
    # the base field is strictly inward at both endpoints.
    # f_base(2,t) <= -15/2+mu < 0, f_base(-2,t) >=15/2-mu >0.
    #
    # The slope of f_theta(.,t) is at most B < 2; hence
    # |x_theta(t;y)-x_base(t;y)| <= 5*EPS*(exp(2*t)-1)/2
    #                             < 5*EPS*600000/2 = MAX_DIFFERENCE.
    assert 5 * EPS * Decimal(600000) / 2 == MAX_DIFFERENCE

    min_margin = None
    for initial, expected in ENDPOINTS:
        d, _, _ = check(initial)
        assert d.sign() == expected, (initial, d, expected)
        margin = d.l if expected == "+" else -d.r
        assert margin > MAX_DIFFERENCE, (initial, margin, MAX_DIFFERENCE)
        min_margin = margin if min_margin is None else min(min_margin, margin)

    # Q_base(-.571) > 0; the same Gronwall bound controls x(pi;y).
    _, events, _ = check("-0.571")
    u_pi = flow(events[1], I.v(-1), PI, *regions["middle"])
    q = u_pi + I.v("-0.571")
    assert q.l > MAX_DIFFERENCE
    print("Endpoint minimum rigorous sign margin:", min_margin)
    print("Uniform perturbation bound:", MAX_DIFFERENCE)
    print("Center separation Q(-0.571) lower bound:", q.l)
    print("CERTIFIED: seven distinct periodic solutions for |dA|,|dB|,|dmu| < 1e-12")
    print("NOTE: isolation and stability are proved only on some open sub-neighborhood.")


if __name__ == "__main__":
    certify()
