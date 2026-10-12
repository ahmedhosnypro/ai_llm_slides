# verify_compare.py — machine-only verification of the retro-banked
# components/slide_033.js.
# GATE: component_full render vs CERTIFIED reference (qa/slide033/render_3.png,
# the passing attempt-3 render) must have 0 differing pixels. Plus smoke checks
# (skip/only/numeral/chrome) mirroring scratch/slide015_component_verify/.
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
V = f"{BASE}/scratch/slide033_component_verify/renders"
S = 150 / 72.0  # pt -> render px

def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)

def pt(v):
    return int(round(v * S))

def diff_mask(a, b):
    if a.shape != b.shape:
        return None, None
    d = np.abs(a - b).sum(axis=2)
    return d > 0, d

def report(name, a_path, b_path, expect_zero=True, zone=None, zone_name=""):
    a, b = load(a_path), load(b_path)
    if a.shape != b.shape:
        print(f"  FAIL {name}: size mismatch {a.shape} vs {b.shape}")
        return False, 0
    m, _ = diff_mask(a, b)
    n = int(m.sum())
    ok = (n == 0) if expect_zero else (n > 0)
    if n:
        ys, xs = np.where(m)
        bbox = f"bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]"
        if zone is not None:
            x0, y0, x1, y1 = zone
            stray = m.copy()
            stray[y0:y1, x0:x1] = False
            s = int(stray.sum())
            print(f"  {name}: n={n} {bbox}; outside-{zone_name} stray px={s}")
            return (s == 0 and n > 0), n
        print(f"  {name}: n={n} {bbox}")
    else:
        print(f"  {name}: n=0 (pixel-identical)")
    return ok, n

ok_all = True
def check(name, cond, detail=""):
    global ok_all
    print(("  PASS " if cond else "  FAIL ") + name + (f"  {detail}" if detail else ""))
    ok_all = ok_all and bool(cond)

print("== sizes ==")
for f in ["component_full", "smoke_skip_sigma", "smoke_only_equivalence",
          "smoke_numeral99", "smoke_nochrome", "smoke_chromeonly_33",
          "smoke_chromeonly_99", "slide_033_recreated"]:
    print(f"  {f}-1.png:", Image.open(f"{V}/{f}-1.png").size)
print("  qa certified reference render_3.png:",
      Image.open(f"{BASE}/recreated_pptx/qa/slide033/render_3.png").size)

print("== GATE: component render vs CERTIFIED reference (must be 0) ==")
ok, n = report("component_full vs qa/slide033/render_3.png",
               f"{V}/component_full-1.png", f"{BASE}/recreated_pptx/qa/slide033/render_3.png")
check("GATE 0-pixel-diff vs certified render", ok, f"diff px={n}")

print("== sanity: certified pptx re-rendered this session vs banked reference ==")
ok, n = report("slide_033_recreated.pptx (re-rendered) vs qa/slide033/render_3.png",
               f"{V}/slide_033_recreated-1.png", f"{BASE}/recreated_pptx/qa/slide033/render_3.png")
check("render pipeline reproduces banked reference", ok, f"diff px={n}")

print("== component vs certified pptx, both rendered this session ==")
ok, n = report("component_full vs slide_033_recreated (same-session renders)",
               f"{V}/component_full-1.png", f"{V}/slide_033_recreated-1.png")
check("component draw == certified pptx draw", ok, f"diff px={n}")

print("== smoke: opts.skip of one block (sigma) ==")
# sigma block ink (frame pt): box (516,194) 135x25; circles r9.5 at CIRC (bottom
# y 381.5); stems top end y225 (arrowhead pad above); stubs to x574 (head pad left)
# zone with generous pad, still clear of neighbours (pills end y184, gray guide
# line x583 ends y194 from ABOVE -> belongs to y2, but skipping sigma leaves it
# unchanged so it cannot contribute diff pixels anyway)
zone = (pt(508), pt(186), pt(658), pt(390))
ok, n = report("full vs skip_sigma (diff confined to sigma zone)",
               f"{V}/component_full-1.png", f"{V}/smoke_skip_sigma-1.png",
               expect_zero=False, zone=zone, zone_name="sigma-zone")
check("skip removes exactly the sigma block", ok, f"diff px={n}")

print("== smoke: opts.only equivalence (only=all-but-sigma == skip=[sigma]) ==")
ok, n = report("only_equivalence vs skip_sigma",
               f"{V}/smoke_only_equivalence-1.png", f"{V}/smoke_skip_sigma-1.png")
check("opts.only == opts.skip complement", ok, f"diff px={n}")

print("== smoke: opts.numeral override (badge glyph proof, renderer-neutral) ==")
# badge: center (893,71)pt, d 36pt -> crop with 3pt pad
bx0, by0, bx1, by1 = pt(874), pt(52), pt(912), pt(90)
def badge(path):
    im = load(path)
    return im[by0:by1, bx0:bx1]
b_full = badge(f"{V}/component_full-1.png")
b_n99 = badge(f"{V}/smoke_numeral99-1.png")
b_c33 = badge(f"{V}/smoke_chromeonly_33-1.png")
b_c99 = badge(f"{V}/smoke_chromeonly_99-1.png")
d33 = int(np.abs(b_full - b_c33).sum())
d99 = int(np.abs(b_n99 - b_c99).sum())
ddiff = int(np.abs(b_full - b_n99).sum())
check("default badge == chrome-only(33)", d33 == 0, f"|diff|={d33}")
check("numeral-override badge == chrome-only(99)", d99 == 0, f"|diff|={d99}")
check("badge 33 != badge 99 (check not vacuous)", ddiff > 0, f"|diff|={ddiff}")
# and the ONLY difference full vs numeral99 is inside the badge crop
zone = (bx0, by0, bx1, by1)
ok, n = report("full vs numeral99 (diff confined to badge)",
               f"{V}/component_full-1.png", f"{V}/smoke_numeral99-1.png",
               expect_zero=False, zone=zone, zone_name="badge-zone")
check("numeral override touches only the badge", ok, f"diff px={n}")

print("== smoke: opts.chrome=false ==")
nc = load(f"{V}/smoke_nochrome-1.png")
check("badge center is canvas-white with chrome off",
      tuple(nc[pt(71), pt(893)]) == (255, 255, 255), f"px={tuple(nc[pt(71), pt(893)])}")
# a point on the gray chrome panel, below all content (y 530pt, x 460pt)
check("gray panel absent with chrome off",
      tuple(nc[pt(530), pt(460)]) == (255, 255, 255), f"px={tuple(nc[pt(530), pt(460)])}")
# same points on the full build for contrast
fu = load(f"{V}/component_full-1.png")
check("same points ARE chrome on the full build",
      tuple(fu[pt(530), pt(460)]) != (255, 255, 255) and tuple(fu[pt(71), pt(893)]) != (255, 255, 255),
      f"panel px={tuple(fu[pt(530), pt(460)])}, badge px={tuple(fu[pt(71), pt(893)])}")

print()
print("ALL CHECKS PASS" if ok_all else "SOME CHECKS FAILED")
raise SystemExit(0 if ok_all else 1)
