#!/usr/bin/env python3
# g1_subtitle.py — settle the subtitle gap. m2's title scan (fy 48..100, red mask)
# reported nothing below fy 76 and its subtitle scan (fy 100..130) found only the
# matrix-header row (fy 118..129) — so band fy 77..99 was never measured for ANY
# color, yet the frame visibly shows a subtitle line there. This script:
#   1. any-ink scan of fy 74..120 -> exact subtitle band(s)
#   2. per-band color-run segmentation (red runs / blue runs, x-projection, gap>=6)
#      with each run's median core color -> the two-tone split, with pixel proof
#   3. saves a 3x crop of the band for visual transcription (crop_subtitle.png)
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_016.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

dev = np.abs(a - np.array([233, 233, 231])).max(axis=2)
ink = dev > 55

print("=== per-row ink fy 74..120 (fx 60..900) ===")
band_rows = []
for fy in range(74, 121):
    n = int(ink[fy, 60:901].sum())
    if n >= 3:
        xs_ = np.nonzero(ink[fy, 60:901])[0] + 60
        band_rows.append(fy)
        print(f"  fy {fy}: ink {n:4d} fx {int(xs_.min())}..{int(xs_.max())}")

if not band_rows:
    print("NO ink rows found in fy 74..120 -> subtitle genuinely ABSENT from frame")
else:
    # merge into bands (gap tolerance 3)
    bands = []
    cur = [band_rows[0], band_rows[0]]
    for fy in band_rows[1:]:
        if fy - cur[1] <= 3:
            cur[1] = fy
        else:
            bands.append(cur); cur = [fy, fy]
    bands.append(cur)
    y0, y1 = bands[0]
    print(f"subtitle band: fy {y0}..{y1}")
    sub = slice(y0, y1 + 1)
    redm = (R - (G + B) / 2 > 45) & (R > 100)
    bluem = (B - (R + G) / 2 > 30) & (B > 100)
    for nm, m in (("RED", redm), ("BLUE", bluem)):
        colmask = m[sub, :].any(axis=0)
        colmask[:60] = False; colmask[901:] = False
        runs = []
        inrun = False
        for x in range(W):
            if colmask[x] and not inrun:
                s = x; inrun = True
            elif not colmask[x] and inrun:
                if x - 1 - s >= 1:
                    runs.append((s, x - 1))
                inrun = False
        # merge runs with gap <= 6
        merged = []
        for s, e in runs:
            if merged and s - merged[-1][1] <= 6:
                merged[-1][1] = e
            else:
                merged.append([s, e])
        print(f"--- subtitle {nm} runs (x-projection, gap<=6 merged): {len(merged)}")
        for s, e in merged:
            msub = m[sub, s:e + 1]
            px = a[sub, s:e + 1][msub]
            med = np.median(px, axis=0).astype(int)
            # most saturated core: top 25 by |score|
            if nm == "RED":
                score = px[:, 0] - (px[:, 1] + px[:, 2]) / 2
            else:
                score = px[:, 2] - (px[:, 0] + px[:, 1]) / 2
            idx = np.argsort(-score)[:max(1, len(score) // 4)]
            core = np.median(px[idx], axis=0).astype(int)
            print(f"    run fx {s:3d}..{e:3d} w{e - s + 1:3d}  median #{med[0]:02X}{med[1]:02X}{med[2]:02X}  sat-core #{core[0]:02X}{core[1]:02X}{core[2]:02X}  n={int(msub.sum())}")

# crop for visual read
crop = im.crop((95, 74, 870, 106)).resize((775 * 3, 32 * 3), Image.LANCZOS)
crop.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide016/crop_subtitle.png")
print("(saved crop_subtitle.png: fx 95..870, fy 74..106, 3x)")
