from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
# red text mask (loose, catches JPEG-darkened C00000)
red = (R - G > 40) & (R - B > 30) & (R > 110)

def show(x0, x1, y0, y1, label, step=1):
    print(f"=== {label} (x {x0}..{x1}, y {y0}..{y1}) ===")
    for y in range(y0, y1, step):
        row = "".join("#" if red[y, x] else "." for x in range(x0, x1))
        print(f"  y={y}: {row}")

# 'W' of "Where" — x 180..230, y 86..122 (serif W = wide flat foot serifs at baseline)
show(180, 232, 86, 122, "title 'W'")
# 'G' of "Get" — x 340..375
show(340, 378, 86, 122, "title 'G'")
