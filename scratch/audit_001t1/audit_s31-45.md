# CERTIFICATE AUDIT — slides 31–45, videos/deep-learning/001_transformers_part1/

Auditor: read-only certificate audit (additive addenda only). Date: 2026-10-12.
Rules honored: zero writes outside scratch/audit_001t1/; no DB writes; no fixes; no banked evidence touched.

## DB terminal status (check 1) — verified 2026-10-12 via sqlite3 -readonly

All 15 rows (slide_id 31–45): gen_status=passed AND visual_check=PASS. PASS for all 15.

Binding transcripts named in DB:
- 31 qa/slide031/judge_attempt_3.txt
- 32 qa/slide032/judge_attempt_5.txt  (double-judged/reconciled — worker_report.md to be cross-checked)
- 33 qa/slide033/judge_attempt_3.txt
- 34 qa/slide034/judge_attempt_3.txt
- 35 qa/slide035/judge_attempt_2.txt
- 36 qa/slide036/judge_attempt_2.txt
- 37 qa/slide037/judge_attempt_1.txt
- 38 qa/slide038/judge_attempt_1.txt
- 39 qa/slide039/judge_attempt_2.txt
- 40 qa/slide040/judge_attempt_1.txt
- 41 qa/slide041/judge_attempt_3.txt
- 42 qa/slide042/judge_attempt_2.txt  (double-judged/reconciled — worker_report.md to be cross-checked)
- 43 qa/slide043/judge_attempt_2.txt
- 44 qa/slide044/judge_attempt_2.txt
- 45 qa/slide045/judge_attempt_2.txt

depends_on: 35→34, 38→37, 44→43, 45→43 (matches audit task edges). Others empty.

Components present in recreated_pptx/build/components/: house_chrome.js, slide_006, 013, 014, 015, 017, 018, 019, 026, 029, 033, 034, 037, 043 — dep parents 34, 37, 43 all present (check 7, minimum met).

## Certified render per slide (named by the BINDING judge prompt in the DB)

