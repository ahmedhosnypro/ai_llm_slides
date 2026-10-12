// components/slide_024.js — slide 024 "Neural Network Model" certified composition
// (001_introduction, Deep Learning DSAI 308). Judge-PASS attempt 1:
//   qa/slide024/judge_attempt_1.txt (FINAL VERDICT: PASS), render_4.png.
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11/12; 001_introduction/slide_dependencies.json):
// slide 25 builds on this composition. It MUST require() this module and call
// renderBase(pptx, slide, opts) (or cherry-pick blocks) — NEVER re-derive or copy-paste
// this geometry. 0-px proof: scratch build requiring this component renders md5-identical
// to the certified render (qa/slide024/component_0px_proof.txt).
//
// Block granularity: renderBase accepts
//   opts.skip   — array of block names to OMIT (child removes inherited blocks)
//   opts.only   — array of block names to DRAW exclusively (child replaces composition)
//   opts.chrome — draw house chrome (default true; via ../shared_patterns/house_chrome.js)
//   opts.numeral— badge numeral (default "24")
// Block names: chrome, blackbar, panel, title, dashline, magboxes, dotsfan, rings,
//   mesh23 (9 lines + col2 ports), mesh34 (9 lines + col3 ports), neurons, netlabels,
//   olabels, wlabels, outboxes, errorbar, classboxes, blockarrows, callouts.
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_024.jpg (960x540, 1px=1pt)
// — qa/slide024/measure_* + build_constants.txt; 4 gate vision reads vread_*.txt.
// Frame-over-spec corrections (declared in judge ground rules (f1)-(f8)): no skip
// connections / no w_ki labels; w_ji x3 + w_kj x3 riding mesh lines at 0/30/51 deg;
// WHITE Output boxes with black bold italic text + violet 9080C8 border; neurons =
// red Sigma (left) + black sigmoid-curve PNG (right) + dark divider, per-column border
// hues; floating rings with no connector segments; block arrows pale fill + darker
// outline + BLACK letter; magenta dashed line with left arrowhead inside the IS box.
//
// LAWS honored: playlist chrome via shared module (numeral = file number "24", PENDING
// FOUNDER VETO); verbatim text; margin:0 + explicit fontFace + explicit lineSpacing
// everywhere; no '#' in hex; cursor artifact omitted; black bottom bar per certified
// slide_002/005/021/023 precedent (y527..537.5).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";

// ---- palette (measured) ----
const TITLE_RED = "C00000";
const BLACK = "000000";
const PANEL_BEIGE = "DAD0C4";
const MAG_FILL = "FF99FF";
const MAG_LINE = "993366";
const MAG_DARK = "990099";
const DOT_MAG = "CC00CC";
const MESH_RED = "C00000";
const FAN_GRAY = "ACA298";
const W_BLUE = "0000CC";
const ERR_FILL = "9E0000";
const ERR_TEXT = "FF0000";
const CLASS_FILL = "E3FFCF";
const OUTBOX_FILL = "FFFFFF";
const OUTBOX_LINE = "9080C8";
const DIVIDER = "555555";
const PORT_DARKRED = "8B0000";
const SIGMOID = { w: 91 / 600, h: 116 / 600 };

const px = (v) => v / 72;
const COL_CX = [160, 261.5, 426.5, 590, 676.5];
const ROW_CY = [211.5, 285.5, 366.5];
const NEURON_FILL = ["EDEDEB", "DCE9F5", "DCFFB5", "F7C99B", "EDEDEB"];
const NEURON_LINE = ["A08C74", "7780AA", "6B9944", "C08850", "A08C74"];
const RINGS_POST1 = [196, 211, 226];
const RINGS_PRE5 = [618, 633, 648];

function bChrome(pptx, slide, opts) { drawHouseChrome(pptx, slide, { numeral: opts.numeral }); }

function bBlackbar(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(38), y: px(527), w: px(883), h: px(10.5),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
}

function bPanel(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(64), y: px(165), w: px(722), h: px(253),
    fill: { color: PANEL_BEIGE }, line: { color: PANEL_BEIGE, width: 0 },
  });
}

function bTitle(pptx, slide) {
  slide.addText("Neural Network Model", {
    x: px(485.5 - 320), y: px(89 - 32), w: px(640), h: 0.55,
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 30.5, bold: true, color: TITLE_RED,
  });
}

function bDashline(pptx, slide) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(140), y: px(141), w: px(680), h: 0,
    line: { color: MAG_DARK, width: 1.25, dashType: "dash" },
  });
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(129 - 8), y: px(141 - 11), w: px(16), h: px(22), rotate: 270,
    fill: { color: MAG_DARK }, line: { color: MAG_DARK, width: 0 },
  });
}

