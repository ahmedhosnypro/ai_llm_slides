from PIL import Image
im = Image.open('render_1-1.png').convert('RGB')
W,H = im.size; S=H/540.0; px=im.load()
def fr(x,y): return px[int(x*S),int(y*S)]
isred = lambda r,g,b: r>150 and r-g>60 and r-b>60
print("panel_bottom band y450..468 at x480:", [(y,fr(480,y)) for y in range(450,469,2)])
print("red rows in y450..470 x300..320:", [y for y in range(450,471) if any(isred(*fr(x,y)) for x in range(300,321))])
print("title stray: red px x75..90 y60..100:", [(x,y) for y in range(60,100) for x in range(75,91) if isred(*fr(x,y))][:6])
print("container top edge: red x-runs per row y194..200:")
for y in range(194,201):
    runs=[];s=None
    for x in range(110,740):
        ok=isred(*fr(x,y))
        if ok and s is None: s=x
        if not ok and s is not None: runs.append((s,x-1)); s=None
    print(" y",y,[r for r in runs if r[1]-r[0]>=0][:12])
print("arc: navy hits per x 210..800 step 6 (y145..215):")
isnavy = lambda r,g,b: b>85 and b-r>55 and r<110
miss=[]
for x in range(210,801,6):
    ys=[y for y in range(145,216) if isnavy(*fr(x,y))]
    if not ys: miss.append(x)
print(" xs with no navy:", miss[:20], "count", len(miss))
print("deep arrow band y266..278 red at x400:", [(y,fr(400,y)) for y in range(266,279)])
