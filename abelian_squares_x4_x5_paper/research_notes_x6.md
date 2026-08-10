# Separate study of the case x=6

Status date: 2026-08-08.

This note is deliberately separate from `main.tex`.  Labels: **[P]** proved, **[C]** computational candidate / conjectural structural statement, **[O]** open.

## 1. Target value

Let a binary word have six `a`'s and `B=n-6` copies of `b`.  The FMMS effective-word prediction is
\[
T_6(n)=F(6)+F(B)=2+\left\lfloor\frac{B+2}{4}\right\rfloor
=2+\left\lfloor\frac{n-4}{4}\right\rfloor.
\]
The FMMS theorem gives this as an upper bound for the non-boundary range `B>=4`, i.e. `n>=10`.

## 2. Complete brute-force evidence [C]

Exact enumeration was carried out for `10<=n<=24`.  In every case
\[
M(6,n)=T_6(n).
\]
The stable extremal run compositions are only
\[
1+5,\qquad 1+3+2
\]
and their reversals.  The composition `3+3` is extremal only at some small lengths `n<=13`; from `n>=14` it is already strict.

For `n>=14`, the observed extremal reversal representatives are exactly the families described in Sections 3 and 4 below.

Run-count audit for `14<=n<=24`:
- one `a`-run is always strict;
- two `a`-runs attain the target only through `1+5` (and reversal);
- three `a`-runs attain the target only through `1+3+2` (and reversal);
- four or more `a`-runs are at least two above the target in the tested range.

The last bullet is still **[C]**, not a theorem.

## 3. The 1+5 family is exactly the old x=4 problem [P]

Define
\[
V_6(s,q,t)=b^s a b^q a^5 b^t,\qquad q\ge1,
\]
and put
\[
M=\max\{s,q,t\},\qquad u=\min\{s,q\},
\]
\[
C_q(u)=\#\{x:0\le x\le u,\ x\equiv q\pmod2\},
\]
\[
C_6(s,q,t)=
\begin{cases}
0,&t<q,\\
\min\{s,t-q\}+1,&t\ge q.
\end{cases}
\]
Then
\[
\boxed{
\theta(V_6(s,q,t))
=2+\left\lfloor\frac M2\right\rfloor+C_q(u)+C_6(s,q,t).
}
\]
Proof by number of `a`'s in the square:
- zero `a`'s: `floor(M/2)` pure `b`-squares;
- inside `a^5`: the two words `aa` and `a^4`;
- two `a`'s crossing the separating gap: exactly `C_q(u)` words;
- six `a`'s: necessarily `b^x a b^q a^5 b^{x+q}`, giving `C_6` words;
- no further four-`a` word can cross the isolated `a`, since the midpoint would lie in a zero central `b`-gap and would force `q=0`.

Compare with the proved x=4 formula for
\[
W_4(s,q,t)=b^s a b^q a^3 b^t:
\]
\[
\theta(V_6(s,q,t))=\theta(W_4(s,q,t))+1.
\]
For the same total `b`-mass `B=s+q+t`, the x=6 target is also exactly the x=4 target plus one.  Therefore the integer optimisation and equality triples from the x=4 theorem transfer verbatim.

For stable lengths this gives, up to reversal:

### n=4k
\[
(s,q,t)=(0,2k-3,2k-3),
(0,2k-1,2k-5),
(1,2k-3,2k-4),
(2,2k-3,2k-5).
\]

### n=4k+1
\[
(s,q,t)=(0,2k-1,2k-4),
(2,2k-3,2k-4).
\]

### n=4k+2
\[
(s,q,t)=(0,2k-1,2k-3).
\]

### n=4k+3
\[
(s,q,t)=(0,2k-1,2k-2).
\]

(As usual, very small `k` must be interpreted separately when exponents become negative.)

## 4. Exact 2+3+1 count [P]; equality optimisation [C, pending proof]

