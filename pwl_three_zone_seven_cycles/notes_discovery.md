# How the seven-cycle candidate was discovered: reconstruction and mathematical mechanism

**Date:** 2026-10-10. **System:** `x'=-A x+(A+B)sat(x)+mu sin t`, A,B,mu>0.
**Main claim supported by computations:** At `(A,B,mu)=(9,3/2,181363/100000)`, six directed-rounding displacement sign tests yield **at least seven geometrically distinct isolated periodic solutions**, provided the certificate implementation and its first-hit argument are correct. This is a lower bound, *not* a sharp global upper bound.

## Discovery reconstruction

1. The QTDS manuscript proved `Lambda_xi * J = (A+B)(rho-T)`, `rho=2*pi*A/(A+B)`, `J>0`, and `Lambda(0)=0`. The five-cycle conjecture would follow from sufficient shape hypotheses such as connectedness of `{xi>0:T(xi)>rho}`.
2. Differentiating four crossing times at a critical periodic orbit gave `T_xi=z1*H`, with explicit H in terms of four crossing velocities and two free flight lengths `r,s`. The Cramer reduction (QTDS Sec. 3) gave the critical compatibility equation `F(A,B,r,s)=0`.
3. Initial parameter scans `A,B<=6` failed to reveal a physical negative H; expanded scans for strong exterior damping (`A≈8–10`, `B≈1.5–2`) found genuine negative H at F=0. A simple rational-coefficient choice was `A=9,B=1.5`.
4. Following the critical amplitudes along F=0 showed a dip from approximately `mu_c=1.81363456294668` at the symmetric critical orbit toward `~1.813584` and then a rise. The chosen rational amplitude `mu=1.81363` is below the symmetric threshold but above this minimum, permitting two distinct genuine three-zone critical points at fixed amplitude.
5. Continuation of the response curve at this mu located two three-zone critical points and the known one two-zone critical point. Three nonzero positive response zeros followed, and the odd symmetry produced three negative partners plus the symmetric center.
6. Because the first excursion is very close to the grazing boundary, numerical root-finding alone was not accepted. Six rational initial values in three disjoint intervals were certified by piecewise exact flows and directed-rounding interval signs of the Poincare displacement. A separate SciPy DOP853 integration agrees.

## Exact formulas

`g(x)=A*x-(A+B)*sat(x)`. For a constant-slope zone `g(x)=c*x+d`, the exact flow from `x(t0)=x0` is

```
x(t)=exp(-c(t-t0))*x0-d*(1-exp(-c(t-t0)))/c
     +mu/(1+c*c)*[c*sin(t)-cos(t)-exp(-c(t-t0))*(c*sin(t0)-cos(t0))].
```

The return map is `P(y)=x(2*pi;0,y)`; roots of `D(y)=P(y)-y` are periodic solutions. The symmetry `Sx(t)=-x(t+pi)` preserves the equation. The unique symmetric periodic solution is the zero of `Q(y)=x(pi;0,y)+y`.

At a critical arc `T=r+u=rho`, four crossing velocities `v_i` give

```
T_xi = z1 * H,
H=1/v1-exp(B*r)/v2+exp(B*r-A*s)/v3-exp(B*r+B*u-A*s)/v4.
```

In particular, negative H on a physical critical orbit refutes the overly strong monotonicity hypothesis used in the attempted upper-five proof.

## Response curve at A=9, B=3/2, mu=1.81363

`rho=12*pi/7 ≈ 5.385587406153931`.

| xi at Lambda_xi=0 | Lambda(xi) | Itinerary | T passes through rho |
|---:|---:|---|---|
| 0.00427530 | -5.83439e-7 | genuine three-zone | from above to below |
| 0.02615002 | +1.20237e-5 | genuine three-zone | from below to above |
| 0.04964750 | -2.30103e-5 | right two-zone | from above to below |

These are *high-resolution numerical estimates*, not interval-certified turning-point enclosures. The resulting response has three positive zeros:

| Initial x(0) | mean xi | crossings | P'(y) |
|---:|---:|---|---:|
| -0.569203954368034 | 0.007659607 | four (`-1,-1,+1,+1`) | 0.9914612791 |
| -0.556760196081272 | 0.037207634 | four (`-1,-1,+1,+1`) | 1.5169801260 |
| -0.555155990304937 | 0.065677290 | two (`+1,+1`) | 0.3330479441 |

The three signs of return multipliers are stable, unstable, stable. The center initial value is about `-0.579022470712` with numerical multiplier about `1.004398616` (slightly unstable).

## The certificate: three disjoint sign changes

`D(-0.571)>0`, `D(-0.567)<0`;
`D(-0.55677)<0`, `D(-0.55675)>0`;
`D(-0.55517)>0`, `D(-0.55514)<0`.

The positive and negative directed-rounding intervals in `rational_decimal_seven_certificate.py` are disjoint from zero by at least `4.96e-6` (allowing the sign-inclusion intervals). That script ran successfully again on 2026-10-10, along with the independent DOP853 program. In particular `Q(-0.571)>0.01911577081336` puts the unique symmetric center below all three intervals. The autonomous-in-phase? NO: distinct Poincare-section initial values correspond to distinct closed curves on the phase cylinder, not time-shifts of one geometric cycle.

For isolatedness, the three witness intervals are interior to fixed first-hit itineraries. The endpoint checks and scalar order preservation keep the entire intervals away from grazing; their return-displacement functions are real-analytic and not identically zero, so their intermediate-value zeros are isolated. The event validity can be audited via the monotonic intervals of `q(t)=exp(c(t-t0))*x'(t)`, since `q'(t)=mu*exp(c(t-t0))*cos(t)` in each zone.

## Why this is subtle, and what it does not prove

The middle-zone slope `+B` is destabilizing, but the exterior slope `-A` is strongly contracting. At `A=9,B=1.5`, the center sits near `P'(y)=1`, and a grazing transition splits the trajectory itineraries, causing two genuine three-zone extrema plus the conventional two-zone extremum. The critical-amplitude window is narrow, and the first response extremum is only `~6e-7` in amplitude. Coarse time-stepping can produce phantom near-center zeros; e.g., a preliminary `mu=1.813634` grid suggested extra near-center roots, but independent higher-accuracy IVP integration did not confirm them.

The sign-certificate code is not a formally verified proof kernel; its use in a paper requires a second, independent audit of outward rounding, Taylor remainders, and first-hit inequalities (ideally an Arb/FLINT or exact rational implementation). Nothing here proves the maximum is 7, or excludes 9 or more for some other parameters.

## Reproducible files

- `rational_decimal_seven_certificate.py`: directed-rounding sign witness.
- `independent_seven_cycle_audit.py`: independent direct DOP853 shooting.
- `high_precision_periodic_roots.py`: 70-digit analytic-piece root refinement and Floquet multipliers.
- `critical_chart_scan.py`, `critical_H_model.py`: candidate discovery via F/H.
- `plot_seven_mechanism.py`: numerical response and residence plots.
- `QTDS_LaTeX_Source(1).pdf`: source identities in sections 2–3 and 8–10.
- Bravo–Carmona–Fernández–Ojeda, arXiv:2507.06705 (2025): maximum five is a conjecture, not an established universal theorem.