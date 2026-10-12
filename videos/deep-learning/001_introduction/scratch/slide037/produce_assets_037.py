# produce_assets_037.py — diagram crop (edge-safety verified) for slide 037.
from PIL import Image
import json

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
im = Image.open(f'{BASE}/unique_slides/slide_037.jpg').convert('RGB')
px = im.load()
out = {}

# crop box (frame px): x 68..893, y 266..450 — inside the drawn panel borders
# (left x65, right x896, top y262, bottom y511), above the question ink (y453+),
# below the top-border halo (263-265). PIL crop is exclusive at right/bottom.
BOX = (68, 266, 894, 451)

def edge_ink(rows=None, cols=None, thr=690):
    """count pixels darker than thr (sum RGB) on given rows/cols within the crop span"""
    res = {}
    if rows:
        for y in rows:
            cnt = sum(1 for x in range(BOX[0], BOX[2]) if sum(px[x, y]) < thr)
            res[f'row{y}'] = cnt
    if cols:
        for x in cols:
            cnt = sum(1 for y in range(BOX[1], BOX[3]) if sum(px[x, y]) < thr)
            res[f'col{x}'] = cnt
    return res

# edge safety: the crop's outermost rows/cols must be free of border stroke/halo
# (content ink touching an edge would mean a clipped element).
out['top_edge'] = edge_ink(rows=[266, 267, 268])
out['bottom_edge'] = edge_ink(rows=[449, 450])
out['left_edge'] = edge_ink(cols=[68, 69])
out['right_edge'] = edge_ink(cols=[892, 893])
# mean brightness of each edge row/col (border halo would lower it)
def edge_mean(kind, idx):
    if kind == 'row':
        vals = [sum(px[x, idx]) / 3 for x in range(BOX[0], BOX[2])]
    else:
        vals = [sum(px[idx, y]) / 3 for y in range(BOX[1], BOX[3])]
    return round(sum(vals) / len(vals), 1)
out['edge_means'] = {
    'row266': edge_mean('row', 266), 'row450': edge_mean('row', 450),
    'col68': edge_mean('col', 68), 'col893': edge_mean('col', 893),
}

crop = im.crop(BOX)
crop.save(f'{BASE}/recreated_pptx/build/assets/diagram037.png')
out['saved'] = dict(path='build/assets/diagram037.png', box=BOX, size=crop.size,
                    w_in=round((BOX[2]-BOX[0])/72, 5), h_in=round((BOX[3]-BOX[1])/72, 5))
print(json.dumps(out, indent=1))
