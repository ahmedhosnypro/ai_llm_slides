# SOURCES.md — slide 039 "Normalization" (covariate-shift motivation)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_039_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner) cross-checked against `analysis/slide_039_raw.json` (raw
agrees on every string, including the double spaces). Web evidence: Ioffe &
Szegedy 2015 fetched live this run (`scratch/webverify/bn_ar5iv.html`,
ar5iv 1502.03167) + one `agy` query whose wording-level attribution was
CONTRADICTED by the banked paper text (recorded below).

## Slide identity

- New (curated) slide **039** ← old extraction **107** (167 frames = heavily
  taught) — `unique_slides/new2old_mapping.json`, frame
  `unique_slides/slide_039.jpg`.
- Frame facts (vision transcript): title "Normalization" (red); badge "39".
  Blue-boxed italic quote: "The behavior of machine learning algorithms
  changes when the input distribution changes." + right-aligned red
  "{Covariate shift }". Three-box left-to-right causal chain (pale yellow):
  "layer weights changes / during training steps" → "Outputs of Activation
  functions / of each layer change" → "Inputs to the next layer, / (With
  different Input distribution)" (red arrows). Then: "Conclusion:" /
  "Input distribution of each layer changes with each step ." / "The basic
  idea behind Normalization is to:" / "Limit covariate shift by normalizing
  the activations of each layer" (underlined) / "Normalization: Transforming
  the inputs to be Zero mean and unit variance." Bottom cyan panel:
  "Normalization allows each layer to:" → "learn on a more stable
  distribution of inputs," (underlined) / "Accelerate the training of the
  network (don't stick with very small learning rates)."
  - Typographic artifacts kept verbatim: double space in "algorithms
    changes", space before "with each step .", space before "{Covariate
    shift }" closing brace. Bottom letterbox strip.

## Primary source

**Ioffe & Szegedy, "Batch Normalization: Accelerating Deep Network Training
by Reducing Internal Covariate Shift" (arXiv:1502.03167)** — ar5iv body
fetched live 2026-10-11 (`scratch/webverify/bn_ar5iv.html`). Concept-by-
concept confirmations, verbatim from the paper:
- The phenomenon ("Covariate shift" tag): "We refer to this phenomenon as
  **internal covariate shift**, and address the problem by normalizing layer
  inputs." (abstract); "We refer to the change in the distributions of
  internal nodes of a deep network, in the course of training, as Internal
  Covariate Shift." (§1)
- The causal chain (weights change → activation outputs change → next
  layer's inputs change distribution): "the distribution of each layer's
  inputs changes during training, **as the parameters of the previous layers
  change**." (abstract)
- "Zero mean and unit variance" definition: "the network training converges
  faster if its inputs are whitened – i.e., linearly transformed to have
  **zero means and unit variances**, and decorrelated." (§1, citing LeCun et
  al. 1998b; Wiesler & Ney 2011)
- The two bottom bullets: "If, however, we could ensure that the
  distribution of nonlinearity inputs remains **more stable** as the network
  trains, then the optimizer would be less likely to get stuck in the
  saturated regime, and **the training would accelerate**." (§1) + "This
  slows down the training by requiring **lower learning rates** and careful
  parameter initialization…" (abstract) — the slide's "learn on a more
  stable distribution of inputs" / "Accelerate the training of the network
  (don't stick with very small learning rates)" is the course paraphrase of
  these two sentences.
- "The goal of Batch Normalization is to achieve a stable distribution of
  activation values throughout training" (§3.1) — "Limit covariate shift by
  normalizing the activations of each layer".

## Wording provenance (correction to the search answer)

- Fresh `agy` query attributed the exact bullet wording to the Ioffe &
  Szegedy text — **contradicted by the banked paper text**: neither "learn
  on a more stable distribution of inputs" nor "stick with very small
  learning rates" nor the opening quote sentence appears in the paper
  (grep-verified on `bn_ar5iv.html`). The slide's sentences are
  **course-authored paraphrases** of the verified §1/abstract statements
  above. No verified published page carries the exact wording (TDS/GfG
  candidates from the slide-031 query were unverified/hallucinated and are
  not cited). The CONCEPTS are CONFIRMED; the WORDING is course-authored
  (frame wins, keep verbatim).

## Figures used by this slide

- **None.** Course-authored 3-box causal schematic (vision: matches no
  published figure). The paper's Figure 1 (sigmoid-input distribution
  evolution) illustrates the same point but is not reproduced on the slide.

## Course-authored elements

- The quote box, the {Covariate shift } tag, the 3-box chain, the
  Conclusion/idea/definition lines, the bottom two bullets, all highlight
  and underline styling, badge "39" — keep verbatim (including the spacing
  artifacts) for recreation.

## [?] Uncertain items

- [?] exact origin of the opening quote sentence ("The behavior of machine
  learning algorithms changes when the input distribution changes.") — no
  verified source carries it verbatim; treated as course-authored framing
  of the abstract's opening. Open only as wording provenance; the claim
  itself is confirmed (abstract).

## Corrections

- Wording-level attribution by agy corrected against the banked paper text
  (recorded above).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.

## Recreation-stage pixel correction (2026-10-12, build worker)

- **Flow box 2, line 2 color split.** The vision transcript above reads
  "of each layer change" as all-red (and the analysis spec inherited that). Pixel
  measurement during the build's closed loop contradicts it: glyph cores are BLACK
  `(1,2,0)`-class at frame cols 389–471 ("of each layer ") and RED `(107,16,13)`-class
  at frame cols 477–522 ("change"). Frame wins (fidelity law): the recreation renders
  "of each layer " black + "change" red. Independent vision confirmation: the 2x
  dense-region crop comparison (`recreated_pptx/qa/slide039/crop_flow_comparison_1.txt`,
  PASS) reads the split as identical in both images. The full-slide transcript's
  "all red" stands recorded as a small-text color misread (same class as its
  "black" bullets reading, which pixel measurement corrected to navy).
