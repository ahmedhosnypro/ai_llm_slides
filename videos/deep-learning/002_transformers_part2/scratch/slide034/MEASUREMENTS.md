# MEASUREMENTS.md — slide 034 "[2] Position Embedding" (002_transformers_part2, P2 #4)

Resume-worker index of `scratch/slide034/`. Written 2026-10-12 by the resume worker
after a provider storm killed the second worker (~52 min in; 27 files banked, no
MEASUREMENTS.md). This doc: file inventory, extracted constants, spec-vs-frame
discrepancies with pixel proof, and which P2 conventions transfer.

## 0. CORPUS STATE (verified read-only 2026-10-12 ~16:40)

**Slide 034 is COMPLETE — built, rendered, judged, and banked by earlier runs.**
Do NOT re-measure, re-build, or re-judge; everything below is the record.

- DB row (slides_progress.db, read-only query): `slide_id=34, pattern_group=P2,
  pattern_seq=4, gen_status=passed, visual_check=PASS, visual_attempts=1,
  validation_verdict=PASS_WITH_FIXES, recreatability_score=9`,
  `updated_at=2026-10-12T16:47:30` (fleet-wide touch; first passed 15:14).
- Deliverable: `recreated_pptx/slide_034_recreated.pptx` (14:48, single version, no suffix).
- Build: `recreated_pptx/build/slide_034.js` (byte-identical to banked
  `qa/slide034/build_attempt_1.js` per worker_report) + asset `build/assets/brace_034.png`.
- Judge: `qa/slide034/judge_attempt_1.txt` — **FINAL VERDICT: PASS**, 3 MINORs
  (arrow tone darker; brace curvature flatter; ellipsis dots greyer), no BLOCKER/MAJOR.
- Chain provenance: `qa/slide034/worker_report.md` (resume report, 15:31).
- **P2 [20,21,22,34] is COMPLETE**: DB rows 20/21/22/34 all `passed/PASS`
  (20: 2 attempts, 21: 1, 22: 2, 34: 1, all touched 16:47:30). The "22 building"
  note in the resume brief was stale. No successor member; no open obligations.

## 1. Ground truth / spec / build paths

- Ground truth frame: `videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg` (960x540)
- Spec: `videos/deep-learning/002_transformers_part2/analysis/slide_034_final.json`
  (PASS_WITH_FIXES, fixes list empty; `_meta`: kept_frame frame_02408.jpg, old_slide 69)
- Certified build script: `recreated_pptx/build/slide_034.js` (constants below are from it)
- QA evidence (BANKED, do not modify): `recreated_pptx/qa/slide034/`

## 2. Frame→slide mapping constants (THREE fits, all in family)

| Fit | ax | sx | sy | Used by |
|---|---|---|---|---|
| measure1 (certified) | 17.943 | 0.962307 | 0.955556 | build slide_034.js, selfcheck, gen_brace_png |
| pm1 (independent re-fit) | 17.891 | 0.962062 | 0.955556 | pm2–pm5 outputs |
| Deck family law (coordinator brief) | 17.628 | 0.961232 | 0.955556 | cross-check only |

- Law: `slide_x=(fx−ax)/sx`, `slide_y=fy/0.955556`. Landmarks (pm1): left 58.30,
  right 901.06, top 42.96, bottom 516.67 (measure1: 58.36/901.34/43.27/516.83).
- pm1 verification: top→44.95 (house 45.0), bottom→540.70 (house edge class); free-fit
  sy=0.957003 within 0.2% of family. Fits differ ≤1.3 slide-pt at frame right edge —
  sub-tolerance (tol 6.24 pt). The CERTIFIED build used measure1's fit.

## 3. Chrome / artifacts (pm1_chrome_output.txt)

- Frame strokes (frame px): left 58.3, right 901.06, top 42.96, bottom 516.67;
  bottom band rows 515–519 = stroke/letterbox blend; **letterbox solid black from row 518**
  (rows 519–539) → video-capture artifact, correctly omitted.
- Badge: yellow bbox x[859,892] y[57,85] center (875.5,71.0) → slide (891.4,74.3) vs
  house (893,71) — same 1–4px JPEG-bbox offset class as certified 020/021/022.
  Numeral ink h=10px; numeral = 34 = the printed frame number (house law).
- Purple-ring artifact around badge: 84 px, mean rgb (157,122,178) — compression
  artifact, not drawn.
- Gray cursor overlay near Vector_P3: 89 px, bbox x[390,469] y[290,329], mean rgb
  (152,160,170) → presenter cursor, omitted per GROUND RULES (c).