Define
\[
W_6(q,r,t)=a^2b^q a^3b^r a b^t,\qquad q,r\ge1.
\]
Put `M=max(q,r,t)`.  Then an exact count is
\[
\begin{aligned}
\theta(W_6(q,r,t))={}&\left\lfloor\frac M2\right\rfloor+1
+\mathbf1_{2\mid q}
+C_r(\min\{t,r\})
-\mathbf1_{q=r,\ 2\mid q}\\
&+\mathbf1_{2\mid q}
+\mathbf1_{r\ge q}
+\mathbf1_{q\ge r}\bigl(\min\{t,q-r\}+1\bigr)\\
&+\mathbf1_{q\ge r,\ t\ge q-r}.
\end{aligned}
\]
Here `C_r(v)` is the parity count `#{0<=z<=v : z == r (mod 2)}`.

The terms are, respectively:
- pure `b`-squares and `aa`;
- rank one across the gaps `q` and `r` (with the duplicate `ab^q a` removed when `q=r` is even);
- rank two from the three possible four-`a` windows;
- rank three using all six `a`'s.

This formula was audited by direct factor enumeration for `1<=q,r<=8`, `0<=t<=7`.

The formula already gives the conjectured lower bound for all parameters.  We use the elementary half-mass inequality
\[
\boxed{
\left\lfloor\frac M2\right\rfloor
+\left\lfloor\frac{v+1}{2}\right\rfloor
\ge
\left\lfloor\frac{2M+v+2}{4}\right\rfloor,
\qquad 1\le v\le M.
}
\tag{HM}
\]
To prove (HM), write `M=2a+eta`, `v=2b+delta`, with `eta,delta in {0,1}`.  The assertion reduces to
\[
b+\delta\ge
\left\lfloor\frac{2b+2\eta+\delta+2}{4}\right\rfloor,
\]
which is immediate (for `b=0` one has `v=1`, and for `b>=1` the right side is at most `b`).

For the exact `2+3+1` formula put
\[
v=\min\{t,r\}.
\]
If `r>q` and `t>0`, let `M=max(r,t)`.  Since `r+t=M+v` and `q<=M`,
\[
B=q+r+t\le2M+v,
\]
while `C_r(v)>=floor((v+1)/2)`.  Keeping only the pure term, the constant `2`, and this parity family, (HM) gives `theta>=2+F(B)`.  If `t=0`, then `B=q+r<=2r-1`, and directly
\[
F(B)\le F(2r-1)\le\left\lfloor\frac r2\right\rfloor.
\]

The case `q>r` is symmetric at the level needed for the lower bound.  If `t>0`, with `M=max(q,t)` we again have
\[
r+t\le M+v,
\qquad B=q+r+t\le2M+v,
\]
and (HM) applies to the pure term plus `C_r(v)`; the additional rank-two/rank-three terms in the exact formula are nonnegative.  If `t=0`, then `B=q+r<=2q-1` and `F(B)<=floor(q/2)`.

Finally, if `q=r`, the exact formula simplifies to
\[
\theta=\left\lfloor\frac{\max(q,t)}2\right\rfloor+4
+\mathbf1_{2\mid q}+C_q(\min(t,q)),
\]
so the same argument (with two units of extra slack) applies when `t>0`, and `t=0` is immediate.  Therefore
\[
\boxed{\theta(W_6(q,r,t))\ge T_6(6+q+r+t)}
\]
for every `q,r>=1`, `t>=0`.

Thus **all one-, two-, and three-run x=6 words now satisfy the conjectured lower bound**.  What remains in this subsection is only the equality optimisation for the genuine extremal `2+3+1` family.

Direct optimisation of the exact formula by exhaustive parameter search through `n=32` gives the following stable equality pattern.  This pattern is strongly supported and matches the complete word enumeration through `n=24`, but the all-parameter equality classification has not yet been written as a proof:

### n=4k
\[
(q,r,t)=(2k-5,2k-3,2),
(2k-5,2k-1,0),
(2k-1,2k-5,0).
\]

### n=4k+2
\[
(q,r,t)=(2k-3,2k-1,0),
(2k-1,2k-3,0).
\]

There are no equality triples in the stable odd residue classes.  These are exactly the observed three-run extremisers (up to reversal).

## 5. Boundary-a theorem [P]

**Theorem.** Let `n>=10`, `|w|_a=6`.  If `w` begins or ends with `a`, then
\[
\theta(w)\ge T_6(n).
\]

