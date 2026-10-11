# Worker report — slide 017 "Encoder – Decoder Transformer" (deep-learning/001_transformers_part1)

**Worker:** per-slide build worker (slide 017 end-to-end). **Date:** 2026-10-11.
**Result: PASS on attempt 1** — judge comparison transcript
`judge_attempt_1.txt` (real comparison winner body, default route `images`, thinking=high,
max-tokens 65536, glm leg DEFERRED/BLOCKED per routing law).

## Deliverable

- `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_017_recreated.pptx`
  (SINGLE-VERSION law — one pptx, no suffixes; contains no equations/OMML/graphgen scope).
- Build script: `recreated_pptx/build/slide_017.js` (pptxgenjs, LAYOUT_WIDE, NODE_PATH
  global install; renders via LibreOffice headless with private profile in
  `scratch/slide017/lo_profile`, TMPDIR set to the slide scratch because /tmp is quota-blocked).
- **Banked component for dependents (18 ← 17, 19 ← 18):**
  `recreated_pptx/build/components/slide_017.js` — exports
  `renderBase(pptx, slide, opts)` with `opts.skip` / `opts.only` / `opts.chrome` /
  `opts.numeral` at BLOCK granularity. Block names: title, callout1..4, leader1..4,
  fig_frame, panels, panel_labels, yellow_band, enc_stack, enc_vkq, enc_pe, enc_embed,
  enc_base, enc_nx, dec_stack, dec_purple, dec_vkq_masked, dec_vkq_cross, dec_top,
  dec_spine, dec_pe, dec_embed, dec_base, dec_nx, green_trunk, feeds, feedback.
  Child 18 should skip `callout1..4` + `leader1..4` and draw its banners + Figure-2
  insets; child 19 composes on 18's component and replaces the banner blocks.
  House chrome drawn ONCE via `components/house_chrome.js` → playlist shared pattern
  `videos/deep-learning/shared_patterns/house_chrome.js`.

## Attempts

| K | Render | Verdict | Evidence |
|---|--------|---------|----------|
| 1 | `qa/slide017/render_1.png` | **PASS** (0 BLOCKER, 0 MAJOR, 5 MINOR) | `judge_attempt_1.txt` |

Judge MINOR findings (documented, non-fix-trigger): (1) decoder sub-layers rendered as
divided compartments of one rounded container vs visually distinct boxes; (2) PE icon
glyph shape nuance; (3) feedback arrow darker maroon vs brighter red, curve hugs panel
edge (still contained); (4) "Outputs" near-black vs original dark-red; (5) diagram scale
slightly larger vs panel whitespace — no containment violation.

## Pre-judge self-checks (all banked in `qa/slide017/`)

- `house_chrome_check.py`: **PASS** (panel x89–1913, badge (1860,148) d70 @150dpi, tol 8).
- `selfcheck_1.txt` / `selfcheck_2.txt` (PIL closed loop, render downscaled to 960×540
  and re-measured with the same masks used on the original): callout boxes pixel-exact
  (±2px), title red extent matched after 32→36pt fix, V/K/Q circle centers within 1px,
  panel fills exact modes, 0 ink pixels outside the white margin, all boxes contained.
- Structural vision probes through the gate (7 transcripts in `qa/slide017/`:
  `probe_enc/dec/gap/decbot/encbot/penc/decgap/opband.txt`) resolved the full Figure-1
  topology: encoder container (A&N/FF/A&N/MHA + residual curves + V/K/Q), decoder olive
  stack (A&N/FF/A&N/MHA), purple group (A&N + Masked MHA + V/K/Q + channel line),
  Linear/Softmax, OP band, PE nodes (⊕ + sine, both panels), N× badges, L-band yellow
  highlight, dashed feedback S-curve, green trunk line. Cross-checked against the paper's
  Figure 1 (arXiv 1706.03762v7, banked at `slide_18_source/`).
- Dense-region crop comparisons (attempt 1: `cmp_encbot_1/cmp_dectop_1/cmp_decbottom_1/cmp_gap_1`;
  fixes applied after them: purple-group sub-structure, rounded decoder container,
  red-arrow head into the Output chip, heavier dash-dot feedback ending at the Outputs
  chip, PE symbols enlarged, sub-layer separators + feed arrowheads, Softmax/Linear fill
  corrections, dec panel fill exact-mode) — attempt 2 re-comparisons banked as
  `cmp_dectop_2/cmp_decbottom_2`.

## Notes for children (18, 19)

- The certified geometry lives in `components/slide_017.js` only — never copy-paste it.
- `dec_purple` includes the purple group's inner A&N sub-box; if child 19's
  normalization callout targets that region, skip `dec_purple`'s text, not the container.
- The measured "N x" glyph is spaced (spec verbatim) even though some vision reads
  returned "N×" — SOURCES.md records this as per-frame course styling.
- Leader lines (callout→diagram, faint gray) are drawn at y151/245-254/364-379/492
  (measured); the spec marks them `[?]` optional — they ARE present in the frame.

## DB state

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide017/judge_attempt_1.txt`,
`pptx_path`, `build_script` set. Dependents: 18 unblocked (17 certified), 19 still
gated on 18.

## Process notes

- Judge procedure executed by the worker (no Agent/Task spawn tool in this
  environment) — orchestrator-approved fallback per 17 §7.
- /tmp quota-blocked: all scratch under
  `videos/deep-learning/001_transformers_part1/scratch/slide017/`; soffice ran with
  `-env:UserInstallation=file://<scratch>/lo_profile` and `TMPDIR=<scratch>` (also used
  for every `16_vision_gate.sh` invocation).
