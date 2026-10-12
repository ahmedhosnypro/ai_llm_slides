from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

def cls(y, x):
    rr, gg, bb = r[y,x], g[y,x], b[y,x]
    if rr>200 and gg<90 and bb<90: return "R"
    if rr>140 and gg<130 and bb<130 and rr-gg>40: return "r"
    if rr>215 and gg>170 and bb<120: return "Y"          # yellow/gold
    if np.abs(rr-240)<22 and np.abs(gg-136)<35 and np.abs(bb-144)<35: return "." # salmon
    if gg>=rr and gg>170 and bb>=gg-8 and gg-bb<25: return "m"   # mint
    if rr>205 and gg>195 and 130<bb<190: return "c"      # cream F7F3D8
    if rr>195 and 165<gg<215 and bb>205: return "P"      # pink/mauve F6DAF3/F2C8F0
    if np.abs(rr-234)<13 and np.abs(gg-228)<13 and np.abs(bb-238)<15: return "l" # lavender EAE4EE
    if rr>235 and gg>235 and bb>235: return " "
    if rr<90 and gg<90 and bb<90: return "#"
    if np.abs(rr-233)<9 and np.abs(gg-233)<9 and np.abs(bb-231)<9: return "-"
    return "?"

def dump(x0, x1, y0, y1, step, label):
    print("=== %s ===" % label)
    for y in range(y0, y1, step):
        row = "".join(cls(min(y+step//2,H-1), min(xx+step//2,W-1)) for xx in range(x0, x1, step))
        print("%4d %s" % (y, row))

dump(95, 350, 425, 502, 3, "QUERY ZONE fine (x95..350)")
