# Full readability and style audit — August 9, 2026

## Executive assessment

The manuscript has a strong mathematical spine, but the previous version read too much like a compressed technical dossier. The main difficulty was not English grammar. It was **loss of narrative continuity when changing mathematical languages**:

1. nodal surfaces -> strict even-node codes;
2. code weights -> residual overlap patterns;
3. weight 64 -> quartic complete intersections and symmetric determinants;
4. overlap patterns -> simultaneous determinant nets;
5. determinant nets -> blow-ups and maps to quadrics;
6. degenerate comparison -> canonical modules / Beilinson--Horrocks data.

Each individual step is mathematically motivated, but several transitions were implicit. A reader who is not already familiar with the entire project could understand each displayed calculation while still losing sight of why that calculation was being made.

The current revision therefore treats readability as a structural problem rather than a cosmetic one. The guiding principle is:

> Before changing mathematical language, say what information is being translated, why the new language is more rigid, and what the next obstruction is supposed to prove.

The main text has been edited accordingly.

---

## 1. Major revisions already applied

### 1.1 Abstract: restored the extremal problem and translated residual numbers

The abstract now starts from

\[
168\le u(8)\le174,
\qquad \text{with the target }u(8)=168,
\]

and explains why a hypothetical 169-node octic leads to an 8-divisible code with minimum weight in

\[
\{48,64,72\}.
\]

The earlier abstract introduced 64, 533, residual 32/36, and six-quartic maps before telling the reader why any of these numbers mattered. The revised version now explicitly explains that residual distances 32 and 36 correspond to **two weight-64 supports meeting in 32 and 28 nodes**, respectively.

This is a major improvement: the reader now sees a geometric overlap before seeing the residual-code label.

### 1.2 Introduction: added a proof dictionary

A new subsection, `A dictionary for the proof`, explains the recurring translations:

- strict even set <-> binary codeword;
- Hamming weight <-> number of nodes;
- residual weight <-> overlap pattern with a chosen support;
- weight 64 <-> transverse `CI(4,4,4)` + symmetric 2x2 determinant;
- comparison of codewords <-> comparison of quartic determinant nets;
- blow-up of the common block <-> removal of the base locus of the combined quartic system;
- quadratic relation among six quartics <-> image in a quadric fourfold.

This subsection should substantially reduce the perceived jump between coding theory and projective geometry.

### 1.3 Section 2: made the code self-contained

The manuscript previously introduced the strict even-node code without giving the geometric definition in the body of the paper. The revised text now defines:

- the minimal resolution;
- exceptional curves `E_p`;
- strict even subsets as 2-divisible sums of exceptional curves;
- symmetric difference as the code addition;
- Hamming weight as the number of nodes;
- 8-divisibility in the octic case.

The hyperplane class `H` is also explicitly defined and the convention of reusing `H` for pullbacks is stated.

This fixes a genuine first-principles readability issue.

### 1.4 Weight-72 branch: added the strategy before the certificate

The section now tells the reader, before any Krawtchouk polynomial appears, that the plan is:

- residual words have two lifts;
- the octic spectrum leaves finitely many allowed lift states;
- construct a polynomial nonpositive on every nonzero allowed state;
- MacWilliams averaging forces the same polynomial to have a larger positive average;
- contradiction.

The exact certificate remains unchanged. What changed is that the reader now knows what role it plays.

### 1.5 Weight-64 determinant theorem: explained why a codeword becomes geometry

A new transition paragraph explains:

- the weight-64 word gives a half-divisor on the resolution;
- Riemann--Roch produces sections of a degree-four system;
- Endrass' stability analysis turns these sections into three quartics;
- the three quartics satisfy a 2x2 symmetric determinant identity.

The term `binary symmetric determinantal representation` was replaced by the clearer `symmetric 2x2 determinantal representation`, avoiding ambiguity with binary forms or binary codes.

### 1.6 First residual classification: translated residual distance into intersection size

The section now explicitly says that the residual code measures how other even sets meet the support of the chosen base word. The formulas

