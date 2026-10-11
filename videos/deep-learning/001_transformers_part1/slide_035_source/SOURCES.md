# SOURCES — slide 35 — "Self Attention Mechanism (Embedding Vector Dimension and Softmax Sensitivity)" (scaling box added)

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1 (fetched 2026-10-11): "We compute
  the dot products of the query with all keys, divide each by √d_k, and apply a
  softmax function to obtain the weights on the values."
- Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  — § "2) Scaling the dot product" (fetched 2026-10-11): w'_ij = q_i^T k_j / √k,
  with the vector-length explanation (a vector in R^k with all values c has length
  √k·c, so dividing by √k divides out the growth with dimension).

## 2. Downloaded figures

- None.

## 3. Course notation → paper mapping

- Blue box "Scale down 'Weights' Values before applying SoftMax / Scaling Factor
  should be related to Embedding Dimension 'd'" ≡ paper eq. (1):
  Attention(Q,K,V) = softmax(QK^T/√d_k)V — the scaling applies to the pre-softmax
  scores; the factor √d_k is a function of the embedding dimension.
- Course "related to Embedding Dimension d" ≡ paper √d_k ≡ Bloem √k — all three
  make the factor a function of the embedding dimension; confirmed.

## 4. What the sources CONFIRM

- Scaling happens to the pre-softmax scores (the course's w'_ij "Weights") BEFORE
  the softmax — confirmed by eq. (1)'s structure and the §3.2.1 sentence quoted
  above (divide, THEN softmax).
- The factor's dependence on the embedding dimension: confirmed (paper √d_k with
  the variance-d_k footnote; Bloem's √k with the length argument).

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- Course calls the pre-softmax scores "Weights" in the blue box; the paper's "the
  weights on the values" refers to the POST-softmax w_ij. The course box's own
  phrase "before applying SoftMax" disambiguates; course wording kept verbatim.
- This slide states the factor qualitatively ("related to Embedding Dimension");
  the precise √d appears in the flow on slide 37 ("Scaling by √d"). The paper
  states 1/√d_k outright. Course sequencing, kept.

## 6. Numeric verification

- n/a (0/0) — no worked example on this slide (the examples are slide 34's, and
  they are verified in ../slide_034_source/SOURCES.md).

## 7. Open questions

- none.

## Corrections

Cross-checked against script-12 raw transcription (correction workers W-F + W-F
resumption, 2026-10-11; W-F died on a provider timeout mid-slide — its raw patch
was verified and its SOURCES.md record completed here):

- PATCHED (formula misread, slide_035_raw.json): the raw originally transcribed the
  mid-right boxed equation of the green concept box as "w'_i = x_i^T x_i". The
  course form "w'_{ij} = x_i^T x_j" (Bloem-verbatim, banked in §1/§3) is now in all
  four places that describe that box — equations list, layout region
  (Left concept box), visual_elements, recreation_brief. Evidence: (a) this slide's
  concept box is INHERITED unchanged from slide 34 (dependency 35←34), and slide
  34's independent vision transcription (untouched raw) reads the same box as the
  same equation repeated smaller — "same equation smaller (~12pt) beside a green
  up-arrow" — in all four of its places; (b) internal consistency — slide 35's own
  equations list, visual_elements and recreation_brief already carried the generic
  form, and only the layout-region strings lagged (2 residual spots fixed by W-F
  resumption). Residual note for build QA: if the visual judge finds the frame
  literally prints "w'_i = x_i^T x_i" on the mid-right box, the frame wins —
  restore from this record.
- The dead worker's patch also added explicit "(LaTeX: …)" render annotations to the
  equations list entries (w'_{ij} = x_i^{\mathsf{T}} x_j ×2 and the softmax
  fraction) — content-identical to the course forms; retained.
- VERBATIM content confirmed unchanged: title + subtitle, the blue scaling callout
  ("Scale down \"Weights\" Values / before applying SoftMax / Scaling Factor should
  be related to / Embedding Dimension \"d\""), the trend statement, the warning
  ("High Weight Values kill the gradient, and slow down learning"), all three
  boxed equations (now matching the course form EXACTLY), and the softmax equation
  fraction w_ij = exp w'_ij / Σ_j exp w'_ij.
- NUMERIC re-verified with numpy (W-F resumption, 2026-10-11) — the three softmax
  examples re-shown from slide 34, all 12 output values at the slide's displayed
  4-dp precision: [1,2,3,4] → [0.0321, 0.0871, 0.2369, 0.6439]; [5,10,15,20] →
  [0.0000, 0.0000, 0.0067, 0.9933]; [10,20,30,40] → [0.0000, 0.0000, 0.0000,
  1.0000]. PASS 12/12 (confirms slide 34's verification; same 1.0000-is-a-4-dp-
  rounding-of-0.9999546 caveat applies — print the slide's rounded value).
- No [?] items in the raw. Nothing else patched.
