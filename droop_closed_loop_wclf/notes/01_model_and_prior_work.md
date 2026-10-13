# Model and boundaries of the contribution

## Nonlinear radial model

Let n be the number of non-slack nodes; D is the descendant matrix, D_r=diag(r), D_x=diag(x), and
R=D^T D_r D, X=D^T D_x D,
M=D^T D_r(I-2D)D_r+D^T D_x(I-2D)D_x.
Let H_r=(D-I)D_r, H_x=(D-I)D_x. Squared voltages nu>0 and squared line currents ell>=0 are the algebraic state z=(nu,ell). On an **unsaturated fixed-gain voltage-magnitude** Q/V droop branch,

$$
p=p^0+w_p,\qquad
q=q^0+w_q-G(\sqrt{\nu}-V^{ref}),
$$

$$
a=Dp-H_r\ell,\qquad b=Dq-H_x\ell,
$$

$$
F(z,w)=
\begin{bmatrix}
\nu-\nu_{\rm slack}{\bf 1}-2Rp-2Xq-M\ell\\
\ell-(a\odot a+b\odot b)\oslash\nu
\end{bmatrix}=0.
$$

The denominator in the second row is the receiving-end squared voltage, consistent with the eliminated-flow version of DistFlow. All products, quotients, and roots of vectors are componentwise where appropriate. Realistic saturating Q/V control is **not** automatically differentiable at switching points.

Each independent uncertainty source obeys a half-disc set
$$
\Omega(C_j)=\{(w_{p,j},w_{q,j}):w_{p,j}\geq0,\ w_{p,j}^2+w_{q,j}^2\leq C_j^2\}.
$$

If a scaled family C_j=epsilon*c_j is used, define U=product Omega(c_j), w=epsilon*u, with nominal center w=0. w=0 is on the half-disc boundary but F may admit a smooth solution on an open neighborhood about 0; that smooth extension is part of the hypothesis.

## Two papers being combined — but not confused

**Sou et al. (IEEE TPS 2026)**: worst-case *algebraic* nonlinear DistFlow without inverter voltage-feedback dynamics as a decision-dependent closed loop; analytically bounds extrema of voltage and line current for uncertain power injections.

**Pantazis--Chong (arXiv:2608.11141v2)**: dynamic local/virtual droop, heterogeneous voltage certificates, forward invariance, and joint linear-program controller synthesis, all based on *linearized* DistFlow. It also handles sparse actuation. It does **not** give nonlinear DistFlow current extrema.

Our current question is a nonlinear **steady-state** worst-case current/voltage certificate in the presence of Q/V algebraic feedback; a proof of all-time safety for a real inverter requires an additional differential-algebraic invariant-set argument, not just the stationary enclosure.

## Mathematical route

Assume F_z(z,w) is nonsingular on a validated operating region and a unique smooth local branch z(w) is certified for every w in the uncertainty set. For current line i define f_i(w)=ell_i(w). We study the worst-case value max f_i over the full set, rather than controlling only its measured nominal value.

The first-order gradient of f_i is obtained from
$$
Dz(w)=-F_z(z(w),w)^{-1}F_w(z(w),w).
$$
The half-disc support function gives a candidate worst-case perturbation. The mathematical question is how far the true nonlinear maximum may lie above this candidate.

The cubic-gap theorem in the next note gives a finite explicit error constant if its nondegeneracy condition holds. A separate fallback is needed for degenerate gradients and near-loss-of-solvability cases.
