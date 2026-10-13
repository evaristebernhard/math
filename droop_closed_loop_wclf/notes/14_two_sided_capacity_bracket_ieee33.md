# IEEE 33: a two-sided numerical hosting capacity bracket using one unsafe witness

Research note, 2026-10-13. This strengthens notes 12-13 by producing both an inner load capacity and an independent physical *exclusion* test at higher loads. **All interval arithmetic in this prototype is ordinary double precision; these are verified formula checks, NOT directed-rounding machine proofs.**

## Scope of the control model

- The radial MATPOWER 33-bus feeder is represented by the existing nonlinear squared-voltage/squared-current DistFlow equations.
- Base P,Q demand scaled by .65; PV nodes 9,18,24,33, base output .25 MW each, semi-disc uncertainty .125 MVA each.
- Add unity power factor load at bus 18 in [0,1.25] MW.
- Gains fixed at g=1.85; unsaturated voltage-magnitude Q/V feedback Q_i=-g_i(V_i-1) in consistent pu and inverter reactive reserve validated inside the safe inner certificate.
- Voltage restriction V>=.95 pu; other upper-voltage, line current, and inverter headroom conditions in note 12.
- This **fixed-g, smooth unsaturated controller branch** is the scope. Outside inverter reactive reserve, realistic saturated Volt/VAr control is a *different* piecewise problem and needs a separate validation.

## 1. Existing conservative inner bound

Note 12 reported a 33-bus *numerically accepted* contiguous steady safe load interval 0–1.032555 MW with blockwise Hessian bounds. This is an inner candidate obtained under the uniform chosen uncertainty sets, not the globally optimal capacity and not a formal directed-rounded safety proof.

## 2. A single valid disturbance excludes a load level

Take one feasible PV disturbance:
$$
\Delta p_i=0,\quad\Delta q_i=-0.125\ {\rm MVA},
\qquad i\in\{9,18,24,33\}.
$$
All four points are on the right half-disc boundary, so this is a valid adversarial witness in the specified uncertainty set.

Direct nonlinear closed-loop solutions along the selected normal branch are:

| Incremental load (MW) | bus-18 voltage (pu) | status for this witness |
|---:|---:|---|
| 1.030 | 0.951311 | passes voltage lower limit |
| 1.065 | 0.9499645040 | violates V>=.95 |
| 1.100 | 0.948608 | violates V>=.95 |

For any fixed controller and load λ, a single *feasible disturbance* violating one security constraint is enough to prove that λ is **not** robustly feasible. But this fact at λ=1.065 alone does NOT exclude every λ>1.065 unless a persistent violating condition is established.

## 3. Excluding all larger loads in the tested domain (conditional inverse-Jacobian sign check)

For the **fixed PV witness**, construct nonlinear power-flow solutions parameterized by λ across [1.065,1.25], with bus 18 injection changed by −0.1 pu per MW. Set q_i baseline to include the selected PV reactive perturbations and set the PV uncertainty radii to zero; enclose each loading subinterval [a,b] with an auxiliary half-disc injection radius (b−a)/10 at bus 18. This is a conservative **superset** of the true load line segment. Use 10 subintervals.

Let J=F_z, J0 its nominal value, P=J0^{-1}, and E a componentwise uniform bound on |J−J0| for the entire state/parameter enclosure. If B=|P|E has spectral radius below one (checked numerically), define the nonnegative inverse majorant
$$
W=(I-B)^{-1}|P|,\quad
|J^{-1}|\le W,\quad |J^{-1}-P|\le W-|P|.
$$
For a verified componentwise bound
$$
|F_\lambda-F_{\lambda,0}|\le \Delta_\lambda,
$$
the parameter sensitivity z_lambda=−J^{-1}F_lambda obeys
$$
\boxed{
z_\lambda \le -P F_{\lambda,0}
+(W-|P|)|F_{\lambda,0}|+W\Delta_\lambda
}
$$
componentwise. In the unit-power-factor loading case,
$$
F_\lambda=
\begin{bmatrix}
2Rd\\2(a/\nu)\odot(Dd)
\end{bmatrix},\quad d=.1e_{\rm bus18}.
$$
A sound interval bound for Δ_lambda uses the independently enclosed change of a/nu on the candidate state box.

The **largest** (least negative) double-precision bound produced across the 10 subintervals for bus-18 squared voltage was
$$
\boxed{\partial_\lambda\nu_{18}\le-0.0729492\ {\rm pu}^2/{\rm MW}.}
$$
Every interval inclusion test reported pass in the existing floating-point implementation. Thus, **assuming the real-arithmetic interval majorants remain valid**, bus-18 voltage is strictly decreasing along this fixed-witness unsaturated normal branch throughout [1.065,1.25] MW. Since it is already below 0.95 pu at 1.065 MW, this excludes the whole larger-load interval from robust feasibility on that branch.

Importantly, the upper exclusion after inverter Q saturation must be checked using the actual saturated controller or interpreted as exclusion for the *unsaturated-control model only*. One cannot silently extend an unsaturated algebraic derivative into a physical saturated-device safety claim. The numerical point at 1.065 MW was still within computed inverter headroom in this model; saturation occurs shortly thereafter.

## 4. Candidate two-sided bracket (fixed g and controller regime)

For the fixed-g, unsaturated-branch study on [0,1.25] MW:
$$
\boxed{1.032555\lesssim\Lambda_{\rm hosting}(g=1.85)\le1.065000\ {\rm MW}}
$$
in the **numerical certificate sense**, yielding an unresolved band ≈0.032445 MW, ~3% of the target. The lower endpoint is a conservative robustness check for *all* PV half-disc disturbances, while the upper endpoint is a *single feasible adversarial PV disturbance* plus monotonic derivative across higher load levels. These logically different guarantees form a useful capacity bracket.

No certification is claimed for controller gains not equal to 1.85, alternate PV/drop settings, loads above the tested 1.25 MW domain, or full saturated-inverter behavior. Since no outward rounding was used, neither endpoint is yet an independently machine-verified IEEE-33 certificate.

## 5. Why this is closer to the right paper

The engineering question is whether the controller can **safely accept more MW**, not whether another WCLF solver is 0.1 seconds faster. The two-sided strategy directly produces a physically interpretable capacity interval. The next mathematically meaningful task is to tighten the *lower* side, validate the *upper* exclusion across actual Q saturation regimes, and extend this two-sided capacity bracket to a range of controller gains g.

The prior experiments/witness_capacity_upper_probe.py from this research session (with dependencies from the experiment bundle, not yet integrated into this PR) reproduces the local inverse-Jacobian derivative sign calculations. Import a complete runnable dependency closure in a future commit rather than adding broken imports.
