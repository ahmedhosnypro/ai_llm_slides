# Slide 030 — worker report

**Slide:** 30 — "Self Attention Mechanism (Input Word plays Different Roles)"
(Deep Learning DSAI 308, Transformers Part I)
**Worker:** per-slide build worker, 2026-10-11. Dependency-gated CHILD (edge 30 ← 29;
parent 29 certified, attempt 2 — DB `passed` + `visual_check=PASS` verified via
`15_progress.py deps` before building: slide 30 showed `unblocked`).
**Fresh run** (no prior qa/slide030 artifacts).

## Deliverables

- PPTX (SINGLE-VERSION law): `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_030_recreated.pptx`
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_030.js`
- Render (150 dpi, 2001×1125): `recreated_pptx/qa/slide030/render_1.png`
- Banked per-attempt provenance: `qa/slide030/build_attempt_1.js`, `qa/slide030/judge_prompt_1.txt`
- Self-check: `scratch/slide030/selfcheck_attempt_1.py` + `selfcheck_attempt_1_out.txt`

## Composition (dependency law)

`slide_030.js` requires the CERTIFIED parent component
`build/components/slide_029.js` → `renderBase(pres, s, { skip: ["title", "resultBox"] })`
(which itself composes the certified slide_026 base — the 30←29←26 import chain). House
chrome drawn ONCE via `build/components/house_chrome.js`, numeral 30. Nothing re-derived.

## Delta measurement (PIL forensics, scratch/slide030/)

Frame-diff vs `slide_029.jpg` (threshold 60, then 45): **every diff pixel accounted** by
(a) title L1 band, (b) three circles, (c) three annotation boxes, (d) question box,
(e) badge numeral 30 vs 29 (chrome), (f) the PARENT frame's mouse cursor at
x736..756/y352..366 (gray blob — video artifact per ground rule (c), correctly absent in
slide 30's frame). The subtitle band y79..101: **0 diff px** — inherited verbatim.
No leader lines exist between the annotation boxes and the circles in the frame
(low-threshold corridor scans show only circle arcs + box borders) — the spec's "red
leader lines" are a spec hallucination; frame wins.

Measured delta (frame px, 1px = 1pt):

| Element | Measured |
|---|---|
| Title L1 | "Self Attention Mechanism (Input Word plays Different Roles)", 20pt bold (S-glyph caps y59..72 = parent's 20pt), ink x181..752 (center 466.5, parent's box), saturated FFFF00 highlight x430..754 y54..77 |
| Circle, Keys stack | center (100, 326), d=70, FFFF00 @ ~50% alpha (B-channel 113 over base 231), no rim |
| Circle, Values stack | center (803, 329), d=70 |
| Circle, Query row | center (294, 492.5), d=70, pink-through-yellow sample (223,165,66) confirms translucency |
| Annotation boxes | white fill, red border (washed cores d2ada7/c8a59f/ceaba7 → C00000 1pt): KEY x178..286 y263..307, VALUE x606..714 y270..314, QUERY x378..487 y415..459.5; text 2 lines 14pt bold, pitch 20px, centered: "X₂ is used as" (ink 87px in all three; X₂ token red 9E101E, body black — cores 63,65,62) / role word all-red: "Key"(25px) "Value"(37px) "Query"(40px) = 14pt bold widths |
| Question box (replaces resultBox) | white rect x573.5..839.5 y440.5..506.5, washed blue-gray border (parent resultBox's certified 0000CC 1pt treatment); 17pt bold ITALIC, pitch ~21.5px → lineSpacing 22, text block 8px above box center (text box y443 h45 valign middle); L1 "Should we use "(blue) + "SAME X₂"(red 9E101E, core 135,13,36) + " Vector"(blue); L2 "for the three Roles ?" (blue; space before "?" verbatim). Word segments pixel-verified: Should(584..639) we(645..665) use(672..699) SAME(705..752) X₂(758..773) Vector(780..830) / for the three Roles ?(626..787) |

Frame-vs-spec corrections applied (fidelity law — frame wins): (1) red span in the
question box is "SAME X₂" (spec said only "X₂"); (2) annotation line-1 "X₂" token is red
(spec said "rest black"); (3) NO leader lines drawn (spec claimed them; absent in frame);
(4) the stack circles enclose the THIRD chip row (measured centers y326/y329 vs row-2
cy287.5) — drawn exactly where the frame shows them; (5) question text is bold ITALIC
(upright in spec-era assumption; corrected after crop-check + A/B font test below).
`[?]` items in the spec: none to carry (validation.uncertain_items were analysis-side).

## Intra-attempt fixes (attempt 1, before judging)

1. **subRed/titleBlack fallback**: the slide_029 component's `COLORS` does not export
   `subRed`/`titleBlack` (those live on slide_026's palette) — first render put the red
   words in black. All delta colors pinned locally in `D`. Detected by the
   inheritance-diff check (7265 px on the subtitle band) + direct red-run scan; after the
   fix the subtitle band diff vs the certified parent render is **0 px**.
2. **Question-box italic**: the crop comparison flagged the original's question text as
   bold italic vs my upright. A/B font test (Liberation Sans Bold vs BoldItalic
   correlated against the original's ink: L2 italic 0.87-0.90 vs upright 0.76;
   CONTROL annotation "Value" correctly reads upright 0.86 vs 0.63) confirmed ITALIC.
   `italic: true` applied. Self-check re-run: ALL PASS.

## Pre-judge self-checks (attempt 1 — ALL PASS)

`selfcheck_attempt_1_out.txt`: house_chrome_check.py **PASS**; inheritance diff vs the
certified parent render confined to delta zones (**0 unaccounted px**); title ink
center 465.6 vs 466.5, y58..76.2 vs 58..76; highlight extent match; all three circles
center/diameter within 0.5px of target d70; all three box border-line centers within
1px; 2-line text bands present in every box; question box border + 2 lines; containment
inside the house frame for all delta elements; no wrap (ink widths 84-85 vs 87, 251 vs
247, 165 vs 161).

## Crop comparisons (self-check #6, vision gate, transcripts in qa/slide030/)

- `crop_qbox_check.txt` — question box: wording/line-break/red-span IDENTICAL
  ("SAME" + subscript "2" red in both); flagged italic (FIXED, see above) and a
  thinner original border (1pt kept — parent resultBox's certified treatment; JPEG wash).
- `crop_annboxes_check.txt` — three annotation boxes: text/structure/colors identical;
  IMG2-only "dark diagonal scribble" over "used" in the Key box = the parent frame's
  mouse cursor (video artifact, ground rule (c)). No recreation defect.
- `crop_title_check.txt` — title verbatim in both; model claimed original title is
  "dark navy" — REFUTED by pixel cores (mean (33,32,35), min (0,0,0), B−R = +2.2 →
  black; documented override). Subtitle red words verified present in my render
  (runs match the certified parent exactly).
- `crop_circles_check.txt` — re-run after a gateway wall-hit; result: see below.

## Judge

Per `17_worker_instructions.md` §7 fallback (no Agent/Task tool in this environment —
ORCHESTRATOR-APPROVED): the banked judge procedure was executed by the worker via
`scripts/16_vision_gate.sh` + `analyze_image.py`, byte-for-byte per
`judge_prompt_1.txt` (script path corrected to the actual
`.agents/skills/image-analysis/scripts/analyze_image.py`; -p template verbatim).
Judge comparison: `--thinking high --max-tokens 65536`, W4 wall (540/420).

- Probe: two 150s hangs (gateway queue busy; endpoint alive, HTTP 401 unauth probe) —
  escalated directly to the wide-wall comparison per the W4 law.
- Transcript: `qa/slide030/judge_attempt_1.txt`

## Attempt 2 (leader lines — the only attempt-1 finding that was on MY delta)

Attempt-1 judge verdict was **PASS** with 4 MINOR findings. Three were on inherited
regions (⊗ multiplier glyph style, Y-box green arrow blockiness, Σ box fill) — the
render is pixel-identical to the certified parent render there (inheritance-diff
check: 0 unaccounted px), so they are judge variance → documented, overridden per the
inheritance law. The fourth (missing leader lines) was on MY delta: re-verified with a
30-only ink scan (`lum<220` in frame 30 AND `>=220` in frame 29) — **all three leaders
are NEW in THIS frame** and my first-diff scan had missed them (thin 1-2px washed-red
anti-aliased strokes; my original corridor scan also used the wrong y-band). Fixed:

- KEY: stub (178,270.5)→(160,270.5) + diagonal →(141,286.5) [stack container edge/circle]
- VALUE: stub (714,279.5)→(731,279.5) + diagonal →(769,303.5) [inside right container]
- QUERY: stub (378,423.5)→(362,423.5) + diagonal →(306,466) [inside the query circle]

First drawing of the QUERY leader used the wrong anchor (box corner instead of the
y423.5 stub) — caught by the closed-loop path check (26/215 samples inked), corrected
to the measured trail (218/218). Final path-hit verification vs the frame: KEY 113/113,
VALUE 161/167, QUERY 218/218 (render+frame ink on every path sample). C00000 0.75pt.

Attempt-2 self-checks: **ALL PASS** (`selfcheck_attempt_2_out.txt`) — inheritance diff
0 unaccounted px (leader zones incl.), house chrome PASS, all geometry/containment/wrap
checks green.

## Judge attempt 2

Transcript: `qa/slide030/judge_attempt_2.txt` (same frozen -p, --thinking high,
--max-tokens 65536, W4 wall). Element-by-element: every delta element verified
("all three present and terminating at the correct targets, matching the original" —
leader lines; note box "two-line break matches original exactly"; circles "same
relative rows/positions"). **FINAL VERDICT: PASS** for 'faithful, usable recreation'.
Zero BLOCKER / zero MAJOR. Four MINOR findings, all documented overrides:

1. Query circle/pointer-arrow near the panel bottom edge (judge confidence ~50%,
   "not clearly a hard overflow") — the ORIGINAL frame itself draws the circle to
   y527.5 and the chunky arrow to y526 past the canvas bottom (y522); the recreation
   pixel-matches the frame there (0 unaccounted diff). Faithful reproduction, not a
   defect.
2. Vertical red stubs below the W₂₃/W₂₄ nodes — inherited flowLines block, pixel-
   identical to the certified slide-026/29 renders (0 unaccounted diff vs the
   certified parent render). Judge variance.
3. ⊗ multiplier glyph scale — inherited block, same evidence. Judge variance.
4. Global scale/stroke-weight impression — rendering-medium difference (150dpi LO
   render vs JPEG video frame), no positional finding.

## Result

**PASS on attempt 2** (2 judge attempts, 2/6 budget). Certificate: single-read,
default route (images), glm leg DEFERRED/BLOCKED; judge procedure executed by the
worker (no spawn tool available in this environment — orchestrator-approved fallback,
17_worker_instructions §7).

- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
  `visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide030/judge_attempt_2.txt`
- Slide 30 has NO dependents in `slide_dependencies.json` (no edge lists 30 as a
  parent) → per the dependency law §2, no component banking is required; the parent
  component `components/slide_029.js` was used read-only (never edited).

### Evidence index (qa/slide030/)

| File | What |
|---|---|
| `render_1.png`, `render_2.png` | 150dpi LO renders (attempt 1 / attempt 2) |
| `build_attempt_1.js`, `build_attempt_2.js` | banked per-attempt build scripts |
| `judge_prompt_1.txt`, `judge_prompt_2.txt` | banked substituted judge prompts |
| `judge_attempt_1.txt`, `judge_attempt_2.txt` | judge comparison transcripts (real winner bodies) |
| `crop_qbox_check.txt`, `crop_annboxes_check.txt`, `crop_title_check.txt`, `crop_circles_check.txt` | mandatory dense-region crop comparisons |
| `probe_1.txt` | probe transcript (gateway queue-busy; both 150s probes hung → wide-wall escalation) |
| `../scratch/slide030/selfcheck_attempt_1.{py,txt}` (+out), `selfcheck_attempt_2.{py,_out.txt}` | PIL self-checks, banked numbers |
| `../scratch/slide030/` | frame-diff maps, 30-only ink scans, A/B italic test, leader path measurements |
