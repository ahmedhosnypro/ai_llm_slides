from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
px = F.load()
def reddish(x,y):
    r,g,b = px[x,y]
    return r>140 and (r-g)>45 and (r-b)>45
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
# d2 final approach: x290-312, y342-368 (border at x311; expect dashes to (311,360))
dump(reddish, 290, 312, 343, 368, "d2 final approach (loose)")
# d1 start zone: x495-525, y232-256 (inset corner at 506.5,236; first strict dash 519,254)
dump(reddish, 495, 525, 230, 256, "d1 start zone (loose)")
# d2 start zone: x192-208, y255-272 (inset corner 199.8,258; first strict dash 205,270)
dump(reddish, 192, 208, 254, 272, "d2 start zone (loose)")
