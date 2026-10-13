# Capacity-first theorem: robust safety via quadratic certificates

**Status (2026-10-13):** the abstract inequality and its safe-inner-region conclusion are proved below. A certified implementation for actual 33-bus nonlinear DistFlow **remains open**: branch validity, inverter mode, and uniform Hessian norms need verified interval checks. The exact one-line example is a linear fixed-voltage toy, not a DistFlow certification.

## 1. Nonlinear control problem

For an unsaturated smooth normal-operation branch z=z(x,w), with controls x=(lambda,g), let
$$
p=p^0-\lambda d+w_p,\quad q=q^0-\lambda e+w_q-\operatorname{diag}(g)(\sqrt\nu-V^{ref}),\quad
F(z,x,w)=0.
$$
Consider safety-violation functions (all must be <=0)
$$
\phi_i^-(x,w)=\nu_i^{min}-\nu_i(x,w),\quad
\phi_i^+(x,w)=\nu_i(x,w)-\nu_i^{max},
$$
$$
\phi_l^I(x,w)=\ell_l(x,w)-\ell_l^{rated},\quad
\phi_i^S(x,w)=P_{inv,i}(x,w)^2+Q_{inv,i}(x,w)^2-S_i^2.
$$
Any additional loading/ramp constraints are separate. The inverter capability must be interpreted on an unsaturated branch; for a saturated branch replace the smooth Hessian argument by a piecewise/semismooth certified enclosure.

Let uncertainty w=epsilon*u where each u_j belongs to the right half disc Omega(c_j), independent across j. The product U is convex and ||u||^2<=R_U^2=sum_j c_j^2.

## 2. Quadratic robust-capacity inner-certificate theorem

Choose nominal x0, w0=0 and a **convex** trust region X of control settings. Assume for every (x,w) in X times epsilon U:

1. There is a specified smooth normal-operation solution branch z(x,w), with voltage squares bounded strictly above 0, and all control modes in the chosen smooth regime.
2. Each composite constraint phi_k(x,w) is twice continuously differentiable on an open convex neighborhood of X times epsilon U, with a **validated** Hessian bound
$$\sup_{(x,w)}\|\nabla^2_{(x,w)}\phi_k(x,w)\|_2\le M_k.$$

Write
$$
a_k=\nabla_x\phi_k(x_0,0),\quad
(b_{kj}^p,b_{kj}^q)=\nabla_{w_j}\phi_k(x_0,0)
$$
and h(a,b)=sqrt(a^2+b^2) for a>=0, |b| for a<0.

Then for every admissible disturbance, the robust constraint is implied by
$$
\boxed{
\Phi_k(\Delta x):=
\phi_k(x_0,0)+a_k^\top\Delta x
+\epsilon\sum_j c_j h(b_{kj}^p,b_{kj}^q)
+\frac12 M_k\bigl(\|\Delta x\|_2^2+\epsilon^2R_U^2\bigr)
\le0,
}
$$
where x0+Delta x belongs to X.

**Proof.** Apply multivariate Taylor's theorem about (x0,0) to the composite smooth function phi_k along the line segment to (x0+Delta x,epsilon u). The Hessian remainder is at most M_k/2 times the squared Euclidean length ||Delta x||^2+epsilon^2||u||^2. The uncertainty linear term maximizes blockwise over the independent half discs, giving the support functions. Bound ||u||^2 by R_U^2. Thus phi_k<=Phi_k for every u. QED.

Because M_k>=0, the safe *inner approximation* defined by all Phi_k<=0 is convex (intersection of convex quadratic sublevel sets), despite the nonlinear robust hosting problem not generally being convex. With a linear capacity objective max lambda and box constraints on g, this is a convex quadratically constrained program (or second-order-cone representable program). This convexity belongs to the **verified conservative region**, not the physical AC feasible set.

Units warning: load, gain and power-disturbance components may have very different numerical magnitudes. In computation normalize coordinates and form M with respect to those scaled variables. The plain Euclidean theorem remains true in whatever consistent coordinates are used.

## 3. Fixed gain => exact interval of the *certificate*

For g fixed, put s=lambda-lambda0 and
$$
\Phi_k(s)=c_k+a_k s+\frac12 M_k s^2,
$$
where
$$
c_k=\phi_k(x_0,0)+
\epsilon\sum_jc_jh(b_{kj}^p,b_{kj}^q)
+\frac12 M_k\epsilon^2R_U^2
$$
and a_k=partial_lambda phi_k(x0,0).

