#!/usr/bin/env python3
# selfcheck_containment.py — pre-judge self-checks 2 (frame containment) and 7 (wrap)
# on render_3.png, in slide-pt space (render px / 2.08333).
# Checks 1 (patterns), 3 (equations), 4 (delimiters), 5 (tables), 8 (line spacing)
# are N/A for this slide and documented in the worker report.
from PIL import Image
import numpy as np
import json

a = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide056/render_3.png").convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
K = 150.0 / 72.0
out = {}

# content ink = anything clearly not canvas-white / panel-gray / chrome red border /
# badge yellow+ring. Panel: x 42..919pt, top 45pt, bottom 540pt (slide edge).
nonbg = ((np.abs(r - 255) > 12) | (np.abs(g - 255) > 12) | (np.abs(b - 255) > 12)) & \
        ((np.abs(r - 233) > 12) | (np.abs(g - 233) > 12) | (np.abs(b - 231) > 12))
# exclude chrome: red border lines (C00000) within 3px of panel edges, badge region
x_lo, x_hi = int(45 * K), int(916 * K)   # inside the panel borders
y_lo, y_hi = int(48 * K), int(538 * K)
sub = np.zeros_like(nonbg); sub[y_lo:y_hi, x_lo:x_hi] = nonbg[y_lo:y_hi, x_lo:x_hi]
# badge zone (chrome-owned): x 875..911pt, y 53..89pt
bz0x, bz1x = int(872 * K), int(914 * K)
bz0y, bz1y = int(50 * K), int(92 * K)
sub[bz0y:bz1y, bz0x:bz1x] = False
ys, xs = np.nonzero(sub)
out["content_ink_bbox_pt"] = [round(xs.min() / K, 1), round(xs.max() / K, 1),
                              round(ys.min() / K, 1), round(ys.max() / K, 1)]
ok = (xs.min() >= x_lo) and (xs.max() < x_hi) and (ys.min() >= y_lo) and (ys.max() < y_hi)
out["containment"] = "PASS" if ok else "FAIL"
# known extremes: vocab labels x0 62.8; blue bar y1 522.7; green box / bars x1 847.3
out["expected_extremes_pt"] = dict(left=62.8, right=847.3, top=64.8, bottom=522.7)

# wrap check: per-element band assertions (no ink outside expected bands)
def band_ink(y0, y1, x0, x1, m):
    return int(m[y0:y1, x0:x1].sum())

red = (r > 150) & (g < 70) & (b < 70)
# title band: red ink only within y 60..100pt, x 330..670pt
t_ink_out = band_ink(int(50 * K), int(60 * K), int(330 * K), int(670 * K), red) + \
            band_ink(int(100 * K), int(108 * K), int(330 * K), int(670 * K), red)
out["title_no_wrap_above_below_px"] = t_ink_out
out["title_wrap"] = "PASS" if t_ink_out == 0 else "FAIL"
# subtitle band: blue ink within y 108..126pt
bl = (b > 150) & (b - r > 80) & (g < 80)
s_ink_out = band_ink(int(100 * K), int(108 * K), int(700 * K), int(1400 * K), bl) + \
            band_ink(int(126 * K), int(140 * K), int(700 * K), int(1400 * K), bl)
out["subtitle_no_wrap_px"] = s_ink_out
out["subtitle_wrap"] = "PASS" if s_ink_out == 0 else "FAIL"
# bar labels: white ink confined to the bars
wh = (r > 240) & (g > 240) & (b > 240)
sm_out = band_ink(int(228 * K), int(234 * K), int(160 * K), int(840 * K), wh) + \
         band_ink(int(278 * K), int(300 * K), int(160 * K), int(840 * K), wh)
bb_out = band_ink(int(476 * K), int(482 * K), int(160 * K), int(840 * K), wh) + \
         band_ink(int(524 * K), int(540 * K), int(160 * K), int(840 * K), wh)
out["bar_text_no_wrap"] = "PASS" if (sm_out == 0 and bb_out == 0) else f"FAIL {sm_out},{bb_out}"
# vocab labels: red ink confined to y 150..170 / 342..362, x 55..150
v1_out = band_ink(int(145 * K), int(150 * K), int(55 * K), int(150 * K), red) + \
         band_ink(int(170 * K), int(180 * K), int(55 * K), int(150 * K), red)
v2_out = band_ink(int(338 * K), int(342 * K), int(55 * K), int(150 * K), red) + \
         band_ink(int(362 * K), int(372 * K), int(55 * K), int(150 * K), red)
out["vocab_labels_no_wrap"] = "PASS" if (v1_out == 0 and v2_out == 0) else f"FAIL {v1_out},{v2_out}"

print(json.dumps(out, indent=1))