function bMagboxes(pptx, slide) {
  const MAG_BOXES = [
    { x: 64, y: 127, w: 76, h: 28, l1: "Input", l2: "Samples" },
    { x: 820, y: 125, w: 68, h: 29, l1: "Sample", l2: "Label" },
  ];
  for (const b of MAG_BOXES) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
      fill: { color: MAG_FILL }, line: { color: MAG_LINE, width: 0.75 },
    });
    slide.addText(
      [
        { text: b.l1, options: { breakLine: true } },
        { text: b.l2, options: {} },
      ],
      {
        x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
        align: "center", valign: "middle", margin: 0,
        fontFace: "Arial", fontSize: 9, bold: true, color: BLACK, lineSpacing: 10.5,
      }
    );
  }
}

function bDotsfan(pptx, slide) {
  const DOTS = [[78, 254], [78, 277.5], [78, 300.5], [78, 323.5]];
  for (const [dx, dy] of DOTS) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(dx - 4.5), y: px(dy - 4.5), w: px(9), h: px(9),
      fill: { color: DOT_MAG }, line: { color: DOT_MAG, width: 0 },
    });
    for (const cy of ROW_CY) {
      const up = dy > cy;
      slide.addShape(pptx.ShapeType.line, {
        x: px(84), y: px(Math.min(dy, cy)), w: px(54), h: px(Math.abs(cy - dy)),
        flipV: up,
        line: { color: FAN_GRAY, width: 0.75 },
      });
    }
  }
}

function bRings(pptx, slide) {
  for (const cy of ROW_CY) {
    for (const rx of RINGS_POST1) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: px(rx - 4.5), y: px(cy - 4.5), w: px(9), h: px(9),
        fill: { color: PANEL_BEIGE }, line: { color: "6B6863", width: 1 },
      });
    }
    for (const rx of RINGS_PRE5) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: px(rx - 4.5), y: px(cy - 4.5), w: px(9), h: px(9),
        fill: { color: PANEL_BEIGE }, line: { color: "2E2A20", width: 1 },
      });
    }
  }
}

function rimPoint(cxFrom, cyFrom, cxTo, cyTo, rFrom, rTo) {
  const dx = cxTo - cxFrom, dy = cyTo - cyFrom;
  const len = Math.sqrt(dx * dx + dy * dy) || 1;
  return [cxFrom + (dx / len) * rFrom, cyFrom + (dy / len) * rFrom,
          cxTo - (dx / len) * (rTo + 1), cyTo - (dy / len) * (rTo + 1)];
}

function bMesh23(pptx, slide) {
  for (const cy0 of ROW_CY) {
    for (const cy1 of ROW_CY) {
      const [x0, y0, x1, y1] = rimPoint(COL_CX[1], cy0, COL_CX[2], cy1, 21, 21);
      slide.addShape(pptx.ShapeType.line, {
        x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
        w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
        flipV: y1 < y0,
        line: { color: MESH_RED, width: 0.75, endArrowType: "triangle" },
      });
    }
  }
  // dark-red output ports at the source (col2) rims — same position in the certified
  // draw sequence (drawn after the mesh23 lines, before mesh34)
  for (const cy0 of ROW_CY) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(COL_CX[1] + 17.5), y: px(cy0 - 4), w: px(7), h: px(8),
      fill: { color: PORT_DARKRED }, line: { color: PORT_DARKRED, width: 0 },
    });
  }
}

function bMesh34(pptx, slide) {
  for (const cy0 of ROW_CY) {
    for (const cy1 of ROW_CY) {
      const [x0, y0, x1, y1] = rimPoint(COL_CX[2], cy0, COL_CX[3], cy1, 21, 21);
      slide.addShape(pptx.ShapeType.line, {
        x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
        w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
        flipV: y1 < y0,
        line: { color: MESH_RED, width: 0.75, endArrowType: "triangle" },
      });
    }
  }
  // dark-red output ports at the source (col3) rims
  for (const cy0 of ROW_CY) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(COL_CX[2] + 17.5), y: px(cy0 - 4), w: px(7), h: px(8),
      fill: { color: PORT_DARKRED }, line: { color: PORT_DARKRED, width: 0 },
    });
  }
}

