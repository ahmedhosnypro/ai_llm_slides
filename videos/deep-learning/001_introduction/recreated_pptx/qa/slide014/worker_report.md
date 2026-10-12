# Worker report — slide 014, 001_introduction (Deep Learning DSAI 308)

**Date:** 2026-10-12. **Worker:** slide-recreation builder (fresh start, no prior artifacts).
**Final verdict: PASS (attempt 1 of the visual judge; 3 closed-loop build iterations before judging).**

## Deliverable

- PPTX (single version, no suffix): `videos/deep-learning/001_introduction/recreated_pptx/slide_014_recreated.pptx`
- Build script: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_014.js`
  (playlist house chrome imported from `shared_patterns/house_chrome.js` — never re-drawn; badge numeral 14)

## Evidence banked under `qa/slide014/`

| File | What |
|---|---|
| `measure_original.py` … `measure_original7.py` | 7 PIL measurement passes over the ground-truth frame (960×540, 1px=1pt): full geometry, colors, text bands, arrows, borders |
| `render_1.png`, `render_2.png`, `render_3.png` | 150 dpi LO renders (judge saw render_3) |
| `build_attempt_1/2/3.js` | per-attempt build provenance |
| `selfcheck_attempt_1/2/3.py` + `_out.txt` | closed-loop PIL checks vs original measurements (scale ×2000/960, tol ~4px@150) |
| `house_chrome_check` output | PASS (panel x89–1913, badge center (1860,148) d=70, within tol 8) |
| `probe_1.txt` | gateway probe (valid analysis body) |
| `judge_prompt_1.txt` | FROZEN -p payload (certified slide_007 template, numeral '14' substituted) |
| `judge_attempt_1.txt` | the judge comparison transcript (winner body) |

## Build iterations (pre-judge closed loop)

1. **Attempt 1** (render_1): first full build. Self-check: 11 failures — title 24px narrow
   (27pt → too small), takeaway 6px short, darkred line1 x0 11px off, ice/yellow fill insets,
   arrow2 scan artifact, error_text 4px short.
2. **Attempt 2** (render_2): title 28pt + y73.5; takeaway box (42.5, 429.5); darkred 20.5pt /
   lineSpacing 22 / line3 17.5pt italic; "Error" 20.5pt; yellow 15pt. Self-check: 5 failures —
   darkred text block ~3px high inside its box (LO valign-middle), green_text 'g' descender
   artifact, ice/yellow fill-vs-border inset artifacts.
3. **Attempt 3** (render_3): darkred box split into fill-rect + separate text box shifted down
   2.5px, lineSpacing 22.5. Self-check: 5 residual "failures", ALL analyzed as measurement
   artifacts, not defects:
   - `green_text` y1 err 4.3px@150: the original's JPEG fades the 'g' descender below its
     is_whiteish threshold; the render correctly shows the full descender.
   - `darkred_box` y errs ≤4.4px@150: split-rect AA columns caught by the fill predicate
     where the original's JPEG AA reads differently; rect geometry is at the measured values.
   - `darkred_line1` x0 err 7.4px@150: the original's line-1 ink center sits 3.75px left of
     its box center (its own ink asymmetry; lines 2/3 are centered); recreation centers all
     lines per the box.
   - `ice_fill` / `yellow_fill` errs ≤8.9px@150: fill-to-border inset — the border checks PASS
     dead-on (≤0.8px); the original's JPEG fades fill pixels near its borders.
   Remaining real geometry all within ~4px@150 (title width 611 vs 614, takeaway 703 vs 707,
   all four arrows, L-frame, black bar, panel navy strokes, all node boxes, "Error" vertical text).

## Judge (attempt 1)

- Executed by the worker via Bash (no Agent/Task spawn tool in this environment — orchestrator-approved fallback, per 17_worker_instructions.md §7).
- Probe: `probe_1.txt` (valid body; gateway window opened).
- Comparison: through `scripts/16_vision_gate.sh` (TMPDIR pointed at the video-namespace
  scratch — /tmp quota blocked), inner `timeout 280`, `--thinking high --max-tokens 65536
  --timeout 270 --rounds 1 --tries 1`, `-p` payload sourced byte-for-byte from the banked
  `judge_prompt_1.txt` (FROZEN certified slide_007 template; sole substitution numeral '14').
- Winner body: coherent element-by-element fidelity check — all elements MATCH (title verbatim
  incl. space before "?"; 5 boxes + 4 arrows; 3-line stacks; rotated Error; verbatim double
  space in "error  (Loss Function)"; no frame-containment violations; no missing elements).
- Findings: 3 × MINOR (arrowheads slightly larger/more triangular than original's; marginally
  more vertical padding around the Classification Model text; container inner margin below the
  flowchart row slightly larger) — all "within tolerance"; no MAJOR, no BLOCKER.
- **FINAL VERDICT: PASS** for 'faithful, usable reproduction' — real comparison transcript
  `judge_attempt_1.txt` (3673 bytes, single-read, default route/images, glm leg deferred).
- Certificate labeling: single-read, default route (images); glm leg DEFERRED/BLOCKED.

## Spec deviations (documented, PIL-law precedence)

- **Spec said "block arrows" and 2 text lines in the Classification Model box; PIL showed four
  THIN line arrows (1–2px shafts + ~11.5×9.5px triangular heads) and THREE lines
  ("Classification" / "Model" / "(with  Model Parameters)").** PIL measurement wins; the judge
  confirmed the 3-line stack as a MATCH.
- **Spec colors corrected by PIL modal measurement:** darkred box 9F0000 (spec A50021), ice box
  E2FFFB (spec CCECFF), tan box F6DEC2 (spec F5DEB3) + a thin warm-gray border A69C90 the spec
  missed, yellow box FAFED9 (spec FFFFCC) + full navy border the spec missed, green 09863A,
  panel/borders navy 000080 (spec 0000FF), reds C00000 family.
- Spec's "gray #D9D9D9 background" + per-slide red frame lines at "~4% top / ~2% left": the
  original frame is white; the per-slide frame is the same L (top y42–44 x57–899, left x57–59
  y42–517) as certified slide_007 (identical darkest-core pixels (106,45,53)); playlist chrome
  overrides the background per founder directive 2026-10-11.
- Gray cursor icon below the ice box: recording artifact — omitted (spec step 16 optional;
  certified slide_007 precedent; judge ground rule (c)).

## DB state (slides_progress.db, VIDEO=deep-learning/001_introduction)

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`, `visual_transcript=
videos/deep-learning/001_introduction/recreated_pptx/qa/slide014/judge_attempt_1.txt`,
`pptx_path` + `build_script` set, `last_error=null`.

## Component banking

No banking obligation: no same-video dependents (edges 16←9, 17←16, 18←9, 19←9, 25←24, 37←36,
41←35) and no cross-video references to `001_introduction:14` (checked 002_transformers_part2's
slide_dependencies.json). Slide 14 is a root slide with an empty `depends_on`.
