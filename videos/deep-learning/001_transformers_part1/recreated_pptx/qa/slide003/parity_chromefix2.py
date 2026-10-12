#!/usr/bin/env python3
"""Chromefix parity v2 — render_4.png (judge-mandated title fix) vs render_pre_chromefix.png.

v1 (parity_chromefix.py, render_3) proved the pure chrome swap: 0 structural-changed px
outside chrome zones; title/agenda ink identical. Judge attempt 2 then FAILED the render
on D1 MAJOR (title straddled the panel top border — the certified title box y:0.28 was
superseded ml-intro chrome; under the ratified playlist chrome the title is CONTENT and
must sit at the original's measured ink y=[69,99]px, center x=421.5px).

v2 therefore EXPECTS exactly one content delta vs the pre-fix render — the title band —
and verifies it against the ORIGINAL frame targets (closed loop). Everything else keeps
the v1 law: agenda ink within 2px + identical, all other structural change confined to
chrome zones, chrome values = ratified playlist values.
"""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide003"
old = np.asarray(Image.open(f"{QA}/render_pre_chromefix.png").convert("RGB")).astype(int)
new = np.asarray(Image.open(f"{QA}/render_4.png").convert("RGB")).astype(int)
H, W = old.shape[:2]
sc = H / 540.0  # 2.0833 render px per frame px
K = 150 / 72.0
print(f"old {old.shape} new {new.shape}")

fails = []

# ---- chrome zones (v1) + EXPECTED content delta: title band (judge D1 fix) ----
panel_top, panel_l, panel_r = int(45 * sc), int(42 * sc), int(918 * sc)
zoneA = np.zeros((H, W), bool); zoneA[: panel_top + 5, :] = True
zoneB = np.zeros((H, W), bool); zoneB[:, : panel_l + 5] = True; zoneB[:, panel_r - 2 :] = True
zoneC = np.zeros((H, W), bool)
zoneC[45 - 4 : 120 + 4, 1872 - 4 : 1947 + 4] = True   # old badge (ml-intro pos)
zoneC[110 - 4 : 185 + 4, 1823 - 4 : 1898 + 4] = True  # new badge (playlist pos)
zoneD = np.zeros((H, W), bool); zoneD[1095:, :] = True
zoneT = np.zeros((H, W), bool); zoneT[30:230, 380:1460] = True  # judge-mandated title move
chrome = zoneA | zoneB | zoneC | zoneD | zoneT

diff = np.abs(old - new).max(axis=2)
changed = diff > 12
outside = changed & ~chrome
print(f"structural-changed px: {int(changed.sum())}; outside chrome∪title zones: {int(outside.sum())}")
if outside.sum():
    ys, xs = np.where(outside)
    fails.append(f"{outside.sum()} changed px outside allowed zones, first at (y={ys[0]},x={xs[0]})")

# ---- title ink vs ORIGINAL frame targets (closed loop, the judge's fix) ----
r, g, b = new[:, :, 0], new[:, :, 1], new[:, :, 2]
red = (r > 120) & (r - g > 50) & (r - b > 50)
m = red[96:300, 300:1700]  # below the border stroke (rows 93-94)
ys, xs = np.where(m)
t_top, t_bot = ys.min() + 96, ys.max() + 96
t_l, t_r = xs.min() + 300, xs.max() + 300
print(f"title ink render rows=[{t_top},{t_bot}] cols=[{t_l},{t_r}] -> frame rows [{t_top/K:.1f},{t_bot/K:.1f}] center x {(t_l+t_r)/2/K:.1f}")
if abs(t_top / K - 69) > 4 or abs(t_bot / K - 99) > 4:
    fails.append(f"title vertical off vs original [69,99]: render [{t_top},{t_bot}]")
if abs((t_l + t_r) / 2 / K - 421.5) > 4:
    fails.append(f"title center x off vs original 421.5: {(t_l+t_r)/2/K:.1f}")
# no ink above the panel top border (the D1 defect must be gone)
if red[0:91, 300:1700].sum():
    fails.append("title ink still above the panel top border (D1 not fixed)")
print(f"title above-border ink: {int(red[0:91, 300:1700].sum())} px (must be 0); border clearance {t_top-94} render px")

# ---- agenda ink parity vs pre-fix (unchanged content) ----
BGS = np.array([[232, 232, 232], [233, 233, 231], [255, 255, 255]])
def ink_mask(a):
    d = np.min(np.abs(a[:, :, None, :] - BGS[None, None, :, :]).sum(axis=3), axis=2)
    return d > 90
oi, ni = ink_mask(old), ink_mask(new)
def bbox(m, r0, r1, c0, c1):
    sub = m[r0:r1, c0:c1]
    ys, xs = np.where(sub)
    return (ys.min() + r0, ys.max() + r0, xs.min() + c0, xs.max() + c0, int(sub.sum()))
bo, bn = bbox(oi, 330, 690, 170, 920), bbox(ni, 330, 690, 170, 920)
dmax = max(abs(a - b_) for a, b_ in zip(bo[:4], bn[:4]))
print(f"agenda: old bbox {bo[:4]} ink {bo[4]} | new bbox {bn[:4]} ink {bn[4]} | max edge delta {dmax}px")
if dmax > 2 or bo[4] != bn[4]:
    fails.append(f"agenda ink moved/changed: edge delta {dmax}, ink {bo[4]} vs {bn[4]}")
both = oi[330:690, 170:920] & ni[330:690, 170:920]
dc = np.abs(old[330:690, 170:920][both] - new[330:690, 170:920][both]).max()
print(f"agenda shared-ink max channel delta: {dc}")
if dc > 8:
    fails.append(f"agenda ink color drifted ({dc})")

# ---- chrome values at ratified sample points ----
def px(y, x): return tuple(int(v) for v in new[y, x])
for name, got, want, tol in [
    ("canvas white", px(50, 1000), (255, 255, 255), 6),
    ("panel gray", px(500, 500), (233, 233, 231), 6),
    ("badge fill (off-glyph)", px(126, 1860), (253, 253, 150), 25),
    ("badge numeral (center)", px(148, 1860), (51, 51, 51), 30),
    ("badge ring purple", px(148, 1860 - 36), (106, 90, 205), 40),
]:
    d = max(abs(a - b_) for a, b_ in zip(got, want))
    print(f"{name}: {got} vs {want} -> {'OK' if d <= tol else 'FAIL'}")
    if d > tol: fails.append(f"{name} {got} vs {want}")
rl, gl, bl = px(500, panel_l - 1)
if not (rl > 120 and gl < 110 and bl < 110):
    fails.append(f"left border not red: {(rl,gl,bl)}")
else:
    print(f"left border red: {(rl,gl,bl)} -> OK")

print()
if fails:
    print("PARITY v2: FAIL")
    for f in fails: print("  -", f)
    raise SystemExit(1)
print("PARITY v2: PASS — title at original-measured position (judge D1 fixed); agenda "
      "unchanged within 2px; all other change confined to chrome zones; chrome values ratified")
