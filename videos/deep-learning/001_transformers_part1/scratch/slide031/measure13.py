#!/usr/bin/env python3
"""measure13 — final geometry probe for the slide_031 build (canvas, callouts, pills,
outcaps, matrix, notebox, subtitle). Frame = unique_slides/slide_031.jpg (960x540)."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def cls(c):
    r, g, b = c
    if r > 244 and g > 244 and b > 244: return "W"      # white
    if abs(r - 233) < 14 and abs(g - 233) < 14 and abs(b - 231) < 16: return "G"  # chrome gray
    if r > 240 and 210 < g < 245 and 185 < b < 225: return "P"  # peach
    if r > 140 and g < 110 and b < 110: return "R"      # red
    if b > 140 and b - r > 30 and b - g > 30: return "B"  # blue
    if g > 110 and g - r > 25 and g - b > 25: return "n"  # green
    if r > 235 and g > 235 and b < 205: return "Y"      # yellow
    if sum(c) < 260: return "k"                          # dark ink
    return "."

def hruns(y, x0, x1, minrun=2):
    out = []; cur = None; s = x0
    for x in range(x0, x1):
        k = cls(px[x, y])
        if k != cur:
            if cur is not None and x - s >= minrun: out.append((cur, s, x - 1))
            elif cur is not None: out.append((cur + "?", s, x - 1))
            cur = k; s = x
    out.append((cur, s, x1 - 1))
    # merge tiny
    return [o for o in out if o[2] - o[1] >= 1][:40]

def vruns(x, y0, y1, minrun=2):
    out = []; cur = None; s = y0
    for y in range(y0, y1):
        k = cls(px[x, y])
        if k != cur:
            if cur is not None and y - s >= minrun: out.append((cur, s, y - 1))
            elif cur is not None: out.append((cur + "?", s, y - 1))
            cur = k; s = y
    out.append((cur, s, y1 - 1))
    return [o for o in out if o[2] - o[1] >= 1][:40]

print("== A. canvas edges: horizontal scans ==")
for y in [70, 95, 200, 305, 524, 533]:
    print(f" y={y}:", hruns(y, 0, 60), "...", hruns(y, 880, 960))
print("   full-width run summary y=200 x0..960:")
print("  ", hruns(200, 0, 960, 3))
print("== B. canvas top/bottom: vertical scans ==")
for x in [700, 480, 60]:
    print(f" x={x} y30..120:", vruns(x, 30, 120, 1))
    print(f" x={x} y500..540:", vruns(x, 500, 540, 1))
print("   canvas hue:", [px[p] for p in [(700, 95), (480, 95), (200, 305), (700, 460), (480, 96)]])

print("== C. callout fills/borders ==")
for lbl, (bx0, by0, bx1, by1) in [("c1", (430, 272, 660, 316)), ("c2", (714, 298, 892, 346)), ("c3", (430, 330, 660, 378))]:
    print(f" {lbl} top border scan y by0..by0+6 @x mid:")
    xm = (bx0 + bx1) // 2
    print("   ", [(y, px[xm, y]) for y in range(by0, by0 + 7)])
    print(f" {lbl} left border scan x bx0..bx0+8 @y mid:")
    ym = (by0 + by1) // 2
    print("   ", [(x, px[x, ym]) for x in range(bx0, bx0 + 9)])
    print(f" {lbl} fill:", [px[p] for p in [(xm, ym - 6), (xm, ym + 6), (bx0 + 30, ym)]])

print("== D. Q pill ==")
print(" y152 x55..225:", hruns(152, 55, 225, 1))
print(" x140 y125..180:", vruns(140, 125, 180, 1))
print(" pill fill:", [px[p] for p in [(78, 152), (200, 152), (140, 140), (140, 165)]])
print(" circle fill:", [px[p] for p in [(107, 152), (130, 152), (153, 152), (176, 152)]])
print("== E. Q outcap ==")
print(" x431 y105..300:", vruns(431, 105, 300, 1))
print(" y200 x400..470:", hruns(200, 400, 470, 1))
print(" outcap fill/tiles:", [px[p] for p in [(431, 122), (431, 140), (431, 155), (431, 180), (431, 220), (431, 260), (431, 285)]])
print("== F. Q matrix ==")
print(" y200 x210..415:", hruns(200, 210, 415, 1))
print(" x300 y108..300:", vruns(300, 108, 300, 1))
print(" cell fill / chip fill:", [px[p] for p in [(240, 122), (240, 200), (280, 200), (300, 140), (240, 285)]])
print("== G. notebox ==")
print(" x700 y440..525:", vruns(700, 440, 525, 1))
print(" y482 x480..905:", hruns(482, 480, 905, 1))
print(" border color:", [px[p] for p in [(700, 448), (700, 518), (491, 482), (893, 482)]])
# text line bands (dark+blue+red ink rows x500..890)
print(" ink rows:")
for y in range(450, 520):
    n = sum(1 for x in range(500, 890) if sum(px[x, y]) < 480)
    if n > 3: print(f"   y={y}: {n}")
print(" blue core:", [px[p] for p in [(700, 503), (750, 503), (800, 460)]])
print("== H. subtitle caps ==")
for y in range(70, 95):
    n = sum(1 for x in range(108, 880) if sum(px[x, y]) < 330)
    print(f"   y={y}: {n}", end="")
print()
print("== I. role letters ==")
def bbox(x0, y0, x1, y1, keep):
    xs = []; ys = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if keep(px[x, y]): xs.append(x); ys.append(y)
    if not xs: return None
    return (min(xs), min(ys), max(xs), max(ys), len(xs))
red = lambda c: c[0] > 120 and c[0] - c[1] > 50 and c[0] - c[2] > 50
blue = lambda c: c[2] > 110 and c[2] - c[0] > 40 and c[2] - c[1] > 30
green = lambda c: c[1] > 100 and c[1] - c[0] > 25 and c[1] - c[2] > 25
dark = lambda c: sum(c) < 300
print(" Q role:", bbox(400, 94, 470, 122, red))
print(" V role:", bbox(800, 94, 880, 122, blue))
print(" K role:", bbox(400, 306, 470, 334, green))
print(" Q '=':", bbox(374, 180, 410, 225, dark))
print(" V '=':", bbox(792, 180, 826, 225, dark))
print(" K '=':", bbox(379, 385, 415, 430, dark))
print(" Q W_Q:", bbox(160, 228, 216, 268, red))
print(" V W_V:", bbox(575, 228, 630, 268, red))
print(" K W_K:", bbox(160, 425, 216, 465, red))
print(" Q 1xd:", bbox(175, 165, 220, 192, dark))
print(" V 1xd:", bbox(585, 165, 630, 192, dark))
print(" K 1xd:", bbox(175, 362, 220, 390, dark))
print(" Q X2:", bbox(100, 178, 160, 220, red))
print(" V X2:", bbox(500, 178, 560, 220, red))
print(" K X2:", bbox(100, 375, 160, 418, red))
print(" Q dxd:", bbox(330, 270, 375, 298, dark))
print(" V dxd:", bbox(745, 270, 795, 298, dark))
print(" K dxd:", bbox(330, 485, 375, 512, dark))
print("== J. panel border cores ==")
print(" Q border:", [px[p] for p in [(250, 98), (250, 299), (57, 200), (466, 200)]])
print(" V border:", [px[p] for p in [(700, 98), (700, 298), (479, 200), (886, 200)]])
print(" K border:", [px[p] for p in [(250, 311), (250, 528), (58, 420), (469, 420)]])
print("== K. matrix text row color cores (Q) ==")
for i, (yy0, yy1) in enumerate([(128, 150), (170, 191), (211, 233), (252, 274)]):
    best = None
    for y in range(yy0, yy1):
        for x in range(222, 372):
            c = px[x, y]
            if sum(c) < 330:
                if best is None or sum(c) < sum(best): best = c
    print(f"   Q row{i+1} darkest: {best}")
print("== L. V/K pill + outcap + matrix quick ==")
print(" V pill y152 x470..660:", hruns(152, 470, 660, 1))
print(" K pill y368 x45..225:", hruns(368, 45, 225, 1))
print(" V outcap x855 y105..300:", vruns(855, 105, 300, 1))
print(" K outcap x430 y325..515:", vruns(430, 325, 515, 1))
print(" V matrix x700 y105..300:", vruns(700, 105, 300, 1))
print(" K matrix x300 y320..515:", vruns(300, 320, 515, 1))
print(" V outcap fill:", [px[p] for p in [(855, 122), (855, 200), (855, 280)]])
print(" K outcap fill:", [px[p] for p in [(430, 345), (430, 420), (430, 495)]])
print(" V matrix cell:", [px[p] for p in [(650, 125), (700, 200), (750, 270)]])
print(" K matrix cell:", [px[p] for p in [(240, 345), (300, 420), (360, 490)]])
