#!/usr/bin/env python3
"""Generate slide_039.js from measured geometry. All positions in slide pt (1pt=1/72in),
converted to inches in the JS. Closed-loop corrector may patch constants afterwards."""
from PIL import Image, ImageFont, ImageDraw

P = {
    # id: (text, font_key, size, bold, color, ink_left_pt, baseline_pt, underline_seg_idx_or_None, extra)
    # font_key: ARB=Arial Bold, AR=Arial, TSI=Times Italic, TSB=Times Bold
}
ASPIRAL = 0.9831   # box_top = baseline - K*size (Arial, empirical from certified slide_002)
ASPTIMES = 0.97    # initial guess, closed-loop corrects

FONTS = {
    "ARB": "/usr/share/fonts/TTF/Arialbd.TTF",
    "AR": "/usr/share/fonts/TTF/Arial.TTF",
    "TSI": "/usr/share/fonts/TTF/Timesi.TTF",
    "TSB": "/usr/share/fonts/TTF/Timesbd.TTF",
}
d = ImageDraw.Draw(Image.new("L", (10, 10)))
_f = {}
def F(k, s):
    if (k, s) not in _f: _f[(k, s)] = ImageFont.truetype(FONTS[k], s)
    return _f[(k, s)]
def ink_w(text, k, s):
    bb = d.textbbox((0, 0), text, font=F(k, s))
    return (bb[2] - bb[0]) * 1.0, bb[0]  # width, lsb

LINES = [
    # id, text, font, size, color, inkL, baseline, runs (None=single)
    ("title", "Normalization", "ARB", 35, "CC0000", None, 87.9, None),      # centered cx 453.45
    ("quoteL1", "The behavior of machine learning algorithms  changes when the input distribution changes.", "TSI", 22, "000080", 64.9, 130.8, None),
    ("covshift", "{Covariate shift }", "TSB", 20.5, "CC0000", None, 155.4, None),  # right-aligned, inkR 858.7
    ("f1l1", "layer weights changes", "ARB", 14.5, "CC0000", None, 202.0, None),   # centered cx 192.9
    ("f1l2", "during training steps", "ARB", 14.5, "000000", None, 235.5, None),   # centered cx 195.0
    ("f2l1", "Outputs of Activation functions", "ARB", 14, "CC0000", None, 204.2, None),  # cx 452.5
    ("f2l2", "of each layer change", "ARB", 14, "CC0000", None, 231.3, None),      # cx 454.5
    ("f3l1", "Inputs to the next layer,", "ARB", 14, "000000", None, 204.2, None),  # cx 739.5
    ("f3l2", "(With different Input distribution)", "ARB", 14, "CC0000", None, 231.3, None),  # cx 739.6
    ("conclusion", "Conclusion:", "ARB", 16.5, "CC0000", 73.2, 277.3, None),
    ("stmt1", "Input distribution of each layer changes with each step .", "ARB", 18.5, "000080", 152.3, 301.4, None),
    ("idea", "The basic idea behind Normalization is to:", "ARB", 18.5, "CC0000", 73.2, 341.2, None),
    # stmt2 runs: 0 plain, 1 underlined, 2 plain
    ("stmt2", "Limit covariate shift by normalizing the activations of each layer", "ARB", 18.5, "000080", 153.3, 365.3, 1),
    # lineC runs: 0 red bold, 1 black regular 19, 2 navy bold
    ("lineC", "Normalization:  Transforming the inputs to be Zero mean and unit variance.", "ARB", 18.5, "CC0000", 73.2, 406.0, -2),
    ("sumhead", "Normalization allows each layer to:", "ARB", 18.5, "CC0000", 67.0, 453.2, None),
    ("b1", "learn on a more stable distribution of inputs,", "ARB", 16.5, "000080", 84.7, 478.4, 1),  # underline 'stable distribution of inputs,'
    ("b2", "Accelerate the training of the network (don't stick with very small learning rates).", "ARB", 16.5, "000080", 83.6, 499.9, 0),  # underline 'Accelerate the training'
]

