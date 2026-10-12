from PIL import Image
import numpy as np
import sys
R = np.asarray(Image.open('recreated_pptx/qa/slide022/render_2.png').convert('RGB')).astype(int)
s = 72/150.0
r, g, b = R[:,:,0], R[:,:,1], R[:,:,2]
lum = (r+g+b)/3
fails = []
def bb(mask, x0,y0,x1,y1,label, gt, tol=4):
    sub = mask[int(y0/s):int(y1/s), int(x0/s):int(x1/s)]
    ys, xs = np.where(sub)
    if not len(ys):
        print(f'{label}: NO INK'); fails.append(label+': no ink'); return None
    res=(x0+xs.min()*s, y0+ys.min()*s, x0+xs.max()*s, y0+ys.max()*s)
    dx0, dx1 = res[0]-gt[0], res[2]-gt[2]
    print(f'{label}: x {res[0]:.1f}..{res[2]:.1f} y {res[1]:.1f}..{res[3]:.1f} | gt {gt} | dx0={dx0:+.1f} dx1={dx1:+.1f}')
    if abs(dx0)>tol or abs(dx1)>tol: fails.append(f'{label}: dx0={dx0:+.1f} dx1={dx1:+.1f}')
    return res
blackish = (lum<120)&(r<130)&(g<130)&(b<130)
redl = (r>120)&(g<110)&(b<110)&(r-g>40)
blu = (b-r>40)&(b>100)
reddish = (r-g>40)&(r-b>30)&(r>120)

print('== title / labels / text ==')
bb(redl, 150,50,850,86, 'title', (228,60,718,82.5))
bb(blu, 290,155,420,180, 'aug label+ul', (300,161,405,173.5))
bb(blu, 660,155,780,180, 'wts label+ul', (670,161,762,173.5))
bb(blackish, 576,408,620,434, 'O/P', (575,416,608,428))
bb(blackish, 640,402,808,423, 'callout l1', (649,408,798,422))
bb(blackish, 640,424,808,443, 'callout l2', (684,426,763,439))
print('== EQ1/EQ2 vectors ==')
bb(blackish, 80,150,120,182, 'X1=', (88,159,117,173))
bb(redl, 170,155,200,178, 'aug red arrow', (180,162,193,169))
bb(reddish, 250,100,280,125, 'red 1 (v2 top)', (258,108,264,119))  # gt corrected: red comp 258..264
bb(reddish, 550,150,585,182, 'red W', (561,159,578,173))
bb(redl, 595,100,620,125, 'red b (wts)', (601,106,613,120))
bb(blackish, 110,100,150,235, 'v1 parens span', (117,112,141,227))
bb(blackish, 246,95,285,245, 'v2 parens span', (248.5,102,273,238))  # gt corrected: parens 248.5/271.5-273
bb(blackish, 590,95,625,245, 'wts parens span', (597,100,619,239))
print('== EQ3 decision ==')
bb(blackish, 85,280,135,306, 'd(', (87,284,108,299))
bb(reddish, 105,282,126,306, 'X red', (110,287,122,302))
bb(reddish, 495,282,528,304, 'big arrow', (500,287,522,299))
bb(reddish, 420,282,462,306, 'b*1', (427,287,456,300))
bb(blackish, 330,292,365,304, 'dots', (337,298,359,300))
bb(blackish, 150,278,190,306, 'WT', (156,282,182,302))
bb(blackish, 188,282,212,306, 'X2', (193,287,206,302))
print('== cases ==')
bb(blu, 548,262,748,287, 'case1', (555,267,671,283))
bb(blu, 548,286,748,308, 'case2', (555,289,672,305))
bb(blu, 548,308,748,330, 'case3', (555,311,741,327))
print('== diagram ==')
cy = (b-r>25)&(b>140)&(g>150)
bb(cy, 400,395,465,445, 'sigma circle', (411,402,450,439))
pur = (b-r>25)&(r>60)&(r<200)&(g<150)
bb(pur, 455,395,525,445, 'step circle ring', (471,403,507,439))
navy = (b-r>60)&(b>100)&(r<90)
bb(navy, 475,405,512,437, 'step glyph', (481,412,508,431))
# fan strip at x306 (gt: ys 377,393,409,~428,458,471)
col = int(306/s)
ys = [round(y*s,1) for y in range(int(352/s), int(506/s)) if lum[y, col] < 240]
print('fan strip x306:', ys, '(gt ~[377,393,409,428,458,471])')
# junction blob (gt x395..407 y415..427)
bb(redl|blackish, 388,410,412,432, 'junction', (395,415,407,427))
print()
print('SELF-CHECK FAILS:' if fails else 'SELF-CHECK: ALL WITHIN TOL')
for f in fails: print('  -', f)
sys.exit(1 if fails else 0)
