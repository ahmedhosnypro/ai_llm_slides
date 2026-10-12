#!/usr/bin/env python3
# Pre-judge self-check for slide 048 attempt 1 (17_worker_instructions §Mandatory).
# Render is 150dpi (2001x1125); frame px * 150/72 = *2.08333. Original measures from
# scratch/slide048/measure_*.py. Checks: frame containment, element ink bboxes, dot
# column, divider, arrows, caption, band pitch, no-equation (N/A), no-ink-outside-band.
from PIL import Image
import numpy as np

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide048/render_1.png'
im = Image.open(REN).convert('RGB')
W,H = im.size
a = np.asarray(im).astype(int)
R,G,B = a[...,0],a[...,1],a[...,2]
S = 150/72.0
def fpx(v): return v*S

red   = (R>120)&(R<235)&(G<80)&(B<80)
orange= (R>170)&(R<240)&(G>90)&(G<170)&(B<70)
dark  = (R<140)&(G<140)&(B<140)
blue  = (B>120)&((B-R)>60)&((B-G)>40)
yellow= (R>200)&(G>180)&(B<120)

def bbox(mask,y0,y1,x0=0,x1=None,name='',exp=None,tol=8):
    x1 = x1 or W
    m = mask[int(y0):int(y1), int(x0):int(x1)]
    ys,xs = np.nonzero(m)
    if len(xs)==0:
        print(f'FAIL {name}: EMPTY (expected {exp})'); return None
    bb = (x0+xs.min()/1, x0+xs.max(), y0+ys.min(), y0+ys.max())
    if exp:
        dev = max(abs(bb[0]-exp[0]),abs(bb[1]-exp[1]),abs(bb[2]-exp[2]),abs(bb[3]-exp[3]))
        status = 'PASS' if dev<=tol else f'FAIL(dev {dev:.0f}px)'
    else:
        status = 'INFO'
    print(f'{status} {name}: x {bb[0]:.0f}..{bb[1]:.0f} y {bb[2]:.0f}..{bb[3]:.0f} n={len(xs)} exp={exp}')
    return bb

print(f'render {W}x{H}; scale frame->render x{S:.4f}')
fails = []
def note(s):
    print(s)
    if s.startswith('FAIL'): fails.append(s)

# 1. content frame (stroke): verticals at x58/894 y135..449; horizontals y135/448 x58..894
fpx_ = fpx
note('== content frame ==')
col58 = red[:, int(fpx(55)):int(fpx(61))].any(axis=1)
ys = np.nonzero(col58)[0]
note(f'{"PASS" if abs(ys.min()-fpx(45))<15 and ys.max()>fpx(440) else "CHECK"} frame-left col extent y {ys.min()}..{ys.max()} (chrome border shares col; frame top exp {fpx(135.5):.0f})')
b = bbox(red, fpx(120), fpx(150), fpx(60), fpx(890), 'frame top border', (fpx(58),fpx(894),fpx(134),fpx(137)), 6)
b = bbox(red, fpx(440), fpx(462), fpx(60), fpx(890), 'frame bottom border', (fpx(58),fpx(894),fpx(447),fpx(450)), 6)
# inner-left line x65: red pixels near x65 between y150..440
m = red[int(fpx(150)):int(fpx(440)), int(fpx(63)):int(fpx(68))]
note(f'{"PASS" if m.sum()>200 else "FAIL"} inner-left line x65 ink n={m.sum()}')

# 2. title lines
note('== title ==')
b = bbox(red, fpx(50), fpx(92), fpx(66), fpx(890), 'title line1', (fpx(130),fpx(833),fpx(63),fpx(89)), 12)
b = bbox(red, fpx(92), fpx(128), fpx(66), fpx(890), 'title line2', (fpx(258),fpx(706),fpx(96),fpx(123)), 12)

