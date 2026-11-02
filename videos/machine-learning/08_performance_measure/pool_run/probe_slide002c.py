import os
from PIL import Image
import numpy as np
NS = os.environ.get("NS", "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
im = np.array(Image.open(f"{NS}/unique_slides/slide_002.jpg").convert("RGB")).astype(int)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
red = (R > 130) & (R - G > 50) & (R - B > 50)
blue = (B > 110) & (B - R > 30) & (B - G > 20)
mr = np.zeros_like(red); mr[80:520, 560:960] = red[80:520, 560:960]
col = mr.sum(axis=0)
print("right red cols>60:", [(x, int(c)) for x, c in enumerate(col) if c > 60])
row = mr.sum(axis=1)
print("right red rows>60:", [(y, int(c)) for y, c in enumerate(row) if c > 60])
mb = np.zeros_like(blue); mb[80:220, 560:960] = blue[80:220, 560:960]
col = mb.sum(axis=0)
print("act blue cols>30:", [(x, int(c)) for x, c in enumerate(col) if c > 30])
row = mb.sum(axis=1)
print("act blue rows>30:", [(y, int(c)) for y, c in enumerate(row) if c > 30])
# any horizontal line (grayish) across right half: pixels where all channels close and <230
line = (np.abs(R - G) < 12) & (np.abs(G - B) < 12) & (R < 235)
ml = np.zeros_like(line); ml[85:525, 560:960] = line[85:525, 560:960]
row = ml.sum(axis=1)
print("right gray rows>250:", [(y, int(c)) for y, c in enumerate(row) if c > 250])
col = ml.sum(axis=0)
print("right gray cols>250:", [(x, int(c)) for x, c in enumerate(col) if c > 250])
# amber fill of Input Sample ellipse: sample around (640,280)? find amber pixels
amber = (R > 200) & (G > 150) & (G < 220) & (B < 180)
ma = np.zeros_like(amber); ma[200:500, 560:960] = amber[200:500, 560:960]
ys, xs = np.where(ma)
if len(xs): print("amber bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "n", len(xs))
# light blue label ellipse
lb = (B > 200) & (B - R > 20) & (G > 200)
mlb = np.zeros_like(lb); mlb[200:500, 560:960] = lb[200:500, 560:960]
ys, xs = np.where(mlb)
if len(xs): print("lightblue bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "n", len(xs))
# pink model box fill
pink = (R > 235) & (G > 200) & (G < 240) & (B > 200) & (B < 240)
mp = np.zeros_like(pink); mp[200:500, 560:960] = pink[200:500, 560:960]
ys, xs = np.where(mp)
if len(xs): print("pink bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "n", len(xs))