**Proof.** By reversal suppose that `w=aQ`.  Then `Q` has five `a`'s and length `n-1`, so the proved x=5 theorem gives
\[
\theta(Q)\ge M(5,n-1)=\left\lfloor\frac n4\right\rfloor=T_6(n)-1.
\]
If `theta(Q)>=T_6(n)`, we are done.  It remains that `Q` is an x=5 minimiser.  Use the complete x=5 classification.

1. If
\[
Q=a^2b^q a^3b^t
\]
is in the canonical `2+3` orientation, then all equality families have `q` odd and, for `n>=10`, `t>=1`.  Hence
\[
a^3b^q a^3b
\]
is a six-`a` Abelian square in `w`: splitting the central `b^q` block with `(q+1)/2` copies on the left gives three `a`'s and the same number of `b`'s in each half.  It contains the first `a`, so it is not a factor of `Q`.

2. If the minimiser is in the reversed orientation
\[
Q=b^t a^3b^q a^2,
\]
then the x=5 equality list has `q>=t`.  If `t=0`, the prefix `a^4` is new.  If `t>0`,
\[
a b^t a^3 b^t
\]
is a four-`a` Abelian square and is new.

3. If
\[
Q=b^s a^5b^s
\]
is a one-run x=5 minimiser, then the whole word
\[
a b^s a^5b^s
\]
is an Abelian square: its two halves have Parikh vector `(3,s)`.  It is new.

Thus one new square always supplements the five-`a` minimum.  QED.

This proves the full x=6 conjectured lower bound for the infinite class of words with an `a` on at least one boundary.

## 6. The 3+3 family is strictly non-extremal for n>=14 [P]

Let
\[
C(s,q,t)=b^s a^3b^q a^3b^t,\qquad q\ge1,
\]
and compress each `a^3` block to one `a`:
\[
U(s,q,t)=b^s a b^q a b^t.
\]
Every pure `b`-square of `U` is also present in `C`.  Every mixed two-`a` square
\[
b^x a b^q a b^z
\]
in `U` injects into the six-`a` square
\[
b^x a^3b^q a^3b^z
\]
in `C`; equality of the two half-Parikh vectors is preserved because each half gains two `a`'s.  Distinct words remain distinct.  In addition, `C` contains `aa`, which is outside the image.  Hence
\[
\theta(C)\ge\theta(U)+1.
\]
By the proved two-`a` theorem,
\[
\theta(U)\ge\left\lfloor\frac{s+q+t}{2}\right\rfloor.
\]
Therefore, with `B=s+q+t`,
\[
\boxed{\theta(C)\ge\left\lfloor\frac B2\right\rfloor+1.}
\]
For `B>=8` (`n>=14`) this is at least `T_6(n)+1`.  Thus the `3+3` family cannot be extremal beyond the small range `n<=13`.

## 7. One-run family [P, elementary]

For
\[
w=b^s a^6b^t
\]
put `M=max(s,t)` and `m=min(s,t)`.  The word contains
- `floor(M/2)` pure `b`-squares;
- `aa` and `a^4`;
- the `m+1` distinct rank-three squares `b^x a^6b^x`, `0<=x<=m` (including `a^6`).
Thus
\[
\theta(w)\ge \left\lfloor\frac M2\right\rfloor+m+3,
\]
which is already strictly above `T_6(n)` in the non-boundary range `n>=10`.

## 8. Exact 2+4 family and the complete two-run reduction [P]

For
\[
D(s,q,t)=b^s a^2b^q a^4b^t,\qquad q\ge1,
\]
put
\[
M=\max\{s,q,t\},\qquad u=\min\{s,q\},
\]
and retain the parity count
\[
C_q(u)=\#\{0\le x\le u:x\equiv q\pmod2\}.
\]
Define
\[
C_6(s,q,t)=
\begin{cases}
0,&t<q,\\
\min\{s,t-q\}+1,&t\ge q.
\end{cases}
\]
Then the exact count is
\[
\boxed{
\theta(D)=
\left\lfloor\frac M2\right\rfloor
+(u+1)
+\mathbf1_{2\mid q}
+C_q(u)
+(\min\{q,t\}+1)
+C_6(s,q,t).
}
\]
The terms have the following origin.

