# SOURCES.md — slide 039 "Parallel Processing — Transform Sequence Elements in Parallel"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 and Peter Bloem's transformers post, plus a python3+numpy check
(no vision calls run; no image access — frame facts below come from the script-12
raw transcription, which is the record of the frame).

## Slide identity

- New (curated) slide **039** ← old extraction slide **82**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_039.jpg`,
  badge "39".
- Frame facts (raw transcription): title "Parallel Processing" / "Transform
  Sequence Elements in Parallel" / "[Calculation of Self Attention of words
  (X₁..X₄)]". Four IDENTICAL self-attention pipeline panels in a cascading
  diagonal stack (front = X₁ through back = X₄), each now INCLUDING the
  complete flow: inputs → W^k boxes → K₁..K₄ → tan "Dot Product" box (with
  "K,q" annotation and the fraction **K,q / √d**) → pink "Scaling by √d" box →
  pink "Soft max" box → ⊗ nodes fed by V₁..V₄ via blue W^V boxes → Σ box → Y
  outputs on a rising diagonal (Y₁ lowest … Y₄ highest). Small red "W^q" box
  produces "q₁" [?] on the front panel. Cream pills "Similarity /
  Probabilities / Weighted SUM" per panel. Bottom: four red up-arrows X₁..X₄;
  dashed green connectors distribute the same inputs to all panels; yellow
  sticker "*** Run in Parallel ***" (rotated ≈ −8°).
- Position in the course: 34/35 (softmax sensitivity + scaling) → 36 (why √d) →
  37/38 (scaling added to the flow + Fig 2-left inset) → **39: the complete
  scaled pipeline, replicated once per word, run in parallel**. Next: 40 opens
  the multi-head section.

## Primary sources

- **Paper**: https://arxiv.org/html/1706.03762v7 — "Attention Is All You Need"
  (Vaswani et al., 2017) (verified live 2026-10-11), §3.2.1 and §4/Table 1.
- **Course notation source**: Peter Bloem, "Transformers from scratch" —
  https://peterbloem.nl/blog/transformers (verified live 2026-10-11).

## Figures used by this slide

**None — course-authored diagram** (cascading panel stack is the instructor's
own composition; it is NOT the paper's Figure 2, despite showing the same
stages — 37/38 carry the paper-figure inset duty in this family). Download
decision: nothing downloaded into this dir.

## What the sources CONFIRM (data behind the slide)

- **Scaling by √d inside the pipeline is the paper's √d_k**: §3.2.1 eq (1),
  Attention(Q, K, V) = softmax(QKᵀ/√d_k)·V — "compute the dot products of the
  query with all keys, **divide each by √d_k**, and apply a softmax function".
  The slide's fraction "K,q / √d" and the "Scaling by √d" stage between the dot
  product and the softmax match this exactly.
- **√d (not d) is the right factor**: paper footnote — with q, k components
  independent, mean 0, variance 1, the dot product has mean 0 and **variance
  d_k**, "so we scale the dot products by 1/√d_k". Bloem gives the same
  justification via vector length: a vector in ℝ^k with all values c has
  Euclidean length √k·c, so dividing by √k "divides out the amount by which
  the increase in dimension increases the length" (w'ᵢⱼ = qᵢᵀkⱼ/√k). The
  course derived this on slides 34–36 (the 36 raw literally derives
  V₁ᵀV₁ = M·√d for an all-M vector) and 37/38 inserted it into the flow.
- **One pipeline per word, all reading the same inputs, outputs Y₁..Y₄**:
  the paper's matrix formulation computes ALL queries at once — Q, K, V are
  whole-sequence matrices (each row a word), so attention of every word over
  every word is one matrix product; Bloem: "y is a matrix, with a row for each
  input" (yᵢ for each xᵢ). The slide's four panels + four Y outputs express
  the same fact graphically.
- **"Run in Parallel" is the paper's core claim**: §4 — "a self-attention layer
  connects all positions with a **constant number of sequentially executed
  operations**, whereas a recurrent layer requires O(n) sequential operations."
  Table 1: Self-Attention — Complexity O(n²·d), **Sequential Operations O(1)**,
  Maximum Path Length O(1); Recurrent — O(n·d²), O(n), O(n). The parallelism
  being sold on this slide is the paper's Table-1 contrast with recurrence.
- **Numeric verification** (python3+numpy, 2026-10-11; re-run and confirmed in
  the W-G cross-check same day): the per-panel shape
  chain verified — (1×d)·(d×d) = (1×d) for q/K/V projections; K·q gives one
  score per word; softmax sums to 1.0; Σᵢ pᵢ·Vᵢ returns (1×d) per panel. No
  numeric values are transcribed on the slide, so no value recomputation
  applies.

## Course-authored elements (no source counterpart — do not "fix" to a source)

- The cascading/overlapping panel stack, the rising Y diagonal, the bottom red
  arrows, the "*** Run in Parallel ***" sticker (wording and asterisks), the
  cream stage pills, the dot-product scatter of blue dots, the dashed green
  distribution connectors, the dark-red frame — all instructor's own.

## [?] Uncertain items

- [?] Tiny labels: "W^k" on the K-row boxes (raw flags it "could read W^q"),
  "W^V" (superscript V vs v), and "q₁" on the front panel's query box. Note
  q₁ is internally CONSISTENT (front panel = X₁'s computation; slide 33's
  q₂ served X₂), but the exact glyphs are blurry. **raw needs re-check** at
  build; no patch.
- [?] K₁..K₄ output labels were each flagged [?] in the raw (blurry subscripts)
  — order top→bottom read as K₁..K₄ here vs K₄..K₁ on slide 33; both are
  plausible row orders, only the frame can decide. **raw needs re-check**.
- [?] Whether each panel's "Dot Product" box also prints the "K,q/√d" fraction
  or it sits only above the Scaling box (raw records it once per panel as an
  annotation above the Scaling box). Layout fact; re-check.

## Corrections

- **Cross-check 2026-10-11 (W-G, post-banking):** none — consistent. No
  patches to `analysis/slide_039_raw.json`: the three [?]s are tiny-glyph
  frame ambiguities the raw itself flags (W^k vs W^q, q₁, K-order) and one
  layout fact (fraction placement) — none answerable from the raw record
  alone. Frame facts in this file re-verified against the raw (q₁ is
  internally consistent with the front panel being X₁'s computation); the
  numpy shape-chain check was re-run and confirmed.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). The sources confirm/correct DATA and record
provenance; they never license inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy — the slide
wins for recreation, the source wins for understanding.
