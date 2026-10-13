# 16. Saturation-aware hosting capacity via a projected variational inequality

Research note — 2026-10-13. Scope: **continuous robust steady-state hosting capacity** for the physically clipped Volt/VAR inverter model in notes/15. This is a conditional theorem plus an exact-rational scalar test; **not** a machine-certified IEEE-33 DistFlow capacity.

## 1. Why the smooth Hessian route stops at the Q limit

For a PV inverter with active output P_j(u), reactive disturbance w_{q,j}, gain g_j>=0 and nameplate S_j, require |P_j(u)|<S_j over the entire uncertainty set and put

```math
c_j(u) = sqrt(S_j^2 - P_j(u)^2),  Q(u) = product_j [-c_j(u),c_j(u)].
```

The physical steady controller is
```math
q = Pi_{Q(u)}(w_q - G(V-Vref)).
```
The projection exactly represents apparent-power saturation. The unsaturated closed-loop Hessians from notes/06 and notes/09 do **not** extend across the switching kink. A new bound must work on both sides of every kink.

Let `u=(lambda,w_p,w_q)` range over a compact rectangular-or-half-disc parameter cell. **Assume**, with independent verification still needed on IEEE 33, that for every `u` and every `q` in a common convex domain `D` containing `Q(u)`, the open-loop nonlinear DistFlow equations admit a designated regular normal-operating solution, and the extracted voltage function `V(u,q)` is continuously differentiable in `q` on this domain. No claim is made about other AC roots outside the verified branch.

Define
```math
A_u(q) = q - w_q + G(V(u,q)-Vref).
```
Then for **any** step `tau>0` the physical equilibrium equation is equivalent to the variational inequality
```math
< A_u(q*), y-q* > >= 0  for every y in Q(u),
```
and to the projected-gradient fixed point
```math
q* = T_u(q*) := Pi_{Q(u)}(q* - tau A_u(q*)).
```
The equivalence follows directly from the characterization of Euclidean projection. It remains valid when active sets switch.

## 2. Uniform projected contraction theorem (no derivative of clip)

**Theorem.** Suppose, uniformly for all `u` in the cell and all `q,q'` in `D`,
```math
< A_u(q)-A_u(q'), q-q' > >= mu ||q-q'||_2^2,
||A_u(q)-A_u(q')||_2 <= L ||q-q'||_2,
```
where `mu>0` and `L>=mu`, and `Q(u) subset D`. Choose `0<tau<2mu/L^2` and define `rho=sqrt(1-2tau mu+tau^2 L^2)<1`.

Then every `u` has a unique physical clipped-control steady equilibrium in `Q(u)`, and for every fixed `q0 in D`,
```math
||q*(u)-q0||_2 <= ||T_u(q0)-q0||_2/(1-rho).
```
In particular, if a validated uniform residual bound `r >= sup_u ||T_u(q0)-q0||_2` is available, all solutions over the parameter cell satisfy `||q*(u)-q0||_2 <= r/(1-rho)`.

**Proof.** Projection onto any nonempty closed convex `Q(u)` is nonexpansive. Therefore
```math
||T_u(q)-T_u(q')||_2^2
 <= ||(q-q')-tau(A_u(q)-A_u(q'))||_2^2
 <= (1-2tau mu+tau^2 L^2)||q-q'||_2^2.
```
For each `u`, `T_u` maps the closed complete box `Q(u)` to itself and is a contraction there. Banach's fixed-point theorem gives existence and uniqueness. Since `q*=T_u(q*)`,
```math
||q*-q0|| <= ||T_u(q*)-T_u(q0)||+||T_u(q0)-q0||
<= rho ||q*-q0||+||T_u(q0)-q0||.
```
Rearrange. QED.

A practical sufficient condition for the first assumption is a **validated** bound
```math
lambda_min((I+G D_qV + (D_qV)^T G)/2) >= mu > 0,
||I+G D_qV||_2 <= L
```
throughout the entire open-loop state/parameter box. A sampled Jacobian at the nominal load is insufficient. Importantly, `||G D_qV||<1` is **not necessary**: strong monotonicity of `I+G D_qV` may survive even at large gain. The projection iteration here is a **proof device**, not a claim that real hardware implements this discrete-time algorithm or that its transient response is stable.

## 3. Turning the q error into a robust capacity certificate