- Rank 0: `floor(M/2)` pure `b`-squares.
- Rank 1 inside the initial `a^2` run: `b^x a^2 b^x`, `0<=x<=u`, giving `u+1` words.
- Rank 1 across the separating gap: `ab^q a`, present exactly for even `q`.
- Rank 2 using the initial `a^2` and the first two letters of `a^4`: the admissible left trims are exactly `0<=x<=u`, `x=q (mod 2)`, giving `C_q(u)` words.
- Rank 2 inside the `a^4` run: `b^x a^4 b^x`, `0<=x<=min(q,t)`, giving `min(q,t)+1` words.
- Rank 3: all six `a`'s force the right trim to be `x+q`, giving `C_6` words.

The classes are disjoint by rank or by their internal `a`-gap pattern.  The formula has been independently audited for `0<=s,t<=7`, `1<=q<=8`.

A useful coarse consequence is completely elementary:
\[
\boxed{\theta(D)\ge\left\lfloor\frac{s+q+t}{2}\right\rfloor+2.}
\]
Indeed, write `B=s+q+t`.  If `t<q`, then `M=max(s,q)` and the terms `floor(M/2)+u+t` already dominate `floor(B/2)`.  If `t>=q`, use the rank-three contribution `min(s,t-q)` from `C_6`; separating the cases `M=s`, `M=t`, and `M=q=t` gives the same inequality.  (In each case it reduces to `floor(A/2)+R >= floor((A+R)/2)` for nonnegative integers.)  Hence for `B>=8` (`n>=14`),
\[
\theta(D)-T_6(n)
\ge \left\lfloor\frac B2\right\rfloor-F(B)
\ge2.
\]
Thus `2+4` is uniformly strictly non-extremal in the stable range, with no computational optimisation needed.

Together with Sections 3 and 6 this closes all two-run compositions:
\[
1+5,\qquad2+4,\qquad3+3.
\]
The `1+5` family is completely inherited from x=4; `2+4` is strictly non-extremal by the formula above; and `3+3` is strictly non-extremal for `n>=14`.  Hence
\[
\boxed{\text{for }n\ge14,\text{ every two-run x=6 extremiser has composition }1+5.}
\]

## 9. Three-run reduction: three easy compositions [P]

Write a general three-run word as
\[
b^s a^{r_1}b^p a^{r_2}b^q a^{r_3}b^t,
\qquad p,q\ge1,
\]
with `r_1+r_2+r_3=6`.  Up to reversal there are six run compositions.  Three can be disposed of by short explicit lower bounds.

### 9.1. Composition 1+1+4

Let
\[
W=b^s a b^p a b^q a^4b^t,
\qquad B=s+p+q+t,
\]
and let
\[
P=b^s a b^p a b^q.
\]
The factor `P` has two occurrences of `a`, so the proved two-`a` theorem gives
\[
\theta(P)\ge\left\lfloor\frac{s+p+q}{2}\right\rfloor.
\]
The words `aa` and `a^4` occur in `W` and are not factors of `P`.  Put `A=s+p+q=B-t`.

If `t<=A`, then except for one floor-borderline,
\[
\left\lfloor\frac A2\right\rfloor\ge F(B).
\]
The only failure is `B=4k+2` and `A=t=2k+1`; there `q,t>=1`, so the additional word
\[
ba^4b
\]
is an Abelian square outside `P` and repairs the missing unit.

If `t>A`, then the longest `b`-run inside `P` is at most `A`, while the final run has length `t`.  Hence the new pure powers supplied by the final run contribute at least
\[
\left\lfloor\frac t2\right\rfloor-\left\lfloor\frac A2\right\rfloor
\]
words beyond `AS(P)`.  Therefore
\[
\theta(W)\ge\left\lfloor\frac t2\right\rfloor+2.
\]
Since `t>A`, one has `floor(t/2)>=F(B)`.  Thus in every case
\[
\boxed{\theta(W)\ge T_6(B+6).}
\]

### 9.2. Composition 2+2+2

