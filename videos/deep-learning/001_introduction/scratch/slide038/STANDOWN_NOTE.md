# Slide 038 — worker stand-down note (collision protocol)

Worker dispatched ~07:02 (re-dispatch after the 07:00:53 predecessor died ~5 min in).
Sweep at 07:02-07:03 was CLEAN (empty qa/slide038 + scratch/slide038, DB row
gen=building updated 07:01:34, no build script) — proceeded as sole owner.

## PEER DETECTED at 08:03 — STOOD DOWN READ-ONLY
- DB row slide 38 touched again at 07:50:25 (gen=building, no other fields) — not by this
  worker (this worker ran zero DB writes).
- Peer asset files appeared in recreated_pptx/build/assets/ at 08:02 (one minute before
  this check): slab038_brown.png/.json, slab038_stack.png/.json — a parallel worker
  running the same measured-asset approach.
- Per the collision protocol ("if a peer is actively writing: stand down READ-ONLY;
  take over only after >=40 min peer silence + zero artifact movement + mid-state DB
  row"), this worker ended WITHOUT building, judging, or writing the DB.
- The peer is sole owner from ~07:50. Banked evidence untouched (never delete).

## Banked by this worker (reusable, all under scratch/slide038/ — read-only forensics)
13 measurement passes on the ground-truth frame (960x540, 1px=1pt), all banked here:
- m1.py/out_m1.txt — global bands, red/blue box borders, formula text lines.
- m2.py/out_m2.txt — ASCII color map (whole frame), title bbox/color, black bar extent,
  formula per-line ink bboxes.
- m3.py/out_m3.txt — dark-crimson mask: top rule y43 x58..901; panel left bar x58
  y43..517; diagram box x183..809 y251..510; title ink x333..632 y68..100, F-stem cap
  y69..92 (24px), word gap x434..447.
- m4.py/out_m4.txt — rule/border segment proof: NO right/bottom panel border in this
  frame; formula box border reconciles to NAVY #000080 (chroma-ratio fit; spec's
  #3333CC loses to ink, deck navy certified law slide_005/030).
- m5.py/out_m5.txt — connected components: image slab hexagon x250..347 y294..440
  (main (175,104,19), light left strip (215,129,24) x250..267 y358..440); 5 filter
  slabs x393..548 y336..400 (~29px pitch, overlapping hexagons; cyan (28,167,191)+
  bright (16,190,232), green (29,163,69), red (211,0,2), yellow (238,224,14)+
  (204,218,13), purple (104,33,127)+(86,28,123)); 5 output circles: colored cores
  ~20x16 (cyan x616..635, green x654..673, red x691..712, yellow x729..750, purple
  x769..787, y361..376) inside tan rings (204,134,39) ~30x24; dashed lines 4x at
  y~356/366/376/387 x258..393; black-ink components (annotations).
- m6..m13 — fine maps: 'RGB' x297..363 y268..283; '3 dims' x222..272 y332..340 +
  arrow y345.5 x228..~285 into the slab edge; 'X' x354..374 y337..352; '7' left edge
  x236..248 y373..385; BIG '7' inside slab bottom-right x272..318 y392..440 (top bar
  y392..399 + stem to (272,436)); '3' x396..410 y403..411 + pencil doodle x411..425
  y404..436; '=' light-blue x572..592 y363..373 (modal (136,205,219)); circles pitch
  ~38px centers y368.5; arrow fan from (462,464) to 5 tips (400,405),(433,402),
  (460,402),(486,402),(514,402); '735 weights' x378..550 y472..494.
- gen_assets.py/out_assets.txt — quantized-redraw asset generation (slab + stack PNGs
  at 8x, dash/tip inpainting) + font solves: title Times New Roman Bold 38pt (w301 vs
  300 target; Arial Bold 35pt alt); formula L1 TNR-Bold 21pt (714 vs 716);
  annotations Comic Sans MS solves in out_assets.txt.
- Assets written by this worker (banked, unused by anyone yet):
  recreated_pptx/build/assets/slab038_image.png (image slab, bbox x246..353 y289..447),
  recreated_pptx/build/assets/stack038_filters.png (filter stack, bbox x388..554
  y330..420).

## Key facts the next worker should not re-derive
- The spec's three '7' annotations (above stack / mid-height between slabs / right of
  purple slab) are NOT present in the kept frame's pixels (multi-threshold scans,
  m8/m10/m11/m12) — only two '7's exist: left edge (x236..248 y373..385) and the big
  in-slab bottom-edge one (x272..318 y392..440). Spec's "5 dashed lines" is actually 4
  (y356/366/376/387). Ink forensics win per building.md / slide_008 precedent.
- Black bottom bar (x38..921 y518..539) = player artifact: certified-precedent split
  (029/040 omit per ground rule (c); 005/010/030 draw); THIS slide's spec step 18 says
  omit — omit and cover under judge ground rule (c).
- Original's top rule y43 + left bar x58 = the deck's own panel chrome — replaced by
  the canonical playlist chrome (drawHouseChrome, numeral 38), per certified
  slide_005/006/010 precedent and ground rule (a).
- Formula box border = navy 000080 (see m4); box x90..879 y117..234; text left x149;
  baselines ~152.5/187/223.5 (pitch ~35.5).
- Diagram box red C00000 x183..809 y251..510.
