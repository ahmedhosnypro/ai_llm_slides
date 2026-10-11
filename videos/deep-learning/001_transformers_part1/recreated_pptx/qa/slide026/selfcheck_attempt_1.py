#!/usr/bin/env python3
"""Self-check attempt 1 (closed-loop): render (2001x1125 @150dpi) vs original-frame
targets. 1 frame-px = 150/72 = 2.08333 render-px. Banked numbers."""
import numpy as np
from PIL import Image

R = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide026/render_1.png").convert("RGB")).astype(int)
H, W, _ = R.shape
S = 150 / 72.0
print(f"render {W}x{H}, scale {S:.4f}")

def med(x, y, r=2):  # frame-px coords
    x, y = int(x * S), int(y * S)
    reg = R[y - r:y + r + 1, x - r:x + r + 1].reshape(-1, 3)
    m = np.median(reg, axis=0).astype(int)
    return f"#{m[0]:02X}{m[1]:02X}{m[2]:02X}"

def bbox(name, x0, y0, x1, y1, target, tol):
    sub = R[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    t = np.array(target)
    m = (np.abs(sub - t).sum(axis=2) <= tol)
    if m.sum() == 0:
        print(f"  {name:30s} NO MATCH in x{x0}..{x1} y{y0}..{y1}")
        return None
    ys, xs = np.where(m)
    bx0, bx1, by0, by1 = x0 + xs.min() / S, x0 + xs.max() / S, y0 + ys.min() / S, y0 + ys.max() / S
    print(f"  {name:30s} x{bx0:.1f}..{bx1:.1f} y{by0:.1f}..{by1:.1f} n={int(m.sum())}")
    return (bx0, bx1, by0, by1)

ok = True
def chk(name, got, want, tol):
    global ok
    d = max(abs(a - b) for a, b in zip(got, want))
    status = "OK " if d <= tol else "FAIL"
    if d > tol: ok = False
    print(f"  [{status}] {name:28s} got={[round(v,1) for v in got]} want={want} maxd={d:.1f}")

print("== fills ==")
checks = [
    ("canvas peach", med(430, 240), (247, 226, 205), 14),
    ("left stack fill", med(62, 300), (231, 252, 233), 16),
    ("strip fill", med(183, 480), (231, 252, 233), 16),
    ("softmax bar", med(473, 220), (248, 222, 251), 16),
    ("dotproduct box", med(264, 380), (219, 203, 187), 16),
    ("sigma box", med(530, 205), (234, 254, 252), 14),
    ("ellipse Sim", med(290, 185), (249, 252, 219), 16),
    ("Ybox c1", med(555, 132), (178, 220, 165), 20),
    ("X2 cell2", med(285, 495), (224, 165, 211), 24),
    ("red block arrow", med(272, 520), (197, 0, 15), 40),
    ("green arrow", med(560, 159), (18, 180, 90), 40),
    ("dot1", med(330, 246), (2, 0, 171), 60),
    ("panel gray", med(200, 60), (233, 233, 231), 12),
]
for name, got, want, tol in checks:
    g = tuple(int(got[i:i+2], 16) for i in (1, 3, 5))
    chk(name, g, want, tol)

print("== geometry (frame-px) ==")
print("-- title/subtitle ink")
sub = R[int(50 * S):int(80 * S), int(60 * S):int(860 * S)]
m = sub.sum(axis=2) < 340
ys, xs = np.where(m)
chk("title ink y", (50 + ys.min() / S, 50 + ys.max() / S), (58, 76), 4)
xs2 = xs[(ys > 6 * S) & (ys < 24 * S)]  # exclude badge rows
chk("title ink x", (60 + xs2.min() / S, 60 + xs2.max() / S), (260, 745), 9)
sub = R[int(79 * S):int(104 * S), int(60 * S):int(860 * S)]
m = sub.sum(axis=2) < 340
ys, xs = np.where(m)
chk("subtitle ink y", (79 + ys.min() / S, 79 + ys.max() / S), (79, 101), 4)
xs2 = xs[(ys > 0)]
# exclude badge cols
xs3 = xs2[(xs2 + 60 * S) < 870 * S]
chk("subtitle ink x", (60 + xs3.min() / S, 60 + xs3.max() / S), (186, 809), 10)
# red tokens present?
sub = R[int(78 * S):int(103 * S), int(180 * S):int(860 * S)]
redm = (sub[:, :, 0] - sub[:, :, 1] > 60) & (sub[:, :, 0] > 120)
print(f"  subtitle red-token px: {int(redm.sum())} (want >200)")

print("-- boxes")
bbox("peach canvas row y=440", 20, 438, 940, 443, (247, 226, 205), 30)
bbox("canvas top scan x700", 698, 100, 702, 120, (247, 226, 205), 30)
b = bbox("Sim ellipse", 240, 150, 380, 200, (249, 252, 219), 24)
if b: chk("Sim ellipse bbox", b, (266, 341, 160, 188), 5)
b = bbox("Prob ellipse", 400, 150, 545, 205, (249, 252, 219), 24)
if b: chk("Prob ellipse bbox", b, (428, 516, 161, 192), 5)
b = bbox("WSum ellipse", 540, 140, 720, 200, (249, 252, 219), 24)
if b: chk("WSum ellipse bbox", b, (568, 693, 152, 187), 6)
b = bbox("DotProduct box", 200, 185, 400, 415, (219, 203, 187), 26)
if b: chk("DotProduct bbox", b, (253, 343, 194, 404), 4)
b = bbox("Softmax bar", 430, 185, 515, 412, (248, 222, 251), 26)
if b: chk("Softmax bbox", b, (458, 488, 196, 401), 4)
b = bbox("Sigma box", 490, 188, 670, 224, (234, 254, 252), 20)
if b: chk("Sigma bbox", b, (516, 649, 196, 217), 4)
b = bbox("Ybox cells", 535, 112, 630, 146, (178, 220, 165), 40)
if b: chk("Ybox bbox", b, (549, 616, 121, 145), 5)
b = bbox("left stack", 40, 300, 160, 320, (231, 252, 233), 22)
if b: chk("left stack x", (b[0], b[1]), (57, 139), 4)
b = bbox("right stack", 730, 300, 880, 320, (231, 252, 233), 22)
if b: chk("right stack x", (b[0], b[1]), (761, 843), 4)
b = bbox("strip", 160, 495, 520, 500, (231, 252, 233), 22)
if b: chk("strip x", (b[0], b[1]), (178, 492), 5)
b = bbox("X2 labelcell", 288, 482, 310, 506, (196, 76, 136), 60)
if b: chk("X2 labelcell", b, (293, 305, 487, 501), 5)
b = bbox("X2 cell5", 318, 482, 336, 505, (220, 146, 227), 40)
if b: chk("X2 cell5", b, (321, 331, 487, 501), 5)

print("-- highlight + dot label")
b = bbox("title highlight", 400, 48, 860, 84, (251, 242, 155), 40)
if b: chk("highlight bbox", b, (508, 748, 54, 77), 8)
b = bbox("dot label ink", 260, 195, 345, 232, (92, 55, 18), 150)
if b: chk("Dot/Product ink", b, (272, 320, 201, 225), 6)
b = bbox("softmax label ink", 460, 255, 487, 345, (107, 0, 110), 150)
if b: chk("softmax label", ((b[0]+b[1])/2, (b[2]+b[3])/2), (473, 299), 6)

print("-- dots")
for i, (cx, cy) in enumerate([(330.5, 246.5), (314.5, 287.5), (295.5, 328), (276.5, 372.5)]):
    b = bbox(f"dot{i+1}", cx - 8, cy - 8, cx + 8, cy + 8, (2, 0, 171), 90)
    if b: chk(f"dot{i+1} center", ((b[0] + b[1]) / 2, (b[2] + b[3]) / 2), (cx, cy), 3)

print("-- lines present (max diff from peach along row)")
PEACH = np.array([247, 226, 205])
for y in (246, 287, 328, 372):
    row = R[int(y * S), int(350 * S):int(450 * S)]
    d = np.abs(row - PEACH).sum(axis=1)
    print(f"  line y={y}: maxdiff {int(d.max())} (want >30)")
for x in (532, 563, 591, 622):
    col = R[int(228 * S):int(240 * S), int(x * S)]
    d = np.abs(col - PEACH).sum(axis=1)
    print(f"  vert x={x}: maxdiff {int(d.max())} (want >30)")
# right lines
for y, x1 in ((246, 755), (287, 755), (328, 755), (372, 680)):
    row = R[int(y * S), int(600 * S):int(x1 * S)]
    d = np.abs(row - PEACH).sum(axis=1)
    print(f"  rightline y={y} to x{x1}: maxdiff {int(d.max())} (want >25)")

print("-- containment: content ink inside house frame (0.15in inset => x>=31, x<=1969, y>=31, y<=1093)")
gray = (np.abs(R - np.array([233, 233, 231])).sum(axis=2) <= 30)
white = (R > 235).all(axis=2)
chrome = gray | white
ink = ~chrome
top = ink[:int(45 * S), :]
bot = ink[int(522 * S + 8 * S):, :]
print(f"  ink above canvas-top zone (y<45px): {int(top.sum())} px (badge/highlight allowed if y>53)")
print(f"  ink below y530: {int(bot.sum())} px (chrome bottom stroke expected)")

print("-- nodes / W labels / arrows / curves (presence)")
for i, (cx, cy) in enumerate([(532, 246), (563, 287), (591, 328), (622, 372)]):
    sub = R[int((cy - 9) * S):int((cy + 9) * S), int((cx - 18) * S):int((cx + 18) * S)]
    redm = (sub[:, :, 0] - sub[:, :, 1] > 45) & (sub[:, :, 0] > 130)
    print(f"  node{i+1} red px: {int(redm.sum())} (want >60)")
for i, wy in enumerate([226, 267, 308, 352]):
    sub = R[int(wy * S):int((wy + 13) * S), int(493 * S):int(512 * S)]
    blum = (sub[:, :, 2] - sub[:, :, 0] > 30) & (sub.sum(axis=2) < 620)
    print(f"  W{i+1} label blue px: {int(blum.sum())} (want >25)")
sub = R[int(500 * S):int(532 * S), int(258 * S):int(300 * S)]
redm = (sub[:, :, 0] - sub[:, :, 1] > 45) & (sub[:, :, 0] > 130)
print(f"  red block arrow px: {int(redm.sum())} (want >100)")
sub = R[int(400 * S):int(475 * S), int(292 * S):int(305 * S)]
redm = (sub[:, :, 0] - sub[:, :, 1] > 45) & (sub[:, :, 0] > 130)
print(f"  query arrow px: {int(redm.sum())} (want >60)")
sub = R[int(390 * S):int(470 * S), int(90 * S):int(180 * S)]
cur = (np.abs(sub - PEACH).sum(axis=2) > 25) & (np.abs(sub - np.array([233, 233, 231])).sum(axis=2) > 25)
print(f"  left curve ink px: {int(cur.sum())} (want >40)")
sub = R[int(400 * S):int(500 * S), int(500 * S):int(810 * S)]
cur = (np.abs(sub - PEACH).sum(axis=2) > 25) & (np.abs(sub - np.array([233, 233, 231])).sum(axis=2) > 25)
print(f"  right curve ink px: {int(cur.sum())} (want >60)")
sub = R[int(148 * S):int(168 * S), int(547 * S):int(578 * S)]
gm = (sub[:, :, 1] - sub[:, :, 0] > 40) & (sub[:, :, 1] > 130)
print(f"  green arrow px: {int(gm.sum())} (want >150)")
sub = R[int(392 * S):int(410 * S), int(94 * S):int(112 * S)]
gm = (sub[:, :, 1] - sub[:, :, 0] > 25) & (sub.sum(axis=2) < 500)
print(f"  left curve head green px: {int(gm.sum())} (want >30)")
sub = R[int(392 * S):int(410 * S), int(795 * S):int(813 * S)]
gm = (sub[:, :, 1] - sub[:, :, 0] > 25) & (sub.sum(axis=2) < 500)
print(f"  right curve head green px: {int(gm.sum())} (want >30)")
# Dot Product label line pitch
sub = R[int(195 * S):int(232 * S), int(260 * S):int(340 * S)]
m = sub.sum(axis=2) < 460
rows = np.where(m.sum(axis=1) > 2)[0]
if len(rows):
    bands, s0, p = [], rows[0], rows[0]
    for v in rows[1:]:
        if v > p + 2: bands.append((s0, p)); s0 = v
        p = v
    bands.append((s0, p))
    tops = [195 + b[0] / S for b in bands]
    print(f"  Dot/Product line tops: {[round(t,1) for t in tops]} (want 201,216 pitch 15)")
    if len(tops) == 2: chk("dotlabel pitch", [tops[1] - tops[0]], [15], 3)

print()
print("SELF-CHECK RESULT:", "PASS" if ok else "FAIL")
