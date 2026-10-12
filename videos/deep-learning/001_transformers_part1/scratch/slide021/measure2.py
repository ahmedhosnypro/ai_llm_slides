#!/usr/bin/env python3
"""Word-blob measurement per line + color samples for slide_021.jpg."""
from PIL import Image
import numpy as np

im = Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_021.jpg"
).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (R > 140) & (G < 90) & (B < 90)
loose_red = ((R - G) > 55) & ((R - B) > 55)
blue = (B > 120) & (R < 110) & (G < 110)
loose_blue = ((B - R) > 45) & ((B - G) > 45)
dark = (R < 150) & (G < 150) & (B < 150)

def word_blobs(mask, y0, y1, x_from=72, x_to=888, gap=4):
    band = mask[y0:y1 + 1, x_from:x_to]
    cols = band.sum(axis=0) >= 1
    xs = np.where(cols)[0]
    if len(xs) == 0:
        return []
    blobs = []
    start = prev = xs[0]
    for x in xs[1:]:
        if x - prev > gap:
            blobs.append((start + x_from, prev + x_from))
            start = x
        prev = x
    blobs.append((start + x_from, prev + x_from))
    return blobs

def show(name, y0, y1, mask=None):
    m = (dark | loose_blue | loose_red) if mask is None else mask
    blobs = word_blobs(m, y0, y1)
    print(f"== {name} y{y0}..{y1}: {len(blobs)} blobs")
    print("   " + " ".join(f"{b[0]}-{b[1]}" for b in blobs))

# P1: header + 3 body lines
show("HDR1 red", 198, 220, loose_red)
show("P1-L1", 222, 243)
show("P1-L2", 245, 264)
show("P1-L3", 267, 286)
# P2
show("HDR2 red", 311, 332, loose_red)
show("P2-L1", 334, 355)
show("P2-L2", 358, 374)
# P3
show("P3-L1", 401, 422)
show("P3-L1 blue cols", 401, 422, loose_blue)
show("P3-L2", 424, 445)
show("P3-L2 blue cols", 424, 445, loose_blue)

# blue column extents inside P3 lines (excluding border cols x<75, x>870)
def blue_extent(y0, y1):
    band = loose_blue[y0:y1 + 1, 75:870]
    cols = np.where(band.sum(axis=0) >= 1)[0]
    if len(cols) == 0:
        print(f"  P3 y{y0}..{y1}: no blue")
        return
    # split into runs
    runs = []
    s = p = cols[0]
    for x in cols[1:]:
        if x - p > 4:
            runs.append((s + 75, p + 75))
            s = x
        p = x
    runs.append((s + 75, p + 75))
    print(f"  P3 y{y0}..{y1}: blue runs {runs}")

blue_extent(401, 422)
blue_extent(424, 445)

# color samples (median of masked pixels)
def sample(name, mask, region=None):
    if region is None:
        m, sub = mask, a
    else:
        y0, y1, x0, x1 = region
        m, sub = mask[y0:y1, x0:x1], a[y0:y1, x0:x1]
    if m.sum() == 0:
        print(f"  {name}: EMPTY")
        return
    px = sub[m]
    med = np.median(px, axis=0).astype(int)
    print(f"  {name}: n={m.sum()} median RGB={tuple(med)} hex=#{med[0]:02X}{med[1]:02X}{med[2]:02X}")

print("== colors ==")
sample("title red", red, (77, 110, 349, 638))
sample("subtitle red", red, (115, 140, 132, 857))
sample("hdr1 red", red, (201, 219, 80, 385))
sample("body black", dark, (224, 242, 80, 855))
sample("box border", blue, (170, 172, 200, 800))
sample("P3 blue term", loose_blue, (403, 421, 100, 300))
sample("badge ring", (B > 120) & (R < 150) & (G < 140), (50, 95, 870, 918))
