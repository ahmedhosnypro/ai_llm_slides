# Worker report — slide 005 (Encoder – Decoder Transformer), deep-learning/002_transformers_part2

Fresh dispatch 2026-10-12; sole owner (collision sweep clean: no prior build script, qa dir,
scratch dir, or pptx for slide005; DB row `pending` unmoved since the 06:46 analysis sync).
**FINAL VERDICT: PASS** (main judge `judge_attempt_3.txt`, W4 retry). DB: `visual_check=PASS`,
`visual_attempts=3`, `gen_status=passed`.

## Deliverable

- Build: `recreated_pptx/build/slide_005.js` (per-attempt copy `qa/slide005/build_attempt_3.js`)
- PPTX: `recreated_pptx/slide_005_recreated.pptx` (single version, plain name; no equations →
  no OMML wrap; no advanced graphs → no graphgen; badge numeral 5)
- Renders: `qa/slide005/render_1..3.png` (150 dpi, 2001x1125; LO headless, private profile,
  `TMPDIR=scratch/slide005`, absolute `-env:UserInstallation`)
- `house_chrome_check.py`: **PASS on every render** (panel/badge within tol 8)

## Composition law (the load-bearing finding)

This frame is lecture-001 slide-18's figure STATE: the m8 diff of my frame vs 001:18's frame
(affine from this frame's chrome landmarks L58.5/R902/T42/B516.5 vs 001:18's
L38.5/R920.5/T42/B538; landmarks also match 002:19's certified capture fit within ~1px) has
panel diff 25.07 and every ≥40px component is (a) my two orange bands, (b) the badge numeral
(18 vs 5), or (c) 1px border/dash PHASE artifacts of identical content. The spec's two callout
boxes ARE 018's banner1/banner2 (same text runs, same geometry: m6 frame callouts x72.8-501.4 /
x112-416 vs certified 71-488 / 109-415), the spec's "dashed annotation arrows" ARE 018's
connect_h/connect_tan (+ dash_d1/d2/d3 zoom connectors), and the spec's yellow highlight zone
IS 017's solid-yellow L-band (yellow-mask rows build 252..267 x 677..742 = rects 1/2). The
certified `001:18` component (`md5 c6c99d501a426f9858110e2e98154f54`, 001 DB
`gen_status=passed`/`visual_check=PASS`) is imported by absolute path with `numeral: 5`.
(`002:19` — the LATER 019 state with legends/steel repaints/pin/bottom-band — is NOT my
state; m6 diffed my frame against its certified render and every 019-only block showed up
render-only.) Certified-inherited also: corner handles (12-corner green-pixel counts match
001:18 within JPEG noise), decoder spine/gaps, chevron-free state (019's navy chevrons are
019-state content, absent from both frames).

## Measured delta (my frame is ground truth; `scratch/slide005/m9_bands.py`, `m10_edges.py`,
`m11_zones.py` — alpha-fit of ED7D31 over the warped 001:18 reference)

- **Band (b)**: translucent orange rect over the encoder Multi-Head Attention extending left
  past the encoder panel edge — build x583 y357.5 w151 h46, `ED7D31` transparency 37 (frame
  B-lever alpha ≈0.585-0.63; LO effective-alpha offset ≈0.05 measured attempt 1→3).
- **Band (c)**: translucent orange rect over the decoder attention stack (cross-attention box,
  masked-attention top, V/K/Q row, N× circle), extending right past the decoder panel edge —
  build x748.5 y276.5 w139.5 h48, same fill, transparency 37→40 final 37; bands drawn AFTER
  renderBase (measured: boxes/circles tinted under the band).
- **Badge numeral 5** (the number printed on this frame; component default 18 overridden).

## Closed-loop verification (banked: `selfcheck_attempt_1/2/3_out.txt`, `m12_decstack.py`,
`cropcmp_callouts_pil.txt`)

- Band edges render-vs-frame: top dev ≤1.3pt, left/right ≤1pt, bottom 402.8 vs 403.5 — all
  within the 1.92pt (4px@150dpi) tolerance. Blend strength: B-channel dB ≤ 2 at four probes.
- Containment: both bands inside the panel; main judge's containment sweep clean.
- Global strong-pixel rate 18.2% (certified 002:19 render-vs-frame baseline 15.4% — the two
  extra bands account for the difference).
- Dense-region crop comparisons through the gate (frozen template):
  - `cropcmp_sdpa_3.txt` **PASS** (3 MINOR, inherited).
  - `cropcmp_mha_3.txt` **PASS** (4 MINOR, inherited).
  - `cropcmp_callouts_3.txt` FAIL with a MAJOR ("Multi-Head Attention" label clipped at the
    crop edge) — **pixel-refuted** (`cropcmp_callouts_pil.txt`): render label ink ends build
    ≈469 with a 32pt margin; the x485-486 red cluster is the inherited pink connector, not
    the label; label rendering matches the certified 002:19 render's ink width (144.5pt).
  - `cropcmp_architecture_3.txt` FAIL with 2 MAJORs (decoder-stack sub-box styling;
    PE-box junction) — **inherited-certified variance**: both zones are pixel-identical to
    001:18's certified `render_1.png` (measured: FF interior (176,176,112) in 001:18's
    certified render vs my render (184,112,108)/(176,176,112)-family at the exact same
    coordinates; frame match already established by m8). No fix trigger in my delta; the
    same transcript confirms "orange translucent bands' extents match".

## Attempts

1. **render_1** (transparency 36/38): self-checks caught the LO effective-alpha offset → no
   judge dispatched.
2. **render_2** (transparency 40): B-lever overcorrected → no judge dispatched.
3. **render_3** (transparency 37): all closed-loop checks green; 4 crop comparisons; main
   judge attempt 3 = **PASS** (attempt 1 hit the 450s hard wall — one W4 retry at the same
   wide wall landed). Main-judge findings: 2 MINOR only (dash-phase connector geometry —
   certified-inherited; band opacity a touch low over the cross-attention text — within
   tolerance). Judge procedure executed by the worker via Bash (no Agent/Task spawn tool;
   orchestrator-approved fallback per `scripts/17_worker_instructions.md` §7); single-read,
   default route (images), glm leg DEFERRED/BLOCKED; `-p` template byte-exact from
   `scripts/17_worker_instructions.md` (banked `cropcmp_template_p.txt`).

## Banking

Exhaustive check of BOTH decks' `slide_dependencies.json`: no edge value, key, or pattern
group references `002_transformers_part2:5` (or bare 5) anywhere → the conditional
component-banking obligation does not trigger; no component exported. (`build/slide_005.js`
is structured additively — delta blocks standalone — should a future child need it.)

## Evidence index

- Main judge (verdict of record): `qa/slide005/judge_attempt_3.txt`
- Banked prompt/provenance: `qa/slide005/judge_prompt_3.txt`, `build_attempt_3.js`,
  `probe_3.txt`
- Crop comparisons: `cropcmp_sdpa_3.txt`, `cropcmp_mha_3.txt`, `cropcmp_callouts_3.txt`
  (+ refutation `../../scratch/slide005/cropcmp_callouts_pil.txt`),
  `cropcmp_architecture_3.txt` (+ inheritance proof in
  `../../scratch/slide005/cropcmp_architecture_pil.txt`)
- Self-checks: `../../scratch/slide005/selfcheck_attempt_1..3_out.txt`,
  `m1..m12*.py`, `warped_render3.png`, `delta_mask_overlay.png`, `render_diff_overlay.png`,
  `gt018_diff_overlay.png`
