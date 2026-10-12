#!/usr/bin/env python3
"""measure4.py — slide 025 precision pass: dividers, rings, eq boxes, borders,
arrows, callouts, cap heights. Banked as measure4_out.txt."""
from collections import Counter
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide025/measure4_out.txt"
im = Image.open(SRC).convert("RGB")
W, H = im.size
P = im.load()
L = []
def pr(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
def bbox(x0, y0, x1, y1, pred):
    x1 = min(x1, W-1); y1 = min(y1, H-1)
    xs, ys = [], []
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            if pred(*P[x, y]): xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None
dark = lambda r, g, b: r < 130 and g < 130 and b < 130
tred = lambda r, g, b: r > 120 and g < 80 and b < 80
blue = lambda r, g, b: b > 120 and r < 100 and g < 100
magenta = lambda r, g, b: r > 140 and g < 110 and b > 140
grayring = lambda r, g, b: 60 <= r <= 160 and 60 <= g <= 160 and 60 <= b <= 160

# 1) divider columns: dark px count per x over each row band
pr("== dividers (dark px per x, count over band) ==")
for cy in [181, 254, 336]:
    for (x0, x1, tag) in [(130, 300, "col0+col1"), (400, 460, "col2")]:
        cnt = {}
        for x in range(x0, x1+1):
            n = sum(1 for y in range(cy-16, cy+17) if dark(*P[x, y]))
            if n >= 12: cnt[x] = n
        pr(f"  cy{cy} {tag}: {cnt}")

# 2) rings: gray stroke px clusters per row
pr("== rings per row (gray px x-clusters x185..245) ==")
for cy in [181, 254, 336]:
    cols = [x for x in range(185, 246) if any(grayring(*P[x, y]) for y in range(cy-7, cy+8))]
    runs, cur, prev = [], None, None
    for x in cols:
        if cur is None: cur = x
        elif x - prev > 2: runs.append((cur, prev)); cur = x
        prev = x
    if cur is not None: runs.append((cur, prev))
    pr(f"  cy{cy}: {runs}")

# 3) equation boxes: dark border bboxes in strip
pr("== equation boxes (border=dark bbox within windows) ==")
for (x0, x1, tag) in [(60, 280, "box1"), (280, 530, "box2"), (515, 790, "box3")]:
    pr(f"  {tag}:", bbox(x0, 438, x1, 518, dark))
# fills
cream = lambda r, g, b: r > 228 and g > 228 and 190 < b < 240
for (x0, x1, tag) in [(70, 270, "box1"), (290, 520, "box2"), (530, 770, "box3")]:
    bb = bbox(x0, 440, x1, 516, cream)
    pr(f"  {tag} fill:", bb)
pr("  box1 fill modal:", Counter(P[x, y] for y in range(460, 495) for x in range(90, 240) if cream(*P[x, y])).most_common(3))

# 4) equation ink bboxes (dark, inside boxes)
pr("== equation ink bboxes ==")
pr("  box1 ink:", bbox(75, 445, 265, 512, dark))
pr("  box2 ink:", bbox(295, 445, 515, 512, dark))
pr("  box3 ink:", bbox(540, 445, 780, 512, dark))
# cap heights: column profile of ink rows
def rowprof(x0, y0, x1, y1):
    return {y: sum(1 for x in range(x0, x1+1) if dark(*P[x, y])) for y in range(y0, y1+1)}
pr("  box1 ink rows:", {k: v for k, v in rowprof(80, 450, 260, 510).items() if v})
pr("  box2 ink rows:", {k: v for k, v in rowprof(300, 450, 510, 510).items() if v})
pr("  box3 ink rows:", {k: v for k, v in rowprof(545, 445, 775, 510).items() if v})

# 5) outboxes: white + border color ring
pr("== outboxes ==")
outw = lambda r, g, b: r > 242 and g > 242 and b > 242
for (y0, y1) in [(165, 200), (238, 273), (320, 355)]:
    pr(f"  white bbox y{y0}:", bbox(495, y0, 585, y1, outw))
    pr(f"  ink bbox y{y0}:", bbox(502, y0, 570, y1, dark))
# border color: px on box1 outline ring (x500..563, y172..194 not white)
cnt = Counter(P[x, y] for y in range(171, 196) for x in range(498, 566)
              if not outw(*P[x, y]) and abs(P[x, y][0]-P[x, y][1]) < 60)
pr("  outbox1 ring modal:", cnt.most_common(8))

# 6) class boxes: border bbox (dark) per row
pr("== class boxes (dark border+text bbox) ==")
for (y0, y1) in [(165, 200), (238, 273), (320, 355)]:
    pr(f"  y{y0}:", bbox(600, y0, 700, y1, dark))
pr("  class1 ring modal:", Counter(P[x, y] for y in range(172, 194) for x in range(606, 690)
    if 190 < P[x, y][0] < 245 and P[x, y][1] > 230).most_common(4))

# 7) block arrows: fill bboxes
bluish = lambda r, g, b: 195 <= r <= 245 and 210 <= g <= 248 and b > 240
grn = lambda r, g, b: 170 <= r <= 228 and g > 230 and 130 <= b <= 210
pr("== block arrows ==")
pr("  i fill:", bbox(235, 360, 300, 420, bluish))
pr("  j fill:", bbox(390, 360, 470, 420, grn))
pr("  i outline bbox:", bbox(235, 360, 300, 420, lambda r, g, b: dark(r, g, b) or (b > 150 and r < 150 and g < 170)))
pr("  j outline bbox:", bbox(390, 360, 470, 420, lambda r, g, b: dark(r, g, b) or (grn(r, g, b) and g - r > 30)))

# 8) callout boxes: border dark bbox
pr("== callouts ==")
pr("  prev box (dark border):", bbox(205, 395, 320, 445, dark))
pr("  curr box (dark border):", bbox(375, 395, 485, 445, dark))

# 9) IS/SL boxes: dark border bbox
pr("== mag boxes ==")
pr("  IS box:", bbox(50, 88, 150, 132, dark))
pr("  SL box:", bbox(595, 88, 690, 132, dark))
pr("  left arrowhead magenta:", bbox(112, 100, 148, 122, magenta))
pr("  right arrowhead magenta:", bbox(594, 100, 618, 122, magenta))

# 10) w_ji labels tight
pr("== w_ji labels ==")
pr("  w1 (row1 line):", bbox(315, 165, 360, 200, blue))
pr("  w2 (descending):", bbox(315, 200, 360, 245, blue))
pr("  w3 (ascending):", bbox(315, 235, 360, 270, blue))

# 11) Net pointers
pr("== net pointers ==")
pr("  Net_i ptr:", bbox(236, 168, 268, 205, tred))
pr("  Net_j ptr (below mesh):", bbox(405, 184, 435, 210, tred))
pr("  Net_i text:", bbox(195, 135, 250, 170, tred))
pr("  Net_j text:", bbox(360, 135, 420, 170, tred))

# 12) green-rim port probe (dark red at col2 right rim, rows away from O_j text)
dr = lambda r, g, b: 100 <= r <= 190 and g < 60 and b < 60
for cy in [181, 254, 336]:
    n = [(x, y) for y in range(cy-6, cy+7) for x in range(446, 460) if dr(*P[x, y])]
    pr(f"  green rim cy{cy} darkred px:", len(n), n[:12])

# 13) title + olabels cap heights
pr("== O label ink (exclude mesh rows) ==")
for (y0, y1, x0, x1, tag) in [(160, 178, 270, 305, "Oi r1"), (160, 178, 440, 475, "Oj r1"),
                               (233, 251, 270, 305, "Oi r2"), (314, 332, 270, 305, "Oi r3")]:
    pr(f"  {tag}:", bbox(x0, y0, x1, y1, tred))
pr("O_i r1 rows:", {y: sum(1 for x in range(272, 302) if tred(*P[x, y])) for y in range(160, 190)})

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("WROTE", OUT)
