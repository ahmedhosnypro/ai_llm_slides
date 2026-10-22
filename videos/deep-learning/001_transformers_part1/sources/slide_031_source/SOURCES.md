# SOURCES.md — slide 031 "Self Attention Mechanism (Linear Transformation of Inputs)"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 and Peter Bloem's transformers post, plus a python3+numpy check
(no vision calls run; no image access — frame facts below come from the script-12
raw transcription, which is the record of the frame).

## Slide identity

- New (curated) slide **031** ← old extraction slide **61**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_031.jpg`,
  badge "31".
- Frame facts (raw transcription, ground truth for WHAT is shown): three
  structurally identical panels — **X₂ · W_Q = Q** (red), **X₂ · W_V = V** (blue),
  **X₂ · W_K = K** (green) — each drawn as an input capsule (4 cells x₂₁..x₂₄,
  "1xd") → a 4×4 weight matrix (generic entries W₁₁..W₄₄, "dxd") → "=" → a
  vertical output capsule (4 cells) with the role letter above it. Subtitle:
  "(Query using X₂ All Keys in Dictionary and retrieve Corresponding Values".
  Callouts "X₂ variant to QUERY with / used as Value / used as KEY"; yellow box
  "Generate Three Variants of X₂ (Based on its Role)"; note box "W_Q W_K W_V are
  controllable parameters (Trainable), allows to modify the incoming vectors to
  suit the three roles they must play". Predecessor of this sequence: slide 030
  ("Input Word plays Different Roles") — this slide is the formal statement of it.

## Primary sources

- **Paper**: https://arxiv.org/html/1706.03762v7 — "Attention Is All You Need"
  (Vaswani et al., 2017), arXiv:1706.03762v7 [cs.CL] (verified live 2026-10-11).
- **Course notation source**: Peter Bloem, "Transformers from scratch" —
  https://peterbloem.nl/blog/transformers (verified live 2026-10-11; 2021 Wayback
  capture https://web.archive.org/web/2021/https://peterbloem.nl/blog/transformers
  re-confirmed the same notation).

## Figures used by this slide

**None — course-authored diagram.** No external figure is redrawn here (the
hand-built panels, callouts, highlight box and note box are the instructor's own
composition). Download decision: nothing downloaded into this dir; there is no
source-hosted figure whose reuse could be claimed with confidence, and
SOURCES_MAP.md forbids speculative downloads.

## What the sources CONFIRM (data behind the slide)

- **The three role projections are the paper's own construction.** §3.2.2:
  head_i = Attention(**QW_i^Q, KW_i^K, VW_i^V**) — the SAME input is multiplied
  by three separate learned matrices to produce its Query, Key and Value
  variants. Bloem, identically: **q_i = W_q x_i, k_i = W_k x_i, v_i = W_v x_i**
  ("each input … is projected three ways"). The slide's X₂·W_Q=Q / X₂·W_V=V /
  X₂·W_K=K is exactly this triple projection.
- **The matrix names W_Q, W_K, W_V are Bloem's** (course capitalizes the
  subscript): his post writes the weight matrices as `W_q`, `W_k`, `W_v`.
- **Multiplication order**: the course writes the row vector on the left
  (X₂ (1×d) · W (d×d)) — the paper's convention (QW_i^Q); Bloem writes the
  matrix on the left (W_q x_i). Both denote the same learned projection; the
  slide matches the paper's ordering, NOT Bloem's. Not an error — record as
  notation provenance.
- **The "Dictionary" metaphor of the subtitle** (query / keys / values):
  - Paper §3.2 opening: "An attention function can be described as mapping a
    query and a set of key-value pairs to an output" (output = weighted sum of
    the values, weights from the compatibility of the query with each key).
  - Bloem, "Why is it called self-attention?": the names "derive from the
    datastructure of a key-value store"; attention is "a softened version of
    this: every key in the store matches the query to some extent."
- **"Controllable parameters (Trainable)"**: the paper lists W_i^Q ∈
  ℝ^(d_model×d_k), W_i^K ∈ ℝ^(d_model×d_k), W_i^V ∈ ℝ^(d_model×d_v) as learned
  parameter matrices; Bloem calls them "bias-free linear layers" of the model.
- **Numeric verification** (python3+numpy, run 2026-10-11; re-run and confirmed
  in the W-G cross-check same day): the slide's dimension labels satisfy
  (1×d)·(d×d) = (1×d) — verified with a 1×4 row vector times a 4×4 matrix. The
  slide transcribes NO numeric matrix/heatmap values (the 4×4 holds generic
  symbols W₁₁..W₄₄), so there is nothing else to recompute. The displayed
  4×4 grid shares slide 032's subscript placement (input index across
  columns, output index down rows — numpy-checked reading recorded in
  `../slide_032_source/SOURCES.md`).

## Course-authored elements (no source counterpart — do not "fix" to a source)

- The three-panel color coding (red = Query, blue = Value, green = Key), the
  pink capsule style, the generic 4×4 matrix of symbol cells (no source prints
  a literal W₁₁..W₄₄ grid), the three dashed callouts, the yellow
  "Generate Three Variants" box, the note-box wording, the yellow-highlighted
  parenthetical in the title, and the unclosed opening parenthesis in the
  subtitle — all instructor pedagogy on the FRAME.

## [?] Uncertain items

- [?] **Output capsule cell labels** read as x₂₁..x₂₄ (identical to the input
  capsule) in all three panels. Suspicious but UNVERIFIED: slide 032 — the very
  next slide, same equation — labels its output cells X_Q21..X_Q24, and this
  slide's role letters (Q/V/K) sit above the outputs. Either the course reuses
  the input symbols on the outputs (possible design choice) or the vision pass
  misread tiny subscripts. **raw needs re-check** at build time; no patch made
  (no evidence of what the frame actually prints).
  → **RESOLVED in cross-check (2026-10-11): the raw answers it.** The raw
  records x₂₁..x₂₄ on the output capsules identically in FOUR places (label
  list ×2, all three panel descriptions, recreation brief) — per the raw (the
  frame record), this slide reuses the input symbols on its outputs. Slide
  032's X_Q… naming is a cross-slide design difference, not evidence of a
  misread here. Build-time frame glance optional.
- [?] **Output dimension label**: the raw's equation strings annotate "= Q
  (dxd)", but dimensionally 1×d · d×d = 1×d (numpy-verified), the raw's own
  label list records "1xd" only under the INPUT capsule, and no output
  dimension label is recorded anywhere. "(dxd)" on the output is most likely a
  model annotation, not printed text. **raw needs re-check**; no patch.
  → **RESOLVED in cross-check (2026-10-11), by patch.** Numpy re-run confirms
  (1×d)·(d×d) = (1×d); the raw's "(dxd)" after = Q/V/K is dimensionally
  impossible for the drawn computation and contradicted by the raw's own label
  list (no printed dim label at any output capsule; the raw states only '=' is
  printed). The three equation annotations were PATCHED to "= Q/V/K (1xd)".
  No frame text altered.
- [?] Whether the "dxd" printed at each matrix's bottom-right is meant as the
  matrix shape (correct) or something else — frame-level detail; re-check.
  → **RESOLVED in cross-check (2026-10-11): internally consistent.** "dxd"
  sits at the bottom-right of each drawn 4×4 weight matrix — the matrix-shape
  label, matching the generic d×d weight matrix. Consistent across all three
  panels and the recreation brief.

## Corrections

- **Cross-check 2026-10-11 (W-G, post-banking):** 3 patches applied to
  `analysis/slide_031_raw.json` — the three equation strings' output-dimension
  annotations corrected from "= Q/V/K (dxd)" to "= Q/V/K (1xd)" (numpy-evidenced:
  (1×d)·(d×d) = (1×d); no printed output dim label exists in the raw's own label
  record, so these were model annotations, not frame text). `_meta` untouched.
  All three [?] items above resolved (2 by raw record, 1 by patch). Everything
  else cross-checked against this file: consistent.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). The sources confirm/correct DATA and record
provenance; they never license inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy — the slide
wins for recreation, the source wins for understanding.
