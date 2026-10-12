# Worker report — slide 024 (002_transformers_part2, "Suggested Positional Encoders / (Rules Controlling Good Positional Encoder)")

## Result

- **Final verdict: PASS** (attempt 1) — real visual-judge comparison, `FINAL VERDICT: PASS` for
  'faithful, usable recreation'.
- Deliverable (single version): `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_024_recreated.pptx`
- Build script: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_024.js`
  (banked copy: `qa/slide024/build_attempt_1.js`)
- Comparison transcript: `videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide024/judge_attempt_1.txt`
- Judge prompt (frozen template + substituted values + shared-base fact in --view):
  `qa/slide024/judge_prompt_1.txt`
- Attempts used: 1 of 6 (render_1.png; judge comparison landed on the first invocation after
  gate-window saturation cleared).
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_transcript=<above>`, `visual_attempts=1`.

## Build law compliance (dependency-gated child 24 ← 23)

- `15_progress.py deps` showed slide 24 `unblocked` (parent 23 `passed`+`PASS`) before building.
- The certified parent component
  `recreated_pptx/build/components/slide_023.js` is **imported** (`require` by absolute path),
  `renderBase(pres, proxy, { numeral: 24 })` — never re-drawn, never edited.
- The banked component is monolithic (only `opts.numeral`; no `opts.skip`), so the two replaced
  parent blocks were suppressed through a **filtering slide proxy** (001 slide_009 precedent:
  the certified drawing code stays the single source of truth). The proxy drops exactly 7 texts
  + 4 shapes (parent subtitle text, cyan problems box, its 6 texts, 3 bullet-dot ellipses);
  every drop is logged by the build (console output) and asserted (7 texts / 4 shapes, fail-loud).
- Delta drawn only at THIS frame's measured geometry (see below). PIL diff frame24-vs-frame23
  (`scratch/slide024/diff_frames.py`) proved the delta is confined to the subtitle band (fy
  82..106) and the bottom-box band (fy 366..491); both frames share the same chrome landmarks
  (L58/R901/T43/B516 → fx = 17.628 + 0.961231·slide_x — identical to slide_023's mapping).
- Parity check (`qa/slide024/selfcheck_attempt_1.py`, part B): the final render diffed against a
  numeral-24 render of the certified parent component differs ONLY inside the two designed delta
  regions (slide y 84.5..111.8 and 362.9..526.1) — every inherited region is pixel-identical to
  the certified composition.

## Measured delta (all PIL on unique_slides/slide_024.jpg; scripts in scratch/slide024/)

- Subtitle "(Rules Controlling Good Positional Encoder)": Arial bold 22pt #0000CC in the parent's
  subtitle box (x 85.9pt, y 84.5pt, w 12.13in, centered), #FFFF00 highlight strip measured
  x 294.8..752.5, y 84.8..112.0 (frame's strip is genuinely narrower than its text — reproduced).
- Rules box: roundRect x 58.7..902.9, y 365.2..525.3 (stroke cores at frame cols 73/886, rows
  349/502 — same strokes as slide 23's box), fill #FFFFCC, border #0066CC 1.5pt (border-row
  census matches the certified parent's 0066CC).
- Six rule lines, uniform baseline pitch ≈23 (== parent's certified lineSpacing 23), per-line
  sizes fitted by fontTools width+height fits (Arial italic family): L1 17.75 (with the frame's
  measured ~15pt gap after "[1]" = 3 spaces), L2 17.75, L3 17.75, L4 17.75, L5 17.5, L6 17.75.
  Emphasis measured via word-run color masks + ink-coverage (bold ≈0.50-0.56 vs regular
  ≈0.39-0.43): red bold leads "[1] δ value" / "[2] Range of position encoded values" /
  "[3] Position Encoding  should be a  VECTOR" (#CC0000, census matches parent's red-text
  family), blue bold "should be same" / "should NOT depend on sequence length" /
  "same dimension as Word Embedding", everything else blue regular (#0000CC).
- Underlines drawn as explicit measured rectangles (frame rows 401-402 / 466-467 → slide y
  419.7..421.8 and 487.7..489.8, 2.1pt thick, #0000CC): "(same positions" (x 99.0..221.5),
  "same values" (x 391.5..489.5), "same dimension as Word Embedding" (x 594.0..897.5 — the
  underline spans the whole tail phrase, continuous through word gaps in the frame's underline
  bins; resolves the spec's [?] on 'Word Embedding'). LO's built-in text underline rendered
  1.7pt lower than the original and its offset is not controllable — rects reproduce the
  measured position/thickness exactly (closed-loop verified ≤0.9px).
- Verbatim fidelity: "form -1 to 1" typo kept; double spaces after "range", "Encoding", "a",
  "easily" kept. Video-player black bar and cursor omitted (capture artifacts).

## Closed-loop self-check (attempt 1; `qa/slide024/selfcheck_attempt_1.py` + output)

All PASS: house chrome check (shared_patterns/house_chrome_check.py), subtitle strip/ink bands,
rules-box border/fill (fill census exactly 255,255,204), six line bands (tops/bottoms/lefts
≤1.9px @150dpi), underlines ≤0.9px, parity (diff confined to the two delta regions).
Documented residuals (right-edge only, at the JPEG-bloom measurement floor, ≤0.65% of line
width): L3 −3.9pt, L4 +2.1pt, L5 +2.1pt vs the raw frame's ink extents.

## Judge (attempt 1)

- Gate window was saturated: 4 probe attempts (150s wall) + 3×300s storm sleeps all hung; the
  comparison itself then LANDED on the first invocation (W4 540s wall, `--thinking high
  --max-tokens 65536 --timeout 420 --rounds 1 --tries 1`).
- Judge procedure executed by the worker (no agent-spawn tool in this environment) —
  orchestrator-approved fallback, byte-for-byte per the banked prompt.
- **FINAL VERDICT: PASS.** Zero BLOCKER/MAJOR. Three MINOR findings — (1) ellipsis dots
  marginally larger, (2) orange triangles ~1-2px lower, (3) "+δ" labels slightly larger — all in
  INHERITED regions whose parity with the certified slide-023 render was proven; per the
  dependency law these are judge variance, documented and overridden (not fix triggers). No
  findings on this slide's delta regions.
- Certificate label: single-read, default route (images), glm leg DEFERRED/BLOCKED.

## Notes

- Slide 24 has NO dependents in any video's dependency graph (checked `deps` + edges list), so
  no component banking obligation applies to 24. Parent 23's component remains frozen/untouched.
- The banked `components/slide_023.js` was not modified (cascade law respected).
