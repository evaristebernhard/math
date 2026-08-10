# Additive squares, run-length encodings, and the FMMS extremal problem

Status date: 2026-08-08

This note separates statements into three classes.

- **[P] proved / formally checkable now**: complete argument is recorded below or already appears in `main.tex`.
- **[C] candidate / partially derived**: supported by earlier calculations or finite experiments, but a paper-level proof has not yet been written and audited.
- **[O] open**: deliberately left as a gap or research question.

The purpose is to understand whether the general FMMS conjecture is merely a difficult finite extremal problem or whether it touches the classical additive-square problem in an essential way.

---

## 1. Baseline FMMS problem [P: source / main.tex]

For a finite binary word `w`, let `theta(w)` be the number of **distinct** Abelian-square factors. For

\[
M(x,n)=\min\{\theta(w): |w|=n,\ |w|_a=x\},
\]

Fazekas--Mammoliti--Mercaş--Simpson (FMMS, 2026) determine `x <= 3`, construct an effective word for general Parikh vectors, and conjecture that the construction is extremal. With

\[
F(t)=\left\lfloor\frac{t+2}{4}\right\rfloor,
\]

the conjectural non-boundary value is

\[
M(x,x+y)=F(x)+F(y).
\]

The present manuscript proves the next two slices:

\[
M(4,n)=1+\left\lfloor\frac{n-2}{4}\right\rfloor,
\qquad
M(5,n)=\left\lfloor\frac{n+1}{4}\right\rfloor,
\]

and classifies their minimisers. These statements and their proofs are already in `main.tex`.

---

## 2. Classical additive-square problem [P: literature]

For a finite integer word

\[
g=g_1g_2\cdots g_m,
\]

an **additive square** is a factor

\[
g_i\cdots g_{i+k-1}\;g_{i+k}\cdots g_{i+2k-1}
\]

such that

\[
\sum_{r=0}^{k-1}g_{i+r}
=
\sum_{r=k}^{2k-1}g_{i+r}.
\]

The classical Pirillo--Varricchio / Halbeisen--Hungerbühler problem asks whether there exists an infinite word over a finite integer alphabet avoiding additive squares. This is still open in 2026; Vukusic's 2026 Monthly article explicitly describes it as open.

Cassaigne--Richomme--Saari--Zamboni (2011), Theorem 19, prove a strict existence equivalence with a binary Abelian-square avoidance property (their BAS property):

> an infinite PVHH/additive-square-free integer word exists if and only if an infinite binary word exists whose set of positions avoiding Abelian squares has positive lower density.

Their forward encoding first affinely normalizes the integer alphabet to odd positive integers and uses

\[
\tau(c)=0\,1^c\,0.
\]

Thus a run-length encoding is not merely an analogy: it is already a standard bridge between additive squares and binary Abelian squares.

Brown--Jungić--Poelstra (2014) also identify the additive-square problem with the bounded-gap **double 3-term arithmetic progression** problem.

---

## 3. A direct finite run-length bridge [P]

For a positive integer word

\[
g=(g_1,\dots,g_m),
\]

define the binary encoding

\[
E(g)=a b^{g_1}a b^{g_2}\cdots a b^{g_m}.
\]

### Proposition 3.1 (strict additive square -> binary Abelian square) [P]

If

\[
q=(g_i,\dots,g_{i+2k-1})
\]

is an additive-square factor of `g`, then `E(q)` is an Abelian-square factor of `E(g)`.

**Proof.** Split `q=UV` with `|U|=|V|=k` and `sum U=sum V`. Then

\[
E(q)=E(U)E(V).
\]

Both halves contain exactly `k` occurrences of `a`; the numbers of `b` are `sum U` and `sum V`, respectively. Hence the halves have equal Parikh vectors. ∎

Because `E` is injective on positive integer words, distinct additive-square factor-words of `g` map to distinct Abelian-square factor-words of `E(g)`. Consequently

\[
\#\{\text{distinct additive-square factors of }g\}
\le
\theta(E(g)).
\]

