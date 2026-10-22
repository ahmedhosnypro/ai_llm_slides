# SOURCES.md — 002 slide 051 "split halves of the Transformer architecture figure" (working title — no raw analysis yet; title TBD from frame)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory; founder-flagged special slide). Machine-verified
2026-10-11 by the Part II web-research worker (no vision calls run — no image
access; the frame placement below is deliberately left to the vision worker).

## Slide identity

- Video-2 (002_transformers_part2) curated slide **051** ← old extraction slide
  **122** (`unique_slides/new2old_mapping.json`), frame
  `unique_slides/slide_051.jpg` (kept from t≈4129 s), badge numeral 51.
- Founder flag + `slide_dependencies.json` `special.51`: this slide shows **001's
  slide-18 source image (arXiv 1706.03762v7 Figure 1) split into left and right
  halves, placed at different measured positions on this slide**.
- Cross-video dependency: `51 ← deep-learning/001_transformers_part1:18`
  (001 slide 18 = the Fig 1 + Fig 2L + Fig 2R paper-figures slide; its provenance
  record is `001_transformers_part1/slide_018_source/SOURCES.md`).
- `[pending raw]` — 002 script-12 analysis has NOT run for this slide yet; the
  frame facts above come from the founder's directive, not a raw transcription.

## Primary source

- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 — **Figure 1**,
  "The Transformer - model architecture."
- **Live asset URL**: https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png
  (NOTE: under `/Figures/`, NOT `/assets/` — see Failed-findings note in the map).
- **Banked original** (do NOT modify):
  `../001_transformers_part1/slide_18_source/The Transformer - model architecture..png`
- **Byte-identity proof (2026-10-11)**: banked file = live arXiv asset, both
  159,152 bytes, sha256 prefix `56d69ccc192b90c3` — the bank's Figure 1 is
  byte-identical to the paper's published asset. So BOTH halves of this slide
  inherit the bank's provenance in full.

## Figures used

The banked Figure 1 (1520×2239 RGBA) **split into left/right halves at the image
midline x=760**. Machine-derived in this dir from the banked original (bank
original untouched):

- `fig1_left_half_x0-760.png` (760×2239, sha256[:16] `93b5ff68248fb219`)
- `fig1_right_half_x760-1520.png` (760×2239, sha256[:16] `7fd176d5bc3298cf`)

Measured facts about the split line (deterministic pixel analysis, 2026-10-11):

- The figure's central white gap between the encoder and decoder columns spans
  x=716–803 (two ≥98%-white bands: 716–756 and 765–803).
- The midline x=760 passes through that gap and **clips a 9-px black vertical
  connector line at x=758–766 (rows y=802–1107)** — part of the K/V arrow
  assembly feeding encoder output into the decoder's Encoder-Decoder Attention.
  A literal "split in half" produces exactly this clipping; each half keeps a
  4–5 px stub of that line.
- Reassembly of the two halves is pixel-identical to the banked original
  (verified programmatically) — the halves are a lossless decomposition.
- Alternative semantic cut candidates (if the frame shows cleaner-cut halves):
  mid-band cuts at x=736 or x=784, which leave the connector line wholly on the
  right half. `[?]` — adjudicate against the frame before composing.

## What the source CONFIRMS

- Provenance: whatever this slide shows as its two halves is (per the founder)
  the paper's Figure 1 — the canonical encoder+decoder composition. Left half =
  the paper's encoder column (input embedding, positional encoding, N×
  [Multi-Head Attention + Feed Forward], each with Add & Norm); right half = the
  decoder column (output embedding shifted right, positional encoding, N×
  [Masked MHA + Encoder-Decoder Attention + Feed Forward], final Linear +
  Softmax). (Layout per the paper's Figure 1 / §3.1 and the bank's SOURCES.md —
  not re-verified pixel-by-pixel here.)
- The half files in this dir are certified-lossless derivatives of that banked,
  byte-identical asset.

## Course-authored elements

- **Placement and size of each half on THIS frame**: `[?]` pending the vision
  pass — the vision worker must PIL-measure (or template-match) each half's
  position/scale against `unique_slides/slide_051.jpg` and compose exactly
  (founder directive: "Attention needed"). Vision work goes through
  `.agents/skills/image-analysis` (banked `.txt` transcripts).
- Whether the halves are recolored/redrawn by the course or used as-is:
  `[?]` pending raw + vision.
- House chrome (red frame, yellow badge "51", title line) is course chrome per
  the playlist law (`../AGENTS.md`, `../shared_patterns/house_chrome.js`).

## [?] Open questions

1. Exact cut line used by the course (midline x=760 vs x=736/784 band cuts) —
   resolve against the frame.
2. Whether the course applies any recolor/scale beyond placement — resolve
   against the frame.
3. Slide's verbatim title/banners — `[pending raw]` (script-12 has not run).

## Corrections

