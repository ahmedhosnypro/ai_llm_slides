# Register — slide_057 (doc-parse accuracy audit, wave 2)

Scope worker: `worker-slide_057` · DB scope `slide_057` (done) · blocker task id **1** (`parse_loop_finish_length`, closed this wave).
Inputs: `03_parses/slide_057/call01_pass1|call02_pass2|call03_retry_pass1|call04_retry_pass2/slide_057.parse.{md,json}`,
`04_ground_truth/slide_057/` (inventory.md + 6 frozen GT files), `05_comparison/slide_057_comparison.md`,
verdicts `06_vision_checks/slide_057_vision.md` (pixel adjudication: tesseract OCR native + 4x word-TSV, color-mask
ink maps, color-cluster censuses — all coordinates frame px on 960×540).
Corroboration vocabulary: transcript-level findings are corroborated by 4 calls agreeing (pass2 pair byte-identical,
cmp-verified) and by the pixel adjudication where cited.

## Findings (severity-ranked)

### BLOCKER

- **B1 — Repetition-loop collapse; `finish=length` on 4/4 calls.** REAL · confidence high · **corroborated**
  (call02_pass2 vs call04_retry_pass2 byte-identical; call01 vs call03 identical 6-unique-line set; adjudication
  verdict 1). All four calls (`03_parses/slide_057/call01..call04*/slide_057.parse.json`, `finish_reason=length`,
  usage 1024/3000/1024/3000 output tokens — exactly the budgets) emit a 21-line identical prefix, then loop the
  bare token `Decoder` ×482 (1024-budget) / ×1470 (3000-budget). On-image the literal string "Decoder" exists only
  ~17 times (legend x466 y448; vertical label x830..855 y225..344; 15 attention-box lines) — the repeated lines are
  model-invented output, though not content hallucination (repetition, not invention; `hallucinated_confirmed=0`).
  Failure is budget-independent and deterministic; endpoint was healthy (no 429/5xx, stderr 0 lines). Defect class:
  degenerate generation (drop + loop), root of every other finding. Closes task 1: confirmed reliability failure.

### MAJOR

- **M1 — dropped-region: 42/48 GT strings lost; coverage ~12%.** REAL · confidence high · **corroborated**
  (adjudication verdicts 3, 4, 11–13). Every dropped group was re-verified legible on the same frame: 8 X-chips +
  8 Y-chips (e.g. Y-row last label OCR "N1" at (419,120)), 8 word-row labels (red ink in all boxes), both embedding
  bars ("Word Embedding" orange ink x≈233..310 y424..431; "Positional Encoding / Embedding" conf 75–86 at
  (197..338, 446..454)), K/V/Q badges ("K=" conf 32.7 at (515,160); big-Q 48 dark-red px at (818..850, 425..455)),
  5 bottom tokens (glyph runs 3/2/2/4/7 at y498..504), Softmax (7-glyph blob x681..705 on maroon bar y70..76),
  `Encoder Block M/1/0` (conf 90–97 at (226,160)/(227,299)/(225,341) — parse caught only "2" at (227,258)),
  plus the sweep additions: the tri-color legend — **the most readable dropped region** ("Encoder" conf 91.5 at
  (466,428), "Decoder" conf 89.1 at (466,448), "Attention" conf 86.1 at (462,467)), the red "Residual Connection
  and Layer Normalization" bars (OCR-verified y268/289/350/371; ink-verified y143/432 — the parse carried the
  string once, unpositioned; certified build encodes 7 redBar instances y143.5/164/268/288/348/368/432 per
  `04_ground_truth/slide_057/slide_057.js:335-369`, one of which the adjudicator's list does not explicitly verify —
  sub-threshold at JPEG scale, single-read), the two vertical side labels (red "Encoder" x73..89 y256..360; green
  "Decoder" x830..855 y225..344 — both match build geometry), and the "Encoder / Decoder / Attention" 3-line text
  inside the 15 navy attention boxes (partial reads "Encode/Lrcod/An/Arert" at y179..317). Also absent: all
  class-token/region markup (class-token-mismatch in the degenerate form — zero tokens emitted) → layout roles
  detected 0/6.