This implication is automatically checked in `research_trimmed_additive.py`; the audit passed for all 3279 words over `{1,2,3}` of length at most 7.

---

## 4. Exact rank-window criterion [P]

Write an arbitrary binary word in gap form

\[
w=b^{g_0}a b^{g_1}a\cdots a b^{g_x},
\qquad g_j\ge0.
\]

Fix a window containing exactly the consecutive occurrences

\[
a_{i+1},a_{i+2},\dots,a_{i+2k}.
\]

Every factor containing exactly this window has the form

\[
Q_{i,k}(u,v)
=
 b^u a b^{g_{i+1}}a\cdots a b^{g_{i+2k-1}}a b^v,
\]

where

\[
0\le u\le g_i,\qquad 0\le v\le g_{i+2k}.
\]

Set

\[
L_{i,k}=\sum_{r=1}^{k-1} g_{i+r},\qquad
R_{i,k}=\sum_{r=k+1}^{2k-1} g_{i+r},\qquad
c_{i,k}=g_{i+k},
\]

and

\[
D_{i,k}(u,v)=u-v+L_{i,k}-R_{i,k}.
\]

### Theorem 4.1 (exact rank-window test) [P]

\[
Q_{i,k}(u,v)\text{ is an Abelian square}
\iff
\begin{cases}
|D_{i,k}(u,v)|\le c_{i,k},\\
D_{i,k}(u,v)\equiv c_{i,k}\pmod 2.
\end{cases}
\]

**Proof.** Since the factor contains `2k` occurrences of `a`, each half must contain exactly `k`; therefore the midpoint lies inside the central run `b^{c_{i,k}}`. If the left half uses `t` letters of this central run, equality of the `b`-counts of the two halves is exactly

\[
u+L_{i,k}+t
=
(c_{i,k}-t)+R_{i,k}+v.
\]

Hence

\[
2t=c_{i,k}-D_{i,k}(u,v).
\]

An integer `t` with `0<=t<=c_{i,k}` exists exactly under the displayed interval and parity conditions. ∎

For `k=1` this is the familiar two-`a` / gap-square condition used throughout `main.tex`.

---

## 5. "Trimmed/split additive square" viewpoint [P definition; terminology provisional]

Equation

\[
u+L+t=(c-t)+R+v
\]

is naturally a **boundary-relaxed additive equality**: the two sides consist of

1. a trimmed amount from the outer left/right gaps (`u,v`),
2. full internal gaps (`L,R`), and
3. a split of the central gap (`t,c-t`).

For discussion we call this a **trimmed/split additive-square condition**. This phrase is provisional; a web/literature search did not locate an established notion with exactly this name.

A strict additive square of the gap word is a special aligned case of this relation. The binary FMMS problem therefore sees a larger family than the classical strict additive-square problem.

This distinction may be decisive: the strict infinite avoidance question is open, whereas the boundary-relaxed finite condition can occur even when the gap word is strict-additive-square-free.

---

## 6. Exact decomposition by number of minority letters [P]

For each `k>=1`, let `D_k(w)` be the set of distinct Abelian-square factor-words of `w` containing exactly `2k` occurrences of `a`. Then the classes `D_k(w)` are disjoint. If

\[
M_b=\max_j g_j,
\]

the zero-`a` squares are precisely

\[
b^2,b^4,\dots,b^{2\lfloor M_b/2\rfloor}.
\]

Therefore

\[
\theta(w)
=
\left\lfloor\frac{M_b}{2}\right\rfloor
+
\sum_{k=1}^{\lfloor x/2\rfloor}|D_k(w)|.
\]

Theorem 4.1 gives an exact local description of the occurrence windows contributing to each `D_k`. The remaining difficulty is **distinctness across windows of the same rank**.

This is a precise reformulation of where global collision accounting enters.

---

## 7. Collision -> gap periodicity [P, local statement]