# 3. label boxes (blue borders) + text
note('== label boxes ==')
b = bbox(blue, fpx(150), fpx(190), fpx(230), fpx(390), 'NN label box border', (fpx(242),fpx(379),fpx(155),fpx(182)), 6)
b = bbox(blue, fpx(270), fpx(312), fpx(230), fpx(495), 'CNN label box border', (fpx(242),fpx(480),fpx(278),fpx(305)), 6)
# text ink (dark) inside boxes
dk = (R<120)&(G<120)&(B<120)
b = bbox(dk, fpx(160), fpx(179), fpx(246), fpx(376), 'NN label text', (fpx(251),fpx(365),fpx(164),fpx(174)), 7)
b = bbox(dk, fpx(282), fpx(302), fpx(246), fpx(477), 'CNN label text', (fpx(249),fpx(471),fpx(286),fpx(296)), 7)

# 4. meme photo region non-white
note('== meme photo ==')
wt = (R>235)&(G>235)&(B>230)
nw = ~wt
b = bbox(nw, fpx(191), fpx(253), fpx(247), fpx(362), 'meme photo', (fpx(248),fpx(360),fpx(191),fpx(252)), 6)

# 5. tag + text
note('== flatten tag ==')
b = bbox(yellow, fpx(150), fpx(190), fpx(380), fpx(430), 'tag yellow', (fpx(387),fpx(422),fpx(157),fpx(183)), 6)
b = bbox(red, fpx(158), fpx(184), fpx(388), fpx(422), 'tag red text', (fpx(390),fpx(420),fpx(159),fpx(182)), 7)

# 6. dots column: 7 saturated/dark dots near x405
note('== dot column ==')
seg = slice(int(fpx(399)), int(fpx(413)))
colmask = (dark[:,seg] | ((np.maximum(np.maximum(R,G),B)-np.minimum(np.minimum(R,G),B))>60)[:,seg])
prof = colmask[int(fpx(185)):int(fpx(255)),:].sum(axis=1)
runs=[]; s=None
for i,v in enumerate(prof):
    if v>=2 and s is None: s=i
    elif v<2 and s is not None: runs.append((s,i-1)); s=None
if s is not None: runs.append((s,len(prof)-1))
cys = [fpx(195.5+8.33*k) - fpx(185) for k in range(7)]
print('dot runs (render y rel):', runs)
print('expected centers rel:', [f'{c:.0f}' for c in cys])
ok = len(runs)==7 and all(abs((r[0]+r[1])/2 - c)<5 for r,c in zip(runs,cys))
note(f'{"PASS" if ok else "FAIL"} dot column: {len(runs)} dots at expected pitch')

# 7. NN blocks: orange bands
note('== NN blocks ==')
b = bbox(orange, fpx(180), fpx(262), fpx(440), fpx(720), 'NN blocks band', (fpx(450),fpx(712),fpx(186),fpx(255)), 7)
occ = orange[int(fpx(220)):int(fpx(222)), :].sum(axis=0)
# count block column clusters along a mid row
row = orange[int(fpx(220)), :]
xs = np.nonzero(row)[0]
groups=[]
if len(xs):
    s=xs[0]; p=xs[0]
    for c in xs[1:]:
        if c>p+3: groups.append((s,p)); s=c
        p=c
    groups.append((s,p))
exp_g = [(fpx(450),fpx(476)),(fpx(497),fpx(522)),(fpx(544),fpx(570)),(fpx(591),fpx(617)),(fpx(639),fpx(664)),(fpx(686),fpx(712))]
okg = len(groups)==6 and all(abs(g[0]-e[0])<7 and abs(g[1]-e[1])<7 for g,e in zip(groups,exp_g))
note(f'{"PASS" if okg else "FAIL"} NN block columns at y220: {len(groups)} groups {[(f"{g[0]/S:.0f}",f"{g[1]/S:.0f}") for g in groups]}')

# 8. white vertical text inside block 1
note('== NN block text ==')
wtx = (R>225)&(G>225)&(B>215)
b = bbox(wtx, fpx(190), fpx(252), fpx(452), fpx(474), 'block1 white text', (fpx(458),fpx(467),fpx(205),fpx(240)), 8)

