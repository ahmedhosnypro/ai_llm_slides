# PATTERN GROUP P4 — masked self-attention diagram [54, 55]

Established by slide 054 (P4#1, certified HEAD — judge PASS 2026-10-12,
transcript `judge_attempt_7.txt`). Slide 055 (P4#2) MUST reuse these
conventions — verify them against 055's own frame, never re-derive. Pattern
reuse ≠ content dependency: 055 draws its OWN frame's content; only the
CONVENTIONS below transfer.

## 1. Frame→slide mapping (measured from THIS deck's frames)

All 002 frames are ~0.958 zoomed-out with black letterbox (deck AGENTS.md).
For slide 054 the four chrome landmarks: left border x=59, right x=902,
top y=42, bottom-border y=516 (frame px, 960×540, 1px = 1pt). Mapping:

```
X0 = 18.63, SX = 0.96123, SY = 0.95556
sx(fx) = (fx - X0) / SX   # frame px -> slide pt
sy(fy) = fy / SY
IN(pt) = pt / 72          # slide pt -> inches (pptxgenjs)
```

Slide 055 must re-fit ITS OWN four landmarks (they can differ by ~1px) and
re-derive its own constants.

## 2. TWO UNIT-CONVENTION TRAPS (both bit this build)

1. NEVER nest IN(): `IN(SM_CX - IN(70))` subtracts 0.97 INCHES from a POINT
   value — the rotated label's box lands with its top-left at the intended
   CENTER (displacement +w/2,+h/2). Correct:
   `x: IN(SM_CX - 70), y: IN(SM_CY - 11), w: IN(140), h: IN(22)`.
   Closed-loop proof: render_1 purple "Soft max" strip center frame (590.1,
   272.9) vs intended (523,262) = +67,+11; after fix (523.5,262.3).
2. ONE coordinate convention per helper. seg()/head() take FRAME px and map
   internally via sx/sy. Mixing conventions (passing frame px where the
   helper expected slide pt) displaced every new shaft ~10px UP (237.5 frame
   px read as 237.5 slide pt = 227 frame px) — exactly the "shaft under the
   fraction, head at the cell" judge finding. Banked evidence:
   `rotlabel_centers_2.txt`, `c5_followup.txt`.

## 3. Rotated labels — pptxgenjs rotate works in LO; anchor + size need
##    closed-loop calibration

Wide-box + `rotate: 90|270` + align/valign center renders CORRECTLY in
LibreOffice headless. But the frame anchor must be measured per label:
redness-profile scan of the column (fill baseline ~34) finds the text-ink
start row precisely — 054's Scaling strip is frame y 229..358 (em ≈ 21pt,
reads TOP-TO-BOTTOM = rotate 90, "S" at top), Mask y 192..227 (em ≈ 14pt,
bottom-to-top = rotate 270), Soft max y 256..284 (em ≈ 8.5pt, rotate 270).
Label sizes within ONE diagram vary wildly — never copy one em to another.
Verify with the per-row strip scan after render (target ±3px).

## 4. Arrow language (redness-forensic model — verify per frame)

Connectors are FAINT THIN SHAFTS (~0.75pt, redness elevation ~+10 over the
pink panel) + COMPACT HEADS (~9x6 frame px) near the target edge; full
strong shafts (1.75pt) only where the frame shows them (054: the K->dot
corridor x 266..328). Some gaps have NO connector at all (054: Wk->Kstrip,
Wv->Vstrip). Head direction from JPEG mush is settled by the SATURATION
GRADIENT: peak redness near the base, steep falloff on the tip side
(054 F head: peak 144 at x448, falls to 19 by x452 → tip toward Mask →
flow is Scaling->Mask RIGHTWARD). One judge misread this blob's direction;
the gradient + a second judge read settled it. Flows follow the
left->right pipeline.

## 5. Embedding-stack primitive (frame reads BOTTOM-UP)

Left/right dashed containers: rows carry **Z4 at TOP → Z1 at BOTTOM**. Each
row: yellow chip (FDFD96) + red bold Z label + 2 pale-lavender cells
(EEF0F5 — NOT green; the spec's "green squares" was corrected by frame
measurement). Row y-tops (054): 231, 270, 310, 352. Bottom container strips
read LEFT→RIGHT Z1..Z4, strip 2 (Z2) magenta DA70D6 + dashed 8B4789 border.

