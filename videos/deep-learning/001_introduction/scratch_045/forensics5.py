#!/usr/bin/env python3
"""Forensics pass 5: zoomed crops for visual verification + fine measurements:
equation bboxes, bullet circles, arrows, border modals, title split, callout text."""
from PIL import Image
import numpy as np

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
mn = a.min(axis=2); mx = a.max(axis=2)
ink = (mn < 205) | (mx - mn > 45)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R - G > 55) & (R - B > 55) & (R > 120)

def crop_zoom(name, x0, y0, x1, y1, z=4):
    c = im.crop((x0, y0, x1, y1))
    c = c.resize(((x1 - x0) * z, (y1 - y0) * z), Image.LANCZOS)
    c.save(f"/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch_045/{name}.png")
    print("saved", name, f"x{x0}..{x1} y{y0}..{y1} zoom={z}")

crop_zoom("z_eq1", 290, 290, 705, 375, 3)
crop_zoom("z_eq2_3", 290, 370, 705, 505, 3)
crop_zoom("z_legend", 65, 348, 270, 440, 4)
crop_zoom("z_title", 180, 45, 900, 115, 2)
crop_zoom("z_remember", 75, 220, 895, 285, 2)
crop_zoom("z_callouts_arrows", 690, 320, 910, 460, 3)
crop_zoom("z_starburst", 740, 35, 910, 150, 3)
crop_zoom("z_defbox", 65, 108, 900, 215, 1)

# --- equation bboxes: exclude bullet-text columns (bullets+text at x<455) ---
# eq (a): right part of band y312..366, x>=470
def bbox(y0, y1, x0, x1, label):
    sub = ink[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        print(f"  {label}: EMPTY"); return
    print(f"  {label}: x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} (w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1})")

print("== equation ink bboxes ==")
bbox(305, 372, 460, 700, "eq(a) right-of-text")
bbox(310, 340, 460, 560, "eq(a) upper (limits?)")
bbox(390, 420, 440, 700, "eq(b)")
bbox(420, 500, 455, 700, "eq(c)")
# bullet text lines: x296..455
bbox(295, 312, 296, 460, "bullet1 text")
bbox(374, 392, 296, 665, "bullet2 text")
bbox(422, 445, 296, 680, "bullet3 text")

# bullet circles: search x296..320 for small dark ellipses
print("== bullet circles ==")
for yr in [(295, 315), (372, 394), (420, 448)]:
    sub = ink[yr[0]:yr[1], 296:325]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"  y{yr}: x{296+xs.min()}..{296+xs.max()} y{yr[0]+ys.min()}..{yr[0]+ys.max()} n={len(ys)}")

# arrows: red strokes in x700..770, y300..480
print("== arrow red strokes (x700..775, y300..480) ==")
sub = red[300:480, 700:775]
ys, xs = np.where(sub)
if len(ys):
    print(f"  bbox x{700+xs.min()}..{700+xs.max()} y{300+ys.min()}..{300+ys.max()} n={len(ys)}")
    # per-row spans to trace shape
    for y in range(300, 480, 6):
        row = np.where(red[y, 700:775])[0]
        if len(row):
            print(f"    y={y}: x{700+row[0]}..{700+row[-1]} n={len(row)}")

# border color modals (exact border rows)
def modal(y0, y1, x0, x1, mask_min=None):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    reg = reg[(reg.min(axis=1) < 215) | (reg.max(axis=1) - reg.min(axis=1) > 45)]
    modal = {}
    for px in reg:
        key = (px[0] // 12 * 12, px[1] // 12 * 12, px[2] // 12 * 12)
        modal[key] = modal.get(key, 0) + 1
    return sorted(modal.items(), key=lambda kv: -kv[1])[:5]

print("== border modals ==")
print("  defbox top y114 x150..700:", modal(114, 116, 150, 700))
print("  eqpanel left x291 y320..480:", modal(320, 480, 291, 293))
print("  callout top y363 x760..880:", modal(363, 365, 760, 880))
print("  legend top y354 x100..240:", modal(354, 356, 100, 240))
print("  legend fill y400..425 x120..240 (bright modal):")
reg = a[400:425, 120:240].reshape(-1, 3)
reg = reg[reg.min(axis=1) > 200]
modal2 = {}
for px in reg:
    key = (px[0] // 8 * 8, px[1] // 8 * 8, px[2] // 8 * 8)
    modal2[key] = modal2.get(key, 0) + 1
print("   ", sorted(modal2.items(), key=lambda kv: -kv[1])[:5])

# title text-only band (exclude starburst x>745)
print("== title text band (x197..745) ==")
for y in range(48, 108):
    n = int(ink[y, 197:745].sum())
    if n:
        xs = np.where(ink[y, 197:745])[0]
        print(f"  y={y} n={n} x{197+xs.min()}..{197+xs.max()}")
