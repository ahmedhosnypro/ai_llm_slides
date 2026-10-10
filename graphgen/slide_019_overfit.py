#!/usr/bin/env python3
"""Slide 019 — Overfitting regression panel-pair generator (advanced graphgen).

Decision (lib / function / algorithm / data), per the triage plan P-19 and the
measured facts banked in qa/slide19/graphgen/ (forensics v1-v3 + probe_panels_1):
  lib      : numpy + scipy.interpolate + matplotlib (Agg)
  function : np.polynomial.Polynomial.fit (polyfit) deg 2 and deg 9; splrep/splev
             for the two hand-drawn-looking curves
  algorithm: polynomial regression — the lecture topic of this slide
             ("Target / Fit" underfit on the left, "2nd vs 10th order" overfit on the right)
  data     : the data points measured from the original frame itself
             (videos/ml-intro/unique_slides/slide_019.jpg, 960x540, 1px = 1pt = 1/72in)
             via PIL forensics (ring-component scans + fine 2D ink maps) merged
             with the gated vision probes (probe_left_geometry_2 /
             probe_right_geometry_1 — y-coordinates reliable to ~1-3 px,
             x-coordinates systematically compressed and used for ORDER only):
               left  panel: 7 open-circle points
               right panel: 11 open-circle points

Binding to the original (judge-validated contract, deviating from the triage's
pre-forensics assumptions where the pixels proved otherwise — documented):
  LEFT panel  (189,360)-(494,486):
    Target = #0000FF smooth U-valley entering at the top-left, flat bottom,
             rising right arm ending mid-height (measured ink reads JPEG-mutated
             gray-teal; probe: "broad U", "dark slate blue"; spec's
             Target=#FF6600/Fit=#0000FF assignment was flagged uncertain in
             slide_019_final.json and is contradicted by pixels+probe).
    Fit    = #FF6600 hand-drawn arch: bottom-left -> crest touching the top
             border -> descent -> long low flat run -> slight downward bend at
             the extreme right (original ink reads mutated ochre).
    Low-order polyfit candidates (deg 1/2 on the left data) were computed and
    PIL-scored as required by the triage plan; they do not reproduce the
    original's arch (banked scores below) — the measured-ink spline wins and is
    used, because the binding requirement is faithfulness to the original.
  RIGHT panel (575,360)-(876,485):
    2nd Order Fit = #00CC66 broad inverted parabola, apex ~(758,392),
                    asymmetric gentle right descent, steep left entry arm
                    (measured ink to x~604). Candidates: polyfit deg2 on the
                    11 measured data points, polyfit deg2 on the measured
                    curve anchors, anchor spline — chosen by PIL score.
    10th Order Fit = #FF0000 measured-ink composite (FIT10_PATH): enters at
                     the bottom axis (630,469), steep climb through circle #2,
                     crest (641,388), grazes #3/#4 from above, troughs at
                     (666,430)/(735,427), passes through the #5-#11 cluster,
                     sharp hump on #8 (765,387), up-spike to (803,373) that
                     stops 9 px below the top border, then a separate re-entry
                     stroke from (823,366) descending through #11 to (831,400);
                     the bottom-left outlier circle #1 (606,460) is missed
                     entirely (classic overfitting illustration). The exact
                     deg-9 polynomial interpolation through the points was
                     computed and EXPLODES (Runge), leaving the panel — banked
                     as algorithm evidence; the slide's verbatim label
                     "10th Order Fit" is kept.
  Both panels: bg #CCFFCC, thin #AA0000 border, #404040 L-axes (no ticks, no
  arrowheads), black-outline/white-fill open-circle markers (~7px diameter).
  Legends + italic y/x labels stay NATIVE pptx text in the final slide (verbatim
  content; repositioned to measured spots); they are NOT baked into the PNGs.

Rendered at 300 dpi at each panel's physical size (1px = 1pt):
  left  4.23611 x 1.75  in -> 1271 x 525 px
  right 4.18056 x 1.73611 in -> 1254 x 521 px
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from PIL import Image
from scipy.interpolate import splrep, splev

ROOT = "/home/ahmed/Projects/ai_llm_slides"
ORIG_JPG = os.path.join(ROOT, "videos/ml-intro/unique_slides/slide_019.jpg")
OUTDIR = os.path.join(ROOT, "videos/ml-intro/recreated_pptx/qa/slide19/graphgen")
DPI = 300

# ---- measured constants (frame px, 960x540; see forensics_v1-v3 outputs) ----
PANELS = {                    # x0, y0, x1, y1 (border inclusive, measured)
    "left":  (189, 360, 494, 486),
    "right": (575, 360, 876, 485),
}
AXES = {  # vertical-axis x, horizontal-axis y (frame px); axes top y~364, no ticks
    "left":  {"vx": 217, "hy": 469, "h_to": 475},
    "right": {"vx": 598, "hy": 469, "h_to": 855},
}

TARGET_ANCHORS = [  # left panel U-valley target ink trace (frame px; teal-mask trace v3)
    (221, 382), (224, 385), (228, 389), (232, 393), (238, 396), (244, 404),
    (250, 411), (262, 418), (272, 425), (282, 432), (292, 438), (302, 443),
    (312, 448), (322, 452), (332, 455), (342, 456), (352, 458), (362, 459),
    (372, 461), (382, 460), (392, 457), (402, 455), (412, 450), (422, 446),
    (432, 441), (442, 438), (452, 433), (456, 430), (460, 427), (464, 424),
    (468, 421), (472, 418), (476, 416), (480, 414),
]
FIT_ANCHORS = [  # left panel arch "Fit" ink trace (frame px; ochre-mask trace v3:
    # the left rise is steeper than the v1/v2 anchors measured it)
    (222, 458), (226, 450), (229, 438), (232, 426), (234, 418), (236, 411),
    (238, 405), (240, 400), (242, 393), (245, 388), (248, 382), (251, 376),
    (254, 371), (257, 368), (263, 370), (272, 372), (282, 376), (292, 385),
    (302, 398), (312, 411), (322, 424), (332, 437), (342, 446), (352, 455),
    (362, 457), (372, 460), (382, 461), (392, 455), (402, 452), (412, 449),
    (422, 446), (432, 443), (442, 440), (452, 438), (462, 442), (472, 456),
    (477, 462),
]
LEFT_DATA = [  # 7 open circles (PIL dark cores + probe_panels_1 count; probe_left_2 found 5 of these)
    (238, 399), (352, 457), (378, 460), (396, 457),
    (420, 446), (434, 440), (452, 436),
]

FIT2_ANCHORS = [  # right panel green 2nd-order ink trace (frame px; left arm
    # extended down to the measured steep entry ink at x~604-609)
    (604, 456), (606, 452), (608, 449), (610, 447), (614, 444), (618, 442),
    (628, 436), (638, 429), (648, 424), (658, 415), (668, 413), (678, 409),
    (688, 404), (698, 403), (708, 405), (718, 397), (728, 396), (738, 394),
    (748, 392), (758, 390), (768, 392), (778, 396), (788, 394), (798, 398),
    (808, 398), (818, 401), (828, 404), (838, 408), (848, 412), (858, 415),
]
RIGHT_DATA = [  # 11 open circles: PIL ring maps (v3 fine ink maps, all 11 rings
    # located) + probe_right_geometry_1 order/y (agreement within 1-3 px).
    # The curve passes through/near #2-#11 and misses the bottom-left outlier #1.
    (606, 460), (634, 419), (652, 415), (661, 427), (690, 397),
    (706, 398), (751, 409), (765, 387), (787, 408), (796, 396),
    (826, 397),
]
# Full measured trace of the red 10th-order curve (frame px), composed from the
# PIL ink-run maps + fine 2D ink maps (v3). Left to right:
#   enters at the bottom axis at (630,469), steep climb through circle #2,
#   crest ~(641,388); descends grazing #3 and #4 from above; trough (666,430);
#   rises through the #5/#6 cluster (arc slightly above their centers);
#   descends to trough (735,427); rises through #7 to the sharp hump on #8
#   (765,387); descends through #9; turns up through #10; near-vertical
#   up-spike to (803,373) [stops 9px below the top border]; [stroke break];
#   re-enters just under the top border at (823,366), descends steeply
#   through #11 and ends at (831,400). Circle #1 (606,460) is missed entirely.
FIT10_PATH = [
    (630, 469),                                              # enters at bottom axis
    (631, 458), (632, 444), (633, 430),                      # steep climb (olive blend zone)
    (634, 419),                                              # through #2
    (635, 411), (636, 403), (637, 396),                      # up to the crest
    (639, 389), (641, 388), (643, 390), (645, 392),          # crest / first hump
    (647, 396), (649, 405), (651, 411), (653, 413), (655, 414),   # graze above #3
    (657, 423), (659, 425), (661, 426),                      # through #4 (just above)
    (663, 429), (666, 430), (668, 429), (670, 428),          # trough 1
    (673, 425), (676, 423), (678, 417), (680, 415), (682, 414),   # rise
    (684, 409), (686, 405), (688, 400), (690, 398),          # through #5
    (693, 396), (696, 395), (698, 393), (701, 394), (704, 394),   # arc between
    (706, 395),                                              # over #6 (3 px above center)
    (709, 400), (712, 404), (715, 405), (717, 410), (719, 413),
    (721, 415), (723, 418), (725, 422), (728, 424), (731, 426),
    (734, 427), (737, 427),                                  # trough 2
    (740, 424), (743, 421), (746, 417), (749, 412), (751, 409),   # rise through #7
    (753, 406), (755, 402), (757, 399), (759, 394), (762, 390),
    (765, 387), (768, 387),                                  # hump peak on #8
    (771, 388), (774, 390), (777, 394), (780, 399),          # descend
    (783, 403), (785, 406), (787, 408),                      # through #9
    (790, 407), (793, 404), (795, 400), (796, 396),          # turn up through #10
    (798, 392), (800, 385), (802, 378), (803, 373),          # up-spike (stops below border)
]
FIT10_REENTRY = [  # separate stroke: re-enters just under the top border and
    # descends steeply through #11, ending at (831,400). The original has NO
    # red ink between x~804 and x~822 (verified gap in every column scan), so
    # this MUST be drawn as a second, disconnected stroke.
    (823, 366), (825, 375), (827, 383), (829, 390), (830, 397), (831, 400),
]

COLORS = {
    "bg": "#CCFFCC", "border": "#AA0000", "axes": "#404040",
    "target": "#0000FF", "fitL": "#FF6600",
    "fit2": "#00CC66", "fit10": "#FF0000",
}
LW = 1.6
MARKER_MS = 7.2      # circle diameter in points (measured ~7px, 1px=1pt)
MARKER_MEW = 1.1


def panel_local(panel, pts):
    ox, oy = PANELS[panel][0], PANELS[panel][1]
    return [(x - ox, y - oy) for x, y in pts]


def dense_spline(anchors, s=5.0, n=400):
    xs = np.array([p[0] for p in anchors], float)
    ys = np.array([p[1] for p in anchors], float)
    tck = splrep(xs, ys, s=s, k=3)
    xd = np.linspace(xs.min(), xs.max(), n)
    return xd, splev(xd, tck)


def render_panel(panel, curves, data, out_png):
    x0, y0, x1, y1 = PANELS[panel]
    w_px, h_px = x1 - x0, y1 - y0
    w_in, h_in = w_px / 72.0, h_px / 72.0
    fig = plt.figure(figsize=(w_in, h_in), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w_px)
    ax.set_ylim(h_px, 0)          # inverted: y down = frame-px convention
    ax.axis("off")
    ax.add_patch(Rectangle((0.5, 0.5), w_px - 1.0, h_px - 1.0,
                           facecolor=COLORS["bg"], edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((0.75, 0.75), w_px - 1.5, h_px - 1.5, fill=False,
                           edgecolor=COLORS["border"], linewidth=1.5, zorder=5))
    # axes (panel-local); v-axis tops at frame y~367 (measured), not at the border
    vx = AXES[panel]["vx"] - x0
    hy = AXES[panel]["hy"] - y0
    h_to = AXES[panel]["h_to"] - x0
    ax.plot([vx, vx], [7, hy], color=COLORS["axes"], lw=1.0, zorder=2)
    ax.plot([vx, h_to], [hy, hy], color=COLORS["axes"], lw=1.0, zorder=2)
    # curves: list of (x_dense, y_dense, color)
    for xd, yd, col in curves:
        yd = np.clip(yd, 4, h_px - 4)
        ax.plot(xd, yd, color=col, lw=LW, zorder=3, solid_capstyle="round")
    # data circles
    if data:
        dx = [p[0] for p in data]
        dy = [p[1] for p in data]
        ax.plot(dx, dy, "o", ms=MARKER_MS, mfc="white", mec="black",
                mew=MARKER_MEW, ls="none", zorder=4)
    fig.savefig(out_png, dpi=DPI)
    plt.close(fig)
    return out_png


# ---------------- curve builders ----------------

def build_left():
    # Target: spline through measured U-valley ink
    tx, ty = dense_spline(panel_local("left", TARGET_ANCHORS), s=6.0)
    # Fit: spline through measured arch ink
    fx, fy = dense_spline(panel_local("left", FIT_ANCHORS), s=4.0)
    return [(tx, ty, COLORS["target"]), (fx, fy, COLORS["fitL"])]


def build_right():
    x0, y0 = PANELS["right"][0], PANELS["right"][1]
    dloc = panel_local("right", RIGHT_DATA)
    dxa = np.array([p[0] for p in dloc], float)
    dya = np.array([p[1] for p in dloc], float)
    aloc = panel_local("right", FIT2_ANCHORS)
    axa = np.array([p[0] for p in aloc], float)
    aya = np.array([p[1] for p in aloc], float)

    # ---- candidate 2nd-order fits, scored against measured green ink ----
    cands = {}
    # (a) real algorithm on the measured DATA points: polyfit deg 2
    p = np.polynomial.Polynomial.fit(dxa, dya, 2)
    cands["polyfit_data_deg2"] = (np.clip(p(np.linspace(23, 283, 400)),
                                          4, 121))
    # (b) polyfit deg 2 on the measured curve anchors
    p2 = np.polynomial.Polynomial.fit(axa, aya, 2)
    cands["polyfit_anchors_deg2"] = p2(np.linspace(23, 283, 400))
    # (c) anchor spline (measured-ink exact)
    sx, sy = dense_spline(aloc, s=4.0)
    cands["anchor_spline"] = sy

    xd = np.linspace(23, 283, 400)
    scores = {}
    for name, yv in cands.items():
        if name == "anchor_spline":
            xs_q = sx
            yv_q = sy
        else:
            xs_q, yv_q = xd, yv
        inter = np.interp(axa, xs_q, yv_q)
        scores[name] = float(np.abs(inter - aya).mean())
    best2 = min(scores, key=scores.get)
    if best2 == "anchor_spline":
        fit2_x, fit2_y = sx, sy
    else:
        fit2_x, fit2_y = xd, cands[best2]

    # ---- 10th-order curve ----
    # Evidence banked: exact deg-9 polynomial interpolation (11 coefficients,
    # 11 points) EXPLODES on these noisy measured points (Runge phenomenon —
    # trace below), which would leave the panel entirely; a PCHIP-through-data
    # variant was generated as v1/v2 and superseded. The final curve is the
    # measured-ink composite FIT10_PATH (see its comment block): it misses only
    # the bottom-left outlier #1, passes through/near #2-#11 with the measured
    # humps/troughs, and ends with the measured up-spike + top re-entry stroke.
    # The slide's verbatim label "10th Order Fit" is kept; the deg-9 explosion
    # trace stays in the facts file as the documented algorithm evidence.
    interp9 = np.polynomial.Polynomial.fit(dxa, dya, 9)
    explosion_trace = {int(c): round(float(interp9(c - x0)), 1)
                        for c in (640, 660, 680, 700, 720, 740, 760, 780, 800, 820)}

    ploc = panel_local("right", FIT10_PATH)
    fit10_x, fit10_y = dense_spline(ploc, s=0.5, n=800)
    fit10_y = np.clip(fit10_y, 4, 121)
    rloc = panel_local("right", FIT10_REENTRY)
    re_x, re_y = dense_spline(rloc, s=0.5, n=60)
    re_y = np.clip(re_y, 4, 121)

    curves = [(fit2_x, fit2_y, COLORS["fit2"]),
              (fit10_x, fit10_y, COLORS["fit10"]),
              (re_x, re_y, COLORS["fit10"])]       # second, disconnected stroke
    return curves, scores, best2, (fit10_x, fit10_y), explosion_trace


# ---------------- PIL measurement / scoring ----------------

def mask_ochre(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 150) & (r - g > 35) & (r - b > 45) & (g < 210) & (g > 55)


def mask_green(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r < 160) & (g > 150) & (g < 235) & (b < 160) & (g - r > 45) & (g - b > 40)


def mask_darkred(a):
    """Right-panel 10th-order curve: mutated red reads dark-brown (93,52,30) or
    ochre halo (172,134,87); both are r-dominant. Excludes bg/green (g-dominant),
    black circles + axes (near-neutral), by color; border ring excluded by caller."""
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 85) & (r > g + 15) & (r > b + 15) & (g < 200)


def mask_color(a, hexcol, tol=120):
    ref = np.array(tuple(int(hexcol[i:i + 2], 16) for i in (1, 3, 5)), float)
    d = np.abs(a.astype(float) - ref).sum(axis=2)
    return d < tol


def midline(mask, x_from, x_to, ref=None, win=None):
    """Per-column mean-y of mask pixels in x range.

    If ref (dict col->y reference) + win given, keep only pixels within +/-win
    of the reference value for that column (kills legend/border contamination).
    """
    out = {}
    for c in range(x_from, x_to + 1):
        ys = np.nonzero(mask[:, c])[0]
        if not len(ys):
            continue
        if ref is not None and win is not None:
            rv = None
            if c in ref:
                rv = ref[c]
            else:  # nearest column with a reference
                near = [k for k in ref if abs(k - c) <= 4]
                if near:
                    rv = np.mean([ref[k] for k in near])
            if rv is None:
                continue
            keep = np.abs(ys - rv) <= win
            if not keep.any():
                continue
            ys = ys[keep]
        out[c] = float(ys.mean())
    return out


def anchors_ref(anchors, x0, y0):
    """dict local-col -> local-y from frame-px anchors (nearest, ±4 col tolerance
    handled in midline)."""
    return {int(p[0] - x0): float(p[1] - y0) for p in anchors}


def compare_midlines(orig_mid, rend_mid_scaled, tol_report=False):
    ds = []
    for c, oy in orig_mid.items():
        c2 = int(round(c))
        if c2 in rend_mid_scaled:
            ds.append(abs(rend_mid_scaled[c2] - oy))
    if not ds:
        return None
    ds = np.array(ds)
    return {"n": int(len(ds)), "mean": float(ds.mean()), "p95": float(np.percentile(ds, 95)),
            "max": float(ds.max())}


def score_panel(panel, png_path):
    """Compare rendered PNG ink to the original frame's measured ink.

    Original-frame masks are noisy (JPEG mutation, legend marks, border AA), so
    per-column midlines are WINDOWED around the measured anchor reference
    (+/-25 px): the comparison asks 'does the original's ink of this family sit
    where I drew the curve', not 'is the mask globally clean'.
    """
    x0, y0, x1, y1 = PANELS[panel]
    orig = np.asarray(Image.open(ORIG_JPG).convert("RGB")).astype(int)[y0:y1 + 1, x0:x1 + 1]
    rend_img = Image.open(png_path).convert("RGB")
    rend = np.asarray(rend_img.resize((x1 - x0 + 1, y1 - y0 + 1), Image.LANCZOS)).astype(int)
    report = {}
    H, W = rend.shape[:2]

    if panel == "left":
        # ---- fit (orange) vs original ochre ink, windowed around fit anchors
        om = mask_ochre(orig)
        om[:6, :] = False; om[-6:, :] = False; om[:, :6] = False; om[:, -6:] = False
        ref_f = anchors_ref(FIT_ANCHORS, x0, y0)
        o_mid = midline(om, 30, 286, ref=ref_f, win=25)
        rm = mask_color(rend, "#FF6600")
        r_mid = midline(rm, 30, 286)
        report["fitL_vs_ochre_windowed"] = compare_midlines(o_mid, r_mid)
        report["fitL_orig_ink_coverage"] = len(o_mid) / 257.0
        # ---- target (blue) vs measured anchors
        bm = mask_color(rend, "#0000FF")
        r_mid2 = midline(bm, 25, 296)
        ax_a = np.array([p[0] - x0 for p in TARGET_ANCHORS], float)
        ay_a = np.array([p[1] - y0 for p in TARGET_ANCHORS], float)
        ds = []
        for c, oy in zip(ax_a, ay_a):
            c2 = int(round(c))
            if c2 in r_mid2:
                ds.append(abs(r_mid2[c2] - oy))
        ds = np.array(ds)
        report["target_vs_anchors"] = {"n": int(len(ds)), "mean": float(ds.mean()),
                                        "p95": float(np.percentile(ds, 95)),
                                        "max": float(ds.max())}
    else:
        # ---- fit2 (green) vs original green ink, windowed around green anchors
        gm = mask_green(orig)
        gm[:6, :] = False; gm[-6:, :] = False; gm[:, :6] = False; gm[:, -6:] = False
        gm[75:112, 145:] = False        # legend block (samples + text + labels)
        ref_g = anchors_ref(FIT2_ANCHORS, x0, y0)
        o_mid = midline(gm, 40, 283, ref=ref_g, win=25)
        rm = mask_color(rend, "#00CC66")
        r_mid = midline(rm, 40, 283)
        report["fit2_vs_green_windowed"] = compare_midlines(o_mid, r_mid)
        report["fit2_orig_ink_coverage"] = len(o_mid) / 244.0
        # ---- fit10 (red) vs original dark-red/brown ink, windowed around the
        #      rendered curve (mutated red reads dark-brown, not ochre)
        om = mask_darkred(orig)
        om[:8, :] = False; om[-8:, :] = False; om[:, :8] = False; om[:, -8:] = False
        om[75:113, 160:] = False        # legend block (red sample seg + text + labels)
        rr = mask_color(rend, "#FF0000")
        rr[:7, :] = False; rr[-7:, :] = False; rr[:, :7] = False; rr[:, -7:] = False
        r10 = midline(rr, 22, 286)
        o10 = midline(om, 22, 286, ref={k: v for k, v in r10.items()}, win=28)
        report["fit10_vs_darkred_windowed"] = compare_midlines(o10, r10)
        report["fit10_orig_ink_coverage"] = (len(o10) / len(r10)) if r10 else 0.0
        report["fit10_render_columns"] = len(r10)

    # ---- border + axes placement check at FULL resolution (1pt lines average
    #      above the dark threshold after downscale, so check pre-resize) ----
    full = np.asarray(rend_img).astype(int)
    fH, fW = full.shape[:2]
    scale = fW / float(W)
    dk = (full[:, :, 0] < 100) & (full[:, :, 1] < 100) & (full[:, :, 2] < 100)
    ring = 14
    dk[:ring, :] = False; dk[-ring:, :] = False
    dk[:, :ring] = False; dk[:, -ring:] = False
    col_counts = dk.sum(axis=0)
    row_counts = dk.sum(axis=1)
    vx_local = AXES[panel]["vx"] - x0
    hy_local = AXES[panel]["hy"] - y0
    report["axes_check"] = {
        "v_axis_col_local": round(float(np.argmax(col_counts)) / scale, 2),
        "v_axis_expected": vx_local,
        "h_axis_row_local": round(float(np.argmax(row_counts)) / scale, 2),
        "h_axis_expected": hy_local,
    }
    return report


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    facts = {"panels": PANELS, "axes": AXES,
             "left_data": LEFT_DATA, "right_data": RIGHT_DATA,
             "colors": COLORS, "dpi": DPI, "lw": LW}

    # ---- low-order polyfit candidates for the LEFT fit (triage due diligence) ----
    lloc = panel_local("left", LEFT_DATA)
    lxa = np.array([p[0] for p in lloc], float)
    lya = np.array([p[1] for p in lloc], float)
    floc = panel_local("left", FIT_ANCHORS)
    fxa = np.array([p[0] for p in floc], float)
    fya = np.array([p[1] for p in floc], float)
    left_cand_scores = {}
    for deg in (1, 2, 3):
        try:
            p = np.polynomial.Polynomial.fit(lxa, lya, deg)
            inter = np.interp(fxa, np.linspace(29, 296, 400), p(np.linspace(29, 296, 400)))
            left_cand_scores[f"polyfit_left_data_deg{deg}"] = float(np.abs(inter - fya).mean())
        except Exception as ex:
            left_cand_scores[f"polyfit_left_data_deg{deg}"] = f"ERR {ex}"
    facts["left_fit_candidate_scores_vs_measured_ink"] = left_cand_scores

    lcurves = build_left()
    lp = render_panel("left", lcurves, panel_local("left", LEFT_DATA),
                       os.path.join(OUTDIR, "graph_left_v3.png"))
    rcurves, fit2_scores, best2, (f10x, f10y), explosion = build_right()
    rp = render_panel("right", rcurves, panel_local("right", RIGHT_DATA),
                      os.path.join(OUTDIR, "graph_right_v3.png"))
    facts["right_fit2_candidate_scores_vs_green_ink"] = fit2_scores
    facts["right_fit2_chosen"] = best2
    facts["fit10_deg9_interpolation_explosion_trace"] = explosion
    facts["fit10_final_method"] = ("measured-ink composite FIT10_PATH: enters bottom (630,469), "
                                  "climb through #2, crest (641,388), grazes #3/#4, troughs, "
                                  "hump on #8, through #9-#11, up-spike (803,373) + top "
                                  "re-entry (823,366)-(831,400); misses only outlier #1; "
                                  "deg-9 Runge explosion banked above as algorithm evidence")

    # trace of the final fit10 curve (sanity / wildness check, frame y)
    x0r, y0r = PANELS["right"][0], PANELS["right"][1]
    trace = {}
    for c in (640, 660, 680, 700, 720, 740, 760, 780, 800, 820):
        trace[c] = round(float(np.interp(c - x0r, f10x, f10y)) + y0r, 1)
    facts["fit10_trace_frame_y"] = trace

    s_left = score_panel("left", lp)
    s_right = score_panel("right", rp)
    facts["score_left_v3"] = s_left
    facts["score_right_v3"] = s_right

    out_json = os.path.join(OUTDIR, "graphgen_facts_v3.json")
    with open(out_json, "w") as f:
        json.dump(facts, f, indent=2, default=str)
    print(json.dumps({k: facts[k] for k in
                      ("left_fit_candidate_scores_vs_measured_ink",
                       "right_fit2_candidate_scores_vs_green_ink",
                       "right_fit2_chosen",
                       "fit10_deg9_interpolation_explosion_trace",
                       "fit10_trace_frame_y",
                       "score_left_v3", "score_right_v3")},
                     indent=2, default=str))
    print("PNGs:", lp, rp)
    print("facts:", out_json)


if __name__ == "__main__":
    main()
