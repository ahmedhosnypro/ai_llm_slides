from PIL import Image
import numpy as np
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

mint = (np.abs(r-232)<20)&(np.abs(g-252)<14)&(np.abs(b-232)<20)
# container horizontal extent at y=497 (below strips, inside container)
row = mint[497]
xs = np.where(row)[0]
print("mint at y=497: x %d..%d" % (xs.min(), xs.max()))
row = mint[473]
xs = np.where(row)[0]
print("mint at y=473: x %d..%d" % (xs.min(), xs.max()))

# magenta highlight box (F2C8F0-ish fill or RED dotted border) in y 465..505
mag = (r>225)&(g<200)&(b>215)&(r-g>40)
sub = mag[465:506, 190:290]
ys, xs = np.where(sub)
if len(xs): print("magenta/red-dotted bbox: x %d..%d y %d..%d n=%d" % (xs.min()+190, xs.max()+190, ys.min()+465, ys.max()+465, len(xs)))

# strip band: print class grid y 479..492 x 158..372 step 3
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
    return "?"
print("   " + "".join(str((158+i*3)//100%10) for i in range(72)))
print("   " + "".join(str((158+i*3)//10%10) for i in range(72)))
for y in range(477, 497, 2):
    row = "".join(q(*a[min(y+1,539), min(158+i*3, 959)]) for i in range(72))
    print("%3d %s" % (y, row))