function bNeurons(pptx, slide) {
  for (let c = 0; c < 5; c++) {
    for (const cy of ROW_CY) {
      const cx = COL_CX[c];
      slide.addShape(pptx.ShapeType.ellipse, {
        x: px(cx - 20), y: px(cy - 20), w: px(40), h: px(40),
        fill: { color: NEURON_FILL[c] }, line: { color: NEURON_LINE[c], width: 1 },
      });
      slide.addShape(pptx.ShapeType.line, {
        x: px(cx), y: px(cy - 20), w: 0, h: px(40),
        line: { color: DIVIDER, width: 0.75 },
      });
      slide.addText("\u03A3", {
        x: px(cx - 19), y: px(cy - 9), w: px(18), h: px(18),
        align: "center", valign: "middle", margin: 0,
        fontFace: "Arial", fontSize: 13, bold: true, color: TITLE_RED,
      });
      slide.addImage({
        path: ASSETS + "/sigmoid_curve.png",
        x: px(cx + 1.5), y: px(cy - SIGMOID.h * 72 / 2), w: SIGMOID.w, h: SIGMOID.h,
      });
    }
  }
}

function bNetlabels(pptx, slide) {
  const sub = (s) => [
    { text: "Net", options: { italic: true, subscript: false } },
    { text: s, options: { italic: true, subscript: true } },
  ];
  const NETS = [
    { runs: sub("i"), left: 203, bl: 184, ax0: 234, ay0: 187, ax1: 249, ay1: 195 },
    { runs: sub("j"), left: 369, bl: 184, ax0: 400, ay0: 187, ax1: 415, ay1: 195 },
    { runs: sub("k"), left: 532, bl: 184, ax0: 563, ay0: 187, ax1: 588, ay1: 196 },
  ];
  for (const n of NETS) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(n.ax0), y: px(Math.min(n.ay0, n.ay1)), w: px(n.ax1 - n.ax0), h: px(n.ay1 - n.ay0),
      flipV: n.ay1 < n.ay0,
      line: { color: MESH_RED, width: 1, endArrowType: "triangle" },
    });
    slide.addText(n.runs, {
      x: px(n.left - 1), y: px(n.bl - 14.5), w: px(34), h: 0.3,
      align: "left", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 12.5, color: TITLE_RED, lineSpacing: 14,
    });
  }
}

function bOlabels(pptx, slide) {
  const OLAB = [
    [280, 205, 2], [278, 274, 2], [275, 355, 2],
    [446, 205, 3], [444, 274, 3], [444, 355, 3],
    [610, 205, 4], [607, 274, 4], [607, 355, 4],
  ];
  const osym = ["i", "j", "k"];
  for (const [left, bl, c] of OLAB) {
    slide.addText(
      [
        { text: "O", options: { italic: true, subscript: false } },
        { text: osym[c - 2], options: { italic: true, subscript: true } },
      ],
      {
        x: px(left - 1), y: px(bl - 21), w: px(30), h: 0.42,
        align: "left", valign: "middle", margin: 0,
        fontFace: "Arial", fontSize: 17, color: TITLE_RED, lineSpacing: 19,
      }
    );
  }
}

function bWlabels(pptx, slide) {
  const WLAB = [
    [327, 205, "ji", 0], [321, 240, "ji", 30], [329, 276, "ji", 51],
    [488, 207, "kj", 0], [489, 243, "kj", 30], [490, 276, "kj", 51],
  ];
  for (const [left, bl, s, rot] of WLAB) {
    slide.addText(
      [
        { text: "w", options: { italic: true, subscript: false } },
        { text: s, options: { italic: true, subscript: true } },
      ],
      {
        x: px(left - 1), y: px(bl - 13), w: px(26), h: 0.28,
        align: "left", valign: "middle", margin: 0, rotate: rot,
        fontFace: "Arial", fontSize: 12, color: W_BLUE, lineSpacing: 13,
      }
    );
  }
}

function bOutboxes(pptx, slide) {
  const OUTBOX = [[723, 206, 58, 13, "Output 1"], [723, 278, 58, 13, "Output 2"], [723, 360, 58, 13, "Output m"]];
  for (let r = 0; r < 3; r++) {
    const [bx, by, bw, bh, label] = OUTBOX[r];
    const cy = ROW_CY[r];
    slide.addShape(pptx.ShapeType.line, {
      x: px(COL_CX[4] + 21), y: px(cy), w: px(bx - 3 - COL_CX[4] - 21), h: 0,
      line: { color: MESH_RED, width: 1, endArrowType: "triangle" },
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: px(bx), y: px(by), w: px(bw), h: px(bh),
      fill: { color: OUTBOX_FILL }, line: { color: OUTBOX_LINE, width: 1 },
    });
    slide.addText(label, {
      x: px(bx), y: px(by), w: px(bw), h: px(bh),
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 10.5, bold: true, italic: true, color: BLACK,
    });
  }
}

