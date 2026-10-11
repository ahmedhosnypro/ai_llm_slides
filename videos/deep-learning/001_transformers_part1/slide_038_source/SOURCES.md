# SOURCES — slide 38 — "Self Attention Mechanism (Adding Scaling)" (Figure 2-left inset)

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1, §3.2.3, Figure 2 (fetched
  2026-10-11; note: the v7 HTML does not render the figure image — the banked PNG
  below is the figure ground truth).
- Figure bank: ../slide_18_source/ (founder-downloaded paper figures from the same
  arxiv HTML; full provenance in ../slide_18_source/SOURCES.md).

## 2. Downloaded figures

- `slide18 scaled dot-production attention figure.png` — byte-identical COPY of the
  founder's banked paper Figure 2 (left) "Scaled Dot-Product Attention"
  (26,323 bytes, copied 2026-10-11 from ../slide_18_source/; the founder's original
  is untouched and keeps its original name). This is the paper figure the course
  inset redraws in course style.

## 3. Course notation → paper mapping

- Inset inputs Q, K, V ≡ the paper's Q, K, V (§3.2.2: linear projections of the
  input).
- Inset block topology per the paper figure, in DATA-FLOW order (the paper figure
  reads bottom-up): MatMul(Q·K) → Scale (÷√d_k) → Mask (opt.) → SoftMax →
  MatMul(·V) → output.
- The verified vision transcript lists the inset blocks as "MatMul → SoftMax →
  Mask (opt.) → Scale → MatMul" — the SAME topology read TOP-DOWN (output side
  first), which is how the paper's figure stacks its blocks visually.
- Mask (opt.) ≡ §3.2.3: "masking out (setting to −∞) all values in the input of
  the softmax which correspond to illegal connections" — the mask acts on the
  scores BEFORE the softmax in the data flow.

## 4. What the sources CONFIRM

- The inset is the paper's Figure 2 (left) topology in course style — confirmed
  against the banked figure's provenance and eq. (1)/§3.2.3 semantics: two MatMuls
  sandwiching Scale / Mask(opt.) / SoftMax, with Q, K, V as the three inputs.
- Block-level semantics of each stage (MatMul = dot products; Scale = ÷√d_k; Mask =
  −∞ on illegal scores before softmax; SoftMax; MatMul with V): confirmed by
  §3.2.1 + §3.2.3.

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- The transcript's block ORDER ("MatMul → SoftMax → Mask (opt.) → Scale → MatMul")
  is a reading-order artifact of the paper's stacked layout (top-down = output-side
  first); the paper's DATA-FLOW order is MatMul → Scale → Mask → SoftMax → MatMul.
  If the course inset draws the same stacked layout (as its "course-style inset of
  Figure 2-left" description implies), recreate it EXACTLY as the frame shows — do
  NOT "fix" the visual order; the banked PNG is the reference for what the layout
  means.

## 6. Numeric verification

- n/a (0/0).

## 7. Open questions

- [RESOLVED 2026-10-11 via the slide's script-12 raw transcription] Arrow directions
  as drawn: the raw describes the inset with **thin black arrows pointing UPWARD** —
  Q and K (bottom-left) → bottom MatMul → Scale → Mask (opt.) → SoftMax → top
  MatMul; V (bottom-right) → long arrow up the right side into the top MatMul. The
  course inset therefore reproduces the paper figure's bottom-up data flow with
  upward arrows; the block STACK reads top-down (MatMul / SoftMax / Mask (opt.) /
  Scale / MatMul from the top), exactly the reading-order layout §5 records.
  Recreate as drawn; compare against the banked Figure 2-left PNG during QA.

## Corrections

- 2026-10-11 (coordinator, from the slide's raw transcription — no raw patches
  needed): §7 [?] resolved (arrow directions above). Raw transcription consistent
  with the paper-figure topology and the course labels; no data misreads found.
  Raw provenance note: the raw JSON was recovered from a one-off response capture
  after three flaky script-12 parse failures (capture parse-verified before
  writing; content class identical).
