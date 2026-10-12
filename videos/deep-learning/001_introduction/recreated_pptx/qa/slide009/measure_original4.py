# stage 4: ASCII maps of structure + per-box masks
from PIL import Image
import numpy as np
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]

def cls(p):
    R,G,B = p
    if R>235 and G>235 and B>235:
        if R>248 and G>248 and B>248: return "W"   # pure white
        return "w"                                  # near-white
    if abs(R-G)<14 and abs(G-B)<14:
        v=(R+G+B)//3
        if v<60: return "K"      # black
        if v<150: return "D"     # dark gray
        if v<205: return "G"     # mid gray
        if v<228: return "g"     # light-mid gray
        return "h"               # high gray
    if R>140 and G<100 and B<100 and R-max(G,B)>60: return "R"   # red
    if R>200 and G>170 and B>140 and R>G>B: return "P"           # peach
    if R>190 and G>190 and B<215 and G>200: return "Y"           # pale yellow
    if R<235 and G>225 and B>225: return "C"                     # pale cyan
    if G>225 and R<240 and B<240 and abs(G-B)<25 and G-R>12: return "N"  # pale green
    if B>225 and R>200 and G<225: return "L"                     # lavender
    if R>200 and G>200 and B<60: return "y"                      # yellow
    return "?"

def amap(x0,x1,y0,y1,step=2,label=""):
    print(f"--- map {label} x{x0}..{x1} y{y0}..{y1} step{step} ---")
    hdr = "     " + "".join(str((x//10)%10) for x in range(x0,x1,step))
    print(hdr)
    for y in range(y0,y1,step):
        row = "".join(cls(a[y,x]) for x in range(x0,x1,step))
        print(f"y{y:4d} {row}")

amap(48, 120, 38, 108, 2, "top-left corner of panel")
amap(880, 915, 38, 108, 2, "top-right corner of panel")
amap(48, 120, 455, 522, 2, "bottom-left of panel")
amap(880, 915, 455, 522, 2, "bottom-right of panel")

# per-box masks
def bbox_of(mask):
    ys, xs = np.nonzero(mask)
    if len(xs)==0: return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(mask.sum()))

def modal(x0,x1,y0,y1):
    reg = a[y0:y1, x0:x1].reshape(-1,3)
    return Counter(map(tuple, (reg//4*4))).most_common(3)

print("\n-- panel interior whites --")
print("white panel interior modal (x200..300,y300..350):", modal(200,300,300,350))
print("outside-left modal (x20..50,y200..250):", modal(20,50,200,250))
print("outside-top modal (x200..300,y10..38):", modal(200,300,10,38))
print("bottom gray band modal (x200..300,y485..515):", modal(200,300,485,515))
print("left gray band modal (x61..67,y200..250):", modal(61,67,200,250))
print("top gray band modal (x200..300,y91..96):", modal(200,300,91,96))
print("bottom inner gray band modal (x200..300,y469..478):", modal(200,300,469,478))

# red border rect of white panel: check col 480 for horizontal border rows
colm = a[:, 480]
redrows = [y for y in range(60, 500) if colm[y][0]>130 and colm[y][0]-max(colm[y][1],colm[y][2])>55]
print("\nred rows at x=480 (panel top/bottom borders):", redrows)
rowm = a[280, :]
redcols = [x for x in range(60, 940) if rowm[x][0]>130 and rowm[x][0]-max(rowm[x][1],rowm[x][2])>55]
print("red cols at y=280 (panel left/right borders):", redcols)
