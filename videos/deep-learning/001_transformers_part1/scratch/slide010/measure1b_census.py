#!/usr/bin/env python3
"""Pass 1 (slide010): full-frame color census — find the dominant fill colors.

JPEG-core data-driven: quantize (round to /8), count, report biggest connected
regions per dominant non-gray color. Frame px (960x540, 1px=1pt).
"""
from PIL import Image
import numpy as np
from scipy import ndimage
from collections import Counter

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_010.jpg"
a = np.asarray(Image.open(IM).convert("RGB"), dtype=np.int16)
H, W = a.shape[:2]

q = (a // 8 * 8).astype(np.int32)
key = q[:, :, 0] * 65536 + q[:, :, 1] * 256 + q[:, :, 2]
cnt = Counter(key.ravel().tolist())
print("top 25 quantized colors (count, hex):")
for k, c in cnt.most_common(25):
    print(f"  {c:7d}  #{k >> 16:02x}{(k >> 8) & 255:02x}{k & 255:02x}")

def comps_for(lo, hi, min_area=400, top=10):
    m = ((a[:, :, 0] >= lo[0]) & (a[:, :, 0] <= hi[0]) &
         (a[:, :, 1] >= lo[1]) & (a[:, :, 1] <= hi[1]) &
         (a[:, :, 2] >= lo[2]) & (a[:, :, 2] <= hi[2]))
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    out = []
    for i, sl in enumerate(objs):
        ys, xs = sl
        area = int((lab[sl] == i + 1).sum())
        if area >= min_area:
            reg = a[sl]
            rm = lab[sl] == i + 1
            core = tuple(int(np.median(reg[..., c][rm])) for c in range(3))
            out.append((area, xs.start, ys.start, xs.stop - 1, ys.stop - 1, core))
    out.sort(reverse=True)
    print(f"--- band {lo}..{hi}: {len(out)} comps")
    for area, x0, y0, x1, y1, core in out[:top]:
        print(f"    area={area:6d} x{x0}..{x1} y{y0}..{y1} (w{x1-x0+1} h{y1-y0+1}) core={core}")

print("\n== yellow/green family (decoder) ==")
comps_for((200, 200, 40), (255, 255, 160), 300)
print("\n== green family (cells/callout) ==")
comps_for((150, 200, 150), (230, 255, 230), 300)
print("\n== orange/peach family (encoder) ==")
comps_for((235, 170, 110), (255, 235, 210), 300)
print("\n== pink family ==")
comps_for((230, 150, 170), (255, 225, 235), 300)
print("\n== lavender family ==")
comps_for((190, 190, 220), (240, 240, 255), 300)
print("\n== magenta/pink-ink family (dashed curves?) ==")
comps_for((200, 60, 130), (255, 170, 210), 30)
print("\n== red ink family ==")
comps_for((120, 0, 0), (220, 60, 60), 30, 25)
