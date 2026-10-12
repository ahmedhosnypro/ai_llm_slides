# Worker report — slide 021 "Word Embedding" (CBOW vs Skip-Gram)

Video: `videos/deep-learning/001_transformers_part1` (Deep Learning DSAI 308, Transformers — Part I).
Deliverable: `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_021_recreated.pptx`
Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_021.js`

## Result

- **Attempts used: 1 of 6. Final verdict: PASS** (real comparison transcript, single-read,
  default route `images`, glm leg DEFERRED/BLOCKED).
- Judge procedure executed BY THE WORKER (no Agent/Task spawn tool in this environment —
  orchestrator-approved fallback per `scripts/17_worker_instructions.md` §7). The banked
  prompt `judge_prompt_1.txt` was executed byte-for-byte via Bash; the only mechanical
  deviation is the skill script path (`.agents/image-analysis/scripts/analyze_image.py`
  in the frozen template → actual `.agents/skills/image-analysis/scripts/analyze_image.py`;
  the template path does not exist on disk).
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
  `visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide021/judge_attempt_1.txt`.

## Evidence (all under recreated_pptx/qa/slide021/)

| File | What |
|---|---|
| `judge_prompt_1.txt` | banked substituted judge prompt (attempt 1) |
| `build_attempt_1.js` | verbatim build script copy for attempt 1 |
| `render_1.png` | 150 dpi render (2001×1125) |
| `probe_1.txt` | gateway window probe (valid analysis body — window open) |
| `judge_attempt_1.txt` | comparison winner body — **FINAL VERDICT: PASS** |
| `selfcheck_attempt_1.py` + `selfcheck_attempt_1_output.txt` | closed-loop PIL self-check (ALL PASS) |
| house chrome check | `HOUSE CHROME CHECK: PASS (panel x 89-1913, y 95-bottom; badge center (1860,148) d=70)` |

## Build basis

- Analysis spec `analysis/slide_021_final.json` (gate-passed PASS_WITH_FIXES, score 9);
  `validation.fixes` already baked into the spec's recreation_brief (three spaces before
  "vs", oval badge, cursor-exclusion region) — all applied. `[?]` items kept verbatim
  (summary line starts lowercase "a …" per frame; frame wins over tutorial's leading
  "While" per SOURCES.md).
- Geometry PIL-measured from `unique_slides/slide_021.jpg` (960×540, 1px = 1pt):
  blue box x69..879 y170..471 (white fill — interior sampled 255,255,255 vs panel
  E9E9E7 — 3333CC 1.5pt border); title ink y77..109 cx493 (Arial bold 35pt);
  subtitle ink y115..139 cx494 (Arial bold 26.5pt, three literal spaces before "vs");
  11-line body block, pitch pinned `lineSpacing: 22.4` (measured fit (425−201)/10),
  body Arial 20pt / headers Arial bold 19.5pt CC0000 (Arial advance-width fit:
  20pt matches all 7 body line ink widths within +2..+5px; 19pt was 25..55px short).
- Exact line wraps reproduced from word-blob measurement, including the original's
  hyphen-point break of "bag-of-" / "words" across P1 lines 2–3 (PowerPoint line-break
  opportunity after a hard hyphen — hand-broken to reproduce deterministically).
- Blue terms: original has 4 blue runs on P3L1 (96..211 "bag-of-words", 219..270 "model",
  709..794 "skip-gram", 802..854 "model"); P3L2 measured ZERO blue — recreation matches
  (blue only on the two terms, both ending line 1).
- House chrome via `shared_patterns/house_chrome.js` (`drawHouseChrome` numeral 21);
  ml-intro values never used.
- Mouse cursor over "not important" = recording artifact, omitted (spec region 6 +
  GROUND RULES (c)).

## Pre-judge self-checks (all banked)

1. Patterns index read; applied house-chrome + explicit-line-spacing (single knob,
   single-space spacer runs — empty-run pitfall). No equations/delimiters/tables/graphs
   on this slide, so the conditional crop-compare mandate did not trigger; the two
   "dense" candidates (three-space subtitle gap, hyphen wrap) were covered by PIL ink
   measurements (subtitle ink width matched within ~1px; wrap bands matched to ≤1px).
2. Frame containment: content ink min/max (frame px) x 68.2..880.3, y 78.7..472.3 —
   inside chrome bounds; text ink strictly inside the blue box (≥2px clearance all sides).
3. EQUATIONS: N/A (spec equations = []).
4. Delimiter geometry: N/A.
5. Table data: N/A.
6. Crop compare: not triggered (no equations/delimiters/tables).
7. Wrap check: exactly 9 text bands detected (no unintended wraps; cursor-free band set
   matches original's 9).
8. Explicit line spacing: pinned 22.4pt; rendered band pitch measured 22.4 ✓.
9. `house_chrome_check.py`: PASS.

## Judge findings (attempt 1)

- Verbatim text confirmed including all three wrap structures (headers, P1 3-line with
  "bag-of-/words" hyphen break, P3 2-line with "skip-gram model" ending line 1). Blue
  terms confirmed. Inter-line spacing, paragraph gaps, top-anchored left-aligned block,
  containment — all matched. Cursor omission confirmed correct per ground rule (c).
- Discrepancies: ONE MINOR (medium confidence): "bottom padding inside blue box slightly
  larger (~12–13% vs ~8%)". Not a fix trigger under the verdict law (PASS). Measured
  geometry contradicts a real deviation: last line band bottom 443.5 vs original 443
  frame px; box bottom 472.3 vs 471 — deltas ≤2 frame px, within the pipeline's ~4px
  closed-loop tolerance; the perceived difference is JPEG blur of the original's soft
  bottom rows.
- No BLOCKER/MAJOR, no visual-quality defects.

## Component banking

No banking obligation: `slide_dependencies.json` (001) has no child of 21, no pattern
group references 21, and `002_transformers_part2/slide_dependencies.json` contains no
`001_transformers_part1:21` qualified ref. Slide 21 is a root with zero dependents.

## Scratch note

`/tmp` is quota-blocked in this environment: all scratch (LibreOffice profile, PDFs,
self-check scripts) lived under
`videos/deep-learning/001_transformers_part1/scratch/slide021/` with `TMPDIR` pointed
there for both soffice and `scripts/16_vision_gate.sh`.