## 6. Palette measured from THIS frame (overrides spec hexes where they differ)

RED C00000 (title/arrows/red labels) · PANEL F5CFF6 · CONT_FILL E4FBE7 ·
CONT_LINE 92D050 dashed · CHIP FDFD96 · PALE_CELL EEF0F5 · WK_FILL C9E9C6 ·
WV_FILL BEECF1 + line 5B9BD5 (W_v light BLUE) · TAN D8C8B9 · SCALE_FILL
F7D3D6 · MASK_FILL B9E8C6 + line 3E7A3E · MASK_LABEL 23844D (green) ·
MASK_CELL F6F6BE with khaki border 8C8250 and DARK RED text C00000 ·
SOFT_FILL F7DCF9 · SOFT_TEXT 7030A0 (purple) · SIGMA_FILL E1F3F8 ·
NAVY 000080 (Σ, legend caption) · DOT_NAVY 1B1F95 · PILL_FILL F0F0D8 +
text 333366 · OUT_FILL A4C6A2 · GREEN_ARR 00B050 · MAG DA70D6 · WQ_FILL
F2BCD8 (no border).
Frame-truth verifier: `frame_truth_2.py` (banked here).

## 7. Diagram structure conventions (054's frame facts)

- 4 ⊗ nodes on a descending diagonal (054: frame (558,238),(588,275),
  (618,312),(648,349), d≈16); softmax fan heads enter node left edges;
  V heads at node right edges; UP heads under the Σ box.
- 4 navy dots inside Dot Product box on the same descending diagonal; thin
  red segments interconnect consecutive dots.
- Fraction "K·q/√d" = ONE mathtext PNG (`render_eq.py '\dfrac{K \cdot q}{\sqrt{d}}'
  12 '#C00000'`) embedded at exact px/600. NOTE: pass the hex WITH '#':
  matplotlib parses a bare `C00000` as CYCLE COLOR C0 (blue!) — one render
  came out navy and the fraction region read as MISSING red ink.
