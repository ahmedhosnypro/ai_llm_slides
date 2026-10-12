# Worker report — slide 044 "Layer , Group, and Instance Normalization" — CERTIFIED (P3 #3)

Video: `deep-learning/002_transformers_part2` · P3 pattern-group member #3 of [42, 43, 44].
Fresh dispatch (P3#2 slide 43 certified ~10:03, unblocked). Sole owner at dispatch —
collision sweep found NO scratch/slide044, NO qa/slide044, NO slide_044 build artifacts,
DB row `pending` / `P3#3 unblocked`. **Mid-flight peer event:** a "resumed by builder-6
(post-storm)" note appeared in the DB `last_error` between this worker's selfcheck
(~13:26) and judge-1 dispatch (~13:28) — builder-6 observed the banked state, wrote the
note ("no judge attempts spent"), and wrote NO artifacts (post-run sweep: every
slide-044 artifact mtime matches this worker's command chain). This worker's judge PASS
is first-to-file; the row was finalized at 14:07. Per the collision protocol, no banked
evidence was deleted.

**FINAL: PASS** — judge attempt 2 (real W4 comparison, `judge_attempt_2.txt`, literal
`FINAL VERDICT: PASS`; attempt 1 FAILed on a real defect, fixed). DB: `gen_status='passed'`,
`visual_check='PASS'`, `visual_attempts=2`,
`visual_transcript=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide044/judge_attempt_2.txt`.
Deliverable: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_044_recreated.pptx`
(single plain-named version; no equations → no OMML wrap; no advanced graphs → no
graphgen). Component banking: NO child of 44 in either deck's `slide_dependencies.json`
(checked both) → no component export obligation.

## Attempts / evidence

| Attempt | What | Verdict | Evidence |
|---|---|---|---|
| build v1–v4 | 4 closed-loop PIL fix rounds BEFORE judging (details below) | pre-judge | `scratch/slide044/selfcheck_attempt_1.py` + `qa/slide044/selfcheck_attempt_1_out.txt`, `house_chrome_check_1.txt` (PASS) |
| judge 1 | W4 comparison, probe SKIPPED (gate congested — pre-build decode call hung 3×330 s; dispatch authorizes skipping) | **FAIL** — 1 MAJOR ("Channels" label under the left stack missing — it was placed INSIDE the layer banner, colliding with its title) + 3 MINOR | `judge_attempt_1.txt`, `judge_prompt_1.txt` |
| judge 2 | fixes applied (below), re-render, W4 comparison | **PASS** | `judge_attempt_2.txt`, `judge_prompt_2.txt` |

Judge procedure executed by the worker via Bash (no Agent/Task spawn tool in this
environment — orchestrator-approved fallback, same as 042/043). Certificate: single-read,
default route (images), glm leg DEFERRED/BLOCKED.

## Closed-loop build fixes (pre-judge, all PIL-verified)

- v1→v2: the red outline rect around the RT stack was drawn with a WHITE FILL, covering
  the whole stack (self-check: "RT front magenta: MISSING") → outline-only.
- v2→v3: `band()` took frame px where slide pt was expected (systematic ~18 px/4 % shift);
  font ems re-derived ×KX; strip y-extents refit to measured; box borders washed (D89F9B —
  the original's borders read pale pink); baselines 408/424/475; oval tightened.
- v3→v4: inst/layer body boxes too narrow → text WRAPPED (short green-phrase runs) →
  boxW 430/780; body ems compensated for LO-vs-original metrics (16.8 / 17.8, measured
  ratio); RT front pitch 32.5/cell 28.5; title em 35.75 (36 wrapped).
- Post-judge-1: the left "Channels" label moved from baseline 473 (inside the layer
  banner, colliding with its title) to the measured original position (ink x95..152,
  y432..441 → baseline 441, center 124); the left arrow REMOVED (three mask passes over
  y415..458 found no shaft/heads in the original — letter-gap periodicity proves the
  y432..441 block is the label text; the spec's "arrow beneath the front face" is a
  vision-model guess, recorded in SOURCES.md); FV arrow + label moved inside the red
  rect (shaft x663, label center 675 — judge attempt-1 direct comparison, MINOR);
  layer banner border removed (original is a borderless pink band, judge MINOR #3,
  high confidence).

## Judge-2 residual MINORs (accepted, no fix triggers)

1. Layer band fill reads pale pink vs the original's paler cream/yellow (fill measured
   #FED6CA from the frame; video wash).
2. Callout boxes slightly more empty space below the last text line (top-anchored both).
3–4. Flat-slab cube construction = certified P3 house style (NOT a discrepancy per
   worker context); cursor/letterbox artifacts correctly omitted.

## Self-check record (final)

`HOUSE CHROME CHECK: PASS` (canonical panel + badge (1860,148) d=70). 41 PIL checks, 13
flagged — all triaged as: (a) orig-side mask artifacts (the original's washed ink fails
the strict masks a crisp render passes — e.g. title strict-red tail 750 vs loose 849);
(b) orig-side deeper-layer peeks inside dark bands (GN/Inst); (c) chrome-wash class
(crisp chrome border at x58 passes red/dark masks; the original's washed border does
not — same class 042/043 certified with); (d) one-row edge-blend pixels (EDFF1A over
5C2E00). No unexplained geometry deviation >5 px.

## Frame-over-spec corrections

Recorded in `slide_044_source/SOURCES.md` (build-phase section): GN front split 45/55;
"(Output of ONE Filter)" GREEN; tinted box fills; solid left front; rect geometry
x658..897 y92..363; oval geometry; **NO arrow under the left stack** (label only);
artifact omissions.

## Provenance notes (honest record)

- `build_attempt_1.js` was inadvertently refreshed to the attempt-2 state at 13:48
  (before `build_attempt_2.js` was banked) — the attempt-1 judged bytes are not
  preserved; the attempt-1 state is fully described by the fix list above + `judge_attempt_1.txt`.
  The CERTIFICATE binds to the attempt-2 chain, which is intact:
  live `build/slide_044.js` ≡ `build_attempt_2.js` (md5 c93f1d26f9cce5ed5cbfbce1e45749a1),
  `render_1.png` (13:48) rendered from the same pptx, `judge_attempt_2.txt` = the PASS
  on that render, deliverable `slide_044_recreated.pptx` (13:48).
- The pre-build crop-decode call (3-region composite) hung 3×330 s on the congested
  gate and was abandoned; the ambiguous regions were resolved by PIL measurement +
  judge comparisons instead (composite + log banked: `scratch/slide044/decode_composite.png`,
  `decode_run.log`).

## Evidence inventory (this dir + scratch)

- `build_attempt_2.js` (certified, ≡ live build) · live `build/slide_044.js` ·
  `slide_044_recreated.pptx` · `render_1.png` (certified) · `render1/` scratch renders.
- Prompts: `judge_prompt_1.txt`, `judge_prompt_2.txt`. Transcripts: `judge_attempt_1.txt`
  (FAIL), `judge_attempt_2.txt` (PASS). Self-checks: `house_chrome_check_1.txt` (PASS),
  `selfcheck_attempt_1_out.txt` + `scratch/slide044/selfcheck_attempt_1.py`.
- Measurement corpus: `scratch/slide044/measure1..9*.py` + `_out.txt` (+ this report).

---

# RESUME APPENDIX — builder-9 (2026-10-12 ~17:00): takeover conflict resolved, certificate re-bound

## What this resume found

Between this report's finalization (14:09) and ~15:51, a SECOND live builder
("builder-7", takeover header in its rewrite) **rewrote `build/slide_044.js` at
14:44:44** (md5 25e85f3347be8413dbb859aa2a5266cc — a 371-line divergence from the
certified build: title em 34→30.5, bluegray 4C5875→2B3F50 diverging from certified
042/043, band bright-edge highlights, washed borders D2B9B4 on all three boxes,
left-cube 4th dark-green band, row pitch 30) and produced renders 2/3 — but **died in
the provider storm WITHOUT ever judging them**. A third builder ("builder-8",
dispatched 13:35) correctly stood by and banked a measurement dossier in the DB
`last_error`. Net damage: the deliverable pptx (15:50) came from the UNJUDGED
builder-7 build while the DB row carried this report's attempt-2 PASS — an
inconsistent state (PASS transcript ≠ deliverable pixels).

## Resolution (verdict law: certification binds to judged pixels)

The certified build's bytes were NOT lost — `qa/slide044/build_attempt_1.js`
(mtime 13:48) IS the certified attempt-2 build, md5
`c93f1d26f9cce5ed5cbfbce1e45749a1`, exactly as this report's provenance note records.
builder-7's rewrite had overwritten `build_attempt_2.js` in place; nothing else of the
certified chain was touched (`render_1.png`, both judge transcripts, both prompts all
intact — builder-7 only added files and rewrote the two build scripts).

builder-9 therefore RESTORED the certified chain instead of re-judging:

1. `build/slide_044.js` := `qa/slide044/build_attempt_1.js` (md5 re-verified c93f…).
2. Rebuilt `slide_044_recreated.pptx` (16:33) and re-rendered via the host's working
   LO route (`scratch/slide011/render_slide011.sh` → `scratch/slide044/render_restore/`).
3. **Pixel identity proof: restored render vs the judged `render_1.png` =
   2,251,225 / 2,251,225 px IDENTICAL (100.0000%, 0 px >0 diff).** The attempt-2
   judge PASS therefore binds to the deliverable as it now stands. NO new judge
   attempt spent (ledger stays FAIL@1 / PASS@2 of 6).
4. Fresh pre-judge gates on the restored render (all banked here):
   - `house_chrome_check.py`: **PASS** (`house_chrome_check_restore.txt`).
   - Badge cross-check: frame badge yellow-core circle x859..893 y56..85 → center
     (876.0, 70.5) frame px [the 13:48 census's center-y 75 had swallowed a
     contaminant full-width row at y94; remeasured cleanly]. Through the build
     mapping: (891.96, 73.78) pt vs canonical chrome (893, 71) pt →
     **dx=1.0 / dy=2.7 frame px — within the ~3 px tolerance** (mapping identical to
     certified 002/039/042/043).
   - Closed-loop PIL self-check re-run (`scratch/slide044/selfcheck_restore.py` +
     `_out.txt`): **41 checks, 13 flagged — same per-check verdicts** as the
     certified profile; exactly 2 lines differ in intermediate numbers vs the BANKED
     `selfcheck_attempt_1_out.txt` because that banked output (13:26) predates
     `render_1.png` (13:48) and measured the earlier v1 build state (the provenance
     note above). All 13 flags are the triaged classes listed above (orig-side mask
     artifacts incl. the x898..901 cursor-class line, chrome-wash class, edge
     blends); no unexplained geometry deviation.
   - Placeholder check: all-shapes build (zero `addImage`); render identical to the
     judged render — no LO "Image 0 1" placeholders (host LO breakage avoided via
     the lo_pdf_test PDF route).

## Banked restore evidence (this dir + scratch/slide044/)

- `restore_verification.txt` — full verification record with all numbers.
- `render_attempt2_restored.png` + `render_attempt2_restored.pdf` — the restored
  certified render (pixel-identical to `render_1.png`) + its PDF.
- `house_chrome_check_restore.txt`; `scratch/slide044/selfcheck_restore.py` +
  `selfcheck_restore_out.txt`; `scratch/slide044/render_restore/`.

## builder-7's unjudged iteration — banked, superseded, not deleted

`build_attempt_2.js` ≡ `build_attempt_3.js` ≡ the 14:44 live build (md5 25e85f33…),
`render_2.png` ≡ `render_3.png`, plus its checks (`house_chrome_check_2/3.txt`,
`selfcheck_attempt_2_out.txt`, `selfcheck_cropA_2.txt`, `judge_prompt_2.txt` was
overwritten by builder-7 at 15:11 — the original attempt-2 judge prompt bytes are
described in the attempt table above) and its measurement probes
(`scratch/slide044/resume2/`, `probe44_resume1..6*`). Kept as evidence for any future
improvement round; it is NOT certified and its notable divergences from the certified
042/043 pattern (bluegray 2B3F50 vs the siblings' 4C5875) would need a pattern-law
review before ever being adopted.

## Final state (unchanged certificate, restored deliverable)

- DB: `gen_status='passed'`, `visual_check='PASS'`, `visual_attempts=2`,
  `visual_transcript=…/qa/slide044/judge_attempt_2.txt`.
- Deliverable: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_044_recreated.pptx`
  (single plain-named version, rebuilt from the certified build; no equations → no
  OMML wrap; no advanced graphs → no graphgen; no component-export obligation).
- **FINAL: PASS** — judge attempt 2, now re-bound pixel-exactly to the deliverable.
