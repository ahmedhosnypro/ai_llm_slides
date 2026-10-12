// P2 MEMBER NOTES — slide 021 ("[1] Position Encoding", P2#2) — for slide 22 (P2#3)
// and 34 (P2#4). Base convention: ../../slide020/p2_row_lane_pattern.js (STILL
// BINDING). This file records what member #2 re-measured/changed on ITS frame —
// re-measure YOUR frame the same way; none of these numbers transfer blindly.
//
// 1. MAPPING (per-frame!): 021's chrome landmarks measured left 58.60, right
//    901.38, top 43.14, bottom 516 (letterbox edge) -> ax=18.13, sx=0.961231,
//    ay=0, sy=0.955556. 020 used ax=18.628 (its left stroke sits 1 frame px
//    right of 021's). FIT YOUR OWN four landmarks with red-weighted subpixel
//    centroids; a 1px landmark error shifts everything ~1pt.
//
// 2. COLUMN GRID: 021 shares 020's pitch (73.4-73.5) but is shifted: box edges
//    [177,236],[250,309],[324,384],[397,457],[471,530],[544,604] + gap +
//    [732,796],[808,872] (020: centers 211.5+73.4k, boxes 7/8 at 769.5/843.5).
//    Row-1 digits sit +3.5 frame px RIGHT of box centers (systematic, all 8 —
//    reproduce with a label dx); row-3 "Vector" labels sit ~3px LEFT of center.
//
// 3. LANE FILLS (hashed, 021): row1 lane = dashed 2E2A62 border + C8C5F6 fill;
//    its boxes CFCEF8 fill; digits 2A2480 em 16 italic. Row3 lane = dashed
//    5A8568 border + EBFFD8 fill; the 8 vector boxes are KHAKI-bordered rects
//    (D1CBAA) y[300,321] with NO distinct fill (lane shows through) — they are
//    SHORTER than the lane and NOT green-bordered (020's lanes differed).
//
// 4. TYPOGRAPHY (crop-judge-verified on 021): diagram serif labels ("Vector") =
//    Times New Roman bold-italic em ~15.6 + red italic subscript em 10, pinned
//    at measured capTop (valign middle mis-centers mixed-size runs); navy bar =
//    Arial, yellow "function" em 20.5 + charSpacing ~1.7, white body em 18.5 +
//    charSpacing ~0.67 (the original tracks both); note boxes: ybox text is
//    ARIAL (metric triple L2/L1 1.087, L4/L2 1.384, L4/L1 1.504 — Arial
//    mixed-weight 1.090/1.393/1.518, single em 16.1; every installed serif
//    breaks a ratio by 5-9% and LiberationSerif overflows the box) with bold
//    "[1]"/"[2]" prefixes + word-only bold "Fixed"/"TRAINABLE" ("Parameters"
//    regular; the "[x]" prefixes are DARK BLUE, NOT red — pixel-verified, the
//    spec's red claim is a vision misread); gbox = Arial bold em 19.9 (per-line
//    width ratios match Arial exactly, NOT Verdana 16% off).
//
// 5. BRACE (traced-alpha variant of the certified raster mechanism): synthetic
//    cusp strokes failed 3 crop-judge rounds (sharp V / blunt apex / shallow).
//    What PASSED: alpha channel traced from the original's redness field
//    (crop y 336..352 EXACTLY — a 1-row misalignment lifts the apex ~1.7pt and
//    reads "shallow"), LANCZOS to the 600dpi box, painted with the census core
//    882830. See scratch/slide021/gen_brace_png.py + qa/slide021/
//    cropcheck5_brace.txt. The tanline/labels/row1/row3/navy/ybox/gbox crop
//    transcripts under this dir carry the full fix history.
//
// 6. NO right-edge red verticals on 021 (020 had them at x 887-890) — checked,
//    do not import. NO dots in row3's gap. Letterbox + mouse cursor omitted.
//
// Verified shared-block consistency: render_17 vs slide020/render_13 chrome-top
// mean|d| 0.57 (0.41% px >30 = the by-design numeral), left canvas 0.00.
