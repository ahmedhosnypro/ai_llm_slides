# SOURCES — slide 49 — "Transformer Stacked Encoder Blocks"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: `transcripts/slide_049_vision_2026-10-11.txt` (2026-10-11,
default `images` route, thinking=high, streamed — banked by this worker).

## Slide content (from the vision transcript — ground truth)

- Title "Transformer Stacked Encoder Blocks" (badge 49). Left labels: "Encoder
  Output", "Encoder Input", "Embedding Words & Pos.", "Input Seq". Bottom-to-top:
  Word 0…Word 5, …, Word N-2, Word N-1 → stacked bars "Word Embedding" (tan)
  + "Positional Encoding / Embedding" (cyan, black-outline container) → segmented
  token row X₀…X₅, …, X_{N-2}, X_{N-1} → pale-blue stack of solid-blue slabs
  "Encoder Block 0" → "Encoder Block 1" → "Encoder Block 2" → …(blue dot
  columns)… → "Encoder Block M" → segmented token row Y₀…Y₅, …, Y_{N-2},
  Y_{N-1}.
- Dependency 49←26 (001 family, "common patterns … but not same as them" per
  `slide_dependencies.json`): reuse the 001 self-attention family's verified
  token-flow PATTERN (X_i in → Y_i out per position); do NOT clone slide 26's
  composition. Slide 26's own provenance record:
  `../001_transformers_part1/slide_026_source/SOURCES.md`.

## 1. Source URLs (fetched live 2026-10-11)

- Vaswani, A. et al. (2017), "Attention Is All You Need", arXiv:1706.03762v7 —
  https://arxiv.org/html/1706.03762v7 — §3.1: "The encoder is composed of a
  stack of N=6 identical layers" (fetched live 2026-10-11; the slide generalizes
  the count to M+1 blocks indexed 0..M). §3.5: "we add 'positional encodings' to
  the input embeddings at the bottoms of the encoder and decoder stacks… same
  dimension d_model as the embeddings, so that the two can be summed" (same
  fetch) — the slide's two stacked bars under the X row. Figure 1 bank: 001
  `../001_transformers_part1/slide_18_source/` (do NOT re-download).
- Jay Alammar, "The Illustrated Transformer" —
  https://jalammar.github.io/illustrated-transformer/ (page fetched live
  2026-10-11): the stacked-encoder depictions
  (`The_transformer_encoders_decoders.png`, `The_transformer_encoder_decoder_stack.png`)
  are the closest published style (stack of encoder slabs, bottom-to-top token
  flow). The course's drawing is its own (blue slabs, explicit 0..M indices,
  Word/embedding/PE bars) — referenced, not downloaded (no direct figure reuse).

## 2. Downloaded figures

- None (course-original schematic; the transcript's resemblance analysis concurs
  — "original custom schematic", not a copy of Vaswani Fig 1/2, Bloem, or an
  Alammar figure).

## 3. What the sources CONFIRM

- A STACK of identical encoder layers sits between input and output: §3.1
  (N=6; course M+1, generic) — confirmed.
- Inputs = word embeddings + positional encodings summed at the stack bottom:
  §3.5 — confirmed (the two bars below the X tokens).
- Per-position token streams X_i → Y_i through the stack: §3.1 + the 001
  self-attention family pattern (dep 49←26) — confirmed.

## 4. Course vs source discrepancies (recreation keeps course verbatim)

- Block count: course "Encoder Block 0..M" (M+1 blocks, generic M) vs paper's
  N=6 concrete stack. Generalization, kept verbatim.
- The slide shows NO sub-layer internals (no MHA/Add&Norm/FFN inside the blocks)
  — the course split that detail across slides 45–48; presentation choice, kept.
- Slide 48's rows end X_{N-1}, X_N; slide 49's end X_{N-2}, X_{N-1}. Course
  inconsistency between slides; frame wins (49 = 0-based …N−1, consistent with
  47).

## 5. Numeric verification

- Indices 0…N−1 (tokens/words), blocks 0…M. No other numerals (badge 49). The
  paper's concrete N=6 recorded above for understanding.

## 6. Open questions

- [?] Exact middle subscripts of the small token cells (transcript: digits
  2..5 plausible, low legibility). Resolve against script-12 raw if the build
  needs them; the pattern (0..N−1 with ellipsis) is unambiguous.

## Corrections

none yet — verify against script-12 raw transcription when it lands.

## Cross-check (parallel web-verification worker, 2026-10-11 — reconciliation note by this worker)

A parallel worker processed this range concurrently and DOWNLOADED a reference
figure into THIS dir (recorded here because this file's §2 predates it):

- `The_transformer_encoders_decoders.png` — Jay Alammar, "The Illustrated
  Transformer" encoder+decoder stack figure, fetched live from
  `https://jalammar.github.io/images/t/The_transformer_encoders_decoders.png`
  (756×474, sha256[:16] dc659655cf7305f7 — parallel worker's record; verified
  on disk by this worker). Closest published depiction of the stacked-encoder
  style; the course's drawing remains its own redraw [?] pixel-wise.
- Parallel worker's map row flags the bar ORDER ("Word Embedding" bar drawn
  ABOVE "Positional Encoding / Embedding") as a course quirk vs paper Figure 1
  (which adds PE to the embeddings; this record's transcript read the same
  order: tan "Word Embedding" upper, cyan "Positional Encoding / Embedding"
  lower). Course quirk kept verbatim.
- Parallel worker notes a bigger Alammar stack figure is already banked in
  `../slide_057_source/` — reference that for the decoder-side work.
- Middle token subscripts: same [?] as this record's open question.

## Raw-landing verification (slide 49, 2026-10-11 — raw pass; nothing above edited)

- `analysis/slide_049_raw.json` (script-12; kept frame frame_03994.jpg, t≈3981–3993 s, old
  extraction 117) now EXISTS and was read in full. It RESOLVES the middle-subscript open
  question: the input row reads **X_0, X_1, X_2, X_3, X_4, X_5, [5 green dots], X_{N-2},
  X_{N-3}[?]** and the output row **Y_0 … Y_5, [5 blue dots], Y_{N-2}, Y_{N-1}**; the word
  row reads Word 0…Word 5, Word N-2, Word N-1. Digits 2–5 are therefore CONFIRMED. One
  residual flag: the FINAL X token's subscript is raw-read "X_{N-3}" with the raw itself
  noting "likely X_{N-1}, subscript slightly blurry" [?] — build-time PIL zoom of the last
  X cell decides (the Y row's parallel cell reads N−1 cleanly, supporting X_{N-1}).
- Everything else agrees with this record: title "Transformer Stacked Encoder Blocks",
  badge 49 (black text in a yellow circle), left label column ("Encoder Output" / vertical
  blue bold-italic "Transformer Encoder" / "Encoder Input" / "Embedding Words & Pos." /
  "Input Seq"), tan "Word Embedding" bar drawn ABOVE the cyan "Positional Encoding /
  Embedding" bar (course quirk kept, as already recorded), four dark-blue "Encoder Block
  0 / 1 / 2 / M" bars with 8 columns of dark-red arrows between consecutive bars and blue
  dot columns between Block 2 and Block M, and the color-coded arrow families (gray /
  medium-blue / dark-red / bright-green).
- No source changes (Vaswani §3.1 "stack of N=6 identical layers" and §3.5
  embedding+positional-encoding anchors unaffected; 49←26 pattern-family note stands;
  banked Fig 1 referenced, not re-downloaded).
