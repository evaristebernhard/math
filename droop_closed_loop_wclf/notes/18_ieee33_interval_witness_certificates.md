# Interval-certified physical unsafe witnesses on IEEE-33

Research record, 2026-10-13. This strengthens the **upper** side of the hosting-capacity brackets in notes 15 and 17. It leaves the original block-Hessian **lower** side unchanged, and does not replace the capacity research program.

## 1. Explicitly fixed physical benchmark and logic

Use the same MATPOWER case33bw 32 in-service radial branches and the manually transcribed decimal impedances and loads, with a 12.66 kV / 10 MVA base, original loads multiplied by exactly 0.65, nominal PV P = 0.025 pu on buses 9/18/24/33, S=0.1 pu for each inverter, and extra unity-PF demand at bus 18. The common 0.31 pu current limit is a **research assumption**; the voltage lower bound is 0.95 pu. An exact feasible PV disturbance is
\[
w_{p,j}=0,\qquad w_{q,j}=-0.0125\ {\rm pu}
\quad(j=9,18,24,33),
\]
which lies on the PV right-half-disc boundary in each component.

The physical PV control has active-power-dependent reactive limit:
\[
Q_j=\operatorname{clip}\bigl(w_{q,j}-g(V_j-1),
-\sqrt{0.1^2-0.025^2},+\sqrt{0.1^2-0.025^2}\bigr).
\]
The following are *exact decimal-model* fixed load and gain inputs, not rounded output capacity roots:

- Case A: \(g=1.92,\ \lambda=1.09322\) MW. All four PV outputs verified **strictly inside** their Q limits in the candidate state box.
- Case B: \(g=2.6,\ \lambda=1.22273\) MW. Bus-18 PV Q is verified **strictly clipped at its positive upper limit** throughout the candidate state box, and the other PV outputs are strictly unsaturated.

Thus each case has a fixed smooth mode-residual \(F(z)=0\) consistent with the **actual physical clipped law** on its box, even for case B.

## 2. Certified local existence (not just a small float residual)

Let \(z=(\nu,\ell)\in\mathbb R^{64}\), and choose a floating-point center \(\widehat z\) from the conventional DistFlow solver, then freeze its decimal representation as an exact rational center. Define the closed axis-aligned box
\[
B_\infty=\{z:\|z-\widehat z\|_\infty\le 10^{-6}\}.
\]
Construct a fixed numerical approximate inverse \(P\) of the center Jacobian (again frozen as exact decimal rational entries). The map
\[
T(z)=z-PF(z)
\]
has the *verified interval* derivative bound
\[
\sup_{z\in B_\infty}\|T'(z)\|_\infty
\le \|I-PJ_0\|_\infty+
\|P\|_\infty\,\sup_{z\in B_\infty}\|J(z)-J_0\|_\infty
=:\rho.
\]

All scalar interval computations are carried out with mpmath.iv at 60 decimal digits; after interval evaluation, exact dyadic endpoint rational numbers are read from each interval and the induced norm upper bounds are compared as exact Python Fractions. This avoids an unverified floating-point maximum in the final Banach inequalities. It is sufficient to prove
\[
\rho<1,\qquad \|PF(\widehat z)\|_\infty+\rho 10^{-6}<10^{-6}.
\]
The map sends the complete box strictly into itself and is a contraction; Banach then gives a **unique solution within that box**. Independently verify the box stays in the positive squared-voltage domain, that the chosen inverter clipping/unsaturated modes are consistent for *every point in the box*, and that \(\sqrt{\nu_{18}}<0.95\) throughout the entire box.

## 3. Output of the outward-enclosing interval tests

| Quantity | Case A: g=1.92, 1.09322 MW | Case B: g=2.6, 1.22273 MW |
|---|---:|---:|
| \(\|P\|_\infty\), interval upper | 2.068382583 | 2.166944627 |
| \(\sup\|J(z)-J_0\|_\infty\), interval upper | 5.651889e-5 | 5.816905e-5 |
| \(\|I-PJ_0\|_\infty\), interval upper | 9.86e-60 | 9.99e-60 |
| \(\rho\), interval upper | 1.169027e-4 | 1.260491e-4 |
| \(\|PF(\widehat z)\|_\infty\), interval upper | 1.123e-16 | 1.746e-15 |
| \(V_{18}\) verified interval | [0.949961367,0.949962420] | [0.949926414,0.949927468] |
| PV switching modes verified | all unsaturated | bus 18 positive clipped |
| Voltage safety \(V_{18}\ge0.95\) | **violated** | **violated** |

Displayed decimals are rounded *for reporting only*; code comparisons use exact upper/lower endpoints after interval evaluation. The proof is for the explicitly transcribed benchmark, not all physical feeder parameter uncertainty. It also proves only existence/uniqueness inside the selected normal-operation box, not global uniqueness of all AC power-flow roots.

Therefore, for **connected steady hosting capacity from zero** in the designated physical clipped-control normal branch, each fixed load is an upper obstruction:
\[
\Lambda_{\mathrm{conn}}(1.92) \le 1.09322\ \mathrm{MW},\qquad
\Lambda_{\mathrm{conn}}(2.6) \le 1.22273\ \mathrm{MW},
\]
assuming the normal branch is the intended operating equilibrium. The non-strict upper inequality is essential: a connected safe prefix may approach the unsafe witness load from below, so its supremum can equal that load even when the point itself is unsafe. The bounds do **not** establish that every disconnected higher load is unsafe.

## 4. Reproduction and outstanding work

The working-session source bundle contains a standalone file verify_witness_interval.py (dependencies: NumPy, SciPy, mpmath) plus the original IEEE-33 feeder/model scripts. Execute from the experiment folder:
- OPENBLAS_NUM_THREADS=1 python3 verify_witness_interval.py
- OPENBLAS_NUM_THREADS=1 python3 verify_witness_interval.py --saturated

The script constructs the network from decimal input data, evaluates physical fixed switching modes through an interval Jacobian and scalar residual, computes exact rational upper norm bounds and checks the voltage violation and mode inequalities. These are **not** probabilistic or sampling certificates.

**Current repository limitation:** this note records the resulting check, but the complete restored source dependency bundle is a separately downloadable conversation artifact and has **not yet been imported into PR #11**, so it is premature to claim reproducibility through this GitHub branch alone. An independent implementation/audit of the interval computations is advisable before publication.

**The remaining gap is on the lower side:** the connected safe capacities around g=1.92 (1.058600 MW, hybrid Hessian/phasor candidate) and g=2.6 (0.932000 MW) are only DOUBLE-precision candidate inner bounds. They require validated outward-rounded **all-input** normal-branch inclusions, Hessian/phasor/current and correlated PV capability enclosures. Where PVs may clip inside the uncertainty region, a local piecewise inclusion is still needed to extend the physical inner bound. No dynamic transient or certified globally optimal gain claim follows.
