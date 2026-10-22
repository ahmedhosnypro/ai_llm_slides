# SOURCES — slide 27 — "Self Attention Mechanism (Fundamental Operation)" (formulas + softmax worked example)

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1 (eq. 1) (fetched 2026-10-11).
- Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  (fetched 2026-10-11, raw HTML grepped). NOTATION MATCH: the course's formulas are
  Bloem's formulas verbatim — this post is almost certainly the course's notation
  source.

## 2. Downloaded figures

- None (the slide's content is formulas + a worked example; no source figure).

## 3. Course notation → paper mapping (course formulas VERBATIM)

- Course `y_i = Σ w_ij x_j` ≡ row i of Attention(Q,K,V) = softmax(QK^T)V (paper
  eq. 1) with V = X (no projection): y_i = Σ_j softmax_j(QK^T)_ij · x_j.
  Bloem (verbatim): "y_i = Σ_j w_ij x_j … the weights sum to one over all j".
- Course `w'_ij = x_i^T x_j` ≡ unscaled dot-product score (the (i,j) entry of QK^T
  with Q=K=X). Bloem (verbatim): "w'_{ij} = x_i^T x_j".
- Course `w_ij = exp w'_ij / Σ_j exp w'_ij` ≡ softmax over j. Bloem (verbatim):
  "w_{ij} = exp w'_{ij} / Σ_j exp w'_{ij}". The paper applies softmax to the SCALED
  scores (QK^T/√d_k); the course introduces scaling only later (slides 34/35/37) —
  a sequencing difference, not an error.
- Boxed X_ℓ and X=X2 labels: X_ℓ is the generic ℓ-th embedding (indexed by
  position/role) with the focus word assigned X=X2 — the x-indexed notation family
  is confirmed by Bloem's presentation; the specific boxed-label semantics rest on
  the vision transcript.

## 4. What the sources CONFIRM

- All three formulas as the standard scalar presentation of the paper's eq. (1)
  (semantics per §3.2.1; formulas verbatim per Bloem).
- Softmax worked example [1.3, 5.1, 2.2, 0.7, 1.1] → [0.02, 0.90, 0.05, 0.01,
  0.02]: RECOMPUTED with numpy — matches at the slide's displayed 2-dp precision
  (see §6). The softmaxed values sum to exactly 1.
- "Probabilities" label for w_ij: correct — softmax output is non-negative and sums
  to 1.

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- Course defines w_ij from UNSCALED w'_ij on this slide (scaling arrives on slides
  34/35/37); the paper's softmax always includes /√d_k. Course pedagogy, kept
  verbatim.
- Course's Σ symbols (in y_i and the softmax denominator) appear without explicit
  j-bounds in the transcript; Bloem/paper sum j over the whole sequence. If the
  slide draws them boundless, keep them boundless.

## 6. Numeric verification (softmax(x) = exp(x)/Σ exp(x), computed with numpy)

Input [1.3, 5.1, 2.2, 0.7, 1.1]:
- Recomputed (6 dp): [0.020190, 0.902538, 0.049661, 0.011081, 0.016531]
- Rounded to 2 dp:  [0.02, 0.90, 0.05, 0.01, 0.02]
- Slide (transcript): [0.02, 0.90, 0.05, 0.01, 0.02]
- RESULT: 5/5 match at displayed precision (0.011081→0.01, 0.016531→0.02 are both
  correct 2-dp roundings). PASS 5/5.

## 7. Open questions

- RESOLVED 2026-10-11 (correction worker W-F): script-12 raw transcription carries the
  red note as the single word "Remember" (no body text transcribed; red text near the
  bottom-right of the diagram). Recreation keeps exactly the word "Remember".

## Corrections

Cross-checked against script-12 raw transcription (correction worker W-F, 2026-10-11):

- PATCHED (formula misread, 5 occurrences in slide_027_raw.json): the raw transcribed
  the output equation box as "y_1 = \sum_j w_{1j} x_j" and the green output box as
  "y_1". Corrected to the course form "y_i = \sum_j w_{ij} x_j" / "y_i"
  (subscript 1 → i). Evidence: (a) the course form is Bloem-verbatim (banked in §3
  above); (b) internal consistency — the same slide's diagram uses the i=2
  instantiation (weights w₂₁–w₂₄, query box "X_i = X_2"), so a w_{1j}/y_1 reading
  contradicts the diagram it sits on; (c) the same slide's two other equation boxes
  (w'_{ij} = x_i^T x_j, w_{ij} = exp w'_{ij}/Σ_j exp w'_{ij}) are generic i/j forms
  transcribed correctly, and the serif math font is where 1/i confusion occurs.
  Residual note for build QA: if the visual judge finds the frame literally prints
  "y_1", the frame wins — restore from this record.
- VERBATIM content confirmed unchanged: all three formulas now match the course form
  EXACTLY (y_i = Σ_j w_ij x_j; w'_ij = x_i^T x_j; w_ij = exp w'_ij / Σ_j exp w'_ij);
  table headers (Output layer / Softmax activation function / Probabilities), the
  generic softmax e^{z_i}/Σ_{j=1}^K e^{z_j}, and inputs 1.3, 5.1, 2.2, 0.7, 1.1.
- NUMERIC re-verified with numpy (correction worker, 2026-10-11): softmax([1.3, 5.1,
  2.2, 0.7, 1.1]) = [0.020190, 0.902538, 0.049661, 0.011081, 0.016531] → 2 dp
  [0.02, 0.90, 0.05, 0.01, 0.02] = slide values. PASS 5/5 (confirms §6).
