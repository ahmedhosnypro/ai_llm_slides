# Worker report — slide 010 "Pre processing" (deep-learning/001_introduction)

## Verdict chain

| Attempt | Build | Pre-judge checks | Judge | Verdict |
|---|---|---|---|---|
| 1 | `build_attempt_1.js` (chrome import + PIL-measured content, charSpacing/baseline-calibrated) | house_chrome_check PASS; selfcheck attempt 1 → geometry PASS after scan-bug fixes; containment 0 stray px | `judge_attempt_1.txt` | **FAIL** — (1) MAJOR: "Problem dependent and data dependent" missing italic + underline; (2) MAJOR: bullet line spacing "looser"; (3) MAJOR/borderline-BLOCKER: final "......." bullet "touches/crosses" the content-box bottom border |
| 2 | `build_attempt_2.js` — phrase italic + underlined (split runs so " is " stays regular); ellipsis baseline 503→501.7 | house_chrome_check PASS; selfcheck attempt 2 → **PASS** (underline 3 continuous rows y154.5-155.4 spanning 375 frame px = exactly the phrase; italic P-stem slant 2.9 frame px ≈ 12°; ellipsis baseline 501.8 vs 501.7; all baselines/extents/dots within ≤1.7 frame px) | `judge_attempt_2.txt` | **PASS** — 0 BLOCKER/MAJOR; 2 MINOR (bullet pitch "very slightly looser" ~conf 0.55, within tolerance; inner border AA weight slightly heavier, inherent medium difference) |

Final: **PASS on attempt 2 of 6** (real comparison winner body, single-read, default route `images`, glm leg DEFERRED/BLOCKED; gate reported 0 degenerate events).

## Judge attempt 1 issue disposition (PIL forensics)

1. **italic+underline (MAJOR)** — CONFIRMED, fixed. Attempt 1's first forensics pass was wrong:
   the underline is a faded-gray continuous 377px run at y153-154 (x300..676) in the original,
   invisible to a sum<330 ink threshold (found at sum<620); the 'P' cap stem slants 3px over
   14 rows = PowerPoint's 12° italic angle (attempt 1 had measured only descender stems).
   Judge was right; spec typography_notes were right.
2. **line spacing (MAJOR)** — DISPROVEN by PIL: bullet pitch render 32.15 vs original 32.17
   frame px (per-line baseline deltas ≤0.4); the perception was a cascade of issue 3.
3. **ellipsis clipping (MAJOR/borderline BLOCKER)** — DISPROVEN by PIL: ellipsis ink bottom
   503.3 (render) vs border top edge ~513.5 → 11.9 frame px clearance (original: 14.7);
   0 ink pixels on or crossing the border. The probe's identical claim is likewise false.
   Nudged the line up 1.3px anyway (baseline 501.7) to match the original's measured ink
   bottom (502.0) — removes the perception entirely.

## Deliverable

- PPTX (SINGLE-VERSION, plain name): `videos/deep-learning/001_introduction/recreated_pptx/slide_010_recreated.pptx`
- Build: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_010.js`
  (playlist house chrome imported from `videos/deep-learning/shared_patterns/house_chrome.js`,
  numeral 10 per 001_introduction/AGENTS.md pending-founder-veto rule; all content at
  PIL-measured frame px; fonts metric-solved against real Arial TTFs: title Arial Bold 25pt,
  lead Bold 21 red C00000 + Regular 21 italic-underlined, intro Bold 21, bullets Regular 20;
  borders 000080 deck navy — spec's 2222CC/CC2222 guesses reconciled to ink per deck pixel law;
  title fill FAFED9 = measured modal (250,254,217), exact modal match in render)
- Closed-loop calibration constants (attempt 1): LO renders baselines +1.1..+2.1 frame px low
  vs the placement formula → per-group CAL shifts; LO hinting compresses advances ~0.45px/char
  (bullets) / 0.35px/char (title) → charSpacing compensations.

## Evidence (qa/slide010/)

`render_1.png`, `render_2.png`, `build_attempt_1.js`, `build_attempt_2.js`,
`judge_prompt_1.txt`, `judge_prompt_2.txt`, `probe_1.txt`, `judge_attempt_1.txt` (FAIL),
`judge_attempt_2.txt` (PASS), `selfcheck_attempt_1.py` + output, `selfcheck_attempt_2.py` + output.
DB row: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
`visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide010/judge_attempt_2.txt`,
`pptx_path` + `build_script` set.

## Notes / deviations

- Spec's "top rule" (#8B1A1A) NOT drawn as a separate element: original rows 42-44 are the
  chrome panel's own red top-border position, covered by `drawHouseChrome` (slide_005 precedent).
- Spec's "red square at far bottom-left" of the black bar NOT drawn: 0 red pixels in bar rows
  519..539 of the original.
- Mouse cursor (recording artifact) omitted per ground rule (c); black bottom bar kept
  (drawn y519..537.5, leaving the chrome's half-visible bottom stroke visible — same treatment
  as certified slide_005).
- Judge procedure executed by the worker via Bash (no Agent/Task spawn tool in this
  environment) — orchestrator-approved fallback; verdicts taken verbatim from the gate's
  validated comparison winner bodies.
- SOURCES.md honored: slide is text-only (no site figures apply); its open questions concern
  analysis provenance, not recreation fidelity.
- No component banking obligation: no slide in any video's dependency graph references slide 10.
