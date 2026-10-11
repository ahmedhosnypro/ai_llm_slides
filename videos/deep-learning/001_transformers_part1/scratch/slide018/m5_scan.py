from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
px = im.load()

def bbox_of(pred, x0,y0,x1,y1,label):
    pts=[(x,y) for y in range(y0,y1) for x in range(x0,x1) if pred(*px[x,y])]
    if not pts: print(label, None); return
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    print(label, "bbox", (min(xs),min(ys),max(xs),max(ys)), "n=",len(pts))
    # per-row density to see box shape
    rc=collections.Counter(y for x,y in pts)
    rows=[ (y,n) for y,n in sorted(rc.items()) if n>50 ]
    print("  dense rows(>50):", rows[:6], "...", rows[-6:] if len(rows)>6 else "")

bbox_of(lambda r,g,b: abs(r-242)<15 and abs(g-198)<15 and abs(b-153)<17, 20,85,560,220, "PEACH banner fill")
bbox_of(lambda r,g,b: abs(r-222)<10 and abs(g-205)<10 and abs(b-187)<10, 20,140,560,230, "TAN box fill")
bbox_of(lambda r,g,b: abs(r-200)<16 and abs(g-126)<18 and abs(b-87)<18, 600,330,760,400, "ORANGE MHA fill")
bbox_of(lambda r,g,b: r>200 and g>200 and b<120, 600,230,820,340, "YELLOW band")

print("== what is at x30-60, y140-215? sample ==")
c=collections.Counter()
for y in range(140,215):
    for x in range(28,62): c[px[x,y]]+=1
print(c.most_common(6))

print("== banner border: column scan x70..76 and x486..492, y100..150 ==")
for x in [69,70,71,72,73,74,487,488,489,490]:
    col=[px[x,y] for y in range(100,150)]
    c=collections.Counter(col)
    print("x",x,c.most_common(3))
