#!/usr/bin/env python3
"""measure6: ASCII maps for the last unknowns (8 vs 33 where useful)."""
from PIL import Image
import numpy as np

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning"
f8 = np.asarray(Image.open(f"{ROOT}/002_transformers_part2/scratch/slide008/frame8_remapped_960x540.png").convert("RGB")).astype(int)
f33 = np.asarray(Image.open(f"{ROOT}/001_transformers_part1/unique_slides/slide_033.jpg").convert("RGB")).astype(int)

def amap(img, x0, x1, y0, y1, test, step=2, tag=""):
    print(f"  {tag} cols {x0}..{x1} step {step}:")
    hdr = "     "
    for x in range(x0, x1, step):
        hdr += str((x // 10) % 10)
    print(hdr)
    for y in range(y0, y1, step):
        line = ""
        for x in range(x0, x1, step):
            line += "#" if test(img[y, x]) else "."
        print(f"{y:4d} " + line)

peach = lambda p: abs(p[0] - 247) < 14 and abs(p[1] - 226) < 14 and abs(p[2] - 205) < 14
notpeach = lambda p: not peach(p)
reddish = lambda p: p[0] - p[1] > 40 and p[0] > 105

print("=== QUERY REGION reddish map (8): x262..336 y356..448 step 2 ===")
amap(f8, 262, 336, 356, 448, reddish, 2, "8 reddish")

print("\n=== QUERY REGION notpeach map (8): x262..340 y426..492 step 2 ===")
amap(f8, 262, 340, 426, 492, notpeach, 2, "8 notpeach")

print("\n=== W_q box bottom / X2->Wq arrow zone reddish (8): x296..322 y446..486 ===")
amap(f8, 296, 322, 446, 486, reddish, 2, "8 reddish")

print("\n=== W_v box1 notpeach (8): x700..750 y228..266 step 2 ===")
amap(f8, 700, 750, 228, 266, notpeach, 2, "8")
print("--- 33 ---")
amap(f33, 700, 750, 228, 266, notpeach, 2, "33")

print("\n=== W_k box1 x-extent: darkgreen col profile y238..258 x148..210 ===")
r, g, b = f8[:,:,0], f8[:,:,1], f8[:,:,2]
dkg = (g - r > 25) & (abs(r - 120) < 50) & (abs(g - 178) < 50) & (abs(b - 120) < 50)
cols = dkg[238:259, 148:210].sum(axis=0)
print("  cols>3:", {148 + i: int(v) for i, v in enumerate(cols) if v > 3})

print("\n=== W_k text darkest in box1 (x162..194 y240..258): 8 vs 33 ===")
reg8 = f8[240:258, 162:194].reshape(-1, 3)
dk8 = reg8[reg8.sum(axis=1).argmin()]
reg33 = f33[240:258, 162:194].reshape(-1, 3)
dk33 = reg33[reg8.sum(axis=1).argmin()]
print("  8 darkest:", tuple(int(v) for v in dk8), "  33 darkest:", tuple(int(v) for v in dk33))

print("\n=== K vector row1 notpeach (8): x196..246 y226..256 step 2 ===")
amap(f8, 196, 246, 226, 256, notpeach, 2, "8")
print("--- 33 ---")
amap(f33, 196, 246, 226, 256, notpeach, 2, "33")

print("\n=== V vector row1 notpeach (8): x660..706 y226..256 step 2 ===")
amap(f8, 660, 706, 226, 256, notpeach, 2, "8")

print("\n=== sentence row notpeach (8): x176..480 y468..522 step 4 ===")
amap(f8, 176, 480, 468, 522, notpeach, 4, "8")

print("\n=== legend region notpeach (8): x730..915 y460..535 step 4 ===")
amap(f8, 730, 915, 460, 535, notpeach, 4, "8")

print("\n=== legend border samples (8) ===")
for (x, y) in [(737, 470), (737, 500), (800, 468), (860, 468), (899, 490), (800, 532)]:
    print(f"  ({x},{y}):", tuple(int(v) for v in f8[y, x]), "  33:", tuple(int(v) for v in f33[y, x]))

print("\n=== blue circle alpha over clean peach (8): samples ===")
for (x, y) in [(330, 415), (340, 430), (320, 405), (262, 440)]:
    obs = f8[y, x]; bg = f33[y, x]
    a_r = (bg[0] - obs[0]) / (bg[0] - 65)
    a_b = (obs[2] - bg[2]) / (225 - bg[2]) if abs(225 - bg[2]) > 40 else float('nan')
    print(f"  ({x},{y}): obs={tuple(int(v) for v in obs)} bg={tuple(int(v) for v in bg)} a_r={a_r:.2f} a_b={a_b:.2f}")

print("\n=== X2 widget cells: notpeach map x250..340 y476..514 step 2 (8) ===")
amap(f8, 250, 340, 476, 514, notpeach, 2, "8")

print("\n=== container->W_k gap arrows: reddish map x140..164 y230..395 step 3 (8) ===")
amap(f8, 140, 164, 230, 395, reddish, 3, "8")

print("\n=== right container->W_v gap: reddish map x736..768 y230..395 step 3 (8) ===")
amap(f8, 736, 768, 230, 395, reddish, 3, "8")
