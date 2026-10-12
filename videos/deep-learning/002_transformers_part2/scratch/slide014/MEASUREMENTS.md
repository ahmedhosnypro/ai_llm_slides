# slide_014 MEASUREMENTS — WORK IN PROGRESS (resumed worker)

Status: resuming after provider storm. Prior worker banked 4 script/output pairs + 28 crops.
This file is appended incrementally. Final version replaces this header.

## Banked files (verified present)

| file | role |
|---|---|
| measure1.py / measure1_output.txt | chrome landmarks: letterbox, red border, gray panel, badge, title/subtitle bands, mapping cross-check |
| measure1b.py / measure1b_output.txt | refined title/subtitle, right-border fade, badge numeral tight scan, floating X5 box |
| measure2.py / measure2_output.txt | outer container, wheat box, bottom container, Y/X rows, matrix panel, zero col + plus, braces, connectors, sigma neurons |
| crops.py / crops_output.txt | 28 zoom crops z_*.png (2-6x) |

## Derived constants so far (from banked outputs; frame 960x540, 1px=1pt)

- Mapping: slide_x=(fx-17.628)/0.961232, slide_y=fy/0.955556
- Letterbox: first black row fy 518; black rows fy 518..539 (bottom strip)
- Chrome red border: left edge ~fx 57..60 (dark red at fx58: (115,38,46)); top rule fy 42..44 (fy43: (108,48,56)); right fade fx 900..902 (fy300); panel gray x-span 61..898; gray panel fx300 y-span 46..513
- Badge: yellow disc fx 860..892, fy 56..85, center (876.0, 70.5), d=(33,30); numeral ink fx 866..881 fy 68..82 n=59; darkest-ink median (82,89,17) — dark ink, NOT red (reddish count 0)
- Title: caps rows fy (54,74) + descender row (78,79); ink fx 187..814, cx 500.5; red core (167,60,71) n=3214
- Subtitle: rows fy (76,101); ink fx 133..901, 23 spans; blue core (123,116,201) n=1723; green core (124,184,122) n=1554; red core "ALL Words" (188,82,96) n=492
- Outer container (blue rounded border): verticals fx 66..68 and fx 291..293 (left panel divider) and fx 885..887/894..896 (right edge, double line); top fy 80..83 at fx480; bottom fy 507..510
- Wheat design box: ink bbox fx 310..902 fy 130..249; fill mode (232,216,200) [wheat]; border dark median (105,46,48); slide px x 304.2..920.0 y 136.0..260.6
- Bottom schematic container: verticals fx 291..293/300..301 ... 894..896; top fy 248..250; bottom fy 508..510
- Y rows (fx~300..450): Y1 bbox(300,450,267,302) Y2 (300,450,304,339) Y3 (300,459,342,377) Y4 (300,450,380,415) Y5 (300,450,448,483); fill mode (248,248,248)-ish white
- X rows (fx~532..663): X1 (532,663,267,300) X2 (532,662,305,339) X3 (536,663,342,377) X4 (532,663,380,415) X5 (532,662,449,483); fill white-ish; X1 has (248,200,248) pinkish mode
- Matrix panel: ink bbox (665,839,286,465); fill mode (208,248,224) [pale green]; slide px x 673.5..854.5 y 299.3..486.6; grid rows [316,317,331,332,342,351,352,367,368,387,388,402,403,426,427,441,442,443]; grid cols [670,745,817,835,836]
- Zero column + plus: ink bbox (838,902,280,469) -> slide px x 853.5..920.0 y 293.0..490.8; green-fill fx 839..878 fy 296..454 (one continuous band 296..454)
- Left brace (blue, fx 515..548): n max at fx527 (n=189), spans fy 248..510
- Right brace (blue fx 895): n=248 fy 255..502; fx898 n=14 fy 369..382
- Dotted connectors orange: row1 only at fy285, n=5 px at fx 527..531 [(202,127,70),(204,125,66),(225,151,88),(245,184,121),(245,196,140)]; rows 2-5 none on that scan line
- Sigma neurons (right edge of left NN): red-ring circles at fy bands: 144..149/150..176 (fx~231..272), 248..269/270..279 (fx~225..271), 353..383 (fx~223..271), 452..481 (fx~225..276)
- Floating X5 box top-left: white-ish blob fx 71..100 fy 103..111 n=121; ink col spans [(58,59),(68,91),(94,113),(115,119)]; row span (58,111)

## Crops index (fx0,fy0,fx1,fy1,zoom)
z_badge(852,46,912,96)x6 | z_title(180,46,822,80)x2 | z_subtitle_L(110,72,460,108)x3 | z_subtitle_R(455,72,910,108)x3 | z_fanlabels(52,48,175,180)x4 | z_nn_top(60,110,300,210)x3 | z_nn_mid(60,210,300,320)x3 | z_nn_bottom(60,320,300,516)x3 | z_weights_top(130,130,230,220)x4 | z_sigma1(215,135,300,200)x4 | z_sigma4_clip(215,440,300,516)x4 | z_wheatbox(300,122,910,256)x2 | z_wheat_lines(310,138,660,250)x3 | z_y_row1(292,258,462,310)x4 | z_y_linear(292,335,540,385)x4 | z_connector1(440,265,545,300)x5 | z_x_row1(525,258,670,305)x4 | z_x_row3(525,335,670,382)x4 | z_x_col_labels(520,250,560,515)x4 | z_matrix_full(660,280,845,470)x3 | z_matrix_row3(660,385,845,445)x5 | z_zero_plus(830,285,912,470)x4 | z_brace_R(872,245,912,515)x4 | z_brace_L(508,240,556,516)x4 | z_container_TL(56,70,180,145)x4 | z_container_TR(870,70,910,145)x4 | z_container_BL(56,480,180,518)x4 | z_left_panel_div(280,110,310,516)x4

## PENDING (to fill this session)
- Spec vs frame comparison, text content reading from crops, remaining colors, spot verification