- **M2 — coordinate-misalignment: the parse's sole positioned token is an anchor artifact.** REAL · confidence high ·
  **corroborated** (adjudication verdict 2/13). `<x_0.0586><y_0.0789>57` → (56.3, 42.6) px lands exactly on the
  frame border's top-left corner (top border y≈43 from x≈58) — an anchor artifact, ~820 px from the true badge
  (ink-map: circle x859..893, y53..87, glyphs "5"+"7", center ≈(876,70)). 0/1 parse items within the ~80 px
  tolerance; the mis-anchored coordinate is unusable for layout reconstruction. GT-side caveat (MINOR, DEBATABLE,
  single-read): the adjudicator's measured badge circle (x859..893) sits ~17 px left of the playlist chrome constant
  used in my wave-1 claim (`shared_patterns/house_chrome.js` badge center (893,71) → box x875..911, whose right edge
  would cross the actual right border at x≈901); `components/slide_047.js:18` already notes "frame badge center is a
  curation artifact" — a per-frame badge offset, project-side observation only, no bearing on the parse scores.

### MINOR

- **m1 — FFN bar label: separator DEBATABLE, "RELL" wrong.** DEBATABLE · confidence high · **corroborated**
  (adjudication verdict 5). Parse `Feed Forward Networks / One Hidden with RELL Activation` vs build
  `Feed Forward Networks - One Hidden with RELU Activation`: OCR reads RELU conf 90.3 at (736,357) — "RELL" is a
  misread (REAL error); but the separator ink is a ~1–2px-wide, 5–8px-tall diagonal at x≈670–672 drifting
  top-right→bottom-left (x672@y360 → x670@y366), read by OCR as "(" / "[" — the parse's "/" was closer to the
  image than the build's flat hyphen. Text-fidelity score counts this string NORMALIZED (glyph/separator
  confusions) either way.
- **m2 — wording settlements (build-vs-analysis divergences), all resolved for the build.** REAL · confidence high ·
  **corroborated** (adjudication verdicts 6–10). (a) decoder purple bar y≈487–496 reads "Word and Position
  **Encoding**" (OCR "Word and Posmton §ncoding") — build wins over analysis "Embedding"; (b) lavender box line-1
  ink span ≈ x589..608 (~10 glyphs) fits "Multi-Head" — "Masked Multi-Headed" (19 glyphs ≈ 38px) cannot fit a
  34px box — build wins; (c) last chip subscript is **N-1** (Y-row OCR "N1" at (419,120); X-row ink includes a
  "1" stroke at x≈435; 8 chips only, centers x114.5..419.5) — 0-BASED law wins over analysis's extra X_N/Y_N;
  (d) Softmax bar present (verdict 9); (e) bottom tokens ARE labeled SOS/Je/ne/suis/faisait (glyph counts
  3/2/2/4/7; first blob x597..607, last x775..794) — analysis "unlabeled boxes" wrong. None of these strings
  reached the parse (they live in the 42 dropped).
- **m3 — reading-order unassessable; no reading-order-inversion finding.** DEBATABLE · confidence high · single-read.
  The 6 surviving lines' order (57 → Encoder → Decoder → Encoder Block 2 → FFN → Residual) does not match the
  top-down image order (Softmax y71 → Residual y143 → FFN y152 → Residual y164 …), but the survivors are
  truncation debris, not a reading pass — order fidelity cannot be scored from this transcript; recorded as
  unassessable rather than inverted. Sub-threshold non-text items (right-margin marks x≈820..840 y≈263..335, mark
  at ≈(456,486), bottom player strip y≈516..538) were correctly out of GT scope (build omits per GROUND RULES(c);
  adjudication §11).

## Scores (0–10, one-line justification each)

- **accuracy — 3/10.** Everything emitted was real (0 content hallucinations, 5 EXACT + 1 NORMALIZED strings), but
  1 of 6 unique strings carried a glyph error ("RELL"), the only coordinate is an anchor artifact ~820 px off, and
  coverage is 6/48 = 12.5%.
- **reliability — 0/10.** 4/4 calls end `finish_reason=length` in a deterministic `Decoder` loop (482×/1470×);
  retries reproduce the failure byte-identically — `finish_all_stop=0`, the only such slide in the set.
- **detail — 1/10.** Six bare strings and zero class tokens; no regions, coordinates (beyond the one artifact),
  colors, fonts, shape semantics, or structure (0/6 layout roles; certified build encodes ≈820 primitives).
- **recreation_power — 1/10.** A builder learns only the domain (Encoder/Decoder/Attention vocabulary) — no
  geometry, palette, fonts, or bar/box/circle inventory to rebuild from; everything needed lives in the dropped 87.5%.
