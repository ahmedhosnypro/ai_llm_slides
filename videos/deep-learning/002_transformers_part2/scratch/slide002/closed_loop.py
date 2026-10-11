#!/usr/bin/env python3
"""Closed-loop: measure render_1.png title ink vs mapped targets (150dpi px)."""
from PIL import Image
import json, sys

RENDER = sys.argv[1] if len(sys.argv) > 1 else "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide002/render_1.png"
img = Image.open(RENDER).convert("RGB")
W, H = img.size
px = img.load()
print(f"render size: {W}x{H}")

def reddish(p):
    r, g, b = p
    return r > 120 and (r - g) > 50 and (r - b) > 50

PXPT = 150 / 72.0  # render px per slide pt

# targets from the frame mapping (slide pts)
targets = [
    {"name": "L1 Transformers", "x0": 246.9, "x1": 709.9, "y0": 197.8, "y1": 252.2, "cx": 478.4},
    {"name": "L2 Part II",      "x0": 409.2, "x1": 549.7, "y0": 278.4, "y1": 316.0, "cx": 479.5},
    {"name": "L3 Aug. 2020",    "x0": 436.3, "x1": 545.5, "y0": 339.1, "y1": 361.0, "cx": 490.9},
]

# measure red ink rows in safe region (avoid chrome border ~x87/1915, y94/1125)
rows = {}
for y in range(300, 900):
    xs = [x for x in range(250, 1750) if reddish(px[x, y])]
    if xs:
        rows[y] = (min(xs), max(xs))
lines = []
cur = None
for y in sorted(rows):
    if cur and y <= cur[1] + 3:
        cur[1] = y; cur[2].append(rows[y])
    else:
        if cur: lines.append(cur)
        cur = [y, y, [rows[y]]]
if cur: lines.append(cur)

ok_all = True
report = []
for i, (t, (y0, y1, segs)) in enumerate(zip(targets, lines)):
    rx0 = min(s[0] for s in segs); rx1 = max(s[1] for s in segs)
    m = {"name": t["name"],
         "meas_px": {"x0": rx0, "x1": rx1, "y0": y0, "y1": y1, "cx": (rx0 + rx1) / 2,
                     "w": rx1 - rx0 + 1, "h": y1 - y0 + 1}}
    # to slide pts
    m["meas_pt"] = {k: round(v / PXPT, 1) for k, v in m["meas_px"].items()}
    m["target_pt"] = {k: t[k] for k in ("x0", "x1", "y0", "y1", "cx")}
    deltas = {k: round(m["meas_pt"][k] - t[k], 1) for k in ("x0", "x1", "y0", "y1", "cx")}
    m["delta_pt"] = deltas
    m["delta_px150"] = {k: round(v * PXPT, 1) for k, v in deltas.items()}
    worst = max(abs(v) for v in deltas.values())
    # size check
    m["size_pt"] = {"w": round((rx1 - rx0 + 1) / PXPT, 1), "h": round((y1 - y0 + 1) / PXPT, 1)}
    m["target_size_pt"] = {"w": round(t["x1"] - t["x0"], 1), "h": round(t["y1"] - t["y0"], 1)}
    m["worst_delta_px"] = round(worst * PXPT, 1)
    m["pass_4px"] = worst * PXPT <= 4.0
    if not m["pass_4px"]:
        ok_all = False
    report.append(m)

print(json.dumps(report, indent=1))
print("CLOSED-LOOP:", "PASS (all lines within 4px)" if ok_all else "FAIL — adjust build")
