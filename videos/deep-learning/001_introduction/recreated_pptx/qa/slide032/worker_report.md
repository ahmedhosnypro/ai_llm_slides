# Worker report — slide 032, videos/deep-learning/001_introduction (RESUMED)

## Summary

- **Slide:** 032 "Where to Get Filters for Recognition" (Deep Learning DSAI 308, lecture 001_introduction)
- **Final verdict:** **PASS** (judge attempt 2, real comparison winner body with the mandated
  `FINAL VERDICT: PASS for 'faithful, usable recreation'` line)
- **Deliverable:** `videos/deep-learning/001_introduction/recreated_pptx/slide_032_recreated.pptx` (single-version)
- **Build script:** `videos/deep-learning/001_introduction/recreated_pptx/build/slide_032.js`
- **DB state:** `gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
  `visual_transcript=.../qa/slide032/judge_attempt_2.txt`
- **Resume note:** resumed from a crashed earlier worker that had banked 7 measurement
  files in `qa/slide032/` (measure_original{,2,3}.{py,out.txt}, solve_fonts.py). All
  banked measurements were re-verified with fresh PIL probes before use; solve_fonts.py
  had never been run — ran it and banked `solve_fonts_out.txt`. No renders/pptx/build
  script existed; build attempt numbering starts at 1 (renders render_1/2/3.png).

## Attempts

| # | Render | What happened |
|---|--------|----------------|
| build 1 | render_1.png | 25pt body (getbbox width-solve). house_chrome_check PASS. Self-check caught: L2 wrapped at the '2-D' hyphen (box too tight) and lines +6% wide |
| build 2 | render_2.png | Body 25→24pt (per-word glyph-ink sums: original L3 words sum 320px ink = 24pt exactly), box w 500→520, title +2px, label +1px. Bands still uniformly +2% wide (LO advance rendering) |
| build 3 | render_3.png | Body 24→23.5pt (LO-advance compensation). **All 6 body bands within ±1.1px of the original; title ±1px; label, boxes, plane, filter, arrow, words, bar all within tolerance (selfcheck_bands_attempt_3_out.txt: 0 hard failures)** |
| judge 1 | judge_attempt_1.txt | Coherent, favorable body ("every content element matches faithfully", IMG1 better) but NO mandated `FINAL VERDICT:` line → not certifiable evidence per verdict law → re-run |
| judge 2 | judge_attempt_2.txt | **FINAL VERDICT: PASS for 'faithful, usable recreation'.** Full element-by-element transcription match; all listed differences are the documented intentional ones (badge, full chrome border, substituted handwriting font, omitted cursor speck) |

Judge procedure executed by the worker (no Agent/Task spawn tool in this environment;
orchestrator-approved fallback), through `scripts/16_vision_gate.sh` with the frozen
template + this deck's chrome ground rules; `--thinking high --max-tokens 65536`.

## Pre-judge self-checks (all banked)

- `house_chrome_check.py` on render_3: **PASS** (panel, border, badge d70 @ (1860,148)).
- `selfcheck_bands_attempt_3.py` → `selfcheck_bands_attempt_3_out.txt`: **0 hard failures**
  (band-based per-line measurement, no neighbor bleed). Key numbers: body lines
  d(x0,x1,y0,y1) ≤ (1.6, 1.0, 1.2, 0.8)px; title (0.3, 0.0, 0.8, 1.0); plane (0.4, 0.1, 0.8, 0.6);
  filter (0.8, 0.2, 1.5, 1.2); words ≤ (0.8, 1.0, 1.5, 1.2).
- Crop comparison of the dense diagram region (2x, both images) through the gate:
  `prep_crop_compare.txt` — favored the recreation; only minor notes (arrowhead present
  in render vs none visible in original at 2x; handwriting letterform difference per ground rules).
- Earlier prep vision read of the original's diagram: `prep_diagram_read.txt`.
- Colors verified by modal probe: body 000080, reds C00000 (JPEG-darkened in original),
  plane AF6712, filter 0D99BB, left-box border 8E88AA.

## Measured facts & documented deviations (ink wins over spec)

1. **No red top rule** — spec claimed a thin red rule at the top edge; PIL found NO red
   rows y0..60. The playlist chrome's panel top border is the only top line (chrome law).
2. **Background** — spec's #E8E8E8 guess replaced by the chrome law (white canvas + E9E9E7 panel).
3. **Left box border** is blue-gray **8E88AA** (measured darkest modal), NOT the spec's #0000CC.
4. **Body = Arial Bold 23.5pt** (LO-advance-compensated; original renders as Arial Bold 24pt
   metrics: per-word glyph-ink sums match 24pt exactly; LO renders ~2% wide at 24pt —
   23.5pt matches the original's rendered line widths within ~2px). Line pitch 26pt
   explicit; paragraph gap 63pt (pitch + 37pt, implemented as separate per-line boxes at
   measured baselines 166/192/255/281/344/370 — the certified slide_005 pattern).
5. **L1 leading space** — original L1 ink starts 7px right of L2-L6 (x95 vs x88) = one
   24pt space; reproduced as a leading space for geometry fidelity.
6. **Title** = Arial Bold 35pt C00000, ink center 474.5 (5.5px LEFT of panel center — matched,
   not "corrected"), baseline 105, lineSpacing 40, per certified slide_005 conventions.
7. **Label '2-D Image'** = Arial Bold 24pt C00000, ink center 749.5, baseline 246.
8. **Diagram** = one 600dpi transparent PNG (plane parallelogram (774,315)(645,407)(645,495)(774,402)
   fill AF6712; filter (754,345)(728,362)(728,378)(754,361) fill 0D99BB; red two-segment
   arrow (787,443)→(774,401)→(746,370), C00000) placed at exact px/72 geometry —
   generator `build/assets/slide_032_make_assets.py`.
9. **Handwritten words** as PNGs at exact measured ink boxes ('Grayscale' 180x33 @(684,276)
   black; 'Filters' 66x16 @(777,441) red C00000). Original's wide marker font
   (Segoe-Print-like) is not installed and no network access (font downloads returned 0
   bytes); closest installed marker font Comic Sans MS, tight ink resized to the exact
   measured boxes. Letterform substitution documented in the judge view (ground rules).
10. **Pen icon** — the spec's "pen-nib icon" is a 3x4px dark speck at (627,315) in the
    original (6 dark px total, PIL) — video-capture artifact, intentionally omitted
    (ground rule c); noted in the judge view.
11. **Black bar** — original y519..539 x38..921; drawn y519 h18.5 (ends 537.5) so the
    chrome's half-visible bottom stroke stays visible for house_chrome_check.py (same
    documented deviation as certified slides 002/005).
12. **Chrome** — this lecture's original frames carry NO badge and only a left red panel
    border (PIL-probed; identical to certified slides 002/005's originals); the playlist
    law (founder directive 2026-10-11) mandates the shared template chrome + badge
    numeral 32 (file number; assumption PENDING FOUNDER VETO). drawHouseChrome imported,
    never re-drawn.

## Evidence inventory (qa/slide032/)

Banked from the previous run (kept): measure_original{,2,3}.{py,out.txt}, solve_fonts.py.
New: solve_fonts_out.txt, prep_diagram_read.txt, prep_crop_compare.txt, render_1/2/3.png,
build_attempt_1/2/3.js, selfcheck_attempt_1.py+_out.txt, selfcheck_attempt_2.py+_out.txt,
selfcheck_bands_attempt_3.py+_out.txt, judge_prompt_1.txt, probe_1.txt,
judge_attempt_1.txt, judge_attempt_2.txt, worker_report.md.
Build assets: `recreated_pptx/build/assets/slide_032_{make_assets.py,diagram.png,
word_grayscale.png,word_filters.png,assets_report.json}`.

Web-verification: honored — `slide_032_source/SOURCES.md` (CS231n, d2l.ai, LeCun 1998)
exists from the research fleet; content is the standard CNN locality rationale, no
conflicts; no figures needed from the web (the original frame is a hand-drawn schematic).

## Status

DONE — certified. No banking obligation (slide 32 has no dependents in
slide_dependencies.json: edges are 16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35).

---

## Verification addendum — post-certification verification worker (2026-10-12 ~07:25)

A second worker was dispatched to this slide while the certification worker above was
still live (collision detected: build_attempt_2.js/render_2.png/selfcheck_attempt_2.py
written 06:58-06:59 during the second worker's startup). Per the orchestrator's
collision protocol it stood down to READ-ONLY and performed independent verification
only. Findings:

1. **Certificate verified genuine.** `judge_attempt_2.txt` is a coherent, structured
   comparison winner body ending in the mandated
   `FINAL VERDICT: PASS for 'faithful, usable recreation'.` The banked
   `judge_prompt_1.txt` carries the frozen `-p` template verbatim (GROUND RULES prelude,
   FINAL VERDICT line) with `--thinking high --max-tokens 65536`; it targets
   `render_3.png`. `diff build/slide_032.js qa/slide032/build_attempt_3.js` = clean, and
   `slide_032_recreated.pptx` (07:04:33) is the pptx that produced the judged render
   (render_3.png 07:04:35). The certificate binds to the judged artifact — intact.
2. **house_chrome_check.py re-run by the verifier on BOTH render_1.png and the judged
   render_3.png: PASS** (panel x 89-1913, y 95-bottom; badge center (1860,148) d=70;
   tol 8).
3. **Independent PIL corroboration (verifier probe of render_1, `probe_render1.py`):**
   title ink 173.7..771.0 x / 80.6..112.7 y vs original (176, 773, 80, 112) — within
   ~2.3px; label, left/right box borders, filter, arrow, 'Grayscale', 'Filters', black
   bar all within tolerance. The selfcheck_attempt_1 "7 hard failures" were shown to be
   check-band artifacts (adjacent-line band bleed; red antialiasing of the arrow/word
   caught by the brown-plane detector — samples RGB (171,58,56) etc.), consistent with
   the certification worker's later band-based checker reporting 0 hard failures on
   render_3.
4. **Provenance caveat (no impact on the certificate):** the verifier's early
   `cp build/slide_032.js qa/slide032/build_attempt_1.js` (06:54) landed WHILE the
   certification worker was mid-edit, so `build_attempt_1.js` captured an intermediate
   (23.5pt) state rather than the exact 25pt script that produced `render_1.png`. No
   peer artifact was overwritten (the file did not exist before the copy). The judged
   chain (build_attempt_3.js ↔ render_3.png ↔ slide_032_recreated.pptx ↔
   judge_attempt_2.txt) is fully self-consistent. `probe_render1.py` is the verifier's
   read-only probe script (additive).
5. **Banking check re-verified:** slide 32 appears in no `slide_dependencies.json` edge
   (16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35) — not a parent, not a child; no
   component bank required.
6. **DB row verified current** (read + confirmed 07:23): gen_status=passed,
   visual_check=PASS, visual_attempts=2,
   visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide032/judge_attempt_2.txt,
   pptx_path and build_script set. No DB writes were made by the verifier (the
   certification worker had already completed all milestone updates).

Verdict: certification STANDS.
