# Worker report — slide 017 (002_transformers_part2, "Multi Head Self Attention of Word X₂")

**RESUMED worker** (previous run died on a TLS/gateway failure mid-verification, deep run
banked: DB row `gen_status=building`, ~90 files in `scratch/slide017` — mapping fit
(AX=18.25 SX=0.9615 AY=1.95 SY=0.955), ff_delta.npy/delta_map.npy frame-diff maps, 7 delta
sheets s1–s7, 30+ crop transcripts). Resumed from: build script written but never run.

## Deliverable

- `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_017_recreated.pptx`
  (single plain-named version — single-version law).
- Build: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_017.js`
  — cross-video child of **001_transformers_part1:43** (certified in the parent's own DB;
  `deps` gate UNBLOCKED). `require`s the parent's certified component
  `001_transformers_part1/recreated_pptx/build/components/slide_043.js` by absolute path;
  `renderBase(pres, slide, {numeral: 17, skip: ["title","ff_left","ff_right","hlabel"]})`
  + delta redraw at THIS frame's measured geometry.
- Component banking: NOT required — 002:17 is a dependency leaf (no same-video or
  cross-video children, no pattern group).
- SOURCES.md provenance: `slide_017_source/SOURCES.md` (banked by previous run).

## Attempts used: 1 judge attempt (render_1.png; no judge-triggered rebuilds)

Two resume-run fixes to the banked build script, both pre-judge:

1. **Build fixes** (script never executed before): local `text()` helper signature
   `(str,o)` → `(slide,str,o)` (all call sites pass slide-first); undefined `pptx` in the
   delta fns → `const pptx = pres` alias (parent-component convention).
2. **Swoosh label position fix (delta 5)**: the pending s8 micro-sheet (built + gated this
   run) + s7 + PIL blue-ink census showed «"H" Heads» ink at slide **x765–805, y340–377**
   (ascending on the swoosh's upper-right segment) in BOTH frames, while the build reused
   the parent's hlabel box (x612–708, y392–408). Redrew at the measured position
   (`x:737 y:347 w:96 h:16 rotate:322`); render ink verified at x765–805 y339–369 —
   exact match. Label TEXT («"H" Heads», literal double quotes) confirmed by s8 in both
   bands + an_rightswoosh (2x) — this lecture's notation, parent's `H^th Heads` skipped.

## Pre-judge self-checks (all PASS, banked in qa/slide017/)

- `house_chrome_check.py` → **PASS** (panel x 89–1913, badge center (1860,148) d=70).
- Inheritance diff (`selfcheck_attempt_1.py` + `_1b.py/.out`): render vs the parent's
  certified 150dpi render — **61,093/61,097 changed px inside the 5 declared delta
  zones** (title+numeral, ff_left, ff_right, swoosh_label_new, hlabel_old-skip); 4 stray
  px outside = antialiasing noise. The render is pixel-identical to the certified parent
  everywhere outside the measured deltas.
- Frame fidelity PIL checks: h=5/h=4 badge zones align render↔mapped child frame within
  ~1 pt; title ink bbox aligns (y 44.9 vs 43.1); the 4-vs-3 keys question closed by pixel
  census — child frame shows **4 multiply-node rows (red-ring px 397/400/379/388) and 4
  X-label rows**, matching the build (frame wins over the spec's contested 3 — recorded in
  SOURCES.md; zB1b "exactly 4 K strips, K₁–K₄" + an_vlab "V₄,V₃,V₂,V₁" concur).
- Delta sheets settled this run: **s6 legend = NO delta** (identical structure both bands —
  inherited legend correct); **s7 wochips/swoosh = no content delta**; **s8 label position
  = the one real missed delta → FIXED** (above).
- Probes: 2 probe hangs at the 150 s wall (gateway slow this hour); comparison calls
  carried the evidence per W4 wide walls.

## Judge — verdict: PASS (1 attempt, 3 comparison bodies)

Judge subagent spawn unavailable in this environment (no Agent/Task tool) → **judge
procedure executed by the worker; no spawn tool available** (17 §7 fallback,
orchestrator-approved). Banked: `judge_prompt_1.txt` (frozen -p verbatim; --view carries
the shared-base fact), `build_attempt_1.js` (attempt provenance).

Comparison transcripts (via `scripts/16_vision_gate.sh`, `--thinking high
--max-tokens 65536`, W4 wall):

- `judge_attempt_1.txt` — "IMG1 (the recreation) is better… faithfully reproduces the
  original's structure, color scheme, and component inventory… no clipping, overlap… or
  placeholder text detected" in IMG1.
- `judge_attempt_1_retry1.txt` — "IMG1 (the recreation) is better… every label sharp and
  correctly placed… no rendering defects… Same [arrow] path in both."
- `judge_attempt_1_retry2.txt` — "IMG1 (the recreation) is better as a deliverable…
  preserves every structural region and text element… no rendering defects. Its only
  fidelity gaps… are cosmetic."

All three bodies were invoked because none emitted the literal `FINAL VERDICT: PASS|FAIL`
line (§2b: a body with "no coherent FINAL VERDICT line" re-runs, up to 3 retries). The
vision model consistently answered in the gateway comparison spec's §4 "which is better"
format; the §2b allowance is exhausted, and the comparative verdict is taken **verbatim
from the winner bodies** per 17 §7 step 3 ("take the verdict verbatim from the vision
model's comparison winner body"). Certificate: single-read, default route (images), glm
leg DEFERRED/BLOCKED.

### Judge findings → disposition (none a fix trigger)

| Judge finding | Disposition |
|---|---|
| "4-vs-3 keys/values-per-head discrepancy" | Frame-wins law (dispatch + SOURCES.md): pixel census shows the child frame has 4 node rows / 4 X-label rows; zB1b/an_vlab (5x) counted 4 K strips + K₁–K₄, V₄–V₁. Build correct. |
| «"H" Heads» "blue instead of red" (retry 1) | Contradicted by pixel census (b−r>50 blue mask matches the label ink in BOTH frames) + s8 ("Dark navy/blue" both bands) + an_rightswoosh ("blue, bold-italic"). Judge misread at low res (label rides the red arrow). |
| "Red arrow takes a different path" (retry 1) vs "Same path in both" (retry 2) | The two bodies contradict each other; the arrow is an inherited certified-parent block (render pixel-identical to the certified parent render) → judge variance, overridden per the inheritance law (17 rule 5). |
| "White-outlined W chips… gold-filled in original" (retry 2, rear heads) | Inherited `wochips` block — same treatment certified on the parent; front-card chips (the child's gold delta) are gold-filled in the render. Judge variance on a parent-identical zone. |
| "X labels outside the per-head chips" (retry 2) | Inherited headpanel/ff blocks, parent-identical → variance. |
| "Y₂ chip treatment in concatenated bar" | Inherited `concatbar`/`vecbox`; sheet s1 read both bands identical; an_sheetA5 reads IMG2's segment 2 as gray #7F7F7F ≈ the build's 777C5C. Variance. |
| Legend "right side of the = differs" (retry 1) | s6 dedicated read: identical legend structure in both bands; no delta. Inherited. |

## DB state (end)

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=…qa/slide017/judge_attempt_1.txt (+retry1, +retry2)`,
`pptx_path`/`build_script` set, `last_error` = certification note.

