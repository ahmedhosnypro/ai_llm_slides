# Worker report — slide 033 (Self Attention Mechanism, Linear Transformation of Inputs)

Deep Learning DSAI 308, Transformers — Part I (`videos/deep-learning/001_transformers_part1`).
Build worker run 2026-10-11/12. Fresh start (prior worker died on a provider timeout with
nothing banked in `qa/slide033/`; its scratch measurement passes in
`scratch/slide033/` — f1..f11, meas/p1..p9, measure1.py, vread_A..K, crops A–R — were
reused as geometry provenance).

## Result

**PASS** — attempt 3. Deliverable: `recreated_pptx/slide_033_recreated.pptx`
(single plain-named version; no equations-PNG / OMML scope on this slide — the legend's
schematic is drawn natively as in the original, no mathtext, no advanced graphs).

| milestone | value |
|---|---|
| gen_status | `passed` |
| visual_check | `PASS` (attempt 3) |
| visual_attempts | 3 |
| visual_transcript | `qa/slide033/judge_attempt_3.txt` |
| build_script | `recreated_pptx/build/slide_033.js` (thin wrapper) |
| certified component | `recreated_pptx/build/components/slide_033.js` — banked per the playlist-scoped obligation (lecture 002 depends on slide 33); verified 0-pixel-diff (0 of 2,251,125 px) against the certified render after the refactor |
| chrome check | `HOUSE CHROME CHECK: PASS` on every render (playlist chrome, badge numeral 33) |
| judge procedure | executed by the worker (no Agent/Task spawn tool in this environment — documented 17 §7 fallback); verdict taken verbatim from the comparison winner body |

## Attempt history

- **Attempt 1** (`render_1.png`): full frame-true build from PIL forensics
  (`scratch/slide033/w1_families.py`, `w2_maps.py` → `meas/w2_maps.txt`, `w3_edges.py`,
  `w4_truth.py`, `w5_conn.py`, `w6_micro.py`) + gated [?] re-checks
  (`scratch/slide033/crops2/q1..q4` + reads). Self-check caught: V labels 12px too low,
  LO tightening the title's 24pt spcPts (fixed by splitting the title into two pinned
  boxes). Self-check PASS after fixes.
- **Dense-region crop comparisons** (mandatory check 6; `qa/slide033/crops/`): legend FAIL
  (right strip top-aligned vs W-midline), kcol PASS, sentence FAIL (W_q↔X₂ arrow flipped),
  y2sigma FAIL (block arrow vertical vs diagonal NE; Y₂ label oversized). All fixed.
- **Attempt 2** (`render_2.png`): self-check PASS; re-crops: legend PASS, sentence PASS,
  y2sigma FAIL (regression: the small "2" pushed below the widget; judge + a decisive
  pixel dump showed the head points UP into the W_q box, tip ~y462).
- **Attempt 3** (`render_3.png`): "2" moved inside cell 3 hugging Y's lower-right; green
  arrow shortened; darker red triangle. Self-check PASS, chrome PASS, y2sigma re-crop
  PASS. **Full judge: PASS** — 4 MINOR findings, no BLOCKER/MAJOR:
  1. "K.q" label sits just inside the DP box's top-right corner vs just outside/above in
     the original (MINOR, high conf).
  2. Translucent red K₂ highlight circle slightly larger/more saturated (MINOR).
  3. ⊗ circles / Σ box proportional scale drift ~5–10% (MINOR).
  4. Diagram-label fonts slightly heavier/larger (MINOR).
  Per the verdict law these are banked as findings, not fix triggers, against a PASS.

## FRAME-VS-SPEC corrections applied at build (frame is ground truth; SOURCES.md
anticipated each as a build-time re-check)

1. Embedding widgets are FIVE-cell strips with the label in the CENTER cell — the spec's
   "white box + 3 squares" misread the tiny full-frame; confirmed by vread_A/G/H/I + q3.
2. Side-container rows read **X₄, X₃, X₂, X₁ top→bottom** (crops2/q3) — resolves the
   K-ordering tension recorded in SOURCES.md (row-wise pairing Xᵢ↔Kᵢ now consistent).