out = []
SHAPES = []
TEXTS = []
out.append("""// slide_039.js — "Normalization" (Deep Learning DSAI 308, Transformers Part II — video 002, slide 39)
//
// CONTENT SPEC: analysis/slide_039_final.json (verbatim text; PASS_WITH_FIXES applied).
// Original frame: unique_slides/slide_039.jpg (960x540). All ink positions PIL-measured
// (scratch/slide039/m1..m8) and mapped to TRUE slide coordinates through the frame->slide
// transform fitted from this frame's four chrome border landmarks (left 59, right 902,
// top 43, bottom 516  <->  slide 42, 919, 45, 540 — identical to certified slide_002):
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Badge cross-check: yellow-bbox center (875.5, 71.0) -> slide (891.4, 74.3) vs house
// (893, 71) — within JPEG-bbox noise (same as certified slide_002), same playlist template.
//
// CHROME LAW: shared playlist module shared_patterns/house_chrome.js, numeral 39.
//
// MEASURED FACTS honored here (frame = ground truth, overrides spec guesses):
//   * title "Normalization" Arial Bold 35 (ink w 229.9pt / cap-h fit), ink center x 453.4
//     (NOT slide-centered — measured as-is).
//   * blues measured navy ~#000080 (text cores (0,0,96)-(24,24,120)); spec's #0000CC was
//     a vision-model guess — frame wins.
//   * "Transforming the inputs to be" is BLACK REGULAR Arial 19 (measured stems 3px vs 5px
//     bold; w/h fit exact) — the spec validation had unified it to blue bold; frame wins.
//   * red text/borders CC0000 (spec; core bins consistent with C00000-family + JPEG).
//   * summary fill pale cyan ~E0FFFF (measured (237-239,255,254) deep interior; spec's
//     E8F2FF has G=242, measured G=255 saturated — frame wins).
//   * underlines measured: stmt2 'covariate shift' (frame x 213..335), b1 'stable
//     distribution of inputs,' (223..428), b2 'Accelerate the training' (99..269).
//   * OMITTED as video-capture artifacts (judge GROUND RULES (c)): black letterbox strip
//     (frame rows 518..539, below slide bottom 516->540) and pen-cursor blob near
//     'inputs,' (~frame 393..410, 455..475).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge "39")
drawHouseChrome(pres, s, { numeral: 39 });

const RED = "CC0000", NAVY = "000080", BLACK = "000000";
const pt = v => v / 72;
const K_AR = 0.9831, K_TS = 0.97; // baseline->boxTop lead (em) — closed-loop corrected

function textLine(id, runs, opts) {
  // runs: [{text, size, bold, color, font, italic, underline}]
  const maxAscent = Math.max(...runs.map(r => (r.options.fontFace === "Times New Roman" ? K_TS : K_AR) * r.options.fontSize));
  const maxSize = Math.max(...runs.map(r => r.options.fontSize));
  const o = {
    x: pt(opts.boxX), y: pt(opts.baseline - maxAscent),
    w: pt(opts.boxW), h: pt(1.6 * maxSize),
    align: opts.align || "left", valign: "top", margin: 0,
  };
  s.addText(runs.map(r => ({
    text: r.text,
    options: {
      fontSize: r.options.fontSize, bold: !!r.options.bold, italic: !!r.options.italic,
      color: r.options.color, fontFace: r.options.fontFace || "Arial",
      underline: r.options.underline,
    },
  })), o);
}
""")

def js_runs(id_, text, font, size, color, runs_spec, fk=None):
    if runs_spec is None:
        bold = fk in ('ARB', 'TSB')
        ital = fk == 'TSI'
        return '[' + run_js(text, font, size, color, bold, ital, False) + ']'
    if runs_spec == -2:  # lineC
        return ('[{text:"Normalization:  ",options:{fontSize:18.5,bold:true,color:RED,fontFace:"Arial"}},'
                '{text:"Transforming the inputs to be ",options:{fontSize:19,bold:false,color:BLACK,fontFace:"Arial"}},'
                '{text:"Zero mean and unit variance.",options:{fontSize:18.5,bold:true,color:NAVY,fontFace:"Arial"}}]')
    if id_ == "stmt2":
        return ('[{text:"Limit ",options:{fontSize:18.5,bold:true,color:NAVY,fontFace:"Arial"}},'
                '{text:"covariate shift",options:{fontSize:18.5,bold:true,color:NAVY,fontFace:"Arial",underline:{style:"sng"}}},'
                '{text:" by normalizing the activations of each layer",options:{fontSize:18.5,bold:true,color:NAVY,fontFace:"Arial"}}]')
    if id_ == "b1":
        return ('[{text:"learn on a more ",options:{fontSize:16.5,bold:true,color:NAVY,fontFace:"Arial"}},'
                '{text:"stable distribution of inputs,",options:{fontSize:16.5,bold:true,color:NAVY,fontFace:"Arial",underline:{style:"sng"}}}]')
    if id_ == "b2":
        return ('[{text:"Accelerate the training",options:{fontSize:16.5,bold:true,color:NAVY,fontFace:"Arial",underline:{style:"sng"}}},'
                '{text:" of the network (don\'t stick with very small learning rates).",options:{fontSize:16.5,bold:true,color:NAVY,fontFace:"Arial"}}]')
    raise ValueError(id_)

def run_js(text, font, size, color, bold, italic, underline):
    u = ',underline:{style:"sng"}' if underline else ''
    it = ',italic:true' if italic else ''
    return (f'{{text:{json_str(text)},options:{{fontSize:{size},bold:{"true" if bold else "false"}{it},'
            f'color:"{color}",fontFace:"{font}"{u}}}}}')

def json_str(t):
    return '"' + t.replace("\\", "\\\\").replace('"', '\\"') + '"'

