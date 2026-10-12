from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
px = F.load()
def dred(x,y):
    r,g,b = px[x,y]
    return r>115 and g<120 and (r-g)>40 and (r-b)>40
from collections import defaultdict
def dump(pred, X0,X1,Y0,Y1,label):
    rows=defaultdict(list)
    for y in range(Y0,Y1):
        for x in range(X0,X1):
            if pred(x,y): rows[y].append(x)
    print(f"--- {label} ---")
    hit=False
    for y in sorted(rows):
        hit=True; print(" y",y,rows[y])
    if not hit: print(" (none)")
# d2 start zone (dark red): x192-210, y252-272
dump(dred, 192, 210, 252, 272, "d2 start zone (dark-red)")
# d3 tail zone: x198-215, y450-472 (does it reach the inset edge/corner?)
dump(dred, 196, 216, 448, 474, "d3 tail zone (dark-red)")
# d1 first-dash zone for completeness x505-520 y240-256
dump(dred, 505, 522, 238, 258, "d1 start zone (dark-red)")