\[
\operatorname{wt}(x)=r+a,
\qquad
\operatorname{wt}(x+c)=r+64-a
\]

are therefore introduced as an overlap dictionary, not merely as bookkeeping.

### 1.7 Residual triangle: gave the geometric picture first

The revised opening explains that residual distance 32 means:

- two weight-64 words meet in 32 nodes;
- their sum is another weight-64 word;
- the three supports are pairwise unions of three disjoint 32-point blocks;
- each support carries a quartic determinant net;
- the real problem is simultaneous coexistence of three determinant presentations of the same octic.

This is exactly the kind of conceptual picture that was missing before.

### 1.8 Blow-up subsection: explained why the blow-up is introduced

The new paragraph states that the two quartic nets define only a rational map on `P^3` because all sections vanish on the common block. Blowing up separates first-order directions at those points and makes the system base-point free.

Thus the blow-up is no longer introduced as a formal device without motivation.

### 1.9 Hundreds of determinant presentations: explained the local-to-global role

The opening now distinguishes:

- local residual classification around one minimum word;
- global abundance of minimum words forced by MacWilliams;
- incidence counting as a **selection principle** for choosing a geometrically favorable pair.

This is important because the theorem `A_64 >= 533` is not merely a coding statistic; it is what allows the geometry to ignore the 40A/40B local profiles globally.

### 1.10 Residual 36: reorganized the reading path

The section now begins with the actual geometric picture:

- two weight-64 determinant sets meet in 28 nodes;
- disjoint determinant nets give six quartics;
- the two determinant equations yield one quadratic relation;
- after blowing up the common base locus, the map lands in a quadric fourfold;
- intersection theory controls the image degree.

The sheet bound, Euler-deficit lemma, and invariant-Lagrangian classification are now grouped under `Three auxiliary tools`, with an explicit note that a first-time reader may skip them and go directly to the main six-quartic theorem.

A new subsection `The six-quartic map` then returns the reader to the main line.

### 1.11 Degenerate residual-36 tools: separated from the main line

The canonical-module / Jacobian-defect material is now placed under

`Local obstructions for the degenerate outlets`.

The text explicitly says that these tools are not part of the degree calculation for the generic six-quartic map. This prevents the reader from interpreting J1/J2 as another unexplained step in the main proof.

### 1.12 Beilinson--Horrocks paragraph: removed internal project terminology

The visible manuscript previously referred to a `Smith--Cartan divisor` without defining it, while the detailed Smith/QT material is excluded from the submission by `\iffalse`. This created a dangling reference to the research process.

The paragraph has been rewritten in terms of the actual visible input: a Casnati--Catanese object, a degree-eight defect, and a coupled degree-0/1 Beilinson--Horrocks block.

### 1.13 Weight 48: explained the different geometric object

The opening now contrasts the two branches:

- weight 64 -> determinant net of quartics;
- weight 48 -> unique reduced contact quadric.

The trade-off

\[
A_{64}+21A_{48}\ge533
\]

is then explained conceptually: if the code does not contain many contact quadrics, it must contain many weight-64 determinant presentations.

### 1.14 Removed manuscript-as-audit wording

Visible `Audit warning` environments have been renamed `Caution`, and phrases such as `legacy input`, `former input`, and `silently delete` have been replaced by normal mathematical prose.

This matters for journal presentation. The paper should read as a finished argument, not as a record of how the argument was debugged.

---

## 2. Current readability assessment by section

### Abstract — GOOD after revision

The mathematical hierarchy is now visible:

`u(8)=168? -> hypothetical 169 nodes -> divisible code -> 48/64/72 -> branch results -> remaining cases`.

The abstract is still technical, but appropriately so for JAG. It now explains the meaning of the main residual numbers instead of merely listing them.

### Introduction — GOOD

The new dictionary is the most important readability improvement in the paper. It should remain even if the manuscript is shortened later.

Recommendation: do not compress this subsection away during final page reduction.

### Even-node codes and uniform reduction — GOOD

