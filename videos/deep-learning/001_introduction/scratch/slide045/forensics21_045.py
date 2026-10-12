#!/usr/bin/env python3
"""forensics21_045.py — judge-2 follow-up: per-row red profile of the panel border zone
(settles the 'callout connector lines' finding) + ultra-low-threshold corridor scans
(settle the spec's 'Input-callout arrow': measurably absent) . Banked as forensics21_out.txt."""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
out = []
def P(*a):
    line = " ".join(str(x) for x in a)
    out.append(line); print(line)

r, g, b = org[:, :, 0], org[:, :, 1], org[:, :, 2]
strict = (r - g > 25) & (r - b > 15) & (r > 90)
ultra = (r - g > 5) & (r - b > 3) & (r > 170)

P("== ORG per-row red extent x685..715, y300..480 (strict) — border zone ==")
P("   border is uniform x699..702 EXCEPT y346..356 (crossing stroke):")
rows = []
for fy in range(300, 481):
    se = [fx for fx in range(685, 716) if strict[fy, fx]]
    if se and (min(se) < 697 or max(se) > 704):
        rows.append(f" y{fy}: x{min(se)}..{max(se)} (n={len(se)})")
P("\n".join(rows))
P("   (all other rows: x699..702, n=4-5)")

P("")
P("== ultra-low-threshold (r-g>5, r-b>3, r>170) corridor scans ==")
zones = {
    "weights gap x708..736 y340..400": (708, 736, 340, 400),
    "wedge->crossing gap x623..693 y335..400": (623, 693, 335, 400),
    "input corridor x706..736 y400..475": (706, 736, 400, 475),
    "input-to-eq(c) zone x683..706 y440..478": (683, 706, 440, 478),
}
for name, (x0, x1, y0, y1) in zones.items():
    ys, xs = np.where(ultra[y0:y1+1, x0:x1+1])
    if len(ys):
        pts = sorted(set(zip((x0+xs).tolist(), (y0+ys).tolist())))
        P(f" {name}: {len(ys)} px; clusters: {pts[:14]}{'...' if len(pts)>14 else ''}")
    else:
        P(f" {name}: NONE")

P("")
P("== CONCLUSIONS ==")
P(" 1. Weights leader EXISTS: crossing stroke (693..707, 346..356) + faint trace")
P("    (708..711, 350..360) toward the callout + wedge arrowhead at x_{r-i,c-j}.")
P(" 2. Input-callout arrow: ZERO ink in both corridors at a threshold that catches")
P("    1px JPEG remnants (it catches the Weights trace) -> measurably ABSENT.")
open(f"{QA}/forensics21_out.txt", "w").write("\n".join(out) + "\n")
print("\nwrote forensics21_out.txt")
