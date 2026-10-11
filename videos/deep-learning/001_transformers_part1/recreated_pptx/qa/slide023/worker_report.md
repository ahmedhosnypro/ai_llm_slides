# Worker report — slide 023 "Review: Cosine Similarity" (001_transformers_part1)

**Final verdict: PASS** (visual judge attempt 1, real comparison transcript, no
degenerate body). **Attempts used: 1 judge attempt** (pre-judge self-check iterations
before the first judge dispatch are not judge attempts; renders banked as render_1.png
and render_2.png).

## Deliverable

- `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_023_recreated.pptx`
  (single-version, no suffix)
- Build: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_023.js`
  (pptxgenjs; NODE_PATH=$(npm root -g) node, run from the project root)
- Judgment render (150 dpi): `recreated_pptx/qa/slide023/render_2.png`
- Comparison transcript: `recreated_pptx/qa/slide023/judge_attempt_1.txt`
  — coherent element-by-element body, 3 MINOR findings, zero BLOCKER/MAJOR,
  `FINAL VERDICT: PASS for 'faithful, usable recreation'`
- Judge prompt banked: `qa/slide023/judge_prompt_1.txt` + `qa/slide023/judge_p_1.txt`
  (the -p template with NNN=023/K=1 substituted; ground rule (a) carries the
  PLAYLIST chrome values per videos/deep-learning/AGENTS.md founder directive
  2026-10-11 — the ml-intro chrome values quoted in the frozen template are
  superseded for this playlist; all other clauses verbatim)
- Build provenance: `qa/slide023/build_attempt_1.js`

## Chrome (playlist law)

`drawHouseChrome` from `videos/deep-learning/shared_patterns/house_chrome.js` is the
only chrome source (white FFFFFF canvas, gray E9E9E7 panel x42..918 / y45..bottom,
thin C00000 border, badge FDFD96 d36 at (893,71) with 6A5ACD ring, bold 333333
numeral "23"). One deliberate deviation in HOW it is called: the panel is drawn via
`drawHouseChrome(pres, s, {numeral: ""})` at the start and the badge is re-emitted
after the content (badge branch of the module, verbatim CHROME constants) — because
this slide's top-right equations box (measured top y80) underlaps the playlist badge
(bottom y89), and the original frame layers the badge OVER the box corner.
`house_chrome_check.py` on the final render: **PASS** (panel x 89-1913, y 95-bottom;
badge center (1860,148) d=70 @150dpi).

## Pre-judge self-checks (all banked in `qa/slide023/selfcheck_attempt_1.txt`)

46/46 PASS on render_2: panel containment, 6 equation ink bands vs the original's
measured bands (±1-8px@150dpi), title band, 24 box-border edges, 2 circle fills,
4 vector segments, 4 axis segments, 2 θ ink regions, callout 3-line pitch 20pt +
width, cyan-bar 2-line pitch 22pt + widths, `a:lnSpc spcPts` XML pins (2000/2200),
Normalize-arrow outline + text center, max/loss text bands. Equations exist (no
empty region), no tables on this slide, no multi-line delimiters beyond the single-line
|bars| inside the equation PNGs.

## Dense-region crop comparisons (mandatory pre-judge item 6; all banked)

Round 1 found real fix triggers; after fixes ALL SIX regions MATCH
(`qa/slide023/crop2_*.txt`, `crop4_theta.txt`):

| Region | Round 1 | Round 2/3 (after fixes) |
|---|---|---|
| treq_eq (top-right fractions) | MISMATCH | **MATCH** (crop2) |
| bceq_eq (dot-product/cos box) | MATCH | MATCH |
| aftnorm | MISMATCH | **MATCH** (crop2) |
| callout | MISMATCH | **MATCH** (crop2) |
| cyanbar | MISMATCH | **MATCH** (crop2) |
| theta | MISMATCH | MISMATCH → **MATCH** (crop4, STIX θ PNG) |

Fixes applied from the crop findings (frame = ground truth over the spec's
typography guesses):

1. `Normalized` in the top-right equations rendered ITALIC (`\mathit`, was upright).
2. eq_unit gained underlined vector letters: `|\underline{a}| = |\underline{b}| = 1`.
3. `After Normalization` headline set in Times New Roman (original is serif).
4. Cyan bar line 1: only `-1 , +1` is bold (was whole-line bold); line 2 underline
   extent corrected to `dot product` (was `dot` only).
5. Callout: ALL three lines are dark blue (was lines 2-3 black).
6. Stroke weights reduced to the original's: vectors 2.5→1.5pt, axes 1.5→1pt,
   box borders 2→1.5pt.
7. Green θ: the original has NO separate arc (the spec's "arc" was the glyph itself) —
   arcs removed; θ re-rendered as a STIX mathtext PNG (round glyph, 11.3×16.6px@72,
   ink centered on the measured blob centers) after two text-glyph variants were
   rejected by the crop verdicts (Arial bold italic too heavy, Times italic too narrow).
8. Vector labels a/b underlined (vector notation, visible in the original).

## Judge findings (3 MINOR, none fixed-optional)

1. MINOR: first fraction's numerator sits close to the treq box's top border
   (tighter than the original's headroom; contained, not clipping) — this is the
   STIX vs PowerPoint fraction-elevation difference, within the alignment law's
   tolerance; the 'Normalized' baseline matches the original within ~1px.
2. MINOR: right diagram's blue b vector a touch longer (cosmetic).
3. MINOR: title x-center ~1-2% right of the original's optical center
   (PIL: both centers = 422.5/960 frame px exactly; documented as judge variance —
   the title is deliberately off panel-center because the original is).

## Omitted by rule

- The gray pencil/pen presenter annotation inside the right circle (spec imagery +
  GROUND RULES (c): presenter artifact).

## Notes / operational

- Judge procedure executed by the worker via Bash (no Agent/Task spawn tool in this
  environment) — the banked judge procedure per 17 §6, orchestrator-approved
  fallback; verdict taken verbatim from the comparison winner body.
- LO render gotcha (relearned at cost): `-env:UserInstallation=file://<RELATIVE path>`
  deadlocks LibreOffice 26.8's config manager at startup (futex hang, exit 255 from
  oosplash). ALWAYS pass an ABSOLUTE path in the file:// URL. Diagnosed via strace.
- Equation PNGs + sidecars banked under `recreated_pptx/build/assets/`
  (eq_a/eq_b/eq_dot/cos_red/cos_black/eq_unit/eq_theta .png + scratch sidecars).
- OMML dual-representation wrap NOT applied — not part of this playlist's worker
  contract (deep-learning AGENTS.md / dispatch); the certified deliverable is the
  judge-PASSED PNG-based build.
- No dependent slides (slide 23 is a dependency root) → no component export needed.

## Milestones (DB `slides_progress.db`, VIDEO=deep-learning/001_transformers_part1)

gen_status: building → judging → **passed**; visual_check=PASS; visual_attempts=1;
visual_transcript=qa/slide023/judge_attempt_1.txt; pptx_path + build_script set.
