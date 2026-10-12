#!/usr/bin/env python3
"""Final detail scans for slide_026."""
from PIL import Image
from collections import deque

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg').convert('RGB')
W, H = im.size
px = im.load()

def dark_rows(x0, x1, y0, y1, thresh=170):
    """print rows containing dark pixels and their x-extent"""
    print(f"--- dark rows x{x0}-{x1} y{y0}-{y1} ---")
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1) if sum(px[x, y]) < thresh*3]
        if xs:
            print(f"  y={y}: x {min(xs)}..{max(xs)} n={len(xs)}")

def nonbg_rows(x0, x1, y0, y1, bg=(196, 220, 160), tol=16):
    print(f"--- non-{bg} rows x{x0}-{x1} y{y0}-{y1} ---")
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1) if any(abs(px[x, y][i]-bg[i]) > tol for i in range(3))]
        if xs:
            print(f"  y={y}: x {min(xs)}..{max(xs)} n={len(xs)}")

# a. PSU/24V area (bg = TIDA green)
nonbg_rows(400, 470, 418, 466)
print()
nonbg_rows(527, 660, 418, 466)

# b. blue->host gap: dark rows (labels + lines)
dark_rows(381, 394, 242, 392)
print("--- blue box right edge labels region: nonbg vs BLUE fill ---")
nonbg_rows(381, 394, 242, 392, bg=(14, 190, 234), tol=30)

# c. right panel bottom: peach sincos box bbox
def comps_pred(x0, y0, x1, y1, pred, min_size=60):
    seen = set(); out = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x, y) in seen or not pred(px[x, y]):
                continue
            q = deque([(x, y)]); seen.add((x, y))
            mnx = mxx = x; mny = mxy = y; n = 0
            while q:
                cx, cy = q.popleft(); n += 1
                mnx = min(mnx, cx); mxx = max(mxx, cx)
                mny = min(mny, cy); mxy = max(mxy, cy)
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    p = (cx+dx, cy+dy)
                    if p in seen or not (x0 <= p[0] < x1 and y0 <= p[1] < y1):
                        continue
                    if pred(px[p[0], p[1]]):
                        seen.add(p); q.append(p)
            if n >= min_size:
                out.append((n, mnx, mny, mxx, mxy))
    out.sort(reverse=True)
    return out

is_peach = lambda c: c[0] > 225 and 185 < c[1] < 235 and 150 < c[2] < 215 and c[0]-c[2] > 40
print("peach comps right panel:", comps_pred(690, 192, 850, 462, is_peach, 100)[:6])
is_gray = lambda c: 100 < c[0] < 200 and abs(c[0]-c[1]) < 18 and abs(c[1]-c[2]) < 18
print("gray comps (motor):", comps_pred(700, 290, 850, 440, is_gray, 80)[:8])

# d. comparator: exact extent via medium-green pred
is_mgreen = lambda c: 80 < c[0] < 150 and 140 < c[1] < 200 and 100 < c[2] < 160
print("mgreen comps (comparator+):", comps_pred(430, 350, 660, 400, is_mgreen, 60)[:6])

# e. sub-block x bounds in blue box: nonbg vs blue
for yy in (265, 270, 320, 325, 370, 375):
    xs = [x for x in range(232, 380) if any(abs(px[x, yy][i]-(14,190,234)[i]) > 35 for i in range(3))]
    runs = []
    if xs:
        s = xs[0]; p = xs[0]
        for x in xs[1:]:
            if x > p+2:
                runs.append((s, p)); s = x
            p = x
        runs.append((s, p))
    print(f"nonblue runs y={yy}:", runs)

# f. signal lines: connector->panel gap x 668-683
print("--- gap connector->panel: nonbg rows x669-682 (bg=green) ---")
nonbg_rows(669, 683, 240, 400)
print("--- gap blue->host: rows with anything (bg=panel gray E9E9E7) ---")
nonbg_rows(381, 394, 242, 392, bg=(233, 233, 231), tol=14)

# g. host->TIDA overlap region lines: y where lines cross x 414-460 (bg green)
print("--- TIDA left strip x414-464 (bg green): rows 245-400 ---")
nonbg_rows(414, 464, 245, 400)

# h. TIDA right strip: outputs labels region x 580-650 (bg green), rows 245-400
print("--- TIDA right strip x582-648 (bg green): rows 245-400 ---")
nonbg_rows(582, 648, 245, 400)
