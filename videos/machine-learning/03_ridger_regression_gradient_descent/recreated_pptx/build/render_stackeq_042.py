#!/usr/bin/env python3
"""Composite equation renderer for slide 042 (Iteration 1).

Extends the certified build/render_stackeq.py segment language with a 2-D
matrix segment, which slide 042's d(x_i) equations need:

  {"segments": [{"t": "d(x_1) = "}, {"mat": [["1","1","1","4"],["-2","0"]]},
                {"t": " = 0"}],
   "fontsize": 14, "color": "000000"}

Same sidecar JSON contract as scripts/render_eq.py, so the pptxgenjs build
consumes it identically (w_in/h_in + baseline_frac).
"""
import json, sys, os, importlib.util
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

DPI = 600
PAD_PX = 8

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "stackeq", os.path.join(HERE, "render_stackeq.py"))
_stackeq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_stackeq)   # __name__ != "__main__ -> CLI skipped

render_text = None  # replaced below: the certified render_text's 6px baseline band
                   # misses the probe's ink at fontsize >= ~18 (its leftmost ink
                   # column sits further right), so use a wider band here.


def render_text(latex, fontsize, color):
    """One mathtext run -> (RGBA array, baseline_row_in_crop, w, h)."""
    fig = plt.figure(figsize=(16, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.03, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="left", va="baseline")
    probe = fig.text(0.01, 0.5, "x", fontsize=fontsize, color=color,
                     ha="left", va="baseline")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pb = probe.get_window_extent(renderer=renderer)
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    px0 = max(int(pb.x0) - 2, 0)
    band = ink[:, px0:px0 + 16]
    rows = np.where(band.any(axis=1))[0]
    if len(rows) == 0:
        raise SystemExit(f"no baseline for {latex!r} (probe band empty)")
    baseline_row = int(rows[-1])
    ink[:, :px0 + 20] = False        # drop the probe
    er = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(er) == 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(er[0] - PAD_PX, 0), min(er[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    plt.close(fig)
    crop = buf[y0:y1, x0:x1]
    return crop, baseline_row - y0, (x1 - x0), (y1 - y0)


def render_mat(grid, fontsize, color, gap_frac=0.42):
    """2-D matrix (ragged rows OK) -> (array, baselines_per_row, w, h)."""
    runs = []
    for row in grid:
        rr = []
        for e in row:
            a, bl, w, h = render_text(e, fontsize, color)
            rr.append((a, bl, w, h))
        runs.append(rr)
    cell_h = max(a[3] for r in runs for a in r)
    gap = int(round(cell_h * gap_frac))
    col_w = []
    for c in range(max(len(r) for r in runs)):
        col_w.append(max(r[c][2] for r in runs if len(r) > c))
    total_w = sum(col_w)
    nrow = len(runs)
    total_h = cell_h * nrow + gap * (nrow - 1)
    out = np.zeros((total_h, total_w, 4), dtype=np.uint8)
    baselines = []
    for ri, rr in enumerate(runs):
        y0 = ri * (cell_h + gap)
        baselines.append(y0 + rr[0][1])
        x = 0
        for ci, (a, bl, w, h) in enumerate(rr):
            xoff = x + (col_w[ci] - w) // 2
            out[y0:y0 + h, xoff:xoff + w] = a
            x += col_w[ci]
    return out, baselines, total_w, total_h


import numpy as np


def main():
    spec = json.loads(sys.argv[1])
    out_path = sys.argv[2]
    fs = spec.get("fontsize", 14)
    color = "#" + spec.get("color", "000000").lstrip("#")
    segs = spec["segments"]

    rendered = []
    for seg in segs:
        if "t" in seg:
            a, bl, w, h = render_text(seg["t"], fs, color)
            rendered.append({"kind": "text", "arr": a, "baselines": [bl],
                             "w": w, "h": h, "anchor": bl})
        elif "col" in seg:
            a, bls, w, h = _stackeq.render_entries(seg["col"], fs * 0.92, color)
            mid = bls[len(bls) // 2]
            rendered.append({"kind": "mat", "arr": a, "baselines": bls,
                             "w": w, "h": h, "anchor": mid})
        elif "mat" in seg:
            a, bls, w, h = render_mat(seg["mat"], fs * 0.92, color)
            anchor = bls[len(bls) // 2]      # centre the matrix on the axis
            rendered.append({"kind": "mat", "arr": a, "baselines": bls,
                             "w": w, "h": h, "anchor": anchor})
        else:
            raise SystemExit(f"bad segment {seg}")

    base_bl = max(r["anchor"] for r in rendered)
    line_y = PAD_PX + base_bl
    H = line_y + max(r["h"] - r["anchor"] for r in rendered) + PAD_PX

    ops = []
    x = 0
    for r in rendered:
        if r["kind"] == "text":
            ops.append(("text", x, r))
            x += r["w"]
        else:
            bw = max(int(round(fs * 0.62)), 5)      # stroke thickness
            serif = max(int(round(fs * 0.55)), 5)   # horizontal hook run
            bx_l = x
            bx_r = x + bw + 2 + r["w"] + 2
            ops.append(("mat", bx_l, bx_r, bw, serif, r))
            x = bx_r + bw
    total_w = x + 2 * PAD_PX

    canvas = np.zeros((H, total_w, 4), dtype=np.uint8)

    def paste(arr, x0, y0):
        h, w = arr.shape[:2]
        if y0 < 0 or y0 + h > H:
            raise SystemExit(f"paste out of range: y0={y0} h={h} H={H}")
        canvas[y0:y0 + h, x0:x0 + w] = arr

    for op in ops:
        if op[0] == "text":
            _, px, r = op
            paste(r["arr"], px + PAD_PX, line_y - r["anchor"])
        else:
            _, bx_l, bx_r, bw, serif, r = op
            y_entries = line_y - r["anchor"]
            paste(r["arr"], bx_l + bw + 2 + PAD_PX, y_entries)
            top, bot = y_entries, y_entries + r["h"]
            lx, rx = bx_l + PAD_PX, bx_r + PAD_PX
            for sy, sx in [
                (slice(top, bot), slice(lx, lx + bw)),
                (slice(top, bot), slice(rx, rx + bw)),
                (slice(top, top + bw), slice(lx, lx + serif)),
                (slice(bot - bw, bot), slice(lx, lx + serif)),
                (slice(top, top + bw), slice(rx + bw - serif, rx + bw)),
                (slice(bot - bw, bot), slice(rx + bw - serif, rx + bw))]:
                canvas[sy, sx, 0:3] = 0
                canvas[sy, sx, 3] = 255

    alpha = canvas[:, :, 3] > 8
    rows = np.where(alpha.any(axis=1))[0]
    cols = np.where(alpha.any(axis=0))[0]
    y0, y1 = rows[0], rows[-1] + 1
    x0, x1 = cols[0], cols[-1] + 1
    canvas = canvas[y0:y1, x0:x1]

    tw = spec.get("target_w_in")
    th = spec.get("target_h_in")
    if tw or th:
        im = Image.fromarray(canvas)
        cw, ch = im.size
        if tw and th:
            nw, nh = int(round(tw * DPI)), int(round(th * DPI))
        elif tw:
            nw = int(round(tw * DPI)); nh = max(1, int(round(ch * (nw / cw))))
        else:
            nh = int(round(th * DPI)); nw = max(1, int(round(cw * (nh / ch))))
        im = im.resize((nw, nh), Image.LANCZOS)
        canvas = np.asarray(im)
        Image.fromarray(canvas).save(out_path)
        nb = int(round(line_y * nh / (y1 - y0)))
        h = canvas.shape[0]
        print(json.dumps({"path": out_path, "w_px": canvas.shape[1], "h_px": int(h),
                          "w_in": round(canvas.shape[1] / DPI, 5),
                          "h_in": round(h / DPI, 5), "baseline_px": int(nb),
                          "baseline_frac": round(nb / h, 5), "dpi": DPI,
                          "fontsize_pt": fs, "color": spec.get("color", "000000")}))
        return

    Image.fromarray(canvas).save(out_path)
    nb = line_y - y0
    h = y1 - y0
    print(json.dumps({"path": out_path, "w_px": int(x1 - x0), "h_px": int(h),
                      "w_in": round((x1 - x0) / DPI, 5), "h_in": round(h / DPI, 5),
                      "baseline_px": int(nb), "baseline_frac": round(nb / h, 5),
                      "dpi": DPI, "fontsize_pt": fs, "color": spec.get("color", "000000")}))


if __name__ == "__main__":
    main()
