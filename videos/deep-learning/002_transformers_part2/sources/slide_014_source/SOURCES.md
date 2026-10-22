# SOURCES.md — slide 014 "Using FF NN for Multiplication of Multiple Vectors by a Matrix"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Vision transcript of record: `transcripts/slide_014_webverify.txt` (2026-10-11,
default `images` route, `--thinking high`, via `scripts/16_vision_gate.sh`).

## Slide identity

- Frame `unique_slides/slide_014.jpg`, badge "14". Pattern group P1
  [9,10,12,14,16] (founder: common pattern, not content dependency); no dep
  edge — fresh verification done here.
- Frame facts (vision transcript): title "Using  FF NN  for Multiplication of
  Multiple Vectors by a Matrix"; blue subtitle "Example: Multiply Vectors of
  ALL Words by W_k (Key) or W_v (Value)  { W_k, W_v is Squared Matrix}".
  LEFT panel: beige design box "Design FF NN with the following
  Considerations:" — "Activation:  Linear" / "Bias:  Zeros" / "Inputs:  All
  Words Within Same Paragraph (X_1, X_2, X_3, X_4, X_5)"; below it a fully
  connected NN diagram (pink Σ neuron units, colored per-input connection
  groups with W_ij labels, outputs y_1..y_4). RIGHT panel: three columns —
  outputs Y_1..Y_5 (each a 4-cell y_1..y_4 strip), "≡Linear" in red between
  columns, inputs X_1..X_5 (each a 4-circle x_1..x_4 strip); far right a
  green 4x4 W matrix panel (W_11..W_44), red "+", a 4-cell zero bias column,
  and a blue closing brace "}". Highlight artifacts: X_3/Y_3 rows outlined
  red; red rectangle over matrix row 3.
- Video artifacts (do not recreate): a floating white "X_5" box overlapping
  the subtitle top-left; the 4th/5th NN units clipped at the slide bottom
  edge; decorative honeycomb hatch under the Σ units.
- Position in the lecture: review block; the vector-by-matrix step of slide
  012 generalized to ALL words at once — and the explicit statement that a
  linear-activation, zero-bias FF NN IS that matrix multiplication (so
  W_k/W_v are "FF NN"s). This is the course's "FC view" of the attention
  projections (001's slides 31–32 precedent).

## Primary sources (verified live 2026-10-11)

- **Vaswani et al. 2017** — https://arxiv.org/html/1706.03762v7
  (WebFetch-confirmed verbatim excerpts this session): §3.2 "An attention
  function can be described as mapping a query and a set of key-value pairs
  to an output"; §3.2.2 "linearly project the queries, keys and values h
  times with different, learned linear projections"; §3.2.3 "all of the
  keys, values and queries come from the same place" — i.e., W_k/W_v are
  linear projections applied to the ENTIRE input sequence (all words), which
  is exactly the slide's "Inputs: All Words" matrix form.
- **Goodfellow, Bengio, Courville, "Deep Learning" (MIT Press, 2016), Ch 6**
  (agy-confirmed, 2026-10-11): a feed-forward network with linear activation
  σ(z)=z and zero bias collapses to a single linear transformation —
  stacking n such layers gives y = (W^(n)···W^(1))x = W_total·x. This is the
  standard text grounding the slide's "Activation: Linear / Bias: Zeros ⇒
  ≡Linear (matrix multiply)" design box. (Elementary linear algebra; also
  re-derivable directly.)
- agy recap check (2026-10-11) confirmed both claims: K/V projections are
  linear layers over all input embeddings; linear-activation zero-bias FF NN
  ≡ y = Wx.

## Figures used by this slide

**None — course-authored diagram** (instructor's own NN/matrix artwork;
matches no published figure — no Vaswani Fig 1/2, no Bloem, no Alammar
composition). Download decision: nothing downloaded into this dir.

## What the sources CONFIRM

