from PIL import Image
import numpy as np

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

def runs(m, minlen=2):
    out=[]; x=0; N=len(m)
    while x<N:
        if m[x]:
            x0=x
            while x<N and m[x]: x+=1
            if x-x0>=minlen: out.append((x0,x-1))
        else: x+=1
    return out
def hruns(y, test, label, minlen=2):
    print("y=%3d %-14s" % (y,label), runs(test(y), minlen))
def vruns(x, test, label, minlen=2):
    print("x=%3d %-14s" % (x,label), runs(test(x), minlen))
def hc(c,tol=18):
    return lambda y: (np.abs(a[y,:,0]-c[0])<tol)&(np.abs(a[y,:,1]-c[1])<tol)&(np.abs(a[y,:,2]-c[2])<tol)
def vc(c,tol=18):
    return lambda x: (np.abs(a[:,x,0]-c[0])<tol)&(np.abs(a[:,x,1]-c[1])<tol)&(np.abs(a[:,x,2]-c[2])<tol)

TAN=(216,200,184)
print("== tan box ==")
for y in [300, 330, 360, 390, 410, 425]:
    hruns(y, hc(TAN), "tan")
for x in [180, 200, 220, 240]:
    vruns(x, vc(TAN), "tan")

print("== gold F5C242 ==")
for y in [315, 330, 345, 360, 375, 390, 405, 415]:
    hruns(y, hc((245,194,66),24), "gold")
for x in [140, 480, 500, 520]:
    vruns(x, vc((245,194,66),24), "gold")

print("== pink-lavender input cells F6DAF3 / EAE4EE ==")
for y in [330, 350, 370, 390, 410]:
    hruns(y, hc((246,218,243),14), "pinkcell")
    hruns(y, hc((234,228,238),10), "lavcell")

print("== spec green B6D7A8 / yellow FFE066 / pink F4CCCC cells ==")
for y in [330, 350, 370, 390, 410]:
    hruns(y, hc((182,215,168),14), "grncell")
    hruns(y, hc((255,224,102),18), "yelcell")
    hruns(y, hc((244,204,204),14), "pinksp")

print("== striped K bars F9FF96 ==")
for y in [330, 358, 386, 414]:
    hruns(y, hc((249,255,150),16), "kbar")

print("== circled-X nodes FCE8E8 ==")
for y in [330, 358, 386, 414]:
    hruns(y, hc((252,232,232),10), "node")
