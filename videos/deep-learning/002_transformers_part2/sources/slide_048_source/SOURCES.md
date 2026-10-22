# SOURCES — slide 48 — (untitled full-bleed) "Encoder Block" + two insets (original block; Alammar encoder zoom)

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: `transcripts/slide_048_vision_2026-10-11.txt` (2026-10-11,
default `images` route, thinking=high, streamed — banked by this worker).

## Slide content (from the vision transcript — ground truth)

- Badge partially occluded ("8" visible → 48 per file id/curation). MAIN panel:
  slide 47's "Encoder Block" composition (Block Input → Multi Head Self
  Attention → ⊕ residuals in dashed orange containers → "Layer Normalization
  (NOT Batch N[ormalization])" bars → per-token FFN cells under "Feed Forward
  Networks [ One Hidden wi…]" → Block Output), tokens X₀…X₄, …, X_{N-1}, X_N.
  Right-inset overlay truncates some right-edge text (overlay artifact).
  - FFN cells carry a tiny label read as "MHA" or "MLP" [?] (low-legibility;
    likely "MLP" given context — resolve against script-12 raw).
- RIGHT INSET (white panel, thick green border): "Multi-Head Attention" fed by
  red circles V, K, Q → "Add & Norm" → "Feed Forward" → "Add & Norm", with two
  black residual loop lines — the published-figure style inset.
- BOTTOM-LEFT INSET (green border): caption "The Original Encoder Block" around
  a tiny schematic + a small word reading "Sentence(s)" [?].

## 1. Source URLs (fetched live 2026-10-11)

- Jay Alammar, "The Illustrated Transformer" —
  https://jalammar.github.io/illustrated-transformer/ (page fetched live
  2026-10-11). **Figure `Transformer_encoder.png`** is the inset's source
  family: it is the figure Alammar places at "Each one is broken down into two
  sub-layers" (self-attention → feed-forward), showing Multi-Head Attention with
  V/K/Q inputs → Add & Norm → Feed Forward → Add & Norm with two residual loops.
  The vision transcript independently describes the inset as closely matching
  this figure (labels, V/K/Q red circles, green Add&Norm / yellow-green FFN /
  tan attention colors, loop routing).
