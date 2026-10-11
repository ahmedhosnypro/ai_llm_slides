# SOURCES — slide 37 — "Self Attention Mechanism (Adding Scaling)"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1 eq. (1); §3.2.2 (projection
  formation) (fetched 2026-10-11).
- Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  — § "Self-attention with key, query and value transformations" + § "2) Scaling
  the dot product" (fetched 2026-10-11).

## 2. Downloaded figures

- None (course-original flow diagram with W-matrix legend).

## 3. Course notation → paper mapping

| Course (slide 37, verbatim) | Paper |
|---|---|
| embeddings →(W_k) K1–K4 | k_j = x_j W^K (K = XW^K) |
| X2 →(W_q) q2 | q_2 = x_2 W^Q |
| Dot Product with q2 | (QK^T)_2j = q_2·k_j |
| "Scaling by √d" (K·q/√d) | ÷√d_k (eq. 1: softmax(QK^T/√d_k)V) |
| Soft max | softmax over j |
| ⊗ weights → Σ weighted sum with V1–V4 | softmax(…)·V with V = XW^V |
| Legend "W (d×d, d: Embedding Length)" | Bloem's three k×k matrices W_q, W_k, W_v (k = embedding dimension); the dimension-preserving single-head special case |

- Pipeline ORDER (project → dot → scale → softmax → weighted sum with V) is
  exactly eq. (1)'s order.

## 4. What the sources CONFIRM

- Full pipeline semantics and order: confirmed by §3.2.1 eq. (1) and the §3.2.1
  sentence "We compute the dot products of the query with all keys, divide each by
  √d_k, and apply a softmax function to obtain the weights on the values."
- The three separate learned projections W_q/W_k/W_v from the same embeddings —
  confirmed by §3.2.2 (QW^Q, KW^K, VW^V) and Bloem (q_i = W_q x_i, k_i = W_k x_i,
  v_i = W_v x_i).
- The d×d legend: confirmed as the dimension-preserving single-head formulation
  (Bloem's k×k matrices).

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- Course W matrices are d×d (embedding-preserving); the paper's multi-head
  projections (§3.2.2) are d_model×d_k = 512×64 — dimension-REDUCING. The course's
  d×d is the single-head dimension-preserving special case (as in Bloem). Course
  keeps d×d verbatim.
- Course writes the scaling as "K·q/√d"; paper writes QK^T/√d_k. Same operation;
  course notation kept.

## 6. Numeric verification

- n/a (0/0) — no worked example on this slide.

## 7. Open questions

- none.

## Corrections

Cross-checked 2026-10-11 (correction worker) against the script-12 raw transcription
(`analysis/slide_037_raw.json`, vision transcript of record):

- Flow, stage labels, and notation all match §§3–4 exactly: X-blocks → W_k boxes →
  K₁–K₄ → tan "Dot Product" box (fed by q₂ from the W_q box above the input-sentence
  strip) → red stacked fraction "K.q / √d" → "Scaling by √d" → "Soft max" → four ⊗
  nodes with V₁–V₄ from the W_v boxes → blue Σ ("Weighted SUM") → Y₂. This is eq. (1)'s
  order — confirmed, no correction needed.
- Raw detail §3's shorthand omitted: the W boxes carry a superscript "(1)" —
  "W_k^(1)" (×4, one per row), "W_v^(1)" (×4), "W_q^(1)" — course notation, kept
  verbatim by the recreation.
- The bottom-right legend glyphs stay [?] in the raw ("1×d" / "d×d" are approximate
  low-res reads; raw's best interpretation: [1×d] → W → = → [d×d], "d: Embedding
  Length"). The d×d SHAPE of W is what §§3–4 confirm; the exact printed glyphs remain
  a frame fact for the build-time frame read. No patch.
- Glyph ambiguity: the raw transcribes the small dot-product label as "K.q" (period);
  §3 wrote "K·q". Same on-frame label — the raw reading is the transcription of
  record; recreation keeps "K.q" unless a frame read shows a middle dot.
- Subtitle typo ("...Sentence ( X₁, X₂, X₃, X₄ )" — unbalanced parentheses) is
  course-authentic, kept verbatim per the raw's typography_notes.
- No patches applied to the raw.
