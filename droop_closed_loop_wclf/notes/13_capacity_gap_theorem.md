# Capacity is the outcome: a certified MW-gap theorem

Research note, 2026-10-13. This note deliberately makes *load hosting capacity* rather than accuracy of standalone worst-case load flow the mathematical objective.

## 1. Precise control target

Choose a *normalized* vector of safety violations phi_k(lambda,g,w) / s_k, with strictly positive physical scales s_k. These include:
- ν_i^min−ν_i (under-voltage),
- ν_i−ν_i^max (over-voltage),
- ell_l−ell_l^rated (line-square-current),
- P_inv,i²+Q_inv,i²−S_inv,i² (inverter apparent-power capability).

All are evaluated on a validated normal-operating branch of nonlinear DistFlow with voltage-dependent inverter reactive control. Given compact uncertainty U and control gain g define

$$
h_k(\lambda,g)=\max_{w\in U}\frac{\phi_k(\lambda,g,w)}{s_k},\quad
H(\lambda,g)=\max_k h_k(\lambda,g).
$$

The real robustly safe scalar load set is

$$
C_{\mathrm{true}}(g)=\{\lambda\in[0,\lambda_{\max}]:H(\lambda,g)\le0\}.
$$

Define the *pointwise hosting upper boundary* Lambda_true(g)=sup C_true(g), if the set is nonempty. A *continuously reachable steady safe* upper capacity from currently safe lambda0 is the right endpoint of the connected component of C_true containing lambda0. They are not interchangeable, especially in the presence of reverse PV power flow.

Do not call this a dynamic/inverter-transient guarantee; it is a steady-state robust capacity definition.

## 2. How worst-case uncertainty certificates become conservative MW capacities

Suppose every h_k admits a verified conservative majorant h_k^U such that for every load in an interval of interest

$$
0\le h_k^U(\lambda,g)-h_k(\lambda,g)\le\delta_k.
$$

Define H^U=max_k h_k^U and δ=max_k δ_k. Then

$$
0\le H^U-H\le\delta,
$$

and the certified load set C_cert={λ: H^U(λ,g)<=0} is a subset of the real robustly safe set.

The error δ has the same dimensionless units as H. Error certificates for squared voltages, squared currents and inverter apparent power MUST be divided by their own s_k first before δ is aggregated.

One practical *a posteriori* δ_k bound comes from verified upper majorant h_k^U and any feasible disturbance candidate w_k*(λ,g). Since
$$
\phi_k(\lambda,g,w_k^*)/s_k\le h_k\le h_k^U,
$$
we may set
$$
\delta_k=h_k^U-\phi_k(\lambda,g,w_k^*)/s_k.
$$
A uniform δ_k over a *whole load interval* must be validated as such, not inferred from a few sampled loads.

## 3. A local quantitative capacity-gap theorem

**Theorem.** Fix g and a compact load domain. Assume C_true(g) is nonempty and Lambda_true(g)=λ* is its right endpoint, with H(λ*)=0. Suppose there exist m>0, δ>=0 and an interval [λ*−δ/m, λ*] inside the domain such that

1. H is continuous, and for every λ in that interval,
$$
H(\lambda)\le H(\lambda^*)-m(\lambda^*-\lambda)=-m(\lambda^*-\lambda).
$$
(a sufficient condition is uniform derivative slope H(λ2)−H(λ1)>=m(λ2−λ1) near λ*);
2. throughout this interval, H<=H^U<=H+δ.

Then λ*−δ/m belongs to C_cert and

$$
\boxed{0\le\Lambda_{\rm true}(g)-\Lambda_{\rm cert}(g)\le\delta/m.}
$$

**Proof:** Evaluate the first inequality at λ*−δ/m: H<=−δ. The certified upper bound satisfies H^U<=H+δ<=0, so that point is certified safe. The inclusion C_cert⊂C_true guarantees Lambda_cert<=λ*. Since Lambda_cert>=λ*−δ/m, the claim follows. QED.

This theorem is LOCAL to a physically valid rightmost capacity boundary. It does not assume global monotonicity of capacity feasibility; nonmonotone under/over-voltage and reverse-flow overcurrent away from this boundary remain allowed. If H is flat at its terminal boundary (m=0), the theorem gives no quantitative loss bound.

**Gain-optimized corollary.** If the hypotheses hold for every admissible g with common m and δ, and all candidate gain settings admit nonempty capacity sets, then

$$
0\le \sup_g\Lambda_{\rm true}(g)-\sup_g\Lambda_{\rm cert}(g)\le\delta/m.
$$

