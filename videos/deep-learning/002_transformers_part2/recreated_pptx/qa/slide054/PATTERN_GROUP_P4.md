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
