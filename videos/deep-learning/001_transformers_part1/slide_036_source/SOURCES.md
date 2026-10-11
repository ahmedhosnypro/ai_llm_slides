# SOURCES.md — slide 036 "Self Attention Mechanism" (Scaling based on Square Root of Embedding Vector Dimension)

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via
pdftotext of the banked v5 PDF (`../slide_012_source/1706.03762v5.pdf`), a
grounded agy web search, and independent numeric computation; no image access
— frame facts below come from the script-12 raw transcription
(`../analysis/slide_036_raw.json`).

## Slide identity

- New (curated) slide **036** ← old extraction slide **78**, diff 0.0
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_036.jpg`,
  kept frame `frame_03603.jpg` (3452–3602 s of the lecture, 151-frame group).
- Frame facts (vision pass — ground truth for WHAT is shown): title "Self
  Attention Mechanism", dark-red subtitle "(Scaling based on Square Root of
  Embedding Vector Dimension)" with yellow highlight on '(Scaling'; badge
  '36'; left green panel with before/after column vectors (V₁ = 12 X's → 12
  M's labeled 1xd₁; V₂ = 5 X's → 5 M's labeled 1xd₂, orange dashed divider,
  white block arrow); mint equations box ("Let Average Values of elements of
  V₁/V₂ = M"; "Vector Length of V₁ (all Ms) = V₁ᵀ V₁ = M √d₁" / same for V₂
  with d₂); bell-curve box (Gaussian, blue dashed peak line, blue 'M' under
  x-axis); green statements "√d is a good choice for scaling" and "⁴√d Some
  times is used"; three red formula boxes "SoftMax [w′ᵢⱼ]", "SoftMax
  (w′ᵢⱼ/√d)", "d=100, √d =10"; red Remember box ("d" is Dimension of
  Embedding / Not length of input Sequence); bottom flowcharts: unscaled
  SoftMax(10,20,30,40) → [0.0000, 0.0000, 0.0000, 1.0000], and scaled chain
  [10,20,30,40] ÷ (√d) → [1,2,3,4] → SoftMax → [0.0321, 0.0871, 0.2369,
  0.6439].

## Primary source

- **URL**: https://arxiv.org/abs/1706.03762 — §3.2.1 "Scaled Dot-Product
  Attention" (v5 PDF banked in `../slide_012_source/`, the complete 15-page
  paper; same section exists in v7 HTML — family record in
  `../slide_18_source/SOURCES.md`).
- **Paper**: "Attention Is All You Need" — Vaswani et al. (2017),
  arXiv:1706.03762.

## What the source CONFIRMS (data behind the slide)

- **The scaling rule and its rationale** (v5 §3.2.1, verified via pdftotext):
  "We compute the dot products of the query with all keys, divide each by
  √dk, and apply a softmax function to obtain the weights on the values";
  "for large values of dk, the dot products grow large in magnitude, pushing
  the softmax function into regions where it has extremely small gradients…
  To counteract this effect, we scale the dot products by 1/√dk"; Eq. (1)
  Attention(Q, K, V) = softmax(QKᵀ/√dk)V. This is exactly the slide's point:
  unscaled SoftMax over large-magnitude scores saturates ([0.0000, 0.0000,
  0.0000, 1.0000]), scaled does not.
- **Numeric example values — verified by independent computation
  (2026-10-11), all four decimals exact**: softmax([10,20,30,40]) =
  [0.0000, 0.0000, 0.0000, 1.0000] at 4 dp ✓; with d = 100 ⇒ √d = 10 (the
  slide's own "d=100, √d =10" box), scaled input [1,2,3,4] and
  softmax([1,2,3,4]) = [0.0321, 0.0871, 0.2369, 0.6439] at 4 dp ✓. The
  division chain [10,20,30,40] ÷ √d → [1,2,3,4] is internally consistent
  with d = 100.
- **The norm value in the course's derivation**: a d₁-dimension vector whose
  elements all equal M has Euclidean length M·√d₁ (‖V₁‖ = √(V₁ᵀV₁) =
  √(M²·d₁)) — the slide's "Vector Length of V₁ (all Ms) = … = M √d₁" end
  value is mathematically correct for the length.
- The paper's saturation-gradient footnote anchor (small-gradient softmax
  regions) is the same phenomenon the slide's Remember box warns about
  ("High Weight Values kill the gradient" is slide 35's wording; here it is
  the Remember box's d-is-embedding-dimension caveat).

## Course-authored elements (no paper counterpart — do not "fix" to paper)

- **The notation w′ᵢⱼ is course-internal**: v5 contains no scalar w′ᵢⱼ
  (its §3.2.1 is matrix-form only). The definition lives on the preceding
  slide 35 (raw: `w'_ij = x_i^T x_j` and `w_ij = exp w'_ij / Σ_j exp
  w'_ij`), so slide 36's unscaled box SoftMax[w′ᵢⱼ] (softmax over raw
  dot-products) vs scaled box SoftMax(w′ᵢⱼ/√d) reuse the course's own
  symbols. Keep them verbatim.
- The toy-vector panel (V₁ with 12 elements / V₂ with 5 elements, X's
  replaced by M's, 1xd₁ / 1xd₂ labels), the "Let Average Values … = M"
  setup, the bell-curve schematic, "⁴√d Some times is used", the "d=100"
  example, the Remember box, all box colors/highlights, and the two
  flowcharts are instructor pedagogy; the paper contains none of these.

## Discrepancy for understanding (recorded, NOT patched — frame is ground truth)

- The equations-box line "Vector Length of V₁ (all Ms) = V₁ᵀ V₁ = M √d₁"
  writes the dot product as if it were the length: strictly V₁ᵀV₁ = M²·d₁
  and only its square root equals M√d₁. The slide's final value (M√d₁) is
  correct for the vector length; the middle equality is course shorthand.
  This is the slide's own math, not a transcription error — the raw is
  faithful to the frame, so nothing is patched; recreate as shown.

## Figures used by this slide

- None downloaded — the slide is course-authored boxes/schematics; no public
  figure's pixels are reused (per `SOURCES_MAP.md` download rule). The §3.2.1
  text evidence lives in the banked `../slide_012_source/1706.03762v5.pdf`.

## [?] Uncertain items

- [?] "⁴√d Some times is used" — the instructor's claim that fourth-root
  scaling is sometimes used. Grounded web search (agy, 2026-10-11) found NO
  mainstream architecture or paper replacing 1/√dₖ with 1/dₖ^{1/4}; d^{1/4}
  appears only in auxiliary contexts (e.g. the equivalent re-parameterization
  that moves the 1/√dₖ factor into Q/K initialization with std d^{-1/4},
  spectral singular-value laws, embedding-size heuristics). No confirming
  citation found; the frame text stands as-is.

## Corrections

- none — patches: **0**. All checkable data verified correct: softmax outputs
  (both flowcharts) exact to 4 dp; √d scaling example consistent (d=100 ⇒
  √d=10 ⇒ [1,2,3,4]); vector dimensions and labels internally consistent.
  The V₁ᵀV₁ shorthand and the ⁴√d remark are frame content (course math /
  instructor claim), not transcription errors.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). This source confirms/corrects DATA and records
provenance; it never licenses inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy above —
the slide wins for recreation, the source wins for understanding.
