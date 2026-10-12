#!/usr/bin/env python3
"""Closed-loop ink check, attempt 1: render_2.png (150dpi, 2000x1125) title ink vs
original-frame mapped targets. 1px @150dpi = 0.48pt; tolerance ~4px = 1.92pt."""
from PIL import Image
import sys

RENDER = sys.argv[1] if len(sys.argv) > 1 else "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide007/render_2.png"
im = Image.open(RENDER).convert("RGB")
W, H = im.size
px = im.load()
print(f"render {W}x{H}")
S = 150 / 72.0  # slide pt -> 150dpi px

# targets from the original frame mapping (slide pts) -> 150dpi px
TARGETS = {
    "L1": dict(x0=307.8 * S, x1=627.2 * S, y0=237.7 * S, y1=274.2 * S,
               cx=467.5 * S, w=319.4 * S),
    "L2": dict(x0=216.2 * S, x1=733.3 * S, y0=292.0 * S, y1=337.9 * S,
               cx=474.7 * S, w=517.1 * S),
}

def is_red(p):  # pure C00000 render ink
    r, g, b = p
    return r > 140 and (r - g) > 80 and (r - b) > 70

BANDS = {"L1": (470, 590), "L2": (596, 730)}
results = {}
for name, (ys, ye) in BANDS.items():
    pts = [(x, y) for y in range(ys, ye) for x in range(90, W - 90) if is_red(px[x, y])]
    if not pts:
        print(f"{name}: NO INK — BLOCKER"); continue
    xs = [p[0] for p in pts]; ys_ = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys_), max(ys_)
    t = TARGETS[name]
    e = dict(x0=x0 - t["x0"], x1=x1 - t["x1"], y0=y0 - t["y0"], y1=y1 - t["y1"],
             cx=(x0 + x1) / 2 - t["cx"], w=(x1 - x0) - t["w"])
    results[name] = e
    print(f"{name}: render ink x {x0}..{x1} (w {x1-x0}) y {y0}..{y1} (h {y1-y0})")
    print(f"    target   x {t['x0']:.1f}..{t['x1']:.1f} (w {t['w']:.1f}) y {t['y0']:.1f}..{t['y1']:.1f}")
    print(f"    err px  " + "  ".join(f"{k}={v:+.1f}" for k, v in e.items()))

ok = all(r and all(abs(v) <= 4.0 for v in r.values()) for r in results.values()) and len(results) == 2
# color sample: mode of title ink
import collections
c = collections.Counter(px[x, y] for y in range(470, 730) for x in range(90, W - 90) if is_red(px[x, y]))
print("render title ink mode:", c.most_common(3))
print("CLOSED-LOOP:", "PASS" if ok else "FAIL (iterate placement)")
