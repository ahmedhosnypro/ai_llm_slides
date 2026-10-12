import json, subprocess, sys
sys.path.insert(0, "/home/ahmed/Projects/ai_llm_slides/scripts")
import render_eq
from PIL import Image
import numpy as np

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/matrix_test"

# Target (frame px = pt): matrix ink x 634..833 (w 200), y 397..494 (h 98);
# theta+sub row ink h ~23, row pitch 33; col ink w ~29, col pitch 71.

def ink_metrics(png):
    im = Image.open(png).convert("RGBA")
    a = np.asarray(im).astype(int)
    ink = a[:, :, 3] > 40
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]
    return im.size, (cols[0], rows[0], cols[-1], rows[-1]), ink

# 1) single theta_1 at several sizes -> row ink height target ~23pt (23px@frame = 23/72in -> at 600dpi: 23/72*600 = 191.7px)
for fs in [26, 28, 30, 32, 34]:
    p = f"{OUT}_t1_{fs}.png"
    info = render_eq.render(r"\theta_1", p, fs, "#000000")
    (w, h), (x0, y0, x1, y1), ink = ink_metrics(p)
    # ink h in pt = (y1-y0+1)/600*72
    ih = (y1 - y0 + 1) / 600 * 72
    iw = (x1 - x0 + 1) / 600 * 72
    print(f"theta_1 fs={fs}: ink w={iw:.1f}pt h={ih:.1f}pt baseline_frac={info['baseline_frac']}")

# 2) try genfrac 3x3 matrix at a candidate size
mat = (r"\left[\ \genfrac{}{}{0}{}{\theta_1\ \ \theta_2\ \ \theta_3}"
       r"{\genfrac{}{}{0}{}{\theta_4\ \ \theta_5\ \ \theta_6}"
       r"{\theta_7\ \ \theta_8\ \ \theta_9}}\ \right]")
for fs in [24, 28, 32]:
    p = f"{OUT}_mat_{fs}.png"
    try:
        info = render_eq.render(mat, p, fs, "#000000")
        (w, h), (x0, y0, x1, y1), ink = ink_metrics(p)
        ih = (y1 - y0 + 1) / 600 * 72
        iw = (x1 - x0 + 1) / 600 * 72
        # row bands
        rowc = ink.sum(axis=1)
        onr = rowc > 2
        bands = []; s = None
        for y, v in enumerate(onr):
            if v and s is None: s = y
            if not v and s is not None:
                bands.append((s, y - 1)); s = None
        if s is not None: bands.append((s, len(onr) - 1))
        # col runs
        colc = ink.sum(axis=0)
        onc = colc > 0
        runs = []; s = None
        for x, v in enumerate(onc):
            if v and s is None: s = x
            if not v and s is not None:
                runs.append((s, x - 1)); s = None
        if s is not None: runs.append((s, len(onc) - 1))
        print(f"matrix fs={fs}: ink w={iw:.1f}pt h={ih:.1f}pt (target 200x98)")
        print("  row bands(px):", bands[:8])
        print("  col runs(px):", runs[:10])
    except Exception as e:
        print(f"matrix fs={fs}: FAILED {e}")
