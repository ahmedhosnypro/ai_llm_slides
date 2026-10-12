# probe: precise frame-vs-render scans for the suspect regions (attempt-1 render)
import numpy as np
from PIL import Image
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
RN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide032/render_1.png"
f = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r = np.asarray(Image.open(RN).convert("RGB")).astype(int)
S = r.shape[1] / f.shape[1]

def ink(img, x0, y0, x1, y1):
    reg = img[y0:y1, x0:x1]
    mx = reg.max(axis=2); mn = reg.min(axis=2); sat = mx - mn
    white = (mx >= 238) & (sat <= 14)
    gray = (np.abs(reg[:, :, 0] - reg[:, :, 1]) <= 8) & (np.abs(reg[:, :, 1] - reg[:, :, 2]) <= 8) & (mx >= 200) & (mx < 246)
    m = ~(white | gray)
    ys, xs = np.where(m)
    if len(xs) == 0:
        return None
    return (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)

def show(name, fb, rb):
    if fb is None or rb is None:
        print(f"{name:28s} MISSING f={fb} r={rb}"); return
    d = [rb[i] / S - fb[i] for i in range(4)]
    print(f"{name:28s} f x{fb[0]:4d}..{fb[2]:4d} y{fb[1]:4d}..{fb[3]:4d} | r {rb[0]/S:6.1f}..{rb[2]/S:6.1f} {rb[1]/S:6.1f}..{rb[3]/S:6.1f} | d {d[0]:+5.1f} {d[1]:+5.1f} {d[2]:+5.1f} {d[3]:+5.1f}")

# 1) title/subtitle row bands in the frame: which rows hold ink (x 555..870)
print("== frame title/subtitle row profile (x555..870) ==")
for y in range(108, 182, 2):
    row = f[y, 555:870]
    mx = row.max(axis=1); mn = row.min(axis=1); sat = mx - mn
    inkc = ~(((mx >= 238) & (sat <= 14)) | ((np.abs(row[:, 0] - row[:, 1]) <= 8) & (np.abs(row[:, 1] - row[:, 2]) <= 8) & (mx >= 200) & (mx < 246)))
    xs = np.where(inkc)[0]
    if len(xs):
        print(f" y={y:3d}: ink x {xs.min()+555}..{xs.max()+555}  n={len(xs)}")
print("-- render same rows (frame-scale) --")
for y in range(216, 364, 4):
    row = r[y, int(555 * S):int(870 * S)]
    mx = row.max(axis=1); mn = row.min(axis=1); sat = mx - mn
    inkc = ~(((mx >= 238) & (sat <= 14)) | ((np.abs(row[:, 0] - row[:, 1]) <= 8) & (np.abs(row[:, 1] - row[:, 2]) <= 8) & (mx >= 200) & (mx < 246)))
    xs = np.where(inkc)[0]
    if len(xs):
        print(f" y={y/S:6.1f}: ink x {xs.min()/S+555:6.1f}..{xs.max()/S+555:6.1f}  n={len(xs)}")

# 2) out circles: clean window away from panel corners
print("\n== out circles (clean win x515..885 y250..312) ==")
show("out row", ink(f, 515, 250, 885, 312), ink(r, int(515 * S), int(250 * S), int(885 * S), int(312 * S)))
for i, cx in enumerate([540, 648, 757, 861]):
    show(f" out c{i+1}", ink(f, cx - 32, 250, cx + 32, 312), ink(r, int((cx - 32) * S), int(250 * S), int((cx + 32) * S), int(312 * S)))

# 3) band right side: what ink exists x820..900, y300..434
print("\n== band region right side ==")
show("band right labels", ink(f, 820, 300, 900, 434), ink(r, int(820 * S), int(300 * S), int(900 * S), int(434 * S)))
print(" frame band-right ink columns (rows 320..420):")
reg = f[320:420, 820:900]
mx = reg.max(axis=2); mn = reg.min(axis=2); sat = mx - mn
m = ~(((mx >= 238) & (sat <= 14)) | ((np.abs(reg[:, :, 0] - reg[:, :, 1]) <= 8) & (np.abs(reg[:, :, 1] - reg[:, :, 2]) <= 8) & (mx >= 200) & (mx < 246)))
cols = np.where(m.any(axis=0))[0]
print("  x:", [c + 820 for c in cols])

