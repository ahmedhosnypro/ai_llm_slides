# Worker report — slide 020 "Self Attention Mechanism" (section divider)

Deep Learning DSAI 308, Transformers — Part I (`videos/deep-learning/001_transformers_part1`).
Worker ran 2026-10-12. Attempts used: **1 of 6**. Final verdict: **PASS** (attempt 1).

## Deliverables

- PPTX: `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_020_recreated.pptx`
- Build: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_020.js`
- Judge comparison transcript: `videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide020/judge_attempt_1.txt`
- Probe transcript: `videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide020/probe_1.txt`
- Banked prompt / build / render: `qa/slide020/judge_prompt_1.txt`, `build_attempt_1.js`, `render_1.png`
- Self-check: `qa/slide020/selfcheck_attempt_1.py` + `selfcheck_attempt_1_output.txt` (ALL PASS)

## Slide facts

Course-authored section divider (SOURCES.md: no external source, no figures). Content =
house chrome + centered red title "Self Attention Mechanism" + badge "20". The spec's
"Bottom rule" element is the playlist chrome panel's half-visible bottom border stroke
(rows 538–539 in the frame; certified slide_001 precedent relies on the chrome stroke
alone). Mouse-cursor artifact over the title omitted (judge GROUND RULES (c); spec brief
step 7).

## Build & calibration (pre-judge, closed-loop)

Chrome: shared `videos/deep-learning/shared_patterns/house_chrome.js`
`drawHouseChrome(pptx, slide, {numeral: 20})` — mandatory playlist law (NOT ml-intro values).

Frame measurements (960x540, 1px=1pt): title ink x 184–774 (591px), band y 261–297,
'S' cap 35px, baseline 297px, ink core (192,15,33) → C00000; badge center (893,72);
panel x 42..918 y 45..540.

Closed-loop calibration on 150dpi LO renders:
- attempt A @50pt: width 604 frame-px (2.2% wide), ink center y 285.7 (6.7 low)
- **final @49pt, box center y 3.856in: ink x 183.7–774.3, y 261.0–297.0 — sub-pixel
  match to the original (dL −0.3, dR +0.3, dT 0.0, dB 0.0 frame-px); ink center
  (479.0, 279.0) vs original (479.0, 279.0)**

## Pre-judge self-checks (17 §2, banked)

- `house_chrome_check.py`: **PASS** (panel x 89–1913, y 95–bottom; badge center (1860,148) d=70, tol 8)
- FRAME CONTAINMENT (adapted to playlist white margin + gray panel): 0 stray ink px on
  the outer white margin; title ink inside the panel with clearance — PASS
- Title geometry vs original within 4 frame-px: PASS (≤0.6)
- Badge center (892.1, 70.8) vs (893, 71); numeral "20" ink present — PASS
- Bottom red rule across the slide — PASS
- No red ink outside the title band inside the panel (no wrap); single line confirmed — PASS
- Equations / delimiters / tables: N/A (none on this slide — spec + original-frame scan)
- Dense-region crop compare: N/A (no equations, delimiters, or tables)

## Judge (attempt 1) — self-executed fallback

No Agent/Task tool available in this environment → judge procedure executed by the
worker via Bash, byte-for-byte per the banked `judge_prompt_1.txt` (17 §7 fallback,
orchestrator-approved). One deviation: the template's relative script path
`.agents/image-analysis/scripts/analyze_image.py` is stale after the skill's
2026-10-11 move — used the actual `.agents/skills/image-analysis/scripts/analyze_image.py`
(SKILL.md amendment confirms the location). Everything else verbatim.

- Probe: valid winner body (`probe_1.txt`), window opened, no retry needed.
- Comparison: `--thinking high --max-tokens 65536`, W4 wall (timeout 540 / --timeout 420),
  single read, default route (images), glm leg DEFERRED/BLOCKED, degenerate events 0.
- Verdict (real winner body, `judge_attempt_1.txt`): element-by-element table all MATCH;
  discrepancy list: none (BLOCKER none / MAJOR none / MINOR none). Cursor omission and
  bottom banding correctly classified as video artifacts; chrome per ground rule (a).
  **"FINAL VERDICT: PASS"** — "The recreation is a faithful, usable recreation."

## DB state (VIDEO=deep-learning/001_transformers_part1)

gen_status=passed, visual_check=PASS, visual_attempts=1,
visual_transcript=…/qa/slide020/judge_attempt_1.txt, pptx_path + build_script set.

## Component banking

Slide 20 has NO dependents (checked `slide_dependencies.json` same-video edges and 002's
cross-video refs — none target 20), so the playlist-scoped banking obligation does not
apply. If a future lecture ever recap-references this divider, the composition is
trivially re-derivable from the shared chrome + one centered text box.

## Notes for the orchestrator

None — no remaining issues. DEP state: root/unblocked, now certified.
