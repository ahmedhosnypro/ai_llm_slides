# m12_strips.py — line strips, band edges, navy head, border colors
import numpy as np
from PIL import Image
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)

def hue(p):
    r,g,b=int(p[0]),int(p[1]),int(p[2])
    if max(p)>=246 and max(p)-min(p)<=10: return "."      # white
    if r-b>25 and r-g>25 and r>150: return "R"            # red/pink
    if b-r>20 and b-g>10: return "B"                      # blue
    if g-r>15 and g-b>15: return "G"                      # green
    if max(p)-min(p)<=14: return "-"                      # gray/band
    if r>200 and g>170 and b<190 and r-b>30: return "y"
    return "?"

def strip(y0,y1,x0,x1,step=2,label=""):
    print(f"--- {label} y{y0}..{y1} (cols x{x0}..{x1} step {step})")
    for y in range(y0,y1,1):
        line="".join(hue(a[y,x]) for x in range(x0,x1,step))
        print(f"{y:3d} {line}")

# strip A: between output circles bottom (y~299) and band top
strip(296,308,500,890,3,"STRIP-A above band")
# strip B: between band bottom and input circles top
strip(428,444,500,890,3,"STRIP-B below band")
