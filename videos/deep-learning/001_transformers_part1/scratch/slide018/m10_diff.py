from PIL import Image, ImageChops
import collections
a = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
b = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_018.jpg').convert('RGB')
pa, pb = a.load(), b.load()
W,H = a.size
diff = [[0]*W for _ in range(H)]
n=0
for y in range(H):
    for x in range(W):
        ra,ga,ba = pa[x,y]; rb,gb,bb = pb[x,y]
        d = abs(ra-rb)+abs(ga-gb)+abs(ba-bb)
        if d > 90:
            diff[y][x]=1; n+=1
print("diff px:", n, "of", W*H)
# cluster into bbox grid cells
cc=collections.Counter()
for y in range(H):
    for x in range(W):
        if diff[y][x]: cc[(x//24*24, y//24*24)]+=1
# merge into a coarse map
print("== coarse diff map (24px cells, #=dense, +=sparse, .=none) ==")
xs = sorted(set(x for x,y in cc)); ys = sorted(set(y for x,y in cc))
for gy in range(0, H, 24):
    row=""
    for gx in range(0, W, 24):
        c = cc.get((gx,gy),0)
        row += "#" if c>150 else ("+" if c>25 else ("." if c>0 else " "))
    print(f"{gy:3d} {row}")
