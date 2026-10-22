# SOURCES — slide 34 — "Self Attention Mechanism (Embedding Vector Dimension and Softmax Sensitivity)"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1 scaling paragraph + its footnote
  (fetched 2026-10-11).
- Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  — § "2) Scaling the dot product" (fetched 2026-10-11; wording match: "kill the
  gradient").

## 2. Downloaded figures

- None.

## 3. Course notation → paper mapping

- Course claim: `w'_ij = x_i^T x_j` grows with embedding dimension d ≡ paper
  footnote (§3.2.1): assuming q, k have components with mean 0 and variance 1, the
  dot product q·k = Σ_{i=1..d_k} q_i k_i has mean 0 and variance d_k — dot-product
  magnitude grows linearly with the dimension.
- Course warning "High Weight Values kill the gradient, and slow down learning" ≡
  paper §3.2.1: "for large values of d_k, the dot products grow large in magnitude,
  pushing the softmax function into regions where it has extremely small
  gradients". Bloem (§ Scaling the dot product, verbatim): "The softmax function
  can be sensitive to very large input values. These kill the gradient, and slow
  down learning, or cause it to stop altogether." — the course sentence is
  essentially Bloem's sentence.

## 4. What the sources CONFIRM

- Dimension-growth claim and gradient-death claim: confirmed by both sources.
- The remedy (scaling) is deferred to slide 35 — consistent with the paper (eq. 1
  divides by √d_k) and Bloem (w'_ij = q_i^T k_j / √k).
- The three softmax worked examples: all RECOMPUTED and match (see §6).

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- Course's worked examples use raw dot products of embeddings (no q/k projections)
  — consistent with the course's pre-projection pedagogy (slides 26–34); the
  paper's analysis is on q·k. Kept.
- Course writes w'_ij (post-dot-product scores) as "Weight Values" in the warning;
  paper calls the pre-softmax quantities "dot products". Course wording kept.

## 6. Numeric verification (softmax(x) = exp(x)/Σ exp(x), computed with numpy)

- softmax([1, 2, 3, 4]) = [0.032059, 0.087144, 0.236883, 0.643914] → max =
  0.6439. Slide claims max 0.6439. PASS.
- softmax([5, 10, 15, 20]) = [0.0000003, 0.0000451, 0.0066925, 0.9932621] → max =
  0.9933. Slide claims 0.9933. PASS.
- softmax([10, 20, 30, 40]) = [9.36e-14, 2.06e-09, 4.54e-05, 0.9999546] → max =
  1.0000 at 4 dp; effectively one-hot. Slide claims 1.0000 (one-hot). PASS.
- RESULT: 3/3 pass. Caveat worth recording: the third example's "1.0000" is the
  4-dp rounding of 0.99995460 (not exactly 1.0) — correct at displayed precision;
  the recreation should print the slide's rounded value, not a fuller one.

## 7. Open questions

- none.

## Corrections

Cross-checked against script-12 raw transcription (correction worker W-F resumption,
2026-10-11): none — consistent.

- All three formulas in slide_034_raw.json match the course form EXACTLY:
  w'_{ij} = x_i^T x_j (twice — the concept box's top-left equation and its smaller
  repeat beside the green up-arrow) and w_{ij} = exp w'_ij / Σ_j exp w'_ij (the
  softmax fraction in the demo-panel header).
- All course labels verbatim: [X_i]_{1×d} (red, twice), SoftMax (three arrows),
  d ↓ / d ↑ / d ↑↑, captions w'_{ij} + For small/medium/large "d", the warning
  "High Weight Values kill the gradient, and slow down learning", the trend
  statement, badge "34".
- NUMERIC re-verified with numpy (W-F resumption, 2026-10-11) — all 12 output
  values at the slide's displayed 4-dp precision: [1,2,3,4] → [0.0321, 0.0871,
  0.2369, 0.6439]; [5,10,15,20] → [0.0000, 0.0000, 0.0067, 0.9933]; [10,20,30,40] →
  [0.0000, 0.0000, 0.0000, 1.0000]. PASS 12/12 (confirms §6; the 1.0000 caveat
  stands — print the slide's rounded value, not a fuller one).
- No [?] items in the raw. No patches.
