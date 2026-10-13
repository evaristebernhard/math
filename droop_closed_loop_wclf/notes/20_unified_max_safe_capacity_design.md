# 20. Unified design of maximum robust safe hosting capacity: first gain-independent outer bound

Date: 2026-10-13. This **unifies** the previously labeled A (nonlinear uncertainty certificate) and B (gain selection) into a **single capacity design objective**. The existing implicit Jacobian, block Hessian, semi-disc support and complex-phasor bounds remain the safe-inner calculation; no replacement control law is proposed.

## 1. One objective, two verification obligations

On the specified normal steady-state branch of radial nonlinear DistFlow, choose four inverter gains \(g\in[0,4]^4\) and the largest loading prefix \([0,L]\) at bus 18 such that every input from the four independent right-half-disc PV uncertainty sets respects physical clipped Volt/VAR control, voltage 0.95–1.05 pu, branch currents \(\le0.31\) pu, and PV apparent-power capability \(P_j^2+Q_j^2\le(0.1)^2\) pu. Formally:

\[
L^\star=\sup_{g\in[0,4]^4}\sup\{L\ge0:
\forall\lambda\in[0,L],\,\forall w\in\mathcal U,\ 
\text{the designated physical steady solution exists and is secure}\}.
\]

The 0.31 pu common branch-current threshold and \(g\in[0,4]^4\) are **study assumptions**, not nameplate limits or dynamic-control admissibility guarantees.

An admitted safe connected prefix, obtained through the existing Hessian plus phasor envelopes, supplies a candidate **lower** design bound. To bound the **globally best** design, a fixed-g unsafe witness is NOT enough. The outer bound must exclude the loading level for every possible gain.

## 2. Gain-independent real-power and voltage necessary inequalities

Choose one *feasible* PV realization \(w_{p,j}=w_{q,j}=0\) for all four PVs. Each PV then has fixed active output \(P_{\rm PV}=0.025\) pu on the 10 MVA base. Regardless of inverter gain and whether clipping occurs,
\[
Q_{{\rm PV},j}\le q_{\rm cap}=\sqrt{0.1^2-0.025^2}<0.096825\ {\rm pu}.
\]
A robustly safe design MUST be secure for this PV realization. Thus we may allow every PV to produce the **ideal** \(+q_{\rm cap}\) independently of its gain; this enlarges the set of physically attainable compensations and gives a gain-independent relaxation.

Use the prior receiving-end DistFlow notation from notes 06:
\[
a=Dp-H_r\ell,\quad b=Dq-H_x\ell,\quad
\ell=(a^2+b^2)\oslash\nu,\quad
\nu=\mathbf1+2Rp+2Xq+M\ell.
\]
Let \(d_i(\lambda)=-\sum_{j\in\operatorname{desc}(i)}p_j(\lambda)\) be downstream **net active demand**, with base loads scaled by 0.65, each PV 0.025 pu active generation, and \(\lambda/10\) pu incremental demand at bus 18.

As all line resistances are positive, the receiving-end active power satisfies
\[
-a_i=d_i+\sum_{k\text{ strictly downstream of }i}r_k\ell_k\ge d_i.
\]
If all bus voltages are \(\le V_{\max}=1.05\) pu, then \(\ell_i=(a_i^2+b_i^2)/\nu_i\) obeys the **global gain-independent necessary lower bound**
\[
\boxed{\ell_i\ge L_i(\lambda):=
\frac{[d_i(\lambda)]_+^2}{V_{\max}^2}.}
\]
This does not require unsaturated droop, invertible Jacobian, a chosen control gain, or uniqueness of the power flow.

### First outer bound: source current and active power

Power balance yields \(P_{\rm source}=d_1+\sum_i r_i\ell_i\). Since source voltage \(V_{\rm source}=1\) pu, its first-line current satisfies \(P_{\rm source}\le I_1\le0.31\) pu for any secure operating point. Necessarily,
\[
\boxed{d_1(\lambda)+\sum_i r_i L_i(\lambda)\le0.31.}
\]
All quantities are rational for the exact-decimal benchmark. This implies the rigorous, but loose, gain-independent upper bound
\[
L^\star\le 1.506628\ {\rm MW}.
\]

### Sharper second outer bound: bus-18 undervoltage

For the explicitly transcribed active 32-branch case33bw, the **entire** bus-18 row satisfies \(X_{18,j}\ge0\) and \(M_{18,i}<0\). These signs are checked as exact rational comparisons by code/exact_design_upper.py. Give all PVs the ideal \(q_{\rm cap}\) and apply the current lower bounds \(L_i(\lambda)\) with negative \(M_{18,i}\). Every secure operating point, for ANY gain and either clipped/unsaturated mode, must satisfy