Let
\[
W=b^s a^2b^p a^2b^q a^2b^t,
\qquad p,q\ge1,
\]
put
\[
M=\max\{s,p,q,t\},
\]
and
\[
R=\max\{\min(s,p),\min(p,q),\min(q,t)\}.
\]
The pure powers give `floor(M/2)` words.  The three `a^2` runs together certify every nested word
\[
b^x a^2b^x,
\qquad0\le x\le R,
\]
so there are `R+1` distinct rank-one words.  Finally, the first two `a^2` runs always give a rank-two word: use
\[
a^2b^p a^2
\]
for even `p`, and
\[
a^2b^p a^2b
\]
for odd `p` (the required final `b` is available because `q>=1`).  Thus
\[
\theta(W)\ge\left\lfloor\frac M2\right\rfloor+R+2.
\]
At most two of the four numbers `s,p,q,t` can exceed `R`, and any such number is at most `M`.  Hence
\[
B=s+p+q+t\le2M+2R.
\]
Since `R>=1`, an elementary parity check gives
\[
F(B)\le\left\lfloor\frac M2\right\rfloor+R.
\]
Therefore `theta(W)>=T_6(B+6)`.

### 9.3. Composition 1+4+1

Let
\[
W=b^s a b^p a^4b^q a b^t,
\qquad p,q\ge1.
\]
Put
\[
M=\max\{s,p,q,t\},\quad
r=\min(p,q),\quad
u=\min(s,p),\quad
v=\min(t,q).
\]
Besides the pure powers, the word contains `aa`, the `r+1` distinct rank-two words
\[
b^x a^4b^x,
\qquad0\le x\le r,
\]
and the two rank-one parity families
\[
b^x a b^p a,
\quad0\le x\le u,\ x\equiv p\pmod2,
\]
\[
a b^q a b^z,
\quad0\le z\le v,\ z\equiv q\pmod2.
\]
The two rank-one families overlap only in the word `ab^p a` when `p=q` is even.  Consequently
\[
\theta(W)\ge
\left\lfloor\frac M2\right\rfloor+r+2
+C_p(u)+C_q(v)-\mathbf1_{p=q,\ 2\mid p}.
\]
Since `r-1_{p=q,2|p}>=1`, this is at least
\[
\left\lfloor\frac M2\right\rfloor+3
+\left\lfloor\frac{u+1}{2}\right\rfloor
+\left\lfloor\frac{v+1}{2}\right\rfloor.
\]
Moreover
\[
s+p\le M+u,
\qquad
q+t\le M+v,
\]
so `B<=2M+u+v`.  A direct parity estimate now yields
\[
F(B)\le
\left\lfloor\frac M2\right\rfloor+1
+\left\lfloor\frac{u+1}{2}\right\rfloor
+\left\lfloor\frac{v+1}{2}\right\rfloor.
\]
Hence again `theta(W)>=T_6(B+6)` (in fact with at least one unit of slack in the displayed estimate).

### 9.4. Composition 1+2+3 [P]

Let
\[
W=b^s a b^p a^2b^q a^3b^t,
\qquad p,q\ge1,
\]
and put
\[
B=s+p+q+t,\qquad
N=\max\{s,p,q,t\},\qquad
u=\min\{p,q\}.
\]
Consider the suffix containing the last five occurrences of `a`,
\[
Q=b^p a^2b^q a^3b^t.
\]
By the exact `2+3` formula from the x=5 theorem,
\[
\theta(Q)=
\left\lfloor\frac{M}{2}\right\rfloor
+\nu+1
+\mathbf1_{2\mid q}
+C_q(\nu)
+\mathbf1_{t\ge q},
\qquad M=\max\{p,q,t\}.
\]
In the full word, the pure `b`-square contribution may be upgraded from `floor(M/2)` to `floor(N/2)`.

There are two further families outside the five-`a` wing.  First, writing
\[
v=\min\{s,p\},
\]
the factors
\[
b^x a b^p a,
\qquad0\le x\le v,\quad x\equiv p\pmod2,
\]
are rank-one squares.  They are new except that the word `ab^p a` may already occur in `Q` when `p=q` is even.  Hence their net contribution is
\[
G=C_p(v)-\mathbf1_{p=q,\ 2\mid p}.
\]

