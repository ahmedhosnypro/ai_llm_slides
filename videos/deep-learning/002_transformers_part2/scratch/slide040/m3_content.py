#!/usr/bin/env python3
"""Stage 3a: content region bboxes in frame px — title, intro box, panel, paragraph lines."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg')).astype(int)
H, W, _ = im.shape

def bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0: return None
    return int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())

r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
# red ink: strong red, low green/blue (title + red borders + red text)
red = (r > 130) & (g < 90) & (b < 90) & (r - g > 60)
# dark ink (black-ish text)
dark = (r < 120) & (g < 120) & (b < 120)
# non-background: anything clearly darker or colored vs the gray panel (~231,233,232)
nonbg = (np.abs(r - 231) + np.abs(g - 233) + np.abs(b - 232)) > 60

# ---------- TITLE ----------
tmask = np.zeros_like(red); tmask[40:100, 100:800] = red[40:100, 100:800]
print('TITLE bbox (x0,x1,y0,y1):', bbox(tmask))

# ---------- INTRO BOX red border ----------
imask = np.zeros_like(red); imask[95:200, 40:920] = red[95:200, 40:920]
print('INTRO red-ink bbox:', bbox(imask))
# border rect: red pixels rows histogram to find the 2 horizontal strokes
rows = np.where(imask.any(axis=1))[0]
print('intro red rows:', rows.min(), '..', rows.max())
cols = np.where(imask.any(axis=0))[0]
print('intro red cols:', cols.min(), '..', cols.max())
# find horizontal stroke rows (many red pixels in a row)
cnt = imask.sum(axis=1)
strokes = [y for y in rows if cnt[y] > 400]
print('intro horiz stroke rows:', strokes)
cntc = imask.sum(axis=0)
vstrokes = [x for x in cols if cntc[x] > 40]
print('intro vert stroke cols:', vstrokes)

# ---------- paragraph text lines (dark+colored ink inside box, excluding border strokes) ----------
inner = np.zeros_like(nonbg)
y0b, y1b = (strokes[0]+3 if strokes else 103), (strokes[-1]-3 if strokes else 183)
inner[y0b:y1b, 95:875] = nonbg[y0b:y1b, 95:875]
prof = inner.sum(axis=1)
lines = []
in_line = False
for y in range(y0b, y1b):
    if prof[y] > 2 and not in_line:
        start = y; in_line = True
    elif prof[y] <= 2 and in_line:
        lines.append((start, y-1)); in_line = False
if in_line: lines.append((start, y1b-1))
print('paragraph line bands (frame y):', lines)
for (a, bb) in lines:
    m = np.zeros_like(nonbg); m[a:bb+1, 95:875] = nonbg[a:bb+1, 95:875]
    print('  line band', (a,bb), 'ink bbox:', bbox(m))

# ---------- ALGORITHM PANEL (white fill, black border) ----------
# find the panel: large white region in lower-left. Scan for black border strokes.
blackish = (r < 100) & (g < 100) & (b < 100)
pm = np.zeros_like(blackish); pm[195:505, 120:580] = blackish[195:505, 120:580]
print('PANEL black-ink bbox (incl text):', bbox(pm))
# border stroke rows: rows with long horizontal black runs in x 120..580
run = pm[:, 120:580].sum(axis=1)
border_rows = [y for y in range(195, 505) if run[y] > 300]
print('panel horiz border rows:', border_rows)
runc = pm[195:505, :].sum(axis=0)
border_cols = [x for x in range(120, 580) if runc[x] > 200]
print('panel vert border cols:', border_cols)
