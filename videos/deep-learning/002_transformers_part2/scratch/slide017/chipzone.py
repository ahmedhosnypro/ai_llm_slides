from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
def q(rr,gg,bb):
    if rr>200 and gg<90 and bb<90: return "R"
    if rr>140 and gg<130 and bb<130 and rr-gg>40: return "r"
    if rr>215 and gg>170 and bb<120: return "Y"
    if abs(rr-240)<22 and abs(gg-136)<35 and abs(bb-144)<35: return "."
    if gg>=rr-6 and gg>175 and abs(gg-bb)<30 and gg-rr>6: return "m"
    if rr>205 and gg>195 and 130<bb<190: return "c"
    if rr>195 and 160<gg<215 and bb>205: return "P"
    if abs(rr-234)<13 and abs(gg-228)<13 and abs(bb-238)<15: return "l"
    if rr>235 and gg>235 and bb>235: return " "
    if rr<90 and gg<90 and bb<90: return "#"
    if 60<rr<160 and 60<gg<130 and bb<110: return "o"   # dark orange A0400E-ish
    if abs(rr-74)<30 and abs(gg-74)<30 and abs(bb-74)<30: return "d" # dark gray 4A4A4A
    if 150<rr<210 and 120<gg<180 and bb<100: return "O" # olive E0DC1E? no
    if abs(rr-233)<9 and abs(gg-233)<9 and abs(bb-231)<9: return "-"
    return "?"
print("CHIP ZONE x290..545 y170..262 (step 3):")
print("    " + "".join(str((x//100)%10) for x in range(290, 545, 3)))
print("    " + "".join(str((x//10)%10) for x in range(290, 545, 3)))
for y in range(170, 262, 3):
    row = "".join(q(*a[y, x]) for x in range(290, 545, 3))
    print("%3d %s" % (y, row))
