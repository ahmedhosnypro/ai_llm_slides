import os
from PIL import Image
import numpy as np
NS = os.environ.get("NS", "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
im = np.array(Image.open(f"{NS}/unique_slides/slide_002.jpg").convert("RGB")).astype(int)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
magenta = (R > 120) & (B > 120) & (G < R - 40) & (G < B - 40)
m = np.zeros_like(magenta); m[90:210, 600:960] = magenta[90:210, 600:960]
ys, xs = np.where(m)
print("magenta act-region bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "n", len(xs))
# green border of negative pane / 0 strip with lower threshold
green = (G > 90) & (G - R > 30) & (G - B > 30)
mg = np.zeros_like(green); mg[100:520, 300:620] = green[100:520, 300:620]
col = mg.sum(axis=0)
print("green cols>40:", [(x, int(c)) for x, c in enumerate(col) if c > 40])
row = mg.sum(axis=1)
print("green rows>40:", [(y, int(c)) for y, c in enumerate(row) if c > 40])
# dark border columns full left area rows 130..510, lower threshold
dark = (R < 140) & (G < 140) & (B < 140)
md = np.zeros_like(dark); md[130:510, 40:640] = dark[130:510, 40:640]
col = md.sum(axis=0)
print("dark cols>250:", [(x, int(c)) for x, c in enumerate(col) if c > 250])
row = md.sum(axis=1)
print("dark rows>350:", [(y, int(c)) for y, c in enumerate(row) if c > 350])
# right panels: find panel borders (tan/gray/blue lines) x560-960 y90-520
sub = dark[90:520, 560:960]
col = sub.sum(axis=0)
print("right dark cols>250:", [(560 + x, int(c)) for x, c in enumerate(col) if c > 250])
row = sub.sum(axis=1)
print("right dark rows>250:", [(90 + y, int(c)) for y, c in enumerate(row) if c > 250])
# +1 strip fill bbox (pink) and 0 strip (light green): sample colors
print("pink strip sample px(280,300):", im[300, 280], " green strip px(520,300):", im[300, 520])
print("plane pane interior px(150,200):", im[200, 150])