\[
\boxed{
0.95^2\le\nu_{18}\le
U_{18}(\lambda):=
1+2(Rp(\lambda))_{18}
+2(Xq^{\max})_{18}
+\sum_i M_{18,i}L_i(\lambda).
}
\]
Here \(q^{\max}\) means the fixed loads' negative reactive demand plus the **slightly larger rational** bound \(+0.096825\) pu on each PV. Using a rational quantity *above* the exact root preserves the direction of the upper bound. Since \(R_{18,18}>0\), downstream demands are nondecreasing with \(\lambda\), and all \(M_{18,i}<0\), this explicit upper envelope is nonincreasing for \(\lambda\ge0\). Once \(U_{18}\) drops below \(0.95^2\), larger connected safe capacities are impossible for every candidate gain.

The standalone exact-fraction script verifies
\[
U_{18}(1.452831\ {\rm MW})=0.9024999025804307\ldots
<0.9025=0.95^2.
\]
As rational inequalities, this gives the valid **all-gain capacity outer bound**
\[
\boxed{L^\star\le 1.452831\ {\rm MW}.}
\]
It is a relaxation-based **necessary** bound, not a proof that a gain achieves this capacity or that the optimum is near it. It uses exact-decimal benchmark data and theoretical upper voltage 1.05 pu, not feeder-parameter tolerances.

## 3. Improved numerical design candidate; safe-inner still NOT formally rounded

Using the previously developed real-arithmetic sufficient voltage Hessian bounds, geometric current bound, and correlated full PV P/Q unsaturation bound, locally optimize the four gains within [0,4] and **adaptively cover every load interval from 0**, refining cells that fail the coarse sufficient test. All such operations currently use **ordinary double precision**, so this is not yet a machine-certified safe inner.

A specifically reproducible fixed candidate is
\[
g_{\rm cand}=(3.80105,\ 1.89598,\ 2.39520,\ 4.00000)
\]
at buses 9,18,24,33. The interval-cover regression passes the *entire* \([0,1.1500]\) MW prefix using the unchanged nonlinear state/Jacobian/Hessian/phasor/physical-PV-capability math. The optimizer and the cover are deliberately separate: passing the terminal load cell alone is insufficient. The original uniform (1.92,1.92,1.92,1.92) float candidate was 1.0586 MW, so this improves the **candidate inner capacity** by 91.4 kW, approximately 8.63%; this is **not** established true physical capacity gain.

For the same exact five-decimal gain design, a feasible fixed PV disturbance \(w_p=0,\ w_q=-0.0125\) pu at all four PVs and extra load \(1.1870\) MW has a locally interval-certified physical equilibrium on the normal branch. The 64-dimensional fixed-point box has \(\rho_\infty<0.000268632\) and
\[
0.9499322797505< V_{18}<0.9499333324567<0.95,
\]
with all four PVs strictly **unsaturated** in the box. Thus the connected physical capacity for **this particular gain** satisfies
\[
\Lambda_{\rm conn}(g_{\rm cand})\le1.1870\ \text{MW}.
\]
This per-gain bound must NOT be substituted for the 1.452831 MW all-gain outer bound.

## 4. What is proved and what is still pending

**Proved:** the necessary all-gain analytic bound \(L^\star\le1.452831\) MW under the stated exact benchmark assumptions. Its proof uses elementary active-power balance and verified sign structure of the nonlinear DistFlow matrices, with rational arithmetic throughout.

**Checked with intervals for one fixed disturbance:** the 1.1870 MW **unsafe** operating point with the optimized candidate gains (local root existence and mode consistency). This remains a fixed-g upper obstruction, not a global bound for all gains.

**Float candidate only:** the 1.1500 MW connected **safe** capacity with the optimized gains, using the prior block Hessian plus phasor method, not outward-rounded all-input evaluation. Therefore one must NOT yet present the pair [1.1500,1.452831] as a rigorously established two-sided bracket: only its **right endpoint is proven**.

**Open and highest priority:** outward-rounded safe-prefix verification for \([0,1.10]\) MW (enough to prove improvement over the previously certified unsafe 1.09322 MW uniform-g witness), then to \([0,1.15]\) MW, before tightening global optimality. No transient, dynamic stability, true device limits, or full optimal-gain theorem has been established.

## 5. Reproduction

In a fresh clone of this PR **without any missing numeric bundle dependencies**:
```sh
cd droop_closed_loop_wclf
python3 code/exact_design_upper.py
```
It requires only Python's standard library and prints the exact gain-independent upper bound.

The **full inner numerical optimization** dependencies are still in the session's accompanying code ZIP, not yet committed into this PR. Their entrypoints are `design_max_safe_capacity.py`, `test_design_capacity.py`, and `verify_optimized_witness_interval.py`. They depend on the original `case33_data.py`, `block_hessian_33.py`, `hessian_phasor_capacity.py`, `physical_q_angular.py` and related scripts. Import the whole closure as one audited change, rather than committing broken single-script imports.
