# IJFCS submission checklist — 2026-08-09

Target journal: **International Journal of Foundations of Computer Science (IJFCS)**, World Scientific.

## 1. Submission portal

Current submission portal used for IJFCS:

`https://www.editorialmanager.com/IJFCS`

The journal publishes theoretical work in foundations of computer science, including automata/formal languages and combinatorics, so the manuscript topic is within the journal's stated subject range.

## 2. Files to prepare for the first submission

Primary manuscript:

- `main.pdf`

Source files to keep ready if requested by the system or after acceptance/revision:

- `main.tex`
- `references.bib`

Supplementary verification material:

- `test_verifier.py`
- `SUPPLEMENTARY_VERIFICATION.md`

Do **not** upload the exploratory files as proof material:

- `research_notes_*.md`
- `research_x6*.py`
- `research_trimmed_additive.py`
- other files beginning with `research_`

A previous `HIGHLIGHTS.txt` was prepared for an Elsevier target; it is not part of the IJFCS submission package unless the submission system explicitly asks for highlights.

## 3. Manuscript metadata

Title:

**Binary Words with Few Abelian Squares: Four and Five Occurrences of a Letter and Run-Length Structure**

Authors:

1. **Jizheng Chen**  
   Department of Mathematics, Chang'an University  
   Middle Section of South Second Ring Road, Xi'an, Shaanxi 710064, People's Republic of China  
   Email: `1253183582@qq.com`

2. **Chaoyu Hu** — corresponding author  
   School of Automation, Hangzhou Dianzi University  
   No. 1158, No. 2 Street, Baiyang Subdistrict, Qiantang District, Hangzhou, Zhejiang 310018, People's Republic of China  
   Email: `evaristebernhardwiener@gmail.com`

Keywords:

- Abelian square
- combinatorics on words
- Parikh vector
- extremal word
- binary word

MSC 2020:

- 68R15
- 05A05

## 4. Cover letter

Use:

- `COVER_LETTER_IJFCS.md`

The letter deliberately states only the proved results:

- exact values of `M(4,n)` and `M(5,n)`;
- complete minimiser classifications;
- five-occurrence run rigidity;
- positive-gap rank-window and two sufficient regimes for the fixed-Parikh lower bound.

It explicitly does **not** claim the general FMMS fixed-Parikh conjecture.

## 5. Verification status

Latest local verification:

- `npm run build`: PASS;
- `npm test`: 14/14 checks PASS;
- current PDF: 27 pages;
- no unresolved references/citations or overfull boxes in the final build.

The finite computations are supplementary audits only; all theorem statements have written proofs in the manuscript.

## 6. Items to enter or confirm in Editorial Manager

When creating the submission, enter the authors in the same order as the manuscript and mark **Chaoyu Hu** as corresponding author.

The portal may request additional metadata that are not part of the PDF, such as:

- author accounts / ORCID, if available;
- funding information, if any;
- conflict-of-interest / originality declarations;
- confirmation that the manuscript is not under consideration elsewhere;
- suggested reviewers or opposed reviewers, if the form asks for them.

These should be answered factually by the authors; do not invent funding, ORCID, reviewer conflicts, or institutional details.

## 7. Positioning

The submission should be described as an exact treatment of the fixed-minority cases `x=4` and `x=5`, with additional results for positive-gap run-length encodings.

Avoid claims such as:

- solving the general fixed-Parikh conjecture;
- establishing a general theory of Abelian-square minimisation;
- proving the `x=6` case;
- claiming that the computational verifier constitutes a proof.

## 8. Current status

The manuscript is prepared for an IJFCS first submission. The only remaining author-side items are any funding information and the routine declarations/questions presented by Editorial Manager during submission.
