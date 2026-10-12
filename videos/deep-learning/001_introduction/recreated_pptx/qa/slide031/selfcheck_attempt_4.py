"""Slide 031 attempt-2 closed-loop self-check (full). Banked as selfcheck_attempt_4.py."""
from PIL import Image
import numpy as np

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide031/render_4.png"
im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
S = W / 960.0
print(f"render {W}x{H}")
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
darkred = (R > 100) & (R - G > 50) & (R - B > 40)
navy = (R < 90) & (G < 90) & (B > 95) & (B - R > 60)
peri = (B - R > 8) & (B - G > 8) & (B > 150) & (R < 235) & (G < 235)
dark = (R < 110) & (G < 110) & (B < 110)
red = darkred

def bbox(mask, x0, x1, y0, y1, label, target=None):
    m = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    rows = np.where(m.any(axis=1))[0]; cols = np.where(m.any(axis=0))[0]
    if not len(rows):
        print(f"  {label}: EMPTY"); return None
    fx0, fy0 = x0 + cols[0]/S, y0 + rows[0]/S
    fx1, fy1 = x0 + cols[-1]/S, y0 + rows[-1]/S
    line = f"  {label}: x {fx0:.1f}..{fx1:.1f}  y {fy0:.1f}..{fy1:.1f}"
    if target: line += f"   d=({fx0-target[0]:+.1f},{fy0-target[1]:+.1f},{fx1-target[2]:+.1f},{fy1-target[3]:+.1f})"
    print(line)
    return (fx0, fy0, fx1, fy1)

def basel(mask, x0, x1, y0, y1, label, target):
    m = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    counts = m.sum(axis=1); mx = counts.max()
    heavy = np.where(counts >= 0.5 * mx)[0]
    bl = y0 + heavy[-1] / S
    print(f"  {label}: baseline {bl:.1f} (target {target}, d {bl-target:+.1f})")

print("== TITLE =="); bbox(red, 100, 900, 60, 135, "ink", (180, 87, 778, 120)); basel(red, 180, 778, 85, 125, "bl", 113.5)
print("== CONTENT BOX =="); bbox(peri, 60, 920, 120, 380, "border", (98, 133, 887, 367))
print("== BODY (navy) ==")
bbox(navy, 95, 890, 134, 172, "L1", (109, 142, 677, 160)); basel(navy, 109, 663, 140, 168, "bl", 159.5)
bbox(navy, 95, 890, 182, 216, "L2", (109, 195, 239, 211)); basel(navy, 109, 236, 194, 218, "bl", 211.5)
bbox(navy, 95, 890, 218, 244, "L3a", (108, 220, 759, 242)); basel(navy, 108, 742, 222, 245, "bl", 237.5)
bbox(navy, 95, 890, 246, 275, "L3b", (109, 246, 486, 268)); basel(navy, 109, 472, 248, 271, "bl", 263.5)
print("== BULLETS ==")
bbox(red, 90, 700, 292, 330, "b1", (135, 302, 468, 323))
bbox(red, 90, 700, 334, 364, "b2", (134, 341, 480, 357))
print("== LABEL ==")
bbox(navy, 382, 602, 438, 473, "text", (388, 445, 596, 464))
bbox(peri, 360, 640, 425, 486, "box", (377, 435, 608, 477))
print("== MATRIX ==")
bbox(darkred, 600, 870, 375, 515, "box", (623, 386, 843, 504))
bbox(dark, 626, 850, 390, 500, "ink band", (634, 397, 833, 494))
bbox(dark, 626, 646, 390, 500, "L bracket", (634, 397, 643, 494))
bbox(dark, 822, 850, 390, 500, "R bracket", (824, 397, 833, 494))
for lbl, tx0, tx1, ty0, ty1, tgt in [
    ("r1c1", 646, 700, 394, 428, (647, 401, 676, 423)), ("r1c2", 712, 760, 394, 428, (718, 401, 747, 423)),
    ("r1c3", 782, 822, 394, 428, (789, 401, 819, 423)), ("r2c1", 646, 700, 429, 461, (647, 434, 676, 456)),
    ("r2c2", 712, 760, 429, 461, (718, 434, 747, 456)), ("r2c3", 782, 822, 429, 461, (789, 434, 819, 456)),
    ("r3c1", 646, 700, 462, 496, (647, 467, 676, 489)), ("r3c2", 712, 760, 462, 496, (718, 467, 747, 489)),
    ("r3c3", 782, 822, 462, 496, (789, 467, 819, 489))]:
    bbox(dark, tx0, tx1, ty0, ty1, f"theta {lbl}", tgt)
print("== BLACK BAR ==")
bb = (R < 90) & (G < 90) & (B < 90)
bbox(bb, 0, 960, 505, 540, "bar", (38, 518, 921, 537.5))
print("== EQ INK EXIST + DELIMITERS ==")
ok = True
for i, (cx, cy) in enumerate([(cx, cy) for cy in (401, 434, 467) for cx in (647, 718, 789)]):
    m = dark[int((cy-6)*S):int((cy+28)*S), int((cx-4)*S):int((cx+34)*S)]
    n = int(m.sum())
    if n < 30: ok = False
print("  9 regions ink:", "PASS" if ok else "FAIL")
lb = bbox(dark, 626, 646, 390, 500, "Lbr")
tb = bbox(dark, 646, 822, 390, 500, "thetas")
print(f"  delimiter covers enclosed ink: {lb[1] <= tb[1]+1 and lb[3] >= tb[3]-1}; clearance {tb[0]-lb[2]:.1f}px")
