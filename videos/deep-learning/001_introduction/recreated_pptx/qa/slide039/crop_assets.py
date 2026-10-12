#!/usr/bin/env python3
"""Crop the two meme photos from slide_039.jpg at measured boxes (incl. baked red
borders + detection overlays) and patch OUT the live-capture mouse cursor
(spec recreation_brief step 8 + judge ground rule (c): artifacts are omitted).
Cursor at frame ~(439..453, 352..372) straddling the left photo's right border —
patch = per-pixel mean of the rows 26px above and below (couch texture / border
stroke / panel gray are all locally stationary). Banked assets + a patch report."""
from PIL import Image
import numpy as np
import json

FR = 'videos/deep-learning/001_introduction/unique_slides/slide_039.jpg'
ASSETS = 'videos/deep-learning/001_introduction/recreated_pptx/build/assets'
img = Image.open(FR).convert('RGB')
a = np.asarray(img).astype(float)

# --- verify patch source rows are clean (no cursor, no detection-rect ink) ---
reg_below = a[377:400, 436:457]
reg_above = a[324:351, 436:457]
def ink_frac(reg):
    R, G, B = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
    red = (R > 140) & (R - G > 60) & (R - B > 60)
    green = (G > 110) & (G - R > 40) & (G - B > 40)
    yellow = (R > 200) & (G > 190) & (B < 140)
    dark = (R < 100) & (G < 100) & (B < 100)
    return float((red | green | yellow | dark).mean())
print('patch-source ink frac below:', round(ink_frac(reg_below), 4), 'above:', round(ink_frac(reg_above), 4))

# --- cursor patch: x 436..456, y 350..374 (frame coords) ---
patched = a.copy()
X0, X1, Y0, Y1 = 436, 457, 350, 375
OFF = 26
for y in range(Y0, Y1):
    src_top = a[y - OFF, X0:X1]
    src_bot = a[y + OFF, X0:X1]
    patched[y, X0:X1] = (src_top + src_bot) / 2.0
# keep the border column's saturation: mean of two red border pixels stays red — OK.

# --- crops (PIL box: right/bottom exclusive) ---
left_box = (183, 308, 449, 444)   # 266 x 136
right_box = (473, 305, 733, 444)  # 260 x 139
pa = np.clip(np.round(patched), 0, 255).astype(np.uint8)
pimg = Image.fromarray(pa)
left = pimg.crop(left_box)
right = pimg.crop(right_box)
left.save(f'{ASSETS}/slide039_cat_photo.png')
right.save(f'{ASSETS}/slide039_dog_photo.png')
print('left crop:', left.size, '-> slide039_cat_photo.png')
print('right crop:', right.size, '-> slide039_dog_photo.png')

# --- verify: no bright cursor-like cluster remains in the patched left crop ---
lc = np.asarray(left).astype(int)
wm = (lc[:, :, 0] > 215) & (lc[:, :, 1] > 215) & (lc[:, :, 2] > 210)
# cursor area within crop: x 436-183=253..274, y 350-308=42..67
zone = wm[38:72, 248:280]
print('residual bright px in cursor zone:', int(zone.sum()))
# border continuity check at x=448-183=265: red pixels in rows 42..67
Rc, Gc, Bc = lc[:, :, 0], lc[:, :, 1], lc[:, :, 2]
border_col = (Rc[38:70, 264:268] > 120) & (Rc[38:70, 264:268] - Gc[38:70, 264:268] > 40)
print('border-column red continuity rows 38..69 (cols 264..267):', int(border_col.sum()), 'of', 32 * 4)

report = {
    'cursor_patch_frame_box': {'x': [436, 456], 'y': [350, 374], 'method': 'mean(rows y-26, y+26)'},
    'left_crop': list(left_box), 'right_crop': list(right_box),
    'left_size': list(left.size), 'right_size': list(right.size),
}
with open('videos/deep-learning/001_introduction/recreated_pptx/qa/slide039/crop_assets_out.json', 'w') as f:
    json.dump(report, f, indent=1)
print('BANKED -> qa/slide039/crop_assets_out.json')
