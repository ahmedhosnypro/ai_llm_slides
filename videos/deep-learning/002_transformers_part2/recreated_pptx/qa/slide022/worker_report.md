# Worker report — slide 022 "Suggested Positional Encoders" (002_transformers_part2, P2#3)

**Final verdict: PASS** (judge attempt 2, real comparison transcript, coherent winner body).
**Deliverable:** `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_022_recreated.pptx`
**Build:** `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_022.js`
**Comparison transcript of record:** `qa/slide022/judge_attempt_2.txt` (DB `visual_transcript`).

## Special circumstances (read this first)

1. **Duplicate dispatch + resume.** A concurrent worker had been dispatched on the same
   slide (its artifacts at 09:05–10:06: measure scripts, build script, pptx, render_1,
   selfchecks 1–3, 4x crops; it called an even-earlier builder "dead"). It stalled after
   10:30 (24+ min, no live process, DB untouched since 10:17). I resumed per the resume
   law from its state at 10:46: reused its build as `build_attempt_1.js` (banked), kept
   all its evidence, continued render numbering from render_2. My own parallel
   measurement set (scratch/slide022/measure1..18, 09:23–09:51) was used to audit its
   build. Verdict: its structure was CORRECT (including the +δ/arrows reading I initially
   disputed — pixel-run re-measurement proved its δ-text centers 226.5/296/378/453/525/793.5
   right and my first eyeball read wrong).
2. **Attempt-3 regression (self-inflicted):** my calibration edit accidentally dropped row
   3's `drawLane` call; judge attempt 1 correctly failed it as MAJOR ("missing dashed
   container on the Position Index strip"). Restored verbatim in attempt 4. Diff your
   drawLane calls after refactoring (lesson banked in p2_member_notes_022.js).

## Attempts (judge attempts; renders = build iterations)

| K | Render | Build | Outcome |
|---|--------|-------|---------|
| (pre) | render_1 (prior worker) | build_attempt_1.js | chrome PASS; their selfchecks showed typography widths off |
| (pre) | render_2 | build_attempt_2.js | my calibration: per-element em corrections from render-vs-original ink spans (ratios → ~1.00) |
| (pre) | render_3 | build_attempt_3.js | all width ratios ≤3.5%; selfcheck 5 ink/spacing/containment OK — **but row-3 drawLane accidentally deleted in the edit** |
| 1 | render_3 | — | **FAIL** — 1 MAJOR (missing dashed container on strip 3; judge transcript `judge_attempt_1.txt`) + 4 MINORs (straight-vs-curved arrows; subscript vs inline N-2/N-1; δ styling; "Last position" case) |
| 2 | render_4 | build_attempt_4.js | **PASS** — 0 BLOCKER/MAJOR; 4 MINORs (+δ slightly large/dark; arrow anchor point; index digits slightly large/bold; gray dots slightly large — all sub-tolerance) |

Judge procedure executed BY THE WORKER (no Agent/Task tool in this environment —
orchestrator-approved self-execution fallback per scripts/17_worker_instructions.md §7):
probe (`probe_K.txt`) + comparison (`judge_attempt_K.txt`) through
`scripts/16_vision_gate.sh`, frozen `-p` template verbatim (banked as
`judge_prompt_K.txt`), `--thinking high --max-tokens 65536`, W4 wall. Note: the gate's
`.agents/image-analysis/...` path in the frozen prompt had to be corrected to
`.agents/skills/image-analysis/...` (fleet-actual path) and the probe needed an explicit
`-p` (this fleet's analyze_image.py requires it); one EmptyStreamError window (11:45)
was ridden out with the mandated sleep-300-and-re-probe-once before the window opened.

## Pre-judge self-checks (mandatory list)

- **Chrome:** `house_chrome_check.py` PASS on render_1/2/3/4.
- **Mapping:** this frame's four chrome landmarks → ax=17.753, sx=0.962235, sy=0.955556;
  badge cross-check (891.6,73.1) vs house (893,71) — same 1–4px class as certified 020/021.
- **Closed-loop widths** (`selfcheck_attempt_4/5/6` outputs + inline scans): title 1.005,
  subtitle 0.996, summary l1a 1.035 / l1b 1.000, Problems 0.996, b1a 1.002, b2 0.976,
  b3 0.973, lab1 0.984, lab2 0.964, lab3 0.991, r1 box 1.022, r2 box 1.007 (all vs
  original ink spans; r3 digit left at 17% narrow — sub-tolerance, judge-passed).
- **Ink presence:** all 21 regions non-empty (no equation/box/panel empty). Labels inside
  boxes; bullet pitch 46–48px vs pinned 22.7pt (explicit lineSpacing everywhere).
- **Containment:** all content inside the navy panels + chrome (the naive full-ink bbox
  touches the chrome strokes themselves, which are the chrome's own ink).
- **Dense regions:** the +δ band was settled by pixel runs (two distinct bands: 6 orange
  marks at y290–305 on the lane's bottom dash + 6 "+δ" maroon glyphs at y315–328 below
  the lane, at measured centers); a 4-image vision probe of that band was attempted
  twice through the gate and failed with persistent upstream EmptyStreamError — the
  judge's full + probe scrutiny covered the region instead (judge attempt 2 explicitly
  verified "6 arrows and 6 +δ in both, same positions").
- **P2 pattern verification:** convention mirrored from certified 020/021 (chrome import,
  per-frame mapping fit, dashed lanes, cap-pinned text, closed loop); verified shared-block
  consistency via the same chrome checker on 020/021/022 renders. NO component import
  (022's composition — three labeled strips + cyan problems panel — is not shared with
  020/021). Group-shared pattern notes banked as `qa/slide022/p2_member_notes_022.js`
  for P2#4 (slide 034).

## Spec-vs-frame reconciliations (frame wins; recorded)

- Ellipsis dots: 5 per row (spec uncertain "5-6", standardized 6 — frame says 5).
- Row-1 container fill gray E8E8E8 (spec "pale yellow" = box fill misread); row-2 boxes
  transparent on lavender (spec "white" misread); row-3 lane fill F8E9ED (spec FFB3B3 off).
- Summary line1a = "Use δ = 1" (spaced, italic; spec normalized "δ=1"; frame ink x80–146).
- "(Depends on Seq. Length)" NOT underlined (spec/underline claim = misread; no run at
  y383-387). Judge confirmed the parenthetical matches as rendered.
- "Last Position Encoding" capital P per spec + judge read (worker-1 had lowercase — fixed).
- Spec's "six orange right-pointing arrows" between boxes: on THIS frame state the gaps
  are empty; the mark chain sits below the boxes — drawn at measured positions (judge
  verified "6 arrows and 6 +δ in both, same positions").
- N-2/N-1: inline same-baseline at 0.8em (measured + judge; not dropped subscripts).

## DB state (end)

gen_status=passed · visual_check=PASS · visual_attempts=2 ·
visual_transcript=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide022/judge_attempt_2.txt ·
pptx_path + build_script set. Component banking: not required — no slide in any video's
graph depends on 22 (slide 034 gates on the PATTERN, satisfied by this certification;
notes banked for it). SOURCES.md: pre-existing, verified (no changes needed; the
spec-divergence notes above are recorded here and in p2_member_notes_022.js).
