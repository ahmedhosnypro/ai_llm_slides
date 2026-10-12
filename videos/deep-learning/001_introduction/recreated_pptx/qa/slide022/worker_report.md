# Worker report — slide 022 (001_introduction, Deep Learning DSAI 308)

**Final verdict: PASS** — single-read comparison via `scripts/16_vision_gate.sh`
(default images route, `--thinking high --max-tokens 65536`), transcript
`qa/slide022/judge_attempt_2.txt`: "No BLOCKER or MAJOR defects… FINAL VERDICT: PASS
for 'faithful, usable recreation'." 4 MINOR findings (case-delimiter curvature/weight,
d(X) operator spacing, O/P vs OIP low-res ambiguity, fan-line weight).

## Deliverable
- `videos/deep-learning/001_introduction/recreated_pptx/slide_022_recreated.pptx`
  (SINGLE-VERSION; no equation OMML wrap owed — the composed-matrix tokens are images;
  no graph image owed.)
- Build: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_022.js`
- DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
  `visual_transcript=…/qa/slide022/judge_attempt_2.txt`.

## Ground-truth resolution (dispatch conflict — documented deviation)
The dispatch's content line ("Compare to ML training: Only Classifier parameters are
updated") was ERRONEOUS. `unique_slides/slide_022.jpg` (= founder-swapped frame
`frame_01094.jpg`, new22←old27) is the **"Visualization of Single Perceptron"** slide;
a banked vision probe of the frame itself (`qa/slide022/gt_probe.txt`) and PIL forensics
(`scratch_022/forensics1..f26`) confirm it matches `analysis/slide_022_final.json`
(PASS_WITH_FIXES content gate, founder_frame_swap=true in _meta). The
"Compare to ML training" slide lives elsewhere in the old-27/28 family (see
`slide_026_source/SOURCES.md` family note). The frame was taken as ground truth
(no second-guessing); the spec was applied verbatim.

## Resume provenance
A predecessor worker crashed after building + rendering (render_1, no judge). Its build
is banked as `qa/slide022/build_attempt_1.js` (= `build_pre_rework.js`) with
`scratch/slide022/MEASUREMENTS.md`. This run resumed from it, re-measured
independently, and reworked the build (attempt 2). Attempt/render numbering continues
from the predecessor's (render_1 → render_4; the first judge dispatch judged render_4).

## Attempts used (visual: 1 judging round on render_4; 3 pre-judge self-check iterations)
- **render_2** (rework v1): closed-loop PIL self-check vs frame + 4 zoomed crop
  comparisons through the gate (eq1/eq2/dec/diag). Found: label underline rendered as
  strikethrough (LO baseline model — text ~4.5px low; MAJOR), Σ glyph missing
  (z-order: opaque cyan disc painted over the glyph PNG; BLOCKER), activation container
  shape wrong (original = pink-filled rectangle w/ magenta border, not circle; MAJOR).
- **render_3**: fixed all three (z-order fix, block→pink-filled rect E9B7D4/CC66CC
  drawn before the shaft, label tops −4.5px, blues → 0000CC per judge+spec). Crops:
  eq1 MATCH, eq2 MATCH, diag MATCH; dec crop MISMATCH — **missing RIGHT case
  delimiter** (the original encloses the 3-case group on BOTH sides; my scans had
  stopped at x748).
- **render_4**: added the closing hairline paren (stretched-glyph pair,
  A9A5D0, span y261..327, x542.8/747.8) replacing the straight bar. Crops: eq1/eq2/
  dec/diag ALL MATCH. house_chrome_check.py PASS; selfcheck_attempt_2.py landmarks
  within ~±3px (paren strokes 117/139.5/248.5/271.5/597/617; dots 337..358; σ present).
- **Judge (render_4)**: PASS.

## Evidence index (qa/slide022/)
- gt_probe.txt (ground-truth identity probe) · probe_2.txt (judge probe)
- judge_prompt_2.txt + judge_p_payload_2.txt + judge_attempt_2.txt (frozen template,
  playlist-chrome ground rules; verdict PASS)
- crop_eq1/crop_eq2/crop_dec(+crop_dec3)/crop_diag.txt + crops/ (render↔original crops)
- selfcheck_attempt_2.py · build_attempt_1.js (predecessor) · build_attempt_2.js (final)
  · build_pre_rework.js · gen_assets_attempt_2.py · eq_022_manifest.json
- renders 1–4 (banked, never deleted)

## Deviations from the spec (PIL-measured overrides, deck pixel law)
- W and b in EQ2 are RED (spec: only b); the X inside d(·) is RED (spec: black);
  all reds C00000-family.
- NO underline below X/W in EQ3's main line beyond the mathtext \underline on
  W̲ᵀX̲ (spec ambiguity); the aug/weights vectors' X̲/W̲ underlines are rendered
  (measured rows y172-173).
- Decision-box fill FAFEED, callout fill E3E5C9 + dark-tan border A79E88 + brown text
  604820 (spec: FFFFE1 / tan+red border / dark-red — measured modals override).
- Case-group delimiters: thin curved lavender-blue paren pair (spec said a red brace;
  measured spine is a washed hairline, and the closing paren exists in the frame).
- "wn" in the diagram sits beside the SECOND dots row (measured), not beside xₙ.
- Black bottom strip DRAWN (certified deck precedent 002/005/031; spec brief said
  exclude — frame-matching wins); mouse cursor omitted (ground rules (c)).
- Blues 0000CC (spec value; judge crop reads favored it over the 000080 first choice).

## Banking obligation
Slide 22 has NO dependents in `slide_dependencies.json` (it is a root, no children
reference 22 in this or other lectures' graphs) — no component bank owed. If a future
graph needs it, the certified build script is single-source at
`recreated_pptx/build/slide_022.js`.

---

## Verification addendum — original fresh-dispatch worker (read-only standby), 2026-10-12 09:50

This slide was worked IN PARALLEL by two dispatches that did not see each other:

- **Dispatch A (this addendum's author)** — fresh dispatch 06:56. Collision sweep at
  06:56 was clean (no 022 artifacts, no live 022 processes; DB `gen_status=building`
  matched the 06:54:25 dispatcher batch marker shared with slides 38/46). Proceeded
  sole-owner: full PIL forensics (`scratch/slide022/forensics1..20.py`,
  `MEASUREMENTS.md`), 72 STIX-mathtext/stretched-delimiter assets
  (`build/assets/eq022_*` + `eq022_manifest.json`), build v1-v3, renders, closed-loop
  checks (`check_loop*.py`), first render banked `render_1.png` + `render_1.pdf`.
- **Dispatch B** — appeared ~07:10 (its `gt_probe.txt`), found dispatch A's mid-state
  at ~08:24 and — per the resume law, reading A as a crashed predecessor — banked A's
  build as `build_attempt_1.js`, re-measured independently, reworked the build
  (`build_pre_rework.js` checkpoint), and continued attempt/render numbering. A did
  not detect B in real time and its last writes (08:45) accidentally landed on B's
  by-then-current script/render cycle; A detected the collision at 08:51
  (foreign build content + B's live gate processes) and STOOD DOWN READ-ONLY from
  that moment per the collision protocol.

**Standby verification of B's certificate (all read-only):**
- Transcript `judge_attempt_2.txt` is a real comparison winner body through
  `scripts/16_vision_gate.sh` (default images route, --thinking high --max-tokens
  65536, frozen -p template + GROUND RULES prelude), ending "FINAL VERDICT: PASS for
  'faithful, usable recreation'." — 4 MINOR findings, no BLOCKER/MAJOR.
- Artifact binding: judged `render_4.png` (09:31:08) is the 150dpi render of
  `slide_022_recreated.pptx` (09:30:45) built by `build/slide_022.js` (09:30:18);
  the DB row (`gen_status=passed`, `visual_check=PASS`, `visual_attempts=2`,
  `visual_transcript=judge_attempt_2.txt`) is current and points at these paths.
- Independent `house_chrome_check.py` on the judged `render_4.png`: **PASS**
  (panel x 89-1913, y 95-bottom; badge center (1860,148) d=70; tol 8).
- Evidence conservation: A's banked artifacts (renders 1-3-era files, eq022_* assets,
  forensics + measurement tables, check scripts) were never deleted; B banked its own
  chain alongside (attempts, crops, judge payload). No evidence loss.

B's substantive contributions beyond A's state: Σ-glyph z-order fix, activation
container corrected to the pink-filled rectangle, label underlines moved below text,
blues reconciled to 0000CC, and the RIGHT case-group delimiter at x≈747.8 (A's
forensics windows had stopped at x748 and missed the hairline right paren; B found it
via crop comparison). No child slides depend on 22 (`slide_dependencies.json`: edges
16←9, 17←16, 18←9, 19←9, 25←24, 37←36, 41←35) — no component banking owed, matching
the dispatch.

Slide 22 is CERTIFIED by B's banked judge PASS; A makes no competing claim.