None yet — record any slide-vs-source discrepancy here when the raw analysis
and vision pass land (fidelity law: slide wins for recreation, source wins for
understanding).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what each slide shows; web sources
confirm/correct data and provenance, never license inventing content. `[?]`
markers are removed only with a confirming URL recorded here.

## Image-mechanism SETTLED (2026-10-12, PIL forensics — append-only)
The frame does NOT contain literal halves of the banked Figure-1 PNG (rejected on correlation +0.20/+0.10, 2.26× aspect distortion, palette mismatch, zero cut-edge stubs). 002:51 inherits 001:18's provenance for CONTENT/TOPOLOGY only — the builder must REDRAW both panels as vectors at measured placements (LEFT (140,105) 304×397; RIGHT (566,99) 315×408; measured saturated palette) — see scratch/slide51_mechanism/SLIDE51_MECHANISM.md for the full measurement. The fig1_*_half*.png files in this directory remain the founder's downloads (untouched) but are NOT the frame's pixels.

## Build-worker measurement pass (2026-10-12, append-only — resolves the [?]s above)

The 051 build worker (scratch/slide051/m01..m11 + selfcheck_attempt_*.py + gate
probes) CONFIRMS the SETTLED verdict above and adds the composition facts used by
the certified-style build (`recreated_pptx/build/slide_051.js`):

1. `[?]` cut line — MOOT for the raster (no raster present, per the correlation +
   palette forensics and this worker's independent palette count: Fig 1's tan
   143,609 px -> 16 px in the frame; light-blue 87,347 -> 8; black 288,904 -> 315).
   The operative "split" is the light SEAM at frame x 724..726 (full height,
   (237,211,154)/(237,238,196)) between the orange callout zone and the mint stack
   zone. The fig1_*_half*.png files stay banked but unused.
2. `[?]` recolor/redraw — RESOLVED: the halves are the instructor's REDRAWN
   architecture, the same drawing family certified for 001 slides 17->18->19.
   Palette identity table (frame core -> 001-certified constant): encPanel
   (253,237,221)~FBECDB; decPanel (206,255,225)=C8F8E0 EXACT; steel Add&Norm
   (109,153,180)~6D99B4 / (92,156,183)=5C9CB7; indigo (97,126,213)~6E87E0; FF
   (128,117,96)~807560 / (110,126,98)=6E7E62; encoder MHA salmon
   (200,126,87)=C87E57 + solid red frame; decoder MHA tan-brown (173,132,86)~B28659
   + red ring; Masked MHA (210,130,205)~CE8ADC, text (97,14,104)~562366;
   embeddings (168,121,79)~B08058 / (172,101,97)=B8706C; V/K/Q navy
   (0,0,155)~2A26A0; residual green ~7FB421/8CC62E.
3. DECISIVE split evidence: the yellow V/K L-highlight is CUT ACROSS THE PANELS —
   encoder keeps the bar (237..289, 243..258) + right stub (285..289, 258..310);
   decoder keeps the continuation (724..734, 242..310) + end bar (742..775,
   300..311) — exactly 001:17's drawYellowBand L (678,251,67,16 / 730,267,15,41 /
   740,307,47,16) cut at the seam.
4. `[?]` title — RESOLVED (gate probe probes/title.txt, character-accurate):
   "Encoder – Decoder Transformer" (en dash, spaces), red C00000 bold, ink
   frame x 224..737, cap y 58..81.
5. Spec-color corrections (frame wins): overlay green = 11FF74 (not 00E100);
   decoder panel orange = F2A557 (not ED7D31); the spec's black footer bar = the
   video letterbox (frame rows 519..539 -> slide y >= 542.7) — omitted per ground
   rule (c) + the certified 002 slide-002/050 precedent.
6. `[?]` remaining: sub-6pt micro-labels (Q/K/V letters, tan-bar glyphs at frame
   392..396, the bottom yellow box's word) sit at the video-resolution floor; the
   spec's verbatim strings are used and the visual judge arbitrates at
   full-frame + crop resolution.

## Resume-worker round 2 (2026-10-12, append-only — judge-1 fixes + crop-comparison record)

Judge attempt 1 (qa/slide051/judge_attempt_1.txt, on render_4) FAILed: (B1) decoder
PE cluster missing, (B2) decoder Nx circle missing, (M3) encoder "Add & Norm"
truncated to "Norm", + 4 MINORs. Resume worker (attempt 5) measured each in
scratch/slide051/m12..m18 and fixed:

1. B1 RESOLVED BY MEASUREMENT: the "clock icon" is the maroon Output Embedding
   box's right portion (b-channel split x782..812: no brown icon anywhere; box
   x740..806 = B8706C with dark-maroon text strokes). Decoder PE cluster = box +
   the "Positional Encoding" label (added at 806,402, matches measured x805..858
   y403..425) + the dark-brown check LEFT of the box (orig ink x726..738 y428..449)
   — added. NO PE icon exists on either panel (encoder region C scan: none).
