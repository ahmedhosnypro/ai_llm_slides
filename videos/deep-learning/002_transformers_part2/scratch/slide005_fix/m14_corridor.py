# m14_corridor.py — ASCII ink maps of the connector regions in the ORIGINAL frame
from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
W,H = F.size; px = F.load()
def lum(x,y):
    r,g,b = px[x,y]; return 0.299*r+0.587*g+0.114*b
def cls(x,y):
    r,g,b = px[x,y]
    L = 0.299*r+0.587*g+0.114*b
    if L >= 225: return '.'
    if r>140 and g<70 and b<70: return 'R'      # red family C00000
    if r>150 and 70<=g<=170 and (r-g)>25 and (r-b)>25: return 'p'  # pink family
    if L < 120: return '#'                       # dark ink
    return 'o'                                   # mid ink
def dump(x0,x1,y0,y1,step=1,label=""):
    print(f"--- {label} x{x0}..{x1} y{y0}..{y1} step{step} ---")
    hdr = "     " + "".join(str((x//100)%10) for x in range(x0,x1+1,step))
    hdr2= "     " + "".join(str((x//10)%10) for x in range(x0,x1+1,step))
    print(hdr); print(hdr2)
    for y in range(y0,y1+1,step):
        print(f"{y:4d} " + "".join(cls(x,y) for x in range(x0,x1+1,step)))
# Corridor 1: banner1 bottom -> MHA inset top (the two pink connectors)
dump(418, 575, 138, 262, 2, "corridor1: banner1-bottom to MHA-inset-top")
