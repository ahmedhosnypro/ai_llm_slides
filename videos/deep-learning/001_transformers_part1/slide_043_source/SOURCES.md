# SOURCES — slide 43 — "Multi Head Self Attention of Word X2 'Wide' Architecture"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.2 "Multi-Head Attention" (fetched
  2026-10-11).
- Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  — § "3) Multi-head attention" (fetched 2026-10-11). Origin of the course's
  Wide/Narrow vocabulary: the post's own update log says "19 October 2019 — Added a
  section on the difference between wide and narrow self-attention."

## 2. Downloaded figures

- None (course-original five-head diagram). For reference, the paper's Figure 2
  (right) "Multi-Head Attention" is banked at ../slide_18_source/ ("slide18
  Multi-Head Attention\n\n.png" — filename contains literal newlines; always quote
  it in shell).

## 3. Course notation → paper mapping

| Course (slide 43, verbatim) | Paper (§3.2.2) |
|---|---|
| Five heads h=1..h=5, each with (Dot Product → Scaling by √d → Soft max → Σ weighted sum) and W^Q/W^K/W^V projections | head_i = Attention(QW_i^Q, KW_i^K, VW_i^V) |
| "Concatenated Vector 1×dH" | Concat(head_1, …, head_h) |
| "Linear Transformation [T] dH×d" → output 1×d | MultiHead(Q,K,V) = Concat(head_1..head_h)W^O, W^O ∈ ℝ^{h·d_v × d_model} |

- Bloem (wide form, verbatim): several self-attention mechanisms indexed r, "each
  with different matrices W_q^r, W_k^r, W_v^r … For input x_i each attention head
  produces a different output vector y_i^r. We concatenate these, and pass them
  through a linear transformation to reduce the dimension back to k."
- "Wide" is the course's (and Bloem's) name for exactly this: every head gets a
  full-size learned projection of the embedding; heads are concatenated, then a
  linear map restores the embedding dimension. The 2017 paper itself has no
  "wide/narrow" vocabulary — it just calls this multi-head attention.

## 4. What the sources CONFIRM

- Wide architecture semantics: per-head full-dimension projections → per-head
  attention (dot / scale by √d / softmax / weighted sum) → concat → linear
  transformation back to the embedding dimension. Confirmed by §3.2.2 and by
  Bloem's wide description.
- The W-matrix legend (per-head W^Q/W^K/W^V): confirmed — the paper's W_i^Q,
  W_i^K, W_i^V with W_i^Q ∈ ℝ^{d_model×d_k}, etc.; paper hyperparameters h=8,
  d_k=d_v=d_model/h=64, d_model=512.

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- Course illustrates with h=5 heads; the paper uses h=8. Illustration choice, kept
  verbatim.
- Course dimension bookkeeping: per-head W matrices are d×d (slide-37 legend), so
  concat = 1×dH with dH = h·d, then the dH×d linear maps back to d. Paper: per-head
  projections REDUCE to d_k = d_model/h, so concat = h·d_v = d_model and W^O is
  d_model×d_model (square). Same structure (concat then linear); different
  dimension accounting. Course keeps its own numbers verbatim.
- Course's per-head symbols W^Q/W^K/W^V (no head index) vs paper's W_i^Q/W_i^K/
  W_i^V. Course notation kept.

## 6. Numeric verification

- n/a (0/0).

## 7. Open questions

- none.

## Corrections

none yet — verify against script-12 raw transcription when it lands.