- "K·q" middle dot (U+00B7): three independent zoom reads of the frame say
  dot/period, never comma (spec's "K,q" was a full-frame misread).
- Dashed green curved connectors (bottom container → side containers) =
  600dpi transparent PNGs (`build/assets/conn_left.png`, `conn_right.png`,
  generator `gen_connectors.py`).
- OMIT as video artifacts: black letterbox strip + bottom-left black corner
  bar (ground rule (c); spec brief step 41).
- Red block-arrow below the bottom container points STRAIGHT UP at Z2
  (apex x≈291 y≈490 — frame-measured per-row spans).

## 8. Dense-region crop comparisons MUST be EQUAL SCALE

Crop pairs sent to analyze_image.py comparison: resize the RENDER crop to
the ORIGINAL crop's pixel grid before upscaling both ×3. Unequal-scale
crops made one judge report the fraction "2.5× larger" (it was 2.17× crop
zoom, not a build defect) and poisoned an entire verdict round.

## 9. Mandatory pre-judge additions for P4 members (lesson from 054)

- Rotated-strip center checks (see `selfcheck_attempt_2.py` checks `rot_*`).
- Arrowhead presence + B/K2-style negative-gap checks.
- Shaft continuity (a 0.75pt seg that silently fails to render was only
  caught by the judge — assert ink along each shaft's midline).

## Banked evidence for 055

- `qa/slide054/selfcheck_attempt_2.py` + `selfcheck6_output.txt` / `selfcheck4_output.txt`
- `qa/slide054/frame_truth_2.py` — frame color/shape verifier
- `qa/slide054/rotlabel_centers_2.txt` — before/after unit-bug numbers
- `qa/slide054/build_attempt_7.js` — CERTIFIED build (pattern source)
- `qa/slide054/judge_attempt_7.txt` + `crop_eq_frac_*.txt` — evidence chain
- `scratch/slide054/f_head_forensics.txt` + `shaft_redness_scan.txt` —
  redness-forensic method for tiny arrowheads
- `build/assets/eq_Kcdotq_over_sqrtd.png` — mathtext fraction asset
- `build/assets/gen_connectors.py` — curved-connector PNG generator

---

## 10. P4#2 (slide 055) verified conventions — addendum 2026-10-12 (group complete)

Slide 055 reused every section above (mapping constants byte-identical — landmarks
58-59/901-902/42-43/516-518 ≈ 054's within 1px; badge cross-check identical). What
055's own frame MEASURED DIFFERENT, banked for any later member of a group reusing
this family:

- Same descending diagonals for dots AND nodes (within 1-4px of 054's), but boxes
  shifted: Dot Product box WIDER [289,186,409,388] (054: 265..347); W_k/W_v boxes
  ~24px right of 054's; Scaling/Softmax columns shifted right ~27px and NARROWER
  text ems (Scaling 20pt vs 21; Soft max unchanged 8.5 + two-line wrap confirmed
  = the frame's own 2-band strip).
- NO Mask column in 055 — the Scaling column abuts the Softmax column directly.
- ARROW LANGUAGE re-measured (do NOT carry 054's per-gap verdicts): Y->W_k arrows
  DARK RED 8B0000 heads at x~192 + faint shafts; W_k->K thin RED connectors EXIST
  (x 229..243 — 054's "B: no ink" does NOT transfer); Y->W_v RED HEAD-ONLY at
  x~762 (no shafts); softmax->node and V->node heads confirmed at (nx-13)/(nx+13.5),
  head-only; K->dot lines run the FULL box width (x 264..407) — they pass THROUGH
  the dots; K1's head is strong (redness 128), others faint.
- Fractions/labels: K·q label INSIDE the tan box top-right [378,192]; fraction PNG
  immediately RIGHT of the Scaling column top (ink [446,185,471,218]); closed-loop
  fraction check PASSED at ±4px @150dpi with the reused 054 asset.
- Z-row: STADIUM container + DASHED DARK GREEN border (2E7D32); 5-cell strips with
  graduated tints; Z2 = dashed crimson rect INSIDE the container + graduated magenta
  cells; labels at measured x (S1 252, S2 300, S3 396, S4 469).
- 3D block arrows at the slide edges point OUTWARD (shape-profile settled: triangle
  bases at the hatched boxes) — a 3x crop read misread them as inward; trust the
  per-row ink-extent profile over a single vision read for arrow direction (P4 §4).
- Hatched "From Encoder Output" boxes: hatch runs the WHOLE box (45° red strokes,
  ~5px pitch), not side bands.
- Y rows: 6 pale cells (thin pink borders) + red label at the left end of cell 3
  (~1/3 in) — NOT centered, NOT right-end.
- Legend: labels RED (1×d below the glyph, d×d below the W, 2nd 1×d horizontal at
  [866-882]) + maroon "="; caption NAVY 1C1F86. W square [792-827] cream/amber.
- Caption "From Decoder / Self Attention Layer" sits on a WHITE box with thin pink
  border, text CENTERED; white 3D arrow with lavender outline points LEFT.
- Z-row FINAL measured truth (after 3 fix rounds): magenta cells y 465..487 (5 cells
  [300,315,330.5,341.5,352], bright F57DBD 3rd), dashed rect [298,464,367,488] hugging
  ONLY the magenta cells, Z2 label ON cell 3 (~x325); S1 = 7-cell strip, label at the
  measured ink x 255; post-label cells COOL bluish/lavender [DDE2F6/E9ECF8/F2D8F0];
  Z-arrow = flipH rtTriangle [299,489.5,322,501.5] (vertical right edge + down-left
  hypotenuse — pixel-identical to the original).
- JUDGE-VARIANCE LAW (2nd precedent after 054's F-head): the zrow crop read failed 5
  rounds with mutually-contradicting MAJORs; the two findings surviving round 5 were
  refuted by ink scans (arrow placement pixel-identical; "intruder" pale cells present
  in the original). Full-slide judges passed the region 3x without a MAJOR. Bank the
  ink-scan override WITH the crop transcripts — never re-litigate from a single read.
- Evidence: qa/slide055/{crop_pair_*.txt, judge_attempt_1/2/3.txt, worker_report.md},
  scratch/slide055/{measure_*.py, forensics*.py, selfcheck*.txt},
  build/slide_055.js (certified build v8).
