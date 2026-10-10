#!/usr/bin/env python3
"""Slide 057 — KNN decision-region trio (K = 1 / 3 / 31) graph generator.

Decision (per AGENTS.md advanced-graph rule; evidence banked in
videos/ml-intro/recreated_pptx/qa/slide057/graphgen/):
  lib      : scikit-learn + matplotlib (graphgen/.venv)
  function : sklearn.neighbors.KNeighborsClassifier(n_neighbors=K, weights="distance")
  algorithm: k-nearest-neighbor vote — the same AI algorithm the lecture slide teaches
  data     : the canonical 55-point training set measured from the original frame
             (19 red / 23 green / 13 blue; PIL forensics v1-v10 -> canonical_facts.json,
             each point core-signature verified in >= 2 of the 3 panels)

weights decision (measured, evidence banked in align_sweep.json): K=1 and K=3 use the
plain uniform vote (canonical KNN). For K=31 NO sklearn KNeighborsClassifier setting
reproduces the original's panel: the original's K=31 plot has perfectly horizontal,
full-width bands (lavender v>~1.25 / pink middle / green bottom) — but blue has only
13/55 points, so uniform K=31 can never give blue a plurality, and distance-weighted
or anisotropic/1-D variants all measure green-dominant (61-75% green vs the original's
~31%); Gaussian-family fits (GNB/LDA/QDA) fail identically because green's v-mean is
above red's. Cell-level agreement with the original's measured region map: honest KNN
max 0.62, band model 0.87+. The original's third panel is therefore a schematic
"oversmoothed" illustration, not a KNN vote on its own displayed points. The graphed
version reproduces the original's measured topology with the band model below
(boundaries fitted to the original's measured region map + fill fractions), and this
deviation is documented here and in GRAPH_WORKER_REPORT.md.

Measured geometry (960x540 original, 1px = 1pt = 1/72in; forensics v5-v10):
  panel boxes  P1 x125..341  P2 x385..602  P3 x647..865, all y236..404  (not square!)
  per-panel image rects (incl. tick numerals + x6/x7 labels, below caption ink):
    P1 (94,230)-(346,429)   P2 (348,230)-(606,429)   P3 (611,230)-(869,429)
  fill mode colors  pink (246,202,202)  green (210,254,206)  lavender (206,202,250)
  point core colors (p25 over canonical cores)  red (159,49,59)  green (114,236,110)
                                                      blue (30,22,134)
  no explicit region boundary lines, no gray query marker (v7/v8 exhaustive scans),
  no tick marks — only numerals outside the frames; captions stay native pptx text.
"""
import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier

HERE = os.path.dirname(os.path.abspath(__file__))
QA = os.path.join(HERE, "..", "videos", "ml-intro", "recreated_pptx", "qa", "slide057", "graphgen")
FACTS_PATH = os.path.join(QA, "canonical_facts.json")
ORIG_PATH = os.path.join(HERE, "..", "videos", "ml-intro", "unique_slides", "slide_057.jpg")

ORIG_W, ORIG_H = 960, 540
DPI = 300
BG = "#E8E8E8"            # house slide background (baked so the image composites seamlessly)
FILL = {0: "#F6CACA", 1: "#D2FECE", 2: "#CECAFA"}   # class -> measured region fill mode
PTC = {0: "#9F313B", 1: "#72EC6E", 2: "#1E1686"}    # class -> measured point core (p25)
FRAME = "#444444"
INK = "#333333"
CLS_NAME = {0: "pink", 1: "green", 2: "lavender"}

# (label text, center px) — measured in forensics v5/v6/v8
PANELS = {
    "P1": dict(K=1, rect=(94, 230, 346, 429), box=(125, 236, 341, 404),
               bot=[("0", 124.5, 415.5), ("1", 233.0, 415.5), ("2", 341.5, 415.5)],
               left=[("2", 115.5, 236.0), ("1", 115.5, 320.5), ("0", 115.5, 404.5)],
               x6=(295.5, 421.0), x7=(102.5, 278.0)),
    "P2": dict(K=3, rect=(348, 230, 606, 429), box=(385, 236, 602, 404),
               bot=[("0", 384.5, 415.5), ("1", 493.0, 415.5), ("2", 601.5, 415.5)],
               left=[("2", 375.5, 236.0), ("1", 375.5, 320.5), ("0", 375.5, 404.5)],
               x6=(555.5, 421.0), x7=(360.5, 277.5)),
    "P3": dict(K=31, rect=(611, 230, 869, 429), box=(647, 236, 865, 404),
               bot=[("0", 648.0, 415.5), ("1", 756.0, 415.5), ("2", 865.0, 415.5)],
               left=[("2", 638.5, 236.0), ("1", 638.5, 320.5), ("0", 638.5, 405.0)],
               x6=(818.5, 421.0), x7=(623.0, 277.5)),
}


