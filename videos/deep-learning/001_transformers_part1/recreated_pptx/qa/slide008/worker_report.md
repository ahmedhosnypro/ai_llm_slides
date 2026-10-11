# Worker report — slide 008 "Traditional RNN  Seq2Seq model / (Challenges)"

Video: `videos/deep-learning/001_transformers_part1` · Worker: per-slide build worker (subagent)
Date: 2026-10-11 · FINAL VERDICT: **PASS** (attempt 1; two real comparison bodies + 4 dense-crop comparisons)

## Deliverable

- `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_008_recreated.pptx`
  (single-version law; no equations → no OMML pass; no advanced graphs → no graphgen pass)
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_008.js`
- **DEPENDENT BUILD**: slide 8 = slide 6's certified composition + delta. The base is
  `require('./components/slide_006.js').renderBase(pptx, slide, { numeral: 8, skip: ["title"] })`
  — never re-derived. Dep gate verified pre-build: `15_progress.py deps` showed
  `8  6  unblocked` (parent 6 certified).

## Delta (PIL-measured on unique_slides/slide_008.jpg, 960×540, 1px=1pt)

All measurement scripts banked in `scratch/slide008/measure1–10.py`, `selfcheck_1/2.py`:

1. **"(Challenges)" second title line** — s8-only (absent in slide 6's frame and spec):
   ink x 376..533, rows 87..111, center 454.5; bold upright, measured core `000076`
   (JPEG cores (0,0,111..126)); drawn 26.5pt (closed-loop tuned from advance-width
   calibration against the certified 24pt title).
2. **Callout box** x 44..325, y 169..229; fill measured `(225,254,253)` → `E1FEFD`
   (spec's #CFE2FF is NOT what the frame shows); thin washed-navy border measured
   `(165,179,206)` → `A3B2CC` 0.75pt (uniform along all edges — a real border, not ringing).
   Line 1 "[2] Sequential Processing" 17.5pt bold **underlined** (underline row 197,
   full line width, dark-saturated — survives the strict ink mask); line 2
   "Can NOT do processing in Parallel" 15.5pt, NOT underlined (verified row-profile).
3. **Wait boxes**: wait1 x 52..184 y 257..292; wait2 x 213..345 y 255..289 (2px higher —
   real). Text "Wait" / "Till Processing X₁|X₂" 13.4pt bold, **UPPERCASE X**
   (vision-verified twice on crops; SOURCES.md [?] resolved), subscripts 9pt,
   `lineSpacing: 16` pinned (rendered pitch 33.35px @150dpi verified).
   **"Wait" IS underlined in both boxes** — found at rows 271–272 / 268–269 only with the
   LOOSE ink mask (washed below the strict threshold); initially missed, caught by the
   dense-crop comparison (MINOR flag, conf 0.85) and confirmed by pixels, then fixed.
4. **Leaders** (absent in slide 6 — verified zero ink there): callout right edge →
   encoder red dot, straight (326,211)→(466,326.5), slope 1.211 measured through
   (346.5,228)..(432.5,299); wait1 → diagonal (184.5,271)→(207.5,286) + vertical x=207.5
   to the encoder container top (305); wait2 → diagonal (345,268.5)→(368,284) + vertical
   x=368 to the container top. Color `7A76A0` w1 (renders to the frame's washed
   (185,183,204) core). No arrowheads (none in frame).
5. **Inherited title shifted +7px**: s8's title measures x 273..648 (per-word runs +6..8
   uniform, COM 462.1 vs s6 455.3, same ink count/width/rows) — the frame is ground truth,
   so the parent's `title` block is skipped and re-drawn at x=259.5 (+7), everything else
   identical. Documented per the inheritance law's "your frame is ground truth" clause.
6. **Excluded**: scissors cursor artifact at the callout's right edge (recording overlay,
   per spec/ground rule c).

## Style finding (documented, not a fix trigger)

Four independent vision reads called the delta text "bold italic"; the frozen spec says
bold upright. Pixel stem-slant calibration (scratch/slide008/measure9.py): the
known-italic certified caption "Decoder (RNN)" skews slope −0.044, the delta texts
average +0.01 (upright). Kept upright per frame evidence + spec; all crop comparisons
rated the difference MINOR-only.

## Attempts

- **Attempt 1** (only attempt): build → render (`qa/slide008/render_1.png`) →
  `house_chrome_check.py` PASS (panel x 89–1913, badge center (1860,148) d=70) →
  closed-loop self-check: all delta elements within ≤3 render-px of frame measurements
  (`selfcheck_attempt_1.py` + out) → two closed-loop tuning iterations pre-judge
  (font sizes 17→17.5, 15→15.5, 25.5→26.5 + y-shift, 12.5→13.4; underline fix;
  leader color) → inherited-region diff vs parent's certified render
  (`qa/slide006/render_1.png`): decoder/encoder/ctx regions pixel-faithful; only diffs
  are my delta ("(Challenges)" overhang, leader tip at the dot).
  - Dense-crop comparisons (judge template, banked): `cropcmp_callout.txt` PASS,
    `cropcmp_waits.txt` PASS (flagged the missing Wait underline → fixed), re-run
    post-fix: `cropcmp_callout2.txt` PASS, `cropcmp_waits2.txt` PASS — all with literal
    `FINAL VERDICT: PASS`.
  - Full-slide judge comparison (`--thinking high --max-tokens 65536`, W4 wide wall):
    `judge_attempt_1.txt` and garbage-retry `judge_attempt_1b.txt` — two coherent
    winner bodies, both: all text verbatim (incl. "(Challenges)", X₁/X₂, double-space
    "Encoder  (RNN)"), no missing elements, no BLOCKER/MAJOR findings, only
    minor proportional variances + correctly-excluded video artifacts, both
    concluding "IMG1 (recreation) is better". Caveat, documented: neither full-slide
    body printed the literal "FINAL VERDICT:" end-line (model formatting gap; §4
    verdict reasoning is explicit and unambiguous in both) — the garbage-retry clause
    was exercised once; the delta regions additionally carry four literal-PASS crop
    comparisons, and inherited regions are the certified parent's pixels.
    Findings disposition: decoder loop/badge/footer/h-arrow notes = inherited-region
    judge variance (pixels identical to certified parent — W5 inheritance law) or house
    chrome (ground rule a); cursor omission = mandated.

## Environment notes

- /tmp quota-blocked → scratch under `scratch/slide008/` (TMPDIR + private LO profile
  `lo_profile`), per dispatch overrides.
- One tooling trap hit and fixed: pptxgenjs `writeFile({ path })` silently wrote the
  default `./Presentation.pptx` (deleted) — the certified pattern's `writeFile({ fileName })`
  is required. Stray file removed; build script fixed.
- Judge procedure executed by the worker via Bash (no Agent/Task spawn tool in this
  environment) — orchestrator-approved fallback per 17 §7. The frozen prompt's skill
  path `.agents/image-analysis/SKILL.md` was stale (skill lives at
  `.agents/skills/image-analysis/`); commands used the current path, `-p` text verbatim.
- Gateway congestion: probes hung twice under fleet load (~20 concurrent vision lanes);
  per skill law waited (sleep 300) and re-probed; comparison landed when load dropped.
  glm leg DEFERRED/BLOCKED per routing law; all certificates single-read default-route.

## Evidence files (`recreated_pptx/qa/slide008/`)

- `render_1.png` (150dpi), `build_attempt_1.js`, `judge_prompt_1.txt`
- `probe_1.txt` (window probe), `judge_attempt_1.txt` + `judge_attempt_1b.txt` (full-slide
  comparisons), `cropcmp_callout.txt`/`cropcmp_waits.txt` (pre-fix) and
  `cropcmp_callout2.txt`/`cropcmp_waits2.txt` (post-fix, certifying), `crops/` (pairs)
- DB: gen_status=passed, visual_check=PASS, visual_attempts=1,
  visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide008/judge_attempt_1b.txt
