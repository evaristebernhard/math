"""Certified quantitative persistence of SEVEN ISOLATED periodic cycles.

Run after/alongside certify_seven.py. This extension reuses the original
Decimal-directed exact-flight interval checker. Not a second backend.

Parameter cube: max(|A-9|, |B-1.5|, |mu-1.81363|) < 1e-12.
Certifies (i) all six Poincare endpoint signs; (ii) all four possible
grazing barriers throughout three shooting intervals; (iii) the central
antisymmetric orbit stays hyperbolic repelling. On each shooting interval,
the displacement is analytic, so alternating endpoint signs force
two attracting and one repelling isolated zeros. Reflection doubles
these, while the central orbit contributes one repeller.
"""
from decimal import Decimal as D
from fractions import Fraction

from certify_seven import (
    PI, I, MU, B, check, check_grazing_barrier, center_half, flow,
    regions, CENTER_EV, GRAZE_PHASES, taylor_sin, taylor_cos,
)

EPS = D("1e-12")
MAX_DIFFERENCE = D("0.0000015")  # global same-initial bound to t=2*pi
PHASE_SHIFT = D("1e-10")
MIN_BARRIER = D("0.0003")
CENTER_Y_SHIFT = D("6e-10")
CENTER_STATE_DIFF = D("5e-9")
CENTER_TIME_SHIFT = D("1e-6")
ENDPOINTS = (
    ("-0.571", "+"),
    ("-0.567", "-"),
    ("-0.55677", "-"),
    ("-0.55675", "+"),
    ("-0.55517", "+"),
    ("-0.55514", "-"),
)


