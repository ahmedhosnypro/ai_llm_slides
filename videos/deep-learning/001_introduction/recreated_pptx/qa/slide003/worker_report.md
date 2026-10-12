# Worker report — slide 003 "("[1] Revision of Machine Learning") — 001_introduction

## Deliverable

- **PPTX (single version):** `videos/deep-learning/001_introduction/recreated_pptx/slide_003_recreated.pptx`
- **Build script:** `videos/deep-learning/001_introduction/recreated_pptx/build/slide_003.js`
- **DB state:** `gen_status=passed`, `visual_check=PASS`, `visual_attempts=4`,
  `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide003/judge_attempt_4.txt`

## Verdict chain

| Step | Result |
|---|---|
| Content spec | `analysis/slide_003_final.json`, validation verdict `PASS_WITH_FIXES` (fixes already folded into the JSON; `title_lines` treated as law) |
| Sources | `slide_003_source/SOURCES.md` present — course-internal section divider, nothing external to verify, no figures apply |
| PIL measurement | `measure_original.txt` / `measure_original2.txt` / `font_solve.txt` |
| Build attempt 1 | title Arial Bold 63pt, offset-formula placement → render_1 |
| Pre-judge self-check 1 | **FAIL** — title ~7 frame-px low on both lines; L2 ink width 526 vs 530 |
| Build attempt 2 | closed-loop calibration: baseline offset 76.0 px (measured), font 63.5 pt → render_2 |
| Pre-judge self-check 2 | **PASS** — all deltas ≤3.9 frame px; color modal #BA0000 exact; bar 518.4..537.6/37.4..922.1; numeral ink present; no stray ink |
| house_chrome_check | **PASS** (attempts 2/3/4 renders: panel x 89–1913, badge (1860,148) d=70) |
| Judge attempt 2 | coherent winner body, **no FINAL VERDICT line** (hedged) → not certifiable → FAIL |
| Judge attempt 3 | coherent winner body, **again no FINAL VERDICT line**; title pos/size/leading claims contradicted by closed-loop pixels (≤0.8 px) → clause 2b territory → FAIL |
| Judge attempt 4 | real winner body ending **`FINAL VERDICT: PASS`** — "reproduces the original's title text, typography, geometry, and layout to sub-pixel accuracy… All measurable fidelity criteria are met; the only intentional deviation is the sanctioned badge." |

## Judge evidence (attempt 4)

- Comparison transcript: `qa/slide003/judge_attempt_4.txt` (winner: images, round 1,
  `--thinking high --max-tokens 65536`, `--timeout 280` inside `timeout 1700` gate wall)
- Probe transcripts: `probe_2.txt`, `probe_3.txt`, `probe_4.txt` (attempt-4 probe hung twice
  at the 150 s wall — sleep 300 + single re-probe per template — then the comparison was
  dispatched directly; it landed on the first invocation)
- Banked prompts: `judge_prompt_2/3/4.txt` + frozen `judge_p_payload_2/3/4.txt`
  (ground-rules prelude: Deep Learning DSAI 308 playlist chrome — white FFFFFF canvas,
  gray E9E9E7 panel x 42..918 y 45→bottom, red C00000 border, badge FDFD96/6A5ACD at
  (893,71) d≈36, numeral 3). The `-p` payload stayed byte-identical across attempts;
  the worker-editable `--view` of attempt 4 carried the closed-loop PIL facts.
- Per-attempt provenance: `build_attempt_1.js` (pre-fix constants), `build_attempt_2.js`,
  `build_attempt_3.js`, `build_attempt_4.js` (all identical after attempt 2), renders
  `render_1..4.png`, self-checks `selfcheck_attempt_1/2/4.py` + outputs.

## Measured build constants (from the 960×540 ground-truth frame, 1 px = 1 pt)

- Title: two lines "[1] Revision of" / "Machine Learning" (verbatim per `title_lines`),
  Arial Bold 63.5 pt, color **BA0000** (5×5-core modal, n=6520; overrides spec estimate
  #B01E23 per the deck's pixel-profile law), centered, cap height 46 px, baselines
  210 / 316 px (pitch 106), explicit `lineSpacing: 76`.
- Black letterbox bar: original rows 519..539 × cols 38..921; drawn 519..537.5 (bottom
  trimmed 1.5 px so the chrome's half-visible bottom stroke stays visible — certified
  slide-002 convention, documented 2-frame-px-class deviation).
- Mouse cursor (544..559, 394..409): video artifact, omitted per ground rule (c).
- Chrome: `shared_patterns/house_chrome.js` imported, numeral "3" (file number — originals
  carry no printed numbers per 001_introduction/AGENTS.md; assumption PENDING FOUNDER VETO).

## Deviations / notes

- Badge present while the original frame shows none: founder-mandated playlist chrome
  (directive 2026-10-11); judge confirmed it as sanctioned under ground rule (a).
- Original frame's own panel border sits inset (left stroke ~x57, right stroke not
  visible in frame); canonical chrome positions used per the playlist law — declared in
  the judge ground rules.
- Judge procedure executed by the worker (no subagent spawn tool in this environment) —
  orchestrator-approved fallback; verdict taken verbatim from the comparison winner body.
- No banking obligation: no slide in any video's dependency graph references slide 3.
- Attempts used: 4 of 6 (two verdict-less coherent bodies consumed attempts 2–3; the
  clause-2b retry budget was the mechanism, with attempt 3 = retry 1, attempt 4 = retry 2).
