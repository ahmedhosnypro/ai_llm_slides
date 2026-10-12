from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def runs(bools, min_len=2):
    out, s = [], None
    for i, v in enumerate(bools):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= min_len: out.append((s, i-1))
            s = None
    if s is not None: out.append((s, len(bools)-1))
    return out

# 1) diagram border frame: the red rectangle around white content. Scan the middle
#    column band (x 200..700) for narrow red rows near top y 55..75 and bottom y 500..525.
red = (r - g > 55) & (r - b > 55)
print("== narrow red rows in x200..700 (top/bottom frame hunt) ==")
rowcnt = red[:, 200:700].sum(axis=1)
for y in list(range(50, 80)) + list(range(495, 525)):
    if 20 < rowcnt[y] < 400: print("  row", y, int(rowcnt[y]))

print("== narrow red cols in y150..250 (left/right frame hunt, avoids bars) ==")
colcnt = red[150:250, :].sum(axis=0)
for x in list(range(60, 110)) + list(range(900, 960)):
    if 20 < colcnt[x] < 200: print("  col", x, int(colcnt[x]))

# 2) tan softmax bar: row profile at x=200 (left of circles)
tan = (abs(r-245)<12)&(abs(g-203)<15)&(abs(b-167)<18)
print("== tan bar rows at col 200 ==", runs(tan[:,200], 3))
print("== tan bar cols at row 95 ==", runs(tan[95,:], 3))

# 3) rose encoder container: row profile at col 200
rose = (abs(r-205)<18)&(abs(g-92)<22)&(abs(b-92)<22)
print("== rose rows at col 120 ==", runs(rose[:,120], 3))
print("== rose cols at row 300 ==", runs(rose[300,:], 3))

# 4) dark red bars: col profile at row within bar1 (~y 283)
darkred = (r>140)&(r<215)&(g<75)&(b<75)
print("== darkred rows at col 700 ==", runs(darkred[:,700], 2))
print("== darkred cols at row 285 ==", runs(darkred[285,:], 3)[:3], "...", runs(darkred[285,:],3)[-3:])

# 5) navy circles: profile at row 95 (circle centers)
navy = (r<90)&(g<90)&(b>95)&(b<190)
print("== navy cols at row 95 ==", runs(navy[95,:], 3))
print("== navy rows at col 437 (circle1 cx?) ==", runs(navy[:,437], 3))

# 6) pink container: row profile at col 200
pink = (abs(r-250)<10)&(abs(g-219)<14)&(abs(b-216)<14)
print("== pink rows at col 700 ==", runs(pink[:,700], 3))
print("== pink cols at row 430 ==", runs(pink[430,:], 3))

# 7) light blue output row: row profile at col 700
lblu = (abs(r-214)<16)&(abs(g-234)<12)&(abs(b-248)<10)
print("== lightblue rows at col 700 ==", runs(lblu[:,700], 3))
print("== lightblue cols at row 242 ==", runs(lblu[242,:], 3))

# 8) peach position row
peach = (abs(r-253)<8)&(abs(g-235)<12)&(abs(b-208)<14)
print("== peach rows at col 700 ==", runs(peach[:,700], 3))
print("== peach cols at row 487 ==", runs(peach[487,:], 3))
