# IEEE-33 capacity recheck: retain the Hessian, tighten currents using existing phasor geometry

Research record, 2026-10-13. **All numbers below use ordinary floating point, not certified outward-rounded interval arithmetic.** This is a continuation of notes 06, 09–10, 12–16 in the SAME capacity-control project; it does not abandon the Hessian analysis or introduce a new optimization objective.

## 1. The existing two bounds are complementary

Fix a gain g and a load cell \(I=[a,b]\). The nonlinear, unsaturated DistFlow solution is enclosed over the input uncertainty set using the original real-arithmetic inclusion inequalities. With load offset \(s=\lambda-\lambda_0\), the prior block-Hessian bound on any signed squared-voltage violation is

\[
U_{V,k}(s)= c_k+a_ks+
\tfrac12B_{\lambda\lambda,k}s^2+
B_{\lambda w,k}R_w|s|+
\tfrac12B_{ww,k}R_w^2 .
\]

The constant \(c_k\) includes the nominal signed violation and **exact** first-order right-half-disc supports (and any stated grouping constants). Every load within that cell for which all these signed voltage bounds are \(\le0\) passes the conservative voltage test.

For squared line current,
\[
\ell_l=\frac{a_l^2+b_l^2}{\nu_l},
\]
retain the previous analytic complex-power numerator enclosure, implemented by the existing aff_phasor routine. It evaluates a one-angle maximum of the affine 2D phasor response over all independent PV half-discs, adds a Lipschitz correction for the finite angular grid, adds a uniform nonlinearity residual, and divides the squared upper phasor norm by an enclosed lower squared voltage. This is another real-arithmetic **upper** enclosure on the *entire original cell*.

Where both valid methods are available, 
\[
U_{\ell,l}=\min\{U_{\ell,l}^{\rm Hessian},\,
U_{\ell,l}^{\rm phasor}\}
\]
is also a valid upper enclosure. The current exploratory implementation selects the phasor bound for every line and the **block Hessian for every voltage**. This is a choice of certificate, not a physical controller mode switch.

For each PV, preserve the correlated total output constraint \(P_{\rm PV}^2+Q_{\rm PV}^2\le S^2\). An affine vector angular support over the input half-discs plus a voltage Hessian remainder upper-bounds the **unsaturated raw** inverter phasor norm over the whole cell. Accept the cell only when its upper bound is \(\le S\). Consequently the smooth feedback equals the physically clipped controller throughout every accepted cell. The method does **not** extend a smooth Hessian across a saturation switch.

Combine the accepted load subintervals into a connected safe prefix from zero. Stop at the first gap; use finer input cells at the boundary. A failed inner test means **unknown**, never physically unsafe.

## 2. Physical outer witness

Independently, evaluate the actual clipped PV reactive law

\[
Q_j=\operatorname{clip}\bigl(w_{q,j}-g(V_j-1),
-\sqrt{S_j^2-P_j^2},+\sqrt{S_j^2-P_j^2}\bigr)
\]

under one feasible fixed adversarial disturbance

\[
(w_{p,j},w_{q,j})=(0,-0.0125)\ {\rm pu},
\quad j\in\{9,18,24,33\}.
\]

A **feasible violating power-flow solution** at a concrete load \(L_u\) obstructs a continuously safe load prefix reaching that load, even if disconnected safe states exist at higher loads. The current witness solves are double-precision normal-branch roots and have **not** received an outward-rounded interval-Newton existence proof.

## 3. Corrected IEEE-33 numerical candidate comparison

Model: manually transcribed in-service MATPOWER case33bw, 32 radial branches; 10 MVA and 12.66 kV base; base demand scaled 0.65; PV nodes 9, 18, 24, 33 with 0.25 MW nominal P and 0.125 MVA half-disc uncertainty each; S=1 MVA each; extra unity-PF load at bus 18; voltage [0.95,1.05] pu. The **uniform current limit 0.31 pu is a research assumption, NOT physical nameplate data**.

| Gain | Old connected inner MW | Improved hybrid inner MW | Float witness crossing MW | Explicit violating witness MW |
|---:|---:|---:|---:|---:|
| 1.85 | 1.032555 | **1.033948** | 1.064081 | 1.06508 |
| 1.90 | 1.019221 | **1.053233** | 1.084209 | 1.08521 |
| 1.92 | not available | **1.058600** | 1.092220 | 1.09322 |
| 2.00 | 0.997477 | **1.039200** | 1.124033 | 1.12503 |
| 2.60 | 0.860000 | **0.932000** | 1.221732 | 1.22273 |
| 3.00 | 0.780000 | **0.884700** | 1.243452 | 1.24445 |

At gain 2.6, around load 1.00–1.02 MW, the old scalar-Hessian current bound on line 1 is approximately 0.334 pu (fails the assumed 0.31 threshold), whereas the existing phasor geometric upper is approximately 0.286 pu (passes). The subsequent high-g conservative inner cutoff is driven primarily by the **full PV apparent-power upper bound**, not the actual observed line current. This is an improvement in usable conservative mathematics, not proof that the physical system cannot operate safely beyond the cutoff.

At gain 1.92, a concrete clipped-controller root for \(L=1.09322\) MW has minimum voltage about 0.9499619 pu and maximum algebraic residual about \(1.46\cdot10^{-16}\); no PV clipped at this particular witness. At gain 2.6 and \(L=1.22273\) MW, PV18 clipped, minimum voltage about 0.9499269 pu, and residual about \(1.12\cdot10^{-13}\).

The best **tested hybrid inner candidate** is around gain 1.92 among tested gains, superseding the former statement that gain 1.85 was best **for the old bound**. Neither a finite gain grid nor any of these float results proves a physically optimal gain.

## 4. Reproducibility and remaining closure

The previous session's IEEE-33 source archive and dependency scripts were recovered in the working session. New scripts (with original dependencies restored) are:

- hessian_phasor_capacity.py — block Hessian voltages + old phasor line-current upper + full PV capability;
- adaptive_hessian_phasor.py — refine connected-safe prefix from the previous value;
- run_hybrid_comparison.py — connected-inner versus clipped-controller unsafe witnesses;
- test_hybrid_capacity.py — sampling checks and nonlinear-solve residual regressions.

Local deterministic 33-bus analytic-Hessian-versus-finite-difference tests, phasor sampling regressions and gain/inner/witness reruns passed. The 18-file Python source-and-results archive is available as a conversation artifact, but the **exact dependency-closed source has not yet been imported into this GitHub PR**. Do not claim GitHub CI reproducibility from this note alone.

The remaining original work is (a) import the source closure, (b) replace double-precision tests with outward-rounded interval inclusion/Hessian/phasor/PV-capability bounds, and (c) certify existence of a physical unsafe witness. When raw PV output reaches S, a saturation-aware local mode inclusion is needed to advance the physical safe **inner** boundary, but there is no reason to discard the smooth Hessian calculations on the large unsaturated subset. The task remains **capacity first**; no dynamic transient or real line-nameplate conclusion is asserted.