## 4. Element geometry (frame px; slide-pt via certified fit in build script)

All from pm2_structure_output.txt / pm4_rows_output.txt / pm5b_bar_arrows_output.txt /
measure10_output.txt. Render-vs-original selfcheck (28 regions, tol 6.24 pt): **ALL OK**
(`selfcheck_attempt_1_output.txt`).

- **Title** ink x[272,698] y[56,99]; red part x[273,478], blue part x[492,696].
  **Subtitle** x[272,695] y[95,124]. Title em 39.5, subtitle em 23.5 (build G).
- **Left labels** (frame): lab1 navy 3 lines y138–194 (x73–239, right-aligned toward diagram);
  lab3 red 2 lines y216–253 + navy paren y258–270.
- **Token lane (lane1)**: dash container x[166,887] y[136,175]; fill CCCCFC; dash 26266E;
  top dash x[172,880], bottom x[171,879]; vertical dash cols 166–173 and 881–887.
  **Token boxes** (8, edge pairs frame px): (180,239)(253,313)(327,386)(400,460)(474,533)
  (547,607)(735,799)(810,875); centers 209.3→843.0; boxes 1–6 linear fit center0=209.5
  **pitch=73.62**; digit ink h=16–17, ink centers within 0.7px of box centers;
  italic slant +2.4…+5.1px/16px (single digits, box7/8 ~+2.5 = "N-2"/"N-1" compound glyph).
- **Ellipsis dots** (5): centers x 638.7/656.8/674.9/693.1/708.2, y[152,161],
  w≈10 h≈10; pitch 18.1/18.1/18.2/15.1 (same 5-dot family grid as 020/021/022).
- **Purple bar**: bbox x[168,887] y[214,253] (slide w 747.4 h 40.8 pt); fill **#8E0095**
  (solid, row fill 1.0 in body rows). Words (yellow=Y / white=W, inkC frame px):
  Embedding Y x[311,433] c372 · Layer W x[450,494] c472 · to W x[506,520] c513 ·
  Learn Y x[530,594] c562 · Position W x[605,675] c640 · Vectors W x[685,750] c717.5.
  Yellow glyphs taller (h 21/17) than white (h 16/12).
- **Red down arrows** (pm5b): arrow1 shaft rows 176–208 w≈8 cx 525.6, head rows 209–214
  max w 13, bbox y[176,214]; arrow2 shaft rows 251–285 w≈7 cx 524.1, head rows 284–289
  max w 12, bbox y[251,289]; both cx→slide ≈527/526; shaft core **#D32C36**.
- **Vector lane (lane3)**: dash container x[166,887] y[290,329]; fill **FBDCFC**;
  dash **5F7382** (slate-teal); dash rows 290/328, vertical dash cols 166/886 only.
  **Vector boxes** (8 edge pairs): (178,238)(250,311)(326,385)(398,458)(474,532)(547,606)
  (733,797)(809,873); label ink x-offset +1.2…+2.5px right of box center; italic slant
  +2.7px; **vector-gap emptiness PROOF: dark px (sum<620) in x612..728 y296..324 = 0**.
- **Brace**: red bbox x[178,870] y[336,351] (slide w≈719 h≈15.7 pt); spine y342–344 full
  width with **cusp gap: y343 runs (208,492)+(555,840)**; cusp apex ≈(524.5,351) pointing
  DOWN; arm tips curl UP to y336. Drawn as raster PNG (`build/assets/brace_034.png`,
  600dpi, stroke 2.7pt, red 8A2436 — LO mis-renders rotated brace presets, 020 law).
- **Summary box**: green border x[222,826] y[360,505] (slide x 212.2–840.0, y 376.7–528.5);
  5 lines y[368,389]/[390,409]/[410,431]/[432,454]/[470,494]; **L5 bbox x[336,710] y[479,496]**;
  **N-1 highlight bbox x[435,489] y[410,433]** (drawn rect 431..492 cross-checked vs strict
  core 435..489: dx −4.0/+2.1, selfcheck note).

## 5. Palette constants (measured cores, pm3_palette_output.txt)

