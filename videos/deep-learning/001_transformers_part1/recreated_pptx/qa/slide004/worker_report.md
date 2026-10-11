# Worker report — slide 004 "Processing Sequential Data" (001_transformers_part1)

Worker: per-slide build worker (slide 4 end-to-end). Date: 2026-10-11.
FINAL VERDICT: **PASS** (judge attempt 2, real comparison transcript).

## Deliverables

- PPTX (single-version law): `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_004_recreated.pptx`
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_004.js`
  (attempt 2 = current; imports the shared playlist chrome module
  `videos/deep-learning/shared_patterns/house_chrome.js` — `drawHouseChrome(pptx, s, {numeral: 4})`)
- DB row: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
  `visual_transcript=.../qa/slide004/judge_attempt_2.txt`

## Attempts

| K | What happened | Verdict |
|---|---|---|
| 1 | Built with per-deck measured chrome (pre-ratification of the playlist law: panel border core x39..920/y44..537, badge ellipse 0.59x0.49in FFFF99/9932CC, numeral 15pt black). Full pre-judge loop passed; full-slide judge comparison returned PASS (2 MINORs) — but the founder then ratified the PLAYLIST chrome law mid-flight. Superseded evidence kept banked (never deleted). | PASS (superseded chrome) |
| 2 | Chrome rebuilt exactly per `videos/deep-learning/AGENTS.md` + `shared_patterns/house_chrome.js` (white FFFFFF canvas; gray E9E9E7 panel x42..918px, y45px to slide bottom, red C00000 border, bottom stroke half-visible at slide edge; badge circle d36px at (893,71), FDFD96 fill, 6A5ACD ~2pt ring, bold 333333 numeral 18pt). Content unchanged. Re-ran the full pre-judge loop + judge. | **PASS** |

## Content geometry (PIL forensics on slide_004.jpg, 960x540, 1px=1pt; closed-loop verified on the 150dpi render)

- Title "Processing Sequential Data": bold 49pt C00000, centered (spec + house title box
  x0.6/w12.13). Ink target cap-top y200/desc y247; render measures 199.6..244.7. Three
  independent word-width checks pin em~49 (5.32em=259px etc.).
- Two-line blue topic list: bold 35.5pt #000099 (pixel core (0,0,152); the spec's #0F0FC8
  was the vision estimate — measurement wins per fidelity law), left ink x89, pinned
  `lineSpacing: 80` (= measured 80px pitch; render pitch 80.12). Verbatim lines incl. the
  three-space gap before "(1-D CNN)" (measured 35px) and two-space gap before "(RNN)"
  (measured 22px). Render bands y341.1..374.2 / y421.2..454.3 vs original 342..372 / 422..452;
  widths within 1.3%.
- Mouse-cursor artifact (~54% w, ~74% h): screen-recording overlay — NOT recreated (spec +
  judge ground rule c).
- No equations, no multi-line delimiters, no tables (self-check items 3/4/5 N/A).

## Pre-judge self-checks (all banked in qa/slide004/)

- `house_chrome_check.py` on render_2.png: **PASS** (panel x89..1913, y95-bottom; badge
  center (1860,148) d70 render px; tol 8).
- `selfcheck_attempt_2.py` / `.txt`: containment PASS (no ink outside the panel; badge
  border-gap 9.6px, no touch); wrap PASS (exactly 2 bands); lineSpacing pin PASS (pitch
  80.12 vs 80; `<a:spcPts val="8000"/>` present ×2).
- Dense-region crop comparisons (pattern law, full judge params, same region both sides,
  upscaled ×3/×6, measurements banked first):
  - body block: **PASS** (`judge_crop_body_2.txt`) — spacing/gaps consistent, no defects.
  - badge: **PASS** (`judge_crop_badge_2.txt`) — zero discrepancies; original's slightly
    wider oval / different hue covered by the ratified playlist chrome directive.

## Judge (attempt 2)

- Transcript: `qa/slide004/judge_attempt_2.txt` (coherent 48-line element-by-element body,
  ends `FINAL VERDICT: PASS for 'faithful, usable recreation'`).
- Findings: 2 MINORs — (1) body "10–12% smaller" — judge variance, REBUTTED by pixel
  measurement (ink widths within 1.3%; the transcript's own §5 measures "~0.8pp of frame
  height, barely perceptible, within tolerance"; the dedicated 3x body crop PASS agrees);
  (2) title optical center 1.4% right of original's — intentional: the spec (validated
  PASS_WITH_FIXES) and the house title box specify a horizontally centered title, the
  original's ink center sits 13px/960 left of true center. Neither is a fix trigger.
- Probe transcript: `probe_2.txt` (banked; window healthy pre-dispatch).
- NOTE: judge procedure executed by the worker via Bash per 17 §7 (no Agent/Task spawn
  tool available in this environment — orchestrator-approved fallback). Prompt banked
  VERBATIM pre-dispatch (`judge_prompt_2.txt`; the analyze_image.py path carries the
  correct `.agents/skills/` prefix — the template's path omitted `skills/`, all other
  text byte-identical).

## Evidence inventory (qa/slide004/)

render_1.png, render_2.png, build_attempt_1.js, build_attempt_2.js, judge_prompt_1.txt,
judge_prompt_2.txt, judge_template_frozen.txt, probe_1.txt, probe_2.txt,
judge_attempt_1.txt (superseded-chrome PASS), judge_attempt_2.txt (FINAL PASS),
judge_crop_body_1/2.txt, judge_crop_badge_1/2.txt, selfcheck_attempt_1.py/.txt,
selfcheck_attempt_2.py/.txt, crops/ (body + badge pairs from render_2).

## Dependency status

Slide 4 is a ROOT with NO dependents in `slide_dependencies.json` (no edges reference 4);
per 17 §2 no component export is required. Chrome is drawn via the playlist-shared
`shared_patterns/house_chrome.js` module, which is the single chrome source of truth for
the whole playlist.

## Spec deviations (documented, measurement-driven)

- Body color #000099 vs spec #0F0FC8 — pixel core measurement (0,0,152) over vision-model
  estimate; frame is ground truth.
- Title 49pt vs spec's "~40pt equivalent" estimate; body 35.5pt vs "~28pt estimate" —
  width-based em computation (two independent checks each) + closed-loop ink match.
- Badge numeral 18pt bold 333333 per the ratified playlist law (supersedes spec's 12pt
  black estimate and my attempt-1 16pt black).