- W_k / W_v are learned LINEAR projections applied to every word in the
  sequence (Y_i = X_i·W for all i): paper §3.2.2/§3.2.3. CONFIRMED.
- "W_k, W_v is Squared Matrix" (course: d×d per head, 001 slide-37 legend
  precedent): the paper's projections are d_model×d_k rectangles; the
  course's squared-matrix choice is its own convention (consistent with its
  d×d bookkeeping across 001/002). Slide wins for recreation; recorded.
- Linear activation + zero bias ⇒ the layer ≡ plain matrix multiplication
  ("≡Linear"): standard result (Goodfellow Ch 6 via agy). CONFIRMED.
- Zero bias specifically: bias vector drawn as four 0s, matching the design
  box "Bias: Zeros". Internal consistency confirmed on the frame.

## Course vs paper discrepancies (NOT defects — recreation keeps course form)

- Course: 5 words (X_1..X_5) with 4-dim vectors and a 4x4 W — a toy
  illustration (the 5th word shows the "ALL words" point; 4 = embedding
  length d as in the rest of the course). Paper: sequence length n and
  d_model=512. Illustration choice, kept verbatim.
- Course wording "All Words Within Same Paragraph" — the course's own phrase
  for the sentence/sequence; the paper says the input sequence. Verbatim.
- Matrix cell labeling reads column-major-looking (W_11 W_21 W_31 W_41
  across the top row) — same as-printed convention as slide 012; transcribe
  verbatim, do not "fix" to row-major.

## Open questions

- [?] per-line W_ij label assignment along the NN connection lines (the
  transcript reads some labels twice, e.g. W_21; colored-line groups are
  approximate at JPEG resolution) — zoom the video frame before building if
  the left NN diagram's weights matter for the recreation; the RIGHT panel's
  4x4 matrix is legible and authoritative.
- [?] whether a fifth Σ neuron exists below the slide's bottom clip —
  content appears cut off in the video frame itself; recreate what is
  visible.

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw landed
after this file's research; the record's frame facts were transcript-based)

- `analysis/slide_014_raw.json` read in full (model `glm-5.3-flash`; old
  extraction 20; kept_frame frame_00498, 7 frames). FULLY CONFIRMS the record:
  title; subtitle "Multiply Vectors of ALL Words by W_k (Key) or W_v (Value)
  { W_k, W_v is Squared Matrix}" (verbatim, double spaces); design box
  "Activation:  Linear" / "Bias:  Zeros" / "Inputs:  All Words Within Same
  Paragraph (X_1..X_5)"; "= Linear" annotation beside the Y₃ row; zero bias
  column; matrix rows printed W_11 W_21 W_31 W_41 / … (as-printed convention).
- [?] RESOLVED (fifth Σ neuron): raw sees exactly THREE Σ neurons with outputs
  y₁, y₂, y₃ ("Σ — appears 3 times") — no fifth neuron; the record's
  bottom-clip question is resolved toward 3-neurons-visible.
- [?] NARROWED (per-line weight labels): raw groups the 16 labels by source
  input — W_11..W_41 (blue) near x₁, W_12..W_42 (blue) near x₂, W_13..W_43
  (magenta) near x₃, W_14..W_44 (green) near x₄ — the 009/010 convention.
  Per-line certainty on tiny edge labels remains a build-time zoom glance.
- Raw ADDITIONS not in the record's transcript (frame truth for the build):
  - Fanned "deck of vector cards" at the network's top-left: boxed X₃ on top
    with X₄, X₂, X₁ cascading beneath (X₅ occluded) [?].
  - Input clusters carry per-circle labels x'₁..x'₄ (prime) in clusters
    1/2/4/5 vs x₁..x₄ in cluster 3 [?tiny].
  - Glyph note: the record read "≡Linear"; raw reads "= Linear" (red '=' + blue
    'Linear') — minor glyph difference, frame wins at build.
- Script-13 final: NOT YET LANDED for 014. Corrections: none yet — verify against
  script-13 final when it lands.
