#!/usr/bin/env python3
"""Slides 16/17/18 — Bishop-style polynomial-fit 2x2 grid generator (shared).

Decision record (graphgen/README.md + per-slide qa/slideNNN/graphgen/):
  lib      : numpy.polynomial.Polynomial.fit + matplotlib (pixel-space canvas)
  function : least-squares polynomial fits of degree M = 0, 1, 3; exact degree-9
             interpolant (Lagrange-equivalent, numpy.polyfit deg 9 on 10 pts)
  algorithm: the lecture's own demo — polynomial curve fitting on noisy sine data
  data     : canonical measured dataset (slide 016's markers, PIL-measured;
             slides 17/18 repeat the same scene at smaller scale and their own
             markers are too tiny/compressed to extract all 10 — slots 0, 1, 9
             that ARE extractable there confirm identical values):
               x = i/9, t = [0.343, 0.813, 1.015, 0.98, 0.11, 0.196,
                             -0.805, -0.437, -0.543, 0.275]
  plot     : 2x2 grid of MATLAB-style boxed axes; green true sine + red fit
             curve over data x in [0,1], blue data markers, M-labels.

Geometry is measured from the original frames (960x540, 1px = 1pt); the graph
image canvas reproduces the measured region at 300 dpi (1 canvas pt = 1 frame
px), so the image drops into the pptx at the measured region size/position.

Measured constants (banked forensics: qa/slide{016,017,018}/graphgen/
forensics_polygrid_{nnn}_out.json + tick/ink scans 2026-10-09):

slide 016  region/container (192,187)-(719,497), red #CC0000 2.5pt border
  boxes    TL(209,198,432,321) TR(467,198,691,321) BL(209,346,432,469) BR(467,346,691,469)
  cal      L: x0=219.2 sx=203.7 | R: x0=478.2 sx=202.9   (x ticks 219.2/422.5, 478/680.5)
           T: t0=259.5 st=39.0 | B: t0=407.5 st=38.8   (t ticks 220.5/259.5/298.5, 368.5/407.5/446)
  chrome   gray boxes #B3B3B3 1pt; y tick marks 8px + "1/0/-1" 6pt black labels
           right-aligned ~1px left of box; x tick marks 5px + "0/1" 6pt labels
           below; yellow #FFFF99 label boxes w/ black "M = K"; NO x/t axis
           titles; NO annotation dot (both checked absent in the original).
  inks     green #00FF00 red #FF0000 blue #0000FF open circles d=7px;
           curve lw ~2px (measured ink ~2.6px incl. AA).

slide 017/018  region/container (552,131)-(872,318), faint light border, white fill
  boxes    TL(561,137,700,212) TR(720,137,857,212) BL(561,227,700,303) BR(720,227,857,303)
  cal      L: x0=568.5 sx=124.5 | R: x0=726.5 sx=124.7   (x ticks 568.5/693, 726.5/851)
           T: t0=174.55 st=23.55 | B: t0=265.5 st=23.55 (t ticks 151/174.5/198+, 242/265.5/289)
           (refined from the banked x_cal anchor via the tick-mark + LSQ scans;
            the banked anchor's dots_per_box x-values are known-miscalibrated)
  chrome   thin light-gray box lines, dark tick marks (t=1,0,-1 left; x=0,1
           below), NO numeric labels, tiny dark "M = K" text at each box's
           upper-right (text right edge ~2px from box right, ~10px below top).
  inks     17: green #90EE90 red #FF0000 blue #0000FF;  18: green #00CC00
           red #CC0000 blue #0000CC; solid dots d=5px; curve lw ~1.3px.

Usage:
  python graphgen/slide_16_17_18_polyfit.py 016 [png_path]
  python graphgen/slide_16_17_18_polyfit.py 016 --verify png_path
Outputs default to videos/ml-intro/recreated_pptx/qa/slideNNN/graphgen/.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from PIL import Image

# ---------------- canonical measured dataset (slide 016 markers) ----------------
XS = np.array([i / 9 for i in range(10)])
TS = np.array([0.343, 0.813, 1.015, 0.98, 0.110, 0.196,
               -0.805, -0.437, -0.543, 0.275])

FIT_M = [0, 1, 3, 9]          # degrees, box order TL TR BL BR
BOX_ORDER = ["TL", "TR", "BL", "BR"]

# ---------------- per-slide configuration (all measured; see docstring) --------
CFG = {
    "016": dict(
        region=(192, 187, 719, 497),
        pad=3,                       # canvas margin (frame px) for the 2.5pt border stroke
        container=dict(border="#CC0000", lw=2.5, fill="#FFFFFF"),
        boxes=dict(TL=(209, 198, 432, 321), TR=(467, 198, 691, 321),
                   BL=(209, 346, 432, 469), BR=(467, 346, 691, 469)),
        xcal=dict(L=(219.2, 203.7), R=(478.2, 202.9)),
        tcal=dict(T=(259.5, 39.0), B=(407.5, 38.8)),
        axes=dict(color="#B3B3B3", lw=1.0),
        colors=dict(green="#00FF00", red="#FF0000", blue="#0000FF"),
        curve_lw=2.0,
        dots=dict(d=7.0, mew=1.2, open=True),
        chrome="big",                # tick marks + numeric labels + yellow M-boxes
        labels=dict(rects=dict(TL=(371, 211, 419, 229), TR=(634, 211, 682, 229),
                                BL=(371, 361, 419, 379), BR=(634, 361, 682, 379)),
                    fill="#FFFF99", text="#000000", fs=9.5),
        tick=dict(mark="#B3B3B3", len_y=8, len_x=5, lw=0.75,
                  label="#000000", fs=6.0),
    ),
    "017": dict(
        region=(552, 131, 872, 318),
        pad=0,
        container=dict(border="#E0D6D6", lw=0.75, fill="#FFFFFF"),
        boxes=dict(TL=(561, 137, 700, 212), TR=(720, 137, 857, 212),
                   BL=(561, 227, 700, 303), BR=(720, 227, 857, 303)),
        xcal=dict(L=(568.5, 124.5), R=(726.5, 124.7)),
        tcal=dict(T=(174.55, 23.55), B=(265.5, 23.55)),
        axes=dict(color="#AEB4AE", lw=0.75),
        colors=dict(green="#90EE90", red="#FF0000", blue="#0000FF"),
        curve_lw=1.3,
        dots=dict(d=5.0, mew=0.6, open=False),
        chrome="small",              # tick marks only + tiny in-box M text
        labels=dict(right_gap=2.0, top_gap=10.0, text="#444444", fs=5.0),
        tick=dict(mark="#7A7E78", len_y=4.5, len_x=4.0, lw=0.75),
    ),
    "018": dict(
        region=(552, 131, 872, 318),
        pad=0,
        container=dict(border="#E0D6D6", lw=0.75, fill="#FFFFFF"),
        boxes=dict(TL=(561, 137, 700, 212), TR=(720, 137, 857, 212),
                   BL=(561, 227, 700, 303), BR=(720, 227, 857, 303)),
        xcal=dict(L=(568.5, 124.5), R=(726.5, 124.7)),
        tcal=dict(T=(174.55, 23.55), B=(265.5, 23.55)),
        axes=dict(color="#AEB4AE", lw=0.75),
        colors=dict(green="#00CC00", red="#CC0000", blue="#0000CC"),
        curve_lw=1.3,
        dots=dict(d=5.0, mew=0.6, open=False),
        chrome="small",
        labels=dict(right_gap=2.0, top_gap=10.0, text="#444444", fs=5.0),
        tick=dict(mark="#7A7E78", len_y=4.5, len_x=4.0, lw=0.75),
    ),
}

# original-measured ink targets (frame px) for the closed-loop check, from the
# banked forensics JSONs (per-box red fit ink bbox; sine extremes where clean)
ORIG_MEASURED = {
    "016": dict(
        red=dict(TL=(251, 253), TR=(228, 277), BL=(367, 435), BR=(348, 467)),
        flat_y=252, m1=(228, 277),
        labels=dict(TL=(372, 212, 418, 229), TR=(634, 211, 680, 227),
                    BL=(372, 362, 418, 375), BR=(634, 362, 680, 375)),
    ),
    "017": dict(
        red=dict(TL=(169, 172), TR=(160, 180), BL=(240, 281), BR=(231, 301)),
        flat_y=170,
    ),
    "018": dict(
        red=dict(TL=(169, 171), TR=(160, 181), BL=(241, 281), BR=(231, 301)),
        flat_y=170,
    ),
}


def fits():
    """Return {M: callable} least-squares / interpolating fits of the data."""
    out = {}
    for M in FIT_M:
        p = np.polynomial.Polynomial.fit(XS, TS, M)  # deg 9 on 10 pts interpolates
        out[M] = lambda x, p=p: p(x)
    return out


def box_cal(cfg, key):
    """(X(x), Y(t)) px-mappers + clip rect for a box."""
    bx0, by0, bx1, by1 = cfg["boxes"][key]
    col = "L" if key in ("TL", "BL") else "R"
    row = "T" if key in ("TL", "TR") else "B"
    x0, sx = cfg["xcal"][col]
    t0, st = cfg["tcal"][row]
    return (lambda x: x0 + x * sx,
            lambda t: t0 - t * st,
            (bx0, by0, bx1, by1))


def render(nnn, out_png):
    cfg = CFG[nnn]
    rx0, ry0, rx1, ry1 = cfg["region"]
    pad = cfg["pad"]
    ox, oy = rx0 - pad, ry0 - pad                 # canvas origin (frame px)
    W, H = (rx1 - rx0) + 2 * pad, (ry1 - ry0) + 2 * pad   # canvas size (frame px)
    dpi = 300
    fig = plt.figure(figsize=(W / 72.0, H / 72.0), dpi=dpi)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)          # y down, frame-px space
    ax.axis("off")
    matplotlib.rcParams["font.family"] = "Arial"

    F = lambda fx: fx - ox     # frame px -> canvas px
    G = lambda fy: fy - oy

    # container fill + border (baked in; the pptx graphed build drops its shape)
    c = cfg["container"]
    rx, ry, rw, rh = F(rx0), G(ry0), (rx1 - rx0), (ry1 - ry0)
    ax.add_patch(Rectangle((rx, ry), rw, rh, facecolor=c["fill"],
                           edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((rx, ry), rw, rh, facecolor="none",
                           edgecolor=c["border"], linewidth=c["lw"], zorder=6))

    fitfns = fits()
    cols = cfg["colors"]

    for key, M in zip(BOX_ORDER, FIT_M):
        X, Y, (bx0, by0, bx1, by1) = box_cal(cfg, key)
        bx, by, bw, bh = F(bx0), G(by0), bx1 - bx0, by1 - by0
        clip = Rectangle((bx, by), bw, bh, transform=ax.transData,
                         facecolor="none", edgecolor="none")
        ax.add_patch(clip)

        # axes box
        ax.add_patch(Rectangle((bx, by), bw, bh, facecolor="none",
                               edgecolor=cfg["axes"]["color"],
                               linewidth=cfg["axes"]["lw"], zorder=2))
        # ticks
        tk = cfg["tick"]
        t0, st = cfg["tcal"]["T" if key in ("TL", "TR") else "B"]
        for tv in (1, 0, -1):
            ty = G(Y(tv))
            ax.plot([bx - tk["len_y"], bx], [ty, ty], color=tk["mark"],
                    lw=tk["lw"], zorder=3, solid_capstyle="butt")
        for xv in (0, 1):
            tx = F(X(xv))
            ax.plot([tx, tx], [by + bh, by + bh + tk["len_x"]], color=tk["mark"],
                    lw=tk["lw"], zorder=3, solid_capstyle="butt")

        if cfg["chrome"] == "big":
            # numeric tick labels (6pt, dark) — y labels right-aligned ~2px
            # left of the box edge, x labels centered under the x ticks
            for tv in (1, 0, -1):
                ax.text(bx - 2, G(Y(tv)), str(tv), ha="right", va="center",
                        fontsize=tk["fs"], color=tk["label"], zorder=5)
            for xv in (0, 1):
                ax.text(F(X(xv)), by + bh + 5.5, str(xv), ha="center", va="top",
                        fontsize=tk["fs"], color=tk["label"], zorder=5)

        # green true sine over data x in [0,1]
        gx = np.linspace(0, 1, 240)
        (gl,) = ax.plot([F(X(v)) for v in gx], [G(Y(np.sin(2 * np.pi * v))) for v in gx],
                        color=cols["green"], lw=cfg["curve_lw"], zorder=3,
                        solid_capstyle="butt")
        gl.set_clip_path(clip)

        # red fit curve (dense sampling for M=9; clipped at the box like MATLAB)
        fx = np.linspace(0, 1, 900 if M == 9 else 240)
        fv = fitfns[M](fx)
        (rl,) = ax.plot([F(X(v)) for v in fx], [G(Y(v)) for v in fv],
                        color=cols["red"], lw=cfg["curve_lw"], zorder=4,
                        solid_capstyle="butt")
        rl.set_clip_path(clip)

        # blue data markers
        d = cfg["dots"]
        if d["open"]:
            ax.plot([F(X(v)) for v in XS], [G(Y(v)) for v in TS], "o",
                    ms=d["d"], mfc="white", mec=cols["blue"], mew=d["mew"],
                    zorder=5, linestyle="none")
        else:
            ax.plot([F(X(v)) for v in XS], [G(Y(v)) for v in TS], "o",
                    ms=d["d"], mfc=cols["blue"], mec=cols["blue"], mew=d["mew"],
                    zorder=5, linestyle="none")

        # M label
        if cfg["chrome"] == "big":
            lx0, ly0, lx1, ly1 = cfg["labels"]["rects"][key]
            ax.add_patch(Rectangle((F(lx0), G(ly0)), lx1 - lx0, ly1 - ly0,
                                   facecolor=cfg["labels"]["fill"], edgecolor="none",
                                   zorder=6))
            ax.text((F(lx0) + F(lx1)) / 2, (G(ly0) + G(ly1)) / 2, "M = %d" % M,
                    ha="center", va="center", fontsize=cfg["labels"]["fs"],
                    color=cfg["labels"]["text"], zorder=7)
        else:
            ax.text(bx + bw - cfg["labels"]["right_gap"],
                    by + cfg["labels"]["top_gap"], "M = %d" % M,
                    ha="right", va="top", fontsize=cfg["labels"]["fs"],
                    color=cfg["labels"]["text"], zorder=7)

    fig.savefig(out_png, dpi=dpi, facecolor="white")
    plt.close(fig)
    return out_png


# ---------------- closed-loop verification (PIL ink edges vs measured) ----------

def _masks(nnn, arr):
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    c = CFG[nnn]["colors"]
    if nnn == "016":
        return dict(
            green=(g > 200) & (r < 110) & (b < 110),
            red=(r > 200) & (g < 100) & (b < 100),
            blue=(b > 190) & (r < 100) & (g < 100),
            yellow=(r > 235) & (g > 235) & (b < 210),
        )
    if nnn == "017":
        return dict(
            green=(g > 200) & (r > 90) & (r < 200) & (b > 90) & (b < 200),
            red=(r > 200) & (g < 100) & (b < 100),
            blue=(b > 190) & (r < 100) & (g < 100),
        )
    return dict(  # 018: #00CC00 / #CC0000 / #0000CC
        green=(g > 160) & (r < 90) & (b < 90),
        red=(r > 170) & (g < 80) & (b < 80),
        blue=(b > 150) & (r < 80) & (g < 80),
    )


def verify(nnn, png_path, tol=2.0):
    """Ink-edge match of the rendered PNG vs original-measured placement.

    All numbers are frame px (the PNG is 300dpi -> frame px = canvas px * 72/300,
    offset by the canvas origin). Returns (ok, report dict).
    """
    cfg = CFG[nnn]
    arr = np.asarray(Image.open(png_path).convert("RGB")).astype(int)
    scale = arr.shape[1] * 72.0 / 300.0          # canvas size in frame px
    ox, oy = cfg["region"][0] - cfg["pad"], cfg["region"][1] - cfg["pad"]
    to_frame = lambda xs, ys: (xs * 72.0 / 300.0 + ox, ys * 72.0 / 300.0 + oy)

    M = _masks(nnn, arr)
    report, checks = {}, []

    def add(name, delta, ok):
        checks.append(ok)
        report[name] = {"delta": [round(d, 2) for d in delta], "ok": bool(ok)}

    def bbox(mask, box=None):
        ys, xs = np.nonzero(mask)
        if box is not None:
            bx0, by0, bx1, by1 = [v * 300.0 / 72.0 for v in
                                  (box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy)]
            keep = (xs >= bx0 - 1) & (xs <= bx1 + 1) & (ys >= by0 - 1) & (ys <= by1 + 1)
            xs, ys = xs[keep], ys[keep]
        if not len(xs):
            return None
        return to_frame(xs.min(), ys.min()) + to_frame(xs.max(), ys.max())

    for key, Mdeg in zip(BOX_ORDER, FIT_M):
        X, Y, box = box_cal(cfg, key)
        # green sine ink bbox vs expectation (sine reaches t=+-1 at data
        # x=0.25/0.75 -> clip range is inside the box for all our boxes)
        gb = bbox(M["green"], box)
        if gb is None:
            add(f"green_{key}_missing", [99], False)
        else:
            t0, st = cfg["tcal"]["T" if key in ("TL", "TR") else "B"]
            exp = (X(0), t0 - st, X(1), t0 + st)
            add(f"green_{key}", [gb[i] - exp[i] for i in range(4)],
                all(abs(gb[i] - exp[i]) <= tol for i in range(4)))
        # red fit ink bbox vs expectation
        rb = bbox(M["red"], box)
        if rb is None:
            add(f"red_{key}_missing", [99], False)
        else:
            fx = np.linspace(0, 1, 2000)
            fv = fits()[Mdeg](fx)
            bx0, by0, bx1, by1 = box
            tv_top = (cfg["tcal"]["T" if key in ("TL", "TR") else "B"][0] - by0) / \
                cfg["tcal"]["T" if key in ("TL", "TR") else "B"][1]
            tv_bot = (cfg["tcal"]["T" if key in ("TL", "TR") else "B"][0] - by1) / \
                cfg["tcal"]["T" if key in ("TL", "TR") else "B"][1]
            vv = np.clip(fv, tv_bot, tv_top)   # same clip the render applies
            exp = (X(0), Y(vv.max()), X(1), Y(vv.min()))
            # x-edge tol 3.0: the blue marker at slot 0/9 occludes the curve end
            # exactly as in the original (measured original offset +2.8px)
            etol = (3.0, tol, 3.0, tol)
            add(f"red_{key}", [rb[i] - exp[i] for i in range(4)],
                all(abs(rb[i] - exp[i]) <= etol[i] for i in range(4)))
        # blue dots: centroids vs canonical positions
        db = bbox(M["blue"], box)
        ys, xs = np.nonzero(M["blue"])
        bx0, by0, bx1, by1 = [v * 300.0 / 72.0 for v in
                              (box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy)]
        keep = (xs >= bx0) & (xs <= bx1) & (ys >= by0) & (ys <= by1)
        xs, ys = xs[keep], ys[keep]
        # cluster: one dot per data point; nearest-centroid error
        cx, cy = to_frame(0, 0)  # noqa (shadow) — compute per-slot below
        worst = 0.0
        for xv, tv in zip(XS, TS):
            px_, py_ = X(xv) - ox, Y(tv) - oy      # canvas frame-px
            ix, iy = px_ * 300.0 / 72.0, py_ * 300.0 / 72.0
            d2 = (xs - ix) ** 2 + (ys - iy) ** 2
            sel = d2 < (6 * 300 / 72.0) ** 2
            if sel.sum() < 3:
                worst = 99.0
                break
            dx = (xs[sel].mean() - ix) * 72.0 / 300.0
            dy = (ys[sel].mean() - iy) * 72.0 / 300.0
            worst = max(worst, (dx * dx + dy * dy) ** 0.5)
        add(f"dots_{key}", [worst], worst <= tol + 0.5)

    # slide-specific chrome checks
    om = ORIG_MEASURED[nnn]
    if nnn == "016":
        yb = bbox(M["yellow"])
        for key in BOX_ORDER:
            lx0, ly0, lx1, ly1 = cfg["labels"]["rects"][key]
            sel = np.nonzero(M["yellow"])
            ys, xs = sel
            fx, fy = to_frame(0, 0)
            keep = (xs * 72 / 300.0 + ox >= lx0 - 1) & (xs * 72 / 300.0 + ox <= lx1 + 1) & \
                   (ys * 72 / 300.0 + oy >= ly0 - 1) & (ys * 72 / 300.0 + oy <= ly1 + 1)
            if keep.sum() < 50:
                add(f"label_{key}_missing", [99], False)
                continue
            X0, Y0 = to_frame(xs[keep].min(), ys[keep].min())
            X1, Y1 = to_frame(xs[keep].max(), ys[keep].max())
            add(f"label_{key}",
                [X0 - lx0, Y0 - ly0, X1 - lx1, Y1 - ly1],
                all(abs(v) <= tol for v in [X0 - lx0, Y0 - ly0, X1 - lx1, Y1 - ly1]))
        # flat line y vs original-measured 252 (TL box)
        red = M["red"]
        box = cfg["boxes"]["TL"]
        ys, xs = np.nonzero(red)
        bx0, by0 = (box[0] - ox) * 300 / 72.0, (box[1] - oy) * 300 / 72.0
        bx1, by1 = (box[2] - ox) * 300 / 72.0, (box[3] - oy) * 300 / 72.0
        keep = (xs >= bx0) & (xs <= bx1) & (ys >= by0) & (ys <= by1)
        if keep.sum():
            ymid = (ys[keep].min() + ys[keep].max()) / 2.0 * 72 / 300.0 + oy
            add("flat_line_y_vs_original", [ymid - om["flat_y"]],
                abs(ymid - om["flat_y"]) <= tol)
    else:
        # flat line (TL) vs original-measured ~170
        red = M["red"]
        box = cfg["boxes"]["TL"]
        ys, xs = np.nonzero(red)
        bx0, by0 = (box[0] - ox) * 300 / 72.0, (box[1] - oy) * 300 / 72.0
        bx1, by1 = (box[2] - ox) * 300 / 72.0, (box[3] - oy) * 300 / 72.0
        keep = (xs >= bx0) & (xs <= bx1) & (ys >= by0) & (ys <= by1)
        if keep.sum():
            ymid = (ys[keep].min() + ys[keep].max()) / 2.0 * 72 / 300.0 + oy
            add("flat_line_y_vs_original", [ymid - om["flat_y"]],
                abs(ymid - om["flat_y"]) <= tol)

    ok = all(checks)
    return ok, {"png": png_path, "ok": ok, "checks": report}


if __name__ == "__main__":
    nnn = sys.argv[1]
    outdir = f"videos/ml-intro/recreated_pptx/qa/slide{nnn}/graphgen"
    args = [a for a in sys.argv[2:]]
    if args and args[0] == "--verify":
        ok, rep = verify(nnn, args[1])
        print(json.dumps(rep, indent=1))
        sys.exit(0 if ok else 1)
    # default: render next version (never overwrite banked evidence)
    k = 1
    while os.path.exists(os.path.join(outdir, f"graph_v{k}.png")):
        k += 1
    out = os.path.join(outdir, f"graph_v{k}.png")
    render(nnn, out)
    ok, rep = verify(nnn, out)
    rep["file"] = out
    print(json.dumps(rep, indent=1))
    sys.exit(0 if ok else 1)
