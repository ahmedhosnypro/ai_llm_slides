from PIL import Image
R = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide005/render_4.png").convert("RGB")
W,H = R.size; px = R.load()
def is_pinkp(x,y):
    r,g,b = px[x,y]
    return r>150 and 70<g<185 and (r-g)>25 and (r-b)>25
# 1. locate the 10 "pink" px in the corridor
pts=[(x,y) for y in range(310,505) for x in range(998,1024) if is_pinkp(x,y)]
print("pink-ish px in corridor:", pts[:15])
# 2. connect_tan path: probe ON the segment (999,503)
def near(pred,cx,cy,rad=6):
    best=None
    for y in range(int(cy-rad),int(cy+rad+1)):
        for x in range(int(cx-rad),int(cx+rad+1)):
            if 0<=x<W and 0<=y<H and pred(x,y):
                d=((x-cx)**2+(y-cy)**2)**0.5
                if best is None or d<best[0]: best=(round(d,2),x,y)
    return best
print("connect_tan @ (999,503):", near(is_pinkp,999,503,7))
print("connect_tan @ (988,478):", near(is_pinkp,988,478,7))
print("connect_tan @ (946,408):", near(is_pinkp,946,408,7))
print("connect_tan @ (902,383):", near(is_pinkp,902,383,7))
print("connect_tan @ (880,379):", near(is_pinkp,880,379,7))
# 3. head alone: window y735..762 (above the ring top 765.9)
def darkbrownp(x,y):
    r,g,b = px[x,y]
    return r<150 and g<110 and b<90 and (r-b)>30 and (0.299*r+0.587*g+0.114*b)<120
xs=[];ys=[]
for y in range(735,763):
    for x in range(1015,1042):
        if darkbrownp(x,y): xs.append(x); ys.append(y)
print("head-only ink bbox: x%d..%d y%d..%d (target x1023.3..1034.6 base y743.1 tip y763.1)"%(min(xs),max(xs),min(ys),max(ys)) if xs else "none")
