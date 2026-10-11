# SOURCES — slide 26 — "Self Attention Mechanism (Fundamental Operation) (Self Attention of word X2 w.r.t All words in Sentence (X1, X2, X3, X4))"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1 "Scaled Dot-Product Attention"
  (fetched 2026-10-11).
- Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  (fetched 2026-10-11; uses the same scalar presentation of this exact operation).

## 2. Downloaded figures

- None. The slide's diagram is a course-original drawing (course style/colors);
  no source page hosts a matching figure. Bloem's illustrative SVG
  (`/files/transformers/self-attention.svg`) shows the same picture family but is
  not the course's figure and was not downloaded.

## 3. Course notation → paper mapping

| Course (slide 26, verbatim) | Paper (§3.2.1, eq. 1) |
|---|---|
| Embedding columns X1–X4 | input vectors x_j (rows of X); here also playing key/value roles |
| Dot Product ("Similarity") | compatibility = q·k; here raw dot products x_2·x_j (unscaled scores w'_2j) |
| Soft max ("Probabilities") | softmax over j (they sum to 1 → "probabilities") |
| W21–W24, multiplied (⊗) then summed (Σ, "Weighted SUM") → Y | attention weights w_2j applied to the values; output row = Σ_j w_2j v_j |

- The one-word framing (X2 w.r.t. all words) is row i=2 of the full
  Attention(X,X,X) operation.
- At this stage the course uses raw embeddings with NO scaling and NO Q/K/V
  projections: this is eq. (1) with Q=K=V=X — the standard pedagogical special case
  (it is exactly Bloem's "basic self-attention": y_i = Σ_j w_ij x_j).

## 4. What the sources CONFIRM

- Operation semantics (dot-product similarity → softmax → weighted sum of the
  values): §3.2.1 — "We compute the dot products of the query with all keys, divide
  each by √d_k, and apply a softmax function to obtain the weights on the values";
  "The output is computed as a weighted sum of the values, where the weight assigned
  to each value is computed by a compatibility function of the query with the
  corresponding key."
- The Diagram semantics (four embeddings → scores → probabilities → ⊗ weights → Σ
  → output) match the paper's per-query computation for query 2.

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- Course labels the four softmax weights "W21–W24": here W denotes SCALAR attention
  weights w_2j, not learned matrices (the paper's W always means learned
  projections). Recreation keeps "W21–W24" verbatim.
- Course labels: "Similarity" (pre-softmax) and "Probabilities" (post-softmax) —
  course labels, kept verbatim.
- No Query/Key/Value vocabulary on this slide — the course introduces it on slide
  29; the paper uses it from §3.2.1. Course sequencing, kept.

## 6. Numeric verification

- None on this slide (no worked example). n/a (0/0).

## 7. Open questions

- none.

## Corrections

Cross-checked against script-12 raw transcription (correction worker W-F, 2026-10-11):

- All course labels match the established notation verbatim: Similarity / Dot Product /
  Soft max / Probabilities / Weighted SUM, W₂₁–W₂₄ (subscripted), Σ, Y, X₁–X₄, subtitle
  "(Self Attention of word X₂ w.r.t All words in Sentence ( X₁, X₂, X₃, X₄ )".
- One patch to the raw JSON: the equations list carries an interpretive note for the
  graphically-depicted (NOT printed) output equation, transcribed as
  "Y = Σᵢ ( W₂ᵢ × Xᵢ )"; its summation index was aligned to the course form
  (Bloem-verbatim y_i = Σ_j w_ij x_j instantiated at i=2) → "Y = Σⱼ ( W₂ⱼ × Xⱼ )".
  Nothing printed on the slide changes (the note is explicitly marked implicit).
- No softmax numbers on this slide — n/a (0/0). No [?] items to resolve.
