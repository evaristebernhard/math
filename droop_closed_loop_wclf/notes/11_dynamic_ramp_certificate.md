# Conditional transient load-ramp safety from nonlinear steady-state hosting margins

This is a separate *dynamic* extension of notes 07, 09, and 10. A steady-state nonlinear DistFlow certificate alone does **not** guarantee safety while inverter reactive controllers are moving. The result below has explicit rate and contraction hypotheses; arbitrary discontinuous renewable disturbances are **not** covered.

## 1. A quasi-static network coupled to real inverter states

Separate physical inverter reactive output q (a dynamic state) from the algebraic network variables z=(nu,ell). For given flexible-load size lambda and external injections w, define the nonlinear *open-control* power-flow residual
$$
F_{\rm PF}(z,q,\lambda,w)=0.
$$
Assume that on a specified compact region the normal operating root defines a continuously differentiable map z=Z(q,\lambda,w), with every squared voltage positive. Let nu(q,u) and ell(q,u) denote the corresponding outputs, u=(lambda,w).

Let physical inverter dynamics be
$$
\tau_i\dot q_i=-q_i+K_i(\nu_i^{ref}-\nu_i(q,u)),
\qquad \tau_i>0.
$$
Use a continuously differentiable unsaturated portion of K or a justified piecewise contraction argument for actual saturation. Denote the ODE right side by f(q,u).

For each u in a convex operating domain U_c, suppose there is a unique selected equilibrium q*(u) satisfying f(q*(u),u)=0, and q*(u) is C^1 in u. For full nonlinear operation, these properties require validation.

## 2. A conditional all-time tube theorem

Let Q be a convex box such that every tube {q:||q-q*(u)||_infty<=E} is contained in Q for all u in U_c. Suppose

1. The matrix measure (logarithmic norm) of the inverter vector field obeys
$$
\mu_\infty(\partial_q f(q,u))\le-\alpha<0
$$
for every q in Q, u in U_c.
2. The moving steady-state control has bounded sensitivities
$$
\|\partial_\lambda q^*(u)\|_\infty\le S_\lambda,\quad
\|\partial_w q^*(u)\|_{\infty\leftarrow\infty}\le S_w.
$$
3. Input trajectories are absolutely continuous with |dot lambda|<=v_lambda and ||dot w||_infty<=v_w almost everywhere. The initial error is ||q(0)-q*(u(0))||_infty<=E.

Then the tracking error satisfies
$$
D^+\|q-q^*(u)\|_\infty
\le-\alpha\|q-q^*(u)\|_\infty+
S_\lambda v_\lambda+S_w v_w.
$$
Thus if
$$
\boxed{S_\lambda v_\lambda+S_w v_w\le\alpha E,}
$$
the tube is forward invariant, and the explicit bound is
$$
\|q(t)-q^*(u(t))\|_\infty
\le e^{-\alpha t}\|e(0)\|_\infty+
\frac{S_\lambda v_\lambda+S_w v_w}{\alpha}(1-e^{-\alpha t}).
$$

**Proof.** For frozen u, the uniform negative matrix measure gives incremental contraction between any two state trajectories of dot q=f(q,u). Since q*(u(t)) is a moving zero of f, subtract its time derivative and apply the contraction/differential inequality to e=q-q*(u(t)). The chain rule and sensitivity bounds give ||dot q*||<=S_lambda v_lambda+S_w v_w. Gronwall yields the explicit bound. The inward derivative at ||e||=E prevents escape and closes the local argument because each tube was assumed contained in Q. QED.

This does **not** prove stability for a detailed electromagnetic converter or for inputs with unbounded time derivatives. It is an inverter first-order / quasi-static-network theorem.

## 3. Turn steady-state hosting margins into a safe ramp rate

Suppose the steady-state envelopes are valid for **all** u in the proposed load/uncertainty region and have squared-voltage/current safety margins
$$
\nu_i(q^*(u),u)-\nu_i^{min}\ge m_i^{lo},
$$
$$
\nu_i^{max}-\nu_i(q^*(u),u)\ge m_i^{hi},\quad
\ell_l^{rated}-\ell_l(q^*(u),u)\ge m_l^I.
$$
Let L_nu, L_ell be verified Lipschitz constants for outputs with respect to q in the tube:
$$
\|\nu(q,u)-\nu(q^*(u),u)\|_\infty\le L_\nu\|q-q^*\|_\infty,
$$
and likewise for ell with L_ell. Require uniform inverter Q reserve headroom >=E (and check actual P^2+Q^2<=S^2 across inputs).

