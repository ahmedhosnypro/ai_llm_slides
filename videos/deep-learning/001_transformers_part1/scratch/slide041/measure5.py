import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg").convert("RGB")).astype(int)

def runs(axis_vals, label, tol=14, minrun=2):
    print(f"--- {label} ---")
    vals = [tuple(int(v) for v in px) for px in axis_vals]
    start = 0
    cur = list(vals[0])
    out = []
    for i in range(1, len(vals)):
        if abs(vals[i][0]-cur[0])>tol or abs(vals[i][1]-cur[1])>tol or abs(vals[i][2]-cur[2])>tol:
            out.append((start, i-1, tuple(cur)))
            start = i; cur = list(vals[i])
        else:
            for j in range(3): cur[j] = int(cur[j]*0.85 + vals[i][j]*0.15)
    out.append((start, len(vals)-1, tuple(cur)))
    for s,e,c in out:
        if e-s >= minrun:
            cr,cg,cb = c
            tag=""
            if cr>235 and cg>235 and cb>235: tag="WHITE"
            elif abs(cr-230)<12 and abs(cg-231)<12 and abs(cb-228)<12: tag="PANELGRAY"
            elif abs(cr-247)<10 and abs(cg-235)<12 and abs(cb-217)<14: tag="ENC-CREAM"
            elif abs(cr-203)<14 and abs(cg-250)<14 and abs(cb-221)<14: tag="DEC-GREEN"
            elif cr>170 and cg<70 and cb<70: tag="RED"
            elif abs(cr-179)<22 and abs(cg-157)<22 and abs(cb-219)<22: tag="PURPLE-B39DDB"
            elif abs(cr-168)<18 and abs(cg-168)<18 and abs(cb-168)<18: tag="GRAY168"
            elif abs(cr-120)<25 and abs(cg-107)<25 and abs(cb-90)<25: tag="DARKBROWN120"
            elif cr>240 and cg>240 and cb<130: tag="YELLOW"
            elif abs(cr-232)<14 and abs(cg-181)<14 and abs(cb-126)<16: tag="TAN-CENTER"
            elif abs(cr-218)<12 and abs(cg-167)<12 and abs(cb-111)<14: tag="TAN-BORDER"
            print(f"  {s:4d}..{e:4d} ({e-s+1:3d}px) rgb{c} {tag}")

# encoder stack center / decoder stack center columns
for x in (600, 640, 690, 750, 782, 812, 850, 880):
    runs(im[:, x, :], f"col x={x}")
# rows through right panel
for y in (115, 130, 150, 175, 200, 225, 255, 285, 320, 345, 375, 400, 420, 440, 455, 480, 505, 518):
    runs(im[y, 540:960, :], f"row y={y} (x offset +540)")