- Vaswani, A. et al. (2017), arXiv:1706.03762v7 — https://arxiv.org/html/1706.03762v7
  — §3.1 (see `../slide_047_source/SOURCES.md` §1 for the verbatim quotes): the
  main panel's two residual+LayerNorm wraps and the "NOT Batch Normalization"
  label (the paper's [1] IS Layer Normalization, Ba et al. 2016). Figure 1 bank:
  001 `../001_transformers_part1/slide_18_source/`.
- Normalization tie-in: this lecture's slides 41–44 (esp. 44's "Transformer
  choice" on LayerNorm) motivate the "(NOT Batch Normalization)" annotation.

## 2. Downloaded figures

- `Transformer_encoder.png` — Alammar's encoder zoom (792×411, 32,628 B),
  fetched from
  `https://jalammar.github.io/images/t/Transformer_encoder.png` into THIS dir
  (unrenamed). Identity: the right inset's source figure family. Pixel-level
  match of the course's redraw vs this file: [?] per-slide build-time check
  (course redraws are established precedent; labels/colors agree).

## 3. What the sources CONFIRM

- The inset's composition (MHA(V,K,Q) → Add&Norm → FFN → Add&Norm, residuals):
  §3.1 + Alammar's encoder figure — confirmed.
- "Layer Normalization (NOT Batch Normalization)": §3.1 uses layer normalization
  [1]; the 2017 paper never batch-normalizes the transformer — confirmed.
- Main panel = slide 47's verified encoder layer (same §3.1 anchors).

## 4. Course vs source discrepancies (recreation keeps course verbatim)

- Token indexing: slide 48 ends rows at X_{N-1}, X_N while slide 47 (same
  diagram) ends at X_{N-2}, X_{N-1}. Course inconsistency between consecutive
  slides; each frame wins for its own recreation.
- Truncated strings on the main panel ("…NOT Batch N", "…One Hidden wi") are
  caused by the right inset overlaying the diagram — the slide's own layering;
  recreation reproduces the overlay, not the completed text. [?] the full
  intended strings are almost certainly the slide-47 forms ("Layer Normalization
  (NOT Batch Normalization)" / "Feed Forward Networks [ One Hidden with RELU
  Activation]") — note only; recreation follows the frame.
- Bottom-left inset's tiny schematic identity: [?] (labels illegible at 960px).
  Candidate: a thumbnail of the original Vaswani Figure 1 encoder half (banked
  in 001 `slide_18_source/`); confirm at build time if needed.

## 5. Numeric verification

- Token indices 0…N (course indexing). No other numerals (badge "8"-of-"48").

## 6. Open questions

- [?] The tiny FFN-cell label ("MHA"/"MLP") — resolve via script-12 raw or a
  founder frame check.
- [?] Pixel-exact identity of the right inset vs the downloaded Alammar figure
  (family identity CONFIRMED; pixel match at build time).
- [?] Bottom-left inset "The Original Encoder Block" schematic identity
  (candidate: banked Fig 1 encoder half thumbnail).

## Corrections

none yet — verify against script-12 raw transcription when it lands.

## Cross-check (parallel web-verification worker, 2026-10-11 — reconciliation note by this worker)

A parallel worker processed this range concurrently; its per-slide record
survives in the SOURCES_MAP rows. Unique findings mirrored here:

- Downloaded figure sha recorded by the parallel worker matches this dir's file:
  `Transformer_encoder.png` sha256[:16] c6d3360f8c0a4701 (792×411) — identity
  confirmed from both runs.
- **Main-diagram source (parallel worker, HIGH origin via agy): Ketan Doshi,
  "Transformers Explained Visually (Part 2): How it works step-by-step",
  Towards Data Science** —
  https://towardsdatascience.com/transformers-explained-visually-part-2-how-it-works-step-by-step-b49fa4a64f34/
  — Block Input/Output, NOT-Batch-Norm bands, dashed groups, plus-circles all
  match. TDS was unfetchable from this network (2× ETIMEDOUT, parallel worker);
  pixels [?] pending build-time check.
- Badge: the parallel worker reports script-12 raw read "49" while the frame
  reads 48 — resolved toward 48, founder check pending [?] (consistent with
  this record's occluded-badge reading).
- FFN-cell tiny label: parallel worker read "MLA", plausibly "MLP" [?] — same
  open question as this record's "MHA"/"MLP".
- Bottom-left inset: parallel worker calls it the "Transformers Encoder"
  thumbnail; this record's transcript read the caption as "The Original
  Encoder Block" — same inset, both readings agree it is a miniature of the
  original block [?] identity pending build-time zoom.

## Raw-landing verification (slide 48, 2026-10-11 — raw pass; nothing above edited)

- `analysis/slide_048_raw.json` (script-12; kept frame frame_03981.jpg, t≈3900–3980 s, old
  extraction 116) now EXISTS and was read in full. It RESOLVES the FFN-cell tiny-label
  question: every pink feed-forward box carries the tiny caption **"MLP"** (raw labels:
  "MLP" ×6; imagery: "tiny 'MLP' caption" per box) under the bar title "Feed Forward
  Networks [ One Hidden with  RELU Activation]" — the "MHA"/"MLA" readings are superseded;
  that open question is CLOSED.
- Main panel confirmed: vertical red "Encoder Block" title, "Block Output"/"Block Input"
  tags, token rows X₁…X₄, Xₖ, X_{N-1}, X_N (one-based, matching this record's indexing
  note vs slide 47's …N−1 ending) → maroon "Multi Head Self Attention" bar (bold yellow) →
  Y rows → dashed-orange ⊕ rows → tan "Layer Normalization (NOT Batch N[?orm)]" bars →
  pink MLP boxes (~8 green neurons each) → top Y row; the string truncations ("…NOT Batch
  N", "…One Hidden wi") are the right inset's overlay, as recorded (raw: "caused by the
  overlapping right inset panel, not by animation").
- Right inset confirmed against the banked figure family (`Transformer_encoder.png`,
  sha256[:16] c6d3360f8c0a4701): red V/K/Q circles (K with a line to the panel bottom) →
  tan "Multi-Head Attention" → light-green "Add & Norm" → yellow "Feed Forward" → second
  "Add & Norm", with the thick black residual path — composition matches the Alammar
  figure; the pixel-level redraw check stays [?] at build time.
- Bottom-left inset: the raw reads its caption as **"Transformer Encoder"** (green border,
  gray "Encoder" box, tiny "Inputs" below, curved side connector) — supporting the parallel
  worker's reading over this record's earlier "The Original Encoder Block"; identity as a
  miniature of the original block figure [?] unchanged (candidate: banked Fig 1 encoder half).
- **Badge conflict ELEVATED, not resolved**: this raw independently reads the badge numeral
  as **"49"** (yellow circle, bold red) — now the SECOND machine read of this frame saying
  "49" (the earlier parallel-worker raw also read 49; only the first transcript saw an
  occluded "8"). Under the root house rule (badge = the number PRINTED on the original
  image) a frame genuinely printing 49 takes badge 49 despite file id 48; under 002's
  AGENTS.md the numeral is assumed = file id. These cannot both hold here. Decisive check:
  PIL zoom of `unique_slides/slide_048.jpg`'s top-right badge + founder confirmation [?] —
  do NOT silently pick either value in the build.
- No source changes (§3.1 anchors + the downloaded Alammar figure unaffected).
