# SOURCES.md — 002 slide 053 "Self Attention Look Ahead Mask (Used in Decoder first Block)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Machine-verified 2026-10-11 by the Part II
web-verification worker: vision transcript banked
(`transcripts/slide_053_vision_2026-10-11.txt`, default `images` route, one
probe, `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`),
web research via `agy` + live fetches.

## Slide identity

- Video-2 (002_transformers_part2) curated slide **053** ← old extraction
  slide **133** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_053.jpg` (kept from t≈4681 s; shown 4555–4680 s = 126
  frames, heavily taught), badge numeral 53.
- Content (banked vision transcript): title verbatim **"Self Attention Look
  Ahead Mask (Used in  Decoder first Block )"** (double space after "in",
  space before ")" — slide's own spacing). A 5×5 look-ahead-mask matrix over
  the SAME running French example as slide 052 — row labels (left, top→bottom)
  and rotated column headers: **SOS / Je / me / sens / malade**. Cell values:
  **0** on and below the diagonal (15 cells, light-green lower triangle),
  **−∞** above the diagonal (10 cells, brown/tan upper triangle). Right
  panel: red "Softmax" label over the boxed equation
  **σ(x_j) = e^(x_j) / Σ_i e^(x_i)**. Bottom callout (verbatim): "Mask Values
  are ADDED to Masked (Scaled) Values" / "Addition of "0" does not change the
  original values, consequently no effect on Softmax output" / "Addition of
  "-inf" gets "Zero" output of Softmax, leaving zero attention scores for
  future Words." A blue block-arrow points left→right into the row labels.

## Primary source — CONFIRMED (mechanism), paper verbatim

- **Paper**: "Attention Is All You Need" — Vaswani et al. 2017,
  arXiv:1706.03762v7. Both masking sentences verified live 2026-10-11 from
  https://arxiv.org/html/1706.03762v7 (HTML banked at `../scratch/paper_v7.html`):
  - §3.2.1: "We implement this inside of scaled dot-product attention by
    **masking out (setting to −∞) all values in the input of the softmax
    which correspond to illegal connections**." — exactly the slide's
    "ADDED … −∞ → Zero output of Softmax" callout and the −∞ cells.
  - §3.2.3.1 (decoder): "masking, combined with fact that the output
    embeddings are offset by one position, ensures that the **predictions
    for position i can depend only on the known outputs at positions less
    than i**." — exactly the slide's lower-triangular pattern (row i may
    attend to columns ≤ i; "future Words" get zero attention) and the title's
    "Used in Decoder first Block" (first decoder sub-layer = masked MHA,
    cf. slide 052 and §3.1).
  - §3.2.1 formula (also verified live): Attention(Q,K,V) =
    softmax(QKᵀ/√d_k)V — the mask matrix is ADDED inside the softmax input,
    matching the callout's "Mask Values are ADDED to Masked (Scaled) Values".
- **Softmax equation**: the boxed σ(x_j) = e^{x_j} / Σ_i e^{x_i} is the
  standard softmax definition — confirmed live against
  https://en.wikipedia.org/wiki/Softmax_function ("normalized exponential…
  converts a tuple of K real numbers into a probability distribution").
- No discrepancy between slide and paper. The slide's 0/−∞ matrix is the
  standard pedagogical rendering of the paper's mask matrix M.

## Figure identity — course-authored; nearest mechanism explainer identified

- The exact matrix cartoon (green token tiles, 0/−∞ chips, boxed softmax,
  callout box) is **course-authored in the deck's own style** — it continues
  slide 052's running example and styling ("SOS Je me sens malade" tokens;
  same green label tiles). No published figure matches the slide's own
  pixels/wording.
- **Nearest published explainer (agy-identified, verified via Wayback)**:
  Greg Mongaras, **"How Do Self-Attention Masks Work?"** (Medium, 2021),
  https://gmongaras.medium.com/how-do-self-attention-masks-work-72ed9382510f
  — live-verified 2026-10-11 via Wayback snapshot
  http://web.archive.org/web/20260227063434/https://gmongaras.medium.com/how-do-self-attention-masks-work-72ed9382510f
  (live site Cloudflare-blocks bots; snapshot archived 2026-02-27). It
  teaches the identical mechanism — "The look-ahead mask was originally used
  in the Attention is All You Need paper for the original transformer";
  mask matrix ADDED to the query-key matrix; "Softmax of the result from
  adding the query-key matrix to the mask matrix … is now all 0s and
  essentially doesn't affect the weights". **Its example sentence differs
  ("cómo estás <END>…")** — so it is a mechanism counterpart, NOT the slide's
  figure source. agy's first attempt on this query timed out (300 s proxy
  timeout); the retry surfaced this article and the link was independently
  resolved (302) and archived before citation.
- No figures downloaded for this slide: the slide does not reuse any
  published figure's pixels (course-authored rendering; the paper has no
  mask-matrix figure, and Mongaras' figures differ in example/labels).
  Reference URLs above serve as the ground-truth mechanism record.

## What the source CONFIRMS / CORRECTS

- CONFIRMED: −∞ masking added to the softmax input (§3.2.1); lower-triangular
  allowed pattern with position i attending only to ≤ i (§3.2.3.1); "0 added
  → no change" and "−∞ added → softmax zero" arithmetic; the softmax
  equation's standard form; the mask living in the DECODER's first
  (masked-MHA) sub-layer (§3.1/§3.2.3.1, and slide 052's stack).
- CORRECTED: nothing — no slide-vs-source disagreement found.
- Continuity note for the build: the row/column token order (SOS first) and
  the 5×5 size match slide 052's decoder column exactly — the two slides form
  one running example.

## [?] Open questions

1. Exact origin of the cartoon rendering: course-authored `[?]` (consistent
   with 052's finding; no confirming external figure). If the P4 pair
   (slides 054/055, verified next) continues this series, the same
   course-authored conclusion likely applies — recorded there when verified.
2. The tiny gray arrow near the matrix's upper-right (reads as a presenter
   cursor, not content) — intent `[?]` per the transcript.
3. Whether the instructor's "(Scaled) Values" refers to QKᵀ/√d_k (the
   paper's scaling) — almost certainly yes, but the slide does not draw the
   QKᵀ/√d_k step itself `[?]` (frame ground truth: only "Masked (Scaled)
   Values" wording).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web
sources confirm/correct data and provenance, never license inventing content.
`[?]` markers are removed only with a confirming URL recorded here.
