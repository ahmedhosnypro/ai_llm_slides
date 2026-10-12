from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
blueish = (B - R > 35) & (B > 140)
reddish = (R - B > 50) & (R - G > 50) & (R > 90)

def profile(mask, x0, x1, y0, y1, label):
    print(f"{label} row profile (x {x0}..{x1}):")
    for y in range(y0, y1):
        n = mask[y, x0:x1].sum()
        if n: print(f"  y={y}: {n}")

# L1 x-height band: 'computer' word x 517..613 (o,m,p,u,t,e) - x-height letters bottom = baseline
profile(blueish, 517, 614, 140, 165, "L1 'computer'")
# L2 'example:' x 150..239
profile(blueish, 150, 240, 192, 215, "L2 'example:'")
# L3a 'Gaussian' x 252..344
profile(blueish, 252, 345, 218, 245, "L3a 'Gaussian'")
# L3b 'filters,' x 260..322
profile(blueish, 260, 323, 244, 270, "L3b 'filters,'")
# bullet2 dot: x 133..152, y 338..362
profile(reddish, 133, 152, 338, 362, "bullet2 dot")
# bullet1 text 'Are' cap top: x 152..218
profile(reddish, 152, 219, 298, 326, "bullet1 'Are...'")
# label 'Filter' x 388..449
lab = (B - R > 35) & (B > 140)
profile(lab, 388, 450, 442, 468, "label 'Filter'")
# title 'W' cap x 180..285
tl = (R - G > 60) & (R - B > 60) & (R > 120)
profile(tl, 180, 286, 84, 124, "title 'Where'")