function bErrorbar(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(797), y: px(180), w: px(21), h: px(213),
    fill: { color: ERR_FILL }, line: { color: ERR_FILL, width: 0 },
  });
  for (const cy of ROW_CY) {
    slide.addText("Error", {
      x: px(807.5 - 30), y: px(cy - 8), w: px(60), h: px(16), rotate: 270,
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 12, bold: true, color: ERR_TEXT,
    });
  }
}

function bClassboxes(pptx, slide) {
  const CLASSBX = [[825, 202, 66, 19, "Class 1"], [825, 275, 66, 18, "Class 2"], [825, 357, 66, 17, "Class m"]];
  for (const [bx, by, bw, bh, label] of CLASSBX) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(bx), y: px(by), w: px(bw), h: px(bh),
      fill: { color: CLASS_FILL }, line: { color: CLASS_FILL, width: 0 },
    });
    slide.addText(label, {
      x: px(bx), y: px(by), w: px(bw), h: px(bh),
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 9, color: BLACK,
    });
  }
}

function bBlockarrows(pptx, slide) {
  const ARROWS = [
    [240, 384, "D9E2F3", "8FA3CF", "i"],
    [405, 384, "C9E3A8", "7FA85E", "j"],
    [565, 384, "F2CC9D", "C08040", "k"],
  ];
  for (const [ax, ay, fill, outline, letter] of ARROWS) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(ax + 16.5), y: px(ay + 24), w: px(16), h: px(20),
      fill: { color: fill }, line: { color: outline, width: 1 },
    });
    slide.addShape(pptx.ShapeType.triangle, {
      x: px(ax), y: px(ay), w: px(49), h: px(26),
      fill: { color: fill }, line: { color: outline, width: 1 },
    });
    slide.addText(letter, {
      x: px(ax + 16.5 - 6), y: px(ay + 24), w: px(28), h: px(20),
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 10, color: BLACK,
    });
  }
}

function bCallouts(pptx, slide) {
  const CALLOUTS = [
    [220, 428, 87, 33, "DEEBF3", "8E96BC", "Previous Layer", "Layer (i)"],
    [384, 428, 87, 33, "DDFFB8", "7FA85E", "Current Layer", "(You are here)"],
    [558, 430, 69, 29, "F2CC9D", "C08040", "Next Layer", "Layer (K)"],
  ];
  for (const [bx, by, bw, bh, fill, line, l1, l2] of CALLOUTS) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(bx), y: px(by), w: px(bw), h: px(bh),
      fill: { color: fill }, line: { color: line, width: 0.75 },
    });
    slide.addText(
      [
        { text: l1, options: { breakLine: true } },
        { text: l2, options: {} },
      ],
      {
        x: px(bx), y: px(by), w: px(bw), h: px(bh),
        align: "center", valign: "middle", margin: 0,
        fontFace: "Arial", fontSize: 8.5, color: BLACK, lineSpacing: 11,
      }
    );
  }
}

const BLOCKS = {
  chrome: bChrome, blackbar: bBlackbar, panel: bPanel, title: bTitle,
  dashline: bDashline, magboxes: bMagboxes, dotsfan: bDotsfan, rings: bRings,
  mesh23: bMesh23, mesh34: bMesh34, neurons: bNeurons,
  netlabels: bNetlabels, olabels: bOlabels, wlabels: bWlabels, outboxes: bOutboxes,
  errorbar: bErrorbar, classboxes: bClassboxes, blockarrows: bBlockarrows,
  callouts: bCallouts,
};
const BLOCK_ORDER = ["chrome", "blackbar", "panel", "title", "dashline", "magboxes",
  "dotsfan", "rings", "mesh23", "mesh34", "neurons", "netlabels",
  "olabels", "wlabels", "outboxes", "errorbar", "classboxes", "blockarrows", "callouts"];

/**
 * Draw the certified slide-024 composition onto a slide.
 * @param {object} pptx  the pptxgenjs instance (for ShapeType)
 * @param {object} slide the slide returned by pptx.addSlide()
 * @param {object} opts  { skip: string[], only: string[], chrome: bool, numeral: string }
 */
function renderBase(pptx, slide, opts = {}) {
  const o = {
    skip: opts.skip || [],
    only: opts.only || null,
    chrome: opts.chrome === undefined ? true : opts.chrome,
    numeral: opts.numeral === undefined ? "24" : String(opts.numeral),
  };
  const draw = (name) => {
    if (o.only ? o.only.includes(name) : !o.skip.includes(name)) BLOCKS[name](pptx, slide, o);
  };
  for (const name of BLOCK_ORDER) draw(name);
}

module.exports = { renderBase, BLOCKS, BLOCK_ORDER };
