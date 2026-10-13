# A conditional O(epsilon^3) worst-case certificate for nonzero nominal flow

This note proves a new-to-this-project *conditional* mathematical proposition. It is not a literature priority claim, and the hypotheses should be verified for each nonlinear network before using the result as a certificate.

## 1. Support function and exact candidate

For c>0 define Omega(c)={(x,y): x>=0, x^2+y^2<=c^2}. For g=(a,b),
$$
\max_{u\in\Omega(c)}g^\top u=c\,h(a,b),\qquad
h(a,b)=\begin{cases}\sqrt{a^2+b^2},&a\geq0,\\|b|,&a<0.\end{cases}
$$

If a>=0 and g!=0, a maximizing u* is c*g/||g||. If a<0,b!=0, it is (0,c*sign(b)). The degenerate cases g=0 or a<0,b=0 have a non-unique maximizing face and must **not** be passed to the cubic theorem.

For U=product_j Omega(c_j), g=(g_1,...,g_m), construct u* by maximizing the linear form separately in every block.

## 2. Quadratic-growth inequality

For each nondegenerate block define
$$
\lambda_j=\begin{cases}
\|g_j\|_2,&(g_j)_p\geq0,\\
|(g_j)_q|,&(g_j)_p<0,\ (g_j)_q\ne0.
\end{cases}
\qquad
\kappa=\min_j\frac{\lambda_j}{2c_j}>0.
$$
Then for every u in U,
$$
g^\top(u_*-u)\geq\kappa\|u-u_*\|_2^2. \tag{1}
$$

Proof: for a>=0, u*=c*g/||g|| lies on the semicircle, and
g.(u*-u)=||g|| (c-(u*/c).u) >= ||g||/(2c)||u-u*||^2,
using ||u||<=c. For a<0,b!=0, u*=(0,sign(b)c) and
g.(u*-u)=(-a)x+|b|(c-sign(b)y) >= |b|/(2c)||u-u*||^2.
Summing and taking the minimum coefficient proves (1).

## 3. Cubic-gap proposition

Let f be C^2 on a convex open neighborhood of epsilon*U (epsilon>0). Let g=grad f(0), let u* maximize g.u on U, and assume (1) with kappa>0. Assume
$$
\sup_{w\in\epsilon U}\|\nabla^2 f(w)\|_2\leq M.
$$
Set R_U=sqrt(sum_j c_j^2). Then
$$
0\leq\max_{u\in U}f(\epsilon u)-f(\epsilon u_*)
\leq \frac{M^2R_U^2}{4\kappa}\epsilon^3. \tag{2}
$$

**Proof.** Write d=||u-u*|| and use the fundamental theorem of calculus along the segment between epsilon*u* and epsilon*u. Convexity keeps this segment inside epsilon*U. Since ||v||<=epsilon*R_U there, ||grad f(v)-g||<=M epsilon R_U. Hence
$$
f(\epsilon u)-f(\epsilon u_*)
\leq \epsilon g^\top(u-u_*)+M\epsilon^2R_U d
\leq-\epsilon\kappa d^2+M\epsilon^2R_Ud
\leq \frac{M^2R_U^2}{4\kappa}\epsilon^3.
$$
The lower inequality holds since epsilon*u* itself is feasible. QED.

The proof uses a Hessian bound, but does **not** require an explicit third derivative or zero base current.

If f(w)=ell_i(w) on a certified nonlinear closed-loop DistFlow branch, (2) turns **one evaluated candidate physical power flow per line** plus an explicit cubic correction into an upper bound on that line's true maximum squared current. This is not yet a bound on transients.

## 4. What fails when gradients degenerate

If a block has g_j=(0,0), or (g_j)_p<0 and (g_j)_q=0, kappa=0: its first-order maximizing set has positive dimension. The cubic claim is then unsupported. This is important in radial networks: a line might be insensitive to some sources at first order. Truly irrelevant blocks can be removed only if their influence vanishes for the full nonlinear function, not merely at nominal first order.

A generic **quadratic fallback** for all blocks is
$$
f(w)\leq f(0)+\epsilon\sum_j c_jh((g_j)_p,(g_j)_q)
+\frac12 M\epsilon^2R_U^2,
$$
valid for all w in epsilon U. This is weaker but needs no nondegeneracy.

## 5. Scope, scaling, and proof obligations

To claim O(epsilon^3) for a family epsilon->0, M and kappa must be bounded uniformly, with kappa bounded away from zero. If the nominal operating point or gradient depends on epsilon and kappa shrinks, the order can deteriorate.

- Error order concerns the *absolute worst-case squared-current value* (ell), not automatically relative current error.
- A floating-point estimate of M is not a mathematical certificate; use verified interval enclosures of F_z^-1 and derivative tensors.
- Multiple algebraic power-flow roots outside the verified operating box are not excluded.
- No novelty claim is made until comparison with existing robust Taylor and support-function techniques.
