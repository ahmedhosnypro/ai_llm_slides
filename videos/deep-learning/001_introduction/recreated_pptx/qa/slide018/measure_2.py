from PIL import Image
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()

def isred(r,g,b): return r>150 and g<80 and b<80
def isdark(r,g,b): return r<110 and g<110 and b<110
def isnavy(r,g,b): return b>90 and b-r>60 and g<b and r<90
def isblack(r,g,b): return r<60 and g<60 and b<60

# Title full extent
xs=[]; ys=[]
for y in range(55,100):
    for x in range(100,860):
        r,g,b = px[x,y]
        if isred(r,g,b): xs.append(x); ys.append(y)
print("TITLE ink bbox x", min(xs), max(xs), "y", min(ys), max(ys), "center_x", (min(xs)+max(xs))/2)

# Panel: find white panel + red border. scan row 300 for red border columns
row=300
reds=[x for x in range(0,W) if isred(*px[x,row])]
print("row300 red columns:", reds[:8], "...", reds[-8:] if len(reds)>8 else "")
# panel top: scan col 480 for red rows
col=480
redr=[y for y in range(90,470) if isred(*px[col,y])]
print("col480 red rows 90..470:", redr)

# Training Data ellipse: peach fill around x78..209,y137..195 in parent. scan row 165
def ispeach(r,g,b): return r>230 and 200<g<235 and 160<b<210
row=165
p=[x for x in range(50,300) if ispeach(*px[x,row])]
print("row165 peach x:", (min(p),max(p)) if p else None)
col=143
p=[y for y in range(110,230) if ispeach(*px[col,y])]
print("col143 peach y:", (min(p),max(p)) if p else None)

# black bar bottom
for y in [515,518,520,525,535,538]:
    r=0
    for x in range(0,W,4):
        if isblack(*px[x,y]): r+=1
    print("y",y,"blackfrac", r/(W/4))
# black bar extent at y525
xs=[x for x in range(0,W) if isblack(*px[x,525])]
print("y525 black x", (min(xs),max(xs)) if xs else None, len(xs))
