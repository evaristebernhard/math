# JAG submission package checklist — 2026-08-09

## Manuscript identity

**Title:** Low-weight even sets of nodes on octic surfaces: divisible codes, symmetric determinants, and comparison geometry

**Authors:**
- Jizheng Chen — Department of Mathematics, Chang'an University, Middle Section of South Second Ring Road, Xi'an, Shaanxi 710064, People's Republic of China — 1253183582@qq.com
- Chaoyu Hu — School of Automation, Hangzhou Dianzi University, No. 1158, No. 2 Street, Baiyang Subdistrict, Qiantang District, Hangzhou, Zhejiang 310018, People's Republic of China — evaristebernhardwiener@gmail.com

**Corresponding author:** Chaoyu Hu

**MSC 2020:** Primary 14J17; Secondary 14J70, 14M12, 94B05.

**Keywords:** nodal octic surface; even set of nodes; divisible code; symmetric determinantal representation; complete intersection; MacWilliams identities.

## Submission-status checks

- Initial manuscript: submit the compiled PDF.
- The manuscript must not be simultaneously under consideration elsewhere.
- The AMS submission instructions request 2020 Mathematics Subject Classification information; this is now included in `main.tex`.
- Full postal affiliations and email addresses are now included.
- The current manuscript uses `amsart` and compiles without unresolved citations or cross-references.
- The exact computational material is separated from exploratory research scripts and documented in `SUPPLEMENTARY_COMPUTATIONAL_CERTIFICATES.md`.

## Statements

### Funding

Do not insert a funding statement until the authors confirm the actual funding situation.

If there was no external funding and the submission form requires a declaration, use:

> The authors received no external funding for this work.

If either author was supported by a grant, replace this with the exact funder and grant number.

### Competing interests

No competing-interest paragraph is currently inserted in the manuscript because the journal-specific author page does not appear to require one in the article text.  If the submission system asks for a declaration and there are no conflicts, use:

> The authors declare that they have no competing interests.

### Author contributions

A CRediT statement is not currently inserted.  For a two-author pure-mathematics paper it should be added only if requested by the submission system or if the authors want to record a division of work.  Do not invent a contribution split without both authors' agreement.

### Data and code availability

There is no empirical dataset.  The appropriate reproducibility statement concerns exact computational certificates rather than “data”.  Suggested wording if the submission system asks:

> Machine-readable exact certificates and verifier scripts supporting the finite coding computations are provided as supplementary material.  No empirical dataset is used in this work.

### Generative-AI disclosure

No explicit JAG/AMS journal-specific generative-AI disclosure rule was located in the official material checked on 2026-08-09.  If the submission form asks about AI assistance, answer it truthfully.

A conservative optional disclosure, if the authors choose to include one, is:

> Generative-AI tools were used during exploratory drafting and computational organization.  All mathematical statements, proofs, references, and computational certificates were independently checked by the authors, who take full responsibility for the content of the manuscript.

This wording is **not** inserted automatically into `main.tex`.

## Computational supplement

Submission-level scripts are separated from research-only experiments.

The supplementary manifest records SHA-256 identifiers for:

- `verify_core_certificates.mjs`;
- `verify_triangle_A88_A96_abundance.py`;
- `verify_triangle_A88_3A96_abundance.py`;
- `verify_triangle_mixed_or_471.py`.

The command `npm test` executes all submission-relevant exact certificates and Hilbert/liaison checks.  `npm run test:research` includes additional exploratory weight-48 computations and should not be described as part of the proof.

## Cover-letter emphasis

The cover letter should describe the proved results directly and should not suggest that the manuscript proves, or nearly proves, `u(8) <= 168`.  The three points that can be stated factually are:

1. every strict weight-64 even set on a nodal octic has a transverse symmetric `CI(4,4,4)` determinantal presentation;
2. in the minimum-64 case, exact coding bounds give `A_64>=533` and allow a global choice with residual distance 32 or 36;
3. the paper proves comparison results in those residual cases, together with the exact 48/64 trade-off and the contact-quadric intersection theorem.

The maximal-node problem should be described as the main motivation, with an explicit sentence that the manuscript does not claim the final bound. No claim of a general theory or broadly applicable method should be made unless such generality is proved separately.

## Final checks before clicking submit

- Confirm spelling and preferred romanization of both author names.
- Confirm both institutional affiliations are the affiliations appropriate for this work.
- Confirm funding and grant information.
- Decide whether to include the optional AI-assistance disclosure.
- Upload `main.pdf` and, if the submission system permits supplementary files at initial submission, the exact certificate scripts plus `SUPPLEMENTARY_COMPUTATIONAL_CERTIFICATES.md`.
- If supplementary files are not accepted at initial submission, retain them in a stable archive and mention availability in the cover letter.
- Do not upload research-only scripts as proof material unless clearly separated from the submission-level certificate set.
