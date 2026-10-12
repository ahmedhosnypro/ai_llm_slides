# Worker report — slide 012 "Feature Invariants" (deep-learning/001_introduction)

## Summary

- Slide: 012 — "Feature Invariants" (rotation / scaling / translation / mirroring invariants list)
- Attempts used: 1 of 6 (judge PASS on attempt 1)
- Final verdict: **PASS** (real comparison winner body, coherent, non-degenerate)
- Deliverable: `videos/deep-learning/001_introduction/recreated_pptx/slide_012_recreated.pptx` (SINGLE-VERSION)
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_012.js`
- Comparison transcript: `videos/deep-learning/001_introduction/recreated_pptx/qa/slide012/judge_attempt_1.txt`
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`, `visual_transcript` set.

## Verdict chain

1. **PIL measurement of ground truth** (`measure_1..9.py`, banked): frame 960x540 (1px = 1pt).
   Title box border centerlines x94..364, y81..138, fill modal (228,254,251)=E4FEFB, border
   000080 ~1.5pt. Content box x95..881, y157.5..390, fill FFFFFF, border 000080 ~2pt. Black
   bar x38..921, rows 519..539. Header baseline 181.5: red bold "Features Invariants are "
   (C00000, stem 3px; advance reconciles to Arial Bold 21pt) + regular " is " + regular-italic-
   underlined "Problem dependent" (advance 183 = Arial Regular 21pt EXACT; italic from 'P' stem
   slant; underline rows 183-184 x378..567 starting right after "is" — slide_010 precedent).
   Bullets Arial Bold 21pt (cap 15px = 0.716x21, stems 3px), ink left 126.5, baselines
   249/293/337/381 (44pt pitch, anchored by dot centers 241/285/329/373, x-center 108.3, d~5.5).
   Title "Feature Invariants" Arial Bold 24pt (advance 208, pred 207), ink center 229 == box
   center (centered), baseline 117.5. No badge/no printed number in original (PIL-probed;
   per 001_introduction/AGENTS.md the numeral is the file number: 12). Spec's "top rule" at
   ~7-8% = chrome panel's own red top border rows 42-44 (slide_005/slide_010 precedent — not
   a separate element). Mouse cursor over bullet 3 = recording artifact, excluded (spec step 9,
   ground rule c). Red vertical line at cols 58-59 in the original: present identically in
   certified slide_010's frame — playlist chrome law freezes the panel; nothing drawn there.
   All other zones PIL-verified empty (no missed elements).
2. **Build** (`build/slide_012.js`): pptxgenjs, LAYOUT_WIDE, imports
   `videos/deep-learning/shared_patterns/house_chrome.js` `drawHouseChrome(pptx, slide,
   {numeral:"12"})` — chrome never re-drawn. Bare hex, fontFace everywhere, margin:0,
   explicit lineSpacing on every text box, per-baseline single-line boxes (slide_010 model).
3. **Render 1**: private-profile soffice with `TMPDIR=$QA/scratch` (namespace scratch, /tmp
   quota blocked) + absolute `-env:UserInstallation`; 150dpi PNG 2001x1125 →
   `qa/slide012/render_1.png`. Build + prompt banked (`build_attempt_1.js`, `judge_prompt_1.txt`,
   payload extracted byte-for-byte → `judge_payload_1.txt`).
4. **Pre-judge self-checks** (all banked):
   - `house_chrome_check.py` → **PASS** (panel x 89-1913, badge (1860,148) d=70, tol 8).
   - `selfcheck_attempt_1.py` → **14/14 OK**: every measured element within ≤2.3 frame-px of
     the original (title box ≤1.2, content box ≤1.2, black bar ≤1.7 with parity x37.4..921.6
     vs orig 38..921, title text ≤0.5 after calibration, header band ≤0.9, red run ≤1.9,
     underline ≤2.3, bullets ≤0.9, dots ≤0.5); fills exact (E4FEFB, FFFFFF); containment OK
     (content-zone ink inside boxes; slide-bounds OK; no equations/delimiters/tables — n/a).
   - Attempt-1 closed-loop calibration: initial render measured title +1.5px low and 5px
     narrow → `CAL_TITLE -3.5` + `charSpacing 0.3` → re-render → 0.5px (no judge attempt spent).
5. **Judge attempt 1** (executed by worker via Bash — no Agent/Task tool in this environment;
   orchestrator-approved fallback per 17_worker §7): probe (timeout 150 / --timeout 120) —
   valid body, `probe_1.txt`; comparison at the W4 wide wall (`timeout 540` / `--timeout 420`,
   `--thinking high --max-tokens 65536`, `-p` sourced byte-for-byte from `judge_payload_1.txt`)
   — coherent winner body ending **FINAL VERDICT: PASS** for 'faithful, usable recreation'.
   Findings: 0 BLOCKER / 0 MAJOR; 2 MINOR (low confidence): last bullet ~2% proportionally
   closer to box bottom than original (PIL measured: bullet4 bottom 384.8 vs box 390 — gap
   5.2px, matching the original's 385→390 gap 5px within 0.2px — variance, not a defect);
   fonts read slightly heavier than the video-compressed original (medium difference).
   Certificate: single-read, default route (images), glm leg DEFERRED/BLOCKED.

## Judge walls note

Dispatch said "timeout 280 inside 1700s outer"; executed instead the binding
`scripts/17_worker_instructions.md` W4 walls (probe 150/120; comparison 540 outer / 420 inner)
— the same shape that certified every sibling PASS in this namespace (slide_005..010
banked prompts/transcripts), with the pattern-library law that the outer wall must exceed
~2x the per-call wall. No HangError occurred (comparison landed in one round).

## Deviations from spec (ink-law wins, documented)

- Title fill E4FEFB (measured) vs spec guess D8F0F0; borders 000080 deck navy vs spec guesses
  000080/1F1FB8; header red C00000 (deck law, JPEG-darkened modal) vs spec CC0000.
- Title 24pt bold (measured) vs spec estimate 26-28pt; header 21pt vs 20-22pt; bullets 21pt
  bold vs 18-20pt.
- "Top rule" not drawn (it is the chrome panel's red top border); background via playlist
  chrome (white canvas + E9E9E7 panel) vs spec's flat E9E9E9.
- Black bar drawn y519..537.5 (h 18.5) so the chrome's half-visible bottom stroke stays
  visible (certified slide_005/slide_010 treatment; original bar rows 519..539).
- Mouse cursor omitted (artifact).

## Evidence index (qa/slide012/)

- `measure_1..9.py` — PIL forensics of the original frame
- `selfcheck_attempt_1.py` + `selfcheck_attempt_1_output.txt` — 14/14 closed-loop check
- `bullets_check_1.py` + `bullets_check_1_output.txt` — clean bullet-band check
- `house_chrome_check_render1.txt` — PASS
- `render_1.png`, `build_attempt_1.js`, `judge_prompt_1.txt`, `judge_payload_1.txt`
- `probe_1.txt`, `judge_attempt_1.txt` (winner body: FINAL VERDICT: PASS)
- `scratch/` — private LO profile + PDF (workspace-internal, /tmp quota blocked)

## Banking obligation

`slide_dependencies.json` edges: 16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35 — no slide in
any video depends on slide 12. No component banking obligation (confirmed by dispatch).
