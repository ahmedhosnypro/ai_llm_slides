from PIL import Image
import collections
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
W,H = im.size
px = im.load()

def mode_col(x0,y0,x1,y1):
    c = collections.Counter()
    for y in range(y0,y1):
        for x in range(x0,x1):
            c[px[x,y]] += 1
    return c.most_common(6)

print("== global corners/background ==")
print("TL", px[5,5], "TR", px[W-5,5], "BL", px[5,H-5], "BR", px[W-5,H-5])
print("== banner region approx x58..480 y92..151 ==")
print(mode_col(60,95,200,148))
print("== SDPA inset region x38..202 y216..502: green border? ==")
print(mode_col(38,300,50,400))
print("== MHA inset region x278..518 y194..518 ==")
print(mode_col(280,300,300,400))
print("== right arch encoder MHA area approx x630..730 y355..385 ==")
print(mode_col(632,358,724,382))
print("== yellow band region (parent) x678..787 y251..323 ==")
# count yellowish pixels
ys=0
for y in range(240,330):
    for x in range(670,790):
        r,g,b = px[x,y]
        if r>200 and g>200 and b<120: ys+=1
print("yellowish px in band region:", ys)
print("== red dashed arrow region? scan for red pixels between enc top and dec ==")
reds = collections.Counter()
for y in range(200,330):
    for x in range(700,870):
        r,g,b = px[x,y]
        if r>150 and g<80 and b<80: reds[(x,y)]=(r,g,b)
print("red px count in enc->dec gap:", len(reds))
xs = sorted(set(x for x,y in reds)); 
if xs: print("red x range", min(xs), max(xs))
