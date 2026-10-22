# SOURCES — slide 45 — "Multi Head Self Attention of Word X2 'Narrow' Architecture"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: 2026-10-11. The course notation quoted below is the
recreation target — kept VERBATIM. The paper is the semantic reference only.

## 1. Source URLs

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.2.1 (per-head attention semantics),
  §3.2.2 (multi-head; the paper has NO projection-free variant) (fetched
  2026-10-11).
- Peter Bloem, "Transformers from scratch" — https://peterbloem.nl/blog/transformers
  — § "3) Multi-head attention" (fetched 2026-10-11): the chunked/"narrow-style"
  computation — "slice the resulting sequence of vectors into chunks", reshape h ×
  k//h, 3h matrices of size k × k/h; and the update log: "19 October 2019 — Added a
  section on the difference between wide and narrow self-attention" (origin of the
  course's Wide/Narrow vocabulary).

## 2. Downloaded figures

- None (course-original five-head diagram with the color-coded "To Head 1..To Head
  5" legend).

## 3. Course notation → paper mapping

- "Split vectors into 'H' chunks" ≡ narrow self-attention: the d-dim embedding is
  split into H non-overlapping chunks of size d/H; head_i attends using only its
  chunk (Bloem's efficient scheme: reshape to h × k//h and slice; "wide" vs
  "narrow" = full learned projection vs embedding slice).
- Per-head inner pipeline (Dot Product → Scaling by √d → Soft max → Σ weighted
  sum) on the chunk ≡ §3.2.1's Attention applied within each head — semantics
  confirmed (same dot/scale/softmax/weighted-sum operation).
- Concat of the H chunk-outputs (1×dH = 1×d, since the chunk sizes sum back to d)
  with the Linear Transformation REMOVED ≡ multi-head WITHOUT W^O. The paper does
  NOT describe this projection-free variant (its multi-head always ends with
  W^O ∈ ℝ^{h·d_v × d_model}); Bloem's efficient chunked implementation also still
  keeps W_o/unifyheads. The course's removal of the output linear is the course's
  own dimensionally valid variant — exactly what makes "Narrow" cheaper.

## 4. What the sources CONFIRM

- The chunking scheme (each head works on a slice of the embedding) as a
  recognized multi-head arrangement: Bloem's efficient multi-head description; the
  Wide/Narrow terminology originates in Bloem's post (its own update log).
- Per-head attention semantics (dot → scale → softmax → weighted sum): §3.2.1.
- Dimensional validity of concat-straight-to-output: follows because the chunk
  dims sum to d — and this is what makes the output projection removable.

## 5. Course vs paper discrepancies (NOT defects — recreation keeps course notation)

- "Narrow" (chunked heads, NO output projection) is not in the 2017 paper — the
  paper's multi-head is always the projected ("wide") form ending with W^O.
  Record as a course-specific variant; the recreation keeps the course
  architecture verbatim (no Linear Transformation block, concat 1×d straight to
  output).
- Course illustrates H=5 chunks (five heads, per the "To Head 1..To Head 5"
  legend); paper h=8 with d_k = d_model/h. Illustration choice, kept verbatim.
- Bloem's chunked implementation still applies W_o; the course's Narrow drops it.
  Course choice, kept.

## 6. Numeric verification

- n/a (0/0).

## 7. Open questions

- [?] The exact original wording of Bloem's wide/narrow definitions: the blog's
  update log confirms the section was added 19 Oct 2019, but the section text is
  absent from the currently served page (rewritten out per the 4 Mar 2023 update
  note) and from the 2021 archive snapshot fetched during research; the
  wide/narrow SEMANTICS recorded in §3 are confirmed from the live multi-head
  section and a web-search summary, not from a verbatim quote of the added
  section.

## Corrections

Cross-checked 2026-10-11 (correction worker) against the script-12 raw transcription
(`analysis/slide_045_raw.json`, vision transcript of record); the MultiHead output
projection was also re-confirmed live the same day — arXiv v7 §3.2.2 reads
"MultiHead(Q,K,V) = Concat(head_1,...,head_h)W^O" (the paper's multi-head always
ends in W^O; see §5):

- Narrow variant confirmed in the raw: NO "Linear Transformation" block appears
  anywhere in the transcription — the five head-output Y vectors (blue "1·d/H"
  labels) feed the 5-segment "Concatenated Vector 1·d" bar straight to the top
  output vector (1·d). Exactly the projection-free variant §§3/5 describe; no patch.
- "Split vectors into 'H' chunks" caption, the 5-row chunk table ("To Head 5" …
  "To Head 1") with per-head colored sub-chunks, and the five h=1…h=5 head layers all
  match §§3/5 (H=5 illustration choice, kept verbatim). Per-head pipeline in the raw
  (Dot Product → K·q/√d → Scaling by √d → Soft max → ⊗ V → Σ Weighted SUM → Y 1·d/H)
  is §3.2.1's attention applied within each head — confirmed; no patch.
- Per-head W^q/W^k/W^v matrix boxes with head subscripts (W₁^q … W₅^v [?]) match the
  chunked scheme (each head owns its projections acting on its 1·d/H chunk); the
  top-right equation box ([strip 1·d/H] · W = [strip 1·d/H], "d : Embedding Length")
  is the per-head chunk projection in the course's own bookkeeping.
- Raw reading flagged for the build-time frame read, NOT patched: the h=1 query is
  transcribed "q₁ [?]" although the slide tracks word X₂ (title; X₂ pink-highlighted
  in the input strip, red arrow out of X₂). Slide 37's same-family diagram used q₂
  for X₂. The frame is ground truth — keep "q₁" verbatim unless the frame read shows
  "q₂"; same for the [?] K₁–K₄/V₁–V₄ subscripts and the W^k superscript.
- No patches applied to the raw.
