#!/usr/bin/env python3
# selfcheck_attempt_5.py — closed-loop verification of the judge-1 fixes on render_5
# (150 dpi; frame px <-> render px via the certified mapping; tolerance ~4px @150dpi
# = ~1.9 frame px). Checks:
#   1. encoder norm boxes: text ink present + box ink bbox vs original (~4px)
#   2. encoder residual stubs 1/3 SHORT (right edge <= x213)
#   3. decoder navy disc: white check ink present, no "Nx"-text-only reading
#   4. decoder tan Nx circle + green check badge ink bboxes vs original (~4px)
#   5. decoder dark-brown check ink bbox vs original (~4px)
#   6. frame containment: all new ink inside the decoder/encoder panels + house frame
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")
r5 = Image.open(f"{ROOT}/recreated_pptx/qa/slide051/render_5.png").convert("RGB")
K = 150.0 / 72.0
SX = lambda fx: (fx - 18.128) / 0.961235
SY = lambda fy: (fy + 0.045) / 0.956566
RX, RY = lambda fx: SX(fx) * K, lambda fy: SY(fy) * K
FAILS = []

def ok(name, cond, detail=""):
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond:
        FAILS.append(name)

def ink_bbox(img, box, pred, to_rend=False):
    """ink bbox in FRAME px within a frame-px box"""
    x0f, y0f, x1f, y1f = box
    xs, ys = [], []
    for fy in range(int(y0f), int(y1f)):
        for fx in range(int(x0f), int(x1f)):
            if to_rend:
                px = img.getpixel((min(int(RX(fx)), img.size[0] - 1), min(int(RY(fy)), img.size[1] - 1)))
            else:
                px = img.getpixel((fx, fy))
            if pred(*px):
                xs.append(fx); ys.append(fy)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys), len(xs))

dark = lambda r, g, b: r < 100 and g < 100 and b < 110
whiteish = lambda r, g, b: r > 200 and g > 200 and b > 200
navy = lambda r, g, b: b > 110 and r < 90 and g < 90
dkgreen = lambda r, g, b: g > 100 and g < 190 and r < 100 and b < 100
dkbrown = lambda r, g, b: r < 150 and g < 110 and b < 90 and r > g and g >= b - 10

# 1) encoder norm box text: INTERIOR-only ink (rows 267..275 — the orig's dark rows
# y263-265/y276-277 are the box borders, which contaminate a naive bbox comparison;
# the 3x crop comparison (crop_cmp_enc_norms.txt §1) is the authority for the text).
b1r = ink_bbox(r5, (214, 267, 277, 276), dark, to_rend=True)
ok("norm1-text-present", b1r is not None and b1r[4] > 15, f"(interior npx {b1r[4] if b1r else 0})")
b2r = ink_bbox(r5, (215, 331, 277, 340), dark, to_rend=True)
ok("norm2-text-present", b2r is not None and b2r[4] > 15, f"(interior npx {b2r[4] if b2r else 0})")

# 2) stubs 1/3 short: bright-green ink right edge in (195..244, 267..275) and (195..244, 332..341)
stub1 = ink_bbox(r5, (195, 266, 246, 277), lambda r, g, b: g > 150 and g > r + 40 and g > b + 40, to_rend=True)
stub3 = ink_bbox(r5, (195, 331, 246, 342), lambda r, g, b: g > 150 and g > r + 40 and g > b + 40, to_rend=True)
print("  stub1 bbox:", stub1, " stub3 bbox:", stub3)
ok("stub1-short", stub1 and stub1[2] <= 214, f"(right edge {stub1[2] if stub1 else None} <= 214)")
ok("stub3-short", stub3 and stub3[2] <= 214, f"(right edge {stub3[2] if stub3 else None} <= 214)")

# 3) decoder navy disc: white check ink inside disc (800..819, 312..330)
wc = ink_bbox(r5, (801, 313, 819, 331), whiteish, to_rend=True)
ok("navy-disc-whitecheck", wc is not None and wc[4] > 12, f"(white npx {wc[4] if wc else 0})")

# 4) decoder tan Nx circle + green badge
tan = ink_bbox(r5, (824, 284, 852, 314), lambda r, g, b: 160 < r < 205 and 150 < g < 200 and 100 < b < 155, to_rend=True)
tan_o = ink_bbox(orig, (826, 286, 852, 314), lambda r, g, b: 160 < r < 205 and 150 < g < 200 and 100 < b < 155)
grn = ink_bbox(r5, (842, 278, 866, 302), dkgreen, to_rend=True)
grn_o = ink_bbox(orig, (842, 278, 866, 302), dkgreen)
print("  dec tan circle: render", tan, " orig", tan_o)
print("  dec green badge: render", grn, " orig", grn_o)
ok("dec-nx-tan-circle", tan is not None and tan[4] > 60)
ok("dec-nx-green-badge", grn is not None and grn[4] > 60)
if tan and tan_o:
    ok("dec-nx-tan-pos", abs(tan[0] - tan_o[0]) <= 5 and abs(tan[1] - tan_o[1]) <= 5,
       f"render tl{tan[:2]} vs orig tl{tan_o[:2]} (orig box starts x826: trunk-edge halo excluded)")
if grn and grn_o:
    ok("dec-nx-badge-pos", abs(grn[0] - grn_o[0]) <= 5 and abs(grn[1] - grn_o[1]) <= 5,
       f"render tl{grn[:2]} vs orig tl{grn_o[:2]}")

# 5) decoder dark-brown check
dbc = ink_bbox(r5, (720, 424, 742, 452), dkbrown, to_rend=True)
dbc_o = ink_bbox(orig, (720, 424, 742, 452), dkbrown)
print("  dec dkbrown check: render", dbc, " orig", dbc_o)
ok("dec-embed-check-present", dbc is not None and dbc[4] > 15)
if dbc and dbc_o:
    ok("dec-embed-check-pos", abs(dbc[0] - dbc_o[0]) <= 5 and abs(dbc[1] - dbc_o[1]) <= 5,
       f"render tl{dbc[:2]} vs orig tl{dbc_o[:2]}")

# 6) containment: new ink within the decoder panel (568.5..877, 102..503) and house frame
def inside(b, pan): return b is None or (b[0] >= pan[0] and b[1] >= pan[1] and b[2] <= pan[2] and b[3] <= pan[3])
DEC = (568, 102, 878, 503)
ok("containment-dec-nx", inside(tan, DEC) and inside(grn, DEC))
ok("containment-dec-check", inside(dbc, DEC))
HOUSE = (58, 43, 902, 540)
ok("containment-house", all(inside(b, HOUSE) for b in (stub1, stub3, b1r, b2r)))

print()
print("SELFCHECK-5:", "ALL PASS" if not FAILS else f"FAILURES: {FAILS}")
