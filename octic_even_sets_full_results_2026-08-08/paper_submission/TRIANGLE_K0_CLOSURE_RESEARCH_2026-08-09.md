# Residual triangle: k=0 six-quartic outlet — closure research

Date: 2026-08-09

Status after proof audit: **NOT CLOSED.**  The downstream finite-plane Segre count and toric factor analysis survive, but the upstream step reading the transverse ramification order `r_a=2` from the divisor-class identity for `K_Y-phi^*K_{X'}` is not justified.  See `TRIANGLE_K0_PROOF_AUDIT_2026-08-09.md`.  Until a global ramification/image-degree argument repairs this step, this file must not be cited as an unconditional closure of `k=0`.

---

## 0. Setup

In the residual-triangle configuration

\[
Z_{AB}=A\sqcup B,\qquad Z_{AC}=A\sqcup C,\qquad Z_{BC}=B\sqcup C,
\qquad |A|=|B|=|C|=32,
\]

let

\[
U=V_{AB},\qquad V=V_{AC},\qquad k=\dim(U\cap V).
\]

The common-pencil theorem gives `k<=1`, and the `k=1` branch has already been closed directly.  Assume from now on

\[
\boxed{k=0.}
\]

Then

\[
W=U\oplus V,\qquad \dim W=6.
\]

On

\[
Y=\operatorname{Bl}_A\mathbf P^3,\qquad
D=4H-\sum_{a\in A}E_a,
\]

the six quartics in `W` are base-point free.  The difference of the two determinant quadrics is nondegenerate, hence defines a smooth quadric fourfold

\[
Q_0^4\subset\mathbf P^5.
\]

The six-quartic map

\[
\phi:Y\longrightarrow X'\subset Q_0
\]

is generically finite, and the already-audited J3 conductor/degree calculation gives