Suppose the same mixed rank-`k` Abelian-square word is realized by two overlapping `2k`-`a` windows whose starting `a`-indices differ by `d`, with `1<=d<=2k-1`. Equality of the binary factor-words forces equality of their internal gap strings on the overlap; in particular

\[
g_{i+r}=g_{i+d+r}
\]

through the common internal range.

Thus a collision forces a local period `d` in the gap sequence. In ranges where two complete copies of the corresponding period block occur, this gives an ordinary square and hence an Abelian square.

**Important limitation.** Turning every possible collision pattern into a global lower bound on the number of **distinct** squares is not yet proved. The local periodicity implication is reliable; the desired global accounting theorem remains [O].

---

## 8. Existing fixed-`x` structural work [P / C]

### [P] Already fully formalized in `main.tex`

- Exact two-`a` count.
- Wing-escape lemma for four/five occurrences.
- `x=4` wing-deficit mechanism, central concentration, complete equality classification.
- `x=5` balancing lemma, run rigidity, complete equality classification.
- Computational verifier for the formalized `x=4,5` statements.

### [C] Derived in conversation, but not yet promoted to paper theorem

The following are promising but should **not** be cited as established results until written and audited line by line:

1. A general odd-balancing lemma extending the four-`a` balancing lemma to `2r`-`a` windows.
2. Endpoint/minimal-counterexample reductions based on the jump
   \[
   F(m)-F(m-1)=1\iff m\equiv2\pmod4.
   \]
3. Low-run (`5` / `6` runs) bridge-coverage arguments.
4. Proposed zero-slack / equality-rigidity mechanisms.

These should be treated as a research program rather than inserted into the main theorem list at present.

---

## 9. Finite experiments: strict additive-square avoidance creates large FMMS surplus [C: computational evidence]

The script `research_trimmed_additive.py` enumerates strict additive-square-free positive integer words and encodes them by `E(g)`. It then computes

\[
\operatorname{margin}(g)
=
\theta(E(g))-
\Bigl(F(|E(g)|_a)+F(|E(g)|_b)\Bigr).
\]

### Alphabet `{1,2,3}`

The additive-square-free tree dies at length 8. Minimum margins for lengths `1,...,7` are

\[
0,0,2,6,10,14,19.
\]

### Alphabet `{1,2,3,4}`

Through gap-word length 10, the numbers of additive-square-free words and minimum FMMS margins are:

| length | AS-free words | minimum margin |
|---:|---:|---:|
| 1 | 4 | 0 |
| 2 | 12 | 0 |
| 3 | 36 | 2 |
| 4 | 88 | 6 |
| 5 | 216 | 10 |
| 6 | 440 | 14 |
| 7 | 896 | 18 |
| 8 | 1626 | 30 |
| 9 | 2980 | 41 |
| 10 | 4692 | 46 |

This is striking evidence that **strict additive-square avoidance is not producing FMMS-like extremisers** in these small bounded-gap models. Instead, boundary-relaxed Abelian squares proliferate.

This is evidence only. It suggests a potentially important dichotomy:

> strict additive-square scarcity may force a large number of trimmed/split additive squares.

No uniform theorem of this kind is currently proved.

---

## 10. Candidate quantitative problems [O]

### Problem A: finite strict-vs-trimmed tradeoff

For a finite positive integer word `g` over a bounded alphabet, prove a lower bound of the form