Every set {s: Phi_k(s)<=0} is an interval (possibly empty/unbounded). Their intersection with a preverified physical load domain is also an interval. For M_k>0 and discriminant a_k^2-2M_k c_k>=0, its endpoints are
$$
s_k^\pm=\frac{-a_k\pm\sqrt{a_k^2-2M_k c_k}}{M_k}.
$$
For M_k=0, solve the linear inequality instead. The final interval [lambdaL,lambdaU] is a **certified inner interval**, not necessarily the full robustly safe capacity set. The controller may have a safe positive-load region even when lambda=0 is unsafe (e.g. PV overvoltage). No monotonicity assumption or global bisection is required.

## 4. A precisely solvable thermal toy example

Take a fixed-voltage, lossless one-line approximation with
$$
p=\lambda-P-w_p,\quad q=w_q,\quad
\ell=p^2+q^2,
$$
P=0.30, C=0.05, I_max=0.20, (w_p,w_q) in Omega(C). This is a **linear/fixed-voltage toy**, not the complete nonlinear DistFlow.

For a=lambda-P, exact optimization of the current square gives
$$
\max_{w\in\Omega(C)}\ell=
\begin{cases}
(a-C)^2,&a<0,\\
a^2+C^2,&a\ge0.
\end{cases}
$$
Thus the exact robust thermal-feasible load interval is
$$
\boxed{\lambda\in[0.150000,\ 0.493649\ldots].}
$$
In particular lambda=0 is unsafe; added demand absorbs the PV export and initially *reduces* current.

Use expansion lambda0=P, w0=0, violation phi=ell-I_max^2. We have phi0=-0.04, dphi/dlambda=0, grad_w phi=0. The exact operator Hessian norm of phi with respect to (lambda,w_p,w_q) is M=4. With uncertainty radius C=.05,
$$
\Phi(\lambda)=-0.04+2(0.05)^2+2(\lambda-0.30)^2
=-0.035+2(\lambda-0.30)^2.
$$
It yields certified **inner** capacity interval
$$
\boxed{\lambda\in[0.1677124,\ 0.4322876].}
$$
This interval is a strict subset of the physical robust interval, quantifying the conservatism of an undifferentiated global Hessian. See code/certified_capacity_interval.py.

An operational conclusion: a capacity estimator that simply bisects between lambda=0 (unsafe) and a high lambda is not valid on this example. The certified interval can be computed directly from quadratic roots, and a better structured current bound can widen it.

## 5. Joint gain design: smooth second derivatives in g

For gain changes, the previous fixed-g Hessian formula requires the following **additional mixed terms**. For a total variation xi including delta nu and delta g,
$$
\delta q_\xi=\delta w_{q,\xi}-e\delta\lambda_\xi
-\operatorname{diag}\left(\frac g{2\sqrt\nu}\right)\delta\nu_\xi
-\operatorname{diag}(\sqrt\nu-V^{ref})\delta g_\xi.
$$
Its second variation along xi,eta is
$$
\boxed{
q_{\xi\eta}^{(2)}
=\operatorname{diag}\left(\frac g{4\nu^{3/2}}\right)
(\delta\nu_\xi\odot\delta\nu_\eta)
-\operatorname{diag}\left(\frac1{2\sqrt\nu}\right)
(\delta g_\xi\odot\delta\nu_\eta+
\delta g_\eta\odot\delta\nu_\xi).
}
$$
Substitute it in the existing residual formula (notes/06, eq. 2) to construct a valid Hessian bound for the **joint** optimization x=(lambda,g). Reusing a Hessian bound for fixed g without these terms would be incorrect.

## 6. Next proof obligations

- Get a practical, tight validated joint Hessian bound M_k for every safety constraint on 33-bus networks; the global-norm M may be overly conservative.
- Certify smooth network branch existence for all x,w in the trust region, and enforce PV inverter apparent-power capability. If limits switch, split into verified smooth regimes or use nonsmooth enclosures.
- Compare certified interval/convex controller optimum against the physical robust hosting bound on independently checked small feeders and larger radial cases, including computation time.
- Extension to *dynamic* controllable loads requires load state equations and transient/inverter DAE invariance. The current theorem is **quasi-static**, not a complete dynamic safety claim.
