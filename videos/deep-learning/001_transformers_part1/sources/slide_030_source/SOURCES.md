# SOURCES — slide 30 — "Self Attention Mechanism (Input Word plays Different Roles)"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1, §3.2.2, §3.2.3 (fetched 2026-10-11).
- Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  (§ "Self-attention with key, query and value transformations" — a passage that
  near-verbatim poses and answers the slide's question).

## 2. Downloaded figures

- None (course-original diagram: yellow role circles around X2 as Key / as Value /
  as Query).

## 3. Course notation → paper mapping

- X2 as Query / as Key / as Value (three role circles on the same vector) ≡ the
  paper's three roles drawn from ONE input set: Q = XW^Q, K = XW^K, V = XW^V
  (§3.2.2); §3.2.3: "in this layer queries, keys and values come from the output of
  the previous layer" — one source set, three roles.
- Course note "Should we use SAME X2 Vector for the three Roles ?" ≡ Bloem
  (verbatim): "In the basic self-attention we've seen so far, each input vector
  must play all three roles. We make its life a little easier by deriving new
  vectors for each role, by applying a linear transformation to the original input
  vector."

## 4. What the sources CONFIRM

- The three-roles framing and the question it raises — confirmed by the paper
  (three learned projections from the same input) and by Bloem's near-identical
  wording (strong evidence the course follows this presentation).
- The implied ANSWER (no — derive three different vectors) is what the course
  implements on slide 37 with W_q/W_k/W_v — matching the paper's W^Q/W^K/W^V
  (§3.2.2) and Bloem's W_q/W_k/W_v (three k×k matrices).

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- On this slide the course keeps the SAME X2 vector in all three roles (raw,
  unprojected) and poses the question; the paper never presents an unprojected
  three-roles stage. Course pedagogy, kept verbatim.
- Course's W^Q/W^K/W^V (as seen later, d×d per slide 37's legend) vs paper's
  W_i^Q/W_i^K/W_i^V (d_model×d_k). Notation/dimension difference, kept.

## 6. Numeric verification

- n/a (0/0).

## 7. Open questions

- none.

## Corrections

Cross-checked against script-12 raw transcription (correction worker W-F resumption,
2026-10-11): none — consistent.

- All course labels match the established notation verbatim: KEYS / Values / Dot
  Product / Soft max / Σ, W₂₁–W₂₄ (subscripted), K / Q / V badges, X₁–X₄ (subscripted),
  ⊗ multiply nodes, badge "30", and the two inherited callouts "Matched KEYS with
  Relevance Percentage" / "Retrieve VALUES Weighted by their Relevance" (verbatim,
  consistent with parent slide 29).
- Role callouts and question are course-authored text confirmed via Bloem/paper
  (internal consistency only, per §3/§4): "X₂ is used as Key" / "X₂ is used as
  Value" / "X₂ is used as Query" / "Should we use SAME X₂ Vector for the three
  Roles ?" (space before "?" kept) — all present verbatim in the raw.
- Subtitle inherited from slide 29, same unclosed-paren pattern — verbatim, kept.
- No attention formulas printed (only symbolic labels) — nothing to check against
  the course formula set. No softmax numbers — n/a (0/0). No [?] items in the raw.
  No patches.
