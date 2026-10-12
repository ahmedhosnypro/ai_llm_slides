#!/usr/bin/env python3
"""Compose the slide-031 theta matrix PNG at 600dpi:
- 9 mathtext-rendered theta_i glyphs (STIX serif italic, fs 36, black) at measured
  column centers / row tops (professional 2D format: true stacked subscripts).
- Bracket strokes drawn to the ORIGINAL's measured geometry (stroke 4pt wide,
  span 99pt, ticks 2pt x ~11.5pt inward at top/bottom).
Final ink = exactly 200 x 99 pt (bracket-left 634 .. bracket-right 833,
bracket-top 396 .. bracket-bottom 494 in frame px). 1 frame px = 1 pt.
"""
import json, os, importlib.util
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "stix"
import numpy as np
from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SCRATCH = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide031"
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
DPI = 600
PT = DPI / 72.0  # px per pt at 600dpi

# ---- measured layout (frame px = pt, origin at bracket ink top-left 634,396)
W_PT, H_PT = 200.0, 99.0
COLS = [28.5, 100.0, 171.0]          # entry ink-center x (662.5/734/805 minus 634)
ROW_TOPS = [5.0, 37.0, 70.0]         # entry ink-top y (401/433/466 minus 396)
BR_W = 4.0                            # stroke width pt
TICK_L = 11.5                         # tick inward length pt
TICK_T = 2.0                          # tick thickness pt

FS = 30.0

# ---- 1. render the 9 glyphs
glyphs = {}
for i in range(1, 10):
    out = os.path.join(SCRATCH, f"th_{i}.png")
    info = mod.render(rf"\theta_{i}", out, FS, "000000")
    im = Image.open(out)
    al = np.asarray(im)[:, :, 3]
    ys, xs = np.where(al > 8)
    glyphs[i] = {"img": im, "info": info, "bbox": (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))}
    print(f"theta_{i}: ink {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}px  sidecar w_in {info['w_in']} h_in {info['h_in']}")

# ---- 2. compose
W = int(round(W_PT * PT))   # 1667
H = int(round(H_PT * PT))   # 825
canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

# brackets (left: stroke x 0..BR_W, y 0..H; ticks at top/bottom extending right)
d = ImageDraw.Draw(canvas)
BLACK = (0, 0, 0, 255)
def px(v): return int(round(v * PT))
# left bracket
d.rectangle([0, 0, px(BR_W), H - 1], fill=BLACK)                     # stroke
d.rectangle([0, 0, px(TICK_L), px(TICK_T)], fill=BLACK)              # top tick
d.rectangle([0, H - px(TICK_T), px(TICK_L), H - 1], fill=BLACK)      # bottom tick
# right bracket (stroke x W-BR_W..W; ticks extending left)
d.rectangle([W - px(BR_W), 0, W - 1, H - 1], fill=BLACK)
d.rectangle([W - px(TICK_L), 0, W - 1, px(TICK_T)], fill=BLACK)
d.rectangle([W - px(TICK_L), H - px(TICK_T), W - 1, H - 1], fill=BLACK)

# entries — anchored by MATH BASELINE (equation alignment law):
# original baselines (frame px): 418.15 / 450.65 / 483.15 (theta top + theta height, pitch 32.5)
BASELINES = [25.2, 57.7, 90.2]      # rel bracket top (396): theta tops land on measured 401/433.5/466
k = 1
for row, bl in enumerate(BASELINES):
    for col, cx in enumerate(COLS):
        g = glyphs[k]
        x0, y0, x1, y1 = g["bbox"]
        gw, gh = x1 - x0 + 1, y1 - y0 + 1
        base_px = g["info"]["baseline_px"] - y0   # baseline row within ink crop
        gx = int(round(cx * PT - gw / 2))
        gy = int(round(bl * PT - base_px))
        crop = g["img"].crop((x0, y0, x1 + 1, y1 + 1))
        canvas.alpha_composite(crop, (gx, gy))
        print(f"theta_{k} baseline {bl} -> px ({gx},{gy}) size {gw}x{gh} ink_bottom {gy+gh}px ({(gy+gh)/PT:.1f}pt)")
        k += 1

out_path = os.path.join(ASSETS, "eq_031_matrix.png")
canvas.save(out_path)
# ink bbox check
al = np.asarray(canvas)[:, :, 3]
ys, xs = np.where(al > 8)
print(f"final ink: {xs.min()}..{xs.max()} x {ys.min()}..{ys.max()} of {W}x{H} -> "
      f"{(xs.max()-xs.min()+1)/PT:.1f} x {(ys.max()-ys.min()+1)/PT:.1f} pt (target 200x99)")

sidecar = {
    "image": "build/assets/eq_031_matrix.png",
    "w_px": W, "h_px": H, "w_in": round(W / DPI, 5), "h_in": round(H / DPI, 5),
    "ink_offset_px": [int(xs.min()), int(ys.min())],
    "dpi": DPI, "font_size_pt": FS, "color": "000000",
    "mathtext": "composed: theta_1..theta_9 (STIX) + measured bracket strokes",
    "frame_target_pt": {"x": 634, "y": 396, "w": 200, "h": 99},
}
json.dump(sidecar, open(os.path.join(ASSETS, "eq_031_matrix.json"), "w"), indent=1)
print("wrote", out_path, "and sidecar")
