from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

def cls(y, x):
    rr, gg, bb = r[y,x], g[y,x], b[y,x]
    if rr>200 and gg<90 and bb<90: return "R"       # strong red
    if rr>140 and 60<gg<130 and 60<bb<130: return "r" # dark/mid red
    if rr>230 and gg>200 and bb<140: return "Y"     # yellow/gold
    if 200<rr<245 and 150<gg<210 and bb<120: return "g" # gold darker
    if np.abs(rr-240)<20 and np.abs(gg-136)<35 and np.abs(bb-144)<35: return "." # salmon card
    if gg>rr and gg>bb and gg>180: return "m"       # mint/pale green
    if rr>200 and gg>200 and bb<180: return "c"     # cream
    if np.abs(rr-234)<14 and np.abs(gg-228)<14 and np.abs(bb-238)<16: return "l" # lavender
    if rr>190 and gg<190 and bb>190: return "P"     # pink/mauve
    if rr>235 and gg>235 and bb>235: return " "     # white
    if rr<90 and gg<90 and bb<90: return "#"        # dark
    if np.abs(rr-233)<10 and np.abs(gg-233)<10: return "-" # panel gray
    return "?"

def dump(x0, x1, y0, y1, step, label):
    print("=== %s (frame px, step %d) ===" % (label, step))
    hdr = "     " + "".join(("%-"+str(step)+"d") % x if False else " " for x in range(x0, x1, step))
    for y in range(y0, y1, step):
        row = "".join(cls(yy, xx) for yy in range(y, min(y+step, H)) for xx in range(x0, x1, step) for _ in [0]) if False else \
              "".join(cls(min(y+step//2, H-1), min(xx+step//2, W-1)) for xx in range(x0, x1, step))
        print("%4d %s" % (y, row))

# bottom-left query zone
dump(55, 360, 425, 516, 5, "QUERY ZONE")