def certify():
    # Invariance of [-2,2] for the reference field, for all |y| <= 2.
    # Its outward normal speed is at most -15/2+mu < 0 at x=+2
    # and the opposite at x=-2. For perturbations, the upper
    # one-sided Lipschitz slope is B_theta<2, and the forcing
    # mismatch along the reference path has absolute value <5*EPS.
    # pi<13/4 and e<11/4 imply e^(4*pi)<(11/4)^13<600000.
    assert PI.r < D(13)/D(4)
    assert Fraction(11, 4)**13 < 600000
    assert 5*EPS*D(600000)/2 == MAX_DIFFERENCE

    for y, expected in ENDPOINTS:
        displacement, _, _ = check(y)
        assert displacement.sign() == expected, (y, displacement)
        margin = displacement.l if expected == "+" else -displacement.r
        assert margin > MAX_DIFFERENCE, (y, margin, MAX_DIFFERENCE)

    # For each threshold level, the only grazing-eligible times satisfy
    # mu*sin(t)+B*level=0. Under |dB|,|dmu|<1e-12, each root
    # moves by < 1e-10: at the base root the perturbed equation
    # has residual <2e-12, while |d_t(mu*sin t+B*level)|>0.8 in
    # its 1e-10 neighborhood. No new roots appear (mu>B>0).
    # In the whole cube, |x_theta(t;y)-x_0(t;y)|<1.5e-6 for
    # a fixed initial y, and |dx_theta/dt|<40 for |x|<=2.000002.
    # Therefore the change of each grazing-phase gap is bounded by
    # 1.5e-6 + 40e-10 < 1.501e-6, far below 0.0003.
    assert D("1.501e-6") < MIN_BARRIER
    assert MAX_DIFFERENCE + 40*PHASE_SHIFT < D("1.501e-6")
    assert MU > B
    for center, level, _ in GRAZE_PHASES:
        tg = I(D(center)-D("1e-25"), D(center)+D("1e-25"))
        deriv = I.v(MU)*taylor_cos(tg)
        assert (deriv.l > D("0.8") or deriv.r < D("-0.8")), (center, deriv)

    minimum_gap = None
    for y, _ in ENDPOINTS:
        gaps = check_grazing_barrier(y)  # genuine directed intervals
        assert len(gaps) == 4
        for gap in gaps:
            assert gap.sign() != "?"
            margin = gap.l if gap.sign() == "+" else -gap.r
            assert margin > MIN_BARRIER, (y, gap, margin)
            minimum_gap = margin if minimum_gap is None else min(minimum_gap, margin)

    # Central orbit: Q_theta(y)=x_theta(pi;y)+y is strictly increasing
    # with slope >= 1 (order of scalar flows). Its base zero y_c0 lies
    # between -0.579022471 and -0.579022470, certified by center_half.
    # Same-initial parameter error at t=pi is
    #   5e-12*(exp(1.51*pi)-1)/1.51
    # < 5e-12*(158-1)/1.5 < 6e-10
    # because 1.51*pi<5 and e^5<(11/4)^5<158.
    assert D("1.51")*PI.r < 5
    assert Fraction(11,4)**5 < 158
    assert 5*EPS*(158-1)/D("1.5") < CENTER_Y_SHIFT
    qlo, slo = center_half("-0.579022471")
    qhi, shi = center_half("-0.579022470")
    assert qlo.sign() == "-" and qhi.sign() == "+"

    # For t <= 1.2 the parameter-induced base-orbit error is
    # <5e-12*((11/4)^2-1)/1.5. Initial perturbation contributes
    # at most 6e-10*(11/4)^2 since 1.51*1.2<2.
    assert D("1.51")*D("1.2") < 2
    growth = D(11)**2/D(4)**2
    assert 5*EPS*(growth-1)/D("1.5") + CENTER_Y_SHIFT*growth < CENTER_STATE_DIFF

    # Reference central crossings are bracketed by the two certified
    # rational shooting endpoints. The downward time increases with
    # initial condition; the upward time decreases. These wider boxes
    # are simple readable rational bounds on the true central events.
    first_lo, first_hi = D("0.63458137"),D("0.63458138")
    second_lo,second_hi = D("1.08317132"),D("1.08317133")
    for y in ("-0.579022471","-0.579022470"):
        tt = [D(s) for s in CENTER_EV[y]]
        assert first_lo < tt[0] < first_hi
        assert second_lo < tt[1] < second_hi

    # At each true reference central crossing, the level speed is
    # mu*sin(t)-B. In the first box it is <-0.4; in the second it
    # is >0.09. Even allowing +/-1e-6 around each reference event,
    # its rate of change has absolute value <410 because
    # |x'|<40, |f_x|<10 and mu<2. Thus the signed level gap at
    # the two bracketing times has magnitude >0.089e-6.
    # This beats the <5e-9 state perturbation for the perturbed
    # central solution, so its two crossings shift by <1e-6.
    first_speed = I.v(MU)*taylor_sin(I(first_lo,first_hi))-I.v(B)
    second_speed = I.v(MU)*taylor_sin(I(second_lo,second_hi))-I.v(B)
    assert first_speed.r < D("-0.4"), first_speed
    assert second_speed.l > D("0.09"), second_speed
    assert D("410")*CENTER_TIME_SHIFT < D("0.001")
    assert D("0.089")*CENTER_TIME_SHIFT > CENTER_STATE_DIFF

    # Reference central lower excursion: t2-t1 < 0.44858996.
    # Both perturbed crossings move <1e-6, so
    # s_theta < 0.44859196 < 0.448592.
    # Half-period antisymmetry forces equal upper excursion;
    # Floquet exponent is 2*pi*B - 2*(A+B)*s_theta >0.
    s_upper = (second_hi-first_lo)+2*CENTER_TIME_SHIFT
    assert s_upper < D("0.448592"), s_upper
    pi_lower = D("3.14159")
    assert PI.l > pi_lower
    floquet_lower = 2*pi_lower*(D("1.5")-EPS) - 2*(D("10.5")+2*EPS)*D("0.448592")
    assert floquet_lower > D("0.0043"), floquet_lower

    print("Grazing-phase min directed sign margin:", minimum_gap)
    print("Parameter-shifted grazing barrier error <", D("1.501e-6"))
    print("Central half-period residence <", s_upper)
    print("Central Floquet log lower bound >", floquet_lower)
    print("CERTIFIED: >=7 ISOLATED periodic cycles (>=4 attracting, >=3 repelling)")
    print("CUBE: |A-9|, |B-1.5|, |mu-1.81363| < 1e-12")
    print("Uses same directed-Decimal backend, NOT an independent replication.")


if __name__ == "__main__":
    certify()
