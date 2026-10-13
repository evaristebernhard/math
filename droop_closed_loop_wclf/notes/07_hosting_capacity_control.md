# Hosting-capacity control is the primary problem

## 1. Formal distinction: true robust capacity vs certified capacity

Fix one active-load direction d>=0 (sum d_i=1) and reactive composition e, and choose an inverter gain vector g. Let S_g(lambda,w) be the chosen verified normal-operating closed-loop branch of nonlinear DistFlow. Let \mathcal U be the full renewable/load uncertainty set.

A load setting lambda is physically *robustly safe* if for **all** w in \mathcal U, with the branch well-defined:
$$
\nu^{min}_i\le\nu_i(\lambda,g,w)\le\nu^{max}_i,\quad
\ell_l(\lambda,g,w)\le\ell_l^{rated},\quad
P_{inv,i}^2+Q_{inv,i}^2\le S_{inv,i}^2.
$$
The last condition must be checked across the entire uncertainty set, including active-power-dependent Q headroom, not only at the nominal condition.

Let C_true(g) be this set of lambdas. For each lambda our analytic / validated numerical enclosures can produce upper and lower bounds:
$$
\nu_i^L(\lambda,g)\le\inf_w\nu_i(\lambda,g,w),\qquad
\nu_i^U(\lambda,g)\ge\sup_w\nu_i(\lambda,g,w),
$$
$$
\ell_l^U(\lambda,g)\ge\sup_w\ell_l(\lambda,g,w).
$$
Let C_cert(g) be the set of lambda for which the verified envelopes satisfy all safety constraints, including inverter capacity. Then
$$
\boxed{C_{\rm cert}(g)\subseteq C_{\rm true}(g).}
$$
This inclusion, rather than matching the true optimal capacity, is the key operational guarantee.

For a fixed g, define pointwise hosting capacity and certified pointwise hosting capacity
$$
\Lambda_{\rm point}^{true}(g)=\sup C_{\rm true}(g),\qquad
\Lambda_{\rm point}^{cert}(g)=\sup C_{\rm cert}(g).
$$
Then Lambda_point^cert <= Lambda_point^true (provided both sets are defined over the same compact search domain).

## 2. Safe load RAMP is a different control objective

A load may **reduce PV overvoltage at first** and **cause undervoltage/overcurrent later**. Therefore the safe set is not necessarily an initial interval [0,Lambda]. It can even be empty near lambda=0.

If current lambda_0 is certified safe, define a continuously reachable safe upward ramp capacity by
$$
\Lambda_{\rm ramp}^{cert}(\lambda_0,g)=
\sup\{L\ge\lambda_0:[\lambda_0,L]\subseteq C_{\rm cert}(g)\}.
$$
Then Lambda_ramp^cert <= Lambda_point^cert if lambda_0>=0 and the latter exists.

Inverter dynamics introduce more restrictions: even if the **steady-state** ramp set is safe, a real-time ramp of load may excite a transient overshoot. The load slew rate and the inverter DAE invariant-box conditions must be analyzed separately before claiming real-time dynamic safety.

## 3. Capacity-aware derivative signs and when bisection is justified

From note 06,
$$
z_\lambda=-F_z^{-1}F_\lambda.
$$
If verified interval enclosures show d nu_i/d lambda <=0 uniformly for all w and lambda in the capacity interval, then:
- the robust minimum voltage is nonincreasing in lambda, so undervoltage feasibility has prefix structure;
- the robust maximum voltage is nonincreasing, so *overvoltage* feasibility has suffix structure (more load can remedy overvoltage).
If also d ell_l/d lambda >=0 uniformly, robust maximum currents are nondecreasing; thermal feasibility has prefix structure.

These are **sufficient**, not necessary, conditions. Their intersection may be a middle interval, not a prefix starting at zero. If any sign is unverified, using a single global bisection for feasible capacity is unjustified. A flexible-load controller cannot treat safety as an assumed monotone predicate.

## 4. Certified one-dimensional search for capacity

For a fixed gain vector, cover lambda in a compact physical interval [0, lambda_max] by parameter subintervals I.
- SAFE: validate a joint enclosure for **all lambda in I** and all w; if every constraint passes, I belongs to C_cert.
- UNSAFE: validate a *single feasible witness disturbance* w* whose unique physical solution violates some limit for **every lambda in I**; then I is disjoint from C_true.
- UNKNOWN: bisect I and repeat, preserving an unresolved list.

For terminal global-capacity certification, unresolved intervals must be controlled: unless every interval above a candidate is proved UNSAFE, a numerical grid of feasible points **cannot** prove a globally maximal capacity. In practice one can report a certified lower bound on feasible capacity and a separate upper search bracket, conditioned on verified coverage. Safe but disconnected intervals may exist.

To optimize gain g as well, use an outer design search with its own parameter enclosures or explicitly report a finite-gain shortlist instead of a global optimality claim.

## 5. Relating analytic worst-case bounds to capacity safety

For line l, the nondegenerate cubic proposition yields a sufficient condition
$$
\ell_l(\lambda,\epsilon u_l^*)+
(M_{l,w}^2 R_{\mathcal U}^2/(4\kappa_l))\epsilon^3
\le \ell_l^{rated}.
$$
For each bus's highest voltage use the same proposition with f=nu_i; for its minimum use f=-nu_i. If the maximizer is degenerate, replace the cubic correction by the general quadratic Taylor upper bound, or an independent interval enclosure.

The resulting constraints define a *certified control admissibility region* in (lambda,g), not just a better plotting of current profiles. This keeps the research focused on hosting capacity.

## 6. Future dynamic flexible-load problem

Only after the steady-state certification is successful, discretize time t and optimize charging/load trajectories lambda_t (or full vectors u_{i,t}) with energy requirements, ramp constraints, and robust safety envelopes. Distinguish instantaneous algebraic certification from all-time DAE safety during transitions; the Pantazis--Chong 2026 paper handles all-time certificates for a different, linearized DistFlow controller and must not be cited as proving nonlinear DAE safety here.
