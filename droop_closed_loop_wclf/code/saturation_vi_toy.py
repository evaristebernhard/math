"""Exact-rational scalar Volt/VAR saturation & hosting-capacity certificate.

Run: python3 code/saturation_vi_toy.py (from droop_closed_loop_wclf).
Affine-feeder toy, NOT a nonlinear DistFlow or IEEE33 certificate.
Integer square roots rigorously enclose irrational inverter Q caps.
"""
from fractions import Fraction as F
from math import isqrt

V0 = F(995, 1000)
A = F(11, 100)      # voltage sensitivity to incremental demand
A_PV = F(2, 100)    # voltage sensitivity to active PV deviation
B = F(6, 100)      # voltage sensitivity to controlled reactive injection
G = F(45)          # high gain: G*B = 2.7 > 1
P0 = F(15, 100)
S = F(25, 100)
C = F(2, 100)      # right-half-disc radius
V_MIN = F(95, 100)
V_MAX = F(105, 100)
SCALE = 10**12


def sqrt_enclosure(x):
    """Exact rational bounds for sqrt(nonnegative rational x)."""
    if x < 0:
        raise ValueError("negative radicand")
    k = isqrt(x.numerator * SCALE * SCALE // x.denominator)
    lo = F(k, SCALE)
    hi = lo if k*k*x.denominator == x.numerator*SCALE*SCALE else F(k+1, SCALE)
    return lo, hi


def clip(x, cap):
    return min(max(x, -cap), cap)


def clip_image(raw_lo, raw_hi, cap_lo, cap_hi):
    """Interval hull of clip(raw,[-cap,cap]) for rectangle intervals."""
    assert raw_lo <= raw_hi and F(0) <= cap_lo <= cap_hi
    lo = clip(raw_lo, cap_hi if raw_lo < 0 else cap_lo)
    hi = clip(raw_hi, cap_hi if raw_hi > 0 else cap_lo)
    return lo, hi


def solve_scalar(lam, wp, wq):
    """Rigorous interval enclosure for the exact clipped Q equilibrium."""
    assert 0 <= wp <= C and abs(wq) <= C
    cap_lo, cap_hi = sqrt_enclosure(S*S - (P0 + wp)**2)
    v_open = V0 - A*lam + A_PV*wp
    stationary_raw = (wq - G*(v_open-1))/(1+G*B)
    return clip_image(stationary_raw, stationary_raw, cap_lo, cap_hi)


def cell_voltage_enclosure(l0, l1, p0, p1, w0, w1):
    """All points in one closed lambda/wp/wq rectangle; no sampling."""
    assert 0 <= l0 <= l1 and 0 <= p0 <= p1 <= C and -C <= w0 <= w1 <= C
    v_open_lo = V0 - A*l1 + A_PV*p0
    v_open_hi = V0 - A*l0 + A_PV*p1
    u_lo = (w0 - G*(v_open_hi-1))/(1+G*B)
    u_hi = (w1 - G*(v_open_lo-1))/(1+G*B)
    cap_lo = sqrt_enclosure(S*S - (P0+p1)**2)[0]
    cap_hi = sqrt_enclosure(S*S - (P0+p0)**2)[1]
    q_lo, q_hi = clip_image(u_lo, u_hi, cap_lo, cap_hi)
    return v_open_lo + B*q_lo, v_open_hi + B*q_hi


def certify_capacity_prefix(capacity, segments=4):
    """Rational interval validation of the entire robust prefix [0,L]."""
    assert capacity >= 0 and segments >= 1
    lower, upper = F(100), F(-100)
    for il in range(segments):
        l0, l1 = capacity*il/segments, capacity*(il+1)/segments
        for ip in range(segments):
            p0, p1 = C*ip/segments, C*(ip+1)/segments
            for iw in range(segments):
                w0 = -C + 2*C*iw/segments
                w1 = -C + 2*C*(iw+1)/segments
                vlo, vhi = cell_voltage_enclosure(l0,l1,p0,p1,w0,w1)
                lower, upper = min(lower,vlo), max(upper,vhi)
    return lower, upper


def test():
    # Ordinary unrelaxed Picard contraction fails, yet VI contraction works.
    assert G*B > 1
    for lam, wp, wq in [
        (F(0), F(0), F(0)), (F(3,10), C, F(0)),
        (F(1,2), C, F(0)), (F(1,2), F(0), -C),
    ]:
        qlo, qhi = solve_scalar(lam,wp,wq)
        assert qlo <= qhi
        base = V0-A*lam+A_PV*wp
        cap_lo, cap_hi = sqrt_enclosure(S*S-(P0+wp)**2)
        # With tau = 1/(1+G*B), the projected map is independent of q.
        for q in [F(-1,5), F(0), F(1,5)]:
            A_q = (1+G*B)*q + G*(base-1)-wq
            x = q - A_q/(1+G*B)
            assert clip_image(x,x,cap_lo,cap_hi) == (qlo,qhi)

    low, high = certify_capacity_prefix(F(1,2), segments=4)
    assert low >= V_MIN and high <= V_MAX, (float(low),float(high))

    # Feasible half-disc witness: wp=C, wq=0, lambda=0.52.
    witness_lam = F(52,100)
    qlo, qhi = solve_scalar(witness_lam,C,F(0))
    witness_v_upper = V0-A*witness_lam+A_PV*C+B*qhi
    assert witness_v_upper < V_MIN
    cap_hi = sqrt_enclosure(S*S-(P0+C)**2)[1]
    unbounded_q = G*(1-(V0-A*witness_lam+A_PV*C))/(1+G*B)
    assert unbounded_q > cap_hi  # actually Q-saturated

    print("GAIN",G,"G*B",G*B,"(ordinary Picard contraction fails)")
    print("Entire rational-certified prefix [0,0.50] V bounds:",float(low),float(high))
    print("Feasible unsafe witness at 0.52 has upper V:",float(witness_v_upper))
    print("Proved toy bracket: 0.50 <= connected capacity < 0.52")
    print("This is NOT an IEEE-33 nonlinear DistFlow certificate.")


if __name__ == "__main__":
    test()
