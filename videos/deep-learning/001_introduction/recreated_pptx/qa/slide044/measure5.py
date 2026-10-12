#!/usr/bin/env python3
"""measure5.py — pass 5: verification crops (bullet, grids, notebox, title),
exact per-cell fill maps, remaining colors, note/bullet font solving."""
from PIL import Image, ImageFont
import numpy as np

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
IMG = f"{BASE}/unique_slides/slide_044.jpg"
QA = f"{BASE}/recreated_pptx/qa/slide044"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)

# --- crops for visual verification ---
def crop(x0, y0, x1, y1, scale, name):
    c = im.crop((x0, y0, x1 + 1, y1 + 1))
    c = c.resize((c.width * scale, c.height * scale), Image.NEAREST)
    c.save(f"{QA}/{name}.png")
    print(f"saved {name}.png {c.size}")

crop(100, 126, 880, 162, 3, "crop_bullet")
crop(95, 165, 385, 390, 2, "crop_g77")
crop(432, 240, 535, 320, 4, "crop_f33")
crop(615, 195, 827, 362, 2, "crop_o55")
crop(70, 380, 690, 520, 2, "crop_notebox")
crop(200, 60, 765, 110, 2, "crop_title")
crop(390, 260, 630, 300, 4, "crop_operators")

# --- exact per-cell fill classification (7x7 and o55 and f33) ---
def classify(px):
    r, g, b = px
    if b > 180 and g > 140 and r < 100: return "C"  # cyan
    if g > 150 and r < 120 and b < 140: return "G"  # green
    if r > 200 and g > 200 and b < 140: return "Y"  # yellow
    if r > 240 and g > 240 and b > 240: return "w"  # white
    return "?"

def cell_fills(x0, y0, n, m, cw, ch, label):
    print(f"{label} fills:")
    for r in range(m):
        row = ""
        for c in range(n):
            cx = int(x0 + c * cw + cw / 2)
            cy = int(y0 + r * ch + ch / 2)
            # sample 5x5 patch mode
            patch = a[cy - 2:cy + 3, cx - 2:cx + 3].reshape(-1, 3)
            med = np.median(patch, axis=0)
            row += classify(med)
        print(f"  r{r+1}: {row}")

cell_fills(101, 173, 7, 7, 277 / 7, 210 / 7, "7x7")
cell_fills(440, 247, 3, 3, 87 / 3, 66 / 3, "3x3")
cell_fills(622, 203, 5, 5, 198 / 5, 151 / 5, "5x5")

# --- exact colors ---
def exact_modal(x0, x1, y0, y1, n=4):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    return [(tuple(int(c) for c in vals[i]), int(counts[i])) for i in order]

print("yellow (f33 r1c1 empty corner):", exact_modal(443, 458, 250, 258))
print("yellow (f33 r3c3):", exact_modal(505, 520, 300, 308))
print("bullet ring px:", [tuple(a[y, x]) for y in [141, 145, 149] for x in [112, 117, 123]])
# bullet circle: non-white pixels
sub = a[138:154, 108:128]
nz = [(tuple(px)) for px in sub.reshape(-1, 3) if not (px[0] > 235 and px[1] > 235 and px[2] > 235)]
print("bullet circle nonwhite count:", len(nz), "sample:", nz[:12])
print("note navy bold stems (L1 'O' at x88..101):", exact_modal(88, 102, 407, 420, 5))
print("gridline darkest on 7x7 vertical between c2/c3 (x~180, y 175..200):",
      sorted([tuple(a[y, x]) for y in range(175, 200) for x in range(178, 184)], key=lambda p: sum(p))[:5])
print("gridline darkest horizontal (y~233, x 105..135):",
      sorted([tuple(a[y, x]) for y in range(231, 236) for x in range(105, 136)], key=lambda p: sum(p))[:5])
print("o55 gridline darkest:", sorted([tuple(a[y, x]) for y in range(229, 236) for x in range(640, 700)], key=lambda p: sum(p))[:5])
print("cyan exact (big patch r1c2..c4):", exact_modal(150, 300, 176, 200, 3))
print("green exact (big patch r4c2..c4):", exact_modal(150, 300, 268, 290, 3))
print("out green exact (o55 r2):", exact_modal(630, 810, 236, 260, 3))

# --- font solving: note lines ---
L1 = "Original 5x5"
L2 = "After padding ONE  pixel (surrounding the image) it will be 7x7"
L3 = "After apply one filter  of size 3x3, output will be 5x5 again"
L4 = "Do the same for next applied filter"
targets = [198 - 88 + 1, 632 - 89 + 1, 589 - 90 + 1, 374 - 88 + 1]
for text, tgt in zip([L1, L2, L3, L4], targets):
    for name, path, bold in [("LibSerif", "/usr/share/fonts/TTF/LiberationSerif-Regular.ttf", False),
                             ("LibSerif-B", "/usr/share/fonts/TTF/LiberationSerif-Bold.ttf", True),
                             ("LibSans", "/usr/share/fonts/TTF/LiberationSans-Regular.ttf", False),
                             ("LibSans-B", "/usr/share/fonts/TTF/LiberationSans-Bold.ttf", True),
                             ("DejaVuSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", False),
                             ("DejaVuSerif-B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", True)]:
        try:
            best = None
            for size10 in range(140, 300):
                size = size10 / 10
                f = ImageFont.truetype(path, int(round(size * 4)))  # 4x for precision
                w = f.getlength(text) / 4
                if best is None or abs(w - tgt) < best[1]:
                    best = (size, abs(w - tgt), w)
            print(f"L '{text[:22]}...' tgt {tgt}: {name} best size {best[0]} (w {best[2]:.0f}, off {best[1]:.0f})")
        except OSError:
            print(name, "missing")

# --- font solving: bullet sans segments ---
segs = [("For", 31), ("surround", 89), ("the", 32), ("image", 58), ("with", 43), ("layers", 50), ("of", 20)]
for text, tgt in segs:
    for name, path in [("LibSans", "/usr/share/fonts/TTF/LiberationSans-Regular.ttf"),
                       ("LibSans-B", "/usr/share/fonts/TTF/LiberationSans-Bold.ttf")]:
        best = None
        for size10 in range(140, 300):
            size = size10 / 10
            f = ImageFont.truetype(path, int(round(size * 4)))
            w = f.getlength(text) / 4
            if best is None or abs(w - tgt) < best[1]:
                best = (size, abs(w - tgt), w)
        print(f"bullet '{text}' tgt {tgt}: {name} best {best[0]} (w {best[2]:.0f}, off {best[1]:.0f})")
