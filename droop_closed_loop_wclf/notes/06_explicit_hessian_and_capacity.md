# Explicit nonlinear Hessian for robust load-hosting capacity

Status: mathematical derivation verified by a one-line numerical derivative test; **not** yet a globally certified IEEE-33-bus implementation. The purpose of this calculation is to bound hosting capacity, rather than develop a standalone Hessian method disconnected from operational constraints.

## 1. Put incremental load capacity in the closed-loop equations

For fixed (unsaturated) inverter gain G=diag(g_i), let incremental flexible load be parameterized by lambda>=0 with an active-power composition vector d>=0 and a reactive-power vector e. If sum_i d_i=1 in the chosen units, lambda measures total added active load.

$$
p=p^0-\lambda d+w_p,\qquad
q=q^0-\lambda e+w_q-G(\sqrt{\nu}-V^{ref}).
$$

For radial descendant matrix D and line impedance matrices D_r, D_x, put
$$
H_r=(D-I)D_r,\quad H_x=(D-I)D_x,\quad
a=Dp-H_r\ell,\quad b=Dq-H_x\ell.
$$
The nonlinear receiving-end eliminated DistFlow residual is
$$
F(z,w,\lambda)=
\begin{bmatrix}
\nu-\nu_s{\bf1}-2Rp-2Xq-M\ell\\
\ell-(a\odot a+b\odot b)\oslash\nu
\end{bmatrix},\qquad z=(\nu,\ell).
$$
All operations on vectors are componentwise unless explicitly written as matrix products.

This model is a **steady-state** algebraic droop feedback branch. It does not establish transient safety, saturation handling, or high-/low-voltage branch uniqueness beyond a certified box.

## 2. Explicit first derivative

Define T=diag(g_i/(2 sqrt(nu_i))). Then
$$
F_z=\begin{bmatrix}
I+2XT &-M\\
\operatorname{diag}((a^2+b^2)/\nu^2)+2\operatorname{diag}(b/\nu)DT&
I+2\operatorname{diag}(a/\nu)H_r+
2\operatorname{diag}(b/\nu)H_x
\end{bmatrix},
$$
$$
F_w=\begin{bmatrix}
-2R&-2X\\
-2\operatorname{diag}(a/\nu)D&
-2\operatorname{diag}(b/\nu)D
\end{bmatrix},\quad
F_\lambda=\begin{bmatrix}
2Rd+2Xe\\
2\operatorname{diag}(a/\nu)Dd+2\operatorname{diag}(b/\nu)De
\end{bmatrix}.
$$
On any smooth branch with nonsingular J=F_z,
$$
z_\lambda=-J^{-1}F_\lambda,\qquad z_w=-J^{-1}F_w.
$$
These are the local load-hosting and uncertainty sensitivities.

## 3. Explicit all-second-derivative formula

Use arbitrary directions xi=(delta nu_xi,delta ell_xi,delta w_p_xi,delta w_q_xi,delta lambda_xi) and eta analogously:
$$
\delta p_\xi=\delta w_{p,\xi}-d\,\delta\lambda_\xi,\quad
\delta q_\xi=\delta w_{q,\xi}-e\,\delta\lambda_\xi-T\delta\nu_\xi,
$$
$$
\delta a_\xi=D\delta p_\xi-H_r\delta\ell_\xi,\quad
\delta b_\xi=D\delta q_\xi-H_x\delta\ell_\xi.
$$
Only the voltage-square-root feedback contributes a nonlinear second derivative to q:
$$
q_{\xi\eta}^{(2)}=
\operatorname{diag}\!\left(\frac{g_i}{4\nu_i^{3/2}}\right)
(\delta\nu_\xi\odot\delta\nu_\eta),\quad
a_{\xi\eta}^{(2)}=0,\quad
b_{\xi\eta}^{(2)}=Dq_{\xi\eta}^{(2)}.
$$
Then
$$
F_{1,\xi\eta}^{(2)}=-2Xq_{\xi\eta}^{(2)}
$$
and for each current-square residual component:
$$
\begin{aligned}
F_{2,i,\xi\eta}^{(2)}
={}&-\frac2{\nu_i}
(\delta a_{i,\xi}\delta a_{i,\eta}
+\delta b_{i,\xi}\delta b_{i,\eta}
+b_i b_{i,\xi\eta}^{(2)})\\
&+\frac2{\nu_i^2}
[(a_i\delta a_{i,\xi}+b_i\delta b_{i,\xi})\delta\nu_{i,\eta}
+(a_i\delta a_{i,\eta}+b_i\delta b_{i,\eta})\delta\nu_{i,\xi}]\\
&-\frac{2(a_i^2+b_i^2)}{\nu_i^3}
\delta\nu_{i,\xi}\delta\nu_{i,\eta}.
\end{aligned}
$$