Second, let
\[
\varepsilon=q\bmod2\in\{0,1\}.
\]
A factor containing all six occurrences of `a` and left boundary trim `x` becomes an Abelian square if its right trim is chosen as
\[
z=x+p-\varepsilon.
\]
Indeed, the midpoint lies in the central `b^q` block and the choice gives `2y=q-\varepsilon` copies of that block in the left half.  Thus every integer
\[
0\le x\le s,\qquad0\le x+p-\varepsilon\le t
\]
gives a distinct rank-three square, automatically outside `Q`.  Their number is
\[
K=\max\{0,\min(s,t-p+\varepsilon)+1\}.
\]
Consequently
\begin{equation}\label{eq:x6-123-lower}
\theta(W)\ge
\left\lfloor\frac N2\right\rfloor
+\nu+1
+\mathbf1_{2\mid q}
+C_q(\nu)
+\mathbf1_{t\ge q}
+G+K.
\tag{L123}
\end{equation}

We compare this with `T_6(B+6)=2+F(B)`.

**Case 1: `q>=p`.**  Here `nu=p`.  The definition of `K` implies
\[
s+t\le N+p+K.
\]
Indeed, if `K=0`, then `t<p-\varepsilon`; if `K>0`, put `r=t-p+\varepsilon>=0`, so `K=min(s,r)+1` and
\[
s+r\le N+\min(s,r)=N+K-1.
\]
Also `p+q<=p+N`, hence
\[
B\le2N+2p+K.
\]
Dropping the nonnegative indicator terms and `G` from (L123), and using
\[
C_q(p)\ge\left\lfloor\frac{p+1}{2}\right\rfloor,
\]
we obtain
\[
\theta(W)\ge
\left\lfloor\frac N2\right\rfloor
+p+1
+\left\lfloor\frac{p+1}{2}\right\rfloor
+K.
\]
For all integers `N>=p>=1`, `K>=0`,
\[
\left\lfloor\frac N2\right\rfloor
+p+1
+\left\lfloor\frac{p+1}{2}\right\rfloor
+K
\ge
2+\left\lfloor\frac{2N+2p+K+2}{4}\right\rfloor.
\]
To see this, write `N=2a+eta`, `p=2b+delta`, with `eta,delta in {0,1}`; after cancelling `a+b+2` the claim reduces to
\[
2b-1+2\delta+K
\ge
\left\lfloor\frac{2\eta+2\delta+K+2}{4}\right\rfloor,
\]
which is immediate (if `delta=0` then `b>=1`, while if `delta=1` the left side is at least `K+1`).  Therefore `theta(W)>=2+F(B)`.

**Case 2: `p>q`.**  Now `nu=q`, and `p!=q`, so there is no duplicate subtraction in `G`.  Put again `v=min(s,p)`.  Since
\[
s+p\le N+v,\qquad q+t\le N+q,
\]
we have
\[
B\le2N+q+v.
\]
Moreover
\[
C_q(q)=\left\lfloor\frac q2\right\rfloor+1,
\qquad
G=C_p(v)\ge\left\lfloor\frac{v+1}{2}\right\rfloor.
\]
Thus (L123), after discarding the other nonnegative terms, gives
\[
\theta(W)\ge
\left\lfloor\frac N2\right\rfloor
+q+2
+\left\lfloor\frac q2\right\rfloor
+\left\lfloor\frac{v+1}{2}\right\rfloor.
\]
This is at least
\[
2+\left\lfloor\frac{2N+q+v+2}{4}\right\rfloor
\ge2+F(B).
\]
For the first inequality, the crude bounds `floor(N/2)>=(N-1)/2`, `floor(q/2)>=(q-1)/2`, and `floor((v+1)/2)>=v/2` already suffice unless `(q,v)=(1,0)`; in that remaining case it reduces directly to
\[
\left\lfloor\frac N2\right\rfloor+1
\ge
\left\lfloor\frac{2N+3}{4}\right\rfloor.
\]
Hence the whole `1+2+3` family satisfies the conjectured x=6 lower bound.

### 9.5. Composition 2+1+3 [P]

