#!/usr/bin/env python3
"""Regenerate equation PNGs from .png.json sidecars and fix sidecar dims to match."""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD = 6
GAP = 4


def render_row(latex, fontsize, color):
    fig = plt.figure(figsize=(20, 2), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="center", va="center")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rs = np.where(ink.any(axis=1))[0]
    cs = np.where(ink.any(axis=0))[0]
    plt.close(fig)
    if len(rs) == 0:
        return np.zeros((1, 1, 4), dtype=np.uint8)
    y0, y1 = max(rs[0] - PAD, 0), min(rs[-1] + PAD, buf.shape[0])
    x0, x1 = max(cs[0] - PAD, 0), min(cs[-1] + PAD, buf.shape[1])
    return buf[y0:y1, x0:x1]


def main():
    base = sys.argv[1]
    for f in sorted(os.listdir(base)):
        if not f.endswith(".png.json"):
            continue
        p = os.path.join(base, f)
        m = json.load(open(p))
        rows = m["rows"]
        pt = m["fontsize_pt"][0] if isinstance(m["fontsize_pt"], list) else m["fontsize_pt"]
        imgs = [render_row(r.split(":", 1)[1], pt, r.split(":", 1)[0]) for r in rows]
        w = max(i.shape[1] for i in imgs)
        h = sum(i.shape[0] for i in imgs) + GAP * (len(imgs) - 1)
        canvas = np.zeros((h, w, 4), dtype=np.uint8)
        y = 0
        for i in imgs:
            canvas[y:y + i.shape[0], :i.shape[1]] = i
            y += i.shape[0] + GAP
    out = os.path.join(base, f[:-5])
    Image.fromarray(canvas).save(out)
    m["w_px"], m["h_px"] = w, h
    m["w_in"], m["h_in"] = round(w / DPI, 5), round(h / DPI, 5)
    json.dump(m, open(p, "w"), indent=1)
    print(f, "->", w, h)


if __name__ == "__main__":
    main()