# emit each line
for (id_, text, fk, size, color, inkL, baseline, runs_spec) in LINES:
    fontname = {"ARB": "Arial", "AR": "Arial", "TSI": "Times New Roman", "TSB": "Times New Roman"}[fk]
    bold = fk in ("ARB", "TSB"); italic = fk == "TSI"
    w, lsb = ink_w(text, fk, int(round(size * 4)))  # supersample for precision
    w /= 4.0
    # measured ink width targets for sanity print
    if id_ == "title":
        cx = 453.45; boxw = w * 1.3 + 20
        TEXTS.append(f'// {id_}: ArialB{size} ink w={w:.1f} (target 229.9) cx={cx}')
        TEXTS.append(f'textLine("{id_}", ' + js_runs(id_, text, fontname, size, "CC0000", None, fk) + f', {{baseline: 87.9, boxX: {cx - boxw/2:.2f}, boxW: {boxw:.1f}, align: "center"}});')
    elif id_ == "covshift":
        inkR = 858.7; rsb = 0.5
        boxw = w * 1.3 + 20
        TEXTS.append(f'// {id_}: TimesB{size} ink w={w:.1f} (target 161.3) right-aligned inkR={inkR}')
        TEXTS.append(f'textLine("{id_}", ' + js_runs(id_, text, fontname, size, "CC0000", None, fk) + f', {{baseline: {baseline}, boxX: {inkR + rsb - boxw:.2f}, boxW: {boxw:.1f}, align: "right"}});')
    elif inkL is None:
        cx = {"f1l1": 192.9, "f1l2": 195.0, "f2l1": 452.5, "f2l2": 454.5, "f3l1": 739.5, "f3l2": 739.6}[id_]
        boxw = w * 1.3 + 20
        TEXTS.append(f'// {id_}: ArialB{size} ink w={w:.1f}')
        TEXTS.append(f'textLine("{id_}", ' + js_runs(id_, text, fontname, size, color, None, fk) + f', {{baseline: {baseline}, boxX: {cx - boxw/2:.2f}, boxW: {boxw:.1f}, align: "center"}});')
    else:
        boxw = w * 1.3 + 20
        TEXTS.append(f'// {id_}: ArialB{size} ink w={w:.1f} inkL={inkL}')
        TEXTS.append(f'textLine("{id_}", ' + js_runs(id_, text, fontname, size, color, runs_spec, fk) + f', {{baseline: {baseline}, boxX: {inkL - lsb/4.0 - 1:.2f}, boxW: {boxw:.1f}}});')

SHAPES.append("""// ---- shapes FIRST (z-order under text): quote box, container, summary box, flow boxes, arrows, dots
function box(x, y, w, h, fill, lineColor, lineW) {
  s.addShape(pres.ShapeType.rect, {
    x: pt(x), y: pt(y), w: pt(w), h: pt(h),
    fill: { color: fill }, line: { color: lineColor, width: lineW },
  });
}
// quote box  frame[74,96,880,153] -> slide [57.6,100.5,896.1,160.1]
box(57.6, 100.5, 838.5, 59.7, "FFFFFF", RED, 2);
// big container  frame[72,162,878,397] -> slide [55.5,169.5,894.0,415.5]
box(55.5, 169.5, 838.5, 246.0, "FFFFFF", RED, 2);
// summary box  frame[72,410,878,503] -> slide [55.5,429.1,894.0,526.4]
box(55.5, 429.1, 838.5, 97.3, "E0FFFF", NAVY, 2);
// flow boxes (yellow fill, thin red border)  slide y 179.0..256.4
box(101.3, 179.0, 183.6, 77.4, "FFFFCC", RED, 1.5);   // box1 frame x 116..292
box(335.4, 179.0, 239.2, 77.4, "FFFFCC", RED, 1.5);   // box2 frame x 342..570
box(622.5, 179.0, 233.0, 77.4, "FFFFCC", RED, 1.5);   // box3 frame x 618..840

// arrows: thin red shafts with triangle heads (measured: shaft ~3px, head ~7px tall)
s.addShape(pres.ShapeType.line, {
  x: pt(285.4), y: pt(218.2), w: pt(50.0), h: 0,
  line: { color: RED, width: 2.5, endArrowType: "triangle" },
});
s.addShape(pres.ShapeType.line, {
  x: pt(574.6), y: pt(217.7), w: pt(48.9), h: 0,
  line: { color: RED, width: 2.5, endArrowType: "triangle" },
});

// bullet dots (measured 6px dia at frame (81..86, 447..452) and (81..86, 469..474))
s.addShape(pres.ShapeType.ellipse, {
  x: pt(67.5 - 3.15), y: pt(470.4 - 3.15), w: pt(6.3), h: pt(6.3),
  fill: { color: NAVY }, line: { color: NAVY, width: 0.5 },
});
s.addShape(pres.ShapeType.ellipse, {
  x: pt(67.5 - 3.15), y: pt(493.4 - 3.15), w: pt(6.3), h: pt(6.3),
  fill: { color: NAVY }, line: { color: NAVY, width: 0.5 },
});
""")

out.append("\n".join(SHAPES))
out.append("\n".join(TEXTS))
out.append("""
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_039_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
""")

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_039.js", "w") as f:
    f.write("\n".join(out))
print("wrote slide_039.js")