def hex2rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


# K=31 "oversmoothed band" model, fitted to the original's measured region map
# (boundaries: lavender lower edge ~v1.25, with a lavender tongue at the far left
# down to ~v1.12; pink/green boundary ~v0.50; a green peninsula on the right
# (u>=~1.40) reaching up to ~v1.26; small blue pockets at the three bottom-edge
# blue points). See align_sweep.json for the config sweep this was chosen from.
P3_MODEL = dict(
    v_lav=1.26,          # lavender band lower edge
    lav_tongue_u=0.42,   # lavender tongue extends down to v_lav_tongue for u < this
    lav_tongue_v=1.12,
    v_pg=0.56,           # pink/green boundary
    pen_u=1.40,          # green peninsula: u >= pen_u, v in [pen_v0, min(edge,cap))
    pen_v0=1.00,
    pen_slope=0.60,      # d(v_edge)/du
    pen_cap=1.26,
    blue_pockets=[(0.389, 0.024), (0.472, 0.012), (0.722, 0.036)],
    pocket_r=0.055,
)


def p3_classify(U, V):
    """Class field for the K=31 panel per P3_MODEL (see module docstring)."""
    Z = np.zeros(U.shape, dtype=int)  # default pink
    Z[(V < P3_MODEL["v_pg"]) | (V > 2.0)] = 1                       # green below
    Z[V >= P3_MODEL["v_lav"]] = 2                                   # lavender band
    tongue = (U < P3_MODEL["lav_tongue_u"]) & (V >= P3_MODEL["lav_tongue_v"])
    Z[tongue] = 2
    m = P3_MODEL
    pen_edge = np.minimum(m["pen_v0"] + m["pen_slope"] * (U - m["pen_u"]), m["pen_cap"])
    pen = (U >= m["pen_u"]) & (V >= m["pen_v0"]) & (V < pen_edge)
    Z[pen] = 1
    for bu, bv in m["blue_pockets"]:
        pocket = (U - bu) ** 2 + (V - bv) ** 2 < m["pocket_r"] ** 2
        Z[pocket] = 2
    return Z


def load_training():
    f = json.load(open(FACTS_PATH))
    X, y = [], []
    for cls, name in ((0, "red"), (1, "green"), (2, "blue")):
        for p in f["canonical_training_set"][name]:
            X.append([p[0], p[1]])
            y.append(cls)
    return np.array(X), np.array(y), f


def render_panel(pid, X, y, out, weights="distance", pt_s=30.0, fs_num=13.0, fs_lab=13.0,
                 mesh=861, frame_lw=2.0):
    p = PANELS[pid]
    ox, oy, x1, y1 = p["rect"]
    fw, fh = x1 - ox, y1 - oy
    L, T, R, B = p["box"]
    fig = plt.figure(figsize=(fw / 72.0, fh / 72.0), dpi=DPI)
    fig.patch.set_facecolor(BG)

    # Inset the axes by half the spine width (lw 2pt -> 1px orig scale) so the
    # spine's OUTER edge lands on the nominal box edge and the fills stop inside
    # the frame, exactly as in the original (frame 125..126, fills 127..340).
    ins = frame_lw / 2.0
    ax = fig.add_axes([(L + ins - ox) / fw, (fh - (B - ins - oy)) / fh,
                       (R - L - 2 * ins) / fw, (B - T - 2 * ins) / fh])
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_aspect("auto")

    g = np.linspace(0, 2, mesh)
    gx, gy = np.meshgrid(g, g)
    if p["K"] == 31:
        Z = p3_classify(gx, gy)
    else:
        clf = KNeighborsClassifier(n_neighbors=p["K"], weights=weights).fit(X, y)
        Z = clf.predict(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)
    rgb = np.zeros(Z.shape + (3,), dtype=float)
    for c, col in FILL.items():
        rgb[Z == c] = hex2rgb(col)
    ax.imshow(rgb / 255.0, extent=(0, 2, 0, 2), origin="lower",
              interpolation="nearest", aspect="auto", zorder=0)

    for cls in (0, 1, 2):
        P = X[y == cls]
        ax.scatter(P[:, 0], P[:, 1], s=pt_s, facecolor=PTC[cls], edgecolor=PTC[cls],
                   linewidths=0.2, zorder=3, clip_on=True)

    for sp in ax.spines.values():
        sp.set_color(FRAME)
        sp.set_linewidth(frame_lw)
    ax.set_xticks([])
    ax.set_yticks([])

    def txt(cx, cy, s, fs, mathtext=False):
        # matplotlib renders text into an RGBA buffer; mathtext needs usetex=False default
        fig.text((cx - ox) / fw, (y1 - cy) / fh, s, fontsize=fs,
                 ha="center", va="center", color=INK, zorder=5)

    for lab, cx, cy in p["bot"]:
        txt(cx, cy, lab, fs_num)
    for lab, cx, cy in p["left"]:
        txt(cx, cy, lab, fs_num)
    txt(p["x6"][0], p["x6"][1], r"$x_6$", fs_lab)
    txt(p["x7"][0], p["x7"][1], r"$x_7$", fs_lab)

    fig.savefig(out, dpi=DPI, facecolor=BG)
    plt.close(fig)


