from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
white = (r>235)&(g>235)&(b>235)

def region_bbox(x0,y0,x1,y1):
    sub = white[y0:y1, x0:x1]
    ys,xs = np.nonzero(sub)
    return (x0+int(xs.min()), y0+int(ys.min()), x0+int(xs.max()), y0+int(ys.max()))

# left top box: search x 60..460, y 80..250
print("leftbox white bbox:", region_bbox(60,80,460,250))
print("rightbox white bbox:", region_bbox(460,80,820,250))
# decision box: y 250..345
sub = white[250:345, 60:900]
ys,xs = np.nonzero(sub)
print("decision box white bbox:", (60+int(xs.min()), 250+int(ys.min()), 60+int(xs.max()), 250+int(ys.max())))
# diagram box: y 350..505
sub = white[350:505, 400:820]
ys,xs = np.nonzero(sub)
print("diagram box white bbox:", (400+int(xs.min()), 350+int(ys.min()), 400+int(xs.max()), 350+int(ys.max())))

# pale yellow region
py = (r>215)&(g>215)&(b<200)&(r>100)&(abs(r-g)<25)
ys,xs = np.nonzero(py)
print("pale-yellow bbox:", (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())), "n=", len(xs))
# tan region (callout): brownish
tan = (r>170)&(r<225)&(g>130)&(g<205)&(b>110)&(b<190)&(r>b+20)
ys,xs = np.nonzero(tan[380:470, 590:860])
if len(xs): print("tan bbox:", (590+int(xs.min()), 380+int(ys.min()), 590+int(xs.max()), 380+int(ys.max())), "n=", len(xs))

# sample border colors: left edge of left top box
print("\nborder samples leftbox (x=86..92, y=160):", [tuple(a[160,x]) for x in range(84,94)])
print("border samples leftbox top (x=200, y=86..92):", [tuple(a[y,200]) for y in range(84,94)])
print("left vertical line x=56..62 @y=150:", [tuple(a[150,x]) for x in range(54,64)])
print("right border of right box @y=160, x=776..788:", [tuple(a[160,x]) for x in range(776,790)])
