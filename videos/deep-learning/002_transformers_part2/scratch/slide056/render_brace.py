#!/usr/bin/env python3
# render_brace.py — slide 056 red curly brace as a transparent 600dpi PNG.
#
# WHY AN IMAGE: the original brace (PIL row profile, debug4.py) is a horizontal
# curly brace with (i) a WIDE LOW center bump (~40pt wide, ~7.8pt high above the
# arm), (ii) thin horizontal arms (~2.6pt stroke) spanning ~637pt, and (iii) short
# end curls hooking DOWN-OUTWARD (~9pt below the arm). The pptxgenjs leftBrace
# preset (rotate 90) renders a narrow spike bump + straight spine + long end
# strokes — reads as a squared bracket (crop-comparison FAIL, 2026-10-11). The
# preset geometry cannot reproduce the measured curvature, so the brace is
# generated here (same 600dpi transparent-PNG mechanism as the certified equation
# pipeline) and embedded at EXACT size in slide_056.js. Never rescale.
#
# MEASURED TARGETS (slide pt; frame->slide mapping of slide_056.jpg):
#   brace ink bbox x 182.4..819.7 (len 637.3), y 126.5..143.2 (thickness 16.7)
#   arm centerline ~8.5pt from bbox top; apex top = bbox top; tips hook down to
#   the bbox bottom, curling slightly outward; stroke ~2.5pt; color CC0000.
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LEN, THICK = 637.3, 16.7          # pt
ARM_Y = 8.5                       # arm centerline from top
APEX_Y = 1.25                     # apex centerline (stroke top = 0)
TIP_Y = 15.2                      # tip end centerline
STROKE = 2.5
COLOR = "#CC0000"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/slide056_brace.png"

cx = LEN / 2.0
bw = 18.5                          # bump half-width (total ~37pt)

def bez(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * np.array(p0) + 3 * (1 - t) ** 2 * t * np.array(p1)
            + 3 * (1 - t) * t ** 2 * np.array(p2) + t ** 3 * np.array(p3))

segs = []
# left tip curl: from tip end (pointing down, slightly outward) up into the arm
segs.append(bez((1.0, TIP_Y), (1.0, ARM_Y + 3.2), (3.2, ARM_Y), (8.0, ARM_Y)))
# left arm
segs.append(np.array([[8.0, ARM_Y], [cx - bw, ARM_Y]]))
# center bump (wide, low): two symmetric cubics through the apex
segs.append(bez((cx - bw, ARM_Y), (cx - bw + 7.5, ARM_Y), (cx - 10.0, APEX_Y), (cx, APEX_Y)))
segs.append(bez((cx, APEX_Y), (cx + 10.0, APEX_Y), (cx + bw - 7.5, ARM_Y), (cx + bw, ARM_Y)))
# right arm
segs.append(np.array([[cx + bw, ARM_Y], [LEN - 8.0, ARM_Y]]))
# right tip curl
segs.append(bez((LEN - 8.0, ARM_Y), (LEN - 3.2, ARM_Y), (LEN - 1.0, ARM_Y + 3.2), (LEN - 1.0, TIP_Y)))

fig = plt.figure(figsize=(LEN / 72.0, THICK / 72.0), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, LEN); ax.set_ylim(THICK, 0)  # y inverted: 0 = bbox top
ax.axis("off")
for sg in segs:
    ax.plot(sg[:, 0], sg[:, 1], color=COLOR, linewidth=STROKE,
            solid_capstyle="round", solid_joinstyle="round")
fig.savefig(OUT, transparent=True)
plt.close(fig)

from PIL import Image
im = Image.open(OUT)
sidecar = dict(image="slide056_brace.png", w_px=im.size[0], h_px=im.size[1],
               dpi=600, w_in=im.size[0] / 600.0, h_in=im.size[1] / 600.0,
               mathtext=None, font_size_pt=None, color=COLOR,
               note="curly-brace drawing, embed at w_in x h_in at x=182.4/72 y=126.5/72 in")
with open(OUT.replace(".png", ".json"), "w") as f:
    json.dump(sidecar, f, indent=1)
print(json.dumps(sidecar, indent=1))
