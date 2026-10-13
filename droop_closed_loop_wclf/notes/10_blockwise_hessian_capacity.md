# Structured-Hessian safe hosting: preserve load/disturbance coupling

This refines the capacity-first theorem in note 09. The mathematical bound is rigorous *if* its block-Hessian constants and the smooth normal-operation branch are validated over the entire region. The numerical toy uses an exact fixed-voltage current formula, not full nonlinear DistFlow.

## 1. A blockwise second-order theorem

Fix gain g, expand one smooth safety violation phi(lambda,w)<=0 about (lambda0,w0=0), with s=lambda-lambda0, w=epsilon*u, u in a product of right half-discs with R_U=sqrt(sum c_j^2). On the convex load/uncertainty parameter region suppose (compatible Euclidean operator norms)
$$
|\partial_{\lambda\lambda}^2\phi|\le B_{\lambda\lambda},\quad
\|\nabla_w\partial_\lambda\phi\|_2\le B_{\lambda w},\quad
\|\nabla_w^2\phi\|_2\le B_{ww},
$$
where B's are nonnegative **uniform** bounds.

The Hessian quadratic form along a segment is bounded above by
$$
B_{\lambda\lambda}s^2
+2B_{\lambda w}|s|\epsilon\|u\|_2
+B_{ww}\epsilon^2\|u\|_2^2.
$$
Integrating the second-order Taylor remainder and maximizing the first-order disturbance term using the independent half-disc supports yields, for every admissible w,
$$
\boxed{\phi(\lambda0+s,\epsilon u)\le
c+a s+\frac12 B_{\lambda\lambda}s^2
+B_{\lambda w}\epsilon R_U|s|,}
$$
$$
c=\phi(\lambda0,0)+\epsilon\sum_j c_j h(\partial_{w_{p,j}}\phi,\partial_{w_{q,j}}\phi)
+\frac12 B_{ww}\epsilon^2R_U^2,
\quad a=\partial_\lambda\phi(\lambda0,0).
$$
Every inequality on the right <=0 certifies the original robust constraint. Its left side is convex in s and can be solved exactly by considering the two halves s>=0 and s<=0 as separate quadratics; intersection over all voltage, thermal, and inverter reserve constraints remains an interval.

Compared with a full joint operator bound M, this retains the actual differences between load curvature, load--uncertainty coupling, and pure uncertainty curvature. For joint gain design, the same argument gives
$$
c+\nabla_x\phi^\top\Delta x+\tfrac12 B_{xx}\|\Delta x\|^2
+B_{xw}\epsilon R_U\|\Delta x\|\le0,
$$
where x=(lambda,g) and B_{xx}, B_{xw}, B_{ww} are appropriate uniform block operator-norm bounds. This is a convex second-order-cone representable sufficient constraint.

## 2. Exactly solvable line-current example

In the idealized fixed-voltage, lossless one-line toy:
$$
p=\lambda-P-w_p,\quad q=w_q,\quad \ell=p^2+q^2,\quad
\phi=\ell-I_{\max}^2.
$$
Take P=.30, C=.05, Imax=.20 and Omega(C). As shown in note 09, the exact robustly safe interval is
$$[.150000,\ .493649\ldots].$$
Expand at lambda0=P,w=0. The block Hessians are H_ll=2, H_lw=(-2,0), H_ww=2I, so
$$B_{\lambda\lambda}=B_{\lambda w}=B_{ww}=2.$$
The blockwise certificate reduces to
$$
-.0375+s^2+.1|s|\le0.
$$
Therefore its **certified inner interval** is exactly
$$[.150000,\ .450000].$$
The prior isotropic Hessian norm M=4 gave [.1677124,.4322876], so retaining Hessian blocks increases the safe inner interval.

This is still not the sharpest use of geometry. In the toy, the full second-order polynomial is known:
$$\phi=s^2-2s w_p+(w_p^2+w_q^2)-I_{\max}^2.$$
Maximizing its structured half-disc expression gives the **exact** two-regime worst-current formula and the wider [.15,.493649] physical interval. For real nonlinear DistFlow, reaching this sharpness may require a certified quadratic robust maximization, higher derivative bounds, or specialized affine-phasor support; a global block norm alone is generally conservative.

## 3. What should go into the actual controller

For every fixed (lambda0,g0), first certify a smooth nonlinear DistFlow branch over a trust region and the current/PV uncertainty set. Then compute:
- verified nominal safety violations and their gradients;
- separate block-Hessian constants (or tighter verified matrix envelopes), not merely one global norm;
- the intersection of all certified safe load intervals;
- additional gain movement with a convex conservative (lambda,g) constraint;
- a dynamic invariant-set / ramp-rate check before claiming real-time transient safety.

The desired engineering output is a **capacity range and proposed gain adjustment** with a mathematical safety guarantee; the Hessian is only a supporting ingredient.

## 4. Important proof limitation

The sign/shape of the *physical* robust current margin in nonlinear DistFlow is not proved convex. Only the **constructed sufficient certificate** is convex. Actual robust-feasible load levels might fall outside its interval. If the original steady-state certificate does not include a specified physical operating branch and relevant actuator limits, the computed capacity is not a safety guarantee.
