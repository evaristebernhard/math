# Residual-36: complete exclusion of the finite normal quadratic target

Date: 2026-08-09

Status: **paper-level candidate.** This note closes the finite normal \((m,e)=(2,9)\) outlet by classifying the six-dimensional self-adjoint Jordan types and counting invariant Lagrangian planes only along smooth target lines, so no fibre bound at a codimension-two singular point is used.

## 0. Setup

Continue with the disjoint-net residual-36 six-quartic map
\[
\phi:Y=\operatorname{Bl}_A\mathbf P^3\longrightarrow X'\subset\mathbf P^5,
\qquad |A|=28,
\]
where \(D=4H-\sum_{a\in A}E_a\), \(D^3=36\), and in the quadratic-target case
\[
X'=Q_0\cap Q_1,
\qquad (m,e)=(2,9).
\]
Assume throughout this note that \(X'\) is normal and \(\phi\) is finite of degree nine.

The previous reduction shows that the pencil contains a rank-four member
\[
Q_\lambda=Q_1-\lambda Q_0
\]
whose radical is a two-dimensional vector space
\[
K=\ker(T-\lambda I),
\qquad T=B_0^{-1}B_1,
\]
and whose projectivization
\[
S=\mathbf P(K)
\]
is contained in \(X'\). Here \(B_i\) denotes the symmetric bilinear form of \(Q_i\), \(B_0\) is nondegenerate, and \(T\) is \(B_0\)-self-adjoint. Since \(S\subset Q_0\),
\[
B_0|_K=0.
\]
Every target plane \(\Pi=\mathbf P(L)\subset X'\) is equivalent to a three-dimensional \(T\)-invariant maximal \(B_0\)-isotropic subspace \(L\subset V\).

The 28 exceptional divisors map isomorphically to target planes. Since a fixed target plane can carry at most nine exceptional divisors over its generic smooth point, at least four distinct invariant Lagrangian planes occur.

We prove that no self-adjoint Jordan type can support these 28 exceptional planes.

---

## 1. Smooth-line capacity lemma

### Lemma 1
Let \(\Gamma\subset X'\) be an integral curve whose generic point \(\eta\) is smooth on \(X'\). Suppose target planes
\[
\Pi_1,\ldots,\Pi_s\subset X'
\]
all contain \(\Gamma\). Let \(n_i\) be the number of exceptional divisors \(E_a\) mapped isomorphically onto \(\Pi_i\). Then
\[
\boxed{n_1+\cdots+n_s\le9.}
\]

### Proof
At the generic point \(\eta\),
\[
A_\eta:=\mathcal O_{X',\eta}
\]
is a regular local ring. Because \(\Gamma\) has codimension two in the threefold \(X'\), \(\dim A_\eta=2\).

For every point \(y\in Y\) over \(\eta\), the local ring \(\mathcal O_{Y,y}\) is regular of dimension two. Since the morphism is finite, a system of parameters of \(A_\eta\) is a system of parameters in each \(\mathcal O_{Y,y}\). Regular local rings are Cohen--Macaulay, hence these parameters form an \(\mathcal O_{Y,y}\)-regular sequence. Therefore the finite \(A_\eta\)-module
\[
(\phi_*\mathcal O_Y)_\eta
\]
is maximal Cohen--Macaulay. Over the regular local ring \(A_\eta\), Auslander--Buchsbaum gives projective dimension zero, so this module is free. Its rank is the generic degree of \(\phi\), namely nine.

Thus the fibre over \(\eta\) has degree nine. Every exceptional divisor mapping isomorphically onto a plane containing \(\Gamma\) contributes a distinct degree-one sheet over \(\eta\), because the exceptional divisors are pairwise disjoint. Hence the total number of such sheets is at most nine. \(\square\)

The same argument at the generic point of a target plane gives the familiar per-plane bound
\[
\boxed{n_\Pi\le9.}
\]

**Important:** no assertion is made about the degree of a fibre over a special point of the singular line; finite need not imply flat there. All counting below is performed at generic smooth points of planes or smooth lines.

---

## 2. Rank at most two and rank three

If a singular pencil member has rank at most two, its projective radical has dimension at least three. Its intersection with an independent pencil member has dimension at least two and lies in the singular locus of the threefold, contradicting normality. Thus only ranks three and four require analysis.

Assume first that a pencil member \(Q_\lambda\) has rank three. Then
\[
K=\ker(T-\lambda I)
\]
has vector dimension three. Since an invariant Lagrangian exists, every primary summand of \(T\) has even dimension: polynomial projectors decompose the Lagrangian among mutually orthogonal nondegenerate primary spaces, and equality in the half-dimension bound forces even primary dimensions.

The \(\lambda\)-primary part has exactly three Jordan blocks. If it has dimension four, its type is \((2,1,1)\), with a two-dimensional primary summand for a second eigenvalue, of type `(2)` or `(1,1)`. If it has dimension six, the possibilities are
\[
(4,1,1),\qquad(3,2,1),\qquad(2,2,2).
\]
These five cases are exhaustive.

For a `(2,1,1)` \(\lambda\)-primary block, write the size-two chain as
\[
e_2\mapsto e_1\mapsto0
\]
and let \(g,h\) span the two size-one blocks with nondegenerate diagonal form. The invariant isotropic two-spaces are exactly
\[
L_\pm=\langle e_1,g\pm i h\rangle.
\]
Indeed an invariant isotropic two-space not contained in the kernel would contain a vector with nonzero \(e_2\)-coefficient, but then its pairing with \(e_1\) would be nonzero. Inside the kernel, isotropy forces the second generator to be one of the two isotropic lines in \(\langle g,h\rangle\).

If the second primary summand is a size-two Jordan block, it contributes a unique invariant isotropic line, so only two target planes occur. If it is semisimple of dimension two, it contributes two isotropic lines \(M_\pm\), so four target planes
\[
\mathbf P(L_\varepsilon\oplus M_\delta),\qquad \varepsilon,\delta\in\{+,-\},
\]
occur. Pair the two planes with fixed \(M_+\), and similarly those with fixed \(M_-\). Each pair meets along
\[
\mathbf P\bigl((L_+\cap L_-)\oplus M_\delta\bigr),
\]
a line mixing the two distinct primary summands. Its generic point is smooth. Lemma 1 therefore gives at most nine exceptional divisors for each pair, hence at most eighteen in total.

For type `(4,1,1)`, let the size-four chain be \(e_4\mapsto e_3\mapsto e_2\mapsto e_1\mapsto0\), with two nondegenerate size-one blocks \(g,h\). An invariant isotropic three-space has kernel dimension two; it is necessarily
\[
\langle e_1,e_2,g\pm ih\rangle.
\]
The kernel-dimension-one case would be cyclic of length three, but for a top vector beginning with \(e_3\) one has the fixed nonzero pairing \(B_0(v,Nv)=1\). Thus exactly two target planes occur.

For type `(3,2,1)`, use chains \(e_3\mapsto e_2\mapsto e_1\mapsto0\) and \(f_2\mapsto f_1\mapsto0\), together with a nondegenerate size-one vector \(g\). A totally isotropic two-space in the three-dimensional kernel must equal \(\langle e_1,f_1\rangle\). Hence an invariant Lagrangian is
\[
\langle e_1,f_1,e_2\pm ig\rangle,
\]
and these are the only two possibilities; a cyclic length-three restriction is impossible because \(B_0(Nv,Nv)=1\). Again only two target planes occur.

Finally, in type `(2,2,2)` the entire three-dimensional eigenspace \(K\) is totally isotropic, so the radical plane \(\mathbf P(K)\) lies in \(X'\) and is singular. This is a codimension-one singular locus, contradicting normality.

Thus every finite normal rank-three case is impossible: four of the five types have at most two target planes, while the only four-plane type is bounded by two smooth-line applications of Lemma 1.

---

## 3. The rank-four primary/Jordan types

Put
\[
N=T-\lambda I
\]
on the \(\lambda\)-primary space. Self-adjointness gives
\[
(\operatorname{im}N)^{\perp_{B_0}}=\ker N=K.
\]
Since \(B_0\) is nondegenerate,
\[
K^\perp=\operatorname{im}N.
\]
But \(K\) is totally isotropic, so \(K\subset K^\perp\). Hence
\[
\boxed{K\subset\operatorname{im}N.} \tag{2.1}
\]
Consequently neither of the two Jordan chains belonging to \(\lambda\) can have length one.

Now decompose into primary spaces
\[
V=\bigoplus_\mu V_\mu.
\]
Distinct primary spaces are mutually \(B_0\)-orthogonal and each restriction of \(B_0\) is nondegenerate. If \(L\) is any invariant Lagrangian three-space, polynomial projectors in \(T\) give
\[
L=\bigoplus_\mu(L\cap V_\mu).
\]
Since each summand is isotropic,
\[
\dim(L\cap V_\mu)\le\left\lfloor\frac{\dim V_\mu}{2}\right\rfloor.
\]
The sum of the left-hand sides is three, exactly half of \(\dim V=6\). Equality therefore forces every primary dimension to be even.

The \(\lambda\)-eigenspace has dimension two, hence the \(\lambda\)-primary part has exactly two Jordan blocks. By (2.1), both have size at least two. Thus the complete list is
\[
\boxed{
(2,2)+(2),\qquad
(2,2)+(1,1),\qquad
(4,2),\qquad
(3,3).
} \tag{2.2}
\]
In the first two cases the term after `+` is the two-dimensional primary space for a second eigenvalue \(\mu\ne\lambda\): `(2)` means one size-two Jordan block, while `(1,1)` means \(T|_{V_\mu}=\mu I\).

For the explicit counts below, use the standard self-adjoint Jordan basis on a size-\(r\) block
\[
Ne_1=0,\qquad Ne_j=e_{j-1}\ (j\ge2),
\]
with
\[
B_0(e_i,e_j)=0\quad\text{unless }i+j=r+1,
\]
and normalize the nonzero anti-diagonal entries to one. Over \(\mathbf C\) this loses no generality.

---

## 3. A size-two plus size-two primary block

Let the \(\lambda\)-primary part have type \((2,2)\), with bases
\[
e_2\mapsto e_1\mapsto0,
\qquad
f_2\mapsto f_1\mapsto0,
\]
and
\[
B_0(e_1,e_2)=B_0(f_1,f_2)=1.
\]
Then
\[
K=\langle e_1,f_1\rangle.
\]
The invariant maximal isotropic two-spaces in this four-dimensional primary block are exactly
\[
K,
\qquad
M_+=\langle e_1+i f_1,\ e_2+i f_2\rangle,
\qquad
M_-=\langle e_1-i f_1,\ e_2-i f_2\rangle. \tag{3.1}
\]
Indeed, if an invariant isotropic two-space is not \(K\), its intersection with \(K\) has dimension one. Writing its non-kernel generator as \(ae_2+bf_2\) modulo \(K\), invariance forces the kernel line to be \(\langle ae_1+bf_1\rangle\), while isotropy gives
\[
a^2+b^2=0,
\]
so \([a:b]=[1:\pm i]\).

### Type `(2,2)+(2)`
A size-two Jordan block for the second eigenvalue has a unique invariant isotropic line, namely its kernel. Hence there are exactly three invariant Lagrangian three-spaces, and therefore exactly three target planes.

Each target plane carries at most nine exceptional divisors. Thus at most
\[
3\cdot9=27
\]
exceptional divisors can occur, contradicting \(|A|=28\).

So
\[
\boxed{(2,2)+(2)\text{ is impossible}.}
\]

### Type `(2,2)+(1,1)`
Let the second two-dimensional primary space be nondegenerate and semisimple. It has exactly two isotropic lines
\[
\ell_+,\qquad\ell_-.
\]
The six invariant Lagrangian three-spaces are
\[
K\oplus\ell_\pm,
\qquad
M_+\oplus\ell_\pm,
\qquad
M_-\oplus\ell_\pm. \tag{3.2}
\]
Denote the corresponding planes by
\[
A_\pm,\qquad B_\pm,\qquad C_\pm.
\]
They may be paired as
\[
(A_+,B_+),\qquad(A_-,B_-),\qquad(C_+,C_-). \tag{3.3}
\]
Each pair meets along a projective line: for example
\[
A_+\cap B_+
=\mathbf P\bigl((K\cap M_+)\oplus\ell_+\bigr),
\]
and
\[
C_+\cap C_-=\mathbf P(M_-).
\]

The singular locus of this intersection of quadrics is the radical line \(\mathbf P(K)\) from the \(\lambda\)-member together with at most the two isotropic points of the semisimple \(\mu\)-radical. None of the three lines in (3.3) is contained in this singular locus; hence each has smooth generic point.

Applying Lemma 1 to the three pairs gives
\[
(n_{A_+}+n_{B_+})
+(n_{A_-}+n_{B_-})
+(n_{C_+}+n_{C_-})
\le9+9+9=27,
\]
again contradicting \(|A|=28\). Therefore
\[
\boxed{(2,2)+(1,1)\text{ is impossible}.}
\]

---

## 4. Type `(4,2)`

Take
\[
e_4\mapsto e_3\mapsto e_2\mapsto e_1\mapsto0,
\qquad
f_2\mapsto f_1\mapsto0.
\]
Again
\[
K=\langle e_1,f_1\rangle.
\]
Let \(L\) be an invariant isotropic three-space and put
\[
r=\dim(L\cap K).
\]
Then \(r=1\) or \(2\).

If \(r=2\), then \(K\subset L\). Modulo \(K\), a third generator lies in \(\ker N^2\) and has the form
\[
ae_2+bf_2.
\]
Isotropy with \(f_1\in K\) forces \(b=0\). Thus there is exactly one such space,
\[
L_0=\langle e_1,f_1,e_2\rangle.
\]

If \(r=1\), the restriction \(N|_L\) is one Jordan block of size three. Choose a cyclic generator and reduce it modulo its first two iterates to
\[
v=e_3+c f_2+\text{lower terms}.
\]
The isotropy equation
\[
B_0(v,Nv)=0
\]
gives
\[
1+c^2=0,
\]
so \(c=\pm i\). The lower terms can be removed by replacing \(v\) by \(v+\alpha Nv+\beta N^2v\). Thus exactly two further invariant Lagrangians occur.

Hence type `(4,2)` has exactly three target planes. The per-plane bound gives at most \(27\) exceptional divisors, contradicting \(28\). Therefore
\[
\boxed{(4,2)\text{ is impossible}.}
\]

---

## 5. Type `(3,3)`

Take two size-three blocks
\[
e_3\mapsto e_2\mapsto e_1\mapsto0,
\qquad
f_3\mapsto f_2\mapsto f_1\mapsto0,
\]
with
\[
K=\langle e_1,f_1\rangle.
\]
There are exactly four invariant isotropic three-spaces.

If \(\dim(L\cap K)=2\), then
\[
L=A_\pm^{\rm vec}
:=\langle e_1,f_1,e_2\pm i f_2\rangle. \tag{5.1}
\]
Indeed, a generator modulo \(K\) is \(ae_2+bf_2\), and self-isotropy gives \(a^2+b^2=0\).

If \(\dim(L\cap K)=1\), then \(N|_L\) is a size-three block. After changing the cyclic generator by lower iterates, the two possibilities are
\[
L=B_\pm^{\rm vec}
:=\langle
 e_3\pm i f_3,
 e_2\pm i f_2,
 e_1\pm i f_1
\rangle. \tag{5.2}
\]
No other cases occur.

Let \(A_\pm,B_\pm\) be the corresponding projective planes. The crucial intersections are
\[
A_+\cap B_+
=\mathbf P\langle e_1+i f_1,e_2+i f_2\rangle=:\Gamma_+,
\]
\[
A_-\cap B_-
=\mathbf P\langle e_1-i f_1,e_2-i f_2\rangle=:\Gamma_-.
\]
Both are projective lines.

Here \(\lambda\) is the only eigenvalue of \(T\). Every pencil member other than \(Q_\lambda\) is nondegenerate. Hence
\[
\operatorname{Sing}(X')=\mathbf P(K).
\]
Neither \(\Gamma_+\) nor \(\Gamma_-\) equals \(\mathbf P(K)\), so each line has smooth generic point.

Apply Lemma 1 to the two pairs:
\[
n_{A_+}+n_{B_+}\le9,
\qquad
n_{A_-}+n_{B_-}\le9.
\]
Since these are all four target planes,
\[
|A|
=n_{A_+}+n_{B_+}+n_{A_-}+n_{B_-}
\le18,
\]
contradicting \(|A|=28\). Therefore
\[
\boxed{(3,3)\text{ is impossible}.}
\]

---

## 6. Main theorem

### Theorem
In the residual-36 disjoint-net quadratic-target branch
\[
(m,e)=(2,9),
\]
there is no finite morphism
\[
\phi:Y=\operatorname{Bl}_A\mathbf P^3\longrightarrow X'=Q_0\cap Q_1
\]
of degree nine with \(X'\) normal.

Equivalently,
\[
\boxed{\text{finite normal }(2,9)\text{ is impossible}.}
\]

### Proof
The previous singular-line reduction produces a rank-four pencil member with totally isotropic two-dimensional radical. Sections 2--5 give the complete list of self-adjoint Jordan types and exclude each one using only generic smooth plane/line fibre counts. \(\square\)

---

## 7. Residual-36 consequence

The existing cubic-target theorem excludes finite
\[
(m,e)=(3,6)
\]
when the normal target has only isolated singularities. The theorem above now removes the finite normal quadratic-target branch completely. Thus, in the disjoint-net residual-36 setup, the remaining normal outlets are
\[
\boxed{
\text{nonfinite map}
\quad\text{or}\quad
\text{finite cubic target }(3,6)\text{ with positive-dimensional singular locus}.
}
\]
Nonnormal targets remain separate.

This is a genuine closure of an entire numerical branch, not a clean-carrier reduction.
