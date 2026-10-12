// P2 PATTERN ASSET — "row-lane diagram convention" (slide 020, P2 group head)
// Banked for P2 members: slides 21, 22, 34 (build STRICTLY in listed order —
// verify this pattern against your own frame, then reuse the convention).
//
// THE CONVENTION (as measured on slide 020; re-measure YOUR frame — the founder
// law is "your frame is ground truth"):
//
// 1. CHROME: every build starts with
//      const { drawHouseChrome } = require("<abs>/videos/deep-learning/shared_patterns/house_chrome.js");
//      drawHouseChrome(pres, s, { numeral: N });   // N = the number printed on YOUR frame
//    NEVER hand-draw the frame/badge. After render, run shared_patterns/house_chrome_check.py.
//
// 2. FRAME->SLIDE MAPPING: video-002 frames are ~0.958-scale zoomed-out captures
//    with a black letterbox strip below. Fit YOUR frame's four chrome stroke centers
//    (left/right/top/bottom) with subpixel centroids, then
//      slide_x = (frame_x - ax) / sx ;  slide_y = (frame_y - ay) / sy
//    Slide 020's fit (matches certified 002/003): ax=18.628, sx=0.961231, ay=0, sy=0.955556.
//
// 3. ROW LANES (full-width dashed containers): pptxgenjs rect, line width 1,
//    dashType "sysDash", fill when the original shows one. Measured lanes on 020:
//      row2 (embedding): frame [164,883]x[154.5,192.5], border 00A550, fill E7FEE9
//      row3 (position):  frame [164,883]x[217,256],   border 3333CC, fill C9C7F6
//      row4 (I/P):       frame [162,883]x[358,398],   border C00000, fill FFFFFF
//    Row1 (words) has NO lane — boxes only (measured). CHECK YOUR FRAME.
//
// 4. SHARED COLUMN GRID: 8 columns at frame centers 211.5+73.4k, ellipsis gap
//    after k=5 (dots at frame x 630-708, 5 dots), then columns 7/8 at 769.5/843.5.
//    Row1/row4 boxes: [c-31.5, c+31.5]. Row2 cell strips: [pinkLeft-20, pinkLeft+40].
//    Row3 boxes measured individually ([174,231],[249,309],[322,383],[396,447],
//    [480,530],[544,603],[730,796],[805,871]).
//
// 5. EMBEDDING CELL STRIPS (row2): 6 cells x ~10px in band y [164,182]; per-cell
//    fills are a MEASURED GRADIENT: cream EFE9BE, pale-green EAF8D8, PINK F2A7C3
//    (3rd cell, holds the red italic X_k), lavender E9E7F4, pinkish F2DEEC,
//    gray-pink E6DDDB. Cell dividers 999999 0.5pt. NO outer red rect (round-3
//    crop check: the original's groups sit bare). Subscripts: rich-text runs
//    (fontSize ~0.55em + subscript: true) in a box WIDE enough to never wrap.
//
// 6. ARROWS: the original's arrows are THIN red shafts (~8px) with SMALL triangular
//    heads (~13x6.5px) — pptxgenjs rect + flipV triangle. Measured (020):
//      A1 cx 614.5 y[264,292] | A2 cx 720 y[196,294] (row2 -> banner THROUGH row3's
//      dot gap) | A3 cx 519.5 y[331,360] | A4 cx 519.5 y[419,446].
//
// 7. BANNER: solid 990000 rect with a single centered rich-text line
//    [{ Combine, FFD700 }, { rest, FFFFFF }], ~20.2pt bold.
//
// 8. UNDERBRACE: LO MIS-RENDERS rotated leftBrace presets (measured). Use the
//    certified raster mechanism instead: matplotlib/PIL -> transparent 600dpi PNG
//    -> addImage at exact size (w = px/600 in). See build/assets/brace_020.png +
//    scratch/slide020/gen_brace_png.py.
//
// 9. MARKS: the small orange marks under the position row are tiny DOWNWARD
//    TRIANGLES (7.5x6.5px) at frame x 274.5/348/422/495.5/569/834.5, straddling
//    the lane's bottom rule; the red "+δ" glyphs (em ~20, Times bold italic) sit
//    at x 236/312/387/463/535/800 (ALTERNATING chain with the triangles).
//
// 10. LEFT LABELS: Arial family (lab1 italic gray 14.5pt 3 lines; lab2 bold green
//     16pt + "e.g. word2vec" 11.5pt; lab3 bold blue 14pt; lab4 bold italic red 14pt)
//     with EXPLICIT lineSpacing from the measured line pitch. Diagram labels use
//     Times New Roman italic (spec typography_notes: serif-italic-like).
//
// 11. CLOSED LOOP: every geometry above was verified by qa/slide020/
//     selfcheck_attempt_*.py (render ink bbox vs original measured bbox, tol
//     ~6 frame px) + house_chrome_check.py + 3 dense-region crop comparisons
//     through the vision gate BEFORE the judge. REPEAT ALL OF IT on your slide.