For each load-and-PV parameter cell `U_cell`, validate `r,mu,L` and write `B=r/(1-rho)`. At the same fixed `q0`, obtain verified intervals for `V_i(u,q0)`, squared line currents `ell_l(u,q0)`, and corresponding Lipschitz constants in `q`:
```math
|V_i(u,q)-V_i(u,q0)| <= K_{V,i}||q-q0||_2,
|ell_l(u,q)-ell_l(u,q0)| <= K_{I,l}||q-q0||_2.
```
Then over the entire cell
```math
V_i in [V_i^lo(q0)-K_{V,i}B, V_i^hi(q0)+K_{V,i}B],
ell_l <= ell_l^hi(q0)+K_{I,l}B.
```
If these bounds satisfy every voltage and thermal inequality, the cell is robustly safe **including all Q saturation surfaces**. Apparent-power capability follows automatically from projection provided the input active-power `|P|<S` was verified.

Cover `[0,Lambda] x U_PV` by finitely many validated cells, using interval/half-disc enclosures and optionally adaptive partition. If all pass, then `[0,Lambda]` is a continuously safe steady load prefix. Separately, one verified feasible PV disturbance at a load `Lambda_unsafe` with a clipped-controller out-of-limits equilibrium proves `Lambda_conn<=Lambda_unsafe` (notes/15). This gives the capacity-first two-sided bracket with no false global load monotonicity assumption.

**Remaining obligations for IEEE 33:** verified open-loop AC/DistFlow branch across the q domain; outward-rounded interval bounds on the symmetric Jacobian, operator norm, projected residual and safety quantities; the full correlated half-disc P/Q set (rectangular supersets are sound but may be loose); physical line-specific current limits; rigorous unsafe witness solve. None is currently completed in this PR.

## 4. Exact-rational switching toy that defeats the naive Picard test

Consider a deliberately simple affine voltage feeder, not full nonlinear DistFlow:
```math
V(lambda,w_p,q) = 0.995 -0.11 lambda -0.02 w_p +0.06 q,
g=45,  P_PV=0.15+w_p, S=0.25,
0<=w_p<=0.02, |w_q|<=0.02.
```
The actual PV set is the right half-disc `w_p^2+w_q^2<=0.02^2, w_p>=0`. We certify over the **larger rectangle**, hence also over that half-disc.

Here `g*dV/dq=2.7>1`, so the usual `g L_q<1` contraction test for the raw physical response fails. Yet
```math
A(q)=(1+2.7)q+45(0.995-0.11lambda-0.02w_p-1)-w_q,
mu=L=3.7.
```
For `tau=1/3.7`, the projected-gradient map is constant in q (contraction factor zero), and the exact equilibrium is
```math
q*(lambda,w_p,w_q)
 = clip((w_q-45(0.995-0.11lambda-0.02w_p-1))/3.7,
        -sqrt(0.25^2-(0.15+w_p)^2),
        +sqrt(0.25^2-(0.15+w_p)^2)).
```
This equilibrium crosses into PV Q saturation as load rises.

The accompanying `code/saturation_vi_toy.py` checks every one of 4^3 **closed rational parameter cells** partitioning `lambda in [0,0.50], w_p in [0,0.02], w_q in [-0.02,0.02]`. It uses Fraction arithmetic and integer square-root upper/lower rational enclosures; it does not use floating point for pass/fail. Interval monotonicity of `clip` and the exact scalar closed form give, over the entire union,
```math
0.95059818166788... <= V <= 1.007,
```
which validates a safe connected voltage capacity of at least `0.50` in the toy's load units (and respects PV apparent-power capability). At the feasible right-half-disc witness `lambda=0.51,w_p=0.02,w_q=0`, the rational upper voltage enclosure is `V<0.94949818166795<0.95`. Thus
```math
0.50 <= Lambda_conn < 0.51
```
for the scalar toy under voltage and inverter capability constraints. The upper-obstruction witness suffices for **connected** capacity, without excluding disconnected safe load levels.

Run `python3 code/saturation_vi_toy.py` from `droop_closed_loop_wclf/`. This is a tested mathematical example, **not** a numerical improvement of the IEEE-33 result.

## 5. Novelty and next step

Projection/variational-inequality formulations of Volt/VAR equilibrium and fixed-point solvability are already present in existing literature; do **not** claim their invention here. Relevant background includes *Equilibrium and dynamics of local voltage control in distribution systems* and *Power Flow Solvability with Volt-Var Controlled Inverter-Based Resources* (arXiv:2604.17205). The specific contribution sought is a computationally **verified, saturation-aware, two-sided nonlinear DistFlow capacity bracket with explicit MW accuracy**, including correlated PV capability, not merely an abstract projection theorem.

**Next required implementation:** import the actual case33bw and old session feeder dependency files into PR #11; compute verified `mu,L,r` on the same fixed-g values g=1.85 and g=2.6, and reject any result not enclosing every PV/load point and Q limit. Only then compare capacities or optimize g.
