# Worker report — slide 015 (002_transformers_part2) — CROSS-VIDEO CHILD of 001:43

## Result

- **Verdict: PASS** (attempt 1). Comparison transcript (judge of record):
  `videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide015/judge_attempt_1.txt`
  — single-read, default route (images), glm leg DEFERRED/BLOCKED; no BLOCKER/MAJOR;
  4 MINOR findings (documented below, none fix triggers under the inheritance law).
- Deliverable: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_015_recreated.pptx`
  (single version, no suffix).
- Build script: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_015.js`
  (banked copy: `qa/slide015/build_attempt_1.js`).
- DB: gen_status=passed, visual_check=PASS, visual_attempts=1,
  visual_transcript=qa/slide015/judge_attempt_1.txt.
- Judge procedure executed by the worker (no spawn tool in this environment —
  orchestrator-approved fallback), byte-for-byte per the banked prompt
  (`qa/slide015/judge_prompt_1.txt`), frozen `-p` template verbatim, shared-base fact
  carried in `--view`.

## Dependency law compliance

- Gate: `15 ← deep-learning/001_transformers_part1:43` — parent certified in ITS OWN DB
  (gen_status=passed, visual_check=PASS) before any build work started (`deps` showed 15
  unblocked). Parent component imported BY ABSOLUTE PATH:
  `require(".../001_transformers_part1/recreated_pptx/build/components/slide_043.js")`;
  its `renderBase(pres, slide, {numeral: 15, skip: [all 18 content blocks]})` draws the
  playlist house chrome ONCE with badge numeral 15. Nothing copy-pasted, nothing re-derived.
- PIL diff of this frame vs the imported composition's output
  (`scratch/slide015/diff_base.py`, 32.7% hot px) showed this recap is NOT a pixel-identical
  re-draw: same architecture family, entirely re-drawn at new geometry (stack shifted
  right+up, no concat/LT row, no top title, title at BOTTOM, per-head W chip columns,
  orange/green input ellipses). Per `references/dependencies.md` (001 slide_045 precedent)
  the deviating blocks are REDRAWN at THIS frame's measured geometry; the import supplies
  the chrome — the composition is still imported, never re-drawn from the parent's coords.
- Component banking: no slide in any video's graph depends on 002:15 (checked
  `slide_dependencies.json` + deps output) — no component banked (playlist-scoped
  obligation applies only when referenced).

## Measurement provenance (all under `scratch/slide015/`)

- Frame→slide mapping fitted from THIS frame's four chrome landmarks:
  frame_x = 17.628 + 0.961232·slide_x; frame_y = 0.955556·slide_y; badge cross-check
  (874.5,70.5)→(891.5,73.8) vs house (893,71) — the same accepted JPEG-bbox delta as the
  certified 002 slide_002/018 builds.
- PIL scans: measure_frame.py, measure_cards*.py, measure_mega.py, measure_elements.py
  (frame resampled into slide coords, per-element color-mask bboxes).
- Gate vision reads (banked .txt): crops A..E (full-region decodes), Z1 (h1 tag row:
  pill fills white, Sim text gray vs Prob/WS blue 4A5AA0, h-oval yellow-on-black),
  Z2 (right flow: W_v^(0) all-four-same superscript, chip borders q red/k green/v blue,
  container strips), Z3 (title: verbatim + colors + 20pt), Z4 (input rows: W_k^(0) all
  four, key boxes, two orange ellipses), Z5b (`"H" Heads` — literal double quotes,
  blue bold italic, ascending), Z6 (swoosh: uniform ~10pt stroke, top J-hook, long
  diagonal, bottom U-turn ending in a NE arrowhead at the h1 container).

## Closed-loop verification (pre-judge, mandatory)

- `house_chrome_check.py`: **PASS** (badge, panel, borders within tol 8).
- `closed_loop.py` (33 element checks, ~4px@150dpi tolerance): final state 21 OK; the
  residual OFFs are documented check artifacts, not build defects: plane soft alpha edge
  (9px on a 45%-translucent edge), title subscript descent (4px, LO drop metric),
  JPEG b-channel classification noise in the plane-dimmed pill zone (dotprod top 15px),
  AA-scatter at ellipse/arrow edges (green_ell, orange_zone, dots, chain_rust, swoosh
  3px), qrow border tone. Full log: `qa/slide015/closed_loop_final.txt`.
- LibreOffice pitfall found and fixed: `prst="line"` shapes with cx=0 (vertical arrows)
  render as huge misplaced bars in LO headless — all vertical arrows are thin rects +
  triangle heads (`varrow()` helper); horizontal 0-height lines render fine.
- Dense-region zoom comparisons (self-check #6, both banked):
  - `jcmp_fraction.txt` — attempt 1 FAIL (real bug caught: rotated pill labels read
    bottom-up vs the original's top-down; also bar tone); FIXED (ROTATE_270 + bar
    D86472 4pt + non-bold K·q label) → attempt 2 **PASS**
    (`jcmp_fraction2.txt`).
  - `jcmp_chips.txt` — **PASS** (0 major, 6 minor tint/typography nuances; labels,
    border order, counts, placements all match).

## Judge findings (MINOR, accepted — none are fix triggers)

1. W-box chip columns "offset" vs the original's arrangement — MINOR conf 0.8: PIL
   measurements place the columns within 1-2px of the frame's own chip positions
   (closed-loop chip_c1_q/chip_c5_q d≤2); judge variance at full-slide resolution.
2. Swoosh upper tip "extends slightly further right/up" — MINOR conf 0.7: the top crook
   was PIL-mapped from the frame's own red pixels (x to 827 matched, d=3 in the
   swoosh_band check).
3. ⊗ micro-placement — MINOR conf 0.6: mult_nodes check d=[0,0,0,0].
4. h=3 olive bar "hatched vs solid" — MINOR conf 0.7: the original's interior census is a
   solid olive fill (73..126 RGB channel spread = JPEG texture); reproduced solid.

## Attempts

1 closed-loop iteration cycle (6 render/check rounds inside attempt 1's build phase),
1 zoom-comparison retry (fraction zone), 1 judge attempt → PASS. No failed judge attempts.
