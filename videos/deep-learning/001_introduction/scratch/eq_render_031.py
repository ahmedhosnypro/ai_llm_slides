"""Batch-render theta_1..theta_9 (STIX serif mathtext, fs=26, black, 600dpi) and build
the placement manifest for slide 031's 3x3 matrix. Certified mechanism: matplotlib
mathtext -> tight transparent PNG -> addImage at EXACT size, baseline-anchored.
Banked to recreated_pptx/build/assets/ (never delete)."""
import importlib.util, json, os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

spec = importlib.util.spec_from_file_location("re_base", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
FS = 26
COLOR = "#000000"

# measured targets (frame px = pt, direct 1px=1pt per certified siblings):
# theta-ink left per column; theta baseline per row. Attempt-1 closed loop: with
# baselines 418/451/484 the rendered band sat 2.7 frame px high (STIX's shallower
# subscript hang vs the original's); baselines shifted +1.3 so the BAND edges
# (theta top .. sub bottom) match the original's 401..423 within ~1.5 frame px.
COLS = [647, 718, 789]
BASELINES = [419.3, 452.3, 485.3]

entries = []
for i in range(1, 10):
    r, c = divmod(i - 1, 3)  # r,c zero-based
    png = f"{ASSETS}/eq_031_theta{i}.png"
    info = base.render(rf"\theta_{i}", png, FS, COLOR)
    with open(f"{ASSETS}/eq_031_theta{i}.json", "w") as f:
        json.dump(info, f, indent=1)
    a = np.asarray(Image.open(png).convert("RGBA")).astype(int)
    ink = a[:, :, 3] > 40
    # theta glyph = the main-height ink cluster: split columns, first cluster = theta
    colc = ink.sum(axis=0)
    runs = []; s = None
    for x, v in enumerate(colc > 0):
        if v and s is None: s = x
        if not v and s is not None: runs.append((s, x - 1)); s = None
    if s is not None: runs.append((s, len(colc) - 1))
    th_x0, th_x1 = runs[0]
    th_rows = np.where(ink[:, th_x0:th_x1 + 1].any(axis=1))[0]
    th_y0, th_y1 = th_rows[0], th_rows[-1]
    # placement: put theta-ink left at COLS[c], theta baseline at BASELINES[r]
    x_in = (COLS[c] - th_x0 / 600 * 72) / 72
    y_in = (BASELINES[r] / 72) - info["baseline_frac"] * info["h_in"]
    entries.append({
        "i": i, "mathtext": rf"\theta_{i}", "image": f"eq_031_theta{i}.png",
        "font_size_pt": FS, "color": COLOR,
        "w_in": info["w_in"], "h_in": info["h_in"],
        "baseline_frac": info["baseline_frac"], "baseline_px": info["baseline_px"],
        "theta_ink_px": [int(th_x0), int(th_y0), int(th_x1), int(th_y1)],
        "target_theta_left_pt": COLS[c], "target_baseline_pt": BASELINES[r],
        "x_in": round(x_in, 5), "y_in": round(y_in, 5),
    })
    print(f"theta_{i}: png {info['w_px']}x{info['h_px']}px  theta ink px {th_x0}..{th_x1},{th_y0}..{th_y1}"
          f"  -> x={x_in:.4f}in y={y_in:.4f}in w={info['w_in']} h={info['h_in']}")

manifest = {
    "slide": 31, "video": "deep-learning/001_introduction",
    "mechanism": "STIX serif mathtext fs=26 black 600dpi; theta-ink-left + baseline anchoring; "
                 "brackets rect-built (certified 002 slide-031 mechanism)",
    "targets": {"theta_left_cols_pt": COLS, "theta_baseline_rows_pt": BASELINES,
                "bracketL": {"x": 634, "y": 397, "w": 3.5, "h": 97.5, "tick_w": 9.5, "tick_h": 2.5},
                "bracketR": {"x": 830, "y": 397, "w": 4, "h": 97.5, "tick_w": 10, "tick_h": 2.5}},
    "equations": entries,
}
with open(f"{ASSETS}/eq_031_manifest.json", "w") as f:
    json.dump(manifest, f, indent=1)
print("manifest written")
