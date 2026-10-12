# CERTIFICATE AUDIT — videos/deep-learning/001_introduction/, slides 1–49 (certified set)

Auditor: read-only certificate audit (additive addenda only). Date: 2026-10-12.
Rules honored: zero writes outside scratch/audit_001i/; no DB writes; no fixes; no banked evidence touched.
(Note: prior attempt scratch/audit_001t1/ audited the OTHER deck 001_transformers_part1 — different audit, not appended here.)

## Certified set (check 1 — DB terminal status, sqlite3 -readonly)

Slides 1–49 with gen_status=passed AND visual_check=PASS: **47 slides** = {1–24, 26–49}.
- Skipped as mid-flight (gen_status=building, visual_check empty): **25, 45**.
- Task's example skip-list "24/41/45" was from an earlier snapshot; the DB (source of truth)
  now shows 24 and 41 terminal PASS — they are audited. 45 remains mid-flight (its pptx exists
  on disk but is NOT certified — excluded).
- Row 50 (pending/blocked): known stale artifact per audit brief — slide 50 does not exist;
  quarantined in analysis_strays/. Ignored (confirmed: no slide_050 in unique_slides or recreated_pptx).

## Existence / single-variant checks (checks 3, 4)

- Deliverables: recreated_pptx/slide_NNN_recreated.pptx present for ALL 47 certified N (only
  025 absent — mid-flight). 48 pptx total in recreated_pptx/ (1–49 minus 25).
- Single variant: NO _graphed/_omml/_v2/_new/_final/copy variants anywhere in recreated_pptx/. PASS.
- Build scripts: recreated_pptx/build/slide_NNN.js present for ALL 47 certified N (only 025 absent). PASS.

## Transcript checks (check 2)

- All 47 DB-bound visual_transcript files exist with genuine coherent judge bodies
  (sizes 2,403–5,244 bytes), each ending in a FINAL VERDICT: PASS.
- Verification addenda from stood-down duplicate workers present on several slides — expected per brief.
- Special cases per brief, verified genuine:
  - S6 (qa/slide006/judge_attempt_1.txt): double-judged certificate; ground rules cite badge "6". PASS.
  - S29 (qa/slide029/judge_attempt_1.txt): ground-ruled certificate; badge "29" cited. PASS.
  - S40 (qa/slide040/judge_attempt_2.txt): banked-evidence certificate; badge "40" cited. PASS.
- ANOMALY (minor, path-format): slide 18's DB visual_transcript is stored as deck-relative
  "judge_attempt_1.txt" (all other rows store project-root-relative paths). File EXISTS at
  videos/deep-learning/001_introduction/recreated_pptx/qa/slide018/judge_attempt_1.txt
  (3,887 B, FINAL VERDICT: PASS). DB row's pptx_path/build_script are also deck-relative for 18.
  Non-blocking: certificate intact, only the row's path convention differs.

## Dep-parent components (check 7)

recreated_pptx/build/components/ contains: house_chrome.js, slide_001.js, slide_009.js,
slide_016.js, slide_024.js, slide_035.js, slide_036.js. Dep parents among certified: 9, 16 — both
present. PASS.

## Chrome + badge law (checks 5, 6 — on renders of the CURRENT certified deliverable)

Method: each of the 47 certified pptx was rendered by LibreOffice headless (profile confined to
scratch/audit_001i/lo_profile/) → PDF → pdftoppm 150dpi PNG (2000x1125), then
videos/deep-learning/shared_patterns/house_chrome_check.py run on that render, plus badge-numeral
OCR (tesseract, digit whitelist; validated psm 7/10 modes + visual confirmation where ambiguous).
Raw output: scratch/audit_001i/chrome_badge_results.txt; renders in scratch/audit_001i/renders/.

- House chrome check: **PASS on ALL 47 renders** (panel extent, red border, badge disc+ring, tol 8).
- Badge law (numeral == file number N, no zero-padding): **PASS on ALL 47.**
  - OCR psm 7/10 matched N on 45/47 directly; S4 and S6 were OCR-ambiguous (tiny-glyph noise) and
    were confirmed VISUALLY from the badge crops: S4 badge reads "4", S6 badge reads "6".
  - psm 6 readings ('0\nNN1'-style) are ring-fragment artifacts of the circle outline — methodology
    noise, not deck defects.
