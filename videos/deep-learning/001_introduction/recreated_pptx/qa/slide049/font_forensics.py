#!/usr/bin/env python3
"""Title font decision: IoU template match of 'Convnets' crop vs Liberation Serif/Sans Bold.
Also body check: 'After the convolutional layers' head IoU (SerifR vs SansR)."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_049.jpg"
a = np.asarray(Image.open(IMG).convert("L")).astype(int)
FONTDIR = "/usr/share/fonts/liberation"

def crop_bin(y0,y1,x0,x1,thr=400):
    return (a[y0:y1, x0:x1] < thr)

def render_word(text, fontpath, size_pt, pad=30):
    """render word, return binarized array + ink bbox"""
    f = ImageFont.truetype(fontpath, int(round(size_pt*4)))
    img = Image.new("L", (4000, 400), 255)
    dr = ImageDraw.Draw(img)
    dr.text((100, 150), text, font=f, fill=0)
    arr = np.asarray(img) < 128
    ys, xs = np.where(arr)
    return arr[ys.min():ys.max()+1, xs.min():xs.max()+1]

def iou(orig, tmpl):
    """resize tmpl to orig shape (nearest) and compute IoU"""
    from PIL import Image as I
    t = I.fromarray((tmpl*255).astype(np.uint8)).resize((orig.shape[1], orig.shape[0]), I.LANCZOS)
    tb = np.asarray(t) > 127
    inter = (orig & tb).sum()
    union = (orig | tb).sum()
    return inter/union

# TITLE: original 'Convnets' ink: x 252..459, y 84..117 (baseline ~116.5, no descenders in 'Convnets')
orig_title = crop_bin(84, 118, 252, 460)
print("orig 'Convnets' crop:", orig_title.shape)
for name, path, size in [("SerifB@52.4", f"{FONTDIR}/LiberationSerif-Bold.ttf", 52.4),
                          ("SerifB@49.0", f"{FONTDIR}/LiberationSerif-Bold.ttf", 49.0),
                          ("SansB@46.5",  f"{FONTDIR}/LiberationSans-Bold.ttf", 46.5),
                          ("SansB@49.0",  f"{FONTDIR}/LiberationSans-Bold.ttf", 49.0)]:
    t = render_word("Convnets", path, size)
    print(f"  {name}: tmpl {t.shape} IoU {iou(orig_title, t):.4f}")

# cap-height check of rendered vs orig: orig cap = 118-84 ~ 34 (with AA); measure tmpl cap at size
for name, path in [("SerifB", f"{FONTDIR}/LiberationSerif-Bold.ttf"), ("SansB", f"{FONTDIR}/LiberationSans-Bold.ttf")]:
    t = render_word("HC", path, 100)
    print(f"  {name} cap@100pt = {t.shape[0]}px -> ratio {t.shape[0]/100:.3f}")

# BODY: original 'After the conv' head: band1 x 148..430, y 199..223 (includes descender y)
orig_body = crop_bin(199, 223, 148, 430)
print("\norig 'After the convolutional layers' head:", orig_body.shape)
for name, path, size in [("SerifR@25.8", f"{FONTDIR}/LiberationSerif-Regular.ttf", 25.8),
                          ("SansR@23.8",  f"{FONTDIR}/LiberationSans-Regular.ttf", 23.8)]:
    t = render_word("After the convolutional layers", path, size)
    print(f"  {name}: tmpl {t.shape} IoU {iou(orig_body, t):.4f}")