Let
\[
W=b^s a^2b^p a b^q a^3b^t,
\qquad p,q\ge1,
\]
and set
\[
B=s+p+q+t,\qquad
N=\max\{s,p,q,t\},\qquad
r=\min\{s,p\},\qquad
u=\min\{p,q\}.
\]
The pure `b`-squares contribute `floor(N/2)`.  The initial `a^2` run gives the `r+1` nested rank-one words
\[
b^x a^2b^x,
\qquad0\le x\le r.
\]
Across the two positive gaps we have the parity families
\[
a b^p a b^z,
\qquad0\le z\le\nu,\quad z\equiv p\pmod2,
\]
and
\[
b^x a b^q a,
\qquad0\le x\le\nu,\quad x\equiv q\pmod2.
\]
Their only possible overlap is the word `ab^p a` when `p=q` is even.  Therefore their union has size
\[
C_p(\nu)+C_q(\nu)-\mathbf1_{p=q,\ 2\mid p}.
\]

**Case 1: `p>q`.**  Then `nu=q`, there is no overlap, and
\[
C_p(q)+C_q(q)\ge q+1.
\]
Moreover
\[
s+p\le N+r,
\qquad
q+t\le N+q,
\]
so
\[
B\le2N+r+q.
\]
Hence
\[
\theta(W)\ge
\left\lfloor\frac N2\right\rfloor+r+q+2.
\]
Since
\[
\left\lfloor\frac N2\right\rfloor+r+q
\ge
\left\lfloor\frac{2N+r+q+2}{4}\right\rfloor,
\]
we obtain `theta(W)>=2+F(B)`.

**Case 2: `p<=q`.**  In this case the two parity families, after subtracting their possible overlap, have at least `p+1` distinct words.  We add a family containing all six occurrences of `a`.  Let
\[
\varepsilon\in\{0,1\},
\qquad
\varepsilon\equiv p-q\pmod2.
\]
Because `p<=q`, the difference `z-x=varepsilon` lies in the admissible rank-three discrepancy interval `[p-q,p+q]`.  Thus every
\[
0\le x\le s,\qquad z=x+\varepsilon\le t
\]
gives a six-`a` Abelian square.  These are distinct from all rank-one words, and their number is
\[
K=\max\{0,\min(s,t-\varepsilon)+1\}.
\]
The definition gives
\[
s+t\le N+K.
\]
Also `p+q<=p+N`, hence
\[
B\le2N+p+K.
\]
Therefore
\[
\theta(W)\ge
\left\lfloor\frac N2\right\rfloor+r+p+2+K
\ge
2+\left\lfloor\frac{2N+p+K+2}{4}\right\rfloor
\ge2+F(B).
\]
The middle inequality is an elementary parity check (indeed it remains true after discarding `r`).

Thus the entire `2+1+3` composition satisfies the x=6 conjectured lower bound.

### 9.6. Remaining three-run case

Up to reversal, the only three-run composition still requiring an optimisation is
\[
\boxed{1+3+2}.
\]
This is the genuine extremal family of Section 4.  Its exact counting formula is already proved; what remains is to turn the computational equality pattern into an all-parameter integer optimisation.

## 10. High-run endpoint compensation [C]

At this point the lower-bound problem has been reduced to `r_a(w)>=4`.  There is a substantially weaker and more targeted replacement for the earlier endpoint-extension conjecture.

Write a six-`a` word as
\[
w=b^{g_0}a_1b^{g_1}\cdots a_6b^{g_6},
\]
and reverse so
\[
d=g_0\le g_6.
\]
Let `Q` be the suffix containing the last five occurrences of `a`, so its `b`-mass is
\[
Y=B-d.
\]
If `r_a(w)>=4`, then `Q` has at least three `a`-runs.  Hence the proved x=5 run-rigidity theorem gives
\[
\theta(Q)\ge M(5,|Q|)+1=F(Y)+2.
\]
Define the surplus above this strict high-run baseline by
\[
e_{\rm hr}=\theta(Q)-[F(Y)+2]\ge0,
\]
and let
\[
N_6(w)=\#\{U\in AS(w):|U|_a=6\}.
\]
Since `Q` contains only five occurrences of `a`, every rank-three word counted by `N_6(w)` lies outside `AS(Q)`.  Therefore the full x=6 lower bound would follow from
\[
\boxed{
e_{\rm hr}+N_6(w)
\ge F(B)-F(Y).
}
\tag{HR}
\]
The right side is only the floor increment caused by restoring the shorter endpoint run `b^d`, hence is about `d/4`.

