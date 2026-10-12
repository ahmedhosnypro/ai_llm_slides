#!/usr/bin/env python3
"""Slide 043 probe E: x615 line full-height check; Batch-size label hunt; left-stack crop."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("=== 1. x615 vertical extent (pale pink line?) ===")
pale = (r > 150) & (r - g > 18) & (r - b > 10) & (g < 215) & (b < 215)
ys = [y for y in range(40, 540) if pale[y, 614] or pale[y, 615] or pale[y, 616]]
print("x614..616 pale rows:", ys[:5], "...", ys[-5:] if ys else [], "count:", len(ys))
print("samples:", [tuple(a[y, 615]) for y in ys[:: max(1, len(ys)//6)]][:8] if ys else None)
# compare with 042's I-beam: full-height thin line
print("=== 2. fine map x836..900 y200..300 pale (step 1) ===")
print("      " + "".join(str((x // 10) % 10) for x in range(836, 900)))
for y in range(200, 302):
    row = "".join("X" if pale[y, x] else "." for x in range(836, 900))
    if "X" in row: print(f"y{y:4d} {row}")

print("=== 3. Batch-size label: red-core clusters x836..900, y200..260 ===")
redc = (r > 130) & (r - g > 50) & (r - b > 40) & (g < b + 35)
for y in range(200, 262):
    xs = np.where(redc[y, 836:900])[0]
    if len(xs): print(f"  y{y}: x {xs.min()+836}..{xs.max()+836} n={len(xs)}")

print("=== 4. LEFT STACK crop for vision (x100..330, y88..350, 2.5x) ===")
crop = im.crop((100, 88, 330, 350))
crop = crop.resize((int(230 * 2.5), int(262 * 2.5)), Image.LANCZOS)
crop.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide043/crop43_leftstack_worker.png")
print("saved crop43_leftstack_worker.png", crop.size)

print("=== 5. d-arrow + label crop for vision (x780..905, y210..340, 3x) ===")
crop2 = im.crop((780, 210, 905, 340))
crop2 = crop2.resize((125 * 3, 130 * 3), Image.LANCZOS)
crop2.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide043/crop43_darrow_worker.png")
print("saved crop43_darrow_worker.png", crop2.size)

print("=== 6. pencil crop for vision (x335..415, y225..270, 4x) ===")
crop3 = im.crop((335, 225, 415, 270))
crop3 = crop3.resize((80 * 4, 45 * 4), Image.LANCZOS)
crop3.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide043/crop43_pencil_worker.png")
print("saved crop43_pencil_worker.png", crop3.size)
