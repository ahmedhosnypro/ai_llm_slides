# f7: final PIL measurements before the build.
from PIL import Image
import numpy as np
from collections import Counter
img = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg').convert('RGB')).astype(int)
H, W, _ = img.shape
A, B, C, D = 21.15, 0.95635, 2.00, 0.95695
def tb(fx, fy): return (round((fx-A)/B,1), round((fy-C)/D,1))
r, g, b = img[...,0], img[...,1], img[...,2]

# 1. gap shafts precise: dark cols near x768-776, y180-210 and y235-265
dark = (r + g + b) < 3*130
for y0, y1, lbl in [(178, 212, 'gap1'), (233, 268, 'gap2')]:
    sub = dark[y0:y1, 760:785]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"{lbl}: frame x {xs.min()+760}-{xs.max()+760} y {ys.min()+y0}-{ys.max()+y0} n={len(xs)}",
              "-> build x", tb(xs.min()+760, 0)[0], "-", tb(xs.max()+760, 0)[0],
              "y", tb(0, ys.min()+y0)[1], "-", tb(0, ys.max()+y0)[1])
        colc = Counter(xs + 760).most_common(4)
        print("   col modes:", colc)

# 2. ring: strong red annulus — outer bbox per row in x630-725 y310-400
strong = (r > 150) & (g < 70) & (b < 80)
print("RING rows (x-extent of strong red, y310-400):")
for y in range(310, 400, 2):
    xs = np.where(strong[y, 620:730])[0]
    if len(xs): print(f"  y={y}: {xs.min()+620}-{xs.max()+620} n={len(xs)}")
mode_core = Counter(map(tuple, img[318:326, 660:690].reshape(-1,3))).most_common(3)
print("ring top band mode:", mode_core)

# 3. dashed box bottom/right hunt: red-ish in x596-745 y380-445 (exclude maroon: r-b<60)
reddish = (r > 140) & (r - g > 50) & (r - b > 40)
print("reddish x596-745 y378-445 rows:")
for y in range(378, 446):
    xs = np.where(reddish[y, 596:746])[0]
    if len(xs) >= 2: print(f"  y={y}: {xs.min()+596}-{xs.max()+596} n={len(xs)}")

# 4. balloon circle fit: strong red x575-700 y150-300 (exclude x>700), per-row extents
print("BALLOON rows:")
for y in range(150, 302, 4):
    xs = np.where(strong[y, 575:700])[0]
    if len(xs): print(f"  y={y}: {xs.min()+575}-{xs.max()+575} n={len(xs)}")

# 5. enc A&N-bot steel box visible? frame zone (656-710, 326-336)
z = img[325:338, 655:712].reshape(-1,3)
print("enc A&N-bot zone mode:", Counter(map(tuple, z)).most_common(4))
# steel ref (109,153,180); salmon (200,126,87)
# also the parent-render equivalents: check dec stack steel: frame (748-806, 205-220)
z2 = img[205:220, 750:805].reshape(-1,3)
print("dec A&N-top zone mode:", Counter(map(tuple, z2)).most_common(3))
# encoder FF zone: build (653-720, 288-315) -> frame (645.6-709.8, 277.7-303.6)
z3 = img[280:300, 650:708].reshape(-1,3)
print("enc FF zone mode:", Counter(map(tuple, z3)).most_common(3))

# 6. PE icons: parent plus-in-circle at build (649-668, 420-439) -> frame (641.8-660, 399.7-417.9)
z4 = img[400:418, 642:660].reshape(-1,3)
print("enc PE icon zone mode:", Counter(map(tuple, z4)).most_common(4))
# 'clock' would show white + dark ring. sample wider PE box: build (649-728, 415-445)->frame(641.8-717.2,395-427.9)
z5 = img[398:425, 645:715].reshape(-1,3)
print("enc PE box mode:", Counter(map(tuple, z5)).most_common(4))

# 7. Q/K/V circles under encoder stack: build y394.5-406.5 -> frame y379.7-391.2
z6 = img[378:393, 630:725]
reds = ((z6[...,0]>140)&(z6[...,1]<80)&(z6[...,2]<80)).sum()
blues = ((z6[...,2]>120)&(z6[...,0]<80)).sum()
greens = ((z6[...,1]>120)&(z6[...,0]<120)&(z6[...,2]<90)).sum()
print(f"enc VKQ zone: red_px={reds} blue_px={blues} green_px={greens}")
ys, xs = np.where((img[375:395, 620:730,2]>120)&(img[375:395, 620:730,0]<90))
if len(xs): print("  blue circles bbox: x", xs.min()+620, xs.max()+620, "y", ys.min()+375, ys.max()+375)

# 8. Nx circle: gray A6A6A6 at build (597.5-622.5, 329.5-354.5) -> frame (592.5-616.5, 317.3-341.3)
z7 = img[317:342, 590:618].reshape(-1,3)
print("enc Nx zone mode:", Counter(map(tuple, z7)).most_common(4))
