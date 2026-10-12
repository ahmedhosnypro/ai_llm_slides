# m15_fine.py — fine ASCII maps with loose threshold (catch JPEG-washed faint strokes)
from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
px = F.load()
def cls(x,y):
    r,g,b = px[x,y]
    L = 0.299*r+0.587*g+0.114*b
    if L >= 248: return '.'
    if L >= 238: return ':'   # very faint
    if L >= 225: return '-'
    if r>140 and g<70 and b<70: return 'R'
    if r>150 and 70<=g<=175 and (r-g)>25: return 'p'
    if L < 120: return '#'
    return 'o'
def dump(x0,x1,y0,y1,step=1,label=""):
    print(f"--- {label} x{x0}..{x1} y{y0}..{y1} step{step} ---")
    print("     " + "".join(str((x//10)%10) for x in range(x0,x1+1,step)))
    for y in range(y0,y1+1,step):
        print(f"{y:4d} " + "".join(cls(x,y) for x in range(x0,x1+1,step)))
# 1. below banner1: does ANY stroke run down from it? (loose threshold)
dump(455, 520, 140, 200, 1, "banner1-bottom corridor (loose)")
# 2. h-circle region: tan arrowhead + black curve + circle
dump(455, 525, 315, 400, 1, "h-circle region")
