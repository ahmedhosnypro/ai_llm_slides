#!/usr/bin/env python3
"""Fourth pass: box bottom edge, x58 line vs box border discrimination, strip colors."""
from PIL import Image
import numpy as np
from collections import Counter

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_008.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# reddish with lower threshold (catch JPEG-faded border)
reddish = (R - G > 45) & (R - B > 45) & (R > 110)

print("-- faint-red row counts rows 500..522 --")
for y in range(500, 523):
    xs = np.nonzero(reddish[y])[0]
    if len(xs) > 3:
        print(f"  y={y}: n={len(xs)} x {xs.min()}..{xs.max()}")

print("\n-- row 153 individual cols 56..76 (reddish) --")
print("  ", [x for x in range(56, 77) if reddish[153, x]])
print("-- row 510 individual cols 56..76 --")
print("  ", [x for x in range(56, 77) if reddish[510, x]])

print("\n-- strip x59..69: modal colors at y 200, 300, 400, 480 --")
for y in (200, 300, 400, 480):
    reg = a[y, 59:70].reshape(-1, 3)
    cnt = Counter(map(tuple, reg))
    print(f"  y={y}: {cnt.most_common(2)}")

print("\n-- white fill column extent at y=300 (cols 50..470) --")
white = (R > 240) & (G > 240) & (B > 240)
xs = np.nonzero(white[300, 50:470])[0] + 50
print(f"  white cols at y300: {xs.min()}..{xs.max()}")
xs = np.nonzero(white[470, 50:470])[0] + 50
print(f"  white cols at y470: {xs.min()}..{xs.max()}")

print("\n-- white fill row extent at x=300 (rows 140..530) --")
ys = np.nonzero(white[140:530, 300])[0] + 140
print(f"  white rows at x300: {ys.min()}..{ys.max()}")
ys = np.nonzero(white[140:530, 250])[0] + 140
print(f"  white rows at x250: {ys.min()}..{ys.max()}")

print("\n-- x58 line top/bottom detail: rows 42..50 and 505..520 at cols 56..60 --")
for y in list(range(42, 51)) + list(range(505, 521)):
    seg = "".join("R" if reddish[y, x] else "." for x in range(56, 61))
    print(f"  y={y}: {seg}  rgb(58)={tuple(a[y,58])}")

print("\n-- col 70 line detail rows 148..158 and 505..514 --")
for y in list(range(148, 159)) + list(range(505, 515)):
    seg = "".join("R" if reddish[y, x] else "." for x in range(68, 74))
    print(f"  y={y}: {seg}  rgb(70)={tuple(a[y,70])}")

print("\n-- box right border col 459..461 detail --")
for y in (153, 300, 505, 509, 510, 513):
    seg = "".join("R" if reddish[y, x] else "." for x in range(457, 463))
    print(f"  y={y}: {seg}")

print("\n-- x58 line: full extent recheck with reddish --")
ys = np.nonzero(reddish[:, 58])[0]
print(f"  col58 reddish y {ys.min()}..{ys.max()} n={len(ys)}")
ys = np.nonzero(reddish[:, 70])[0]
print(f"  col70 reddish y {ys.min()}..{ys.max()} n={len(ys)}")
ys = np.nonzero(reddish[:, 460])[0]
print(f"  col460 reddish y {ys.min()}..{ys.max()} n={len(ys)}")

print("\n-- top border row 152..156 x extent (reddish, excluding x58 line) --")
for y in range(151, 157):
    xs = np.nonzero(reddish[y, 62:470])[0] + 62
    if len(xs):
        print(f"  y={y}: x {xs.min()}..{xs.max()} n={len(xs)}")