| Element | Measured core | Spec hex | Note |
|---|---|---|---|
| title red | #940D1A | #CC0000 | JPEG-dark class |
| title blue | #040076 | #0000CC | JPEG-dark class |
| subtitle red | #860B19 | #CC0000 | JPEG-dark class |
| lab1 navy | #120A61 | #0000CC | |
| lab2 red italic | #7B1824 | #CC0000 | maroon family |
| lane1 fill / dash | #B7B5EE / #1D1757 | (none) / #2244CC | drawn CCCCFC / 26266E |
| token box border / fill | #312B84 / #D2D0FE | #3366CC / #C9D6EF | |
| digit ink | #0D0470 | #000066 | |
| dots | #91A2CE | #8899BB | judge MINOR (greyer) |
| arrows | #AF0109/#AA0113, shaft core #D32C36 | #EE0000 | judge MINOR (darker) |
| bar fill | #8E0096 | #990099 | |
| bar yellow / white | #FFEA8F / #FFE8FF | #FFFF00 / #FFFFFF | |
| lane3 fill / dash | #FCDDFC / #5A6B73 | (none) / #00AA44 | |
| vec box border / fill | #A15562 / #F7ECFD | #CC0000 / #FFDDE4 | |
| vector label ink | #120561 (navy) | #CC0000 (red) | see §6.1 |
| brace red | #88232E | #CC0000 | drawn 8A2436 |
| summary border | #4D8A49 | #009900 | |
| summary black | #000000 | #000000 | |
| summary red lines | #7F101A | #CC0000 | maroon |
| highlight | #FFFF20 core, #EFF4A7 halo | #FFFF00 | judge MINOR (pale) |
| canvas | #FFFFFF; house bg #E8E8E8 | #E6E6E6 | house rule wins |

## 6. Spec-vs-frame discrepancies (PIXEL PROOF; frame wins — all recorded in build
header `slide_034.js` lines 24–41 and covered by judge GROUND RULES)

