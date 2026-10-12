from PIL import Image
import numpy as np
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg"
RD = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide040/render_3.png"
im = np.array(Image.open(FR).convert("RGB")).astype(int)
rm = np.array(Image.open(RD).convert("RGB")).astype(int)
print(f"render {rm.shape[1]}x{rm.shape[0]}")

def runs_of(mask, x0):
    out=[];s=None
    for i,v in enumerate(mask):
        if v and s is None: s=i
        if not v and s is not None: out.append((x0+s,x0+i-1)); s=None
    if s is not None: out.append((x0+s,x0+len(mask)-1))
    return out

print("== 1. frame row 156..161 x 480..900 exact runs (L2 underline?) ==")
for y in range(155,162):
    row = im[y,480:901]
    dark = row.mean(axis=1)<205
    rr = runs_of(dark,480)
    long_runs = [r for r in rr if r[1]-r[0]>=25]
    if long_runs:
        segs=[]
        for a,b in long_runs:
            med=np.median(im[y,a:b+1],axis=0)
            segs.append(f"{a}..{b} med{med.astype(int)}")
        print(f"  y={y}: runs>=25px: {segs}")

print("\n== 2. frame L1 blue ink columns (find word windows) ==")
band = im[126:152, 88:900]
r,g,b = band[:,:,0],band[:,:,1],band[:,:,2]
blue = (b>r+40)&(b>90)&(r<150)
cols = np.where(blue.any(axis=0))[0]+88
# group into words (gaps>4px)
words=[];s=cols[0];p=cols[0]
for c in cols[1:]:
    if c-p>4: words.append((s,p)); s=c
    p=c
words.append((s,p))
print(f"  blue words x-ranges: {words}")
print(f"  blue ink rows: {126+np.where(blue.any(axis=1))[0][0]}..{126+np.where(blue.any(axis=1))[0][-1]}")

print("\n== 3. italic slant clean (exclude underline rows) ==")
def slant(x0,x1,y0,y1,hue):
    data=[]
    for y in range(y0,y1):
        row=im[y,x0:x1]
        rr,gg,bb=row[:,0],row[:,1],row[:,2]
        if hue=="red": m=(rr>gg+40)&(rr>90)&(bb<120)
        elif hue=="blue": m=(bb>rr+40)&(bb>90)&(rr<150)
        idx=np.where(m)[0]
        if len(idx)>0: data.append((y,x0+idx[0],x0+idx[-1]))
    if len(data)<5: return "insufficient"
    q=max(1,len(data)//4)
    top=data[:q]; bot=data[-q:]
    tl=np.mean([t[1] for t in top]); bl=np.mean([t[1] for t in bot])
    tr=np.mean([t[2] for t in top]); br=np.mean([t[2] for t in bot])
    return f"rows {data[0][0]}..{data[-1][0]}: L top {tl:.1f} bot {bl:.1f} drift {tl-bl:+.1f} | R top {tr:.1f} bot {br:.1f} drift {tr-br:+.1f}"
for w in words[:8]:
    print(f"  blue word x{w[0]}..{w[1]}:", slant(w[0],w[1]+1,128,150,"blue"))
print("  convert (red L2) x674..734 rows154..176:", slant(674,735,154,176,"red"))
print("  Minimizes x318..405 rows168..182:", slant(318,406,168,182,"red"))
print("  Loss. x406..440 rows168..182:", slant(406,441,168,182,"red"))
print("  variance x102..172 rows170..182:", slant(102,173,170,182,"red"))

print("\n== 4. RENDER L3 underline state (rows 386..402, x 140..930) ==")
for y in range(386,403):
    row = rm[y,140:931]
    dark = row.mean(axis=1)<205
    n=dark.sum()
    if n>0:
        rr = runs_of(dark,140)
        longr=[f"{a}..{b}" for a,b in rr if b-a>=15]
        print(f"  y={y}: n={n} longruns {longr[:6]}")

print("\n== 5. RENDER L2 zone rows 300..320 x 700..1400 (any underline?) ==")
for y in range(300,321):
    row = rm[y,700:1401]
    dark = row.mean(axis=1)<205
    n=dark.sum()
    if n>20:
        rr=runs_of(dark,700)
        longr=[f"{a}..{b}" for a,b in rr if b-a>=25]
        if longr: print(f"  y={y}: n={n} longruns {longr[:5]}")

print("\n== 6. frame: does L2 red phrase have text-underline at y~157 under which words? zoom ==")
# exact: continuous run boundaries at y=157
row = im[157,480:901]
dark = row.mean(axis=1)<205
rr = runs_of(dark,480)
print(f"  y=157 all runs: {[(a,b) for a,b in rr if b-a>=3]}")
row = im[156,480:901]
dark = row.mean(axis=1)<205
print(f"  y=156 all runs: {[(a,b) for a,b in runs_of(dark,480) if b-a>=3]}")