These formulas explicitly cover all blocks F_zz, F_zw, F_ww and F_zlambda, F_wlambda, F_lambdalambda, without manually expanding dense third-order tensors.

## 4. Uniform constructive Hessian bound

Let t=(w_p,w_q,lambda). Assume a verified state/parameter box with
nu_i>=nu_*>0, ||a||_infty<=A0, ||b||_infty<=B0.
Use spectral/Euclidean operator norms consistently. Set
$$
T_1=\frac{\|G\|_2}{2\sqrt{\nu_*}},\quad
T_2=\frac{\|G\|_2}{4\nu_*^{3/2}},
$$
$$
P_1=1+\|d\|_2,\quad Q_1=1+\|e\|_2+T_1,
$$
$$
A_1=\|D\|_2P_1+\|H_r\|_2,\quad
B_1=\|D\|_2Q_1+\|H_x\|_2,\quad
B_2=\|D\|_2T_2.
$$
For arbitrary total directions xi=(delta z,delta t), eta likewise, the directional first variations obey
||delta a_xi||_2<=A_1||xi||_2, ||delta b_xi||_2<=B_1||xi||_2,
and the quadratic correction obeys ||b_xieta^(2)||_2<=B_2||xi||||eta||.
Consequently the full second-derivative operator has a computable, conservative bound
$$
\|D^2F[\xi,\eta]\|_2\le C_F\|\xi\|_2\|\eta\|_2,\quad
C_F=\sqrt{(2\|X\|_2T_2)^2+C_2^2}
$$
with
$$
C_2=\frac{2}{\nu_*}(A_1^2+B_1^2+B_0B_2)
+\frac{4}{\nu_*^2}(A_0A_1+B_0B_1)
+\frac{2(A_0^2+B_0^2)}{\nu_*^3}.
$$
This norm estimate is not designed to be tight. It is useful because every quantity comes from a validated network box, not unknown true power-flow solutions.

Let K>=sup ||J^{-1}F_t||_2 over this box. For the extracted line-current-square response f_l(t)=ell_l(t), let alpha_l>=sup ||e_l^T J^{-1}||_2. Implicit differentiation yields
$$
D^2 z[h,k]=-J^{-1}D^2F[(z_t h,h),(z_t k,k)].
$$
Thus a constructive uniform Hessian bound is
$$
\boxed{\sup\|\nabla_t^2 f_l\|_2\le M_l:=\alpha_l C_F(1+K^2).}
$$
The same technique can bound selected squared-voltage rows. Sign-changing sensitivities are allowed. Replacing the global spectral bounds by linewise interval rows should strongly improve tightness.

For numerical *certification*, construct bounds on J^{-1} with an outward-rounded interval solve. For example if a fixed P and a validated box give ||I-PJ||<=gamma<1 in a compatible operator norm, then ||J^{-1}||<=||P||/(1-gamma), while tighter row-specific alpha_l requires an additional bound. Do not use the spectral radius in place of an induced norm without a justification.

## 5. How M enters the actual capacity theorem

For each fixed lambda and gain G, suppose w=epsilon u, u in a product of independent half-discs, and that the physical closed-loop branch is certified for all w. Let f_l(w)=ell_l(lambda,w), g_l=grad_w f_l(0). If the first-order half-disc maximizer u_l* is nondegenerate with quadratic-growth kappa_l>0, then note 02 establishes
$$
\max_w \ell_l(\lambda,w)
\le
\ell_l(\lambda,\epsilon u_l^*)+
\frac{M_{l,w}^2 R_{\mathcal U}^2}{4\kappa_l}\epsilon^3.
$$
Here M_{l,w} may be bounded by the uniform Hessian in section 4, keeping lambda fixed. This is a **certified sufficient** thermal constraint if the nominal physical point and Hessian bounds are themselves verified. Degenerate lines must use the second-order fallback or a different safe enclosure.

The next note defines a mathematically correct hosting-capacity and ramping search based on these certificates.