31→render_4, 32→render_5, 33→render_3, 34→render_1 (prompt_3 header says "attempt 1"
but names render_1.png, the dir's only render; path is what binds), 35→render_1
(banked-verbatim header format, COMMAND line names render_1.png), 36→render_7,
37→render_1, 38→render_1, 39→render_2, 40→render_1, 41→render_3, 42→render_2,
43→render_2, 44→render_2, 45→render_2. All 15 files exist on disk.

## Check 5 — house_chrome_check.py on certified renders (run 2026-10-12)

- 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45: exit 0, "HOUSE CHROME CHECK:
  PASS (panel x 89-1913, y 95-bottom; badge center (1860,148) d=70; all within tol 8)".
- 44: exit 1, FAIL "badge center (1860,140) vs (1860,148) (tol 8)". DOCUMENTED: slide044
  worker_report.md records this exact FAIL as the Figure-2-right inset panel occluding the
  badge's bottom-left arc — faithful to the ORIGINAL frame. INDEPENDENTLY VERIFIED by this
  audit (PIL yellow-extent, frame-px): render_2 badge y 54.7..80.1 vs ORIGINAL slide_044.jpg
  y 57.0..80.0 (both cut at ~80); unoccluded parent slide_043 render y 54.7..87.8 vs its
  original y 57.0..86.0. The original frame's own badge is identically cut, so the render
  matches ground truth; the mechanical gate just has no occlusion allowance. Other chrome
  checks (panel, red strokes, purple ring) PASS on 44. Classified: benign/documented, NOT
  a fidelity defect.

## Check 3 — deliverable sole-variant (find over recreated_pptx, 2026-10-12)

Exactly 45 pptx files, all plain `slide_NNN_recreated.pptx`; 31–45 all present; ZERO
variant-suffix files anywhere under recreated_pptx/. PASS for all 15.

## Check 4 — build scripts

build/slide_031.js … build/slide_045.js all present (plus non-deliverable helpers
slide_042_postpass.py, slide_045_base_probe.js — not pptx variants, no conflict).

## Check 7 — dep-parent components

components/ contains slide_034.js, slide_037.js, slide_043.js (+ house_chrome.js and
earlier parents). Edges 35←34, 38←37, 44←43, 45←43 all covered by banked components.
slide044 worker_report.md confirms 44 requires components/slide_043.js with
`opts.skip:["title"]` (title re-drawn at child-measured position, x=491 vs parent 500).

## Check 6 — badge numeral = printed number on original frame

Banked qa evidence per slide (binding transcript badge mentions unless noted):
31 'Badge "31" present' · 32 'badge "32"' · 34 '"34" — present and matching in both' ·
35 'yellow "35" badge' · 36 'yellow "36" oval badge' · 37 'yellow "37" oval badge' ·
38 'yellow "38" oval badge' · 39 'yellow "39" badge' · 40 'yellow "40" badge with purple
ring' · 41 'yellow "41" badge' · 42 'yellow "42" badge' + 'Slide number 42 in yellow oval' ·
43 'Badge "43" present' · 44 '44 badge right' + 'Occlusion 2 — 44-badge bottom-left arc' ·
45 '"45" oval badge'.
- 33 (no numeral in its transcript): banked in slide033/worker_report.md ("chrome check …
  badge numeral 33") + probe_3.txt ("the '33' oval badge at top-right"), PLUS an independent
  crop-read by this auditor (crops banked in scratch/audit_001t1/s033_orig_badge_crop.png and
  s033_render_badge_crop.png): original unique_slides/slide_033.jpg badge prints "33"; the
  certified render_3.png badge prints "33". MATCH. PASS for all 15.

## Check 2 — binding transcript coherence (skimmed 2026-10-12)

All 15 DB-named transcripts exist and are genuine coherent comparison winner bodies:
ground-rules disposition up front, element-by-element content (tables/regions/colors/
geometry), explicit discrepancy/quality sections, and a final "FINAL VERDICT: PASS for
'faithful, usable recreation'" line. Minor-only findings in all 15 (no BLOCKER/MAJOR in any
winner body). Special certificates in scope verified:
- 32 (reconciled race): worker_report.md documents a two-worker race on the same takeover
  path; BOTH bodies were genuine coherent comparisons of the same render vs the same
  original from the same frozen prompt and BOTH returned FINAL VERDICT: PASS (no
  BLOCKER/MAJOR); certification stands on the on-disk judge_attempt_5.txt (the DB-named
  file, verified genuine by this auditor). Race participant also re-verified the on-disk
  deliverable renders pixel-identical to the judged render_5.png (md5 chain) and passes
  house_chrome_check. BINDING TRANSCRIPT = DB-named judge_attempt_5.txt. VERIFIED.
- 42 (double-judged / collision-verified): worker_report.md + an independent read-only
  verifier session's addendum confirm judge_attempt_2.txt is a genuine coherent winner
  body (3× MINOR only, PASS), chrome check PASS, single-version deliverable, DB terminal.
  BINDING TRANSCRIPT = judge_attempt_2.txt. VERIFIED.

## Per-slide results (all 7 checks)

- **31 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_3.txt coherent PASS (badge "31"); sole pptx (218,577 B, zip OK); build/slide_031.js; chrome PASS on render_4.png; badge 31 banked; no deps.
- **32 PASS-CHAIN** — DB terminal passed/PASS; binding judge_attempt_5.txt coherent PASS (badge "32"), reconciled-race certificate verified (both race bodies PASS); sole pptx (140,801 B, zip OK); build/slide_032.js; chrome PASS on render_5.png; badge 32 banked; no deps.
- **33 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_3.txt coherent PASS; sole pptx (193,140 B, zip OK); build/slide_033.js; chrome PASS on render_3.png; badge crop-read orig "33" = render "33" (+ banked worker_report "badge numeral 33"); no deps.
- **34 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_3.txt coherent PASS (badge "34" matching in both); sole pptx (212,650 B, zip OK); build/slide_034.js; chrome PASS on render_1.png (the only render, named by binding prompt_3 — stale "attempt 1" header label, path binds); badge 34 banked; dep parent with components/slide_034.js banked.
- **35 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_2.txt coherent PASS (badge "35"; inherited-parent clause documented); sole pptx (216,902 B, zip OK); build/slide_035.js; chrome PASS on render_1.png; badge 35 banked; dep 35←34 satisfied (component 34 banked).
- **36 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_2.txt coherent PASS (badge "36"); sole pptx (378,531 B, zip OK); build/slide_036.js; chrome PASS on render_7.png; badge 36 banked; no deps.
- **37 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_1.txt coherent PASS (badge "37"); sole pptx (216,249 B, zip OK); build/slide_037.js; chrome PASS on render_1.png; badge 37 banked; dep parent with components/slide_037.js banked.
- **38 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_1.txt coherent PASS (badge "38"; declared expected Scaling-box position difference); sole pptx (228,871 B, zip OK); build/slide_038.js; chrome PASS on render_1.png; badge 38 banked; dep 38←37 satisfied (component 37 banked).
- **39 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_2.txt coherent PASS (badge "39"; 3× MINOR); sole pptx (542,957 B, zip OK); build/slide_039.js; chrome PASS on render_2.png; badge 39 banked; no deps.
- **40 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_1.txt coherent PASS (badge "40" with purple ring; section-divider contentlessness matched per rule b); sole pptx (48,438 B, zip OK); build/slide_040.js; chrome PASS on render_1.png; badge 40 banked; no deps.
- **41 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_3.txt coherent PASS (badge "41"; 3× MINOR); sole pptx (145,272 B, zip OK); build/slide_041.js; chrome PASS on render_3.png; badge 41 banked; no deps.
- **42 PASS-CHAIN** — DB terminal passed/PASS; binding judge_attempt_2.txt coherent PASS (badge "42"), double-judged/collision-verified certificate verified incl. independent read-only verifier addendum; sole pptx (61,251 B, zip OK); build/slide_042.js (+postpass); chrome PASS on render_2.png; badge 42 banked; no deps.
- **43 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_2.txt coherent PASS (badge "43"; 4× MINOR); sole pptx (357,689 B, zip OK); build/slide_043.js; chrome PASS on render_2.png; badge 43 banked; dep parent with components/slide_043.js banked.
- **44 ANOMALY (documented, benign — see below)** — DB terminal passed/PASS; judge_attempt_2.txt coherent PASS (badge "44"; "no fix-trigger defects … occlusions reproduce the original exactly"); sole pptx (379,410 B, zip OK); build/slide_044.js; **check 5 house_chrome_check exit 1 on certified render_2.png** — badge center (1860,140) vs (1860,148), tol 8; worker_report.md documents this exact FAIL as the inset's faithful occlusion of the badge arc, and this auditor INDEPENDENTLY VERIFIED via PIL yellow-extent (render y 54.7..80.1 frame-px vs ORIGINAL y 57.0..80.0, both cut at ~80; unoccluded parent 43 runs to ~86–88): the original frame's own badge is identically cut, so the render matches ground truth; the mechanical gate has no occlusion allowance; all other chrome checks PASS on 44; badge 44 banked; dep 44←43 satisfied (component 43 banked, 44 renders base via require with skip:["title"]).
- **45 PASS-CHAIN** — DB terminal passed/PASS; judge_attempt_2.txt coherent PASS (badge "45"; no BLOCKER/MAJOR); sole pptx (445,728 B, zip OK); build/slide_045.js; chrome PASS on render_2.png; badge 45 banked; dep 45←43 satisfied (component 43 banked).

## Anomalies by severity

### BLOCKER-class
**NONE.** No broken terminal states, no missing/incoherent transcripts, no missing or
variant-suffixed deliverables, no missing build scripts, no fidelity defect found by this
audit, no missing dep-parent components.

### Cosmetic / documentation-level (2)
1. **Slide 44 — mechanical chrome-gate FAIL on the certified render** (check 5 exit 1:
   badge center y 140 vs canonical 148, tol 8 render-px). Verified benign: the green
   Figure-2-right inset faithfully occludes the badge's bottom-left arc exactly as the
   ORIGINAL frame does (independent PIL measurement by this auditor: render yellow
   y-extent 54.7..80.1 frame-px vs original 57.0..80.0; parent slide 43 unoccluded to
   ~86–88). The gate tool has no occlusion allowance; the worker documented and
   justified the FAIL at build time (worker_report.md "Chrome check" section,
   scratch/slide044/s1_chrome_occl.py). Not a fidelity defect — the render matches the
   original. No action required; recorded so future re-runs of the bare gate on
   qa/slide044/render_2.png are not mistaken for a regression.
2. **Slide 34 — stale header label in the binding prompt**: qa/slide034/judge_prompt_3.txt
   line 5 reads "Render being judged (attempt 1)" though it is prompt 3 for judge attempt 3.
   The named path render_1.png is the directory's only render and is the artifact the
   attempt-3 judge compared; certification unaffected. Documentation nit only.

### Observations (not anomalies)
- Slide 32's on-disk judge_attempt_5.txt is the race-monitor's winner body; the peer
  builder's body (same verdict PASS) was overwritten at 08:04:32 and survives only as
  quoted content in worker_report.md. The reconciliation section documents the race
  explicitly; the DB-named binding transcript is the on-disk file and is genuine. Chain
  (build → render md5 → deliverable re-verified pixel-identical) is banked.
- Slide 42's judge was self-executed by the worker via the documented §7 fallback (no
  spawn tool in that environment) — same pattern in several other slides' reports; the
  transcripts carry the full gated-invocation provenance.
- Deliverable zip integrity verified for all 15 (all non-empty, zip OK).

## Audit closure

- Slides audited: 45 slides' worth of checks applied to slide_id 31–45 (15/15).
- Result: 14/15 clean PASS-CHAIN; 1 benign documented ANOMALY (slide 44, cosmetic);
  0 BLOCKER-class.
- Audit artifacts written by this auditor (all inside scratch/audit_001t1/):
  this file, s033_orig_badge_crop.png, s033_render_badge_crop.png. No other writes;
  no DB writes; no banked evidence touched.
