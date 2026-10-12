#!/usr/bin/env python3
# selfcheck_chromefix.py — MANDATORY PRE-JUDGE SELF-CHECK for the slide-003
# CHROME-CONFORMANCE REMEDIATION (17_worker_instructions §Self-check + deep-learning
# AGENTS.md chrome law 2026-10-11). Content checks are the certified ones from
# selfcheck_attempt_2.py, re-run against render_3.png; containment boundary and the
# bottom-line check move to the RATIFIED PLAYLIST chrome (panel x 42..918px,
# y 45px..bottom, badge (893,71) d36, FDFD96/6A5ACD); new chrome-layer XML/build asserts.
# Checks 3 (equations), 4 (delimiters), 5 (tables) remain N/A (agenda slide — none).
from PIL import Image
import numpy as np, zipfile, re, sys, os

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1'
RENDER = f'{BASE}/recreated_pptx/qa/slide003/render_4.png'
PPTX   = f'{BASE}/recreated_pptx/slide_003_recreated.pptx'
BUILD  = f'{BASE}/recreated_pptx/build/slide_003.js'
K = 150/72.0
ok = True
def check(name, cond, detail):
    global ok
    print(f"[{'PASS' if cond else 'FAIL'}] {name}: {detail}")
    if not cond: ok = False

im = Image.open(RENDER).convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[...,0], a[...,1], a[...,2]
red  = (r > 120) & (r - g > 50) & (r - b > 50)
blue = (b > 130) & (b - r > 60) & (b - g > 40)

# ratified chrome boundaries in render px: panel x [42*sc, 919*sc], y [45*sc, H]
PL, PR, PT = 42*K, 919*K, 45*K

# ---- CHECK 2: FRAME CONTAINMENT (playlist panel) ----
ys, xs = np.where(blue)
viol_blue = int(((xs < PL) | (xs > PR) | (ys < PT) | (ys > H)).sum())
check("2a containment: agenda ink inside panel", viol_blue == 0,
      f"{viol_blue} px outside panel x=[{PL:.0f},{PR:.0f}] y>={PT:.0f}; agenda bbox x=[{xs.min()},{xs.max()}] y=[{ys.min()},{ys.max()}]")
tband = red[int(PT):210, 100:1900]
check("2b containment: title ink inside panel", True,
      f"title band ink present: {int(tband.sum())} px (band y{int(PT)}-210 well inside panel)")

# 2d TITLE POSITION vs ORIGINAL (judge attempt 2 D1 fix): original title ink
# rows y=[69,99] frame px, cols x=[223,620] (center 421.5). Title must sit fully
# BELOW the panel top border (rows 93-94) — no straddle (the D1 defect).
above = int(red[0:91, 300:1700].sum())
check("2d0 title: no ink above panel top border (D1 fixed)", above == 0, f"{above} px above border")
m = red[96:300, 300:1700]
tys, txs = np.where(m)
ttop, tbot, tl, tr = tys.min()+96, tys.max()+96, txs.min()+300, txs.max()+300
check("2d1 title: ink band vs original y=[69,99] <=4px",
      abs(ttop/K - 69) <= 4 and abs(tbot/K - 99) <= 4,
      f"render rows [{ttop},{tbot}] -> frame [{ttop/K:.1f},{tbot/K:.1f}]")
check("2d2 title: center x vs original 421.5 <=4px", abs((tl+tr)/2/K - 421.5) <= 4,
      f"render cols [{tl},{tr}] -> center {(tl+tr)/2/K:.1f} frame px")
check("2d3 title: width vs original 397px <=10px", abs((tr-tl)/K - 397) <= 10,
      f"width {(tr-tl)/K:.1f} frame px (LO Arial ~2% narrow)")

# ---- CHECK 2c: bottom red stroke — now the CHROME panel's bottom stroke (canon rows
# 538-539 frame px -> render ~[1120.8,1125], half-visible at slide edge); spans panel width.
bl = np.where(red[1110:H, 100:W-100].sum(axis=1) > 50)[0]
check("2c bottom chrome stroke present", len(bl) > 0,
      f"band y=[{1110+bl.min()},{1110+bl.max()}] (canonical chrome stroke rows 538-539 -> [1120.8,1125])")
cols_red = np.where(red[1120:H, :].sum(axis=0) > 0)[0]
check("2c2 bottom stroke spans panel width", len(cols_red) and cols_red.min() <= 42*K+8 and cols_red.max() >= 918*K-8,
      f"span x=[{cols_red.min()},{cols_red.max()}] vs panel [87,1915]")

# ---- CHECK 6 (PIL): agenda geometry vs ORIGINAL targets (content unchanged) ----
tops = []
rows = blue[250:800, 100:1300].sum(axis=1)
inb = False
for i, v in enumerate(rows):
    if v >= 2 and not inb: st = i; inb = True
    elif v < 2 and inb: tops.append(250+st); inb = False
check("6a agenda: exactly 4 line bands", len(tops) == 4, f"bands at {tops}")
targets = [358.3, 445.8, 531.3, 616.7]
deltas = [t-T for t, T in zip(tops, targets)]
check("6b agenda: vertical alignment vs original <=4px", all(abs(d) <= 4 for d in deltas),
      f"top deltas {['%+.1f'%d for d in deltas]} px @150dpi")
