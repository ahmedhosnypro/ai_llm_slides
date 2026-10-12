# Worker report — slide 036 "Multi Head Self Attention Block" (002_transformers_part2)

**Final verdict: PASS (attempt 1, real comparison transcript).**
DB row: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide036/judge_attempt_1.txt`.

## Deliverables

- PPTX: `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_036_recreated.pptx`
  (single plain-named deliverable; no equations → no OMML wrap; no advanced graphs → no graphgen).
- Build entry: `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_036.js`
  (pptxgenjs, LAYOUT_WIDE, NODE_PATH=$(npm root -g)).
- **BANKED COMPONENT** (dependency audit recommends 38←36; 36 is the ancestor of the
  block-diagram family reused by 38/45/46):
  `videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_036.js`
  — `renderBase(pptx, slide, opts)` at BLOCK granularity with `opts.skip` =
  [`title`,`infoPanel`,`diagram`,`strips`,`dots`,`banner`,`arrows`,`gutters`,`caption`],
  `opts.numeral` (default 36), `opts.chrome:false` to omit the house chrome; exports
  `MEAS` (all frame-px measurements), `C` (colors), `FX/FY/PT` (frame→slide transform).

## Attempt history (2 renders, 1 judge dispatch)

- **Render 1** (attempt-1 build): chrome check PASS; PIL self-check found 4 scan-region
  artifacts → tightened re-check (selfcheck_attempt_1b) ALL PASS; gated dense-region crop
  comparison (5-region sheets, `cropcheck_attempt_1.txt`) → **CROP VERDICT: PASS** with
  1 MAJOR (arrow fill white vs original's tinted fill) + 2 MINOR (tail strips missing a
  5th pale-pink cell; caption not italic / slightly narrow).
- **Fixes applied** (all three confirmed against raw pixels before fixing):
  arrow fill `FFFFFF`→`BCB8F4` (interior census mean (187,183,244)); ALL 8 token strips
  rebuilt with the measured 5-slot anatomy yellow|green|pink(label)|violet|pale-pink
  (censuses of units 1/3/6/7/8; strips extend ~60px, pitch 73); caption → bold italic
  13.5pt (width then 280pt vs original 292pt, was 261pt).
- **Render 2** = judged attempt: chrome check PASS; self-check ALL PASS
  (`selfcheck_attempt_2*.txt`); crop comparison re-run
  (`cropcheck_attempt_2.txt`) → **CROP VERDICT: PASS** (residual: MINOR ~60% "faint
  hatch/gradient texture" on arrows — pixel census supports flat lavender fill;
  documented, not a fix trigger).
- **Judge** (banked `judge_prompt_1.txt`, executed by the worker per 17 §7 fallback —
  no spawn tool in this environment; orchestrator-approved): probe ran (probe transcript
  not written by the tool — probe request produced no body; comparison landed first
  try) → comparison `judge_attempt_1.txt`:
  **FINAL VERDICT: PASS** for 'faithful, usable recreation'.
  Judge findings: 0 BLOCKER / 0 MAJOR / 3 MINOR — (1) bracket-gap width in info-panel
  lines slightly wider than original (spec-verbatim spacing kept per the verbatim law;
  zoom transcript itself read 2 spaces vs the spec's 3 — ambiguous at video resolution);
  (2) arrow fill treatment (see above, reconciled at crop zoom); (3) ellipsis dots
  slightly larger (d = 7/6.5 frame px, measured). No clipping/overflow/collisions; frame
  containment confirmed; subscripts clean; cursor + video-player bar correctly omitted.
  Note: the judge called the upper gutter label "red italic" — the render is BLUE per the
  measured blue-core census + zoom transcript (judge variance at full-slide scale; crop
  check confirmed blue in both sheets).

## Content decisions of record

- Token labels 0-BASED: Y_0..Y_5, Y_{N-2}, Y_{N-1} / X likewise — per SOURCES.md read of
  record + build-time zoom (`zoom_tail_labels.txt`: "not N+1 and not N/2") + certified-
  convention slide 020 syms. The analysis JSON's raw 1-based/[?] tails are superseded per
  the SOURCES.md subscript note (recorded correction).
- Upper gutter label "Output of Self / Attention" is BLUE (2121A5), lower "Input␣␣to
  Self / Attention" (double space) RED (C00000), both bold italic 13pt, 2 lines — per
  zoom + PIL core censuses (spec's "red bold" for the upper label was a mis-read).
- Info-panel text verbatim incl. indent groups (headers x105; Input/Output bodies x181;
  Remember bodies x146/x144; "[Apply␣␣Pad or Cut]" x227 frame px), 16.5pt, line pitch
  19.9pt as measured; single-line boxes (no multi-line auto-pitch anywhere → lineSpacing
  law satisfied by construction; the only 2-line texts are drawn as separate single-line
  boxes at measured cap tops).
- Colors (measured-color law): banner 1A0EAE (solid census (26,14,174); zoom #1D1DAE);
  text/border blue 2121A5; title/labels/diagram border C00000; panel fill FFFFE6; caption
  990000 (spec [?]-estimate) on FFFF00; dots 2222CC / 22CC22; slots FAFDC3/F0FFDE/
  FFCCCC/E9E5F5/F7DEF4; strip borders AAAAAA; arrows outline 2121A5, fill BCB8F4.
- Chrome: shared `shared_patterns/house_chrome.js` numeral 36;
  `house_chrome_check.py` PASS on both renders.

## Evidence banked under `qa/slide036/`

`judge_prompt_1.txt`, `build_attempt_1.js`, `build_attempt_1_component.js`,
`render_1.png`, `render_2.png`, `probe_1.txt` (not produced by tool), `zoom_tail_labels.txt`,
`zoom_texts.txt`, `cropcheck_attempt_1.txt`, `cropcheck_attempt_2.txt`,
`judge_attempt_1.txt`; measurement scripts + outputs + crops under
`scratch/slide036/` (incl. resumed prior-worker artifacts `measure6_out.txt`,
`asciimap_out.txt`, which this run reused per the resume law).

## Environment notes

- /tmp quota-blocked: all soffice/gate TMPDIR set to the video scratch dir; soffice
  profile absolute (`scratch/slide036/lo_profile_036`).
- Judge template paths adapted: the skill script lives at
  `.agents/skills/image-analysis/scripts/analyze_image.py` (template's
  `.agents/image-analysis/...` lacks `skills/`); noted in the banked prompt.
- Prior worker (died at launch): only scratch measurement artifacts existed — no pptx,
  no build script, no qa evidence; attempt numbering started fresh at render_1.
