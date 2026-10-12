// P2 MEMBER NOTES — slide 022 ("Suggested Positional Encoders", P2#3) — for slide 34 (P2#4).
// Base convention: ../../slide020/p2_row_lane_pattern.js (STILL BINDING); member-2 deltas:
// ../../slide021/p2_member_notes_021.js. This file records what member #3 measured/changed
// on ITS frame — re-measure YOUR frame the same way; none of these numbers transfer blindly.
//
// 1. MAPPING (per-frame!): 022's chrome landmarks (red-weighted subpixel centroids,
//    scratch/slide022/measure1.py): left 58.17, right 901.09, top 42.94, bottom 516.89
//    => ax=17.753, sx=0.962235, ay=0, sy=0.955556. Badge cross-check (875.7,69.9) ->
//    slide (891.6,73.1) vs house (893,71) — the same 1-4px JPEG-bbox class. 020 used
//    ax=18.628, 021 ax=18.13, 022 ax=17.753 — the fit drifts ~1px per frame; FIT YOUR OWN.
//
// 2. LAYOUT differs from 020/021: 022 = title + subtitle, a NAVY-BORDERED white diagram
//    panel (solid 1.25pt border x65..892, y111..341.5 — NOT dashed), THREE dashed row lanes
//    INSIDE it (y119/157.5, 188/225.5, 262.5/302 — sysDash 1pt, roundRect r0.06), each with
//    8 boxes at its OWN slightly-different column grid (r1 [182,241]...[816,874]; r2
//    [178,238]...[809,874]; r3 [178,235]...[808,871] — re-measure per row!), a +δ annotation
//    band BELOW row 3, and a second navy-bordered CYAN problems panel (y349.5..502.5,
//    fill E9F9F9). Two separate bordered panels stacked with a 7px white gutter between
//    (the navy side borders are ABSENT in the gutter — do not draw one continuous frame).
//
// 3. FILLS/COLORS (hashed cores, measure8/17): r1 lane fill = GRAY E8E8E8 (the spec's
//    "pale-yellow" is a vision misread — the BOXES are cream F0F0E0); r2 lane fill
//    C9C6FA with TRANSPARENT boxes (no distinct fill — lavender shows through; spec's
//    "white boxes" is a misread); r3 lane fill F8E9ED (pinkish-white; spec's FFB3B3 way
//    off), boxes F8F0E0. Box borders: r1/r2 soft (BFA9A5 / 8482C0), NOT the C00000 family.
//    Title/deep-red text cores measure ~(125,25,35) on this frame (JPEG-dark class) ->
//    drawn 901220/9C1622.
//
// 4. DOTS: FIVE per row (NOT the spec's uncertain "6"): x-centers 637/655/673/691/706.5,
//    r1 gray 7E807C d~8.4 cy 138, r2 steel-blue 7390BC d~7.3 cy 207.5. Same 5-dot grid
//    as 020/021. Row-3 gap EMPTY.
//
// 5. THE +δ ANNOTATION (the tricky part — TWO bands, both BELOW the row-3 boxes):
//    (a) SIX small ORANGE marks (core ~(186,95,30) = BC621E), w12-20 x h~15, ink
//        y[290,305], OVERLAPPING the lane's bottom dash (y300-302), at x-centers
//        278/350/423/496.5/569/836.5 — the SAME chain positions as 020's bolts
//        (274.5/348/422/495.5/569/834.5). Drawn as short straight arrows
//        (line+triangle head); the judge accepted the style as MINOR variance (the
//        original reads slightly curved at zoom).
//    (b) SIX "+δ" TEXT glyphs (dark maroon 8A2436, Times bold italic), ink y[315,328]
//        — BELOW the lane, OUTSIDE it — at x-centers 226.5/296/378/453/525/794.5.
//        Cap-pin them (capTop FY(315.5), valign top, em 18). Do NOT place +δ at the
//        gap centers — this slide's labels sit under the boxes' left portions.
//
// 6. TYPOGRAPHY (closed-loop calibrated, qa/slide022/selfcheck 4-6 + judge attempt 2 PASS):
//    title Arial bold 24.3 (PERFECT at that size); subtitle 22.3; left labels 12.0/11.2/12.0
//    (bold-italic); box labels r1 Times-italic-bold 15.2, r2 19.4, r3 digits = ARIAL BOLD
//    (non-italic!) 18.5 (orig digit w/h 0.8 = DejaVu-bold class; Times renders 12% narrow);
//    summary line1a "Use δ = 1" ITALIC 16.2 (spaces around '=' — the spec's "δ=1" is a
//    spacing normalization; frame ink spans x80..146), line1b 17.8; Problems 18.0; bullets
//    17.7 with lineSpacing 22.7pt (pitch measured 21.7 frame px); bullet markers 4.5x5.5
//    dots at x80-84. N-2/N-1 tokens: INLINE at 0.8em on the SAME baseline (measured: ink
//    band y132-142 = "Word 0"'s band; judge-confirmed) — NEVER pptxgenjs subscript (it
//    drops the baseline; judge MINOR on attempt 1).
//    VERBATIM: "Last Position Encoding" (capital P per spec+frame; worker-1 had lowercase).
//    "(Depends on Seq. Length)" has NO underline on this frame (measured: no contiguous
//    run under x567-820 at y383-387) — the spec's underline claim is a misread.
//
// 7. OMITTED AS ARTIFACTS: mouse cursor over box8/N-1 (x~818-837 y~272-306) + letterbox
//    rows 517-539. NO right-edge red verticals (checked — 021 class, not 020's).
//
// 8. REGRESSION WARNING for member #4: worker-2's attempt-3 edit accidentally DELETED
//    row 3's drawLane line (judge attempt 1 MAJOR "missing dashed container"). When you
//    refactor a row block, diff the drawLane calls afterward. Judge history: attempt 1
//    FAIL (1 MAJOR), attempt 2 PASS (4 MINORs: +δ slightly large/dark; arrow anchor;
//    index digits slightly large/bold; gray dots slightly large — all sub-tolerance).
//