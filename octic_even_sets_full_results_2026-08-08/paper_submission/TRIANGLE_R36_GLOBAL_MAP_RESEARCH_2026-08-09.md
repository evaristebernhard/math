# Residual-36: global six-quartic map route

Date: 2026-08-09

Status: **new structural reduction; not yet a closure theorem.**

## 0. Setup

In the residual-36 branch, two weight-64 even sets have the form
\[
Z_{AB}=A\sqcup B,\qquad Z_{AC}=A\sqcup C,
\]
with
\[
|A|=28,\qquad |B|=|C|=36.
\]
Their determinant nets are
\[
U=V_{AB},\qquad V=V_{AC},\qquad k=\dim(U\cap V).
\]
Each pair is a reduced transverse `CI(4,4,4)` and satisfies a symmetric determinant identity for the same octic.

Put
\[
Y=\operatorname{Bl}_A\mathbf P^3,\qquad D=4H-\sum_{a\in A}E_a.
\]
Then
\[
D^3=4^3-28=36>0.
\]
As in the residual-32 branch, the system `U+V` is base-point free on `Y`.

---

## 1. Common-pencil bound and the k=1 outlet

The common-pencil argument uses only `D^3>0` and the difference of the two ternary determinant quadrics. If `k=2`, then `dim(U+V)=4` and the corresponding map lands in a nonzero quadric surface in `P^3`, contradicting `D^3>0`. Hence
\[
\boxed{k\le1}.\tag{R36.1}
\]

For `k=1`, let the common quartic be `q`. The same three isotropic cases as in residual-32 occur.

1. Mixed isotropic/non-isotropic: the difference relation has rank five, while the image of each exceptional plane forces the quadric relation containing it to have rank at most four. Contradiction.
2. Both isotropic: if `q` is irreducible, UFD forces the two nets to coincide; if `q` is reducible, a linear or quadratic factor gives a contact plane/quadric and returns to the already excluded low-weight geometry.
3. Both non-isotropic: after completing squares,
   \[
   F=\lambda q^2+u_1u_2=\mu q^2+v_1v_2.
   \]
   Rank considerations force `lambda=mu`, then UFD gives
   \[
   u_1=ab,\quad u_2=cd,\quad v_1=ac,\quad v_2=bd,
   \]
   with
   \[
   \deg a=\deg d=\alpha,\qquad \deg b=\deg c=\beta,\qquad \alpha+\beta=4.
   \]
   The clean `(1,3)` decomposition has nominal complete-intersection lengths `4` and `36`, incompatible with a reduced common block of length `28` unless a lower-degree common component occurs. In the `(2,2)` case, restriction to a reduced quadric factor gives `F=lambda q^2` and hence a strict weight-48 contact quadric, contradicting the minimum-64 assumption.

Thus the **clean k=1 outlet is eliminated**, with only the usual reducible/nonreduced low-degree degenerations requiring explicit audit if promoted to the main paper.

The preferred global route is therefore `k=0`.

---

## 2. k=0 six-quartic map

Assume
\[
U\cap V=0,
\qquad W=U\oplus V,
\qquad \dim W=6.
\]
The difference of the two rank-three determinant forms is nondegenerate on `W`, defining a smooth quadric fourfold
\[
Q_0^4\subset\mathbf P^5.
\]
The six quartics define
\[
\phi:Y\longrightarrow X'\subset Q_0.
\]
Since `D^3=36`, the image is three-dimensional and `phi` is generically finite. Write
\[
X'\sim mH_{Q_0},\qquad e=\deg\phi.
\]
Then
\[
\boxed{2me=D^3=36,\qquad me=18}.\tag{R36.2}
\]

---

## 3. The general D^2-curve still has genus 33

For the blow-up of `P^3` at 28 points,
\[
K_Y=-4H+2\sum E_a.
\]
Using the standard intersection rules,
\[
K_Y\cdot D^2=-4\cdot16+2\cdot28=-8.
\]
Take general
\[
C=D_1\cap D_2,\qquad D_i\in|D|.
\]
Adjunction gives
\[
2g(C)-2=(K_Y+2D)\cdot D^2=-8+72=64,
\]
so
\[
\boxed{g(C)=33}.\tag{R36.3}
\]

