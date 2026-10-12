#!/usr/bin/env python3
"""forensics13_045.py v2 — attempt-4 issue forensics (crop-compare FAIL triage).
1. Dot region ASCII ink maps (org vs ren), x638..660 y334..356 — read blob structure.
2. ij subscript: correlate token PNG vs fresh ij/jj renders (XOR on aligned bboxes).
3. Arrow shaft thickness: red column profile in the shaft band.
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"
ren = np.asarray(Image.open(f"{QA}/render_4.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
s = ren.shape[0] / 540.0

def ink(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    lum = (r + g + b) / 3
    reddish = (r - g > 30) & (r - b > 20)
    return (lum < 205) & (~reddish)

def red(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (r - g > 30) & (r - b > 20) & (r > 100)

print("== 1. DOT region map (x638..660, y334..356; '#'=ink, '.'=bg; 1 char = 1x2pt) ==")
for nm, im, is_r in (("org", org, False), ("ren", ren, True)):
    k = s if is_r else 1
    win = ink(im)[int(334*k):int(356*k)+1, int(638*k):int(660*k)+1]
    print(f"-- {nm} (window left=x638 top=y334) --")
    for row in range(0, win.shape[0], 2):
        line = "".join("#" if win[row, col:col+int(k)].any() else "." for col in range(0, win.shape[1], int(k)))
        print(f"  y{334 + row/k:5.1f} {line}")

print("== 2. ij subscript identity ==")
import json, subprocess, sys, os
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
man = json.load(open(f"{ASSETS}/eq_045_manifest.json"))
tok = man["ij_a"]
ref = np.asarray(Image.open(tok["path"]).convert("RGBA")).astype(int)
mask_ref = ref[:, :, 3] > 128
CWD = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide045/ijcheck"
os.makedirs(CWD, exist_ok=True)
open(f"{CWD}/matplotlibrc", "w").write("mathtext.fontset: dejavuserif\nfont.family: serif\n")

def crop(m):
    ys, xs = np.where(m)
    return m[ys.min():ys.max()+1, xs.min():xs.max()+1]

a = crop(mask_ref)
for cand in ("ij", "jj"):
    subprocess.run([sys.executable, "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py",
                    cand, f"{CWD}/cand_{cand}.png", str(tok["fontsize_pt"]), "#000000"],
                   capture_output=True, text=True, cwd=CWD, check=True)
    ci = np.asarray(Image.open(f"{CWD}/cand_{cand}.png").convert("RGBA")).astype(int)
    b = crop(ci[:, :, 3] > 128)
    bi = np.asarray(Image.fromarray((b*255).astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.LANCZOS)) > 128
    xor = int(np.logical_xor(a, bi).sum())
    print(f" cand '{cand}': ink {b.shape[1]}x{b.shape[0]}px@600, xor-vs-token {xor} px of {int(a.sum())} token ink")

print("== 3. ARROW shaft thickness (band y346..356, x624..700 frame px) ==")
for nm, im, is_r in (("org", org, False), ("ren", ren, True)):
    k = s if is_r else 1
    win = red(im)[int(346*k):int(356*k)+1, int(624*k):int(700*k)+1]
    th = win.sum(axis=0)
    cols = th[th > 0]
    if len(cols):
        print(f" {nm}: red cols={len(cols)} thickness mean={cols.mean()/k:.1f}pt median={np.median(cols)/k:.1f}pt max={cols.max()/k:.1f}pt")
    else:
        print(f" {nm}: no red in band")