\[
\boxed{X'=Q_0\cap Q_1,\qquad \deg\phi=8.}\tag{K0.1}
\]

Every exceptional plane `E_a` maps linearly to a maximal plane `L_a\subset X'`.  Its transverse ramification index is `2`, so at most four exceptional planes can map to a fixed target plane.  Therefore

\[
\boxed{X'\text{ contains at least eight distinct maximal planes.}}\tag{K0.2}
\]

The task is to show that this is impossible unless the configuration returns to the already-closed plane/quadratic carrier geometry.

---

## 1. Positive-dimensional families of common planes force a rank <=3 pencil member

This outlet can be removed geometrically, without a Hilbert-vector classification.

Identify the smooth quadric fourfold with the Klein quadric

\[
Q_0\simeq \operatorname{Gr}(1,\mathbf P^3).
\]

Its maximal planes come in two rulings:

- `alpha_p`: all lines through a point `p\in P^3`, parametrized by `P^3`;
- `beta_H`: all lines contained in a plane `H\subset P^3`, parametrized by the dual `P^{3*}`.

Suppose a positive-dimensional family of alpha-planes is contained in `X'`.  Choose an irreducible curve `Gamma` in the parameter space.  The union of the corresponding planes is

\[
D_\Gamma=\{\ell\in\operatorname{Gr}(1,3):\ell\cap\Gamma\ne\varnothing\}.
\]

This is the Chow divisor of `Gamma`; in `Pic(Q_0)=Z H` one has

\[
[D_\Gamma]=(\deg\Gamma)H.
\]

But `D_\Gamma\subset X'`, and both are three-dimensional divisors in the irreducible fourfold `Q_0`.  Since

\[
[X']=2H,
\]

we must have

\[
D_\Gamma=X',\qquad \deg\Gamma=2.
\]

Thus `Gamma` is a conic (with reducible/nonreduced degree-two limits allowed).  Put its plane in coordinates `x_3=0`.  If

\[
q(x_0,x_1,x_2)=0
\]

is the conic equation, the Chow equation for lines meeting `Gamma` is, in Pluecker coordinates,

\[
q(p_{03},p_{13},p_{23})=0.
\]

Hence the corresponding quadric in `P^5` has rank at most `3`.  Since it cuts the same divisor on `Q_0` as `Q_1`, it differs from `Q_1` by a scalar multiple of `Q_0`.  Therefore the pencil contains a member of rank at most `3`.

The beta-ruling case is dual.  We obtain:

\[
\boxed{\text{positive-dimensional common-plane family}\Longrightarrow
\text{a pencil member of rank }\le3.}\tag{K0.3}
\]

So the positive-family outlet is absorbed by the rank <=3 analysis below.

---

## 2. Rank <=2 is impossible; rank 3 returns to the quadratic carrier

### 2.1 Rank <=2

Over an algebraically closed field of characteristic different from `2`, a quadratic form of rank at most `2` is a square or a product of two linear forms.  Substituting the six linearly independent quartic sections would then force a nonzero linear combination of them to vanish identically in the integral polynomial ring.  This contradicts `dim W=6`.

Hence only rank `3` must be treated.

### 2.2 Rank 3 UFD normal form

After a linear change of coordinates in `W`, a rank-three relation is

\[
f_0f_2=f_1^2.
\]

Unique factorization gives

\[
f_0=ha^2,\qquad f_1=hab,\qquad f_2=hb^2,
\qquad \deg h+2\deg a=4.\tag{K0.4}
\]

The possibility `deg a=0` makes `f_0,f_1,f_2` proportional and is impossible.  Thus there are two cases.

#### Case A: `h` is constant

Then `a,b` are quadrics.  Since every section in `W` vanishes at every point of `A`,

\[
a|_A=b|_A=0.
\]

Hence `A` lies on a quadric.  A nonzero quadric is either reduced (including a cone or a union of two planes), in which case this is the already-closed quadratic carrier branch, or a double plane, in which case `A` lies on a plane, already impossible by nefness.

#### Case B: `deg h=2` and `a,b` are linear

Let `Pi` be the radical plane of the rank-three quadric in `P^5`.

Suppose `p\in A` but `h(p)\ne0`.  Since `f_0(p)=f_2(p)=0`, one has

\[
a(p)=b(p)=0.
\]

Then

\[
df_0(p)=df_1(p)=df_2(p)=0.
\]

Therefore the exceptional plane `E_p` is mapped by first jets entirely into `Pi`.  Since `E_p` maps linearly onto a plane, its image is exactly `Pi`.  In particular

\[
\Pi\subset Q_0,
\]

and hence `Pi\subset X'`.  But the rank-three pencil member is singular along `Pi`; consequently the complete intersection `X'` is singular in codimension one along `Pi`, so `Pi` is contained in the normalization conductor.

This contradicts the same J3 conductor-sign calculation already used in deriving (K0.1): the actual coefficient of `E_p` in

\[
K_Y-\phi^*K_{X'}=D+\sum_{a\in A}E_a
\]

is `+1`, while a divisor dominating the conductor has local coefficient

\[
(r-1)-rc\le-1.
\]

Therefore no such `p` exists.  Thus

\[
\boxed{A\subset(h=0).}
\]

If `h` is reduced, this is the already-closed quadratic carrier.  If `h=\ell^2`, all `A` lies in the plane `(\ell=0)`, impossible.

Hence

\[
\boxed{\operatorname{rank}\le3\text{ is completely returned to the closed low-degree branch}.}\tag{K0.5}
\]

Combined with Section 1, this also closes the positive-dimensional common-plane outlet.

---

## 3. Finite-plane rank-4 case and the classical Segre lemma

Assume now:

1. the common maximal planes of `X'` form a finite set;
2. the pencil has no rank <=3 member.

The finite-plane statement can in fact be proved directly by self-adjoint linear algebra; the classical Segre classification is only a useful cross-check.

Let

\[
T=Q_0^{-1}Q_1.
\]

Common maximal planes are exactly `T`-invariant maximal `Q_0`-isotropic 3-spaces.  The primary decomposition

\[
V=\bigoplus_\lambda V_\lambda
\]

is `Q_0`-orthogonal and each `V_\lambda` is nondegenerate.  If `L` is an invariant maximal isotropic 3-space, the spectral projectors (polynomials in `T`) preserve `L`, so

\[
L=\bigoplus_\lambda (L\cap V_\lambda).
\]

Since

\[
\dim(L\cap V_\lambda)\le\left\lfloor\frac{\dim V_\lambda}{2}\right\rfloor
\]

and the sum is `3`, every nonzero primary dimension must be even and `L\cap V_\lambda` is maximal isotropic in `V_\lambda`.

It therefore suffices to count invariant Lagrangians in a single primary component of dimensions `2,4,6`.  Put `N=T-\lambda I`.  In the standard self-adjoint Jordan normal form (each Jordan block paired with the reverse-identity Gram matrix), solving `NL\subset L` together with `Q_0|_L=0` gives the following complete finite table:

\[
\begin{array}{c|c|c}
\dim V_\lambda&\text{Jordan partition}&\#\{N\text{-invariant maximal isotropics}\}\\\hline
2&(2)&1\\
2&(11)&2\\\hline
4&(4)&1\\
4&(31)&2\\
4&(22)&3\\
4&(211)&2\\
4&(1111)&\infty\\\hline
6&(6)&1\\
6&(51)&2\\
6&(42)&3\\
6&(411)&2\\
6&(33)&4\\
6&(321)&2\\
6&(3111),(222),(2211),(21111),(111111)&\infty.
\end{array}\tag{K0.10}
\]

The finite entries can be checked directly in the canonical block basis.  In particular, for two Jordan blocks of sizes `a>=b` the count is `b+1`; the remaining finite three-block cases `(211),(411),(321)` have two solutions.  The displayed infinite cases contain a positive-dimensional family of invariant isotropics, already absorbed by Section 1.

Consequently a finite global invariant-plane set has size at most

\[
\max\{4,\ 3\cdot2,\ 2^3\}=8.\tag{K0.11}
\]

Moreover equality `8` is possible only for three distinct two-dimensional primary components, each of type `(11)`.  Thus `T` is semisimple with three distinct eigenvalues, each of multiplicity two.  Choosing a hyperbolic basis `(x_i,y_i)` in each primary component gives

\[
Q_0=x_1y_1+x_2y_2+x_3y_3,
\qquad
Q_1=\lambda_1x_1y_1+\lambda_2x_2y_2+\lambda_3x_3y_3.
\]

After replacing the two generators of the pencil, the intersection has the toric normal form

\[
\boxed{x_1y_1=x_2y_2=x_3y_3.}\tag{K0.12}
\]

Its eight maximal planes are obtained by choosing one isotropic line from each hyperbolic two-space.  This is exactly the classical Segre type `[(11)(11)(11)]`; Avritzer--Gonzalez-Sprinberg--Pan, Example 4.15, lists the same eight planes.

By (K0.2), the finite case therefore has exactly eight planes and is toric.

---

## 4. Toric factorization: dominant atoms are impossible

Write the pullback toric identities as

\[
X_1Y_1=X_2Y_2=X_3Y_3=:P_8.\tag{K0.6}
\]

Factor the common degree-eight product in the UFD `k[x_0,x_1,x_2,x_3]`.  If an irreducible factor chooses one member from each pair `(X_i,Y_i)`, it determines a cube pattern `epsilon\in{0,1}^3`; call such a factor an atom `G_epsilon`.  On `(G_epsilon=0)` the map lands in the corresponding toric coordinate plane `L_epsilon`.

There are exactly eight common target planes.  Since there are 32 exceptional planes, each target plane must receive exactly four of them.  Each exceptional plane contributes transverse local degree `2`, so the generic degree over each target plane is already

\[
4\cdot2=8=\deg\phi.
\]

Therefore no nonexceptional divisor can dominate any `L_epsilon`.  Hence:

\[
\boxed{\text{every atom divisor is contracted to a curve or a point}.}\tag{K0.7}
\]

This replaces the old informal `relative-contact` assertion by a degree-saturation statement.

---

## 5. Contracted atoms have degree <=2 and are impossible or quadratic

Let `G` be an irreducible atom of degree `d`, and let `S=(G=0)`.  Since `S` is contracted to dimension at most one,

\[
D^2\cdot\widetilde S=0.
\]

Thus

\[
16d=\sum_{p\in A\cap S}\operatorname{mult}_p(S).\tag{K0.8}
\]

A singular `A`-point of `S` has multiplicity at least `2`.  At such a point the three toric coordinates divisible by `G` have zero first jet, so the exceptional plane maps to the opposite coordinate plane.  At most four exceptional planes map to any fixed target plane.  Hence `S` can be singular at at most four points of `A`.

Since `mult_p(S)\le d`,

\[
16d\le 28+4d,
\]

and therefore

\[
\boxed{d\le2.}\tag{K0.9}
\]

### 5.1 `d=1`

Then `S` is a plane and (K0.8) gives exactly `16` points of `A` on `S`.  The restricted base-point-free system has square zero, hence maps the blown-up plane to a curve.  Every exceptional curve over one of these 16 points has degree one under `D`, so the image curve must be a line `ell\subset L_epsilon`, and all sixteen corresponding exceptional planes `L_p` contain `ell`.

In the toric eight-plane configuration, a line is contained in at most two of the eight maximal coordinate planes.  Since each target plane receives at most four exceptional planes, at most

\[
2\cdot4=8
\]

exceptional planes can contain `ell`, contradicting `16`.

So a contracted linear atom is impossible.

### 5.2 `d=2`

If `S` is smooth, (K0.8) gives all `32` points of `A` on the quadric, returning to the already-closed quadratic carrier.

If `S` is an irreducible quadric cone and its vertex is an `A`-point, the vertex contributes multiplicity `2`, so (K0.8) leaves `31` distinct `A`-points on `S`, at least `30` of them smooth.  As above, the contracted image is then a line and at least 30 exceptional image planes contain it, contradicting the `2\times4=8` bound.

Thus every degree-two contracted atom either returns to the closed quadratic branch or is impossible.

Consequently **no nonconstant atom survives**.

---

## 6. Common-component factors are also closed

The atom decomposition may degenerate if an irreducible factor `G` divides both `X_i` and `Y_i` for some `i`.  From

\[
X_1Y_1=X_2Y_2=X_3Y_3
\]

it then divides at least one member of each of the other two pairs.  Hence on `S=(G=0)` at least four of the six toric coordinates vanish identically, so

\[
\dim\phi(S)\le1.
\]

If `S` were singular at an `A`-point, those four coordinate sections would all have zero first jet, leaving at most two independent first jets, contradicting the fact that every `E_p` maps to a plane.  Thus every `A`-point on `S` is a smooth point of `S`, and

\[
16d=|A\cap S|\le32.
\]

Therefore `d<=2`.

- `d=2` forces `|A\cap S|=32`, hence the quadratic carrier.
- `d=1` gives a plane through 16 points whose image is a line.  The same `2\times4=8` target-plane count contradicts the existence of 16 exceptional image planes containing that line.

Thus common-component / nonreduced toric degenerations do not create a new outlet.

---

## 7. Current logical status of k=0

The old list

- rank <=3 member;
- positive-dimensional common-plane family;
- non-dominant atom;
- nonreduced/common-component degeneration

is no longer a genuine open collection:

\[
\boxed{
\begin{aligned}
\text{positive family}&\Rightarrow\operatorname{rank}\le3,\\
\operatorname{rank}\le3&\Rightarrow\text{plane/quadratic carrier},\\
\text{contracted atom}&\Rightarrow d\le2\Rightarrow\text{impossible/quadratic},\\
\text{common component}&\Rightarrow d\le2\Rightarrow\text{impossible/quadratic}.
\end{aligned}}
\]

The finite clean case is reduced to the classical finite-plane Segre lemma; once that lemma is either cited in precisely the needed form or supplied by the short self-adjoint primary-count proof, the toric degree-saturation argument gives a contradiction because the degree-eight common product must possess a nonconstant factor, while Sections 4--6 show that no such factor can survive.

Thus the accurate remaining interface is now:

\[
\boxed{\text{one finite invariant-Lagrangian / Segre plane-count lemma}.}
\]

This is substantially smaller than the previous `low-rank quadric-pencil / relative-contact compatibility` gap.

---

## 8. Recommended next action before promoting to main.tex

Do **not** reopen the 31 Hilbert candidates.  Instead:

1. write a self-contained proof of the primary finite-count bound
   \[
   \#\{\text{invariant Lagrangians in a }2r\text{-dimensional primary block}\}\le r+1
   \]
   for `r<=3`, or cite the classical Segre classification with an explicit proposition/table reference;
2. audit the conductor coefficient in Section 2.2 against the already-used J3 local formula;
3. then promote the whole `k=0` argument to the submission as a single theorem.

If the finite-count lemma checks out, the residual-32 triangle is very close to a genuine unconditional closure, without any use of the invalid old split-MacWilliams weight deletion.
