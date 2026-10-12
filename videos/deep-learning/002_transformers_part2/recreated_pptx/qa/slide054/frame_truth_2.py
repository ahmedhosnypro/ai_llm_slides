#!/usr/bin/env python3
"""Frame-truth PIL pass for slide 054 (settles contradictory vision reads).
Original frame: unique_slides/slide_054.jpg (960x540, 1px = 1pt)."""
from PIL import Image
import numpy as np
from collections import Counter

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_054.jpg"
A = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = A.shape
print("frame", W, "x", H)

def region(x0, y0, x1, y1, label):
    sub = A[y0:y1, x0:x1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    print(f"\n== {label} frame[{x0},{y0},{x1},{y1}] ({x1-x0}x{y1-y0})")
    # darkest ink pixels (text) vs fill
    lum = 0.299*r + 0.587*g + 0.114*b
    ink = sub[lum < 140]
    if len(ink):
        print(f"  dark-ink n={len(ink)} mean RGB=({ink[:,0].mean():.0f},{ink[:,1].mean():.0f},{ink[:,2].mean():.0f})")
        # classify ink hue
        rr, gg, bb = ink[:,0].mean(), ink[:,1].mean(), ink[:,2].mean()
        if bb - rr > 40: print("  -> ink reads BLUE/PURPLE" + (" (purple: r>g)" if rr > gg else " (blue)"))
        elif rr - gg > 40 and rr - bb > 40: print("  -> ink reads RED")
        elif rr - bb > 40 and gg - bb > 20: print("  -> ink reads BROWN/ORANGE")
        else: print(f"  -> ink reads DARK/NEUTRAL (r{rr:.0f} g{gg:.0f} b{bb:.0f})")
    else:
        print("  no dark ink")
    fill = sub[(lum >= 160) & (lum <= 245)]
    if len(fill):
        c = Counter(map(tuple, fill[::3]))
        top = c.most_common(3)
        print("  mid-lum fill top colors:", [(f"#{t[0][0]:02X}{t[0][1]:02X}{t[0][2]:02X}", t[1]) for t in top])

# 1. Softmax rotated text (build says purple 7030A0; C5 said red)
region(514, 240, 532, 288, "softmax rotated text")
# 2. Scaling rotated text (build says dark red)
region(386, 240, 410, 360, "scaling rotated text")
# 3. Mask label (build says green 23844D)
region(464, 192, 478, 228, "mask label text")
# 4. Similarity pill text (build says navy 333366; C6 said red)
region(284, 160, 342, 176, "similarity pill text")
# 5. Mask cells text + fill (build: pale yellow fill, black text; C5: pale-green fill dark-red text)
region(459, 233, 478, 245, "mask cell 1 (-inf)")
# 6. K strip row 1: vertical color profile x 216..245 at cy 236.5 -> show column colors
print("\n== K strip row1 x-profile (frame y 233..240, x 216..246) ==")
sub = A[233:240, 216:246]
prev = None
for x in range(sub.shape[1]):
    col = sub[:, x]
    m = col.mean(axis=0).astype(int)
    c = f"#{m[0]:02X}{m[1]:02X}{m[2]:02X}"
    # quantize
    r, g, b = m
    if r >= 200 and g >= 200 and b < 160: q = "YELLOW"
    elif r >= 215 and g >= 215 and b >= 200: q = "WHITE"
    elif abs(r-238) < 25 and abs(g-240) < 25 and abs(b-245) < 25: q = "LAVENDER"
    elif r < 150 and g < 150 and b < 150: q = "DARK"
    elif g - r > 15 and g - b > 15: q = "GREEN"
    elif r - b > 30 and r - g > 30: q = "RED"
    else: q = f"other"
    if q != prev:
        print(f"  frame x={216+x}: {q} ({c})")
        prev = q
# 7. Left container row 1 x-profile: x 84..153 at ry 231..245
print("\n== left container row1 x-profile (frame y 233..243, x 84..154) ==")
sub = A[233:243, 84:154]
prev = None
for x in range(sub.shape[1]):
    col = sub[:, x]
    m = col.mean(axis=0).astype(int)
    c = f"#{m[0]:02X}{m[1]:02X}{m[2]:02X}"
    r, g, b = m
    lum = 0.299*r + 0.587*g + 0.114*b
    if r >= 200 and g >= 200 and b < 160: q = "YELLOW"
    elif lum < 140: q = "DARK-INK"
    elif abs(r-238) < 30 and abs(g-240) < 30 and abs(b-245) < 30: q = "LAVENDER"
    elif g - r > 15 and g - b > 15: q = "GREEN"
    elif r - g > 40 and r - b > 40: q = "RED"
    elif r >= 225 and g >= 225 and b >= 210: q = "WHITE"
    else: q = "other"
    if q != prev:
        print(f"  frame x={84+x}: {q} ({c})")
        prev = q
# 8. red arrow below bottom container: shape (up vs up-right) — ink bbox rows 489..508, x 270..305
print("\n== red arrow below bottom container: per-row ink spans (x 265..310, y 486..510) ==")
sub = A[486:510, 265:310]
r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
red = (r - g >= 60) & (r - b >= 50) & (r >= 140)
for yy in range(sub.shape[0]):
    xs = np.where(red[yy])[0]
    if len(xs):
        print(f"  frame y={486+yy}: x {265+xs.min()}..{265+xs.max()} (n={len(xs)})")
