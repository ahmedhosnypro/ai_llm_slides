# Worker report — slide 019 (Encoder – Decoder Transformer), deep-learning/002_transformers_part2

Cross-video child of `deep-learning/001_transformers_part1:19`. Dispatched 2026-10-12; five
judge attempts; **FINAL VERDICT: PASS** (main judge `judge_attempt_5.txt`; pin crop
`cropcmp_pin_5.txt` PASS; decoder-stack crop `cropcmp_chev_3.txt` PASS). DB:
`visual_check=PASS`, `visual_attempts=5`, `gen_status=passed`.

## Deliverable

- Build: `recreated_pptx/build/slide_019.js` (per-attempt copies: `build_attempt_2/3/4/5.js`)
- PPTX: `recreated_pptx/slide_019_recreated.pptx` (single version; no equations → no OMML
  wrap; no advanced graphs → no graphgen)
- Renders: `qa/slide019/render_1..5.png` (150 dpi, 2001x1125)

## Cross-video import (build law)

`require()` of 001's certified component **by absolute path, fresh at build time**:
`/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_019.js`
(md5 eeda3307335a7f398fe106d3864929cb, re-banked v2 01:52, coordinator-notified fresh-bank;
`renderBase(pres, slide, {numeral: 19, skip: [...]})`). Inheritance verified: my render vs
001's certified `render_4.png` differs ONLY at my measured delta regions. Badge numeral 19 =
the number printed on this frame (== parent default, passed explicitly).

## Frame→build mapping (derived from THIS frame's chrome landmarks)

Video 002's capture is zoomed out ~0.958. Fitted from this frame's four border landmarks
(L 58.32 / R 901.37 / T 43.26 / B 516.85, sub-pixel centroids), composed with 001's own
frame→build transform (001:19 landmarks vs certified render; `m7/m8`):

```
frame_x = 18.0787 + 0.961084 * build_x ;  frame_y = 0.4700 + 0.957187 * build_y
```

Cross-checks: frame badge ring (875.5, 71.0) → build (892.1, 73.7) — the same ~+2.8pt y
residual the certified 002 slide-002 build measured and accepted; content-masked affine
SSD fit (`m6`, masked-SSD 11) agrees within ~0.5px. slide_002's precedent mapping agrees
within ~1px. (Self-check lesson recorded: render→build is `×150/72` with ZERO offset — a
wrongly offset build→render map caused two false alarms, fixed in `selfcheck_attempt_1c`.)

## Measured delta (my frame is ground truth; `m9_delta.py` + probes m10–m15)

REMOVED (present in 001:19, 100% panel-gray here — via `opts.skip`):
- `legend1/2/3` callout boxes ('Normalization Layer' / 'Feed Forward Layer' /
  'Residual Connections')
- `leader1..5` hairlines + the two black arrowheads into the encoder/decoder FF boxes
- `dec_green`'s navy chevron pairs at zones (783.5,197/202) and (783.5,255.5/259.5) —
  this frame shows the thin dark up-arrow shafts there instead; the zone-3 pair
  (772,313/318) IS present → redrawn by `drawDecGreenChild` (geometry verbatim from the
  certified component, minus those four chevrons; the certified component file untouched)

ADDED (drawn after renderBase):
- `drawGapShafts`: thin dark (2F2F2F 1.75pt) inter-box shafts through the two decoder gaps
  (build y194–206 and y250–263 at x784.7) — 017's decoder spine stops at y201/306 because
  lecture 001's chevrons filled those gaps; this frame shows continuous shafts
  (`selfcheck_attempt_3` gap probes: REND 141 vs FRAM 32–301 before fix → both gaps dark
  after)
- `drawBottomBand`: translucent yellow rounded band, build x561.5 y412.5 w351 h84,
  FFFF00 @ 50% transparency, rectRadius 0.12in — blend-fit alpha 0.45–0.5 over mint/peach/
  dark-tan backgrounds (m13); drawn OVER the outer green frame border (measured)
- `drawPin`: red map-pin 'WE ARE HERE' — head circle d71.4 at (531.8,333.8) (chord fit
  <2pt, m13); single smooth tail wedge (rotate 340) apex on the measured tip (595.1,435.2);
  two rotated bulge ellipses filling the bulb→tail transition; text THREE tilted lines
  'WE'/'ARE'/'HERE' 12.5pt bold white, rotate 342, lineSpacing 17. Pin sits ON TOP of the
  band (measured: tail red over band yellow).

