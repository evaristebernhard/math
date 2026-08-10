# JAG final preflight audit — 2026-08-09

## Verdict

The manuscript now presents a set of proved results on low-weight strict even sets of nodes on octic surfaces, with the unresolved cases stated explicitly. The main proof chain is internally consistent with the current theorem statements, the principal exposition gaps identified in the previous audit have been repaired, and the submission-level exact computations pass. The remaining submission items are mainly author confirmations and supplementary-material preparation.

## Official JAG requirements checked

The current Journal of Algebraic Geometry author information was checked on 2026-08-09. The relevant requirements are:

- initial submission is a PDF;
- accepted manuscripts must be prepared in AMS-LaTeX;
- manuscripts are encouraged to be in English;
- author names should be in First-Middle-Surname order;
- all authors' affiliations and email addresses should be fully listed at the end of the paper, with current postal addresses;
- an abstract is required and must not exceed 300 words;
- footnotes should be avoided except for a possible first-page acknowledgment of assistance or financial support;
- references should be in alphabetical-chronological order and use Mathematical Reviews-style journal abbreviations.

## Changes made in this preflight

1. Removed the first-page `\thanks{Corresponding author: ...}` footnote. The corresponding author should instead be identified in the submission metadata and cover letter.
2. Shortened the abstract from about 292 words to about 227 words while preserving the first-principles `u(8)=168` motivation and the exact proof status.
3. Corrected the abstract's residual-32 description: it now says that the paper proves the common-pencil bound and excludes the one-dimensional common-net comparison, rather than using the broader phrase `exclude the common-pencil comparison`.
4. Reordered the bibliography into alphabetical-chronological order, including Endrass 1997/1998/1999.
5. Added Catanese's 1981 foundational reference on contact surfaces and symmetric determinantal varieties and cited it in the historical paragraph.
6. Tightened the use of Endrass Proposition 3.6: since the proposition produces a polynomial of degree `2v-s`, at `v=4`, `s=8` the coefficient is directly a nonzero constant; the previous unnecessary argument about `alpha=0` was removed.

## Mathematical audit status

### Green

- high-node shortening and the `48/64/72` minimum-weight trichotomy;
- minimum-distance-72 exclusion by exact MacWilliams/Krawtchouk certificate;
- universal strict weight-64 transverse `CI(4,4,4)` symmetric determinant theorem;
- first residual classification for minimum 64;
- `A_64 >= 533` and global reduction to residual 32 or 36;
- residual-32 split-MacWilliams compensation theorems;
- residual-32 common-pencil bound and complete `k=1` exclusion;
- residual-36 six-quartic global map reduction;
- finite normal quadratic target exclusion;
- finite cubic target with isolated singularities exclusion;
- J1/J2 degree-eight local obstruction statements at their stated hypotheses;
- coupled Beilinson--Horrocks obstruction as a standalone theorem;
- minimum-48 first residual, `A_64+21A_48>=533`, global pair thresholds, and contact-quadric intersection theorem.

### Explicitly open, and correctly stated as open

- residual-32 `k=0` six-quartic compatibility;
- residual-36 finite cubic targets with positive-dimensional singular locus;
- residual-36 nonfinite and nonnormal target geometries;
- remaining weight-48 pair geometries;
- the final bound `u(8)<=168`.

No new contradiction with these status statements was found in this preflight.

## Items that still require author confirmation before submission

### 1. Postal affiliations

The manuscript now records the author-supplied units and official university addresses: Jizheng Chen is listed with the Department of Mathematics, Chang'an University, at the university's South Second Ring Road address in Xi'an (710064); Chaoyu Hu is listed with the School of Automation, Hangzhou Dianzi University, at No. 1158, No. 2 Street, Baiyang Subdistrict, Qiantang District, Hangzhou (310018). These should still be checked by the authors against the exact institutional naming they want printed in the published paper.

### 2. Funding

No funding statement should be invented. If either author or the project was supported by a grant, add the exact funder and grant number as a first-page acknowledgment. If there was no funding, only provide a `no external funding` statement if the submission system asks for one.

### 3. Corresponding author

Use Chaoyu Hu as corresponding author in the submission system / cover letter. It no longer appears as a manuscript footnote because JAG discourages non-acknowledgment footnotes.

### 4. ORCID

Optional unless the submission system requests it. Add only verified ORCID identifiers.

## Computational supplement: the main remaining practical issue

The manuscript states that machine-readable exact certificates and verifier scripts are supplied as supplementary material. Therefore the initial submission package should actually include, if the portal permits it:

- `SUPPLEMENTARY_COMPUTATIONAL_CERTIFICATES.md`;
- the exact certificate/verifier files used by the submission-level tests;
- a manifest mapping each theorem to its verifier and SHA-256 identifier.

Research-only exploratory scripts should remain clearly separated.

If JAG's initial-submission portal accepts only the manuscript PDF, place the supplementary package in a stable archive and state its availability in the cover letter. A DOI-bearing archive is preferable for reproducibility, but this is a recommendation rather than a stated JAG formatting requirement.

## Cover-letter framing

The cover letter should state directly what the paper proves on low-weight strict even sets of nodes on octics, and should use the maximal-node problem as motivation. It should also state that the manuscript does not prove `u(8)<=168`.

Suggested emphasis:

1. every strict weight-64 even set has a transverse `CI(4,4,4)` symmetric determinant presentation;
2. exact coding theory forces at least 533 simultaneous minimum presentations and reduces the global minimum-64 problem to two residual comparison geometries;
3. the paper proves comparison results in the residual 32/36 cases and gives an exact 48/64 trade-off together with a contact-quadric intersection theorem.

A single sentence should make clear that the manuscript does not claim the final inequality `u(8)<=168`.

## Current metadata status

- title: present;
- authors: present and in First-Surname order;
- MSC 2020: present (`14J17`; secondary `14J70, 14M12, 94B05`);
- keywords: present;
- abstract: now comfortably below 300 words;
- affiliations and emails: present;
- references: now alphabetical-chronological;
- non-acknowledgment footnotes: removed;
- AMS-LaTeX/`amsart`: present;
- computational-material statement: present.

## Final recommendation

Before clicking submit, the only genuinely necessary human decisions are:

1. confirm both postal affiliations / departments;
2. confirm funding information;
3. prepare the actual supplementary certificate package or stable archive;
4. enter Chaoyu Hu as corresponding author in the portal;
5. use a cover letter that lists the proved results accurately, states the remaining open cases, and explains that `u(8)=168` is the motivating extremal problem rather than a theorem of the paper.

After those confirmations, the manuscript is ready for a JAG first submission on formatting/presentation grounds. The principal remaining risk is editorial significance, not formal compliance.