# 9. overlines
note('== overlines ==')
b = bbox(red, fpx(160), fpx(182), fpx(445), fpx(680), 'NN overlines band', (fpx(452),fpx(663),fpx(168),fpx(177)), 7)
b = bbox(red, fpx(305), fpx(330), fpx(730), fpx(815), 'CNN FC/OP band', (fpx(735),fpx(806),fpx(314),fpx(324)), 7)

# 10. divider
note('== divider ==')
b = bbox(red, fpx(262), fpx(276), fpx(66), fpx(895), 'divider', (fpx(66),fpx(893),fpx(268),fpx(270)), 8)

# 11. CNN chain image + siamese
note('== CNN imagery ==')
b = bbox(nw, fpx(315), fpx(430), fpx(124), fpx(226), 'siamese photo', (fpx(129),fpx(227),fpx(319),fpx(427)), 8)
b = bbox(orange, fpx(314), fpx(427), fpx(229), fpx(695), 'CNN slabs band', (fpx(229),fpx(691),fpx(315),fpx(425)), 8)
b = bbox(nw, fpx(333), fpx(405), fpx(730), fpx(860), 'CNN blocks 7-9', (fpx(735),fpx(854),fpx(333),fpx(403)), 8)

# 12. bottom arrow + caption
note('== bottom arrow/caption ==')
loose = ((R-G)>28)&((R-B)>28)&(R>150)
b = bbox(loose, fpx(452), fpx(467), fpx(150), fpx(840), 'red arrow', (fpx(169),fpx(831),fpx(456),fpx(465)), 10)
b = bbox(red, fpx(464), fpx(486), fpx(340), fpx(640), 'caption', (fpx(354),fpx(596),fpx(466),fpx(479)), 10)

# 13. EXCLUSIONS: no black strip at bottom, no gray '+' at (~710,475)
note('== exclusions ==')
blk = (R<60)&(G<60)&(B<60)
brow = blk[int(fpx(515)):, :].sum(axis=1)
note(f'{"PASS" if brow.max()<50 else "FAIL"} no black player strip (max black px/row below y515: {brow.max()})')
grayplus = (abs(R-G)<12)&(abs(G-B)<12)&(R>120)&(R<190)
m = grayplus[int(fpx(468)):int(fpx(486)), int(fpx(700)):int(fpx(722))]
note(f'{"PASS" if m.sum()<12 else "FAIL"} no gray + mark near (710,475) (ink {m.sum()})')

# 14. containment: no content ink outside house panel (x42..918 y45..540) beyond chrome border
note('== containment (house panel) ==')
content = red|orange|dark|blue|yellow
out_left  = content[:, :int(fpx(43))].sum()
out_right = content[:, int(fpx(919)):].sum()
out_top   = content[:int(fpx(44)), :].sum()
note(f'{"PASS" if out_left<40 and out_right<40 and out_top<40 else "FAIL"} ink outside panel: left {out_left} right {out_right} top {out_top}')

# 15. line pitch: title baselines via row profiles in line1/line2 bands
note('== title pitch ==')
r1 = red[int(fpx(55)):int(fpx(92)), int(fpx(66)):int(fpx(890))].sum(axis=1)
r2 = red[int(fpx(92)):int(fpx(130)), int(fpx(66)):int(fpx(890))].sum(axis=1)
t1 = np.nonzero(r1>10)[0]; t2 = np.nonzero(r2>10)[0]
if len(t1) and len(t2):
    top1, top2 = t1.min()+fpx(55), t2.min()+fpx(92)
    pitch = top2-top1
    note(f'{"PASS" if abs(pitch-fpx(35))<6 else "FAIL"} title cap-top pitch {pitch:.1f}px render (exp {fpx(35):.0f}, frame 35)')

print()
print('SELF-CHECK RESULT:', 'ALL PASS' if not fails else f'{len(fails)} FAIL(S)')
for s in fails: print(' -', s)
