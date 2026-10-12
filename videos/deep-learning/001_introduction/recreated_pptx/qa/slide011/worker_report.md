# Worker report — slide 011 "Feature Extraction" (deep-learning/001_introduction)

## Verdict chain

| Attempt | Build | Pre-judge checks | Judge | Verdict |
|---|---|---|---|---|
| 1 | `build_attempt_1.js` (house chrome import + PIL-measured content; iterate-in-place pre-judge: title-box wrap fix w 3→4.5in, bullet charSpacing 0.25→0.1, title charSpacing 0.35→0.2) | `house_chrome_check.py` **PASS**; `selfcheck_attempt_1.py` **PASS** (all ~60 checks ≤4 frame px: boxes ≤1.4, title ink ≤1.6, headline ≤3.9, underline rows +1.7, 8 bullets ≤1.4, 9 dots ≤0.4, ellipsis 9 dots ≤0.8, left rule x-center 0.1, black bar ≤1.1) | `judge_attempt_1.txt` | **PASS** — 0 BLOCKER/MAJOR; 2 MINOR (body-box border hue reads slightly more navy, within approx-hex tolerance; bullet dots marginally larger, sub-pixel) |

Final: **PASS on attempt 1 of 6** (real comparison winner body — coherent element-by-element analysis with a single `FINAL VERDICT: PASS` line; single-read, default route `images`, glm leg DEFERRED/BLOCKED).

## Procedure notes

- Judge executed by the worker via Bash (no Agent/Task spawn tool in this environment) — byte-for-byte per the banked `judge_prompt_1.txt`: probe (`probe_1.txt`, valid body) then comparison through `scripts/16_vision_gate.sh` with `--thinking high --max-tokens 65536`, wall regime `timeout 1700` outer / `--timeout 280` (dispatch's frozen regime, same as certified slide 040). No garbage/hang retries needed.
- Ground rules payload (`judge_p_payload_1.txt`): playlist chrome (FFFFFF canvas, E9E9E7 panel x42..918 y45→bottom, C00000 border, badge FDFD96/6A5ACD (893,71) d≈36, numeral 11) declared intentional; original's own inset gray band + dark-red L-rule covered by clause (a); mouse-cursor artifact near "Number of intersections"/"Moments" covered by clause (c).

## Measured build (frame px, 1px = 1pt; full constants in the build header)

- Title box x94..364 y61..119, fill E0FFFF, navy 000080 1.5pt; title "Feature Extraction" Arial Bold **24pt** (advance-solved: 24pt err −2 vs 25pt +7), centered (ink center 229 = box center), baseline ~97.5, charSpacing 0.2.
- Content box x95..881 y128..499, white, navy 2pt.
- Lead line baseline 151.75: "Features Types are " C00000 bold + "is " regular + "Problem dependent" bold italic underline (original underline = continuous 183px faded-gray run y154-155 x345..527 — same forensics as certified slide 010).
- "Features may include:" Arial Bold 21pt, baseline 198.8, text-left 127 (no bullet — 'F' stem ink-verified).
- 8 bullets Arial Regular 21pt (all strings advance-solved, err ≤3 with JPEG bleed), text-left 147, baselines 231.8/263.8/295.8/328.2/360.2/392.7/424.7/456.5 (pitch ~32.1 = slide 010's certified rhythm), black dots d5 center x129 at y 224/256/288/320.5/352.5/385/417/449/481.
- Left red rule 8B0000 ~2.4px core x57-58 y43..517; the original's TOP rule row 43 = chrome top-border position → covered by `drawHouseChrome`, not drawn (slide 005/010 law). Original's gray band x61..902 y47..517 subsumed by chrome panel, not drawn. Black bar x38..921 drawn y519..537.5 (h18.5) keeping the chrome's half-visible bottom stroke visible (certified 005/010 treatment, 2-frame-px documented).

## Documented deviations from the spec JSON

1. **Ellipsis bullet rendered "………" (3 × U+2026) not "……" (4 ×)** — ink forensics: 9 baseline dots, pitch 6.6px, span 57px = exactly 3 ellipsis glyphs at 20pt (12 dots/80px or 9 periods' pitch 5.83px both rejected); the spec's `_meta` flagged the dot count as unverifiable. Verbatim content preserved as the same dotted-placeholder element.
2. **Ellipsis line 20pt vs the 21pt list** — dot pitch (em/3) solves 20pt.
3. **Title 24pt vs spec's "28-32pt" estimate** — cap height 17.5px and advance 213px both solve 24pt (spec sizes were vision-model estimates).
4. **Title centered in its box** — ink center == box center measured; spec said left-aligned with 0.15in padding (ink starts x123, box x94).
5. House chrome badge numeral 11 added (originals carry no printed numbers — 001_introduction AGENTS.md assumption pending founder veto).

## No dependencies / no banking obligation

`deps`: slide 11 is root; children edges are 16/18/19←9, 17←16, 25←24, 37←36, 41←35 — nothing depends on 11; no pattern groups; no cross-video refs to `001_introduction:11` → no component banking required.

## Evidence files

- Build: `recreated_pptx/build/slide_011.js` (banked copy `build_attempt_1.js`)
- Deliverable: `recreated_pptx/slide_011_recreated.pptx` (single version, no suffix; no equations → no OMML pass; no advanced graphs → no graphgen)
- Render: `qa/slide011/render_1.png` (150 dpi)
- Checks: `qa/slide011/selfcheck_attempt_1.py` + `_output.txt`; `house_chrome_check.py` PASS; region crops `crop_ellipsis_*` / `crop_underline_*` (no equations/delimiters/tables → crop-vision clause not triggered)
- Judge: `qa/slide011/judge_prompt_1.txt`, `judge_p_payload_1.txt`, `probe_1.txt`, `judge_attempt_1.txt` (comparison transcript, PASS)
- DB: gen_status=passed, visual_check=PASS, visual_attempts=1, pptx_path/build_script/visual_transcript set