Complete enumeration for `10<=n<=24` and `r_a(w)>=4` found no counterexample to (HR).  In fact, in that range every case with a positive right-hand side has at least one unit of additional slack.

The rank-three term has an exact geometric interpretation.  Put
\[
A=g_1+g_2-g_4-g_5,
\qquad c=g_3.
\]
For an all-six-`a` factor with left and right boundary trims `x,z`, respectively,
\[
0\le x\le d,\qquad0\le z\le g_6,
\]
the Abelian-square condition is
\[
|x-z+A|\le c,
\qquad x-z+A\equiv c\pmod2.
\]
Restricting further to `0<=x,z<=d`, if `m` denotes the smallest absolute value of an admissible difference `h=x-z`, then
\[
N_6(w)\ge\max\{0,d+1-m\}.
\]
Thus the only hard situation is when the admissible discrepancy band lies far from the diagonal.  In that case
\[
m=|A|-c
\]
(up to the one-unit parity case), so the left and right internal two-gap sums are strongly unbalanced.  The intended proof of (HR) is to show that precisely this imbalance forces the five-`a` wing surplus `e_hr` to grow.  This is now the main structural gap.

### 10.1. Older stronger endpoint candidates

For comparison, an earlier computational candidate was the stronger inequality
\[
e+N_{esc}\ge \left\lceil\frac d2\right\rceil+1,
\tag{E6}
\]
where `e=theta(Q)-M(5,|Q|)` and `N_esc=|AS(w)\\AS(Q)|`.  It also held through `n=24`, but (HR) is much closer to exactly what the proof needs and avoids counting arbitrary escape words.

The six-`a` restricted padding candidate and its general counterexample are recorded below.  The old E6 statement is retained only for comparison; (HR) is now the preferred target.

A related six-`a` computational candidate is
\[
\boxed{|AS(b^2ub^2)\setminus AS(u)|\ge1.}
\tag{Pad2-6}
\]
for `|u|_a=6`.  No six-`a` counterexample has been found in the tested range.  However, the corresponding statement for arbitrary binary words is **false**.  A counterexample is
\[
u=a^5b^4a^2bab^3,
\]
which has eight occurrences of `a` and satisfies
\[
AS(b^2ub^2)=AS(u).
\]
Thus only the restricted six-`a` version remains a candidate; it should not be promoted to a general padding principle.

Neither (E6) nor (Pad2-6) is currently proved; do not cite them as theorems.

## 11. Current picture

The x=6 problem now looks substantially more structured than initially expected.

**Proved infinite pieces:**
- every word with a boundary `a` satisfies the x=6 lower bound;
- every one-run word satisfies the lower bound;
- every two-run word satisfies the lower bound; for `n>=14` a two-run extremiser must have composition `1+5`, and that family is completely solved by transfer from x=4;
- every three-run word satisfies the lower bound: `1+1+4`, `1+4+1`, `2+2+2`, `1+2+3`, and `2+1+3` have direct lower-bound proofs, while `1+3+2` has an exact counting formula;
- `2+4` and `3+3` are uniformly strictly non-extremal for `n>=14`;
- an exact count is proved for the genuine `2+3+1` / reversed `1+3+2` family.  Its stable equality pattern is computationally identified through `n=32`; only the all-parameter equality optimisation remains to be written.

Thus the **x=6 lower-bound problem is now reduced entirely to words with at least four `a`-runs**:
\[
\boxed{r_a(w)\ge4.}
\]
Complete enumeration through `n=24` shows these words are not merely non-extremal but, for `n>=14`, lie at least two units above the target.  The principal remaining theorem should therefore be a high-run surplus statement rather than another extremal family classification.

**Main open step:** prove a uniform lower bound for `r_a(w)>=4`.  The most promising routes are now:
1. use the x=5 run-rigidity theorem on a five-`a` wing and combine its surplus with rank-three boundary-trim squares;
2. prove the endpoint-extension inequality (E6), which would directly finish the remaining high-run regime (and in fact much more);
3. develop a direct high-run dispersion lemma.  The unrestricted Pad2 route has been abandoned because its general form is false; only the six-`a` restricted Pad2-6 remains as secondary computational evidence.
