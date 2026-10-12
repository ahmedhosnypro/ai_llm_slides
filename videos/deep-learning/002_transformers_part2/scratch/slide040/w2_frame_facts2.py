from PIL import Image
import numpy as np
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg"
im = np.array(Image.open(FR).convert("RGB")).astype(int)

print("== 1. eq1/eq2 rectangle scan (rows 295..395, x 150..620) ==")
def col_runs(x, y0, y1, thr=215):
    col = im[y0:y1, x]
    nonbg = (col.mean(axis=1) < thr)
    best=0; cur=0; bs=None; s=None
    for i,v in enumerate(nonbg):
        if v:
            if cur==0: s=i
            cur+=1
            if cur>best: best,bs=cur,s
        else: cur=0
    return best,(y0+bs if bs is not None else None)
for label,y0,y1 in [("eq1",295,345),("eq2",352,395)]:
    print(f"  {label}: columns with vertical runs >= 18px:")
    hits=[]
    for x in range(150,621):
        L,a = col_runs(x,y0,y1)
        if L>=18: hits.append((x,L,a))
    # compress consecutive
    for x,L,a in hits:
        print(f"    x={x}: run {L}px from y={a}")

print("\n== 2. darkest-pixel color of box strokes ==")
def stroke_color(x0,x1,y0,y1):
    reg = im[y0:y1, x0:x1].reshape(-1,3)
    lum = reg.mean(axis=1)
    idx = np.argsort(lum)[:30]
    return np.median(reg[idx],axis=0)
print(f"  eq3 box left stroke  (x163..167, y405..445): {stroke_color(163,168,405,445)}")
print(f"  eq3 box top stroke   (y398..401, x180..280): {stroke_color(180,280,398,402)}")
print(f"  eq3 box bottom stroke(y444..448, x180..280): {stroke_color(180,280,444,449)}")
print(f"  eq4 box left stroke  (x163..167, y455..473): {stroke_color(163,168,455,473)}")
print(f"  eq4 box right stroke (x369..373, y455..473): {stroke_color(369,374,455,473)}")
print(f"  eq4 box bottom stroke(y473..477, x200..360): {stroke_color(200,360,473,478)}")
print(f"  eq4 box top stroke   (y449..453, x200..360): {stroke_color(200,360,449,454)}")

print("\n== 3. L3 stroke profile rows 174..190 (x 85..455) ==")
for y in range(174,191):
    row = im[y,85:456]
    dark = row.mean(axis=1)<200
    n=dark.sum()
    if n>0:
        idx=np.where(dark)[0]
        med=np.median(row[dark],axis=0)
        # coverage pattern: longest run of dark
        best=0;cur=0
        for v in dark:
            cur = cur+1 if v else 0
            best=max(best,cur)
        print(f"  y={y}: n={n} span {85+idx[0]}..{85+idx[-1]} longestrun={best} med {med}")
print("  leftmost-ink check rows 170..186, x 85..115:")
for y in range(170,187):
    row = im[y,85:116]
    dark = row.mean(axis=1)<210
    if dark.sum()>0:
        idx=np.where(dark)[0]
        print(f"    y={y}: cols {85+idx[0]}..{85+idx[-1]} n={dark.sum()} med {np.median(row[dark],axis=0)}")

print("\n== 4. mystery ink rows 153..158 x 495..835 (L2 red zone) ==")
for y in range(152,160):
    row = im[y,495:836]
    dark = row.mean(axis=1)<200
    n=dark.sum()
    if n>0:
        idx=np.where(dark)[0]
        best=0;cur=0
        for v in dark:
            cur=cur+1 if v else 0
            best=max(best,cur)
        print(f"  y={y}: n={n} span {495+idx[0]}..{495+idx[-1]} longestrun={best} med {np.median(row[dark],axis=0)}")

print("\n== 5. italic slant — clean per-row leftmost/rightmost method ==")
def slant(x0,x1,y0,y1,hue):
    """leftmost ink x at top band vs bottom band of glyph height"""
    rows_top=[]; rows_bot=[]
    yy0,yy1 = y0,y1
    for y in range(yy0,yy1):
        row = im[y,x0:x1]
        r,g,b = row[:,0],row[:,1],row[:,2]
        if hue=="red": m=(r>g+40)&(r>90)&(b<120)
        elif hue=="blue": m=(b>r+40)&(b>90)&(r<150)
        else: m=row.mean(axis=1)<150
        idx=np.where(m)[0]
        if len(idx)>0:
            rows_top.append((y,x0+idx[0],x0+idx[-1]))
    if len(rows_top)<6: return None
    h=len(rows_top); q=max(1,h//5)
    top=rows_top[:q]; bot=rows_top[-q:]
    tl=np.mean([t[1] for t in top]); bl=np.mean([t[1] for t in bot])
    tr=np.mean([t[2] for t in top]); br=np.mean([t[2] for t in bot])
    return f"rows {rows_top[0][0]}..{rows_top[-1][0]} Ledge top {tl:.1f} bot {bl:.1f} (drift {tl-bl:+.1f})  Redge top {tr:.1f} bot {br:.1f} (drift {tr-br:+.1f})"
print("  strictly (blue L1):", slant(497,562,126,154,"blue"))
print("  mean (blue L1):     ", slant(632,674,126,154,"blue"))
print("  variance,(blue L1): ", slant(788,872,126,154,"blue"))
print("  convert (red L2):   ", slant(674,734,153,178,"red"))
print("  Minimizes (red L3): ", slant(318,405,168,190,"red"))
print("  variance (red L3):  ", slant(102,172,168,190,"red"))

print("\n== 6. title ink center + gamma/beta exact boxes ==")
reg = im[60:110, 300:720]
dark = reg.mean(axis=2)<160
idx = np.where(dark.any(axis=0))[0]
print(f"  title ink x {300+idx[0]}..{300+idx[-1]} (center {300+(idx[0]+idx[-1])/2})")
rows = np.where(dark.any(axis=1))[0]
print(f"  title ink y {60+rows[0]}..{60+rows[-1]}")
