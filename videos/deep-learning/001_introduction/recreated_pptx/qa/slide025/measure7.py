#!/usr/bin/env python3
"""measure7.py — slide 025 pixel-map probes: top strip, arrows/callouts zone,
Net pointers, outbox/class borders, arrow rows. Banked as measure7_out.txt."""
from collections import Counter
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide025/measure7_out.txt"
im = Image.open(SRC).convert("RGB")
P = im.load()
L = []
def pr(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)

def cls(r, g, b):
    if r > 200 and 100 < g < 200 and b > 200: return "M"      # bright magenta
    if 120 <= r <= 210 and g < 110 and 120 <= b <= 210: return "m"  # dark magenta
    if r > 130 and g < 80 and b < 80: return "R"               # red
    if 100 <= r <= 190 and g < 60 and b < 60: return "r"       # dark red
    if 120 <= r <= 175 and 130 <= g <= 185 and 165 <= b <= 220: return "L"  # lav border
    if 195 <= r <= 245 and 215 <= g <= 248 and b > 238: return "l"  # lav fill
    if 95 <= r <= 155 and 140 <= g <= 195 and 60 <= b <= 125: return "G"    # green border
    if 185 <= r <= 240 and g >= 243 and 145 <= b <= 215: return "g"         # green fill
    if 120 <= r <= 200 and 95 <= g <= 165 and 175 <= b <= 235: return "V"   # violet
    if r < 130 and g < 130 and b < 130: return "K"             # dark
    if 150 <= r <= 215 and 140 <= g <= 210 and 130 <= b <= 190: return "t"  # tan-ish
    return "."

def band(x0, x1, y0, y1, step=1, tag=""):
    pr(f"-- {tag} x{x0}..{x1} step{step} y{y0}..{y1}")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1 + 1, step))
    pr(hdr)
    for y in range(y0, y1 + 1):
        row = "".join(cls(*P[x, y]) for x in range(x0, x1 + 1, step))
        pr(f"{y:4d} {row}")

# 1) top strip: IS box + dash + SL box
band(50, 180, 88, 138, 1, "IS/dash-left")
band(560, 690, 60, 140, 1, "SL zone")

# 2) arrows + callouts
band(225, 320, 360, 440, 1, "i arrow + prev callout")
band(375, 480, 360, 440, 1, "j arrow + curr callout")

# 3) Net pointer zones
band(236, 262, 155, 200, 1, "Net_i ptr zone")
band(395, 425, 170, 205, 1, "Net_j ptr zone")

# 4) arrow rows 2/3 profile
band(442, 505, 246, 260, 1, "outrow2")
band(442, 505, 328, 342, 1, "outrow3")

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("WROTE", OUT)
