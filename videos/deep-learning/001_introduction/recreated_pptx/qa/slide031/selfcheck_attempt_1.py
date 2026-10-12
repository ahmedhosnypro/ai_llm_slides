"""Slide 031 attempt-1 closed-loop self-check: PIL-compare the 150dpi render against the
original frame's measured geometry. Scale: render 2001x1125 for a 960x540 frame -> frame_pt
= render_px * 960/2000 (1 frame px = 1 pt). Banked as selfcheck_attempt_1.py."""
from PIL import Image
import numpy as np
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide031/render_1.png"
im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
S = W / 960.0  # render px per frame px
print(f"render {W}x{H}, scale {S:.4f} render-px per frame-px")
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def to_frame(v): return v / S

# masks in render space
darkred = (R > 100) & (R - G > 50) & (R - B > 40)
blueish = (B - R > 35) & (B > 140)
peri = (B - R > 8) & (B - G > 8) & (B > 150) & (R < 235) & (G < 235)
dark = (R < 110) & (G < 110) & (B < 110)

def bbox(mask, x0, x1, y0, y1, label, target=None):
    m = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    rows = np.where(m.any(axis=1))[0]; cols = np.where(m.any(axis=0))[0]
    if not len(rows):
        print(f"  {label}: EMPTY in region"); return None
    fx0, fy0 = x0 + cols[0]/S, y0 + rows[0]/S
    fx1, fy1 = x0 + cols[-1]/S, y0 + rows[-1]/S
    line = f"  {label}: x {fx0:.1f}..{fx1:.1f}  y {fy0:.1f}..{fy1:.1f} (frame px)"
    if target: line += f"   target {target}   d=({fx0-target[0]:+.1f},{fy0-target[1]:+.1f},{fx1-target[2]:+.1f},{fy1-target[3]:+.1f})"
    print(line)
    return (fx0, fy0, fx1, fy1)

print("== TITLE (target ink x180..778 y87..120) ==")
bbox(darkred, 100, 900, 60, 135, "title red ink", (180, 87, 778, 120))

print("== CONTENT BOX (target x98..887 y133..367) ==")
bbox(peri, 60, 920, 120, 380, "peri border", (98, 133, 887, 367))

print("== BODY LINES (targets: L1 x109 y142..160 | L2 x109 y195..211 | L3a x108 y220..242 | L3b x109 y246..268) ==")
bbox(blueish, 90, 900, 136, 172, "L1", (109, 142, 677, 160))
bbox(blueish, 90, 900, 185, 218, "L2", (109, 195, 239, 211))
bbox(blueish, 90, 900, 216, 244, "L3a", (108, 220, 759, 242))
bbox(blueish, 90, 900, 244, 272, "L3b", (109, 246, 486, 268))

print("== BULLETS (targets: b1 dot+text x135..468 y302..323 | b2 x134..480 y341..357) ==")
bbox(darkred, 90, 700, 292, 330, "bullet1", (135, 302, 468, 323))
bbox(darkred, 90, 700, 334, 364, "bullet2", (134, 341, 480, 357))

print("== LABEL (target text ink x388..596 y445..464; box x377..608 y435..477) ==")
bbox(blueish, 360, 640, 440, 470, "label text", (388, 445, 596, 464))
bbox(peri, 360, 640, 425, 486, "label box", (377, 435, 608, 477))

print("== MATRIX BOX (target x623..843 y386..504) ==")
bbox(darkred, 600, 870, 375, 515, "matrix box red", (623, 386, 843, 504))

print("== MATRIX INK (targets: brackets x634..643/824..833 y397..494; thetas rows 401..423/434..456/467..489, cols 647..676/718..747/789..819) ==")
bbox(dark, 626, 850, 390, 500, "all matrix ink", (634, 397, 833, 494))
# per-element: left bracket
bbox(dark, 626, 646, 390, 500, "L bracket", (634, 397, 643, 494))
bbox(dark, 822, 850, 390, 500, "R bracket", (824, 397, 833, 494))
bbox(dark, 646, 700, 394, 428, "theta r1c1", (647, 401, 676, 423))
bbox(dark, 646, 700, 429, 461, "theta r2c1", (647, 434, 676, 456))
bbox(dark, 646, 700, 462, 496, "theta r3c1", (647, 467, 676, 489))
bbox(dark, 712, 760, 394, 428, "theta r1c2", (718, 401, 747, 423))
bbox(dark, 782, 822, 394, 428, "theta r1c3", (789, 401, 819, 423))
bbox(dark, 782, 822, 462, 496, "theta r3c3", (789, 467, 819, 489))

print("== BLACK BAR (target x38..921 y518..537.5) ==")
bb = (R < 90) & (G < 90) & (B < 90)
bbox(bb, 0, 960, 505, 540, "black bar", (38, 518, 921, 537.5))

print("== EQUATION INK EXISTENCE (self-check 3: nonzero ink in all 9 entry regions) ==")
ok = True
for i, (cx, cy) in enumerate([(647, 401), (718, 401), (789, 401), (647, 434), (718, 434), (789, 434), (647, 467), (718, 467), (789, 467)]):
    m = dark[int((cy-6)*S):int((cy+28)*S), int((cx-4)*S):int((cx+34)*S)]
    n = int(m.sum())
    if n < 30: ok = False
    print(f"  theta{i+1} region ink px: {n}")
print("  EQUATIONS EXIST:", "PASS" if ok else "FAIL")

print("== DELIMITER GEOMETRY (self-check 4: bracket stroke extent vs enclosed ink) ==")
lb = bbox(dark, 626, 646, 390, 500, "L bracket")
tb = bbox(dark, 646, 822, 390, 500, "theta block")
if lb and tb:
    print(f"  bracket spans y {lb[1]:.1f}..{lb[3]:.1f}; enclosed ink y {tb[1]:.1f}..{tb[3]:.1f} -> covers: {lb[1] <= tb[1]+1 and lb[3] >= tb[3]-1}")
    clearance = tb[0] - lb[2]
    print(f"  L clearance bracket->text: {clearance:.1f} frame px (must be > 0)")
