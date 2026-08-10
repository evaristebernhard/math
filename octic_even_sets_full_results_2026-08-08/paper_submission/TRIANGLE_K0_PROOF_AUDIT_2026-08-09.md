# Residual triangle k=0: proof audit

Date: 2026-08-09

## Verdict

The proposed k=0 closure is **not yet promotable to `main.tex` as a closed theorem**.  The downstream Segre/toric analysis is largely sound, but the upstream assertion

\[
\boxed{r_a=2\text{ for every exceptional plane }E_a}
\]

has not been proved.  The previous argument read this ramification order from the coefficient of `E_a` in the divisor-class identity

\[
K_Y-\phi^*K_{X'}\sim(3-m)D+\sum E_a,
\]

but a linear-equivalence identity does **not** determine the actual coefficient of the Jacobian/relative-canonical divisor along a fixed exceptional component.  Nonexceptional strict transforms can change the exceptional coefficients while preserving the divisor class.

Consequently the deductions

\[
r_a=2\Rightarrow m\le3\Rightarrow (m,e)=(2,8)
\]

and then

\[
32\text{ exceptional planes}\Rightarrow\ge8\text{ distinct target planes}
\]

are not currently justified.

---

## 1. Local check: determinant-node geometry alone does not force r=2

Locally normalize a node to

\[
q(a,b,c)=ac-b^2.
\]

There are nonlinear local automorphisms preserving `q` and tangent to the identity.  For example, using the unipotent `SL_2` action with parameter `t=c`,

\[
(a,b,c)\longmapsto
\bigl(a+2bc+c^3,\ b+c^2,\ c\bigr)
\]

satisfies exactly

\[
(a+2bc+c^3)c-(b+c^2)^2=ac-b^2.
\]

Hence two transverse determinant triples defining the same ordinary double point can agree to first order but differ already in quadratic order.  After blowing up the common zero, this gives a nonzero first transverse derivative of the combined six-section map.  Thus the local determinant identity by itself does not force second-order transverse ramification.

This does not construct a global octic counterexample, but it proves that any proof of `r_a=2` must use genuinely global information, not merely the two local determinant presentations of the node.

---

## 2. Parts that survive the audit

### 2.1 Positive-dimensional family of common planes

For

\[
Q_0\simeq\operatorname{Gr}(1,\mathbf P^3),
\]

a positive-dimensional family of maximal planes contains an irreducible parameter curve `Gamma`.  The union of the corresponding alpha-planes is the Chow divisor of lines meeting `Gamma`, of class

\[
(\deg\Gamma)H.
\]

If this divisor is contained in the irreducible threefold `X'\sim2H`, equality of divisors forces `deg Gamma=2`.  For a plane conic the Chow equation is a quadratic form in only three Pluecker coordinates, hence has rank at most three.  Thus, **once `X'` is known to be a quadratic complex**, a positive-dimensional plane family forces a rank-<=3 pencil member.

### 2.2 Finite invariant-Lagrangian count

For a self-adjoint operator `T=Q_0^{-1}Q_1`, common maximal planes are the `T`-invariant maximal isotropic three-spaces.  The primary decomposition reduces the finite count to nilpotent self-adjoint primary blocks of dimensions 2,4,6.

An exact Grassmann-chart computation of

\[
NL\subset L,\qquad Q_0|_L=0
\]

for every Jordan partition gives the finite maxima

\[
2,\qquad3,\qquad4
\]

in dimensions 2,4,6.  Therefore the global finite number is at most

\[
\max\{4,3\cdot2,2^3\}=8.
\]

Equality is possible only for three distinct two-dimensional semisimple primary components, giving Segre type

\[
[(11)(11)(11)]
\]

and the toric normal form

\[
x_1y_1=x_2y_2=x_3y_3.
\]

This agrees with Avritzer--Gonzalez-Sprinberg--Pan, Example 4.15, which explicitly lists eight planes for this Segre type.

### 2.3 Toric factor/atom analysis

Conditional on reaching the degree-eight toric cover

\[
\deg\phi=8,
\qquad
x_1y_1=x_2y_2=x_3y_3,
\]

the later factor analysis is consistent:

* degree saturation over each of the eight target planes forces any extra atom divisor not to dominate that plane;
* for a contracted irreducible factor `S=(G=0)` of degree `d`, projection formula gives
  \[
  D^2\widetilde S=0
  \Rightarrow
  16d=\sum_{p\in A\cap S}\operatorname{mult}_pS;
  \]
* singular `A`-points of one atom all map their exceptional planes to the same toric target plane, so under the degree-eight / ramification-two hypothesis there are at most four such points, yielding `d<=2`;
* linear factors contradict the toric line-incidence bound; quadratic factors return to the already-closed quadratic carrier;
* the same reasoning handles factors common to both members of one toric coordinate pair.

Thus the toric downstream argument is reusable once the upstream covering multiplicities are established.

---

## 3. Independent correction: what can be proved without r=2

Take a general complete-intersection curve

\[
C=D_1\cap D_2\subset Y,
\qquad D_i\in|D|.
\]

One computes

\[
D^3=32,
\qquad
K_Y\cdot D^2=0,
\qquad
g(C)=33.
\]

If `X'\sim mH_Q` and `e=deg(phi)`, then `me=16`.  A general codimension-two linear section `C'` of `X'` has arithmetic genus

\[
g(C')=(m-1)^2.
\]

When the induced curve map is between smooth normal sections, Riemann--Hurwitz gives

\[
64=e\,2m(m-2)+R
=32(m-2)+R,
\]

hence

\[
R=32(4-m)\ge0,
\qquad m\le4.
\]

Thus a normalization/curve argument can at least reduce the possible image degree to

\[
m\in\{1,2,4\},
\]

with `m=1` still excluded by linear independence.  The unresolved alternative is therefore essentially

\[
\boxed{m=4,e=4}
\]

plus, in the `m=2,e=8` case, the possibility that some exceptional planes have transverse order `1` rather than `2`.

This is a more accurate upstream gap than the old broad `K0-LD return`.

---

## 4. What is needed for a genuine closure

Any one of the following would repair the proof:

1. a global theorem forcing every `E_a` to have transverse order at least `2`;
2. a global argument excluding the `m=4,e=4` image and proving enough ramification in the `m=2,e=8` case to force eight distinct maximal planes;
3. a direct use of the full three-net structure `U\oplus V\oplus T` that bypasses the ramification claim and still forces the toric eight-plane model (or a lower-degree carrier).

Until one of these is proved, `main.tex` should continue to state residual 32 as not fully closed.

## 5. Submission action

Do **not** insert the proposed k=0 closure theorem into `main.tex` yet.  Keep the already-proved `k=1` closure and the existing statement that `k=0` is reduced to a concentrated comparison problem, but update the research notes so the precise remaining interface is the exceptional-plane ramification / image-degree step above.
