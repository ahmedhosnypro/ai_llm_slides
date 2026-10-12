# Worker report — slide 048 (001_introduction, Deep Learning DSAI 308)

**Slide:** 48 — "Standard Neural  Network (NN) vs  Convolutional Neural Network (ConvNet/CNN)"
**Deliverable:** `videos/deep-learning/001_introduction/recreated_pptx/slide_048_recreated.pptx`
**Build script:** `videos/deep-learning/001_introduction/recreated_pptx/build/slide_048.js`
**Final verdict:** **PASS** (visual judge, attempt 4; real comparison transcript)
**Judge attempts used:** 1 (dispatched as attempt 4, after 3 pre-judge self-check iterations; 1 of max 6)
**Dependency status:** `root` (no `depends_on`); no same-video or cross-video dependents
(002's graph references only 001_transformers_part1; this video's edges: 16←9, 17←16, 18←9,
19←9, 25←24, 37←36, 41←35) → **no component-banking obligation**.

## DB milestones
- `gen_status`: building → judging → **passed**
- `pptx_path`, `build_script` set; `visual_check=PASS`, `visual_attempts=4`,
  `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide048/judge_attempt_4.txt`

## Method / evidence chain
1. **Measurements** (PIL, 960×540 frame, 1px=1pt): `scratch/slide048/measure_1..15.py` —
   content frame x58..894 y135.5..448.5 (+inner-left line x65), title 2 lines Arial-Bold
   baselines 84/119 (cap 21px), label boxes x242..379/x242..480 (y155..182/y278..305),
   meme photo x248..360 y191..252, tag x387..422 y157..183, 7-dot column (cx405.5, cys
   195.5+8.33k), 6 NN blocks (y186..255, pitch ~47), CNN slab chain (bottom-lefts 229/311/
   399/477/554/635, y~315..425), blocks 7-9 (x735/782/829, y333..403), divider y269
   (dash-dot), red arrow y462.5 x169..831 (head tip x831), caption x354..~596 y466..479.
2. **Vision build-input forensics** (analysis through the gate, 2× crop of label box + tag +
   dots): comic-style dark-charcoal (#333333) text in square blue-bordered boxes; tag text
   bold; dot colors. Banked: `scratch/slide048/dense_crop_analysis.txt`.
3. **Crops from the original frame** (photos/complex 3-D artwork per the certified
   slide_029 precedent, exact-size embed): `build/assets/s048_meme.png` (114×65),
   `s048_siamese.png` (105×118), `s048_cnn_chain.png` (465×128 — six 3-D slabs with baked
   white labels + red Conv overlines + blue Non Linearity notes + gap arrows).
   Native drawing for everything else (frame, title, label boxes, tag, dots, NN blocks with
   vert270 white text, FC/OP overlines, arrows, divider, bottom arrow, caption).
4. **House chrome:** `shared_patterns/house_chrome.js` `drawHouseChrome(..., {numeral:"48"})`;
   `house_chrome_check.py` PASS on every render (1,3,4). Badge numeral = 48 = slide file
   number — **assumption PENDING FOUNDER VETO** (001_introduction/AGENTS.md 2026-10-12;
   frames carry no printed numbers). Chrome drawn at canonical playlist values; this
   frame's own washed panel border sits inset (x58) — covered by judge ground rule (a).
5. **Pre-judge self-checks** (banked): `selfcheck_attempt_1.py/_out.txt` (found 3 real
   deviations: title −3% width, label text narrow, caption wrong font family/width),
   `selfcheck_attempt_2.py/_out.txt` (after fixes: all geometry PASS; 5 residual sub-6px
   marginal items noted). Fixes applied between iterations:
   - it.1→2: title 29.5→30.5pt (width-solved), label text 14→16pt (Comic Sans MS,
     width-solved), caption Arial→Comic Sans MS 13.5pt + charSpacing 0.9 (width-solved:
     Arial rendered 202px vs original 242px), FC/OP 13→13.5pt at measured ink centers.
   - it.2→3: overline centers → measured (NN FCs 461/508/554.5/600.5, O/P 651; CNN 744.5/793.5).
6. **Mandatory dense-region crop comparisons** (render vs original, ~2×, through the gate):
   - `cropcompare_A.txt` (label box + tag + dots): caught 2 MAJORs — original tag text is
     BLACK bold upright (not red italic) and reads as yellow highlight behind text → fixed
     (text 000000 bold upright 9pt; yellow rect footprint kept — black glyph coverage
     reproduces the highlight look). Also label border 1.75→1.5pt.
   - `cropcompare_B.txt` (slabs 1-2 + Conv + Non Linearity + photo edge): **CROP VERDICT:
     MATCH** (2 MINORs: NL note ~3-5px, connector line slightly thicker — both inherent to
     exact-size crop embedding).
7. **Render:** 150dpi, private LO profile (`scratch/slide048/lo_profile`), TMPDIR=scratch
   (/tmp quota-blocked). Renders banked: render_1/2/3/4.png; build_attempt_2/3/4.js.
8. **Judge (attempt 4, self-executed per 17 §7 fallback — no Agent/Task spawn tool in this
   environment; orchestrator-approved):** probe → gateway window never opened (no probe
   transcript; re-probe after sleep 300 per procedure) → full comparison landed at the W4
   wall on the first try (degenerate events: 0). Transcript:
   `qa/slide048/judge_attempt_4.txt`. Prompt banked: `judge_prompt_4.txt` +
   `judge_p_payload_4.txt` (deck-adapted ground rules per certified slide_029 convention).

## Judge findings (attempt 4 — FINAL VERDICT: PASS)
5 MINOR findings, no BLOCKER/MAJOR:
1. "Flatten" italic styling vs bold upright (MINOR, high conf) — note: the crop comparison
   read the original as bold upright black; judge read the original as italic-bold. Typed
   styling variance on a 9pt label; accepted.
2. Dot column ~7 larger dots vs ~8 finer (MINOR, medium) — PIL counted exactly 7 in the
   original (195.5+8.33k) and the render reproduces those positions; judge count at full
   slide is an estimate.
3. NN FC blocks slightly taller proportionally (MINOR, medium) — blocks are y186..255 =
   70px in both (PIL-verified; render band 387.5..531.3 vs exp 387.5..531.25).
4. "Max pool. 2" grazes slab right edge — original mirrors it (baked crop = original pixels).
5. "Non Linearity" horizontal nudges of a few px (crop-compare: ~3-5px at 2×) — baked-crop
   resampling, sub-1% of slab pitch.

## Deviations / notes
- Judge procedure executed by the worker (no spawn tool) — per 17 §7 fallback, byte-for-byte
  prompt, verdict taken verbatim from the comparison winner body.
- Probe transcript absent (gateway window never opened during probes; comparison itself
  succeeded first-try at the wide wall) — noted as the only method deviation.
- Excluded per spec recreation_brief step 25 + judge ground rule (c): black video-player
  strip (y519..539) and gray '+' annotation mark (~x710, y~475).
- No equations on this slide (spec: "No bullet lists, no numbered items, no equations") —
  Math equation format rule N/A; OMML/graphgen passes N/A.
- Attempt numbering: renders 1-3 were pre-judge self-check iterations; the judge dispatch
  (attempt 4) is the 1st of the allowed 6 judge attempts.