INHERITED VARIANCE (documented, no action): dash-phase fragments of 018's dashed zoom lines
at build (623–628, 303–309)/(374–380); the decoder container right-border capture-phase
darkness (frame x825: (32,74,38) here vs (79,120,91) in 001's frame — sub-pixel blend of
the same dark line).

## Attempts

1. **render_1** (imported base + first delta draft): self-checks caught the band left edge
   2–4pt wide → fixed before judging (no judge dispatched).
2. **render_2 / judge attempt 2**: main comparison **PASS** (2 MINOR); pin crop **FAIL**
   (MAJOR: zig-zag two-triangle tail + two horizontal text lines vs original's smooth
   tilted teardrop with three lines); decoder-stack crop **FAIL** (missing inter-box arrow
   in gap 2, 0.75 conf). Fixes: single tail wedge, three tilted text lines, gap shafts.
3. **render_3 / judge attempt 3**: chevron crop **PASS** (shaft fix verified); main judge
   **PASS**; pin crop **FAIL** — findings "green dashes crossing the bulb" (BLOCKER 0.7)
   and "red dashed diagonal over the yellow box" (MAJOR 0.6) were **pixel-refuted against
   the ground truth** (`m15`/follow-up scan: 4 anti-alias edge px, zero dashes-on-red, zero
   red px in the claimed region); my own scan found the real residual: the tail's
   lower-left bulge ran 7–10pt thin.
4. **render_4**: bulge filler added; left-edge deviations reduced to ≤4pt except two rows.
5. **render_5 / judge attempt 5**: pin crop **PASS** (5×MINOR, incl. fill tone = video
   shading); main judge **PASS** (3×MINOR: inner-diagram spacing, pin size/offset,
   leader-routing angles — spacing-only). **DONE.**

Probe hangs: probes hung at both attempt-3 and attempt-5 first tries (rc 124; per the
frozen procedure, one sleep-300 re-probe; attempt-5 re-probe landed). Comparisons landed
first try throughout. Judge procedure executed by the worker via Bash — no Agent/Task
spawn tool in this environment (orchestrator-approved fallback, per
`scripts/17_worker_instructions.md` §7). One runner fix: the banked prompt's
`.agents/image-analysis/...` path is stale in this workspace; the actual script lives at
`.agents/skills/image-analysis/scripts/analyze_image.py`.

## Closed-loop numbers (banked under `scratch/slide019/`)

- `selfcheck_attempt_2.txt`: band edges ≤2pt; pin blob within 2pt; white text px 2108 vs
  2113; legends 100% gray in both; chevron zones navy R/F 0/0, 0/0, 278/269.
- `selfcheck_attempt_3_out.txt` / attempt_5 verification: gap shafts present; tail
  left-edge within ≤4–6pt on all rows; full-panel strong-pixel rate 15.4% (the certified
  parent's own render-vs-frame baseline is 23.05%).
- `house_chrome_check.py` PASS on every render.

## Component banking

No slide in ANY video's dependency graph references 002:19 (edges: 19→001:19 and
37→001:19 only), so per rule 2 the conditional banking obligation does not trigger and no
component was banked. The build script is structured so a component can be derived
additively later (delta blocks are standalone functions) without touching this certified
deliverable.

## Evidence index

- Main judge (verdict of record): `qa/slide019/judge_attempt_5.txt`
- Supporting PASSes: `qa/slide019/cropcmp_pin_5.txt`, `qa/slide019/cropcmp_chev_3.txt`
- Historical: `judge_prompt_2/3/5.txt`, `run_gate_attempt2/3/5.sh`, `probe_2/3/5.txt`,
  `render_1..5.png`, `build_attempt_2..5.js`, `selfcheck_attempt_*.txt`,
  `cropcmp_pin_2/3.txt` + `cropcmp_chev_2.txt` (failed attempts, kept as provenance)
- Measurement scripts: `../../scratch/slide019/m1..m15*.py`, `affine.npy`,
  `frame_in_render_space.png`, `warped_001_f21.png`, `delta_mask_overlay.png`
