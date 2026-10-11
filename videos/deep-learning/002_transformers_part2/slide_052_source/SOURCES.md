# SOURCES.md — 002 slide 052 "Transformer decoder walkthrough (I feel sick → Je me sens malade)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Machine-verified 2026-10-11 by the Part II
web-verification worker: vision transcript banked
(`transcripts/slide_052_vision_2026-10-11.txt`, default `images` route, one
probe, `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`),
web research via `agy` + live fetches.

## Slide identity

- Video-2 (002_transformers_part2) curated slide **052** ← old extraction
  slide **123** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_052.jpg` (kept from t≈4195 s; shown 4173–4194 s),
  badge numeral 52.
- Content (from the banked vision transcript): a two-panel decoder walkthrough —
  LEFT "Transformer Encoder" panel taking English tokens **I / feel / Sick**
  and emitting 3 output token-grids; RIGHT decoder stack over French tokens
  **SOS / Je / me / sens / malade** in two sub-panels: lower = purple bar
  **"Word and Position Encoding"** → 5 blue cards **"Masked Multi-Head Self
  Attention"** → dark-red bar **"Residual Connection and Layer
  Normalization"**; upper = 5 blue cards **"Encode Decoder Attention"**
  (fed by **K** and **V** circles receiving curved arrows from the encoder,
  **Q** circles from below) → "Residual Connection and Layer Normalization" →
  green bar **"Feed Forward Networks [ One Hidden with RELU Activation]"** →
  "Residual Connection and Layer Normalization" → 5 output token-grids.
  Two red callout boxes label the "Multi-head Encoder-Decoder Attention Block"
  and "Masked Multi-head Self Attention Block". Footnote: "SOS = Start Of
  Sentence". 5 decoder columns vs 3 encoder tokens.

## Primary source — CONFIRMED (architecture), paper verbatim

- **Paper**: "Attention Is All You Need" — Vaswani et al. 2017,
  arXiv:1706.03762v7, **§3.1 (Decoder)** + **§3.2.2 (Multi-Head Attention
  mechanics for cross-attention)**. Verified live 2026-10-11 (recorded in
  `../slide_057_source/SOURCES.md`, same worker session's fleet record — the
  §3.1 fetch quotes are banked there):
  - decoder = stack of N=6 identical layers; inputs are the output embeddings
    **shifted right** (one position; first position = a start-of-sentence
    token — this is exactly the slide's SOS column);
  - sub-layer 1 **masked** multi-head attention (mask out positions > i);
  - sub-layer 2 **encoder-decoder (cross) multi-head attention** — queries
    from the layer below (decoder), keys/values from the encoder output
    (exactly the slide's Q from the decoder column, K/V arrows from the
    encoder panel);
  - sub-layer 3 position-wise **feed-forward**; each sub-layer wrapped in
    **residual connection + LayerNorm** (paper's "Add & Norm" = the slide's
    "Residual Connection and Layer Normalization" bars);
  - embeddings + **positional encodings** at the decoder input (the slide's
    "Word and Position Encoding" bar).
- The slide's architecture content is fully consistent with §3.1 — nothing in
  the transcript contradicts the paper.

## Tutorial counterpart — Jay Alammar, "The Illustrated Transformer" (fetched live 2026-10-11)

- Page: https://jalammar.github.io/illustrated-transformer/ (HTML banked at
  `../scratch/alammar_it.html` during this run; figures verified live).
- CONFIRMED from the live page: its decoding section teaches the SAME
  topology and Q/K/V dataflow — verbatim quote: the "Encoder-Decoder
  Attention" layer "works just like multiheaded self-attention, except it
  creates its **Queries** matrix from the layer below it, and takes the
  **Keys** and **Values** matrix from the output of the encoder stack." The
  paper Fig-1-style decoder figure `Transformer_decoder.png` was downloaded
  into this dir as reference-grade ground truth for the decoder anatomy.
- **CORRECTED (agy confabulation, do not repeat)**: agy (2 queries) asserted
  the slide's exact cartoon — labels "Word and Position Encoding" /
  "Residual Connection and Layer Normalization" / "Feed Forward Networks
  [One Hidden with RELU Activation]", the sentence "I feel sick" → "Je me
  sens malade", and the SOS footnote — comes from Alammar's page with the
  "Je me sens malade" example. **The live page disproves this**: its only
  example sentence is *"je suis étudiant" → "i am a student"* (French→English
  direction; the slide runs English→French), and the strings "malade", "SOS",
  "Word and Position Encoding" do NOT occur on the page. The slide is a
  **course redraw with course-authored labels and a different example
  sentence** — topology/labels follow the paper + Alammar dataflow, pixels
  and wording are the slide's.

## Figures downloaded (into this dir, 2026-10-11)

- `Transformer_decoder.png` — Jay Alammar, "The Illustrated Transformer",
  decoder-anatomy figure (masked MHA → Encoder-Decoder Attention → Feed
  Forward, Q from below, K/V from the encoder side). 879×279 RGBA, 38,751
  bytes, fetched live from
  https://jalammar.github.io/images/t/Transformer_decoder.png (same live
  asset as the copy in `../slide_057_source/`; kept separately per-dir).
- `transformer_resideual_layer_norm.png` — same page, residual-connection +
  LayerNorm concept figure. 666×483 RGBA, 63,629 bytes, fetched live from
  https://jalammar.github.io/images/t/transformer_resideual_layer_norm.png
- Reference-only (not duplicated): banked paper Figure 1
  (`../001_transformers_part1/slide_18_source/The Transformer - model
  architecture..png`) and Alammar's stack figure
  (`../slide_057_source/The_transformer_encoder_decoder_stack.png`).

## What the source CONFIRMS / CORRECTS

- CONFIRMED: decoder-block order (masked MHA → cross-attention → FFN),
  Q-from-decoder / K,V-from-encoder dataflow, residual+LayerNorm wrappers,
  shifted-right inputs with a start-of-sentence token, word+positional input
  encoding, one-token-per-step autoregressive decoding (the 5 SOS..malade
  columns are the running output prefix).
- CORRECTED: nothing contradicts the paper. Note only: the slide runs its
  example **English→French** ("I feel sick" → "Je me sens malade") while
  Alammar's tutorial runs French→English with a different sentence — an
  example swap, not a data error.
- Minor transcription flags (from the vision transcript, for the build):
  "with  RELU" double space; encoder-output grids carry a red "Ŷ"-like mark
  (reading uncertain); the "Channels (4 Filters)-style" count discrepancy of
  slide 042 does NOT apply here.

## [?] Open questions

1. Exact origin of this cartoon rendering (course-redrawn, or copied from an
   unidentifiable third-party tutorial): `[?]` — two `agy` attempts named
   Alammar but the live Alammar page lacks every distinctive label/sentence;
   no other candidate surfaced. Slide frame remains ground truth.
2. The small red mark over the encoder output grids (reads as "Ŷ"/caret):
   exact intent `[?]` (the transcript flags it as partly merged with the Y).
3. Whether the "5 columns vs 3 tokens" asymmetry implies a mid-animation
   state (decoding step 5 of a growing prefix) — likely, but the frame alone
   cannot prove the animation intent `[?]`.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web
sources confirm/correct data and provenance, never license inventing content.
`[?]` markers are removed only with a confirming URL recorded here.

## Raw-landing verification (slide 52, 2026-10-11 — raw pass; nothing above edited)

- `analysis/slide_052_raw.json` (script-12; kept frame frame_04195.jpg, t≈4173–4194 s, old
  extraction 123) now EXISTS and was read in full: agrees with this record on every element —
  callout boxes "Multi-head  Encoder-Decoder / Attention Block" ('Encoder-Decoder'
  italic+underlined) and "Masked Multi-head  Self / Attention Block" ('Self'
  italic+underlined) with thick red arrows into the two containers; upper beige container
  (token-square groups → dark-red "Residual Connection and Layer Normalization" → green
  "Feed Forward Networks [ One Hidden with  RELU Activation]" — 'RELU' monospace + double
  space CONFIRMED → second dark-red bar → five royal-blue 3D boxes "Encode / Decoder /
  Attention" with red K / green V circles fed from the left and a blue Q circle beneath each
  box → pink + green output arrows exiting right); lower pink container (token groups →
  "Residual Connection and Layer Normalization" → five "Masked / Multi-Head / Self
  Attention" boxes with 'Masked' in yellow and red/blue/green curved Q/K/V bundles rising
  from the purple bar → "Word and Position Encoding" → SOS / Je / me / sens / malade);
  left panel (three Y-tagged token groups → royal-blue "Transformer Encoder" →
  I / feel / Sick → pale-green "SOS = Start Of Sentence" legend); badge 52; black mouse
  cursor over the left panel (artifact — omit).
- Open-question status after the raw: [?]1 (cartoon origin — course redraw vs unidentified
  third-party tutorial) STANDS (the raw adds no provenance signal; the Alammar
  confabulation correction above remains the caution of record); [?]2 (red "Ŷ"-like mark
  over the encoder output grids): the raw reads the three tags as plain red "Y" with no
  caret — weakly supporting the merged-glyph misread theory, keep [?] pending a build-time
  zoom; [?]3 (5 decoder columns vs 3 encoder tokens as a mid-animation decoding state)
  STANDS (frame-limited).
- No source changes: the paper §3.1/§3.2.2 decoder architecture + Alammar dataflow
  confirmations (masked MHA → cross-attention with Q-from-decoder / K,V-from-encoder →
  FFN, each Add&Norm-wrapped, shifted-right inputs with SOS) are unaffected; downloaded
  Alammar figures (`Transformer_decoder.png`, `transformer_resideual_layer_norm.png`)
  stay banked in this dir.