3. W-matrix labels read **W_k^(r) / W_v^(r) / W_q^(r)** — superscript "(r)" in lighter
   tan-olive, NOT "(1)" (two independent high-zoom reads: crops/vread_F + crops2/q1).
   Spec's `W_k^(1) [?]` resolved by frame evidence.
4. Dot-Product corner label reads **"K.q"** — NO subscript (crops2/q2); the spec's
   "K₂q [?]" subscript-2 was a dot misread.
5. Legend labels are **"1\*d" / "d\*d"** with literal asterisks and baseline "d", no
   middle-dot separator; "=" red-brown; caption **"d: Embedding Length" navy blue**
   (crops2/q4 + crops/vread_H). The spec's verbatim "1^d · W(d*d) = 1^d" described the
   math, the frame prints 1*d — frame wins for recreation.
6. Pill text is **indigo-blue** (#3F3F8F), not dark red (crops/vread_K + measured cores).
7. The peach diagram panel (#F7E2CD, thin gray border) sits INSET on the chrome gray
   panel (x51..868, y107..522 frame px); the spec's full-panel maroon border was the
   chrome's own red strokes bleeding into the JPEG.
8. Connectors: only the right vertical dashed green (x802, arrowhead up into the right
   container, lower end running behind the legend) + a small green up-arrowhead stub
   under the LEFT container. The spec's full L-shaped left connector and horizontal
   segment are NOT in the frame (pixel-verified empty peach).
9. Arrow topology corrections: the W_q↔X₂ connector points UP into the yellow box
   (X₂ → W_q flow; judge + pixel-verified); the Σ→Y₂ green arrow is diagonal NE; no
   visible softmax→circle lines (only short right stubs with left arrowheads at circles
   rows 2–4; row 1 has none — pixel-verified).

## Evidence index (all under `recreated_pptx/qa/slide033/`)

- `judge_prompt_3.txt`, `judge_template.txt` (frozen template), `build_attempt_3.js`
  (certified pre-refactor build), `probe_3.txt`, `judge_attempt_3.txt` (comparison
  winner body → PASS)
- `selfcheck_attempt_1/2/3.py` + `selfcheck_1/2/3_output.txt` (containment incl.
  playlist white-margin adaptation, equation-region ink, title band/pitch, spacing pins,
  fill presence) — attempt 3 PASS
- `render_1.png`, `render_2.png`, `render_3.png` (certified), renders also under
  `scratch/slide033/render/`
- `crops/cmp_legend.txt` (FAIL→fix), `cmp_kcol.txt` (PASS), `cmp_sentence.txt`
  (FAIL→fix), `cmp_y2sigma.txt` (FAIL→fix), `cmp_legend_2.txt` (PASS),
  `cmp_sentence_2.txt` (PASS), `cmp_y2sigma_2.txt` (FAIL→fix), `cmp_y2sigma_3.txt` (PASS)
- Geometry provenance: `scratch/slide033/` (w1..w6 passes, `meas/w2_maps.txt`,
  `meas/w4_truth.txt`, prior worker's f/p passes + vreads), `scratch/slide033/crops2/`
  (q1..q4 re-check reads)

## DISPATCH FLAG (for the orchestrator)

At dispatch time `VIDEO=deep-learning/001_transformers_part1 python3 scripts/15_progress.py
buildable` printed an EMPTY dispatch list even though slide 33 passed both gates
(analysis/slide_033_final.json = gate-passed PASS_WITH_FIXES, score 9; `deps` showed
33 as `root`, i.e. no dependency and no pattern gate). Slide 33 was buildable but was
omitted from the v2 `buildable` output. Likely cause: the DB row's `validation_status`
was still `pending` (the `sync` refresh hadn't been applied for this slide at that
moment) so the content gate in `buildable` saw the stale DB value rather than the
passed analysis/final JSON. No data loss — the dispatcher's own list was simply
incomplete; this worker proceeded on the root/deps evidence.
