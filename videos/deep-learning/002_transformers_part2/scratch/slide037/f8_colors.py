# f8: aligned color comparison original(slide-space) vs parent render(base_960), per box.
from PIL import Image
import numpy as np
from collections import Counter

orig = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/slide037_slide_space.png').convert('RGB')).astype(int)
base = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/base_960.png').convert('RGB')).astype(int)
print('shapes', orig.shape, base.shape)

def mode(img, x0, x1, y0, y1, n=3):
    z = img[y0:y1, x0:x1].reshape(-1, 3)
    return Counter(map(tuple, z)).most_common(n)

BOXES = {
  'enc_addn_top (019 steel 6D99B4)': (656, 716, 275, 286),
  'enc_ff (019 807560)':             (656, 716, 291, 312),
  'enc_addn_bot (019 6C99B4)':       (660, 716, 345, 352),
  'enc_mha (018 salmon C87E57)':     (654, 718, 358, 384),
  'enc_container (017 tan C8A888)':  (632, 648, 320, 335),
  'enc_nx (017 tan)':                (600, 620, 332, 352),
  'dec_addn_top (019 5C9CB7)':       (756, 814, 208, 217),
  'dec_ff (019 6E7E62)':             (756, 814, 226, 247),
  'dec_addn_mid (019 5C9CB6)':       (756, 814, 265, 273),
  'dec_indigo (019 6E87E0)':         (756, 814, 331, 342),
  'dec_purple (017 CE8ADC)':         (750, 815, 355, 380),
  'dec_olive_container':             (747, 752, 230, 260),
  'yellow_band (017 FFFF00)':        (682, 740, 255, 320),
  'enc_pe (017 brown B08058)':       (652, 725, 418, 442),
  'enc_embed (017 brown)':           (640, 724, 447, 481),
  'dec_embed (017 maroon B08058?)':  (752, 822, 420, 445),
  'encVk_q (017 C00000)':            (712, 723, 396, 405),
  'encVk_v (019 green 55A044)':      (658, 669, 396, 405),
  'softmax (017 A8ECBC)':            (755, 815, 154, 164),
  'linear (017 B0E4CE)':             (755, 815, 179, 189),
}
for lbl, (x0, x1, y0, y1) in BOXES.items():
    mo = mode(orig, x0, x1, y0, y1)
    mb = mode(base, x0, x1, y0, y1)
    print(f"{lbl}\n  ORIG {mo}\n  BASE {mb}")

# yellow band precise bbox in ORIGINAL slide space
yel = (np.abs(orig - np.array([255, 241, 118])).sum(axis=2) < 90) | ((orig[...,0]>230)&(orig[...,1]>210)&(orig[...,2]<160))
ys, xs = np.where(yel[200:350, 640:780])
if len(xs):
    print('ORIG yellow band bbox (slide):', xs.min()+640, xs.max()+640, ys.min()+200, ys.max()+200, 'n', len(xs))
ys, xs = np.where(((base[...,0]>230)&(base[...,1]>210)&(base[...,2]<160))[200:350, 640:780])
if len(xs):
    print('BASE yellow band bbox (slide):', xs.min()+640, xs.max()+640, ys.min()+200, ys.max()+200, 'n', len(xs))
