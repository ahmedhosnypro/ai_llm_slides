# Pass 4: full structural measurement.
from PIL import Image
import numpy as np
from scipy import ndimage

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_024.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def report(mask, label, minpx=50):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        m = lab == i
        s = int(m.sum())
        if s < minpx: continue
        ys, xs = np.nonzero(m)
        out.append((s, xs.min(), xs.max(), ys.min(), ys.max()))
    out.sort(reverse=True)
    print(f"== {label}: {len(out)} clusters >= {minpx}px")
    for s, x0, x1, y0, y1 in out:
        print(f"   x[{x0:3d},{x1:3d}] y[{y0:3d},{y1:3d}] w={x1-x0+1:3d} h={y1-y0+1:3d} ctr=({(x0+x1)/2:.0f},{(y0+y1)/2:.0f}) n={s}   in=({(x0+x1)/144:.2f},{(y0+y1)/144:.2f})")
    return out

# pale yellow nodes
yellow = (r > 232) & (g > 228) & (b > 165) & (b < 242) & (r - b > 12)
report(yellow, 'PALE-YELLOW nodes', 150)
# green nodes (Boy)
green = (g > 150) & (g - r > 20) & (g - b > 20)
report(green, 'GREEN nodes', 100)
# red strokes (loose)
red = (r > 140) & (g < 120) & (b < 120)
report(red, 'RED strokes', 25)
# black text (title, labels, sentence)
black = (r < 80) & (g < 80) & (b < 80)
report(black, 'BLACK text', 40)
# dark blue (circle/sentence borders, icon outlines)
dblue = (b > 130) & (b - r > 60) & (g < 140)
report(dblue, 'DARK-BLUE', 40)
# orange
orange = (r > 200) & (g > 60) & (g < 190) & (b < 110) & (r - b > 110)
report(orange, 'ORANGE', 20)
# pink (block arrow fill)
pink = (r > 210) & (r - g > 25) & (r - b > 25) & (g > 120)
report(pink, 'PINK hatch', 30)

# gray panel bounds: E9E9E9-ish
grayp = (np.abs(r - 0xE9) < 14) & (np.abs(g - 0xE9) < 14) & (np.abs(b - 0xE9) < 14)
ys, xs = np.nonzero(grayp)
print(f"GRAY panel-ish bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] n={len(xs)}")
# circle interior sample
for pt in [(278,120),(278,450),(90,291),(460,291),(700,300),(700,450),(120,120)]:
    print(f"sample {pt}: rgb={tuple(a[pt[1], pt[0]])}")
