# Worker report — 002_transformers_part2 slide 004 "Encoder – Decoder Transformer"

**Final verdict: PASS** (attempt 1 of up to 6). DB row: `gen_status=passed`,
`visual_check=PASS`, `visual_attempts=1`.

## Deliverable

- PPTX: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_004_recreated.pptx`
- Build script: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_004.js`
  (banked copy: `qa/slide004/build_attempt_1.js`)
- Render (150 dpi): `qa/slide004/render_1.png`

## Resume note

Two prior attempts died on provider errors before banking anything (DB had
`gen_status=building`, empty `qa/slide004/`, no pptx). This run resumed from their
scratch evidence (`scratch/slide004/`): reused the banked base render
(`base-1.png` = imported 001:15 component with numeral 4) and the measurement
scripts (diff1/m1–m3), then added m4–m8 (robust borders-based affine fit,
highlight geometry, overlay-color fit, structure maps). Attempt numbering starts
at 1 (no prior renders/transcripts existed).

## GRAPH-EDGE MISMATCH (pending founder amendment — do not propagate)

The registered edge `4 ← 001:15 AND 001:18` is a MISMATCH per the dependency audit
(`scratch/dependency_audit_findings.md` §B, final list item 6): 002:4's real
composition parent is **001:15**; 001:18 contributes only the orange-highlight
motif. The founder has NOT ruled on the amendment. **Built per audit evidence:**
composition imported from 001:15's certified component
(`/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_015.js`,
absolute path, `renderBase(pptx, slide, {numeral: 4})`); the highlights are drawn
as 002:4's own measured delta. The `slide_dependencies.json` edge itself was NOT
modified (graph is founder-owned).

## Delta (PIL-measured from `unique_slides/slide_004.jpg`, 960×540, 1px=1pt)

Robust frame→slide fit from chrome border landmarks + badge
(scratch/slide004/m5–m8; base render vs 001:15's certified render: **max diff 0
outside the badge** — pixel-exact inheritance):

1. Badge numeral 4 (chrome, via `renderBase` opts).
2. Two semi-transparent orange highlight rects (frame orange-mask, >80%-density
   edges over box-free bands):
   - encoder-side: slide pt x 582.3..735.3, y 356.5..405.2 (153.0×48.7)
   - decoder-side: slide pt x 737.3..885.1, y 278.0..325.1 (147.8×47.1)
   - fill `E76B00` @ transparency 50 — fitted overlay color (m8, 7 purity-screened
     patches, model obs = α·C+(1−α)·bg, rms 5.3); the spec's estimated
     `F7A94F`@50% is measurably too pale against the frame (rms 30). Frame wins.
   - the two rects stop ~2pt short of each other at the Encoder/Decoder zone
     boundary and ~7pt inside the zone outer edges — as measured.
3. **No palette drift drawn**: cell-median tint census (m7) shows the frame's zone
   fills EQUAL the certified asset's (peach FDEDDD, mint CEFFE1) — residual tint
   is video-capture/JPEG only, covered by the judge's sanctioned palette-drift
   clause.

No equations (no OMML pass), no tables, no text boxes in the delta.

## Pre-judge self-checks (all PASS, banked)

- `house_chrome_check.py` → **PASS** (panel x 89–1913, y 95–bottom; badge center
  (1860,148) d=70; tol 8).
- `qa/slide004/selfcheck_attempt_1.py`:
  - Inheritance diff vs imported base render: 62,722 hot px, **0 outside the
    delta zones** (two highlight rects + badge numeral) — confined as required.
  - Highlight geometry in render: enc edges d=(0,1,0,−1) px, dec d=(0,0,0,−1) px
    vs measured (≤4 px tolerance) — PASS.
  - Containment: both rects fully inside the green card interior — PASS.
- Crop vision comparison (gate, `cropcheck_attempt_1.txt`): flagged
  "(shifted right)" caption and an up-arrow "clipped" — PIL verified both are
  fully present in the full render (caption ink rows 1020–1093, up1 red rows
  1020–1066); they were artifacts of the crop window (bottom cut at y=1064),
  not build defects. The model also confirmed the mouse-cursor artifact is
  correctly omitted.

## Judge (attempt 1)

- Frozen prompt banked: `qa/slide004/judge_prompt_1.txt` + `judge_p_1.txt` (-p
  byte-identical to the 17 §Judge template; --view carries the shared-base fact:
  "base = 001 slide 15's certified component (imported cross-video per audit
  evidence); expected difference = orange highlight rects + badge + palette drift").
- **No Agent/Task spawn tool available in this environment — judge procedure
  executed by the worker itself per 17 §7 fallback (orchestrator-approved).**
- Probe: `qa/slide004/probe_1.txt` (valid body, window opened).
- Comparison: `qa/slide004/judge_attempt_1.txt` — default route (images),
  `--thinking high --max-tokens 65536`, W4 wall 540s, single read; glm leg
  DEFERRED/BLOCKED. Winner body ends:
  **"FINAL VERDICT: PASS for 'faithful, usable recreation'."**
- Findings (all MINOR, no BLOCKER/MAJOR):
  1. Decoder "Output Embedding" fill green-tinted vs original pink; decoder "Feed
     Forward" hue greener than original's blue — MINOR, "sanctioned palette drift
     per brief". These are inherited 001:15 certified pixels (0-diff proven) →
     judge variance per the inheritance law, not fix triggers.
  2. Top red up-arrow "partially clipped blob" / 3. bottom arrow "tighter to
     'Inputs'" — MINOR; the arrows are inherited certified blocks (up1/up2 from
     001:15's component; 0-diff vs its certified render) → judge variance,
     documented and overridden per 17 §dependency rule 5.
  4. Right-panel fills "slightly more saturated/green-shifted" — MINOR, expected
     palette drift.
- The orange highlights: "Positions, extents, and overlap behavior match the
  original. These are the sanctioned additions."

## Attempts used

1 of 6. First-judge PASS.

## Evidence index

- `qa/slide004/render_1.png`, `build_attempt_1.js`, `judge_prompt_1.txt`,
  `judge_p_1.txt`, `probe_1.txt`, `judge_attempt_1.txt`,
  `cropcheck_attempt_1.txt`, `crop_right_render_1.png`, `crop_right_frame.png`,
  `selfcheck_attempt_1.py`
- Measurements: `scratch/slide004/` (m4–m8 scripts + outputs, fit4.npy,
  frame_warped4.png, prior attempt's base-1.png/render_base.js — reused)
- Progress DB: VIDEO=deep-learning/002_transformers_part2, slide 4 → passed/PASS
