#!/usr/bin/env python3
"""Slide 030 fixups: shared size for the six (t+delta)) cells; d2_s10 target fix;
minus bar rows for rect shapes. Updates eq_030_manifest.json in place."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import importlib.util
spec = importlib.util.spec_from_file_location("gen", "videos/deep-learning/002_transformers_part2/scratch/slide030/build/gen_eqs.py")
# reuse render() without re-running the module body: copy the function instead
DPI = 600
PAD = 8
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets"

def render(latex, color, fontsize, out):
    fig = plt.figure(figsize=(20, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    eq = fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
                  ha="center", va="baseline")
    probe = fig.text(0.15, 0.5, "x", fontsize=fontsize, color=color,
                     ha="center", va="baseline")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pb = probe.get_window_extent(renderer=renderer)
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    px0, px1 = max(int(pb.x0) - 2, 0), int(pb.x1) + 2
    baseline_row = int(np.where(ink[:, px0:px1].any(axis=1))[0][-1])
    ink[:, :px1 + 20] = False
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, buf.shape[0])
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    plt.close(fig)
    return {"w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "baseline_frac": round(float(baseline_row - y0) / float(y1 - y0), 5)}

with open(f"{ASSETS}/eq_030_manifest.json") as f:
    manifest = json.load(f)

# 1) shared size for the six (t+delta)) cells: fit inner "(t+delta)" to 38px
info = render(r"(t{+}\delta)", "#000000", 15.0, f"{ASSETS}/_probe_td.png")
fs = 15.0 * (38 / 0.96123 * DPI / 72.0) / info["w_px"]
print(f"inner (t+delta) at 38px -> fs {fs:.2f}")
for name in ["vb2_r1b", "vb2_r2b", "d1_s2", "d2_s2", "m_lb", "m_l2b"]:
    m = manifest[name]
    info = render(m["latex"], m["color"], fs, f"{ASSETS}/{name}.png")
    m.update(info, fontsize_pt=round(fs, 2))
    print(f"  {name}: w={info['w_px']} h={info['h_px']} bf={info['baseline_frac']}")

# 2) d2_s10: target 65 (marker edge excluded), ink_left 585
m = manifest["d2_s10"]
target = 65 / 0.96123 * DPI / 72.0
fs2 = m["fontsize_pt"] * target / (m["w_px"])
for _ in range(4):
    info = render(m["latex"], m["color"], fs2, f"{ASSETS}/d2_s10.png")
    err = target - info["w_px"]
    if abs(err) <= max(2.0, target * 0.012):
        break
    fs2 = fs2 * target / info["w_px"]
info = render(m["latex"], m["color"], fs2, f"{ASSETS}/d2_s10.png")
m.update(info, fontsize_pt=round(fs2, 2), target_w_px=65, ink_left_frame=585)
print(f"  d2_s10: fs={fs2:.2f} w={info['w_px']} h={info['h_px']}")

# 3) minus bar exact rows (frame): deriv L2 minus x508..511, matrix minus x288..291
im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
lum = im.mean(axis=2)
for label, (x0, x1) in [("derivL2 minus", (507, 513)), ("matrix minus", (287, 293))]:
    ys = np.where((lum[290:320, x0:x1] < 140).sum(axis=1) > 0)[0]
    print(f"{label}: rows {ys.min()+290}..{ys.max()+290}" if len(ys) else f"{label}: none in 290..320")
for label, (x0, x1) in [("matrix minus", (287, 293))]:
    ys = np.where((lum[395:425, x0:x1] < 140).sum(axis=1) > 0)[0]
    print(f"{label} (395..425): rows {ys.min()+395}..{ys.max()+395}" if len(ys) else f"{label}: none")

with open(f"{ASSETS}/eq_030_manifest.json", "w") as f:
    json.dump(manifest, f, indent=1)
print("manifest updated")