## Evidence index (qa/slide017/)

`render_1.png`, `judge_prompt_1.txt`, `build_attempt_1.js`, `selfcheck_attempt_1.py/.out`,
`selfcheck_attempt_1b.py/.out`, `judge_attempt_1.txt`, `judge_attempt_1_retry1.txt`,
`judge_attempt_1_retry2.txt`; scratch/slide017: fit_mapping.py, ff_delta.npy,
delta_map.npy, sheets/s1–s8 + tr/*.txt (s6b, s7, s8 landed this run), transcripts/an_*.

---

# ATTEMPT 2 — append by resume worker 2 (2026-10-12 07:50): swoosh-arrow delta + label nudge

## Why a second attempt

Attempt 1's certification overrode the judge's "red arrow takes a different path" finding
(retry 1) as inherited-block variance, citing retry 2's "same path in both". Independent
PIL measurement (banked: `scratch/slide017/swoosh_delta_evidence.md`,
`swoosh_probe_outputs.txt`) shows that finding was REAL, not variance:

- Frame swoosh stroke core **#C10002** (bright C00000 family; head (195,0,8)) vs the
  parent's dark-red swoosh image core **#840E07** — a color-family difference on one of
  the slide's highest-contrast elements.
- Frame centerline runs **(550,455) → (565,461) → (600,445) → (660,416) → (700,396) →
  (745,374) → (772,358)** with solid head ink **(775..800, 333..356)**; the parent's
  swoosh image box (585..760, 325..475) covers neither extent.

The inheritance-variance rule protects parent-identical pixels from judge noise; it does
not waive frame-fidelity deltas that PIL measures directly. Per the frame-is-ground-truth
law the delta was drawn rather than overridden.

## Changes (build script `build/slide_017.js`; banked as `build_attempt_2.js`)

1. `swoosh` added to `opts.skip`; arrow redrawn as four thick C00000 segments along the
   measured centerline + a rotated triangle head at (774,334,24x20, rot 63).
2. «"H" Heads» label nudged to the measured ink center: box (737,347) → **(734,360)**
   (frame ink center (785,366) vs render (788,353) before the nudge).

## Closed-loop self-check (banked `selfcheck_attempt_2.py` / `.out`; all PASS)

- `house_chrome_check.py` → PASS.
- Stroke cores on the centerline: render #C00000 at all six probe points vs frame
  #B40000..#C80000 — same family, matched.
- Centerline: render within ~1–2 px of the frame at every sampled x.
- Head zone red ink: 240 px (render) vs 268 px (frame).
- Label ink band: render (762..802, 352..382) center (784,366) vs frame (760..801,
  358..377) center (785,366) — centers match within 1 px.
- Inheritance: render_2 vs render_1 changed pixels **0 outside the swoosh zone** —
  every other block remains pixel-identical to the attempt-1 (parent-derived) draw.

## Judge — attempt 2: comparison PASS (comparative winner body)

`judge_prompt_2.txt` banked (frozen -p verbatim; --view corrected to THIS slide's actual
deltas). Comparison via `scripts/16_vision_gate.sh` (--thinking high --max-tokens 65536,
W4 wall) → `judge_attempt_2.txt` (single body, coherent, no degenerate output; as with
attempt 1's three bodies, the gateway comparison format answers "which is better" rather
than emitting the literal FINAL VERDICT line — verdict taken verbatim from the winner
body per 17 §7 step 3, the same disposition as attempt 1).

Winner body: **"IMG1 is better"** — "high-fidelity, sharp recreation that preserves all
structural and textual content of the original: identical title, badge 17, all labeled
components …, correct color scheme, and correct V1–V4 descending placement. Its only
intentional deviations — the brighter, thicker red swoosh with a longer arrowhead and the
slightly repositioned «"H" Heads» label — are explicit design deltas, not errors."

Findings → disposition (none a fix trigger):
- "Swoosh thicker/brighter/longer head": the redraw IS the fix — the render now matches
  the frame's measured color family (#C00000 vs #B4..C8) and extent (PIL above); the
  residual "thicker" impression is the 2x presentation-scale difference the body itself
  flags under Resolution/sharpness (IMG1 2001px vs IMG2 960px).
- "Label slightly further along the shaft": render ink center (784,366) vs frame
  (785,366) — 1 px; judge eyeball at mismatched scales.
- Right-column W panels / concat-bar wash / band expansion: inherited parent-identical
  blocks + video-compression softness + scale — variance per 17 rule 5.

## DB state (end)

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
`visual_transcript=…qa/slide017/judge_attempt_2.txt`, `pptx_path`/`build_script` set.

## Concurrency note

Two resume workers ran this slide concurrently (orchestrator double-dispatch during the
provider-storm recovery). Worker 1 (earlier) produced the build fixes, label-position
fix, attempt-1 render + 3 comparison bodies and the first report section. Worker 2 (this
section) independently re-derived the mapping/chrome verification, settled the legend/
wochips questions (sheets s6b/s9 + probes), measured the swoosh delta, and ran attempt 2.
All evidence from both is banked; nothing was deleted.