\[
\#\{\text{trimmed/split square factor-words in }E(g)\}
\ge
\Psi(|g|,\sum g,\#\text{ strict additive squares of }g),
\]

where `Psi` becomes strong when the strict additive-square count is small.

A theorem of this form would explain the experimental surplus and could bypass the infinite PVHH problem rather than solve it.

### Problem B: extremal incompatibility

Prove that sufficiently long strict-additive-square-free gap words cannot encode FMMS minimisers; for example seek

\[
\theta(E(g))\ge F(|E(g)|_a)+F(|E(g)|_b)+c(|g|)
\]

with some positive (ideally growing) `c`.

Even `c=1` beyond an absolute length would already show that FMMS zero-slack words lie on the opposite side of the classical additive-square difficulty.

### Problem C: collision accounting for rank windows

Use Theorem 4.1 to lower-bound

\[
\sum_k |D_k(w)|
\]

directly. Repeated rank windows force gap periodicity; the missing step is a global injective/charging argument converting each distinctness loss into sufficiently many new periodic/power squares.

### Problem D: relation to BAS density

Cassaigne--Richomme--Saari--Zamboni relate infinite additive-square avoidance to a **positive-density set of Abelian-square-free starting positions**, whereas FMMS counts the number of **distinct Abelian-square factor-words** in a finite word. Determine whether there is a quantitative finite theorem connecting these two statistics.

This is conceptually the most direct bridge between the classical open problem and FMMS, but no such theorem is currently known to us.

---

## 11. What can safely go into a paper even if the quantitative theorem remains open?

Yes: failure to prove the full quantitative theorem would still leave a coherent and mathematically useful discussion section, provided the status is explicit.

A defensible paper narrative is:

1. prove `x=4,5` completely (current main result);
2. record the exact rank-window criterion as a general lemma;
3. explain the strict additive-square -> run-aligned Abelian-square injection;
4. cite the 2011 PVHH <-> BAS equivalence;
5. isolate the genuinely new gap: **FMMS counts distinct factor-words, while BAS/additive-square theory is primarily about occurrence/avoidance positions**;
6. formulate the finite strict-vs-trimmed tradeoff as an open problem motivated by the proofs and experiments.

This would be substantially better than claiming that the FMMS conjecture has been reduced to the classical additive-square problem. No such reduction is currently proved.

---

## 12. Current research judgement

The evidence points to a nuanced relationship:

- the two subjects are **structurally linked** through run-length encodings;
- strict additive squares form a **subclass** of the rank-window Abelian squares relevant to FMMS;
- the classical infinite avoidance problem is genuinely deep and remains open;
- small experiments suggest that avoiding strict additive squares may actually create **large surplus** in the FMMS statistic, so FMMS extremisers may live in a rigid regime far from additive-square-free words;
- the most promising new theorem is therefore not an equivalence with PVHH, but a **tradeoff theorem** between strict additive-square scarcity and trimmed/split-square abundance.

That tradeoff theorem is currently [O].

---

## 13. Post-audit correction: the n/2-scale isolated-a conjecture is false [P: counterexample]

A stronger conjecture considered during exploration was

\[
\theta(E(g))\stackrel{?}{\ge}\left\lfloor\frac{|E(g)|}{2}\right\rfloor-1
\]

for every positive gap word `g`. This is false. For example

\[
g=(11,1,1,8)
\]

gives a binary word of length `25` with only `10` distinct Abelian-square factor-words, whereas the proposed lower bound is `11`.

This failure is structurally informative: two large separated gaps contribute essentially the same family of pure powers `b^{2j}`, so an n/2-scale bound is too strong. The FMMS scale, roughly one quarter of the total mass, remains compatible with this example.

Accordingly, the n/2-scale conjecture is withdrawn and should not be used elsewhere.

---

## 14. Weakly monotone positive gaps [P]

Let

\[
E(g)=ab^{g_1}\cdots ab^{g_m},\qquad g_i\ge1.
\]

If the positive gaps are weakly monotone (nondecreasing or nonincreasing), then

\[
\boxed{\theta(E(g))\ge \left\lfloor\frac{|E(g)|}{2}\right\rfloor-1.}
\]

The proof groups equal consecutive gaps. Write, in the nondecreasing case,

\[
g=h_1^{r_1}h_2^{r_2}\cdots h_t^{r_t},\qquad h_1<\cdots<h_t.
\]

For `h>=1` put `P_h=ab^h`. If `P_h^L` occurs, then for every rank `k<L/2` there are

\[
C(h)=\left\lceil\frac{(h+1)^2}{2}\right\rceil
\]

distinct mixed Abelian squares with `2k` occurrences of `a`, obtained by choosing the two boundary trims `u,v in {0,...,h}` with `u+v congruent h (mod 2)`. If `L` is even, the top rank contributes at least

\[
B(h)=\left\lfloor\frac h2\right\rfloor+1.
\]

Thus

\[
\mu(h,L)\ge C(h)\left\lfloor\frac{L-1}{2}\right\rfloor
+\mathbf 1_{2\mid L}B(h).
\]

Every non-final constant block `h^r` is followed by a larger gap and hence supplies a factor `P_h^{r+1}`. The final block supplies `P_h^r`; adding the global pure `b`-squares gives the last missing boundary contribution. Using `C(h)>=h+1` one obtains

\[
\mu(h,r+1)\ge \left\lceil\frac{r(h+1)}2\right\rceil
\]

for non-final blocks and

\[
\mu(h,r)+\left\lfloor\frac h2\right\rfloor
\ge \left\lfloor\frac{r(h+1)}2\right\rfloor-1
\]

for the final block. Since mixed square words coming from different values of `h` have different internal gap lengths, their contributions are disjoint. Summing gives the claimed bound.

Consequently every weakly monotone positive-gap word satisfies the FMMS lower bound by a large margin in the non-boundary regime.

---

## 15. Mixed-square lower bound and amortized extension [C]

The next candidate is deliberately much weaker and better aligned with FMMS.

### Candidate M (mixed-square lemma)

For every positive gap word of length `m`,

\[
\boxed{\#\{Q\in\AS(E(g)):|Q|_a>0\}\ge m-1.}
\]

Exhaustive computation for `g_i in {1,2,3,4}` and `2<=m<=7` finds no counterexample. The minimum is exactly `m-1`, attained in that range by the constant word `g=(1,...,1)` (for `m>=3`). Random searches with much larger gaps also found no counterexample.

A one-step induction is false. Let `W_j=E(g_1,...,g_j)` and

\[
\Delta_j=|\AS_{mix}(W_j)\setminus\AS_{mix}(W_{j-1})|.
\]

For example `g=(4,1,1,1)` has increment pattern

\[
0,1,3,0,
\]

so one extension can create no new mixed factor-word. However exhaustive computation on the same finite range supports the stronger amortized statement

\[
\boxed{\Delta_j+\Delta_{j+1}\ge2.}
\]

If this two-step extension lemma is proved, Candidate M follows immediately by pairing extension steps.

The proof difficulty is global distinctness: a canonical square created at the new boundary may already have occurred earlier in the prefix. The promising mechanism is that such a collision records a repeated local gap pattern, and the preceding/following extension then appears to generate a higher-rank or conjugate square as compensation.

---

## 16. A more FMMS-aligned dispersion target [C/O]

Let

\[
S=\sum_i g_i,\qquad M=\max_i g_i.
\]

Pure `b`-squares contribute exactly `floor(M/2)`. The precise mixed deficit that remains to prove the isolated-`a` FMMS bound is

\[
D_{mix}=F(m)+F(S)-\left\lfloor\frac M2\right\rfloor.
\]

A computationally stable stronger candidate is

\[
\#\AS_{mix}(E(g))
\stackrel{?}{\ge}
(m-1)+\left\lfloor\frac{S-M-(m-1)}4\right\rfloor.
\]

Here `S-M-(m-1)` measures the excess `b`-mass outside the largest gap beyond the unavoidable baseline of one `b` per remaining gap. This candidate implies the isolated-`a` FMMS bound by an elementary floor calculation. It survived exhaustive tests for gaps in `{1,2,3,4}` through `m=7` and random tests with larger gaps, but no proof is currently known.

This formulation captures the current structural picture: concentration in one gap is paid by pure squares, while dispersion of the remaining mass should force additional mixed squares.

---

## 17. Constant-block charging and return compensation [P]

The mixed-square problem admits a clean reduction at the level of the **internal** gaps `g_1,...,g_{m-1}`. The final gap `g_m` is a positive right extension.

### Lemma 17.1 (constant internal block) [P]

Suppose `r` consecutive internal gaps are equal to `h>=1`. Then `E(g)` contains at least `r` distinct mixed Abelian-square factor-words whose consecutive internal `a`-gaps are all equal to `h`.

**Proof.** Put `P_h=ab^h` and `Q_h=b^h a`.

If `r=2t` is even, the block contains the ordinary squares

\[
P_h^{2},P_h^{4},\ldots,P_h^{2t}
\]

and

\[
Q_h^{2},Q_h^{4},\ldots,Q_h^{2t}.
\]

They are pairwise distinct (different lengths or different first letters), giving `2t=r` words.

If `r=2t+1` is odd, the same two families through exponent `2t` give `r-1` words. One more word is obtained as follows. If `h` is even, use `ab^h a`. If `h>1` is odd, use `ab^h ab`, which is available because every gap following an internal gap is positive. If `h=1`, then the positive gap after the block supplies one final `b`, so `(ab)^{r+1}` occurs; since `r+1` is even it is an ordinary square. In each case the extra word is distinct from the previous families. ∎

### Corollary 17.2 (no-return internal gaps) [P]

Assume that, for every integer value `h`, all occurrences of `h` among `g_1,...,g_{m-1}` form a single contiguous block. Then

\[
\#\AS_{mix}(E(g))\ge m-1.
\]

Indeed, apply Lemma 17.1 to each maximal constant block. Different block values `h` give disjoint square-word families because the common internal gap length is recoverable from the binary factor-word. The block lengths sum to `m-1`.

Thus the mixed-square candidate is already proved for every internal gap sequence with **no separated return to a previously used gap value**. The first genuinely new obstruction is therefore recurrence of the form

\[
h^{r}\;X\;h^{s},
\]

where `X` is nonempty and contains no `h` at its ends.

### Lemma 17.3 (single-gap return compensation) [P]

If the internal gap sequence contains

\[
h^r\,x\,h^s,\qquad x\ne h,
\]

then it forces at least `min(r,s)` distinct mixed Abelian squares whose internal gap strings are nonconstant.

For `1<=t<=min(r,s)`, take the consecutive internal gap window

\[
h^t\,x\,h^t.
\]

It has odd length and is symmetric about the central gap `x`. The corresponding binary factor contains an even number of `a`'s. If `x` is even, the factor ending at the final `a` is an Abelian square; if `x` is odd, append one `b` from the positive following gap. The two halves then have equal numbers of both letters. Different `t` give different ranks, hence distinct square words.

This exactly compensates the possible overlap of the constant-block families from the two `h`-blocks: the overlap can be at most `min(r,s)` words, and Lemma 17.3 supplies that many new heterogeneous words.

### Lemma 17.4 (balanced odd separator) [P]

More generally, let

\[
X=(x_1,\ldots,x_d,c,y_1,\ldots,y_d)
\]

have odd length and satisfy

\[
\sum_{i=1}^{d}x_i=\sum_{i=1}^{d}y_i.
\]

If the internal gap sequence contains `h^r X h^s`, then for every `1<=t<=min(r,s)` the window `h^t X h^t` yields a mixed Abelian square. Again, if the central gap `c` is odd, one trailing `b` supplies the parity correction. Hence such a balanced separator gives at least `min(r,s)` return-compensation squares.

This is the additive analogue of the palindromic special case. It shows precisely where the classical additive structure enters: a separated return to the same gap value is harmless whenever the intervening odd block is additively balanced around its center.

### Lemma 17.5 (good center for an arbitrary separator) [P]

Let `h>=1` and let `X=(x_1,...,x_ell)` be any positive integer word. For `1<=j<=ell` define

\[
D_j=h(\ell-2j+1)+\sum_{i<j}x_i-\sum_{i>j}x_i.
\]

Then there is an index `j` such that

\[
\boxed{|D_j|\le h+x_j.}
\]

**Proof.** Consecutive values satisfy

\[
D_{j+1}-D_j=x_j+x_{j+1}-2h.
\]

If no `j` satisfies the displayed bound, each `D_j` lies either strictly above `h+x_j` or strictly below `-(h+x_j)`. It cannot jump from the upper region to the lower region, because such a jump would be smaller than `-2h-x_j-x_{j+1}`, whereas the actual increment is `x_j+x_{j+1}-2h`; the reverse jump is similarly impossible. Hence all `D_j` would have to lie on the same side.

Writing `T=sum X`, the two endpoint values are

\[
D_1=h(\ell-1)-T+x_1,
\qquad
D_\ell=T-x_\ell-h(\ell-1).
\]

If both were above their upper bands, the first inequality would give `T<h(ell-2)` while the second would give `T>h ell+2x_ell`, a contradiction. If both were below their lower bands, the second gives `T<h(ell-2)` while the first gives `T>h ell+2x_1`, again a contradiction. ∎

### Corollary 17.6 (quantitative arbitrary-return bridge) [P]

Suppose the internal gap sequence contains

\[
h^r\,X\,h^s,
\qquad |X|=\ell.
\]

Choose a good center `j` from Lemma 17.5 and put

\[
d=\ell-2j+1,
\qquad
\alpha_0=\max(d,0),
\qquad
\beta_0=\max(-d,0).
\]

For every integer `t>=0` with

\[
\alpha=\alpha_0+t\le r-1,
\qquad
\beta=\beta_0+t\le s-1,
\]

take the internal gap window consisting of `alpha` copies of `h`, then all of `X`, then `beta` copies of `h`. The chosen value of `d` makes `x_j` the central gap in the `a`-count sense. The left/right internal `b`-sum discrepancy is exactly `D_j`. Since one unused `h`-gap remains on each side, both outer trim budgets equal `h`; the exact rank-window criterion and `|D_j|<=h+x_j` therefore give an Abelian square. Different `t` give different ranks.

Consequently this return forces at least

\[
1+\min(r-1-\alpha_0,\ s-1-\beta_0)
\]

bridge squares whenever the right side is nonnegative. In particular, uniformly in the separator,

\[
\boxed{
N_{bridge}\ge
\max\{0,\min(r,s)-\ell+1\}.
}
\]

Thus an arbitrary separator of length `ell` can leave at most `ell-1` units of the naive `min(r,s)` overlap uncompensated, regardless of how long the two returning constant blocks are.

### Remaining return gap [O]

The genuinely difficult regime is therefore no longer a long return block: it is a return for which the separator length is comparable to the shorter returning block. Equivalently, after the universal bridge charging above, the unresolved loss is controlled by the **complexity/length of the separator itself**, not by `r` or `s`.

This suggests a recursive stability statement: the residual `ell-1` loss should be paid by surplus squares internal to `X` whenever all good centers are forced far from the middle. Proving such a separator-surplus inequality is the current sharp form of the oscillation gap.

---

## 18. Absence of rank two forces low-rank explosion [P]

Let `D_2(E(g))` denote the set of Abelian-square factor-words containing exactly four occurrences of `a`. Assume `m>=4` and

\[
D_2(E(g))=\varnothing.
\]

For the rank-two window starting at the `i`-th `a`, define

\[
\Delta_i=(g_i+g_{i+1})-(g_{i+2}+g_{i+3}),
\qquad 1\le i\le m-3,
\]

with left trim budget `p_i=g_{i-1}` for `i>1` and `p_1=0`. The exact positive-gap window criterion says that this window contains a rank-two Abelian square iff

\[
-(p_i+g_{i+3})\le \Delta_i\le 2g_{i+1}.
\]

Hence, under `D_2=empty`, every `Delta_i` lies in one of the two forbidden regions. The sign-change lemma for consecutive windows implies that all `Delta_i` lie on the same side.

### Descending forbidden side

If

\[
\Delta_i>2g_{i+1}
\]

for every `i`, then

\[
\boxed{g_i>g_{i+1}+g_{i+2}+g_{i+3}}
\tag{18.1}
\]

for `1<=i<=m-3`. In particular

\[
g_1>g_2>\cdots>g_{m-2},
\]

and `g_1` is the global maximum (the last inequality in (18.1) also gives `g_{m-3}>g_{m-1},g_m`).

Pure `b`-squares contribute `floor(g_1/2)`. For every internal gap `g_i`, `2<=i<=m-2`, the left gap is larger than `g_i`; setting the right trim to zero and varying the left trim through

\[
0\le u\le g_i,\qquad u\equiv g_i\pmod 2,
\]

produces `floor(g_i/2)+1` distinct rank-one square words. These families are disjoint because their central internal gaps are the distinct values `g_2,...,g_{m-2}`. Hence

\[
\theta(E(g))\ge
\sum_{i=1}^{m-2}\left\lfloor\frac{g_i}{2}\right\rfloor+(m-3).
\tag{18.2}
\]

Put

\[
A=\sum_{i=1}^{m-2}g_i,\qquad
T=g_{m-1}+g_m,\qquad
S=A+T.
\]

From (18.1) at `i=m-3` and positivity,

\[
A\ge T+m-1.
\tag{18.3}
\]

Using `sum floor(g_i/2) >= (A-(m-2))/2`, (18.2) gives

\[
\theta(E(g))\ge \frac{A+m-4}{2}.
\tag{18.4}
\]

For `m>=7`, (18.3) implies

\[
\frac{A+m-4}{2}
\ge
\frac{S+m+4}{4}
\ge
F(S)+F(m).
\]

For `m=6`, the recurrence is much stronger than (18.3): from `g_3>g_4+g_5+g_6`, together with `g_2>g_3` and `g_1>g_2`, one gets `A-T>=14`, which again makes the displayed comparison strict. The cases `m=4,5` are already covered by the complete fixed-`x` theorems in `main.tex`.

### Ascending forbidden side

If instead every window lies below the lower endpoint, then

\[
\boxed{g_{i-1}+g_i+g_{i+1}<g_{i+2}}
\tag{18.4}
\]

(with `g_0=0`). Thus `g_2<g_3<\cdots<g_{m-1}` and `g_3>g_1`. Put

\[
H=g_{m-1},\qquad q=g_m,\qquad M=\max(H,q).
\]

The pure squares contribute `floor(M/2)`. For each `2<=i<=m-2`, the right gap is larger than `g_i`, so setting the left trim to zero and varying the right trim produces `floor(g_i/2)+1` rank-one square words. Their central gaps `g_2,...,g_{m-2}` are distinct. Hence, with

\[
A=M+\sum_{i=2}^{m-2}g_i,
\qquad
U=g_1+\min(H,q),
\qquad
S=A+U,
\]

we have

\[
\theta(E(g))\ge \frac{A+m-4}{2}.
\tag{18.5}
\]

Moreover

\[
A-U\ge \sum_{i=2}^{m-2}g_i-g_1\ge m-2
\]

for `m>=5`, because `g_3>=g_1+g_2+1` and all remaining gaps are positive. Therefore (18.5) implies the FMMS bound for `m>=7`. For `m=6`, the next recurrence `g_4>g_1+g_2+g_3` strengthens the last estimate to `A-U>=9`, which is again sufficient. The cases `m=4,5` are covered by the fixed-`x` results in `main.tex`.

Thus in the ascending forbidden branch as well,

\[
\theta(E(g))\ge F(S)+F(m).
\]

Therefore

\[
\boxed{
D_2(E(g))=\varnothing
\quad\Longrightarrow\quad
\theta(E(g))\ge F(m)+F(S).
}
\]

This is the first rigorous instance of the desired compensation principle

\[
\text{missing higher rank}\Longrightarrow\text{low-rank explosion}.
\]

It is stronger conceptually than the bounded-gap every-rank theorem: the latter forces rank two to appear in long bounded-gap words, while the present result shows that if rank two is absent because the gaps are unbounded/strongly dispersed, then pure and rank-one squares already pay the FMMS target.
