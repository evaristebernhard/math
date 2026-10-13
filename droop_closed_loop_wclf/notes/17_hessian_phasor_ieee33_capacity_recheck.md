# IEEE-33 capacity recheck: retain the block Hessian, tighten current via existing phasor geometry

Date: 2026-10-13. **Numerical status: ordinary double-precision exploratory results, NOT outward-rounded certificates.** This note continues notes 06, 09, 10, 12–16; it does **not** replace the Hessian route with a different control theory.

## 1. One hybrid inner-envelope, rather than competing methods

In each load cell (I=[a,b]), use the existing nonlinear smooth-branch state inclusion and its componentwise implicit Hessian bound (H_k). For squared-voltage safety, preserve the existing block-Hessian inequality
[
U_{V,k}(s)=c_k+a_ks+rac12B_{lambdalambda,k}s^2+
B_{lambda w,k}R_w|s|+rac12B_{ww,k}R_w^2 le 0,
]
where the independent right-half-disc first-order supports are included in (c_k). The cell is only accepted for those load values where all upper and lower voltage inequalities pass.

For a line, the prior code also has a *different valid real-arithmetic upper bound*, derived directly from the complex-power numerator
[
ell_l=rac{a_l^2+b_l^2}{
u_l}.
]
Taylor-expand the phasor ((a_l,b_l)) in the uncertain injections; compute the exact affine norm maximum via one angular support-function maximization over independent half-discs, add the angular-grid Lipschitz allowance and a uniform nonlinear residual bound, and divide its squared upper numerator by the verified lower (
u_l). This is `affine_phasor_current_bound.aff_phasor` from our earlier work.

**Hybrid rule:** for a line cell, use whichever proven-in-real-arithmetic squared-current upper enclosure is smaller, (U_{I,l} = min{U_{I,l}^{H},U_{I,l}^{mathrm{phasor}}}). In this exploratory implementation, use the phasor bound for every line on the whole original cell while retaining block-Hessian for every voltage constraint. Minima of upper bounds are still upper bounds. There is no discontinuous switching of the *physical controller* in this hybrid decision; it only selects between two upper-bounding formulas.

For each inverter, continue to use the corrected correlated **full** apparent-power bound on its raw ((P,Q)) output: one angular support maximum plus the voltage Hessian Taylor remainder, requiring (P^2+Q^2le S^2) over the **entire original cell**. Thus every accepted cell is unsaturated for all modeled uncertainties, and its smooth-branch state coincides with the physically clipped PV controller. No Hessian is applied across an uncertified saturation surface.

The final connected prefix is the union of accepted safe load subintervals reachable from zero, and **stops at the first gap**. Adaptive refinement of cells near the boundary improves the load resolution. Failure of an inner bound is **unknown**, not proof of unsafe physical operation.

## 2. Independently computed physical outer witnesses

For the actual clipped inverter law (Q=mathrm{clip}(w_q-g(V-1),pmsqrt{S^2-P^2})), solve nonlinear DistFlow at the *admissible fixed disturbance*
[
(w_{p,j},w_{q,j})=(0,-0.0125) {m pu},qquad jin{9,18,24,33}.
]
It is on each PV right-half-disc boundary. Any concrete load where the clipped physical solution violates voltage or thermal safety is an upper obstruction to **connected** load hosting, even without proving voltage monotonicity for all larger load levels. At present the physical witnesses are double-precision roots (residual roughly 1e-16 to 1e-13); a genuine interval-Newton existence proof remains to be added.

## 3. Corrected IEEE-33 candidate numerical values

Same assumed feeder as note 15: MATPOWER case33bw, 32 branches, 12.66 kV / 10 MVA base; 0.65 times original loads; PVs at 9/18/24/33, each with nominal P=0.25 MW, right-half-disc radius 0.125 MVA, nameplate S=1 MVA; bus-18 additional unity-PF flexible load. Bounds 0.95–1.05 pu voltage and a **research-assumed** common 0.31 pu line-current threshold, not actual line ratings.

| Gain g | Prior float inner (MW) | Hybrid connected float inner (MW) | Numerically located witness crossing (MW) | Explicit violating load (MW) |
|---:|---:|---:|---:|---:|
| 1.85 | 1.032555 | **1.033948** | 1.064081 | 1.06508 |
| 1.90 | 1.019221 | **1.053233** | 1.084209 | 1.08521 |
| 1.92 | not previously tabulated | **1.058600** | 1.092220 | 1.09322 |
| 2.00 | 0.997477 | **1.039200** | 1.124033 | 1.12503 |
| 2.60 | 0.860000 | **0.932000** | 1.221732 | 1.22273 |
| 3.00 | 0.780000 | **0.884700** | 1.243452 | 1.24445 |

For example at g=2.6, load interval [1.00,1.02] MW, first-line current upper estimates from the *same* smooth model were approximately 0.33422 pu using the full scalar Hessian and 0.28617 pu using phasor geometry, versus 0.31 pu assumed limit. A current-Hessian failure was artificial; independent **PV capability** may still prevent certification of the high-g cell. At g=1.92, the candidate connected inner exceeds the old best tested g=1.85, **but neither this finite gain sweep nor its float margins proves the physical optimal gain**.

A fixed explicit violating witness for g=1.92 at 1.09322 MW yielded minimum bus voltage 0.9499619 pu (<0.95 pu) and residual 1.46e-16 (double precision); no PV was saturated at that witness. For g=2.6 at 1.22273 MW, PV 18 was clipped, minimum voltage was 0.9499269 pu, and residual 1.12e-13.

## 4. Code status and next closure

The complete source dependency package from the earlier IEEE-33 session archives was recovered and run, together with these added scripts:
- `hessian_phasor_capacity.py`: reuse block Hessian for voltage, original phasor envelope for all currents, full correlated PV capability;
- `adaptive_hessian_phasor.py`: refine the connected safe prefix near the apparent limit;
- `run_hybrid_comparison.py`: independent clipped-Q witness and comparison table;
- `test_hybrid_capacity.py`: floating Hessian/phasor/witness consistency regressions and randomized sampling checks.

The full 18-file runnable research bundle has been prepared as a downloadable session artifact, but **is not yet imported into this PR's source tree**. Do not portray this note as a GitHub-CI-reproducible experiment until the exact dependency-closed source is imported. Local 33-bus Hessian finite-difference regression and hybrid regression were run, and the numerical bracket scripts were rerun.

The next priority remains **the original capacity objective**, not a new theorem: import the complete source dependency closure, replace double precision with outward-rounded enclosures for the inner branch and its Hessian/current/PV reserve, certify existence of the explicit unsafe witness, and then tackle Q-limited modes only where the new full PV capability bound actually fails. An interval failing the raw unsaturation test is not evidence of physical unsafety. No dynamic-transient safety or actual feeder thermal nameplate claim follows from this work.
