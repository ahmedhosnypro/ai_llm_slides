# SOURCES.md — slide 032 "Linear Transformation (= Fully connected Layer)"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 and Peter Bloem's transformers post, plus a python3+numpy check
(no vision calls run; no image access — frame facts below come from the script-12
raw transcription, which is the record of the frame).

## Slide identity

- New (curated) slide **032** ← old extraction slide **62**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_032.jpg`,
  badge "32".
- Frame facts (raw transcription): white panel with the SAME equation as slide
  031's Q panel — **X₂ (1×d) · W_Q (d×d) = X_Q (1×d)**, drawn as pink input pill
  (X_21..X_24) → pale-yellow 4×4 matrix (entries W_11..W_44, color-coded by row:
  blue row 1, magenta row 2, orange row 3, green row 4) → red "=" → pink output
  column **X_Q21..X_Q24**; red title "Linear Transformation" + blue subtitle
  "(= Fully connected Layer)"; elbow block arrow down into a blue-bordered
  **fully-connected-network diagram**: 4 gray/red-bordered input circles
  (X_21..X_24) → gray band holding "W_Q" + weight labels → 4 white/blue output
  circles (X_Q21..X_Q24), 16 all-pairs thin connection lines (red from X_21,
  blue from X_22, faint orange from X_23, green from X_24).

## Primary sources

- **Course notation source**: Peter Bloem, "Transformers from scratch" —
  https://peterbloem.nl/blog/transformers (verified live 2026-10-11). His
  self-attention weight matrices are implemented as plain linear layers.
- **Paper**: https://arxiv.org/html/1706.03762v7 — "Attention Is All You Need"
  (Vaswani et al., 2017) (verified live 2026-10-11) — §3.2.2's projection
  matrices and §3.1's "point-wise, fully connected layers" framing.

## Figures used by this slide

**None — course-authored diagram** (pill-matrix-equals equation + generic FC
network sketch; no published figure is redrawn). Download decision: nothing
downloaded into this dir — no source-hosted figure is plausibly reused here.

## What the sources CONFIRM (data behind the slide)

- **"Linear Transformation = Fully connected layer" is literally true of the
  attention projections.** Bloem implements `W_q`, `W_k`, `W_v` as
  `nn.Linear(k, k, bias=False)` — fully connected (linear) layers, no bias. The
  slide's claim that the X₂·W_Q step IS a fully connected layer matches the
  implementation-level source exactly.
- **Paper parallel**: §3.2.2 defines the projections as learned matrices
  (W_i^Q, W_i^K ∈ ℝ^(d_model×d_k); W_i^V ∈ ℝ^(d_model×d_v)); §3.1 describes the
  Transformer as "stacked self-attention and point-wise, fully connected
  layers" — the paper's own vocabulary unites "attention projection" and
  "fully connected layer" the way the slide does.
- **Output naming X_Q21..X_Q24** (role-suffixed output cells) is consistent
  with the same equation's course rendering; note this slide labels its
  outputs X_Q… where slide 031's raw read its outputs as x₂₁..x₂₄ — recorded
  as a cross-slide observation in slide_031_source/SOURCES.md, not as an error
  here.
- **Matrix subscript convention** (raw: first digit = input index, varying
  across columns; second digit = output index, varying down rows) matches the
  network-diagram labels exactly (red W_11..W_14 on input X_21's fan = W_(input
  1, output j), etc.) and the computation Y_j = Σ_i X_i·W_(i,j). **Placement
  precision (numpy, W-G cross-check 2026-10-11):** with G = the displayed grid
  and x = the input column, `G @ x` reproduces the network-label pairing
  Y_j = Σᵢ Xᵢ·W_(i,j) (verified numerically), while a literal row product
  `X @ G` yields the transposed pairing — i.e., the displayed grid is the
  TRANSPOSE of the row-product's W, equivalently exactly the W of the
  column-vector product W·x. Purely notational (the grid holds generic
  symbols); the frame wins for recreation, recorded for understanding. It also
  matches slide 031's entry layout (row 1 = W₁₁ W₂₁ W₃₁ W₄₁). Convention only;
  neither source fixes one — the frame wins.
- **The FC-network sketch is the graphical form of the same product**: every
  input connects to every output with its own weight = the d×d matrix, exactly
  how a fully connected layer is drawn in any ML course (no single canonical
  published figure; SOURCES_MAP.md row "8–9 challenges" marks such sketches as
  course-authored framing).
- **Numeric verification** (python3+numpy, 2026-10-11; re-run and confirmed in
  the W-G cross-check same day): (1×d)·(d×d) = (1×d) verified; the slide
  transcribes no numeric values (cells are symbols W_11..W_44), so no value
  recomputation applies. Grid-placement check recorded under the convention
  bullet above.

## Course-authored elements (no source counterpart — do not "fix" to a source)

- The white equation panel, the row-color coding of the matrix cells, the
  elbow block arrow, the exact FC-network rendering (gray band, arc marks under
  X_Q21/X_Q22/X_Q24, red/blue/green line coloring by input, the small
  dark-navy arrowhead on a blue line), the red title/blue subtitle colors, and
  the gray #E8E8E8 background with dark-red frame — all instructor's own.

## [?] Uncertain items

- [?] The second blue weight label in the gray band was read "W_21" with the
  raw itself flagging "possibly W_23" — a tiny-label ambiguity only the frame
  can resolve. **raw needs re-check** at build time; no patch.
  (Cross-check 2026-10-11: the raw flags but does not answer this; stays open
  for the build-time frame check. Note the internal coherence argument: blue
  labels ride input X_22's fan, so W_23 is the semantically expected third
  label — but the frame decides.)
- [?] No W_3x labels are shown for input X_23's connection fan (raw flags
  "deliberate omission or paused build"). Frame fact; **raw needs re-check**;
  recreation should reproduce the frame as transcribed until re-checked.
  (Cross-check 2026-10-11: unresolvable from the raw record; stays open.)

## Corrections

- **Cross-check 2026-10-11 (W-G, post-banking):** none — consistent. No
  patches to `analysis/slide_032_raw.json`: both open doubts are tiny-label
  frame ambiguities the raw flags but cannot answer, and the raw's convention
  description ("first digit = input index, varies across columns") is a
  faithful record of the frame. The convention bullet above was refined with
  the numpy grid-placement result (SOURCES.md-side correction, not a raw
  patch).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). The sources confirm/correct DATA and record
provenance; they never license inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy — the slide
wins for recreation, the source wins for understanding.
