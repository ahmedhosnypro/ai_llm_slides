# Worker report — slide 038 (deep-learning/001_transformers_part1)

**Slide:** 38 — "Self Attention Mechanism (Adding Scaling)" + Figure-2-left inset
(child of 37; Deep Learning DSAI 308, Transformers — Part I)
**Attempts used:** 1 (judge attempt 1) — **Final verdict: PASS**
**Deliverable:** `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_038_recreated.pptx`
**Build script:** `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_038.js`
**Comparison transcript:** `recreated_pptx/qa/slide038/judge_attempt_1.txt`

## Resume note

This run resumed from a dead prior worker: the only banked state was three unrun
scratch measurement scripts (`scratch/slide038/m1_diff.py, m2_clusters.py, m3_zones.py`),
an empty `qa/slide038/`, no build script, no pptx, DB row at `gen_status=building`
with nothing else set. The run restarted from attempt 1 and executed everything.

## Dependency gate

`15_progress.py deps`: slide 38 `unblocked` (parent 37 `passed` + `PASS` in the same
DB). Build proceeded legally. Slide 38 has NO dependents in any video's dependency
graph (checked `001` and `002` edge lists — only `38 ← 37` exists), so the
playlist-scoped component-banking obligation does NOT trigger; no
`components/slide_038.js` was banked.

## Delta analysis (PIL-measured on unique_slides/slide_038.jpg; scratch/slide038/m1–m11)

1. **Inset (pure addition, verified):** green panel x[797..914] y[114..313] (#1D7136,
   ~2.25pt, white fill); five rounded boxes centered on x843.5 except the top MatMul
   (x[836..901], offset right, as drawn): MatMul #C3B9DB y[136..156], SoftMax #CEE6D0
   y[166..185], Mask (opt.) #D8B6C5 y[196..214], Scale #F5F9C0 y[225..243], MatMul
   #C3B9DB y[255..273]; thin black UP chain arrows (x843.5), output stub above the top
   MatMul (x868.5, y136→124), V bypass up the right side (x891.5, y296→157), Q/K arrows
   below the bottom MatMul, faint Q K V labels at y≈295. Stack reads top-down
   MatMul/SoftMax/Mask (opt.)/Scale/MatMul per the frame (SOURCES.md reading-order
   artifact — arrows flow bottom-up, NOT "fixed").
2. **Scaling box y-shift (inherited block at child geometry):** the yellow Scaling box
   sits 8px lower in slide 38's frame than in 37's (yellow run y[186..419] vs
   y[178..411], x identical) while the K.q/√d fraction and the rotated label ink are at
   the SAME absolute positions in both frames. Per the child law (frame = ground truth),
   the parent's `scaling` block is skipped via `opts.skip` and redrawn: outer rect
   y185 h228, inner rect y191 h217 (+8); fraction images/bar and rotated label keep the
   parent's measured-identical placements.
3. **Rotated label rendering:** the certified parent renders "Scaling by √d" wrapped
   into two short columns (ink y[272..309]); BOTH original frames (37 and 38) show ONE
   unwrapped top-to-bottom line (ink y[240..359], x[386..401]). Since this block is
   already the child's redrawn delta, the label is rendered as the frame shows
   (pre-rotation 130×16 box centered (393.5,299.5), rotate 90, 16pt bold, charSpacing
   1.5) — closed-loop verified to ≤0.9 frame px on all four ink edges (m11 +
   `selfcheck_final_1.txt`). The parent component itself was never touched (cascade law).
4. **Cursors:** 37's frame has a cursor in the subtitle area, 38's frame near the lowest
   W_v box (x[690..740] y[355..405] — matches the spec's artifact note). Both omitted
   per judge ground rule (c).
5. Badge numeral 38 via `components/house_chrome.js` (drawn once).

## Pre-judge self-checks (all banked in qa/slide038/)

- `house_chrome_check_1.txt`: **PASS** (panel x89–1913, badge center (1860,148) d70, tol 8).
- `selfcheck_attempt_1.txt` / `selfcheck_final_1.txt` — **inheritance diff vs the
  parent's certified render (`qa/slide037/render_1.png`): 0 pixels outside the declared
  delta zones** (badge / inset / scaling-box); inset delta bbox fully inside panel+6px
  (containment); inset box border bands match the frame within ~1px; fraction bar rows
  427–430 (150dpi) IDENTICAL to the certified parent's; Scaling yellow run y[185.3..412.3]
  frame-equivalent vs frame [186..419] (bottom halo ≈ the certified parent's own
  relationship to its frame).
- Crop comparisons through the gate (3× same-scale crops, `judge_crop_p.txt` template):
  - `cropcmp_inset.txt` — **FINAL VERDICT: PASS** (5 MINORs: font weight, saturation,
    dash styling, arrowhead style, one gap at crop-artifact level).
  - `cropcmp_scaletop.txt` — **FINAL VERDICT: PASS** after the label fix (8
    MINOR/NEGLIGIBLE; arrow-tip gaps / K.q font / pill borders are INHERITED-region
    variances — pixel-identical to the certified parent, documented override per the
    W5-inheritance law).
  - Gate anomalies encountered: repeated transient `EmptyStreamError` (empty content,
    no deltas) on several calls — worked around by re-invocation; one earlier
    `cropcmp_scaletop` read truncated at the wall (superseded by the complete PASS
    read banked above). All evidence is from completed winner bodies.

## Judge (attempt 1)

- Banked: `judge_prompt_1.txt` (frozen `-p` template verbatim, NNN=038/K=1 substituted),
  `build_attempt_1.js`, `render_1.png`. Judge procedure executed by the worker (no
  subagent spawn tool in this environment — orchestrator-approved fallback per 17 §7).
- Probe: the gateway window entered a transient empty/slow phase; two probe calls
  empty-streamed and one hit the wall without a transcript. The comparison (the
  evidentiary call) landed on invocation.
- Comparison (`--thinking high --max-tokens 65536`, W4 wall): **FINAL VERDICT: PASS** —
  no MAJOR/BLOCKER, no missing elements, no containment violations. Judge MINORs:
  D1 ⊗ circle-X vs the original's circle-asterisk glyph (same as the parent's certified
  MINOR; glyph style only), D2 inset occludes the right stack's upper labels (present in
  BOTH images — inherited from the original), D3 faint dashed connector at video
  resolution (low confidence, possibly a compression artifact). Judge accepted the
  declared scaling-box shift and the imported base.

## Verdict law

PASS backed by a real comparison transcript → DB: `visual_check=PASS`,
`visual_attempts=1`, `visual_transcript=qa/slide038/judge_attempt_1.txt`,
`gen_status=passed`. No OMML wrap (PNG-only equation mechanism, deck-consistent);
single-version deliverable only.
