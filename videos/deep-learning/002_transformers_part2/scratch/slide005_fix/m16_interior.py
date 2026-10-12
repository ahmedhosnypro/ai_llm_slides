from PIL import Image
F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
px = F.load()
def cls(x,y):
    r,g,b = px[x,y]
    L = 0.299*r+0.587*g+0.114*b
    if L >= 248: return '.'
    if L >= 238: return ':'
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
# interior corridor: inset top border down to h circle
dump(440, 530, 236, 350, 2, "inset-interior corridor (down to h circle)")