Proof: choose a sequence of gains whose true capacities approach the supremum, apply the fixed-g theorem to each, and take the supremum. The uniform-in-g hypothesis is substantial and has NOT yet been certified for IEEE 33 buses.

## 4. How the Hessian theory can deliver δ

For a normalized constraint φ_k/s_k with disturbance w=epsilon*u in a product of half-discs, compute an exact first-order maximizing candidate u_k* from the support function.

If the quadratic growth kappa_k>0 and a *uniform certified* Hessian bound M_k applies on the entire disturbance set, then the note/02 cubic-gap theorem provides

$$
0\le h_k - \frac{\phi_k(\lambda,g,\epsilon u_k^*)}{s_k}
\le \frac{M_k^2R_U^2}{4\kappa_k}\epsilon^3.
$$

Therefore the rightmost expression can serve as a δ_k for h_k^U=(φ_k evaluated at u_k*)/s_k + δ_k. For a minimum voltage constraint the normalized violation φ^L=(νmin−ν)/s is already a *maximum* type, so the same approach works without a separate minimization theorem.

If kappa_k=0 or a regime switches, apply a valid quadratic fallback or interval enclosure. The advertised O(epsilon^3) capacity-gap scaling additionally requires a uniform m>0, uniform M and kappa bounded away from zero as epsilon shrinks. Otherwise no such scaling follows.

## 5. Exactly solvable non-monotone toy

Take a one-line **lossless fixed-voltage** toy, NOT full nonlinear DistFlow:

$$
\ell(\lambda,w)=(\lambda-0.30-w_p)^2+w_q^2,\qquad
w_p\ge0,\quad w_p^2+w_q^2\le0.05^2,\qquad
\ell\le0.20^2.
$$

Its exact robust maximum is

$$
h_I(\lambda)=\begin{cases}
(\lambda-0.35)^2,&\lambda<0.30,\\
(\lambda-0.30)^2+0.05^2,&\lambda\ge0.30,
\end{cases}
$$
and the *physical* safe load interval is [0.15, 0.4936491673...] in the same per-unit active-power coordinates. λ=0 is unsafe; moderate extra load reduces reverse flow and restores safety.

Suppose a reliable outer bound for the squared-current maximum has additive conservatism δ_I=0.001 (squared-current pu, not MW). On the right branch, the outer certificate h_I^U=h_I+0.001 gives
$$
\Lambda_{\mathrm{cert}}=0.30+\sqrt{0.20^2-0.05^2-0.001}
=0.4910497317\ldots
$$
while Lambda_true=0.4936491673..., so the actual loss is 0.0025994356 pu of incremental power.

On [0.45,Lambda_true], derivative h_I' =2(lambda-0.30)>=0.30, so the theorem gives
$$
0\le\Lambda_{\rm true}-\Lambda_{\rm cert}\le0.001/0.30=0.0033333333\text{ pu},
$$
which is satisfied. These numbers are per unit; converting to MW requires specifying the power base. This demonstrates what a capacity-gap result means without claiming an actual IEEE-33-bus bound.

## 6. How to finish the real capacity-control paper

The most relevant next step is **not** demonstrating that a new interval solver outperforms a published worst-case-flow algorithm, but constructing a validated capacity boundary and an error bracket for that boundary:

1. Fix a load distribution and converter gain(s), and verify the nonlinear normal power-flow branch for all inputs in the chosen domain.
2. Compute safe inner capacity sets with existing quadratic/block Hessian enclosures and geometric worst-case bounds.
3. Near the upper capacity boundary, certify limiting-constraint slopes m using interval implicit derivatives (all possible active constraints, not just one sampled case).
4. Obtain upper/lower worst-case violation bounds, and a uniform δ. Convert this into an explicit error in MW via δ/m. If m cannot be verified, label the capacity a lower-bound estimate only.
5. Optimize gain g on top of the certified capacity mapping. Do not infer global optimality from a grid of g choices.
6. Only after single-period capacity is closed, add multi-period flexible-load energy scheduling. The existing dynamic-ramp demonstration remains a separate optional extension, not a prerequisite to mathematical capacity certification.

## 7. Current evidence: IEEE 33 remains a float prototype

Earlier custom 33-bus calculation at g=1.85 found a numerically accepted *connected conservative inner* loading interval approximately 0–1.033 MW at bus 18 (block-Hessian, no outward rounding), while a previous pointwise contractor passed a load level of approximately 1.04 MW on a 0.02 MW grid. The two results cannot establish tightness or a global capacity optimum, and do not yet provide verified δ/m. The contribution of this note is a precise mathematical bridge from a bound gap to lost load-hosting capacity.
