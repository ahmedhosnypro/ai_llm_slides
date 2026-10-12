# m38_elbow.py — trace the original's gray elbow lines: where do the y330/y336
# horizontals start, and where does the connect_h line really end?
from PIL import Image
from collections import defaultdict

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
FR = Image.open(VID + "/unique_slides/slide_005.jpg").convert("RGB")
RD = Image.open(VID + "/recreated_pptx/qa/slide005/render_4.png").convert("RGB")
SX, SY = 2.16770, 2.17684
po, pr = FR.load(), RD.load()


def grayish(p):
    r, g, b = p
    L = 0.299 * r + 0.587 * g + 0.114 * b
    return 120 < L < 225 and abs(r - g) < 30 and abs(g - b) < 30


def row_runs(p, y, x0, x1, pred):
    xs = [x for x in range(x0, x1) if pred(p[x, y])]
    runs = []
    if xs:
        s = pv = xs[0]
        for x in xs[1:]:
            if x - pv > 2:
                runs.append((s, pv))
                s = x
            pv = x
        runs.append((s, pv))
    return runs


print("ORIG gray-ish runs per row (x380..512):")
for y in range(318, 346):
    rr = row_runs(po, y, 380, 512, grayish)
    if rr:
        print(f"  y{y}: {rr}")
print("REND4 gray-ish runs per row (mapped):")
for y in range(318, 346):
    xs = []
    for x in range(380, 512):
        rx, ry = round((x - 18.0787) * SX), round((y - 0.4700) * SY)
        if grayish(pr[rx, ry]):
            xs.append(x)
    runs = []
    if xs:
        s = pv = xs[0]
        for x in xs[1:]:
            if x - pv > 2:
                runs.append((s, pv))
                s = x
            pv = x
        runs.append((s, pv))
    if runs:
        print(f"  y{y}: {runs}")

print("\nORIG darker-ink runs per row y300..340 x380..512 (lum<200):")
def inky(p):
    r, g, b = p
    return 0.299 * r + 0.587 * g + 0.114 * b < 200
for y in range(300, 341, 2):
    rr = row_runs(po, y, 380, 512, inky)
    if rr:
        print(f"  y{y}: {rr}")
