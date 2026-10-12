from PIL import Image
import numpy as np
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg"
im = np.array(Image.open(FR).convert("RGB")).astype(int)

print("== L2 red ink columns (rows 138..162) ==")
band = im[138:163, 600:940]
r,g,b = band[:,:,0],band[:,:,1],band[:,:,2]
red = (r>g+40)&(r>90)&(b<120)
cols = np.where(red.any(axis=0))[0]+600
if len(cols):
    words=[];s=cols[0];p=cols[0]
    for c in cols[1:]:
        if c-p>5: words.append((s,p)); s=c
        p=c
    words.append((s,p))
    print(f"  red word groups: {words}")
    print(f"  red extent: {cols[0]}..{cols[-1]}")
rows = np.where(red.any(axis=1))[0]+138
print(f"  red rows: {rows[0]}..{rows[-1]}")

print("\n== L2 full dark ink extent (rows 138..162, black+colored) ==")
band2 = im[138:163, 88:940]
dark = band2.mean(axis=2)<160
cols2 = np.where(dark.any(axis=0))[0]+88
print(f"  L2 ink extent: {cols2[0]}..{cols2[-1]}")

print("\n== underline stroke y=157 vs red text ==")
print(f"  stroke 663..828; red text {cols[0]}..{cols[-1]}" if len(cols) else "no red")

print("\n== eq3/eq4 math ink vertical extent inside boxes (containment pre-check) ==")
# eq3 box frame x 164..287, y 399..446: math ink = dark pixels excluding box strokes/highlights
reg = im[400:446, 166:286]
darkm = reg.mean(axis=2)<170
rr = np.where(darkm.any(axis=1))[0]+400
cc = np.where(darkm.any(axis=0))[0]+166
print(f"  eq3 math ink: y {rr[0]}..{rr[-1]} x {cc[0]}..{cc[-1]} (box y399..446 x164..287)")
reg = im[452:475, 166:370]
darkm = reg.mean(axis=2)<170
rr = np.where(darkm.any(axis=1))[0]+452
cc = np.where(darkm.any(axis=0))[0]+166
print(f"  eq4 math ink: y {rr[0]}..{rr[-1]} x {cc[0]}..{cc[-1]} (box y451..475 x164..371)")

print("\n== intro box borders exact (frame) ==")
# left border col, right border col, top row, bottom row
for x in range(84,96):
    col = im[104:186, x]
    n = (col.mean(axis=1)<200).sum()
    if n>60: print(f"  left border col x={x} (n={n})")
for x in range(886,898):
    col = im[104:186, x]
    n = (col.mean(axis=1)<200).sum()
    if n>60: print(f"  right border col x={x} (n={n})")
for y in range(100,110):
    row = im[y, 88:893]
    n = (row.mean(axis=1)<200).sum()
    if n>600: print(f"  top border row y={y} (n={n})")
for y in range(182,190):
    row = im[y, 88:893]
    n = (row.mean(axis=1)<200).sum()
    if n>600: print(f"  bottom border row y={y} (n={n})")