# 4) net panel corner radius: frame top-right corner ink profile
print("\n== net panel top-left corner (x468..500, y234..268) frame rows ==")
for y in range(234, 270, 2):
    row = f[y, 468:500]
    mx = row.max(axis=1); mn = row.min(axis=1); sat = mx - mn
    inkc = ~(((mx >= 238) & (sat <= 14)) | ((np.abs(row[:, 0] - row[:, 1]) <= 8) & (np.abs(row[:, 1] - row[:, 2]) <= 8) & (mx >= 200) & (mx < 246)))
    xs = np.where(inkc)[0]
    if len(xs):
        print(f" y={y}: first ink x={xs.min()+468}")
print("-- render --")
for y in range(int(234 * S), int(270 * S), 4):
    row = r[y, int(468 * S):int(500 * S)]
    mx = row.max(axis=1); mn = row.min(axis=1); sat = mx - mn
    inkc = ~(((mx >= 238) & (sat <= 14)) | ((np.abs(row[:, 0] - row[:, 1]) <= 8) & (np.abs(row[:, 1] - row[:, 2]) <= 8) & (mx >= 200) & (mx < 246)))
    xs = np.where(inkc)[0]
    if len(xs):
        print(f" y={y/S:.1f}: first ink x={xs.min()/S+468:.1f}")

# 5) eq panel + matrix exact edges (frame): stroke centers via dark-red mask
def red_cols(img, y0, y1, x0, x1):
    reg = img[y0:y1, x0:x1]
    m = (reg[:, :, 0] > 90) & (reg[:, :, 1] < 110) & (reg[:, :, 2] < 110) & (reg[:, :, 0] - reg[:, :, 1] > 40)
    cols = np.where(m.any(axis=0))[0]
    return [c + x0 for c in cols]
print("\n== eq panel border stroke columns (row 170..172, x40..80 and x440..490) ==")
print(" frame left :", red_cols(f, 168, 174, 40, 85))
print(" frame right:", red_cols(f, 168, 174, 440, 495))
print(" render left :", [round(c / S, 1) for c in red_cols(r, int(168 * S), int(174 * S), int(40 * S), int(85 * S))])
print(" render right:", [round(c / S, 1) for c in red_cols(r, int(168 * S), int(174 * S), int(440 * S), int(495 * S))])
print("== matrix panel pink edges (row 170..172) ==")
def pink_cols(img, y0, y1, x0, x1):
    reg = img[y0:y1, x0:x1]
    m = (reg[:, :, 0] > 200) & (reg[:, :, 1] < 215) & (reg[:, :, 2] < 215) & (reg[:, :, 0] - reg[:, :, 1] > 25)
    cols = np.where(m.any(axis=0))[0]
    return [c + x0 for c in cols]
print(" frame:", pink_cols(f, 168, 174, 200, 400))
print(" render:", [round(c / S, 1) for c in pink_cols(r, int(168 * S), int(174 * S), int(200 * S), int(400 * S))])
print("== matrix vertical (col 300) ==")
def pink_rows(img, x0, x1, y0, y1):
    reg = img[y0:y1, x0:x1]
    m = (reg[:, :, 0] > 200) & (reg[:, :, 1] < 215) & (reg[:, :, 2] < 215) & (reg[:, :, 0] - reg[:, :, 1] > 25)
    rows = np.where(m.any(axis=1))[0]
    return [rr + y0 for rr in rows]
print(" frame:", pink_rows(f, 298, 302, 70, 290))
print(" render:", [round(rr / S, 1) for rr in pink_rows(r, int(298 * S), int(302 * S), int(70 * S), int(290 * S))])
