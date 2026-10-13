# Turning the cubic proposition into an explicit nonlinear DistFlow certificate

## 1. A uniform smooth solution branch is required

Take F(z,w)=0 from note 01 and a nominal root z0 at w=0. Let J0=F_z(z0,0). Construct a *validated* enclosing box Z containing z(w) for all w in epsilon U, and ensure nu>0 within Z. The uniform inverse-Jacobian condition and existence must be proved rather than inferred from finite samples.

One possible sufficient certificate uses a preconditioned map
$$
T_w(z)=z-PF(z,w),\quad P\approx J_0^{-1}
$$
and componentwise nonnegative L,b,r with
$$
|T_w(z_0)-z_0|\leq b,\quad
|I-PF_z(z,w)|\leq L,\quad b+Lr<r.
$$
The last condition with strictly positive r proves contraction in a weighted infinity norm and an invariant-box inclusion in exact arithmetic. Implement it with directed-rounding interval arithmetic (not plain float).

## 2. First and second implicit derivatives

For an admissible smooth solution z(w), write A=F_z(z(w),w), B=F_w(z(w),w). The first derivative is
$$
Dz=-A^{-1}B.
$$
For directions h,k in the uncertainty space:
$$
D^2 z[h,k]=-A^{-1}\big(
F_{zz}[Dz\,h,Dz\,k]+F_{zw}[Dz\,h,k]
+F_{zw}[Dz\,k,h]+F_{ww}[h,k]\big).
$$
Let e_i select line-current square ell_i out of z and f_i(w)=e_i^T z(w). Then
$$
D^2 f_i[h,k]=e_i^T D^2 z[h,k].
$$
If the following uniform bounds are available over Z times epsilon U:
$$
\|e_i^\top A^{-1}\|\leq a_i,\quad
\|A^{-1}B\|\leq K,\quad
\|F_{zz}\|\leq C_{zz},\quad
\|F_{zw}\|\leq C_{zw},\quad
\|F_{ww}\|\leq C_{ww},
$$
where tensor norms are induced bilinear norms compatible with the chosen vector norm, then
$$
M_i=a_i(C_{zz}K^2+2C_{zw}K+C_{ww})
$$
is a valid uniform bound on ||Hess f_i||. The conservative norm estimate may be replaced with a tighter row/block-wise interval Hessian bound.

This completes the *algebraic path* to M; an efficient machine-checked numerical implementation remains open.

## 3. How to get an inverse-Jacobian enclosure

If the box provides a verified bound ||I-PF_z||<=lambda<1 in a compatible induced operator norm, then
$$
F_z^{-1}=(PF_z)^{-1}P,\qquad
\|F_z^{-1}\|\leq \frac{\|P\|}{1-\lambda}.
$$
For selected row e_i one can use a tighter interval linear solve or bound ||e_i^T(PF_z)^{-1}P|| directly. The spectral radius alone does not bound a particular unweighted operator norm; keep norms consistent.

## 4. Physical constraints yet to be integrated

- Saturation: a clipped droop law is nonsmooth at its limits. Either certify a branch remains unsaturated or apply piecewise/semismooth enclosure tools. Do not assume classical Hessians across switching surfaces.
- Active-power-dependent reactive headroom: |Q_i|<=sqrt(S_i^2-P_i^2). The base model assumes fixed unsaturated gains.
- Dynamic safety: even a uniquely solvable nonlinear equilibrium for every w does not establish forward invariance of a first-order inverter control loop. A separate DAE/invariant-set argument is needed.
- Hosting-capacity maximization: safety feasibility along a load direction can be nonmonotone (increasing load may relieve PV overvoltage), so naive bisection is not a global-capacity guarantee.

## 5. Research sequence

1. Verify the second derivative formulas for a two-bus DistFlow model symbolically and with finite differences.
2. Implement a directed-rounding enclosure for F_z and the Hessian of ell_i.
3. Evaluate the cubic certificate for nonzero-base-flow lines; record failed kappa=0 blocks separately.
4. Compare against Sou et al.'s WCLF bounds, interval/Krawczyk, and general robust optimization using equal network inputs and wall-clock budgets.
5. Only then extend the steady-state envelope to inverter dynamic invariance and flexible-load hosting.
