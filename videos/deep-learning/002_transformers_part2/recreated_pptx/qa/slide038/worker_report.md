# Worker report — slide 038 "Residual Connections and Normalization" (002_transformers_part2)

Worker: BUILD WORKER, slide 038 end-to-end. Resumed from the prior worker's crash
(provider timeout at launch — it banked only measurement scripts + zoom crops in
`scratch/slide038/`, no build, empty qa dir); scratch measurements m1–m8 + crops
z_*/hh_* reused per the resume rule. Attempt numbering started at K=1 (no prior
renders/transcripts existed).

## Deliverable

- **PPTX**: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_038_recreated.pptx`
  (single version, no suffix; no equations -> no OMML pass; no advanced graphs).
- **Build script**: `recreated_pptx/build/slide_038.js` (thin wrapper) ->
  **banked component**: `recreated_pptx/build/components/slide_038.js`
  (`renderBase(pptx, slide, {numeral})`) — **banking obligation MET**: slide 59
  depends on 38 (in-video edge), and the dependency audit recommends 38←36 (36
  unbuilt => STANDALONE build from this slide's own spec; component ready for a
  future 36-family refactor and for slide 59).
- **Assets**: `build/assets/s038_blkarrow.png` (spiral-hatched navy block arrow,
  16 placements), `build/assets/s038_orangearrow.png` (curved residual arrow,
  8 placements) — PIL-generated at 4/6 px-per-pt, embedded at exact pt/72 sizes.

## Attempts used: 1 of 6 — FINAL VERDICT: PASS

| K | render | judge transcript | verdict |
|---|---|---|---|
| 1 | `qa/slide038/render_1.png` | `qa/slide038/judge_attempt_1.txt` | **PASS** (0 BLOCKER, 0 MAJOR, 4 MINOR) |

Judge procedure executed BY THE WORKER (no Agent/Task spawn tool in this
environment — orchestrator-approved fallback per 17 §7): probe
(`probe_1.txt`, valid body, window opened) + full comparison with the frozen `-p`
GROUND RULES template, `--thinking high --max-tokens 65536`, W4 wide wall
(540s wrap / 420s inner), default route (images), single-read,
glm leg DEFERRED/BLOCKED. Zero degenerate-garbage events.

### Judge findings (all MINOR, none fix-mandated)

1. MINOR — recreation token boxes slightly larger / more saturated than the
   original's washed-out video cells (spec colors #FFFF00/#92D050/#FF9999/#D9D9D9
   kept per the approx-hex law; the original is JPEG-washed).
2. MINOR — the spiral hatching inside the hollow block arrows reads as an
   "H"-like glyph at small size; original arrows read plainer at frame resolution
   (sheets A/B/C DID see spiral/spring hatching in the original's arrows at high
   zoom, so the detail is faithful at the source level).
3. MINOR — defbox vertical rhythm between the two "Adding" groups a touch looser
   (all five lines are at their individually measured ink positions).
4. MINOR — top token row marginally closer to the inner red frame (measured
   geometry; containment verified at all edges).
Judge also independently confirmed: labels read Y_1..Y_6, dots, Y_{N-1}, Y_N
(1-based), X row same, unclosed bracket "[With Same Input Vectors Dimension"
faithfully reproduced, mouse cursor correctly omitted (rule (c)).

## Pre-judge self-checks (all PASS — banked)

- `house_chrome_check.py render_1.png 38` → **PASS** (panel x 89–1913, badge
  center (1860,148) d=70, within tol 8) — playlist chrome, numeral 38.
- `selfcheck_attempt_1.py` (+ `selfcheck_attempt_1_output.txt`): defbox/panel gap
  empty; defbox = exactly 5 text bands (no wrap); panel/container containment;
  11 color samples OK (navy 00008B, gray bar D9D9D9, 4 cell colors, blue/green
  dots, plus ring, caption highlight, title ink); navy band 874..980 px vs
  expected 874..981; gray band 646..696 vs 645..698; 8 plus-circle centers within
  0.5pt of measured; red/green/navy arrows + 16 block arrows + orange curves all
  present; caption 4685 red px; title ink y 73.9..94.6 / x 236.6..781.9 vs
  target 74.3..94.2 / 232.4..788.9. Patterns applied: house-chrome,
  inner-frame-budget (containment logic), dense-region-crop-compare,
  highlight-box, explicit-line-spacing (N/A — all single-line boxes; lineSpacing
  still pinned on the two valign-middle boxes).
- Dense-region crop comparisons (gate, `--thinking high`): 
  `cropcmp_text_1.txt` (title/defbox/graybar/caption — all text verbatim incl.
  the dangling bracket; recreation judged faithful) and
  `cropcmp_diagram_1.txt` (top row/plus row/tails/annotations).
- Plus-node density closed loop: original full-circle red fraction 0.39–0.42 vs
  recreation 0.46–0.47 after thickening the ring to 2.75pt + 14pt bold "+".

## Content decisions & evidence (frame is ground truth)

- **Vector labels 1-BASED: Y_1..Y_6, 5 blue dots, Y_{N-1}, Y_N; X row same; mid
  row carries primes (Y′).** Evidence: the transcript of record
  (`slide_038_source/SOURCES.md`, full-frame thinking-high read) + raw agreement;
  pixel-width analysis of the tail subscripts (col7 subscript ink spans ~13px
  across two cells = 3 glyphs "N-1"; col8 = single 6px glyph "N" in its own cell
  with no digit ink at 842+ where "N-1"'s second glyph would sit); col1's
  subscript is a narrow 3px stem (an Arial "1", not a 4–5px ring "0"). The three
  zoomed-vision reads that said "Y_0.., N-2/N-1" (sheets A/C, diagram cropcmp)
  were reading cell-border-contaminated 3px glyphs (cell borders run at pitch
  12px exactly through the subscript zone) and pattern-completing; the
  border-corrected pixel reads supersede them. This also matches the spec brief's
  6 pre-dot column structure; the brief's guessed tails (Y_{N-3}, Y_{N-2}) are
  superseded per SOURCES.md's own indexing note, which prescribed exactly this
  build-time zoom.
- **Labels are printed ON the bars** (red bold italic, centered per column,
  overlapping the 3rd pink sub-cell), NOT beside them — sheet C high-zoom reads
  ("the peach square contains a dark red Y with a red subscript"); the "blue
  labels" near the mid/X rows in the raw spec are the hollow block arrows'
  outline strokes (double-cluster signature).
- **Bar structure**: 4 sub-cells × 12.5pt = 50pt bar, order [FFFF00][92D050]
  [FF9999][D9D9D9], thin dark outlines; per-row measured heights/bands.
- **Arrows**: thin red up-arrows gray-bar→top-row; thin green ⊕→gray-bar; thin
  navy mid-row→⊕ (all crossing the green dash-dot container border, as in the
  original); 16 hollow navy block arrows with spiral hatching (X→block,
  block→mid); 8 orange curved residual arrows entering each ⊕ from the left —
  drawn BEHIND the navy block (measured: original curve ink vanishes at the
  block's rows, re-emerges below — caught by the judge probe as an overlap defect
  and fixed before the comparison).
- **⊕ nodes**: white fill + thick red ring (2.75pt) + bold red "+" — density
  closed-loop matched to the original (0.46 vs 0.39–0.42 full-circle red).
- **Omitted as video artifacts** (GROUND RULES (c)): mouse cursor near the
  LayerNorm bar; black letterbox strip.
- **No equations** on this slide (plain-text labels only) → mathtext/OMML N/A.

## DB milestones (VIDEO=deep-learning/002_transformers_part2)

gen_status building → judging → **passed**; visual_check=PASS; visual_attempts=1;
visual_transcript=qa/slide038/judge_attempt_1.txt; pptx_path & build_script set;
prior crash last_error cleared.

## Evidence index (qa/slide038/)

`render_1.png`, `judge_prompt_1.txt`, `judge_attempt_1.txt`, `probe_1.txt`,
`build_attempt_1.js`, `build_attempt_1_component.js`,
`selfcheck_attempt_1.py`, `selfcheck_attempt_1_output.txt`,
`build_cropsheets.py`, `crops_text.png`, `crops_diagram.png`,
`cropcmp_text_1.txt`, `cropcmp_diagram_1.txt`.
Measurement scripts: `scratch/slide038/m1..m18` (m1_chrome, m2_content,
m3_defbox, m4_raw, m5_diagram, m6_solids, m7_crops, m8_hh [prior worker],
m9_bands, m10_disambig, m11_ascii, m12_sheets, m13_detail, m14_sheetC,
m15_container, m16_surgical, m17_final, m18_tails [this worker]).
Vision clarification transcripts: `scratch/slide038/vision_sheet{A,B,C}.txt`.

---

## VERIFICATION ADDENDUM — second dispatched worker (2026-10-12 03:41–03:50)

A second worker was dispatched for slide 038 end-to-end (retry context: "previous
builder died on provider timeout mid-measurement"). During its measurement phase a
concurrent worker completed and CERTIFIED this slide (judge PASS attempt 1, DB
gen_status=passed at 03:40). The second worker therefore did NOT rebuild or edit
anything (cascade law: never edit a certified component); it performed the
verification duties instead:

### Banking verification (slide 59 ← 38 obligation) — VERIFIED

- `components/slide_038.js` == `qa/slide038/build_attempt_1_component.js` (byte-identical);
  `build/slide_038.js` == `qa/slide038/build_attempt_1.js` (byte-identical).
- Component module loads standalone; exports `renderBase(pptx, slide, opts)` + `T`
  (22 measured-geometry keys); chrome via `shared_patterns/house_chrome.js`.
- Fresh rebuild FROM the certified component into
  `scratch/slide038/bankverify/verify_038.pptx` (certified deliverable untouched),
  rendered 150 dpi (`bankverify/verify-1.png`) and PIL-diffed against the certified
  `qa/slide038/render_1.png`: **0 of 2,251,125 pixels differ**. Banked component =>
  certified pixels, exact.
- `house_chrome_check.py` on the verify render: PASS (same chrome numbers).
- Judge transcript `judge_attempt_1.txt` read in full: coherent element-by-element
  comparison, 0 BLOCKER / 0 MAJOR / 4 MINOR, non-degenerate
  `FINAL VERDICT: PASS` line. DB row: gen_status=passed, visual_check=PASS,
  visual_attempts=1, visual_transcript=judge_attempt_1.txt. Certification chain REAL.

**Component path for slide 59's builder (REQUIRED import):**
`/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_038.js`
(`require` by absolute path; `renderBase(pptx, slide, {numeral: 59})` + the 59-delta;
opts.skip/only supported per the 001 slide_014 pattern.)

### Dissent for the record (NOT acted on — certified state stands)

The second worker's independent pixel analysis reached DIFFERENT readings on three
points; all evidence is banked under `scratch/slide038/` (m16 grids, m18_labels.py,
m20_final_probes.py outputs in shell history + scripts re-runnable). Recorded so a
future re-open (founder's call only) starts from both chains:

1. **Token label indexing**: this worker reads the labels as 0-BASED — Y_0..Y_5,
   dots, Y_{N-2}, Y_{N-1} (X row same) — vs the certified 1-based build.
   Evidence: sheetC 9x glyph reads (col1 sub "0", col2 sub "1", X-col2 "1"); label
   ink widths from the dark-red mask (col1 12px = wide oval sub, col2 7px = narrow
   sub — "0" is wider than "1"; col7 18px vs col8 12px); slide 036's build-zoom
   vision read (`qa/slide036/zoom_tail_labels.txt`: 6th token Y_5; tails "N-2/N-1,
   minus signs clearly visible, not N+1"); certified-convention slide 020's syms
   ["0".."5","N-2","N-1"]; and the col1/col2 glyph grids being pixel-identical
   between the 036 and 038 frames. Counter-evidence (certifying worker): transcript
   of record + raw agreement, border-contamination theory on the width reads, and
   the visual judge independently reading 1-based. The judge PASS governs.
2. **Token strip anatomy**: this worker measures FIVE pastel slots per strip
   [FAFDC3|F0FFDE|FFCCCC(label)|E9E5F5|F7DEF4], AAAAAA borders (m17/m20 raw spans;
   matches 036's censused anatomy) vs the certified 4 saturated cells
   [FFFF00][92D050][FF9999][D9D9D9]. The judge's MINOR #1 ("original tokens are
   smaller, paler... recreation tokens larger with more saturated fills") points in
   exactly this direction if that MINOR is ever promoted to a fix.
3. **Blues**: certified 039 (same video) measured the deck text-blue as ~000080 and
   the MHSA-block-family solid as 1A0EAE ((26,14,172) census here, matching 036's
   bannerBlue) vs the certified 0000CC/00008B used here. Styling-level; judge-passed.

No action taken on any of these: the slide is certified, the component is frozen
for slide 59, and reopening is founder-owned.