- Build-script wiring cross-check: every build draws chrome via the shared module — direct
  `house_chrome` import (slides 1–15, 18, 20–35, 38–40, 42–49 builds) or via certified components
  (16→components/slide_016.js→9; 17/19→components/slide_009.js; 36→components/slide_036.js;
  37/41→parents 36/35; components/house_chrome.js re-exports shared_patterns/house_chrome.js).
  Numeral args confirmed as file numbers (e.g. slide_004.js `numeral = 4`, slide_049.js
  `numeral = 49`, slide_016.js `numeral: "16"`). "Import, never re-draw" law honored.

## Per-slide results (one line each)

Format: S<n> | DB terminal | transcript | pptx | build | chrome | badge. All 47 PASS-CHAIN.

- S1 | passed/PASS | qa/slide001/judge_attempt_3.txt, FINAL VERDICT PASS | single variant | yes | PASS | "1"=1 PASS
- S2 | passed/PASS | qa/slide002/judge_attempt_2.txt, PASS | single | yes | PASS | "2"=2 PASS
- S3 | passed/PASS | qa/slide003/judge_attempt_4.txt, PASS | single | yes | PASS | "3"=3 PASS
- S4 | passed/PASS | qa/slide004/judge_attempt_1.txt, PASS | single | yes | PASS | "4"=4 PASS (visual-confirmed)
- S5 | passed/PASS | qa/slide005/judge_attempt_2.txt, PASS | single | yes | PASS | "5"=5 PASS
- S6 | passed/PASS | qa/slide006/judge_attempt_1.txt, PASS (double-judged certificate) | single | yes | PASS | "6"=6 PASS (visual-confirmed)
- S7 | passed/PASS | qa/slide007/judge_attempt_1.txt, PASS | single | yes | PASS | "7"=7 PASS
- S8 | passed/PASS | qa/slide008/judge_attempt_5.txt, PASS | single | yes | PASS | "8"=8 PASS
- S9 | passed/PASS | qa/slide009/judge_attempt_1.txt, PASS | single | yes | PASS | "9"=9 PASS | dep-parent component present
- S10 | passed/PASS | qa/slide010/judge_attempt_2.txt, PASS | single | yes | PASS | "10"=10 PASS
- S11 | passed/PASS | qa/slide011/judge_attempt_1.txt, PASS | single | yes | PASS | "11"=11 PASS
- S12 | passed/PASS | qa/slide012/judge_attempt_1.txt, PASS | single | yes | PASS | "12"=12 PASS
- S13 | passed/PASS | qa/slide013/judge_attempt_1.txt, PASS | single | yes | PASS | "13"=13 PASS
- S14 | passed/PASS | qa/slide014/judge_attempt_1.txt, PASS | single | yes | PASS | "14"=14 PASS
- S15 | passed/PASS | qa/slide015/judge_attempt_1.txt, PASS | single | yes | PASS | "15"=15 PASS
- S16 | passed/PASS | qa/slide016/judge_attempt_1.txt, PASS | single | yes | PASS | "16"=16 PASS | dep-parent component present
- S17 | passed/PASS | qa/slide017/judge_attempt_1.txt, PASS | single | yes | PASS | "17"=17 PASS
- S18 | passed/PASS | qa/slide018/judge_attempt_1.txt (DB path deck-relative — see anomaly A-1), PASS | single | yes | PASS | "18"=18 PASS
- S19 | passed/PASS | qa/slide019/judge_attempt_8.txt, PASS | single | yes | PASS | "19"=19 PASS
- S20 | passed/PASS | qa/slide020/judge_attempt_1.txt, PASS | single | yes | PASS | "20"=20 PASS
- S21 | passed/PASS | qa/slide021/judge_attempt_1.txt, PASS | single | yes | PASS | "21"=21 PASS
- S22 | passed/PASS | qa/slide022/judge_attempt_2.txt, PASS | single | yes | PASS | "22"=22 PASS
- S23 | passed/PASS | qa/slide023/judge_attempt_1.txt, PASS | single | yes | PASS | "23"=23 PASS
- S24 | passed/PASS | qa/slide024/judge_attempt_1.txt, PASS | single | yes | PASS | "24"=24 PASS
- S26 | passed/PASS | qa/slide026/judge_attempt_1.txt, PASS | single | yes | PASS | "26"=26 PASS
- S27 | passed/PASS | qa/slide027/judge_attempt_1.txt, PASS | single | yes | PASS | "27"=27 PASS
- S28 | passed/PASS | qa/slide028/judge_attempt_1.txt, PASS | single | yes | PASS | "28"=28 PASS
- S29 | passed/PASS | qa/slide029/judge_attempt_1.txt, PASS (ground-ruled certificate) | single | yes | PASS | "29"=29 PASS
- S30 | passed/PASS | qa/slide030/judge_attempt_1.txt, PASS | single | yes | PASS | "30"=30 PASS
- S31 | passed/PASS | qa/slide031/judge_attempt_2.txt, PASS | single | yes | PASS | "31"=31 PASS
- S32 | passed/PASS | qa/slide032/judge_attempt_2.txt, PASS | single | yes | PASS | "32"=32 PASS
- S33 | passed/PASS | qa/slide033/judge_attempt_3.txt, PASS | single | yes | PASS | "33"=33 PASS
- S34 | passed/PASS | qa/slide034/judge_attempt_2.txt, PASS | single | yes | PASS | "34"=34 PASS
- S35 | passed/PASS | qa/slide035/judge_attempt_1.txt, PASS | single | yes | PASS | "35"=35 PASS
- S36 | passed/PASS | qa/slide036/judge_attempt_1.txt, PASS | single | yes | PASS | "36"=36 PASS
- S37 | passed/PASS | qa/slide037/judge_attempt_2.txt, PASS | single | yes | PASS | "37"=37 PASS
- S38 | passed/PASS | qa/slide038/judge_attempt_2.txt, PASS | single | yes | PASS | "38"=38 PASS
- S39 | passed/PASS | qa/slide039/judge_attempt_1.txt, PASS | single | yes | PASS | "39"=39 PASS
- S40 | passed/PASS | qa/slide040/judge_attempt_2.txt, PASS (banked-evidence certificate) | single | yes | PASS | "40"=40 PASS
- S41 | passed/PASS | qa/slide041/judge_attempt_3.txt, PASS | single | yes | PASS | "41"=41 PASS
- S42 | passed/PASS | qa/slide042/judge_attempt_4.txt, PASS | single | yes | PASS | "42"=42 PASS
- S43 | passed/PASS | qa/slide043/judge_attempt_1.txt, PASS | single | yes | PASS | "43"=43 PASS
- S44 | passed/PASS | qa/slide044/judge_attempt_1.txt, PASS | single | yes | PASS | "44"=44 PASS
- S46 | passed/PASS | qa/slide046/judge_attempt_1.txt, PASS | single | yes | PASS | "46"=46 PASS
- S47 | passed/PASS | qa/slide047/judge_attempt_1.txt, PASS | single | yes | PASS | "47"=47 PASS
- S48 | passed/PASS | qa/slide048/judge_attempt_4.txt, PASS | single | yes | PASS | "48"=48 PASS
- S49 | passed/PASS | qa/slide049/judge_attempt_1.txt, PASS | single | yes | PASS | "49"=49 PASS