Then a sufficient safety tube radius is
$$
\boxed{E_{\max}=\min\left\{
\min_i m_i^{lo}/L_{\nu},\
\min_i m_i^{hi}/L_{\nu},\
\min_l m_l^I/L_\ell,\
E_Q
\right\},}
$$
with zero-Lipschitz denominators omitted when the corresponding output is independent of q.

For any E<=Emax with initial error<=E, a sufficient ramp-speed constraint is
$$
\boxed{
v_\lambda\le\frac{\alpha E-S_w v_w}{S_\lambda}
}
$$
when S_lambda>0 and the right side is nonnegative. The formula is a *bound on load change speed* inside a previously certified *range of admissible load levels*. It does not itself establish the maximum load level.

If w can jump, the assumption ||dot w||<=v_w fails. A different reachable-set/invariant-box treatment is required. The same is true at uncontrolled inverter mode-switching instants unless a piecewise proof covers them.

## 4. Computable local contraction and equilibrium sensitivities

Let k_i=K_i'(\nu_i^{ref}-\nu_i), with k_i>=0 inside a differentiable droop segment and K_d=diag(k_i), T=diag(tau_i). Then
$$
f_q=-T^{-1}(I+K_d\nu_q),\quad
f_\lambda=-T^{-1}K_d\nu_\lambda,
$$
where nu_q and nu_lambda are evaluated from the *physical* nonlinear power-flow map Z(q,lambda,w), keeping q fixed in nu_lambda.

A sufficient infinity-norm contraction check uses
$$
\mu_\infty(f_q)=\max_i\left[
-\frac{1+k_i(\nu_q)_{ii}}{\tau_i}
+\sum_{j\ne i}\frac{k_i|(\nu_q)_{ij}|}{\tau_i}
\right]\le-\alpha.
$$
At a differentiable equilibrium the implicit function theorem gives
$$
\boxed{(I+K_d\nu_q)\,\partial_\lambda q^*
=-K_d\nu_\lambda,}
$$
and the analogous equation for external disturbances w. These matrices can be bounded with the interval-Jacobian machinery already required for hosting certification.

The logarithmic norm may establish contraction even when a naive small-gain condition ||K_d nu_q||<1 fails. For an arbitrary nonnormal multivariable system a weighted norm may substantially improve the bound.

## 5. Scalar worked example (only a check of the theorem)

Take nu=nu0-a lambda+bq, linear unsaturated K(y)=g y, nu_ref=nu0, tau=1, a=.1, b=.08, g=2. Then
$$
\dot q=-(1+gb)q+ga\lambda,\qquad
q^*(\lambda)=\frac{ga}{1+gb}\lambda,
$$
$$
\alpha=1.16,\qquad S_\lambda=ga/(1+gb)\approx0.172414.
$$
For a constant load ramp dot lambda=v and initial equilibrium state,
$$
q(t)-q^*(\lambda(t))=-\frac{S_\lambda v}{\alpha}(1-e^{-\alpha t}).
$$
If reserve and safety margins permit a tracking tolerance E=.02, the sufficient rate is v<=.13456 pu per second. This number is a didactic toy under an artificial first-order inverter, not an operational engineering speed limit.

See code/dynamic_ramp_demo.py.

## 6. Research significance / remaining gap

The mathematical objective is now two-dimensional in engineering meaning:
(i) how many additional MW can be *certifiably* hosted, and
(ii) how fast can a dynamic flexible-load scheduler safely move between hosted setpoints.

The quadratic / block-Hessian envelopes certify (i), while this conditional contraction argument supplies a route to (ii). A real 33-bus theorem still needs verified Jacobian/second-derivative bounds, nontrivial certified margins, Q limits, and numerical validation for fast renewable ramps or discontinuous disturbances.

Pantazis--Chong (arXiv:2608.11141v2) already develops all-time droop voltage certificates for a linearized network; merely adding a dynamic tube is not an independent originality claim. The potential contribution must be benchmarked on nonlinear line-current and hosting/ramp certification.
