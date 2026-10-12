# m41_verify5b.py — CORRECTED re-run of m40_verify5.py (same render_5, same checks).
#
# WHY A RE-RUN: m40_verify5_out.txt reported 11/12 with one FAIL —
#   "connect_tan end on inset border  probe (1002,515)".
# That FAIL is a PREDICATE ARTIFACT, not an attachment failure:
#  - connect_tan is drawn in pinkConn C47070, which renders (196,112,112);
#    m40's redink() requires g < 110, so pure and blended pink pixels
#    (196,112,112)/(137,112,94) can never pass it — redink only fits C00000
#    strokes (d1/d2/d3, which PASSed).
#  - Pixel dump at the endpoint (banked in the session log): at render column
#    x=1002 the pink connector ink runs y=509..514, and rows y=510..514 at that
#    column are the MHA inset's green top border (27,114,63) — the connector's
#    ink OVERLAPS the border band and stops at y=514, before the interior
#    (y>=515 background 233,233,231). Attachment = ink on border ink: TRUE.
#  - Original-frame parity: at frame (480.3,237.2) the original's faint gray
#    connector (212,212,212) likewise descends into the green border rows
#    (42,140,37 at y238-239) — same junction topology.
#  - Vision corroboration: afix_cropcmp_corridor_4.txt (render_4 crop; m40's diff
#    proves connect_tan pixels identical render_4 -> render_5, changed px
#    confined to the connect_h window, outside=0) PASSed this exact junction:
#    "its ink terminates **on** the green top border — the junction is present".
# ONLY the connect_tan check's ink predicate is corrected (pink-family +
# structural overlap assert); every other check is byte-identical in logic to
# m40_verify5.py.
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
    (315, 240, 500, 395),   # connect_h line + leaders A/B + hook + head zone
]
changed = []
for y in range(0, H, 2):
    for x in range(0, W, 2):
        if po[x, y] != pn[x, y]:
            changed.append((x, y))
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
    return L < 235 - tol // 2

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

# pinkConn-family ink: C47070 renders (196,112,112); antialiased blends keep
# r leading g and b by a visible margin. (redink's g<110 excludes this family.)
def pinkink(x, y):
    r, g, b = pn[x, y]
    return r > 130 and (r - g) > 20 and (r - b) > 20

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
# 2h. connect_tan end on inset top border — CORRECTED predicate (see header).
#     (i) pink-family connector ink within radius 5 of the endpoint ...
cte = 480.9 * K, 247.3 * K
check("connect_tan end on inset border", near_ink(cte[0], cte[1], 5, pinkink), f"probe ({cte[0]:.0f},{cte[1]:.0f})")
#     (ii) ... AND structural attach: at the endpoint column the connector's ink
#     rows overlap the green border's ink rows (tip reaches INTO the border band).
col = int(round(cte[0]))
border_rows = [y for y in range(500, 526) if pn[col, y][1] > pn[col, y][0] and pn[col, y][1] > pn[col, y][2] and pn[col, y][1] < 200]
conn_rows = [y for y in range(495, 521) if any(pinkink(x, y) for x in range(col - 2, col + 3))]
overlap = sorted(set(border_rows) & set(conn_rows))
check("connect_tan ink overlaps border rows", len(overlap) > 0 and max(conn_rows) >= min(border_rows),
      f"border_rows={border_rows} conn_rows={conn_rows} overlap={overlap}")
# 2i. head tip touches circle top (head tip build (493.9,366.3); circle top 367.6)
tip = 493.9 * K, 366.5 * K
check("head tip touches circle", near_ink(tip[0], tip[1], 5, lambda x, y: darkink(x, y) or ink(None, x, y)),
      f"probe ({tip[0]:.0f},{tip[1]:.0f})")

print("\n%d checks, %d FAIL" % (13, len(fails)))
sys.exit(1 if fails else 0)