If the target is normal and a general codimension-two linear section is smooth, then a curve section of `X'=(2,m)` has
\[
g(C')=(m-1)^2.
\]
The induced curve map has degree `e=18/m`. Riemann--Hurwitz therefore gives
\[
64=e\cdot 2m(m-2)+R
=36(m-2)+R,
\]
so
\[
\boxed{R=136-36m\ge0}.\tag{R36.4}
\]
Hence `m<=3`. The case `m=1` would put `X'` in a hyperplane of `P^5`, contradicting the six-dimensionality of `W`. Therefore the normal-target case reduces to exactly
\[
\boxed{(m,e)=(2,9)\quad\text{or}\quad(3,6)}.\tag{R36.5}
\]

This is the main new compression.

---

## 4. The quadratic-complex outlet (m,e)=(2,9)

Here
\[
X'=Q_0\cap Q_1\subset\mathbf P^5.
\]
Every exceptional plane `E_a` maps linearly to a maximal plane `L_a\subset Q_0` contained in `X'`.

Without assuming any transverse ramification order, a degree-nine generically finite map can have at most nine divisorial sheets over the generic point of one target plane. Hence 28 exceptional divisors produce at least
\[
\left\lceil\frac{28}{9}\right\rceil=4
\]
distinct maximal planes on `X'`.

Let
\[
T=Q_0^{-1}Q_1
\]
be the associated `Q_0`-self-adjoint operator. Common maximal planes are exactly invariant maximal isotropic three-spaces. If every pencil member had corank at most one, every primary block would be cyclic and there would be at most one invariant maximal isotropic three-space. Since at least four occur, the pencil contains
\[
\boxed{\operatorname{rank}Q_\lambda\le4}.\tag{R36.6}
\]

Thus the quadratic-complex outlet returns to the same rank-three/rank-four UFD factorization used in residual-32. In rank four,
\[
f_1f_2=f_3f_4,
\]
so
\[
f_1=ab,\quad f_3=ac,\quad f_2=cd,\quad f_4=bd,
\]
with
\[
\deg a=\deg d=\alpha,
\quad
\deg b=\deg c=\beta,
\quad
\alpha+\beta=4.
\]
The genuine new candidates are again
\[
\boxed{(\alpha,\beta)=(2,2)\text{ or }(1,3)}.\tag{R36.7}
\]

Unlike residual-32, the common block has length 28 rather than 32, so the `(2,2)` case does not enjoy the same two-sided `16+16` saturation. This mismatch may make the residual-36 quadratic-complex branch easier: any clean two-curve decomposition must lose four points somewhere, forcing either overlap, a contracted factor, or a lower-degree common component.

This is a primary target for the next audit.

---

## 5. The cubic-target outlet (m,e)=(3,6)

Here
\[
X'=Q_0\cap C_3\subset\mathbf P^5,
\qquad K_{X'}\simeq\mathcal O_{X'}(-1).
\]
The curve formula gives the exact ramification budget
\[
\boxed{R=136-108=28}.\tag{R36.8}
\]

Numerically this equals the number of exceptional planes. This suggests a rigid equality case: if each `E_a` contributes one simple transverse ramification to a general `D^2`-curve and there is no other divisorial ramification, then the entire ramification budget is exhausted by the 28 exceptional divisors.

Important audit warning: one must **not** read this directly from the divisor-class identity
\[
K_Y-\phi^*K_{X'}\sim\sum E_a.
\]
The residual-32 audit showed that linear equivalence alone does not determine the actual coefficient of the Jacobian ramification divisor along a prescribed exceptional component. The equality case must be established by a genuine local differential or finite-map argument.

If it is established, then each target plane can receive at most three simple ramified sheets in a degree-six cover, giving
\[
\#\{L_a\}\ge\left\lceil\frac{28}{3}\right\rceil=10.
\]
One would then reduce the cubic-target outlet to the projective geometry of a `(2,3)` threefold in `P^5` carrying at least ten distinguished planes coming from the exceptional divisors.

Thus the preferred question is:

> **R36 cubic equality problem.** Prove (or disprove) that in the normal `(2,3)` outlet the 28 exceptional planes account for all ramification of a general `D^2`-curve, each with simple transverse order.

A second route is to classify planes on `(2,3)` complete intersections and show that the required plane configuration is impossible even without exact ramification multiplicities.

---

## 6. Relation to the older J1/J2/Horrocks/QT analysis

The previous residual-36 work remains useful but should now be viewed as downstream structure, not the first reduction. In particular:

- J1 gives canonical-module gluing;
- J2 turns orientation noncoherence into degree-eight saturation defect;
- the coupled Beilinson--Horrocks theorem eliminates a genuine degree-0/1 coupled block;
- the QT/Smith material controls selected nonregular comparison carriers.

The new six-quartic route compresses the branch **before** those comparisons into two global image types `(2,9)` and `(3,6)`. The older comparison results can then be reinserted only inside the surviving image type where they are actually needed.

---

## 7. Current status and next actions

The accurate residual-36 picture is now:
\[
\boxed{
k\le1,
\qquad
k=1\text{ clean outlet essentially closed},
\qquad
k=0\Rightarrow
\begin{cases}
(m,e)=(2,9),\\
(m,e)=(3,6),
\end{cases}}
\]
under the normal-target/general-section hypotheses used in the curve argument.

Priority order:

1. Audit the `k=1` residual-36 proof, especially reducible/nonreduced common-quartic degenerations.
2. Analyze `(m,e)=(2,9)` rank-four `(2,2)/(1,3)` factorization with common-block length 28; test whether the missing four points force a low-degree carrier.
3. Analyze `(m,e)=(3,6)` via actual differential ramification, not divisor-class coefficients; exploit the exact curve budget `R=28`.
4. Keep nonnormal target as an explicit separate outlet.

Do not claim residual-36 closed until these outlets are eliminated.
