from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()

def bbox(pred, x0,y0,x1,y1):
    xs=[];ys=[]
    for y in range(y0,y1):
        for x in range(x0,x1):
            if pred(*px[x,y]): xs.append(x); ys.append(y)
    if not xs: return None
    return (min(xs),max(xs),min(ys),max(ys))

def show(name, bb): print(f"{name}: x{bb[0]}..{bb[1]} y{bb[2]}..{bb[3]}  w{bb[1]-bb[0]+1} h{bb[3]-bb[2]+1}" if bb else f"{name}: NONE")

# pipeline boxes by fill color (sample first, then bbox)
print("sample colors:", px[170,236], px[340,236], px[490,236], px[650,236], px[800,230], px[140,240])
def near(c, t, tol=18): return all(abs(a-b)<=tol for a,b in zip(c,t))
# measure each box via known approximate centers, scanning outward
def boxscan(cx, cy, name):
    # find fill extents by walking from center while color near center color
    base = px[cx,cy]
    x0=cx; x1=cx; y0=cy; y1=cy
    while x0>0 and near(px[x0-1,cy], base): x0-=1
    while x1<W-1 and near(px[x1+1,cy], base): x1+=1
    while y0>0 and near(px[cx,y0-1], base): y0-=1
    while y1<H-1 and near(px[cx,y1+1], base): y1+=1
    print(f"{name}: fill x{x0}..{x1} y{y0}..{y1} (w{x1-x0+1} h{y1-y0+1}) color{base}")

boxscan(170,236,"box_pre")
boxscan(340,236,"box_extraction")
boxscan(490,236,"box_selection")
boxscan(650,236,"box_classification")
boxscan(800,230,"box_classifier_output")
# training ellipse peach
print("ellipse sample:", px[110,150])
def ispeach(r,g,b): return r>235 and 200<g<235 and 160<b<215
show("training_ellipse_fill", bbox(ispeach, 60,110, 230,220))
# end-to-end chip light blue
print("chip sample:", px[450,143])
def isltblue(r,g,b): return 190<r<225 and 215<g<245 and b>245 or (195<r<225 and 220<g<240 and 245<b<256)
show("endtoend_chip", bbox(lambda r,g,b: 185<r<230 and 210<g<245 and b>235, 330,120, 580,170))
# dashed red container bounds: find red pixels in band y195..280 excluding box fills
def isred(r,g,b): return r>150 and g<80 and b<80
show("container_red", bbox(isred, 100,185, 745,285))
# classifier output tan
def istan(r,g,b): return 175<r<215 and 140<g<180 and 90<b<135
show("classifier_output_tan", bbox(istan, 730,180, 900,290))
# deep model label pale green
print("deeplabel sample:", px[410,290])
def ispalegreen(r,g,b): return 200<r<235 and 235<g<256 and 200<b<235
show("deep_label", bbox(ispalegreen, 250,270, 580,320))
# deep arrow red row
for y in range(265, 310):
    c = sum(1 for x in range(100,760) if isred(*px[x,y]))
    if c>50: print("deep-arrow row y",y,"count",c)
# callout grays
def isgray(r,g,b): return 205<r<230 and 205<g<230 and 205<b<230 and abs(r-g)<8 and abs(g-b)<8
show("callout_row_gray", bbox(isgray, 60,300, 740,380))
# starburst yellow
def isyellow(r,g,b): return r>230 and g>225 and b<160
show("starburst", bbox(isyellow, 720,300, 940,390))
# statement box
show("statement_box_redtext", bbox(isred, 250,380, 600,460))
print("statement sample:", px[300,410], px[430,412])
# navy arc
def isnavy(r,g,b): return b>90 and b-r>60 and r<100
show("navy_arc", bbox(isnavy, 200,120, 800,240))
# curve from ellipse to preproc (red curve) region x60..160 y190..260
show("curve_red", bbox(isred, 60,190, 170,265))
