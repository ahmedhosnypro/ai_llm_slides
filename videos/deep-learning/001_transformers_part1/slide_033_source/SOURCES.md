# SOURCES.md — slide 033 "Self Attention Mechanism (Linear Transformation of Inputs) — Self Attention of word X₂ w.r.t All words in Sentence"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 and Peter Bloem's transformers post, plus a python3+numpy check
(no vision calls run; no image access — frame facts below come from the script-12
raw transcription, which is the record of the frame).

## Slide identity

- New (curated) slide **033** ← old extraction slide **63**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_033.jpg`,
  badge "33".
- Frame facts (raw transcription): full self-attention **dataflow diagram for the
  queried word X₂** against the whole sentence (X₁..X₄): left input column →
  four yellow **W_k** boxes → **K₄, K₃, K₂, K₁** → taupe **"Dot Product"** box
  (labeled "K₂q" [?]) receiving **q₂** from a yellow **W_q** box below → orchid
  **"Soft max"** bar → four ⊗ circles fed by **V₄..V₁** from yellow **W_v** boxes
  and the right input column → blue **Σ** box → green dashed **Y₂** output.
  Stage pills: **Similarity / Probabilities / Weighted SUM**. Bottom: sentence
  row X₁..X₄ (X₂ magenta-highlighted); legend "(1×d) · W(d×d) = (1×d)",
  "d: Embedding Length". Emphasis overlays: translucent red circle on the K₂
  row; red block arrow at X₂.
- Position in the course: completes 26–33 (fundamental operation → dictionary
  metaphor 29 → roles 30 → projections 31 → FC view 32 → this full pipeline).
  Scaling is NOT on this slide — the course adds it at 34–37 and restores the
  complete pipeline (now scaled, run in parallel) at 39. The absence of √d here
  is the course's deliberate pedagogical order, not an error.

## Primary sources

- **Paper**: https://arxiv.org/html/1706.03762v7 — "Attention Is All You Need"
  (Vaswani et al., 2017) (verified live 2026-10-11), §3.2 / §3.2.1.
- **Course notation source**: Peter Bloem, "Transformers from scratch" —
  https://peterbloem.nl/blog/transformers (verified live 2026-10-11).

## Figures used by this slide

**None — course-authored diagram** (hand-drawn lecture style; no published
figure is redrawn). Download decision: nothing downloaded into this dir.

## What the sources CONFIRM (data behind the slide)

- **The three-stage structure matches the paper's operational description of
  scaled dot-product attention** (§3.2.1): "compute the dot products of the
  query with all keys, divide each by √d_k, and apply a softmax function to
  obtain the weights on the values" — the slide shows the same computation
  MINUS the (not-yet-introduced) scaling: Similarity = dot products q₂·K_i,
  Probabilities = softmax, Weighted SUM = Σᵢ softmaxᵢ ⊗ Vᵢ.
- **The output Y₂ is the weighted sum over the values**: paper §3.2 — the
  output is "computed as a weighted sum of the values"; Bloem — y_i = Σ_j
  w_ij·v_j ("y is the same size as x"). The slide's Σ box over softmax⊗V rows
  is exactly that.
- **K and V come from every word, q from the queried word**: paper §3.2.2 —
  the input is projected with W^Q, W^K, W^V to form Q, K, V for the sequence;
  each query attends over ALL keys/values. Bloem: every x_i produces k_i, v_i;
  the query q_i is compared against all of them. The slide's sentence row
  feeding BOTH the left (K) and right (V) columns via dashed green connectors
  is this exact arrangement.
- **"K₂q" dot-product ordering** (key written before query): the dot product
  is commutative; the paper writes q·k ("dot products of the query with all
  keys"), Bloem writes q_i^T k_j. The course's K₂·q denotes the same score.
  Notation provenance, not a discrepancy.
- **"d: Embedding Length" and the legend (1×d)·W(d×d)=(1×d)**: Bloem's k is
  the embedding dimension; the paper's d_model. The row-vector identity is
  verified (see below).
- **Numeric verification** (python3+numpy, 2026-10-11; re-run and confirmed in
  the W-G cross-check same day): with d=4, a (1×d) row
  vector × (d×d) matrix → (1×d); then scoresᵢ = Kᵢ·q (4 values), softmax sums
  to 1.0, and Σᵢ pᵢ·Kᵢ returns a (1×d) vector — the Similarity → Probabilities
  → Weighted SUM pipeline produces a 1×d output Y₂, as the slide's legend
  claims. The slide transcribes NO numeric values, so no heatmap/matrix value
  recomputation applies.

## Course-authored elements (no source counterpart — do not "fix" to a source)

- The hand-drawn diagram style (peach panel, dashed green containers, yellow W
  boxes, taupe Dot-Product box, orchid Softmax bar), the stage-pill wording
  ("Similarity", "Probabilities", "Weighted SUM" — the paper says "compatibility
  function"/"weights"; the pills are the instructor's own names), the emphasis
  overlays (red circle on K₂, magenta X₂ box, red block arrow), the W^(1)
  superscript styling [?] and the legend box — all instructor's own.

## [?] Uncertain items

- [?] Exact string "K₂q" in the Dot-Product box corner (raw flags it [?]) —
  could be K₂q, K₂·q, or Kq. **raw needs re-check** at build; no patch.
- [?] The W-box labels read "W_k^(1)", "W_q^(1)", "W_v^(1)" with a tiny
  superscript the raw itself flags [?] — could be a head/layer index or a
  stray mark. Note: a superscript-(1) would be odd here (single head, no
  head indexing yet in the course); re-check at build. No patch.
- [?] Left/right input-column row labels read "X₁" per row with tiny
  subscripts "[possibly X₁..X₄]" — presumably each row is one word X₁..X₄
  (matching K₄..K₁ / V₄..V₁). **raw needs re-check**; no patch.
  → Cross-check note (2026-10-11): there is an ordering tension the raw cannot
  adjudicate — if the input rows run X₁→X₄ top→bottom while the K/V labels run
  K₄→K₁ / V₄→V₁ top→bottom, row-wise alignment pairs X₁ with K₄/V₄. So either
  the input rows actually read X₄..X₁ top→bottom (subscripts too tiny to read),
  or the K/V labels run bottom-up. Frame-level; stays open for the build-time
  re-check; recreation reproduces the raw as transcribed.

## Corrections

- **Cross-check 2026-10-11 (W-G, post-banking):** none — consistent. No
  patches to `analysis/slide_033_raw.json`: all three [?]s are tiny-label
  frame ambiguities the raw itself flags and cannot answer (the K-ordering vs
  input-row alignment tension is recorded as a note on the third [?] above).
  Frame facts in this file re-verified against the raw; the numpy pipeline
  check was re-run and confirmed.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). The sources confirm/correct DATA and record
provenance; they never license inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy — the slide
wins for recreation, the source wins for understanding.
