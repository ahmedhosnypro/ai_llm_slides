# Worker report — slide 039 (Normalization), video deep-learning/002_transformers_part2

**RESUMED WORK.** A previous builder died in a provider storm mid-work. State found:
`build/slide_039.js` (9867 B, 23:13) + `slide_039_recreated.pptx` (23:13) built, full
measurement campaign banked in `scratch/slide039/` (m1–m8, closed_loop_a1/v2),
provenance banked (`slide_039_source/` — vision transcript + webverify; SOURCES.md was
left as `.tmp`, promoted to `SOURCES.md` this run — its references all verified on disk).
`qa/slide039/` was EMPTY (no renders, no judge transcripts) → resumed at the pre-judge
stage, judge attempt numbering starts at 1. DB row had been reset to `pending`.

## Resume verification

- Re-rendered the banked 23:13 pptx → render was **byte-identical** (md5) to the dead
  builder's last scratch render — the 23:13 "closed-loop corrected" edit had NOT changed
  rendered output, so `closed_loop_v2`'s BAD list (12 regions) still applied.
- Deps gate: slide 39 is `root`, in `buildable`. No dependents (no component-banking
  obligation; not in any pattern group).

## Closed-loop fix rounds (checker: `scratch/slide039/closed_loop_v3b.py`)

v3b measures RENDER and ORIGINAL with identical wide-then-tight windows + predicates and
self-derives targets from the original (m5/m6 cross-checked). v2's three checker bugs were
fixed: b1/b2 x-windows started at 95pt (clipping target ink at 84.7/83.6pt — their dx0
"errors" were artifacts), lc_trans y-window clipped the 'g' descender, underline scans hit
text rows instead of below-baseline rows; plus a `blackish` predicate (darkp catches pure
red borders), and windows excluding the pen-cursor blob and neighboring lines.

| Round | BAD count | Fixes applied |
|---|---|---|
| v3b_a1 (banked render) | 13 | — (baseline) |
| v3b_a2 | 3 | title 35→35.6 + up 1.16pt + center +0.79; quoteL1 22→22.2 + boxX +1.73; covshift charSpacing 0.77 + right +2.3 + up 1.32; f1l1/f1l2 14.5→14.75; conclusion charSpacing 0.55 + up 0.79; stmt1 18.5→18.4; stmt2 18.5→18.7; **lineC split into 3 verbatim run-boxes** at measured ink x (73.2/213.7/466.5; runs 2-3 had rendered ~3.5pt left as one box — inter-run gap metrics; shared baseline preserved via ascent-delta compensation); sumhead 18.5→18.7; b1 16.5→16.3 + up 1.0pt; b2 16.5→16.4 + up 0.6pt; **f2l2 color split** (below) |
| v3b_a3 | 1 | b1/b2 → 16.25 (b1 ✓; b2 overshot) |
| v3b_a4 (final = render_1.png) | **0** | b2 → 16.34 (interpolated) |

Final: all 20 line regions within 4px @150dpi (worst 3.5px); box edges −1..−3px;
`house_chrome_check.py` **PASS**; fills verified (flow FFFFCC, summary E0FFFF, quote/container white).
Self-check items: no equations/delimiters/tables on this slide (rules 3/4/5 n/a); every
text box is single-line (rule 8 n/a); containment via edge scans + window ink (rule 2 ✓);
dense-region crop vision comparison run (rule 6) — **PASS**, 3 MINOR stroke-weight notes,
and it independently CONFIRMED the f2l2 color split (`crop_flow_comparison_1.txt`).

## Frame-wins corrections (fidelity law; documented, evidence banked)

1. **f2l2 "of each layer change" is NOT all-red.** Pixel column-profile of the original
   (cores (1,2,0) black at frame cols 389–471; (107,16,13) red at 477–522):
   "of each layer " BLACK bold + "change" RED bold. The vision transcript/spec said
   "red" — a small-text color misread (same error class the dead builder corrected for
   the navy bullets). Build updated; crop comparison (vision model, 2x upscale)
   confirmed the split matches the original. Recorded in SOURCES.md.
2. **lineC run positions**: original run boundaries at slide x 73.2 / 213.7 / 466.5
   (m6 lineC_norm_red / lineC_transform_ink / lineC_zero_blue); one-box rendering
   drifted runs 2–3 left ~3.5pt → split into three verbatim run text boxes.

## Judge (attempt 1) — PASS

- Probe: hung once at the 150s wall (RC 124, no window) → sleep 300 → re-probe ONCE →
  valid body (`probe_1.txt`, validated winner, 0 degenerate events).
- Full comparison: `judge_attempt_1.txt` (default route `images`, `--thinking high
  --max-tokens 65536`, W4 wall 540/420s, rc=0) → **FINAL VERDICT: PASS for "faithful,
  usable recreation"**. Findings: 1 MINOR (flow box 1 inter-line gap, confidence 0.5) —
  closed-loop data contradicts it (f1l1/f1l2 ink edges within 2px, line pitch 33.5pt =
  original's exactly); documented as judge variance, not a fix trigger.
- Dense-region crop comparison: `crop_flow_comparison_1.txt` → PASS (MINOR: box border
  weight, arrow weight, box-3 right margin tightness — all stroke-weight/marginal).
- Certificate label: single-read, default route (images), glm leg DEFERRED/BLOCKED.
- **Judge procedure executed by the worker itself** (no Agent/Task spawn tool in this
  environment) — orchestrator-approved fallback per scripts/17_worker_instructions.md §7;
  prompts banked byte-for-byte (with the documented skill-path correction per the
  image-analysis SKILL.md 2026-10-11 amendment) in `judge_prompt_1.txt`.

## Deliverables

- `recreated_pptx/slide_039_recreated.pptx` (single-version, chrome numeral 39)
- `recreated_pptx/build/slide_039.js` (attempt-1 copy: `qa/slide039/build_attempt_1.js`)
- Evidence: `qa/slide039/{render_1.png, probe_1.txt, judge_prompt_1.txt,
  judge_attempt_1.txt, crop_flow_render_1.png, crop_flow_original.png,
  crop_flow_comparison_1.txt}` + `scratch/slide039/`
  (m1–m8 measurements, closed_loop_v3b.py + a1–a4 JSON outputs, LO profiles)
- Provenance: `slide_039_source/SOURCES.md` (+ `transcripts/`, webverify bank)

DB final: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=…/judge_attempt_1.txt`, `last_error=""`.

No equations on this slide → no mathtext/OMML pass. No advanced graphs → no graphgen.