2. B2 RESOLVED BY MEASUREMENT: the orig cluster x828..862 y280..310 = tan "Nx"
   circle (829,289) d~20 (text sub-resolution) + green check badge disc at
   (853,290) d19 — mirrors the encoder's certified pair. Added. The navy disc at
   (800..819, 312..330) holds a WHITE CHECK (probe dec_nxpe, 3x), not "Nx" — fixed.
3. M3 ROOT CAUSE: residual stubs 1/3 (x199..244) are drawn AFTER the box text and
   cover "Add & " (texttest + z-order). Orig stubs 1/3 are SHORT (x195..211);
   stub 2 is long (x195..249). Fixed + solid corner patches at the bus joints
   (orig joint x194..202 y310..322 is a filled rounded corner).
4. Crop comparisons through the gate (qa/slide051/crop_cmp_enc_norms.txt,
   crop_cmp_dec_right.txt): round 1 FAILed the encoder region on (a) residual
   stubs vs continuous paths + (b) missing FF→A&N connectors — both fixed with
   measured short connectors (encoder x~245: y277-279/306-311/322-327 + arrowhead;
   decoder x~772: y212-216/241-254/309-317); round 2 PASSed the encoder region
   (all deltas MINOR). Also fixed: black disc + white check overlapping the FF
   box's left edge (x202..214 y282..302, was a gray-patch artifact), FF fill core
   (136,133,117)→888575, MHA box top y342 (border measured, was y345).
5. RESOLUTION-FLOOR DISPOSITIONS (crop findings NOT acted on — sub-3px glyphs,
   spec-vs-pixel conflicts; the full-frame judge arbitrates): decoder QKV-circle
   letters (measured: 2 navy discs ~(740,376)/(782,376) d~12 + a green disc
   ~(784,388); spec says "Q red/K blue/V green" — colors conflict with measured
   navy); the "⊕ node + swirl symbol" on the PE→embedding path (no ⊕-shaped ink
   found in x712..762 y438..478; the probe's "swirl" = the maroon box's text at
   3x); badge navy tone (orig (0,0,~120) vs vkBlue 2A26A0 — MINOR per crop judge);
   capture tint (cream vs tan — the certified 002 tint precedent).
6. Cross-video law record: the certified parent component
   (001:18, passed in its own DB) is REQUIRED by absolute path in the build and
   its certified constants (salmon C87E57, tanBrown B28659) are reused; calling
   its renderBase is impossible for this frame (no geometry transform in the API;
   every parent block is baked at 001's unsplit geometry; the yellow-band piece
   map 52x15/4x52/10x68/33x11 vs 67x16/15x41/47x16 kills any affine copy) — full
   record in the build header. This is the content dependency honored without a
   geometry clone, per the settled "redraw at measured placements" verdict above.

## Resume-worker round 3 (2026-10-12, append-only — judge-2 adjudication + PASS)

Judge attempt 2 (render_5) FAILed with 5 MAJORs. Every claim was adjudicated against
the frame (scratch/slide051/m19/m20 pixel masks + raw samples):

- VARIANCE (contradicted by pixels, documented, not fixed): #3 "large yellow block"
  (yellow masks orig-vs-render IDENTICAL: bar y244..258 x239..289 + right stub
  x287..290); #1 "encoder light-green rounded outline" (no outline ink anywhere in
  x211..286 / y258..380; the green is the bus+stubs); #7 "orange band 61% vs 50%"
  (orange ends x724..725 in both, m17); #5 "(shifted right) containment" (text ink
  bottom ~y498 vs panel border y501).
- MEASURED REAL, FIXED: continuous QKV-row bar y382..391 x196..246 (was two short
  bars with a gap) + bright right segment + brown connector x245.5 y392..400; the
  "tan bar" is actually DARK BROWN (88..91,58..65,30..33) y393..395 x196..277 (the
  old light-tan bar + yellow line were misreads — replaced); stub2 bright segment
  x224..249; decoder trunk is a CONTINUOUS ~10px band x814..824 y199..390 (was two
  5px segments); green bar below the Masked MHA y383..391 x778..814 (was absent);
  red check beside the decoder MHA (spec-backed, x801..816 y286..306); decoder top
  arrow lowered to the measured y114..137.
- Judge attempt 3 (render_6): **PASS** — final verdict with 5 MINORs only, all
  resolution-floor/styling items consistent with the dispositions above (PE "dial"
  glyph = the dark-brown bar + connector at crop zoom; QKV micro-circles ~6px;
  olive-vs-green residual tone; yellow L-shape geometry; stack proportion within
  tolerance). No BLOCKERs, no containment violations. Transcript:
  recreated_pptx/qa/slide051/judge_attempt_3.txt. Certificate: single-read,
  default route (images), glm leg DEFERRED/BLOCKED; judge procedure executed by the
  worker (no spawn tool available in this environment), per the orchestrator-approved
  fallback.
- Banking: NO deck's dependency graph references 002:51 as a parent (verified across
  videos/deep-learning/*/slide_dependencies.json) — no component-export obligation.
