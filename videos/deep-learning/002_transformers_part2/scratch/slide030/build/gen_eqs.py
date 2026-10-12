#!/usr/bin/env python3
"""Slide 030: generate all mathtext equation PNGs (600dpi, transparent, width-fitted)
+ the underbrace raster. Certified mechanism per references/equations.md and the
certified slide-031 pattern (fit ink width to the original's measured ink extent;
placement recorded as ink-left + baseline in FRAME px; build maps frame->slide).
Colors HASHED per the 2026-10-12 equation color law ('#C00000', '#000080', '#000000').
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

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
    noProbe = ink.copy()
    noProbe[:, px0:px1 + 1] = False
    left = np.where(noProbe.any(axis=0))[0]
    if left.size and left[0] <= px1 + 20:
        raise SystemExit(f"probe overlap for {latex!r}")
    baseline_row = int(np.where(ink[:, px0:px1].any(axis=1))[0][-1])
    ink[:, :px1 + 20] = False
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, buf.shape[0])
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    h = y1 - y0
    w = x1 - x0
    plt.close(fig)
    return {"w_px": int(w), "h_px": int(h),
            "baseline_frac": round(float(baseline_row - y0) / float(h), 5)}

def fit(latex, color, target_w, name, fs=12.0):
    target_canvas = target_w * DPI / 72.0
    out = f"{ASSETS}/{name}.png"
    for _ in range(6):
        info = render(latex, color, fs, out)
        err = target_canvas - info["w_px"]
        if abs(err) <= max(2.0, target_canvas * 0.012):
            break
        fs = fs * target_canvas / info["w_px"]
    info = render(latex, color, fs, out)
    info.update({"name": name, "latex": latex, "color": color,
                 "fontsize_pt": round(fs, 2), "target_w_px": target_w})
    print(f"  {name:10s} fs={fs:5.2f} ink={info['w_px']}px h={info['h_px']}px bf={info['baseline_frac']}")
    return info

# frame-px targets from scratch/slide030/build probes (measure_final/probe2-7/precheck)
SEGMENTS = [
    # vecbox vector 1 (red cells)
    ("vb1_r1",  r"\mathrm{sin}(\omega t)",  "#C00000", 55, 261, 83),
    ("vb1_r2",  r"\mathrm{cos}(\omega t)",  "#C00000", 57, 261, 129),
    # vecbox vector 2 (black cells, (t+delta) yellow-highlighted)
    ("vb2_r1a", r"\mathrm{Sin}\;(\omega",   "#000000", 58, 245, 170),
    ("vb2_r1b", r"(t{+}\delta))",           "#000000", 55, 303, 170),
    ("vb2_r2a", r"\mathrm{cos}(\omega",     "#000000", 51, 250, 210),
    ("vb2_r2b", r"(t{+}\delta))",           "#000000", 45, 301, 210),
    # derivation line 1 (baseline 263)
    ("d1_s1",  r"\mathrm{sin}(\omega",                 "#000000", 44, 103, 263),
    ("d1_s2",  r"(t{+}\delta))",                       "#000000", 46, 147, 263),
    ("d1_s3",  r"=",                                   "#000000", 10, 200, 263),
    ("d1_s4",  r"\mathrm{sin}(\omega t\;+\omega\delta)", "#000000", 98, 217, 263),
    ("d1_s5",  r"=",                                   "#000000", 9, 350, 263),
    ("d1_s6",  r"\mathrm{sin}(\omega t)",              "#C00000", 55, 366, 263),
    ("d1_s7",  r"\mathrm{cos}(\omega\delta)",          "#000080", 66, 429, 263),
    ("d1_s8",  r"+",                                   "#000000", 8, 503, 263),
    ("d1_s9",  r"\mathrm{cos}(\omega t)",              "#C00000", 61, 519, 263),
    ("d1_s10", r"\mathrm{sin}(\omega\delta)",          "#000080", 61, 587, 263),
    # derivation line 2 (baseline 308)
    ("d2_s1",  r"\mathrm{cos}(\omega",                 "#000000", 50, 104, 308),
    ("d2_s2",  r"(t{+}\delta))",                       "#000000", 46, 154, 308),
    ("d2_s3",  r"=",                                   "#000000", 9, 207, 308),
    ("d2_s4",  r"\mathrm{cos}(\omega t\;+\omega\delta)", "#000000", 104, 223, 308),
    ("d2_s5",  r"=",                                   "#000000", 9, 350, 308),
    ("d2_s6",  r"\mathrm{cos}(\omega t)",              "#C00000", 61, 366, 308),
    ("d2_s7",  r"\mathrm{cos}(\omega\delta)",          "#000080", 66, 434, 308),
    ("d2_s8",  r"-",                                   "#000000", 4, 508, 308),
    ("d2_s9",  r"\mathrm{sin}(\omega t)",              "#C00000", 55, 520, 308),
    ("d2_s10", r"\mathrm{sin}(\omega\delta)",          "#000080", 68, 582, 308),
    # matrix box left vector (black)
    ("m_la",   r"\mathrm{Sin}\;(\omega",   "#000000", 52, 128, 372),
    ("m_lb",   r"(t{+}\delta))",           "#000000", 46, 180, 372),
    ("m_l2a",  r"\mathrm{cos}(\omega",     "#000000", 51, 127, 411),
    ("m_l2b",  r"(t{+}\delta))",           "#000000", 45, 178, 411),
    # bold equals + row-2 minus (single glyphs; ink-top anchored in build)
    ("m_eq",    r"=", "#000000", 10, 255, 0),
    ("m_minus", r"-", "#000000", 4, 288, 0),
    # 2x2 matrix cells (navy)
    ("m_r1c1", r"\mathrm{cos}(\omega\delta)", "#000080", 68, 303, 371),
    ("m_r1c2", r"\mathrm{sin}(\omega\delta)", "#000080", 61, 388, 371),
    ("m_r2c1", r"\mathrm{sin}(\omega\delta)", "#000080", 62, 305, 418),
    ("m_r2c2", r"\mathrm{cos}(\omega\delta)", "#000080", 66, 384, 418),
    # right vector (red cells)
    ("m_ra",   r"\mathrm{sin}(\omega t)", "#C00000", 55, 504, 378),
    ("m_rb",   r"\mathrm{cos}(\omega t)", "#C00000", 60, 504, 423),
    # remember identities (italic navy)
    ("rm_id1", r"\mathit{sin}(a{+}b)=\mathit{sin}\,(a)\,\mathit{cos}(b)\;+\;\mathit{cos}(a)\,\mathit{sin}(b)", "#000080", 261, 513, 159),
    ("rm_id2", r"\mathit{cos}(a{+}b)=\mathit{cos}(a)\,\mathit{cos}(b)-\mathit{sin}(a)\,\mathit{sin}(b)", "#000080", 266, 512, 176),
]

manifest = {}
print("== rendering equation segments ==")
for name, latex, color, tw, ink_left, baseline in SEGMENTS:
    info = fit(latex, color, tw / 0.96123, name)
    info.update({"ink_left_frame": ink_left, "baseline_frame": baseline,
                 "anchor": "baseline"})
    manifest[name] = info

# ink-top anchored single glyphs (=, -)
manifest["m_eq"]["ink_top_frame"] = 390
manifest["m_eq"]["anchor"] = "inktop"
manifest["m_minus"]["ink_top_frame"] = 408
manifest["m_minus"]["anchor"] = "inktop"

# ---- underbrace raster (certified slide-020 mechanism: PIL draw, 600dpi) --------
# frame anatomy: x272..469 y447..467; spine rows 456..458; arms curl UP to 447;
# central cusp DOWN to 467, apex ~x371 (frame). C00000.
W_PT = 198 / 0.96123   # 206.03 slide pt
H_PT = 21 / 0.95556    # 21.98 slide pt
W = round(W_PT / 72 * DPI)
H = round(H_PT / 72 * DPI)
S = DPI / 72.0

def fx2pt(fx): return (fx - 272) * (W_PT / 198.0)
def fy2pt(fy): return (fy - 447) * (H_PT / 21.0)

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
RED = (192, 0, 0, 255)
SW = max(2, round(2.2 * S))
y_sp = fy2pt(457.2) * S
x_a, x_b = fx2pt(273.6) * S, fx2pt(362) * S   # spine left part (cusp gap 363..379)
x_c, x_d = fx2pt(380) * S, fx2pt(467.4) * S   # spine right part
d.line([(x_a, y_sp), (x_b, y_sp)], fill=RED, width=SW)
d.line([(x_c, y_sp), (x_d, y_sp)], fill=RED, width=SW)
# arms as curled polylines (measured: arm ink cols 273-275 / 468-469, rows 447..456)
def fpts(pairs):
    return [(fx2pt(a) * S, fy2pt(b) * S) for a, b in pairs]
d.line(fpts([(283, 457.2), (276.5, 455.2), (273.6, 451.5), (273.4, 447)]), fill=RED, width=SW, joint="curve")
d.line(fpts([(458, 457.2), (464.5, 455.2), (467.4, 451.5), (467.6, 447)]), fill=RED, width=SW, joint="curve")
cx_apex = fx2pt(371) * S
y_apex = fy2pt(467) * S
d.line([(x_b, y_sp), (cx_apex, y_apex)], fill=RED, width=SW)
d.line([(cx_apex, y_apex), (x_c, y_sp)], fill=RED, width=SW)
img.save(f"{ASSETS}/brace_030.png")
print(f"brace_030.png {img.size}")
manifest["brace"] = {"name": "brace", "file": "brace_030", "w_px": W, "h_px": H,
                     "ink_left_frame": 272, "ink_top_frame": 447, "anchor": "inktop"}

out_json = f"{ASSETS}/eq_030_manifest.json"
with open(out_json, "w") as f:
    json.dump(manifest, f, indent=1)
print("manifest ->", out_json)