Now sufficiently self-contained for a reader who knows nodal surfaces but not this exact coding convention.

### Weight 72 — GOOD

The proof is computational in spirit but conceptually clean. The finite certificate is reproduced in the appendix and the averaging contradiction is transparent.

### Weight 64 determinant presentation — GOOD, citation-sensitive

The narrative is now clear, but the proof relies heavily on the exact hypotheses and terminology of Endrass, especially the transition

`h^0(L)>=2 -> nonstable degree-four system -> unstable alternative -> determinant construction`.

This is not a stylistic defect, but for submission the precise correspondence with the cited propositions should be checked one more time. A referee is likely to inspect this theorem carefully because it is the main bridge from coding theory to projective geometry.

### First residual classification — GOOD

This section is elementary and readable once the overlap interpretation is stated.

### Residual triangle — MODERATELY DENSE but now navigable

This remains the densest part of the manuscript. The main conceptual path is now visible, but the subsection contains several different techniques:

- split MacWilliams;
- determinant-net intersection;
- blow-up intersection theory;
- Hilbert vectors;
- liaison;
- contact quadrics/cubics;
- low-rank quadratic relations.

The section is mathematically coherent, but it asks a lot from the reader. The present signposting is probably the minimum acceptable level.

### Hundreds of determinant presentations — VERY GOOD

This is one of the clearest sections and should be treated as the global pivot of the paper.

### Residual 36 — DENSE but structurally improved

The new auxiliary-tool/main-map division is important. Without it, the invariant-Lagrangian lemma appeared before the reader knew why invariant Lagrangians mattered.

### Local Jacobian / Beilinson--Horrocks tools — STILL SPECIALIZED

These results are now better framed, but they remain somewhat detached from the central theorem chain. If the paper needs shortening, this is the first material I would consider moving to an appendix or supplementary note unless it is explicitly used to close one of the stated surviving outlets before submission.

### Weight 48 — GOOD

The contact-quadric picture gives this branch a clear identity. The trade-off theorem is a natural global replacement for a nonexistent abundance theorem for weight 48.

### Consequences and open cases — GOOD

The manuscript is commendably explicit about what is not proved. This should remain.

---

## 3. Proof-presentation points that deserve one more mathematical check

These are not newly discovered contradictions. They are places where the current exposition compresses a nontrivial mathematical assertion enough that a referee may ask for more detail.

### A. Endrass stability input in the automatic weight-64 determinant theorem

The theorem depends on several cited implications from Endrass. The current proof is plausible and well organized, but the exact proposition hypotheses should be checked against the notation `v=4`, `s=8`, strict versus weak even sets, and the semistable/unstable alternatives.

**Priority: high**, because this theorem supports essentially all later weight-64 geometry.

### B. Rank-three pencil plane counts in residual 36

In the finite quadratic-target argument, five rank-three Jordan types are listed, followed by assertions that some types have two target planes and one type has exactly four. These are described as direct invariant-isotropic calculations but are not expanded into a separate lemma in the visible manuscript.

A referee could reasonably request the finite calculation.

**Recommendation:** either add a short lemma analogous to the rank-four invariant-Lagrangian lemma or place a complete table in an appendix.

**Priority: medium-high.**

### C. Orientation statement in J2

The relation

\[
J_E(p)=\varepsilon_p\lambda J_Z(p),\qquad \varepsilon_p\in\{\pm1\}
\]

is conceptually important for the local saturation defect, but the reason the pointwise ratios reduce to signs times one global scalar is compressed.

If J2 remains in the journal version, add a sentence or reference explaining the orientation normalization.

**Priority: medium.**

### D. Beilinson--Horrocks obstruction is not part of the main theorem chain

The theorem is now more self-contained stylistically, but its role in the final reduction is still secondary. If it remains unused in the main conclusion, consider moving it out of the core narrative.

**Priority: medium, editorial rather than mathematical.**

### E. Computational certificates