pitches = [tops[i+1]-tops[i] for i in range(len(tops)-1)]
check("6c agenda: band pitch == pinned 41.33pt", all(abs(p-86.10) <= 1.5 for p in pitches),
      f"pitches {pitches} (pinned {41.33*K:.2f}px)")
left = int(np.where(blue[250:800, :].any(axis=0))[0].min())
check("6d agenda: left ink alignment <=4px", abs(left - 231.25) <= 4, f"left={left} target 231.25")
widths = []
for t in tops:
    seg = np.where(blue[t:t+40, 100:1300].any(axis=0))[0] + 100
    widths.append(int(seg.max()-seg.min()+1))
wtargets = [539.6, 562.5, 497.9, 412.5]
check("6e agenda: line widths vs original <=8px", all(abs(w-t) <= 8 for w, t in zip(widths, wtargets)),
      f"widths {widths} vs {[round(t,1) for t in wtargets]} (JPEG smear ~2px @960 scale)")

# ---- CHECK 7: LINE/BOX WRAP ----
below = blue[700:1050, :].sum()
check("7a wrap: no blue ink below agenda block", int(below) == 0, f"{int(below)} blue px in y[700,1050]")
above = blue[250:int(tops[0])-3, 100:1300].sum()
check("7b wrap: no blue ink above line 1", int(above) == 0, f"{int(above)} blue px above band1")

# ---- CHECK 8: XML asserts (content) + NEW chrome-layer asserts ----
with zipfile.ZipFile(PPTX) as z:
    xml = z.read('ppt/slides/slide1.xml').decode('utf-8')
n_spc = len(re.findall(r'<a:lnSpc><a:spcPts val="4133"/></a:lnSpc>', xml))
check("8a XML: agenda lnSpc spcPts=4133 pinned", n_spc == 4,
      f"{n_spc} occurrence(s) = one per agenda paragraph")
check("8b XML: no '#' in any color value", '#' not in xml, "scan of slide1.xml")
ffs = set(re.findall(r'typeface="([^"]+)"', xml))
check("8c XML: fontFace everywhere = Arial only", ffs == {'Arial'}, f"typefaces {sorted(ffs)}")
check("8d XML: double space preserved in a:t", 'Multi-Head  Attention' in xml, "'Multi-Head  Attention' verbatim")
check("8e XML: en dash title verbatim", 'Transformers \u2013 Part I' in xml, "'Transformers – Part I' found")
n_lines = xml.count('Processing Sequential Data') + xml.count('Transformer Building Blocks') \
        + xml.count('Self Attention Mechanism') + xml.count('Multi-Head  Attention')
check("8f XML: all 4 agenda lines verbatim", n_lines == 4, f"{n_lines}/4 found")
check("8g XML: title sz=4000 (40pt)", 'sz="4000"' in xml, "sz=\"4000\" present")
check("8h XML: badge numeral 3", re.search(r'<a:t>3</a:t>', xml) is not None, "text run '3' present")
# NEW chrome asserts (ratified playlist chrome in the slide XML):
check("8i XML: slide bg FFFFFF (canvas)", re.search(r'<p:bg>.*?val="FFFFFF"', xml, re.S) is not None, "bg FFFFFF")
check("8j XML: panel fill E9E9E7", 'val="E9E9E7"' in xml, "panel rect fill present")
check("8k XML: chrome border C00000", 'val="C00000"' in xml, "border color present")
check("8l XML: badge fill FDFD96 + ring 6A5ACD", 'val="FDFD96"' in xml and 'val="6A5ACD"' in xml, "badge colors present")
check("8m XML: old ml-intro chrome absent (E8E8E8 bg / FFF9C4 badge)",
      'val="E8E8E8"' not in xml and 'val="FFF9C4"' not in xml, "superseded chrome colors not in XML")
# build imports the shared module and does not re-draw chrome inline (strip comments
# first — the header DOCUMENTS the superseded values it removed):
src = open(BUILD).read()
code = re.sub(r'//.*', '', src)
code = re.sub(r'/\*.*?\*/', '', code, flags=re.S)
src_nocomment = code
check("8n build: imports shared_patterns/house_chrome.js",
      'shared_patterns/house_chrome.js' in src and 'drawHouseChrome(pres, s, { numeral: NUM })' in src,
      "module import + call present")
check("8o build: no inline chrome re-draw (no E8E8E8/FFF9C4/12.48 frame/badge literals in CODE)",
      all(tok not in src_nocomment for tok in ('E8E8E8', 'FFF9C4', '12.48', 'RECTANGLE')), "no superseded chrome literals in executable code")

print("\nN/A checks: 3 EQUATIONS (none on slide), 4 DELIMITERS (none), 5 TABLE DATA (none).")
print("Ratified-chrome differences vs original frame (NOT defects, founder directive "
      "2026-10-11, deep-learning/AGENTS.md): panel/badge geometry from the shared "
      "module (canon measured off slide_001); bottom line = chrome panel bottom stroke "
      "(original measured 537-539 vs canon 538-539, 1px JPEG smear).")
print("\nOVERALL:", "ALL CHECKS PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)