1. **Vector labels are NAVY, not red.** Spec: "red #CC0000 bold italic". Proof: pm3
   `vector label ink (box1 'Vector' zone)` core **#120561** (n=189); red px in ALL
   boxes total only 378 (core #742531 = the rose box borders + subscripts). Crop
   `crops/orig_vector_row.png` shows navy "Vector" + small red italic subscripts P0…PN-1.
   Drawn vecText 181070 (navy).
2. **Vector-lane dash is slate-teal, not green.** Spec: "dashed green #00AA44". Proof:
   pm3 lane3 band green-class bbox ABSENT (no green entry for lane3); dash core
   **#5A6B73**. Drawn 5F7382.
3. **Both lanes HAVE fills.** Spec: "no fill" containers. Proof: pm3 lane1 fill census
   n=352 core #B7B5EE / pm4 gap fill #C8C7F5 vs mid-lane #CCCBF7; lane3 fill census
   n=1920 core #FCDDFC. Drawn CCCCFC / FBDCFC.
4. **Summary line 4 is NOT underlined in the frame.** Spec: "underlined". Proof:
   resume-worker re-scan 2026-10-12 of y452–470 x224–824 dark-red mask: max contiguous
   run 11px at y452 (letter descenders), nothing beyond y453 — no underline stroke
   (matches measure9's max-run-20px finding recorded in the build header).
5. **Vector-row gap contains NO dots.** Spec: "[?] dots omitted or too faint". Proof:
   pm4 `vector-gap emptiness: dark px count=0` (x612..728, y296..324). Gap left empty;
   [?] resolved.
6. **JPEG-dark color class throughout** (title/subtitle/labels/summary-red/brace/arrows
   maroon vs spec CC0000/EE0000) — same class as certified 020/021/022; judge MINORs
   for arrow tone + pale highlight accepted.
7. **Token dash 26266E not 2244CC** (dash core #1D1757); **bar fill 8E0094 not 990099**.
8. **Artifacts correctly omitted** per judge GROUND RULES (b)/(c): bottom letterbox
   (rows 519–539, solid from 518), purple badge-ring compression halo, gray presenter
   cursor near Vector_P3 (x390–469 y290–329).
9. **House chrome overrides**: bg #E8E8E8 (not spec #E6E6E6); badge numeral 34 =
   printed frame number; title-box y=0.28 etc. — house rule wins over spec %s.

## 7. P2 conventions that transfer from certified members (from
`qa/slide034/p2_final_member_notes_034.js` + build header — group now COMPLETE)

- Shared chrome import `shared_patterns/house_chrome.js` (2 refs in each of
  slide_020/021/022/034.js); numeral per member = own frame number.
- Per-frame chrome-landmark mapping fit RE-MEASURED per member (ax family drift:
  020=18.628, 021=18.13, 022=17.753, 034=17.943) — never import another member's fit.
- Dashed row lanes (sysDash family + dash dashcontainers) in all four members.
- Raster-brace mechanism (LO mis-renders rotated leftBrace presets → generated 600dpi
  PNG embedded at w=px/600): brace_020/021/034.png in build/assets/.
- Closed-loop discipline: PIL band self-check vs original before judging (034: 28
  regions ALL OK, tol 6.24 pt) + dense-region crop comparisons (5 crops in
  qa/slide034/cropcheck_*.txt, all CROP VERDICT: MATCH) + judge through vision gate.
- JPEG-dark color class (8A2436-family instead of spec CC0000), 5-dot ellipsis grid,
  cap-pinned text, spec-vs-frame reconciliation records in build header.
- 034-specific deltas: TWO separate dashed lanes (no shared navy panel like 022) with
  a full-width purple bar between them; two block arrows (8A1620); raster brace sits
  UNDER the vector lane pointing at a green-outline summary box; NO +δ annotation band
  (020/021/022-only); NO Problems panel (022-only).

## 8. File index — scratch/slide034/ (nothing outside scratch was written by this run)

**Banked by earlier runs (DO NOT MODIFY):**
- `measure1_chrome.py`…`measure11_ascii.py` — first-pass measurement scripts
  (13:19–13:21). stdout-only; their console outputs died with the first storm.
  measure1 chrome landmarks+mapping; 2 bands; 3 color rows; 4 fine census; 5 geometry;
  6 box edges; 7 vecdump RGB strips; 8 core colors; 9 box edges via masks/text/arrows/
  brace/dots; 10 vector pink-fill edges, label lines, brace profile, slant, L5,
  highlight, bar word runs, text bands; 11 ASCII label maps.
- `pm1_chrome.py` + `pm1_chrome_output.txt` — independent chrome re-fit (ax 17.891).
- `pm2_structure.py` + output — global ink bands, per-element bboxes, color-class
  bboxes, lane dash rows, gap checks.
- `pm3_palette.py` + output — palette census per region (§5 table source).
- `pm4_rows.py` + output — token/vector rows: box edges, centers, digit ink, slant,
  dots, gap emptiness proof, dash extents.
- `pm5_bar_arrows.py` — bar words + arrows script. **BUG: line 75 `ig` should be
  `sub_g`; buffers all output to end, so the crash wrote no file. Left unmodified.**
- `gen_brace_png.py` — brace PNG generator (wrote build/assets/brace_034.png in the
  earlier run — out-of-scratch write by a PRIOR worker; banked evidence, not touched).
- `selfcheck_attempt_1.py` + `selfcheck_attempt_1_output.txt` — 28-region render-vs-
  original overlay check, ALL OK.
- `crops/` — 8 crop pairs (orig/rend token_row, vector_row, bar, summary) used for
  the 5 banked cropcheck transcripts.
- `render1/slide-1.png` (= copy of banked qa render_1.png, 161657 B) +
  `render1/slide_034_recreated.pdf` — render copies.
- `loprofile/` — LibreOffice profile from the 14:48 render.
- `ir_vision_gate_0.lock` — vision-gate lock remnant (empty; from the judge call).

**Added by THIS resume run (16:40):**
- `measure10_output.txt` — recovered stdout of measure10_final.py (§4 brace/label/L5/
  highlight/bar-run constants; underline-absent confirmation).
- `pm5b_bar_arrows.py` — fixed copy of pm5 (ig→sub_g, line 75 only; output renamed
  pm5b). Banked pm5 untouched.
- `pm5b_bar_arrows_output.txt` + `pm5b_stdout.txt` — §4 bar/arrow constants source.
- `MEASUREMENTS.md` — this file.

## 9. Related banked evidence OUTSIDE scratch (prior runs; read-only references)

`recreated_pptx/qa/slide034/`: build_attempt_1.js, judge_prompt_1.txt, probe_1.txt,
judge_attempt_1.txt (PASS + 3 MINORs), render_1.png + render_1_pre_fix.png,
cropcheck_token_row/cropcheck_vector_row/cropcheck2_vector_row/cropcheck_bar/
cropcheck2_summary.txt (all MATCH; MINOR tone notes: border green tone, maroon vs
crimson red, pale highlight, wider gap after "Learn"), p2_final_member_notes_034.js,
worker_report.md. Deliverables: `recreated_pptx/slide_034_recreated.pptx`,
`recreated_pptx/build/slide_034.js`, `recreated_pptx/build/assets/brace_034.png`.

## 10. Storm log

No provider errors were hit by this resume run — no sleeps required. Provider-storm
protocol (sleep 120s ×3) stood ready but unused.
