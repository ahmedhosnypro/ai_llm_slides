from PIL import Image
import numpy as np

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

def runs(mask_1d, minlen=3):
    out = []; x = 0; N = len(mask_1d)
    while x < N:
        if mask_1d[x]:
            x0 = x
            while x < N and mask_1d[x]: x += 1
            if x - x0 >= minlen: out.append((x0, x-1))
        else: x += 1
    return out

def hscan(y, test, label, minlen=3):
    m = test(y)
    rr = runs(m, minlen)
    print("y=%3d %-12s" % (y, label), rr)

def near(c, tol=20):
    return lambda y: (np.abs(a[y,:,0]-c[0])<tol)&(np.abs(a[y,:,1]-c[1])<tol)&(np.abs(a[y,:,2]-c[2])<tol)

# card fills
SALMON = (240,136,144); LAV=(192,192,240); YEL=(248,248,152); GRN=(216,248,228); PEACH=(240,224,200)
for y in [300, 340, 380, 420, 460, 500]:
    hscan(y, near(SALMON), "salmon")
print()
for y in [200, 240, 280, 320, 360]:
    hscan(y, near(LAV), "lavender")
print()
for y in [180, 220, 260, 300]:
    hscan(y, near(YEL), "yellow")
print()
for y in [160, 200, 240, 280]:
    hscan(y, near(GRN), "grnwhite")
print()
for y in [120, 160, 200, 240]:
    hscan(y, near(PEACH), "peach")

# vertical scans through the card stack: column x=200, 400, 600, 800
def vscan(x, test, label, minlen=3):
    m = test(x)
    rr = runs(m, minlen)
    print("x=%3d %-12s" % (x, label), rr)
def vnear(c, tol=20):
    return lambda x: (np.abs(a[:,x,0]-c[0])<tol)&(np.abs(a[:,x,1]-c[1])<tol)&(np.abs(a[:,x,2]-c[2])<tol)
print()
for x in [100, 200, 400, 600, 800]:
    vscan(x, vnear(SALMON), "salmon")
print()
for x in [300, 500, 700]:
    vscan(x, vnear(LAV), "lavender")
    vscan(x, vnear(YEL), "yellow")
    vscan(x, vnear(GRN), "grnwhite")
    vscan(x, vnear(PEACH), "peach")
    print()
