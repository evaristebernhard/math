# Submission audit — 2026-08-09

Manuscript: **Binary Words with Few Abelian Squares: Four and Five Occurrences of a Letter and Run-Length Structure**

## 1. Submission-level mathematical status

The paper currently proves the following results at theorem level:

- the exact minimum for four occurrences of one letter,
  \[
  M(4,4)=2,\qquad M(4,n)=1+\left\lfloor\frac{n-2}{4}\right\rfloor\quad(n\ge5),
  \]
  together with a complete classification of minimisers;
- the exact minimum for five occurrences,
  \[
  M(5,5)=2,\qquad M(5,n)=\left\lfloor\frac{n+1}{4}\right\rfloor\quad(n\ge6),
  \]
  together with a complete classification of minimisers;
- run rigidity for the five-occurrence case: a minimiser has at most two runs of the minority letter;
- an exact rank-window criterion for positive-gap encodings `E(g)`;
- the lower bound
  \[
  \vartheta(E(g))\ge \left\lfloor\frac{m+S}{2}\right\rfloor-1
  \]
  for weakly monotone positive gaps;
- the conjectured fixed-Parikh lower bound for positive-gap words with no rank-two (four-minority-letter) Abelian square.

The manuscript does **not** prove the general fixed-Parikh conjecture and does not treat the complete case `x=6`. The general run-length results are stated only for the positive-gap encoding and should not be described as a theorem for arbitrary boundary-gap words.

The long run-rigidity proof and the integer optimisations remain conventional mathematical proofs. The finite verifier is an audit, not a formal proof.

## 2. Verification status

`npm test` currently runs 14 submission-level checks. At the 2026-08-09 audit all 14 passed.

The detailed finite ranges and theorem-to-test correspondence have been moved to `SUPPLEMENTARY_VERIFICATION.md`. Research scripts beginning with `research_` are explicitly excluded from the submission-level verification package.

## 3. Literature and framing changes

The Introduction now distinguishes the present extremal counting problem from classical Abelian-power avoidance. References to Dekking and Keränen have been added as historical background.

The discussion of the additive-square problem now cites the original Pirillo--Varricchio and Halbeisen--Hungerbühler papers directly, together with Rao--Rosenfeld for a later variant. The bibliography now contains sources actually used in the text rather than relying on a short secondary list.

No claim is made that the rank-window method solves the general conjecture. The final Discussion identifies the intermediate multi-rank regime as open.

## 4. Computational material

The previous research-log-style paragraph listing every enumeration range has been shortened in the manuscript. The detailed ranges are now in the supplementary manifest.

Recommended submission supplement:

- `test_verifier.py`;
- `SUPPLEMENTARY_VERIFICATION.md`.

Exploratory files such as `research_x6*.py`, `research_trimmed_additive.py`, and research notes should not be uploaded as proof material.

## 5. Elsevier-specific preparation for Discrete Mathematics

The current manuscript already has:

- a concise abstract below 250 words;
- five English keywords;
- MSC 2020 codes;
- editable LaTeX source;
- editable tables;
- no figures requiring separate artwork files;
- a supplementary-computation statement;
- a generative-AI disclosure section before the references;
- a separate `HIGHLIGHTS.txt` with four short bullet points.

The bibliography format is consistent and may be left in the current numbered style for initial submission.

## 6. Recommended first target

Because the authors prefer a conservative submission rather than a higher-risk attempt, the recommended first target is now **International Journal of Foundations of Computer Science (IJFCS)**.  Its scope includes formal languages and combinatorics, and the present manuscript is naturally presented as a finite-word extremal/combinatorial paper.  Current public 2025/2026 indexing summaries place IJFCS in SCIE Q4 and Chinese Academy of Sciences category 4.  This is therefore a deliberately conservative choice rather than an attempt to maximise journal ranking.

No journal should be described as guaranteed acceptance.  The reason for preferring IJFCS here is the combination of topical fit and a lower expected selectivity than the previously considered Discrete Mathematics or Journal of Combinatorial Theory, Series A.

If the authors still want a venue around category 3 while remaining close to combinatorics on words, **RAIRO -- Theoretical Informatics and Applications** is a possible intermediate choice.  Its current scope explicitly lists combinatorics on words, but its annual article volume is small and its public partition status has changed across recent editions, so it should not be treated as a risk-free option.

**Discrete Mathematics** remains a reasonable stronger fallback if the authors later decide to accept more editorial risk.

## 7. Author metadata

The manuscript now records the author information supplied by the authors:

- **Jizheng Chen**, Department of Mathematics, Chang'an University, `1253183582@qq.com`;
- **Chaoyu Hu**, School of Automation, Hangzhou Dianzi University, `evaristebernhardwiener@gmail.com`, corresponding author.

The manuscript title block now uses a compact journal-style presentation: author names in the title area, with department/university, city/postcode/country, email, and corresponding-author status in author footnotes. Full street addresses are retained for Editorial Manager metadata and need not be printed in the title block. Before submission, the authors still need to supply any funding/grant information required by the journal system and confirm that both authors approve the submitted version and that the manuscript is not under consideration elsewhere.

## 8. Current recommendation

After the final PDF and supplementary files are rebuilt, the paper is suitable for a conservative first submission to **International Journal of Foundations of Computer Science**.  The submission should be presented factually as an exact treatment of the fixed-minority cases `x=4,5` with additional positive-gap results, not as a solution of the general FMMS conjecture.