The current handling is good: exact arithmetic, explicit finite state counts, appendix values, and independent scripts. For a journal submission, make sure the supplementary package has a stable archival location and that every computational theorem has an exact theorem-to-script map.

**Priority: medium.**

---

## 4. Style principles for the final manuscript

The following style should be preserved throughout final revisions.

### Prefer geometric nouns over project-internal labels

Use:

- `common block`, `overlap pattern`, `quartic net`, `contact quadric`, `six-quartic map`, `target threefold`.

Avoid in the visible paper unless fully defined:

- `legacy route`, `QT outlet`, `Smith-border outlet`, `regular comparison package`, `audit input`, `closure route`.

Those labels are useful in research notes but not in a journal article.

### Translate every important number once

Examples:

- residual 32 = 32 common nodes of two weight-64 supports;
- residual 36 = 28 common nodes;
- 533 = forced abundance of determinant presentations;
- 28 exceptional planes = one for each blown-up common node.

After the translation has been given once, technical notation can be used freely.

### State the purpose before a long calculation

Good pattern:

> We now show that the target degree has only two possibilities. Since `D^3=36`, it is enough to compare the degree of the image with the degree of the map.

Then perform the calculation.

This is preferable to presenting three intersection formulas and only afterward explaining what they were meant to constrain.

### Distinguish main line from auxiliary technology

The manuscript now does this in residual 36. The same principle should be kept if more technical material is added later.

### Do not over-explain routine algebra

The goal is not textbook exposition. The intended reader can follow MacWilliams identities, adjunction, liaison, and blow-up intersection formulas. The extra prose should explain **why the tool appears**, not every algebraic manipulation.

---

## 5. Overall journal-readability verdict

Before this revision, the manuscript had a genuine accessibility problem: it was possible to read several pages correctly while not knowing how the current calculation advanced the `u(8)=168` program.

After the structural edits, the paper is much closer to a coherent JAG-style research article. The main argument can now be summarized as a single chain:

\[
\text{hypothetical }\nu\ge169
\Longrightarrow
8\text{-divisible code}
\Longrightarrow
d(K)\in\{48,64,72\}
\]

with

- `72`: MacWilliams contradiction;
- `64`: determinant presentations -> many presentations -> residual 32/36 comparison geometry;
- `48`: contact quadrics -> 48/64 abundance trade-off.

The remaining weakness is no longer the overall exposition. It is concentrated in a few very specialized local arguments, especially the rank-three pencil calculation and the Jacobian/Beilinson--Horrocks material. Those should be treated as targeted proof-presentation tasks rather than another global rewrite.

## Follow-up proof-presentation pass completed

The three items identified above have now been addressed directly in `main.tex`.

1. **Endraß chain:** the weight-64 determinant proof now derives `h^2(L)=h^0(L)` explicitly from Serre duality and Lemma 4.1, identifies the stability notion as Endraß' quadratic-contact-system terminology, separates the stable/semistable/unstable alternatives of Definition 3.1 and Proposition 3.3, and explains why the degree-four semistable case would force a reduced contact quadric. The application of Proposition 3.6 now records `2v-s=0` and explains why the scalar is nonzero in the unstable alternative.
2. **Rank-three pencil:** the former phrase `a direct invariant-isotropic calculation` has been replaced by a standalone lemma giving the five possible Jordan types and explicitly classifying the invariant Lagrangian three-spaces needed in the finite normal quadratic-target proof. The main theorem now cites this lemma and performs sheet counting only along lines with smooth generic point.
3. **J2 orientation:** the global scalar and pointwise signs are now derived from the determinant of the quadratic tangent cone. For each determinant net, the Hessian determinant at a common node is the determinant of the ternary determinant form times the square of the complete-intersection Jacobian, up to a common convention factor. Hence `J_E(p)^2/J_Z(p)^2` is independent of `p`, giving the required global scalar and intrinsic sign pattern.

After these changes the submission build succeeds, and the full submission test suite still passes. The remaining open issues recorded in the paper are mathematical outlets of the `u(8)` problem, not unexplained transitions in the exposition.