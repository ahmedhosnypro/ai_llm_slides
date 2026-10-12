from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)

def bands(mask, axis, min_count, gap=3):
    rows = np.where(mask.sum(axis=axis) > min_count)[0]
    out=[]
    if len(rows):
        s=rows[0]; p=rows[0]
        for r in rows[1:]:
            if r>p+gap: out.append((int(s),int(p))); s=r
            p=r
        out.append((int(s),int(p)))
    return out

def ink_runs(mask2d, axis=0, min_count=0, gap=3):
    proj = mask2d.sum(axis=axis)
    idx = np.where(proj > min_count)[0]
    out=[]
    if len(idx):
        s=idx[0]; p=idx[0]
        for i in idx[1:]:
            if i>p+gap: out.append((int(s),int(p))); s=i
            p=i
        out.append((int(s),int(p)))
    return out

# black-ish ink mask (text): dark pixels, not the footer, not fraction bar ambiguity
blk = (a.sum(axis=2) < 330)

# Tan box 1: rows 126..299, x 79..648
sub = blk[126:300, 79:649]
print('TAN1 black row bands (abs):', [(126+s,126+e) for s,e in bands(sub,1,8,gap=4)])
# per band, x extent + column runs (to split equation / arrow / note)
for (s,e) in bands(sub,1,8,gap=4):
    ss, ee = 126+s, 126+e
    sub2 = blk[ss:ee+1, 79:649]
    cols = ink_runs(sub2, axis=0, min_count=0, gap=12)
    print(f'  rows {ss}..{ee} col-runs(abs):', [(79+c0,79+c1) for c0,c1 in cols])

# Yellow box: rows 306..369, x 82..762
sub = blk[306:370, 82:763]
print('YELLOW row bands:', [(306+s,306+e) for s,e in bands(sub,1,8,gap=4)])
for (s,e) in bands(sub,1,8,gap=4):
    ss, ee = 306+s, 306+e
    sub2 = blk[ss:ee+1, 82:763]
    cols = ink_runs(sub2, axis=0, min_count=0, gap=12)
    print(f'  rows {ss}..{ee} col-runs(abs):', [(82+c0,82+c1) for c0,c1 in cols])

# Final tan box: rows 375..501, x 79..842
sub = blk[375:502, 79:843]
print('TAN2 row bands:', [(375+s,375+e) for s,e in bands(sub,1,8,gap=4)])
for (s,e) in bands(sub,1,8,gap=4):
    ss, ee = 375+s, 375+e
    sub2 = blk[ss:ee+1, 79:843]
    cols = ink_runs(sub2, axis=0, min_count=0, gap=12)
    print(f'  rows {ss}..{ee} col-runs(abs):', [(79+c0,79+c1) for c0,c1 in cols])
