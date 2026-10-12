# stage 9: final micro-measurements
from PIL import Image
import numpy as np
from collections import Counter
im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)

def modal(x0,x1,y0,y1,n=6):
    reg = a[y0:y1, x0:x1].reshape(-1,3)
    return Counter(map(tuple, (reg//2*2))).most_common(n)

# box3 (green) edges: column scan x=500 y200..275
print("col x=500 y205..270:")
prev=None
for y in range(205,271):
    c = tuple(a[y,500]//16*16)
    if c != prev: print(f"  y={y}: {tuple(a[y,500])}")
    prev = c
print("row y=236 x430..470 (green left edge):")
prev=None
for x in range(430,471):
    c = tuple(a[236,x]//16*16)
    if c != prev: print(f"  x={x}: {tuple(a[236,x])}")
    prev = c
print("row y=236 x548..575 (green right edge):")
prev=None
for x in range(548,576):
    c = tuple(a[236,x]//16*16)
    if c != prev: print(f"  x={x}: {tuple(a[236,x])}")
    prev = c
# green border modal on top edge
print("green top border modal (x470..530, y206..210):", modal(470,530,206,210))

# box5 lavender border: left/right edges
print("\nrow y=240 x746..760 (lav left edge):")
prev=None
for x in range(746,761):
    c = tuple(a[240,x]//16*16)
    if c != prev: print(f"  x={x}: {tuple(a[240,x])}")
    prev = c
print("row y=240 x852..866 (lav right edge):")
prev=None
for x in range(852,867):
    c = tuple(a[240,x]//16*16)
    if c != prev: print(f"  x={x}: {tuple(a[240,x])}")
    prev = c
print("lav top edge modal (x770..840, y206..211):", modal(770,840,206,211))

# title: any red beyond x715?
print("\nred-ish pixels x712..790, y64..95:")
redm = a[...,0] > 110
for x in range(712,791):
    col = [y for y in range(64,96) if redm[y,x] and a[y,x][0]-max(a[y,x][1],a[y,x][2])>40]
    if col: print(f"  x={x}: y {min(col)}..{max(col)} n={len(col)} vals {[tuple(a[y,x]) for y in col[:3]]}")
# left start
print("red-ish x205..222, y64..95:")
for x in range(205,223):
    col = [y for y in range(64,96) if redm[y,x] and a[y,x][0]-max(a[y,x][1],a[y,x][2])>40]
    if col: print(f"  x={x}: y {min(col)}..{max(col)} n={len(col)}")

# classification box outer edges incl border
print("\ncol x=650 y200..275 (classification top/bottom):")
prev=None
for y in range(200,276):
    c = tuple(a[y,650]//16*16)
    if c != prev: print(f"  y={y}: {tuple(a[y,650])}")
    prev = c
print("row y=220 x578..596 (classification left):")
prev=None
for x in range(578,597):
    c = tuple(a[220,x]//16*16)
    if c != prev: print(f"  x={x}: {tuple(a[220,x])}")
    prev = c
print("row y=220 x715..732 (classification right):")
prev=None
for x in range(715,733):
    c = tuple(a[220,x]//16*16)
    if c != prev: print(f"  x={x}: {tuple(a[220,x])}")
    prev = c

# arrow4 span: row y=236 x720..755
print("\nrow y=236.5 x720..755:")
for x in range(720,756):
    px = a[236,x]
    if px[0]-max(px[1],px[2])>40: print(f"  x={x}: {tuple(px)}")

# training ellipse outline: top edge scan x=143 y136..146
print("\ncol x=143 y136..148 (training ellipse top):")
for y in range(136,149):
    print(f"  y={y}: {tuple(a[y,143])}")

# gray label corner: box1 top-left corner x241..250 y291..300
print("\nlabel1 top-left corner map:")
for y in range(289,301):
    print(f"  y={y}: " + "".join("K" if max(a[y,x])<150 else ("g" if abs(a[y,x][0]-a[y,x][1])<15 and a[y,x][0]<235 else ".") for x in range(239,253)))
