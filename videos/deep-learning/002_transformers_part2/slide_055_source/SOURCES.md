# SOURCES.md — 002 slide 055 "Encoder-Decoder Attention Mechanism (In Decoder)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Machine-verified 2026-10-11 by the Part II
web-verification worker: vision transcript banked
(`transcripts/slide_055_vision_2026-10-11.txt`, default `images` route, one
probe, `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`).

**P4 pattern-group FOLLOW (54, 55)**: the shared pipeline pattern was
verified once against the primary sources — full verification, search
history, and figure-identity analysis live in
`../slide_054_source/SOURCES.md` (P4 LEAD). This file records slide 055's
own frame facts and the ONE additional quote its content needs
(paper §3.2.3.2 encoder-decoder attention), referencing 054 for the rest.
No additional agy/web calls were spent for 055 beyond that shared
verification, per the P4 directive.

## Slide identity

- Video-2 (002_transformers_part2) curated slide **055** ← old extraction
  slide **138** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_055.jpg` (kept from t≈4852 s; shown 4821–4851 s =
  31 frames), badge numeral 55.
- Content (banked vision transcript): title verbatim **"Encoder-Decoder
  Attention Mechanism (In Decoder)"** ("(In Decoder)" in red); subtitle
  verbatim **"(Self Attention of word Z₂ w.r.t All words in Sentence (
  Y₁, Y₂, Y₃, Y₄ )"** (unbalanced parentheses as printed; Z₂ and the Y
  tokens in red). Single-head cross-attention walkthrough, same stage style
  as 054: two hatched callouts **"From Encoder Output"** feed yellow columns
  of tokens **Y₄…Y₁** (top→bottom) through green **W_k^(1)** boxes → keys
  **K₄…K₁** (left) and through blue **W_v^(1)** boxes → values **V₄…V₁**
  (right); bottom decoder row (magenta pill) **Z₁ Z₂ Z₃ Z₄** with **Z₂
  highlighted** under a red pointer, annotated **"From Decoder Self
  Attention Layer"** → red **W_q^(1)** box → **q₂** → tan **"Dot Product"**
  panel (pill "Similarity"; label "K₁.q" [?]) → pink bar **"Scaling by √d"**
  (fraction "K₁.q / √d" [?]) → purple bar **"Soft max"** (pill
  "Probabilities") → four ⊗ nodes with the V lines → blue **"Σ"** box
  (pill "Weighted SUM") → green output box **"O"** (striped vector).
  Bottom-right legend identical in kind to 054's: strip "1×d", box "W" =
  "d×d", "1×d", caption **"d: Embedding Length"**.

## Primary source — CONFIRMED (mechanism), paper verbatim

- **Paper**: "Attention Is All You Need" — Vaswani et al. 2017,
  arXiv:1706.03762v7. NEW quote for this slide, verified live 2026-10-11 from
  https://arxiv.org/html/1706.03762v7 (HTML banked at
  `../scratch/paper_v7.html`):
  - **§3.2.3 "Applications of Attention in our Model"**: "In
    'encoder-decoder attention' layers, the **queries come from the previous
    decoder layer, and the memory keys and values come from the output of
    the encoder**." — exactly the slide's dataflow: queries q₂ from decoder
    token Z₂ (fed "From Decoder Self Attention Layer"), keys/values from
    encoder outputs ("From Encoder Output" → W_k/W_v → K/V).
- Everything else (Dot Product K.q → Scaling by √d → Softmax → Probabilities
  → weighted sum of V via ⊗ and Σ; learned projections W^Q/W^K/W^V; the
  1×d·(d×d)=1×d legend) is the SAME §3.2.1/§3.2.2 pipeline verified for the
  P4 pattern in `../slide_054_source/SOURCES.md` (Eq. (1)
  Attention(Q,K,V)=softmax(QKᵀ/√d_k)V; "learned linear projections"; legend
  arithmetic) — not repeated here.

## Figure identity — course-authored (per the shared P4 verification)

- Same conclusion as P4 lead (054): the stage-labeled walkthrough cartoon is
  **course-authored** — paper topology, slide pixels/wording. agy's
  figure-origin searches for this family defaulted to Alammar's Illustrated
  Transformer, whose live page lacks these labels ("Similarity", "Weighted
  SUM", "Embedding Length" absent; verified by grep in 054's record). The
  closest published counterpart remains banked paper Figure 2 left (Scaled
  Dot-Product Attention, `../001_transformers_part1/slide_18_source/…`).
- Continuity with the deck: 052 (decoder stack with the "Encode Decoder
  Attention" cards) ← this slide expands exactly that card; 054 is the
  self-attention sibling of the same walkthrough pattern.

## What the source CONFIRMS / CORRECTS

- CONFIRMED: cross-attention dataflow (queries from the decoder's previous
  layer; keys+values from the encoder output); the full scaled
  dot-product-to-weighted-sum stage order; the projection legend.
- Wording note (recorded, not a correction of data): the subtitle calls the
  operation "Self Attention of word Z₂ w.r.t All words in Sentence
  (Y₁…Y₄)" — the drawn dataflow is **encoder-decoder (cross) attention**
  (the slide's own title and callouts say so; the Y's are encoder outputs,
  not decoder-internal words). Paper's name wins for understanding; the
  slide's verbatim wording wins for recreation (fidelity law).
- Notation notes as in 054: "K₁.q" reads the dot product key-first (paper:
  QKᵀ); superscript "(1)" on W_k/W_v/W_q here (054's transcript read (0) on
  W_k/W_v) is the course's own indexing — see [?].

## [?] Open questions

1. The dot-product label reads "K₁.q" [?] in the transcript (may be
   "K₂.q" matching the highlighted Z₂/q₂) — frame-level read needed.
2. Superscript semantics of the (1)s (layer vs head index; and the 054/055
   cross-slide difference) `[?]`.
3. Whether the "Y" tokens are meant as encoder OUTPUT embeddings (paper:
   encoder memory) — the callouts say so; the exact course notation intent
   ("All words in Sentence") is loose `[?]` (recreation keeps slide wording).

## Figures downloaded

- None: the slide reuses no published figure's pixels (course-authored; same
  finding as P4 lead). Reference-only: banked Figure 2 left
  (`../001_transformers_part1/slide_18_source/`), Alammar live page
  (https://jalammar.github.io/illustrated-transformer/), paper HTML
  (https://arxiv.org/html/1706.03762v7).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web
sources confirm/correct data and provenance, never license inventing content.
`[?]` markers are removed only with a confirming URL recorded here.
