# slide_022 measurements (PIL, frame px = pt, 960x540) — forensics1..20
## Chrome: playlist house_chrome.js, numeral 22 (frames carry no printed numbers)
## Frame: original's own red frame line x58-59 y43..516 REPLACED by playlist chrome (law)
## Boxes (fill bbox -> draw rect path, C00000 1.5pt line unless noted)
- leftbox   fill x84..417  y90..244   white;  rect (82.5, 88.5, 336, 158)
- rightbox  fill x530..791 y90..243   white;  rect (528.5, 88.5, 264, 157)
- decision  fill x83..765  y257..340  #FAFEED (modal 250,254,237); rect (81.5, 255.5, 685, 87)
- diagram   fill x230..611 y352..506  white;  rect (228.5, 350.5, 384, 157.5)
- callout   fill x629..816 y396..443  #E3E5C9 (modal 226,229,202); border DARK TAN #A79E88 (NOT red: PIL (186,176,149)); rect (626.5, 395.5, 192, 49)
- black bar x38..921 y518..539 (same as certified 002/005/031; draw y518 h19.5, chrome stroke stays visible)
## Title: "Visualization of Single Perceptron" TNR Bold ~33pt C00000, ink x227..719 (center 473.5), cap top 60, baseline 82.5, descender 89; no underline
## EQ1 (left box), line baseline 171.5; X(86,159..172) BLACK; =(101..113,162..169); v1 parenL x115..118 y~116..228, parenR x138..144;
##   entries x121..136: x1 b131, x2 b154.5, ... b178, ... b199, xn b220  (b=baseline)
##   red => (178,160..194,171); X2(218,159..231,172); =(234..246); v2 parenL x248..250 y104..235, parenR x271..277 y~104..236;
##   entries x253..268: 1 RED b120, x1 b141, x2 b165, ... b188, ... b209, xn b230
##   label "Ugmented Vector" BLUE 0000CC italic UNDERLINED, ink x297..407 y159..176 (baseline 172, underline y~175)
## EQ2 (right box), line baseline 172.5; W(559,159..575,173) RED (PIL, overrides spec); =(578..589);
##   parenL x592..594 y104..234, parenR x618..620 y102..236; entries x597..615:
##   b RED b120, w1 b141, w2 b165, ... b189, ... b209, wn b230
##   label "Model Weights" ink x668..762 y159..176
## EQ3 (decision box), main baseline 301:
##   d( x87; X RED x108 (PIL (159..165,0,6..16)); ) x126; = x137; W^T x156 (T sup y282..290); X x192; = x215;
##   w1x1 x233 (sub hangs below baseline); + x272; w2x2 x285; + x324; ..... x337..359 (five dots); + x362;
##   wnxn x375; + x414; b*1 RED x426..456; red => x502..522 (y287..299)
##   brace: x543..557 y271..320 (JPEG-chroma-destroyed; spec red; render stretched "{" RED spanning full case block y267..326)
##   cases BLUE 0000CC (incl. case arrows - PIL, overrides spec "red"): rows b282/b304/b326 (pitch 22):
##     >0 x554..574; => x586..601; "Class I" x614..666; "Class II" x614..672; "Undefined Class" x614..741
## DIAGRAM (box x228..612):
##   inputs BLACK italic x~250: x1 b364.5, x2 b387.5, x3 b409.5, ... b432, ... b455, xn b478, 1 RED b500
##   weights BLUE x~288: w1 b367, w2 b384.5, w3 b405.5, (none @dots rows), wn b457 (sits HIGH, beside 2nd dots row - measured), b b499
##   fan lines: 7 pink FF66CC from (312,row_y) to junction (397,420.5), rows y=360.5,383,405,430.5,453,473.5,494.5
##   junction: RED triangle (398,415)-(398,427)-(409,421)
##   sigma circle: oval x411..444 y406..432 (CCFFFF fill, black outline); Sigma glyph ink (415,410)-(432,430) fs~30
##   red shaft FF0000 y419..423.5 x447..563 (gaps at block borders 470..476 / 486..494 / 506..512 - shaft UNDER block+stem)
##   step block: rect x470.5..512 y413..429 path, border PURPLE #6F449D (PIL (111,68,157); overrides spec FF66CC), NO fill
##   step glyph: bottom bar (476..490.5, 428..430.5), stem (488.5..491.5, 414..428) dark #333 (breaks red), top bar (492..505.5, 412..414.5)
##   red head: triangle (563,415.5)-(563,427.5)-(574.5,421.5)
##   O/P: bold black TNR ~19pt, ink x583..609 y415..428 (baseline 428)
## CALLOUT text: bold italic, line1 "Binary Classification" ink x648..799 cap407 baseline420; line2 "(2 Classes)" x683..764 baseline437; both centered x723.5; ink DARK BROWN (PIL core (81..93,55..68,17..28) -> #663300)
## Artifacts excluded: mouse cursor (~x38,y238 area), nothing else. wn-high position reproduced as measured.
## NO underlines under X/W (PIL: 0-7 px noise) - spec's "bold underlined X/W" overridden by PIL.
