#!/usr/bin/env python3
"""Chromefix content-parity check — slide 003, render_3.png vs render_pre_chromefix.png.

Laws (dispatch 2026-10-12): only the CHROME layer may differ between the pre-fix
certified render and the chromefix render; all non-chrome ink (title glyphs, agenda
glyphs) must sit within ~2px of the pre-fix render with identical colors; chrome
regions must match the ratified playlist values (shared_patterns/house_chrome.js).

Chrome zones (render px @150dpi, 2001x1125; frame px *2.0833):
  A canvas above panel        rows 0..(45*sc+4)                 (E8E8E8 -> FFFFFF + strokes)
  B canvas left/right         cols <(42*sc+4) or >(918*sc+4)    (canvas swap + old/new side strokes)
  C badge zone                union of old badge bbox and new badge bbox, padded 4px
  D bottom band               rows >= 1095                      (old 0.15in frame bottom stroke
                                                                + old content line + new chrome
                                                                panel bottom stroke)
Panel background E8E8E8 -> E9E9E7 differs by <=2/channel -> below the 12 structural
threshold, correctly NOT counted as a structural change.
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide003"
old = np.asarray(Image.open(f"{QA}/render_pre_chromefix.png").convert("RGB")).astype(int)
new = np.asarray(Image.open(f"{QA}/render_3.png").convert("RGB")).astype(int)
H, W = old.shape[:2]
sc = H / 540.0
print(f"old {old.shape} new {new.shape} scale {sc:.4f}")
assert old.shape == new.shape, "size mismatch"

fails = []

# ---- chrome zones ----
panel_top = int(45 * sc)          # 93
panel_l = int(42 * sc)            # 87
panel_r = int(918 * sc)           # 1912
zoneA = np.zeros((H, W), bool); zoneA[: panel_top + 5, :] = True
zoneB = np.zeros((H, W), bool); zoneB[:, : panel_l + 5] = True; zoneB[:, panel_r - 2 :] = True
zoneC = np.zeros((H, W), bool)    # badge: old (1872..1947, 45..120) + new (1823..1898, 110..185)
zoneC[45 - 4 : 120 + 4, 1872 - 4 : 1947 + 4] = True
zoneC[110 - 4 : 185 + 4, 1823 - 4 : 1898 + 4] = True
zoneD = np.zeros((H, W), bool); zoneD[1095:, :] = True
chrome = zoneA | zoneB | zoneC | zoneD

# ---- 1. structural change confined to chrome zones ----
diff = np.abs(old - new).max(axis=2)
changed = diff > 12
n_ch = int(changed.sum())
outside = changed & ~chrome
print(f"structural-changed px: {n_ch}; outside chrome zones: {int(outside.sum())}")
if outside.sum():
    ys, xs = np.where(outside)
    fails.append(f"{outside.sum()} changed px outside chrome zones, e.g. first at (y={ys[0]},x={xs[0]})")

# ---- 2. content ink bboxes within 2px (title + agenda ROIs) ----
BGS = np.array([[232, 232, 232], [233, 233, 231], [255, 255, 255]])
def ink_mask(a):
    d = np.min(np.abs(a[:, :, None, :] - BGS[None, None, :, :]).sum(axis=3), axis=2)
    return d > 90

oi, ni = ink_mask(old), ink_mask(new)
def bbox(m, r0, r1, c0, c1):
    sub = m[r0:r1, c0:c1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (ys.min() + r0, ys.max() + r0, xs.min() + c0, xs.max() + c0, int(sub.sum()))

ROIS = {"title": (120, 230, 380, 1450), "agenda": (330, 690, 170, 920)}
for name, (r0, r1, c0, c1) in ROIS.items():
    bo, bn = bbox(oi, r0, r1, c0, c1), bbox(ni, r0, r1, c0, c1)
    d = [abs(a - b) for a, b in zip(bo[:4], bn[:4])]
    ok = max(d) <= 2
    print(f"{name}: old bbox {bo[:4]} ink {bo[4]} | new bbox {bn[:4]} ink {bn[4]} | max edge delta {max(d)}px -> {'OK' if ok else 'FAIL'}")
    if not ok:
        fails.append(f"{name} ink bbox moved >2px: {d}")
    # ink color identity on overlapping ink
    both = oi[r0:r1, c0:c1] & ni[r0:r1, c0:c1]
    if both.sum():
        dc = np.abs(old[r0:r1, c0:c1][both] - new[r0:r1, c0:c1][both]).max()
        print(f"  shared-ink max channel delta: {dc}")
        if dc > 8:
            fails.append(f"{name} ink color drifted (max {dc})")

# ---- 3. chrome values at ratified sample points ----
def px(a, y, x): return tuple(a[y, x])
checks = [
    ("canvas white", px(new, 50, 1000), (255, 255, 255), 6),
    ("panel gray", px(new, 500, 500), (233, 233, 231), 6),
    ("left border red", px(new, 500, panel_l - 1), None, None),
    ("badge fill (off-glyph, disc upper area)", px(new, 148 - 22, 1860), (253, 253, 150), 25),
    ("badge numeral ink at center (333333)", px(new, 148, 1860), (51, 51, 51), 30),
    ("badge ring purple", px(new, 148, 1860 - 36), (106, 90, 205), 40),
]
for name, got, want, tol in checks:
    if want is None:
        r, g, b = got
        ok = r > 120 and g < 110 and b < 110
        print(f"{name}: {got} -> {'OK' if ok else 'FAIL'} (red)")
        if not ok: fails.append(f"{name} not red: {got}")
    else:
        d = max(abs(a - b) for a, b in zip(got, want))
        print(f"{name}: {got} vs {want} (tol {tol}) -> {'OK' if d <= tol else 'FAIL'}")
        if d > tol: fails.append(f"{name} {got} vs {want}")

# ---- 4. no leftover old-chrome ink: old 0.15in frame stroke zone must be clean in new ----
fr = slice(int(0.15 * 150) - 4, int(0.15 * 150) + 6)  # rows/cols ~18..28
r, g, b = new[:, :, 0], new[:, :, 1], new[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)
leftover = int(red[fr, 100:1900].sum()) + int(red[300:800, fr].sum())
print(f"old-frame stroke red px remaining in new render (top band + left band): {leftover}")
if leftover > 4:
    fails.append(f"old 0.15in frame stroke still present ({leftover} red px)")

print()
if fails:
    print("PARITY: FAIL")
    for f in fails: print("  -", f)
    raise SystemExit(1)
print("PARITY: PASS — only chrome zones changed; content ink within 2px; chrome values ratified")
