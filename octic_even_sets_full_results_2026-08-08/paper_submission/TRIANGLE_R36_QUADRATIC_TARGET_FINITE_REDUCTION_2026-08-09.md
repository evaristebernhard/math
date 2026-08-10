# Residual-36: finite quadratic target forces a positive-dimensional singular locus

Date: 2026-08-09

Status: **superseded for the normal finite branch by `TRIANGLE_R36_QUADRATIC_TARGET_JORDAN_CLOSURE_2026-08-09.md`; retained only as an intermediate reduction.** Its earlier rank-three singular-conic sheet count is not part of the final proof, since finite need not be flat over a codimension-two singular locus.

## Setup

In the disjoint-net residual-36 branch, the six quartics define
\[
\phi:Y=\operatorname{Bl}_A\mathbf P^3\longrightarrow X'\subset Q_0^4\subset\mathbf P^5,
\qquad |A|=28,
\]
with
\[
D=4H-\sum_{a\in A}E_a,
\qquad D^3=36.
\]
In the quadratic-target case
\[
(m,e)=(2,9),
\qquad
X'=Q_0\cap Q_1,
\]
where \(Q_0\) is the smooth rank-six difference quadric and \(\deg\phi=9\).

Assume in this note that \(\phi\) is finite. We prove
\[
\boxed{\dim\operatorname{Sing}(X')\ge1.}
\]
Consequently the finite \((2,9)\) case with isolated target singularities is impossible.

## 1. Exceptional planes give several planes on X'

For every \(a\in A\), the exceptional divisor
\[
E_a\simeq\mathbf P^2
\]
is mapped linearly by \(|D|\), because \(D|_{E_a}\simeq\mathcal O_{\mathbf P^2}(1)\) and the determinant complete intersections are transverse at \(a\). Hence \(E_a\) maps isomorphically to a plane
\[
\Pi_a\subset X'.
\]

A generic point of a fixed target plane has at most nine preimages under a finite degree-nine map. Therefore at most nine exceptional divisors can map to the same plane. Since there are 28 exceptional divisors, \(X'\) contains at least
\[
\left\lceil\frac{28}{9}\right\rceil=4
\]
distinct planes. For the pencil argument below, two distinct planes already suffice.

## 2. Linear-algebra lemma: two common planes force a corank-at-least-two pencil member

Let \(V\) be the six-dimensional vector space underlying \(\mathbf P^5\), let \(B_0\) be the nondegenerate symmetric form defining \(Q_0\), and let
\[
T=B_0^{-1}B_1.
\]
Then \(T\) is self-adjoint with respect to \(B_0\).

A plane \(\Pi=\mathbf P(L)\subset Q_0\cap Q_1\) corresponds to a three-dimensional subspace \(L\subset V\) that is totally isotropic for both forms. Since \(L\) is maximal \(B_0\)-isotropic,
\[
L^{\perp_{B_0}}=L.
\]
For \(x,y\in L\),
\[
B_0(Tx,y)=B_1(x,y)=0,
\]
so \(Tx\in L\). Thus every plane in \(X'\) is a \(T\)-invariant Lagrangian subspace.

Suppose every eigenspace of \(T\) were one-dimensional. Decompose \(V\) into generalized eigenspaces
\[
V=\bigoplus_i V_i.
\]
Self-adjointness makes the primary summands pairwise orthogonal and the restriction of \(B_0\) to each \(V_i\) nondegenerate. One-dimensional eigenspace means \(T|_{V_i}\) is a single Jordan block. Such a block has a unique invariant subspace of each dimension.

Any invariant Lagrangian decomposes as
\[
L=\bigoplus_i(L\cap V_i).
\]
Isotropy gives
\[
\dim(L\cap V_i)\le\left\lfloor\frac{\dim V_i}{2}\right\rfloor.
\]
Since \(\dim L=3=\frac12\dim V\), equality in the total dimension forces every \(\dim V_i\) to be even and
\[
\dim(L\cap V_i)=\frac12\dim V_i
\]
for every \(i\). The single-Jordan-block property then makes each summand unique. Hence there is at most one \(T\)-invariant Lagrangian.

But \(X'\) contains at least two distinct planes. Therefore some eigenspace of \(T\) has dimension at least two. Equivalently, for some \(\lambda\),
\[
\ker(B_1-\lambda B_0)
\]
has dimension at least two. Thus the pencil contains a quadric
\[
Q_\lambda
\]
of rank at most four.

This is the elementary self-adjoint version of the standard regular-pencil picture for intersections of two quadrics.

## 3. Rank at most three already gives a singular curve

Let \(R=\mathbf P(\ker Q_\lambda)\) be the radical. If
\[
\operatorname{rank}Q_\lambda\le3,
\]
then
\[
\dim R\ge2.
\]
On \(R\), the gradient of \(Q_\lambda\) vanishes identically. The intersection
\[
R\cap(Q_\mu=0)
\]
with any independent pencil member is a positive-dimensional projective quadric (or all of \(R\)). At every point of this intersection the Jacobian of the two defining quadrics has rank at most one. Hence
\[
\dim\operatorname{Sing}(X')\ge1.
\]

Thus the only case that could conceivably have isolated target singularities is a rank-four pencil member.

## 4. Rank four: UFD produces a curve over the radical line

Assume
\[
\operatorname{rank}Q_\lambda=4.
\]
Choose linear coordinates in the six-dimensional quartic space so that
\[
Q_\lambda=f_1f_2-f_3f_4,
\]
with radical coordinates \(r,s\). The four non-radical coordinates \(f_1,f_2,f_3,f_4\) are linearly independent quartic forms on \(\mathbf P^3\).

Unique factorization gives the standard factorization. Let
\[
g=\gcd(f_1,f_3),
\qquad f_1=ga,
\qquad f_3=gc,
\qquad\gcd(a,c)=1.
\]
The relation \(f_1f_2=f_3f_4\) yields
\[
a f_2=c f_4,
\]
so
\[
f_2=cd,
\qquad
f_4=ad.
\]
Homogeneity gives
\[
\deg g=\deg d=\alpha,
\qquad
\deg a=\deg c=\beta,
\qquad
\alpha+\beta=4.
\]
Neither \(\alpha\) nor \(\beta\) is zero: otherwise two of \(f_1,f_2,f_3,f_4\) would be proportional, contradicting their linear independence.

Therefore
\[
C_1=V(g,d),
\qquad
C_2=V(a,c)
\]
are positive-dimensional projective schemes (curves in the coprime case, with an even larger component if a pair has a common factor). On \(C_1\),
\[
f_1=f_2=f_3=f_4=0,
\]
so the six-quartic morphism maps the strict transform of every positive-dimensional component of \(C_1\) into the radical line
\[
L=\mathbf P(\ker Q_\lambda)\simeq\mathbf P^1.
\]
The base locus of all six quartics is only the finite set \(A\), so blowing up \(A\) does not remove this positive-dimensional component.

Because \(\phi\) is finite, it cannot contract a curve. Hence the image of such a component must be one-dimensional and therefore dense in \(L\). Since the image lies in \(X'\),
\[
L\subset X'.
\]
But the gradient of \(Q_\lambda\) vanishes identically on its radical line. Thus every point of \(L\) is singular on the complete intersection \(X'=Q_\lambda\cap Q_\mu\): the two-gradient Jacobian has rank at most one. Consequently
\[
L\subset\operatorname{Sing}(X').
\]
Therefore again
\[
\dim\operatorname{Sing}(X')\ge1.
\]

## 5. In the normal finite case rank three is also impossible

Assume now that \(X'\) is normal and \(\phi\) finite. Rank at most two is immediately impossible: the radical has projective dimension at least three, so its intersection with the second quadric has dimension at least two and lies in \(\operatorname{Sing}(X')\), contradicting regularity in codimension one.

Suppose a pencil member has rank three. Its radical is a plane
\[
R\simeq\mathbf P^2.
\]
Normality rules out \(R\subset X'\), so
\[
\Gamma=R\cap X'
\]
is a plane conic (possibly reducible or nonreduced) contained in the singular locus.

Let \(\Pi=\mathbf P(L)\subset X'\) be any target plane. For the rank-three quadratic form, the quotient of the six-dimensional vector space by the three-dimensional radical is a nondegenerate three-dimensional quadratic space, whose maximal totally isotropic vector subspaces have dimension one. Since \(L\) has dimension three and is totally isotropic, its image in the quotient has dimension at most one. Hence
\[
\dim(L\cap\ker Q_\lambda)\ge2,
\]
so projectively
\[
\Pi\cap R
\]
contains a line. Because \(\Pi\subset X'\), this line lies in \(\Gamma\). Therefore \(\Gamma\) is reducible or doubled and has at most two line components.

For every exceptional plane \(E_a\), the isomorphism \(E_a\to\Pi_a\) carries the line \(\Pi_a\cap R\) back to a line in \(E_a\) mapping with degree one to one of these at most two target lines. Distinct exceptional divisors are disjoint. Over a generic point of a fixed target line, a finite degree-nine morphism has at most nine preimages, so at most nine exceptional lines can dominate that target line. Two target lines can therefore account for at most eighteen exceptional divisors, contradicting \(|A|=28\).

Thus rank three is impossible in the normal finite case.

Combining this with the rank-four argument above gives a sharper conclusion: any normal finite quadratic target must have a rank-four pencil member whose radical line \(L\) is contained in \(X'\). In particular
\[
L\subset\operatorname{Sing}(X').
\]

## Theorem

In the residual-36 disjoint-net quadratic-target case
\[
(m,e)=(2,9),
\]
if the six-quartic morphism \(\phi:Y\to X'\) is finite, then
\[
\boxed{\dim\operatorname{Sing}(X')\ge1.}
\]
If in addition \(X'\) is normal, then the surviving finite case is forced into the single rank-four singular-line model:
\[
\boxed{\exists\ Q_\lambda\text{ of rank }4\text{ with }\mathbf P(\ker Q_\lambda)\subset X'.}
\]
Consequently a finite \((2,9)\) target with isolated singularities is impossible.

No reduced/integral `CI(3,3)` or `CI(2,2)` carrier hypothesis is used. The clean rank-four `(1,3)/(2,2)` analysis is therefore replaced, for the normal finite problem, by a single singular-line quadratic-complex outlet.

## Combined residual-36 consequence

The existing cubic-target theorem already excludes finite
\[
(m,e)=(3,6)
\]
when the target has only isolated singularities. Combining the two results gives:

> If the disjoint-net residual-36 six-quartic morphism is finite and the target is normal, then every surviving target must have a positive-dimensional singular locus.

Thus the normal residual-36 problem is compressed to
\[
\boxed{\text{nonfinite map}\quad\text{or}\quad\text{finite target with singular curve}.}
\]
Nonnormal targets remain a separate outlet.

## Literature cross-check

The self-adjoint-operator formulation used in Section 2 is standard in the theory of pencils of quadrics. Xiaoheng Wang, *Maximal linear spaces contained in the base loci of pencils of quadrics* (arXiv:1302.2385), formulates a common isotropic subspace as a subspace satisfying \(X\subset X^{\perp}\) and \(TX\subset X^{\perp}\), and identifies regular pencils with self-adjoint operators whose eigenspaces are one-dimensional. The proof above is included to keep the paper-level implication self-contained.