## Anomalies by severity

**BLOCKER: none.**

- A-1 (MINOR, metadata only): slide 18's DB row stores deck-relative paths — visual_transcript
  "judge_attempt_1.txt", pptx_path/build_script "recreated_pptx/..." — while all 46 other rows use
  project-root-relative paths. All three files EXIST (transcript verified: 3,887 B, FINAL VERDICT
  PASS). Certificate intact; recommend (do-not-fix by auditor) normalizing the row's path convention
  to the project-root-relative standard.
- A-2 (NOTE, not a defect): slide 45's deliverable slide_045_recreated.pptx already exists on disk
  while its DB row is mid-flight (gen_status=building, visual_check empty). It was excluded from this
  audit as non-certified; flagged so nobody mistakes the file for a certificate.
- A-3 (NOTE, methodology): badge-OCR psm 6 is unreliable on the badge circle (ring read as digit 0);
  audit verdicts rest on psm 7/10 agreement plus visual confirmation of the two ambiguous crops
  (S4, S6). No deck change implied.

## Stale-row confirmation (check 8)

Row 50 confirmed stale as briefed: no slide_050 deliverable, no unique_slides/slide_050; only
analysis_strays/slide_050_raw.json and slide_050_final.json in quarantine. Ignored.

## Evidence in this audit dir (scratch/audit_001i/)

audit_report.md (this file), chrome_badge_results.txt (raw per-slide checker+OCR output),
renders/ (47 deliverable PDFs + 150dpi PNGs), badge_s001.png, badge_s004_inspect.png,
badge_s006_inspect.png, run_chrome_badge.py (driver), lo_profile/ (confined LO profile).

**Audited: 47/47 certified slides. Result: ALL PASS-CHAIN. Zero BLOCKERs. 1 minor anomaly (A-1), 2 notes (A-2, A-3).**
