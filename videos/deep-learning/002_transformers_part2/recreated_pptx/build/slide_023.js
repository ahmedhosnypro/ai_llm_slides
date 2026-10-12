// slide_023.js — "Suggested Positional Encoders (Normalize Seq. Length to "1")"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 23)
//
// CONTENT SPEC: analysis/slide_023_final.json (PASS_WITH_FIXES; verbatim text, [?]
// items honored). SOURCES: slide_023_source/SOURCES.md (BANKED — Kazemnejad PE blog
// + Vaswani §3.5 + MLM tutorial; course-original strawman diagram, no figures).
// Original frame: unique_slides/slide_023.jpg (960x540, video-002 zoomed-out capture).
//
// CHROME LAW (playlist, founder directive 2026-10-11): outer chrome is the SHARED
// module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas,
// gray E9E9E7 panel x 42..919px / y 45px..slide bottom, thin C00000 border, badge
// circle d36px at (893,71)px FDFD96 + 6A5ACD ring, bold 333333 numeral. Badge
// numeral = 23 (the number printed on THIS original frame; verified: yellow badge
// bbox 859..892 x 56..85 maps back to slide (892.4, 73.7) vs house (893, 71)).
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide023/measure_chrome*.py):
// same zoom-out as certified slide 002. Fitted from THIS frame's four chrome border
// landmarks (panel left stroke 57..59 ctr 58 <-> 42; right 900..902 ctr 901 <-> 919;
// top 42..44 ctr 43 <-> 45; bottom stroke 516..517 ctr 516.5 <-> 540):
//   slide_x = (frame_x - 17.628) / 0.961230 ;  slide_y = (frame_y + 0.045) / 0.956566
// All content ink below is mapped to TRUE slide coordinates (pt; 1pt = 1/72 in)
// through this transform. Black letterbox strip (frame rows 519..539) and the white
// mouse cursor are video-capture artifacts — OMITTED (judge ground rule (c)).
//
// MEASURED STRUCTURE (scratch/slide023/*.py, frame px -> slide pt; full record in
// components/slide_023.js which holds the identical draw as the banked component):
//   title ink x 334.3..698.5 (cx 516.4 — genuinely RIGHT of slide center 480, as
//     measured; slide-002 precedent: reproduce as measured), cap 61.7, baseline 80.5
//     -> Arial Bold ~25pt C00000 (core (138,18,32)). Subtitle ink x 362.4..682.8
//     (cx 522.6), cap 88.9 -> ~23pt bold 0000CC.
//   3 strips: left label + dashed rounded container + 8 thin-bordered boxes
//     (white fill rows 1/3, transparent row 2 — container fill shows through):
//     R1 container x 147.6..896.7, y 123.4..164.2, BLACK dashed, no fill; boxes
//     y 132.3..154.2; 5 gray dots cx 635.0/653.7/672.4/691.2/709.9, cy 144.3, d 9.4.
//     R2 container x 145.5..893.1, y 195.5..235.8, 3333CC dashed, CCCCFF fill; boxes
//     y 203.9..226.7; 5 blue dots cx 635.5/655.3/673.0/692.7/707.8, cy 217.0, d 10.4.
//     R3 container x 144.0..894.4, y 273.4..316.3, CC0000 dashed, FFE0E0 fill; boxes
//     y 284.9..307.4; NO dots in the 5d..1-d gap (measured empty).
//   ARROWS (measured; NOT long arcs — the frame shows, for each of the 6 arrows, a
//     short vertical FF9900 drop from the DESTINATION box's bottom-center through the
//     container's bottom border, ending in a small down-arrowhead, plus a red bold
//     "+d" label in the gap LEFT of the drop): shafts cx 260.5/339.5/416.0/493.5/
//     570.0/844.1 y 306.9..317.5 w ~6pt; heads y 316.5..321.0 w 14.6; labels cx
//     217.3/289.6/373.9/452.4/527.8/807.2, glyph band y 327.3..342.9 -> ~17pt bold.
//   Highlight box x 54.5..907.6, y 363.9..525.9; fill measured (232,252,250) ~E8FCFA
//     (frame wins over spec D6EAF8), border 0066CC. Lead line mixed-color as
//     measured (red "d=1/Seq. Length", red underlined "(Independent of Seq.
//     Length)"); "Problems:" RED (measured); bullet 1 with RED parenthesized d;
//     bullet 2 with RED underlined "position # 4"/"position #4", wraps to an ALL-
//     MAGENTA line 2 "(though they are same position)" (measured); bullet 3 blue.
//
// SINGLE-VERSION law: this build IS the deliverable slide_023_recreated.pptx.
// COMPONENT: the identical draw is banked at build/components/slide_023.js
// (renderBase) — slide 024 depends on this slide (slide_dependencies.json).

const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_023.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();
renderBase(pres, s, { numeral: 23 });

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_023_recreated.pptx" })
  .then(() => console.log("WROTE slide_023_recreated.pptx"));
