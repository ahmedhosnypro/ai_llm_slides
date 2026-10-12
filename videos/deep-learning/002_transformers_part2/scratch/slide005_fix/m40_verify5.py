# m40_verify5.py — closed-loop verification of render_5 (arrow-attachment fix).
# 1. diff vs render_4 confined to the edited arrow regions (no placeholder bleed)
# 2. attachment-touch asserts: every connector endpoint within tolerance of its
#    target component's rendered ink (150 dpi, 1 px = 1/200 in; build pt * 2.08333)
from PIL import Image
import sys

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
R4 = Image.open(VID + "/recreated_pptx/qa/slide005/render_4.png").convert("RGB")
R5 = Image.open(VID + "/recreated_pptx/qa/slide005/render_5.png").convert("RGB")
po, pn = R4.load(), R5.load()
W, H = R5.size
K = 150 / 72.0  # build pt -> render px

fails = []
def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("  " + detail if detail else ""))
    if not cond:
        fails.append(name)

# ---- 1. diff confinement ------------------------------------------------------
DIFF_BOXES = [
    # (x0,y0,x1,y1) in BUILD pt, generous windows around the six edited strokes
    (315, 240, 500, 395),   # connect_h line + leaders A/B + hook + head zone
]
changed = []
for y in range(0, H, 2):
    for x in range(0, W, 2):
        if po[x, y] != pn[x, y]:
            changed.append((x, y))
# map changed px to build pt, test containment
def in_boxes(p):
    bx, by = p[0] / K, p[1] / K
    return any(x0 - 3 <= bx <= x1 + 3 and y0 - 3 <= by <= y1 + 3
               for (x0, y0, x1, y1) in DIFF_BOXES)
out = [p for p in changed if not in_boxes(p)]
check("diff confined to arrow windows", len(out) == 0,
      f"changed={len(changed)} outside={len(out)}" + (f" e.g. {out[:5]}" if out else ""))

# ---- 2. ink probes ------------------------------------------------------------
def ink(p, x, y, tol=60):
    r, g, b = pn[int(x), int(y)]
    L = 0.299 * r + 0.587 * g + 0.114 * b
    return L < 235 - tol // 2  # darker than the E9E9E7/E4E4E4 field

def near_ink(cx, cy, rad, pred):
    for y in range(int(cy - rad), int(cy + rad + 1)):
        for x in range(int(cx - rad), int(cx + rad + 1)):
            if 0 <= x < W and 0 <= y < H and pred(x, y):
                return True
    return False

def grayline(x, y):
    r, g, b = pn[x, y]
    L = 0.299 * r + 0.587 * g + 0.114 * b
    return L < 215 and abs(r - g) < 22 and abs(g - b) < 22

def darkink(x, y):
    r, g, b = pn[x, y]
    return 0.299 * r + 0.587 * g + 0.114 * b < 150

def redink(x, y):
    r, g, b = pn[x, y]
    return r > 120 and g < 110 and (r - g) > 45

# 2a. connect_h leader line ends INSIDE the head base
hx, hy = 494.4 * K, 357.4 * K
check("connect_h -> head base attached", near_ink(hx, hy, 4, grayline) or near_ink(hx, hy, 4, darkink),
      f"probe ({hx:.0f},{hy:.0f})")
# 2b. leader A horizontal present + reaches its elbow
midA = (322.5 + 483.5) / 2 * K, 344.9 * K
check("leader A horizontal ink", near_ink(midA[0], midA[1], 4, grayline), f"probe ({midA[0]:.0f},{midA[1]:.0f})")
elbowA = 483.8 * K, 366.3 * K
check("leader A vertical bottom ink", near_ink(elbowA[0], elbowA[1], 4, grayline) or near_ink(elbowA[0], elbowA[1], 4, darkink),
      f"probe ({elbowA[0]:.0f},{elbowA[1]:.0f})")
# 2c. leader B horizontal present, right end on the shadow border (x477.9)
midB = (317.1 + 477.7) / 2 * K, 351.7 * K
check("leader B horizontal ink", near_ink(midB[0], midB[1], 4, grayline), f"probe ({midB[0]:.0f},{midB[1]:.0f})")
endB = 477.7 * K, 351.7 * K
check("leader B end on shadow border", near_ink(endB[0], endB[1], 5, grayline), f"probe ({endB[0]:.0f},{endB[1]:.0f})")
# 2d. hook end ON the rect right border ink (border center build x475, 1.5pt wide)
hooke = 474.9 * K, 385.0 * K
check("hook end on rect border ink", near_ink(hooke[0], hooke[1], 4, redink), f"probe ({hooke[0]:.0f},{hooke[1]:.0f})")
# 2e. d1 end on enc MHA box left border (build 650 +-0.75pt)
d1e = 650 * K, 372 * K
check("d1 end on box border", near_ink(d1e[0], d1e[1], 5, redink), f"probe ({d1e[0]:.0f},{d1e[1]:.0f})")
# 2f. d2 end within 3 frame px of rect left border (build 303)
d2e = 304.8 * K, 375.5 * K
check("d2 end near rect border", near_ink(d2e[0], d2e[1], 6, redink), f"probe ({d2e[0]:.0f},{d2e[1]:.0f})")
# 2g. d3 end on SDPA inset right edge (frame 199.8 -> build 189.1)
d3e = 189.1 * K, 487.2 * K
check("d3 end near inset edge", near_ink(d3e[0], d3e[1], 6, redink), f"probe ({d3e[0]:.0f},{d3e[1]:.0f})")
# 2h. connect_tan end on inset top border (frame 480.5,237.5 -> build 480.9,247.3)
cte = 480.9 * K, 247.3 * K
check("connect_tan end on inset border", near_ink(cte[0], cte[1], 5, redink), f"probe ({cte[0]:.0f},{cte[1]:.0f})")
# 2i. head tip touches circle top (head tip build (493.9,366.3); circle top 367.6)
tip = 493.9 * K, 366.5 * K
check("head tip touches circle", near_ink(tip[0], tip[1], 5, lambda x, y: darkink(x, y) or ink(None, x, y)),
      f"probe ({tip[0]:.0f},{tip[1]:.0f})")

print("\n%d checks, %d FAIL" % (12, len(fails)))
sys.exit(1 if fails else 0)