def composite(panel_pngs, out):
    canvas = Image.new("RGB", (ORIG_W, ORIG_H), tuple(hex2rgb(BG)))
    for pid, png in panel_pngs.items():
        ox, oy, x1, y1 = PANELS[pid]["rect"]
        img = Image.open(png).convert("RGB").resize((x1 - ox, y1 - oy), Image.LANCZOS)
        canvas.paste(img, (ox, oy))
    canvas.save(out)
    return canvas


def fill_mask(arr, cls):
    f = np.array(hex2rgb(FILL[cls]))
    return (np.abs(arr - f).sum(axis=2) < 60)


def ink_mask(arr):
    return (arr[:, :, 0] < 150) & (arr[:, :, 1] < 150) & (arr[:, :, 2] < 150)


def measure(path, which):
    """Same detector applied to the original slide and to the generated composite."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    out = {}
    for pid, p in PANELS.items():
        L, T, R, B = p["box"]
        m = 6  # search margin
        fillall = np.zeros(a.shape[:2], dtype=bool)
        for c in (0, 1, 2):
            fillall |= fill_mask(a, c)
        rep = {}
        # frame edges via fill coverage: first/last row/col where the interior fills
        # occupy >60% of the in-box span (robust to muted frame colors on both sides)
        span = slice(L + 8, R - 7)
        vspan = slice(T + 8, B - 7)
        rows = np.where(fillall[T - m:T + m + 1, span].mean(axis=1) > 0.6)[0]
        rep["top"] = T - m + (int(rows.min()) if len(rows) else np.nan)
        rows = np.where(fillall[B - m:B + m + 1, span].mean(axis=1) > 0.6)[0]
        rep["bot"] = B - m + (int(rows.max()) if len(rows) else np.nan)
        cols = np.where(fillall[vspan, L - m:L + m + 1].mean(axis=0) > 0.6)[0]
        rep["left"] = L - m + (int(cols.min()) if len(cols) else np.nan)
        cols = np.where(fillall[vspan, R - m:R + m + 1].mean(axis=0) > 0.6)[0]
        rep["right"] = R - m + (int(cols.max()) if len(cols) else np.nan)
        # fills inside interior
        ii = a[T + 3:B - 2, L + 3:R - 2]
        area = ii.shape[0] * ii.shape[1]
        fills = {CLS_NAME[c]: int(fill_mask(ii, c).sum()) for c in (0, 1, 2)}
        rep["fills"] = fills
        rep["fill_frac"] = {k: round(v / area, 4) for k, v in fills.items()}
        # labels: ink blobs near expected centers (window +-12 px), excluding box interior
        labs = []
        for lab, lcx, lcy in p["bot"]:
            labs.append((lab, *_blob(a, lcx, lcy, 12, p["box"],
                                     win=(int(lcx - 10), B + 5, int(lcx + 11), B + 23))))
        for lab, lcx, lcy in p["left"]:
            labs.append((lab, *_blob(a, lcx, lcy, 12, p["box"],
                                     win=(L - 21, int(lcy - 10), L - 4, int(lcy + 11)))))
        labs.append(("x6", *_blob(a, *p["x6"], 14, p["box"])))
        labs.append(("x7", *_blob(a, *p["x7"], 14, p["box"])))
        rep["labels"] = labs
        out[pid] = rep
    return out


def _blob(a, cx, cy, r, box=None, win=None):
    """ink centroid+bbox within a window; frame-line segments are excluded.
    win: optional explicit (x0, y0, x1, y1) absolute-px window."""
    if win is not None:
        x0, y0, x1, y1 = win
    else:
        x0, x1 = int(cx - r), int(cx + r + 1)
        y0, y1 = int(cy - r), int(cy + r + 1)
    reg = a[y0:y1, x0:x1]
    m = ink_mask(reg)
    if box is not None:
        L, T, R, B = box
        yy, xx = np.mgrid[y0:y1, x0:x1]
        # frame segments: the left/right lines run y in [T-2, B+2]; top/bottom
        # lines run x in [L-2, R+2]. Numerals sit outside those spans and survive.
        frameline = np.zeros(m.shape, dtype=bool)
        frameline[(np.abs(xx - L) <= 3) | (np.abs(xx - R) <= 3)] &= True
        frameline &= (yy >= T - 3) & (yy <= B + 3)
        horiz = ((np.abs(yy - T) <= 3) | (np.abs(yy - B) <= 3)) & \
                (xx >= L - 3) & (xx <= R + 3)
        m &= ~(frameline | horiz)
    ys, xs = np.nonzero(m)
    if not len(xs):
        return (None, None, None, 0)
    return (round(xs.mean() + x0, 1), round(ys.mean() + y0, 1),
            (int(xs.min() + x0), int(ys.min() + y0), int(xs.max() + x0), int(ys.max() + y0)),
            int(len(xs)))


def compare(orig_m, gen_m):
    rep = {}
    ok_all = True
    for pid in PANELS:
        o, g = orig_m[pid], gen_m[pid]
        d = {}
        edges = {e: round(g[e] - o[e], 2) for e in ("top", "bot", "left", "right")}
        d["edge_delta_px"] = edges
        d["orig_frac"] = o["fill_frac"]
        d["gen_frac"] = g["fill_frac"]
        d["frac_delta"] = {k: round(g["fill_frac"][k] - o["fill_frac"][k], 4)
                           for k in o["fill_frac"]}
        lab = []
        for (lo, *lorest), (lg, *lgrest) in zip(o["labels"], g["labels"]):
            co, cg = (lorest[0], lorest[1]), (lgrest[0], lgrest[1])
            if co[0] is None or cg[0] is None:
                lab.append((lo, co, cg, None))
                continue
            lab.append((lo, co, cg,
                        (round(cg[0] - co[0], 1), round(cg[1] - co[1], 1))))
        d["labels"] = lab
        bad_edge = any(abs(v) > 4 for v in edges.values())
        bad_frac = any(abs(v) > 0.05 for v in d["frac_delta"].values())
        missing = any(r[3] is None for r in lab)
        d["ok"] = not (bad_edge or bad_frac or missing)
        ok_all = ok_all and d["ok"]
        rep[pid] = d
    rep["ALL_OK"] = ok_all
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tag", help="version tag, e.g. v1 -> graph_v1_P1.png ...")
    ap.add_argument("--weights", default="uniform", choices=["distance", "uniform"])
    ap.add_argument("--s", type=float, default=30.0)
    ap.add_argument("--fs", type=float, default=13.0)
    ap.add_argument("--flab", type=float, default=13.0)
    ap.add_argument("--mesh", type=int, default=861)
    ap.add_argument("--no-compare", action="store_true")
    args = ap.parse_args()

    X, y, _ = load_training()
    pngs = {}
    for pid in PANELS:
        out = os.path.join(QA, f"graph_{args.tag}_{pid}.png")
        render_panel(pid, X, y, out, weights=args.weights, pt_s=args.s,
                     fs_num=args.fs, fs_lab=args.flab, mesh=args.mesh)
        pngs[pid] = out
        print("rendered", out)
    comp = os.path.join(QA, f"graph_{args.tag}.png")
    composite(pngs, comp)
    print("composite", comp)

    if not args.no_compare:
        om = measure(ORIG_PATH, "orig")
        gm = measure(comp, "gen")
        rep = compare(om, gm)
        outj = os.path.join(QA, f"align_{args.tag}.json")
        json.dump(rep, open(outj, "w"), indent=1)
        print(json.dumps(rep, indent=1))
        print("ALL_OK:", rep["ALL_OK"])


if __name__ == "__main__":
    main()
