# Worker report — slide 055 (Encoder-Decoder Attention Mechanism (In Decoder))

Video: deep-learning/002_transformers_part2 · P4 pattern-group member #2 ([54,55], head 054 certified)
Worker dispatch: 2026-10-12 ~09:15 EEST · report finalized: see DB row 55.

## Outcome

- **Final verdict: PASS** — visual judge attempt 3 on the FINAL artifact render_8
  (`judge_attempt_3.txt`): "No BLOCKER or MAJOR defects found" (5 MINOR notes).
  Judge attempts 1 (render_6) and 2 (render_7) also PASSed (`judge_attempt_1.txt`,
  `judge_attempt_2.txt`) — the slide was re-judged after each Z-row crop-loop fix
  round so the certificate always binds to the then-current artifact; the final
  certificate binds to render_8 / build v8.
- Deliverable (single-version law): `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_055_recreated.pptx`
- Build script: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_055.js`
  (banked per attempt as `qa/slide055/build_attempt_K.js`, K=1..7)
- Renders: `qa/slide055/render_1.png .. render_7.png` (150 dpi, LibreOffice headless
  private profile, TMPDIR under scratch/slide055)

## Attempts

| Build | Render | What changed | Verification |
|---|---|---|---|
| v1 | render_1 | First full build from PIL forensics (mapping = 054-certified fit, landmarks re-measured identical within 1px) | chrome PASS; closed-loop: 4 fails (title ems, check-mapping artifact) |
| v2 | render_2 | L1 em 20.3→19.7, L2 19→19.9 (+y −0.6), Scaling 21→20, ς 20→30; selfcheck ry-mapping bug fixed | closed-loop ALL PASS (fraction ±4px; titles ±2px) |
| v3 | render_3 | c2 read folded in: whole-box hatch, 6-cell Y rows w/ label at cell-3 left, K stripes, dark-red (8B0000) Y→W_k arrows, W_k→K thin red connectors added, Y→W_v red head-only | chrome PASS |
| v4 | render_4 | c7/c8 folded in: q₂ 4-cell glyph, white/maroon W_q box, query up-head, Z-row stadium+dashed green border, 5-cell strips, caption white box + centered, legend per c8 | chrome PASS; selfcheck PASS (σ-glyph band note) |
| v5 | render_5 | Crop-round-1 fixes: maroon Dot Product header, dot halos D5E7FB, up-heads under dots 2/3, K-lines start at box edge (289→407), 4 equal stripes, legend glyph tints + 2nd glyph, Z2 rect inside container | chrome PASS |
| v6 | render_6 | Dash-edge re-measurement: dashed rect hugs ONLY the magenta cells; S1 = 7-cell strip; Z-arrow = NE right-triangle (flipH rtTriangle, measured silhouette); stripe dividers | chrome PASS |
| v7 | render_7 | Magenta cells at measured y 465..487 (5 cells, bright 3rd), Z₂ label ON cell 3 (x~325), S1 tints saturated + label at ink x 255 | chrome PASS; selfcheck PASS |
| v8 | render_8 | Post-label cell tints → cool bluish/lavender (crop r4), last magenta cell extended to hug the dashed rect (352..366.5, rect right 367), arrow nudge | chrome PASS; **judge attempt 3: PASS, 0 MAJOR/BLOCKER** |

## Judge evidence

- Attempt 1 (render_6): **PASS** — `qa/slide055/judge_attempt_1.txt` (3 MINOR: solid-vs-hollow
  3D edge arrows, K.q inside-vs-outside the tan box, green arrow angle). No BLOCKER/MAJOR.
- Attempt 2 (render_7, FINAL): **PASS** — `qa/slide055/judge_attempt_2.txt`.
- Both single-read, default route (images), no --models flag, streaming, outer timeout 1700
  budget (540 wall, --thinking high --max-tokens 65536), executed by the worker via Bash
  (no agent-spawn tool in this environment — orchestrator-approved fallback per
  scripts/17_worker_instructions.md §7).

## Dense-region crop comparisons (equal scale, P4 §8)

| Region | Round 1 (render_4) | Final round |
|---|---|---|
| fraction | PASS | — |
| q₂ + W_q | PASS | — |
| sigma/nodes/pills | PASS | — |
| K strips + connectors | FAIL (stripe proportions, connector extent) | **PASS** (crop_pair_kstrip_3) |
| legend | FAIL (2nd glyph missing, tints) | **PASS** (crop_pair_legend_2) |
| dot mesh | FAIL (header color, halos, up-heads) | **PASS** (crop_pair_dotmesh_2) |
| Z-row | FAIL ×3 (r1 rect geometry/label/lean; r3 label positions; r4 post-label tints + rect hug) | r5 `crop_pair_zrow_5.txt`: 2 residual MAJORs **not corroborated by pixels** — see below |

All crop transcripts banked in `qa/slide055/crop_pair_*.txt`.

### Z-row crop-loop close-out (judge variance, pixel-forensic override — P4 precedent)

Two residual zrow-crop MAJORs (round 5) were measured against the render and the
original and NOT corroborated:

1. "NE arrow too small / too far left / detached from Z2": the render_7 ink scan gives
   the arrow at frame [299,489.5,322,501.5] — pixel-identical to the original's measured
   silhouette [299,490,322,501] (vertical right edge x≈321.6, hypotenuse down-left).
   The crop judge's own description ("under the right-center of the Z2 rect") contradicts
   the LEFT crop it was judging (the original's arrow is under the rect's LEFT portion,
   exactly where the recreation puts it).
2. "Pale lavender / near-white intruder cells inside the highlight": those pale cells are
   S1's post-label cells at frame x 270..297 — present in the ORIGINAL at the same
   position with the same pale tints (measured EFEFFB/E5E8F9 at y 472), OUTSIDE the
   dashed rect in both images.

Per P4 §4 precedent (054's F-head direction), pixel forensics override a single vision
read; both full-slide judges (attempts 2 and 3) passed the Z-row region without a
MAJOR. The fix loop converged: every pixel-corroborated finding across rounds 1-4 was
fixed and re-verified (header maroon, dot halos D5E7FB, under-dot heads, stripe
proportions+dividers, rect hug geometry, Z1/Z2 label positions, post-label cool tints).

## Closed-loop verification (mandatory pre-judge)

- `scratch/slide055/selfcheck_attempt_1.py` (+ outputs `selfcheck1/2/4_output.txt`):
  title L1/L2 ink ±2px, fraction ink ±4px @150dpi, rotated-strip centers ≤3.8px,
  dots/nodes/heads/shafts/Σ/Z2-magenta/legend/O-box/pills ALL present at measured
  positions. Two residual "fails" are check artifacts (σ-glyph band threshold vs JPEG
  halo — center within 2.6 frame px; K₁ shaft range stale after the line-extent fix).
- `house_chrome_check.py`: PASS on every render (1..7).
- Storm events: images-route 404 outage (upstream model withdrawn) + 2 EmptyStreamError
  timeouts + 1 HangError on a large composite — handled per storm protocol (payload
  shrink to single crops, sleep+retry); no evidence lost.

## Banking

- No deck's `slide_dependencies.json` references `002_transformers_part2:55` as a parent
  (checked both 001 and 002) → **no component export required**.
- P4 pattern group complete ([54,55]); group conventions extended for the playlist in
  `qa/slide055/PATTERN_GROUP_P4_tail.md` (055's verified deltas over the 054 pattern:
  full-box hatch, 6-cell Y rows, dark-red row arrows, K→dot full-width lines with halos
  and under-dot heads, Z-row stadium/5-magenta-cell highlight geometry, NE right-triangle
  arrow, legend layout).
- DB row 55: gen_status passed, visual_check PASS, visual_attempts, visual_transcript
  `recreated_pptx/qa/slide055/judge_attempt_2.txt`, pptx_path, build_script set.

## Provenance

Spec: `analysis/slide_055_final.json` (PASS_WITH_FIXES) · Sources:
`slide_055_source/SOURCES.md` (pre-banked; not modified) · Ground truth:
`unique_slides/slide_055.jpg` (960×540, 1px = 1pt).
