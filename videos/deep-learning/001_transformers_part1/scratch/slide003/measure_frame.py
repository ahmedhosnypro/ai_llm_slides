from PIL import Image
import numpy as np

im = Image.open('unique_slides/slide_003.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def bbox(mask, label):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"{label}: NO PIXELS")
        return None
    print(f"{label}: x=[{xs.min()},{xs.max()}] y=[{ys.min()},{ys.max()}]  w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1}  (in: x={xs.min()/72:.3f}-{(xs.max()+1)/72:.3f}, y={ys.min()/72:.3f}-{(ys.max()+1)/72:.3f})")
    return xs.min(), xs.max(), ys.min(), ys.max()

# title red text: red-ish, in top 20% band
red = (r > 140) & (g < 90) & (b < 90)
title_mask = np.zeros_like(red); title_mask[30:110, :] = red[30:110, :]
print("== TITLE band y=30..110 (px=pt) ==")
bbox(title_mask, "title red ink")

# blue agenda text
blue = (b > 130) & (r < 90) & (g < 110)
print("== BLUE pixels overall ==")
bbox(blue, "all blue ink")
# per-row profile to find the 4 lines
rows = blue.sum(axis=1)
print("== blue row profile (row: count) nonzero bands ==")
bands = []
in_band = False
for y in range(H):
    if rows[y] > 0 and not in_band:
        start = y; in_band = True
    elif rows[y] == 0 and in_band:
        bands.append((start, y - 1)); in_band = False
if in_band: bands.append((start, H - 1))
for (y0, y1) in bands:
    seg = blue[y0:y1 + 1, :]
    ys, xs = np.where(seg)
    print(f"  band y={y0}..{y1} (h={y1-y0+1}) x=[{xs.min()},{xs.max()}] px_in y={y0/72:.3f}-{(y1+1)/72:.3f} x={xs.min()/72:.3f}-{(xs.max()+1)/72:.3f}")
if len(bands) >= 2:
    pitches = [bands[i+1][0] - bands[i][0] for i in range(len(bands)-1)]
    print("  band-start pitches (px):", pitches)

# badge: yellow-ish fill region top right
yellow = (r > 200) & (g > 200) & (b < 190)
badge_mask = np.zeros_like(yellow); badge_mask[0:120, 850:960] = yellow[0:120, 850:960]
print("== BADGE (yellow) top-right ==")
bbox(badge_mask, "badge fill")

# house/outer red frame: red pixels near edges
print("== frame red: column x=0..15 rows, and row y=0..15 cols ==")
col_red = red[:, 0:16].any(axis=1)
print("  left edge red rows:", np.where(col_red)[0][:5], "...", np.where(col_red)[0][-5:] if col_red.any() else "none")
# bottom red line
bot = red[520:540, :]
print("  bottom rows y=520..539 red col-extent:", end=" ")
ys, xs = np.where(bot)
if len(xs): print(f"y=[{ys.min()+520},{ys.max()+520}] x=[{xs.min()},{xs.max()}]")

# purple badge outline?
purple = (r > 110) & (r < 190) & (b > 150) & (g < 110)
print("purple-ish px count in badge area:", purple[0:120, 850:960].sum())
