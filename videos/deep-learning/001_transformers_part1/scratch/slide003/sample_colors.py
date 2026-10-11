from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_003.jpg').convert('RGB')
a = np.asarray(im)
def sample(name, y0,y1,x0,x1, cond=None):
    reg = a[y0:y1, x0:x1].reshape(-1,3).astype(int)
    if cond is not None:
        m = cond(reg)
        reg = reg[m]
    if len(reg)==0: print(name, "none"); return
    med = np.median(reg, axis=0).astype(int)
    print(f"{name}: median RGB={tuple(med)} hex=#{med[0]:02X}{med[1]:02X}{med[2]:02X} n={len(reg)}")

# title ink (strong red pixels)
sample("title ink", 70, 99, 223, 621, lambda p: (p[:,0]>150)&(p[:,1]<80)&(p[:,2]<80))
# agenda ink (blue)
sample("agenda ink", 172, 311, 111, 381, lambda p: (p[:,2]>130)&(p[:,0]<90))
# badge fill
sample("badge fill", 58, 86, 877, 911, lambda p: (p[:,0]>200)&(p[:,1]>200))
# background
sample("background", 350, 500, 500, 700)
# frame line (left border)
sample("frame line", 100, 500, 39, 42, lambda p: (p[:,0]>120)&(p[:,0]-p[:,1]>50))
# bottom line
sample("bottom line", 537, 540, 100, 900)
# badge numeral ink (dark pixels in badge)
sample("badge numeral", 60, 85, 878, 910, lambda p: (p[:,0]<100)&(p[:,1]<100))
# top border rows?
red = (a[...,0].astype(int)>120)&(a[...,0].astype(int)-a[...,1]>50)&(a[...,0].astype(int)-a[...,2]>50)
for y in range(42, 52):
    print("row", y, "red count:", int(red[y].sum()), "x-extent:", end=" ")
    xs = np.where(red[y])[0]
    print(f"[{xs.min()},{xs.max()}]" if len(xs) else "-")
