#!/usr/bin/env python3
"""selfcheck_resume.py — fresh closed-loop PIL ink check of slide 019's main elements
vs the original frame (resume worker 2026-10-12).

Checks the exact regions the builder's cropcmp_enc_2/cropcmp_dec_2 (01:03-01:07) flagged
on render_2, plus the builder's m15-m18 measured pixel facts, in 960x540 frame space
(1px = 1pt). Render space = 150dpi 2001x1125, scale = 2000/960 (use 2.0833).

A region PASSES only if ink presence AGREES between original and render:
  - solid-red border rows (dec MHA): original must have them; render_2 must too.
  - navy inter-layer chevrons: original has navy px; render must too.
  - leader arrowheads into enc/dec FF boxes: original dark px; render must too.
Tolerance: ink-count bands, plus ~4px @150dpi positional agreement for the bands.
"""
from PIL import Image
import sys

RENDER = sys.argv[1] if len(sys.argv) > 1 else "recreated_pptx/qa/slide019/render_2.png"
ORIG = "unique_slides/slide_019.jpg"

render = Image.open(RENDER).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
S = 2000 / 960.0  # 960-frame pt -> 150dpi px (render is 2001 wide; 0.5px slack)

def rimg_region(x0, y0, x1, y1):
    """crop render (150dpi) for a 960-space box"""
    return render.crop((round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S)))

def oimg_region(x0, y0, x1, y1):
    return orig.crop((round(x0), round(y0), round(x1), round(y1)))

def count(px_img, pred):
    n = 0
    for p in px_img.getdata():
        if pred(p):
            n += 1
    return n

def red_ink(p):
    r, g, b = p
    return r > 110 and g < 90 and b < 90 and (r - max(g, b)) > 50

def navy_ink(p):
    r, g, b = p
    return b > 60 and b > r + 30 and b > g + 30 and r < 120

def dark_ink(p):
    r, g, b = p
    return r < 70 and g < 70 and b < 70

def green_ink(p):
    r, g, b = p
    return g > 120 and g > r + 30 and g > b + 30

checks = []

def check(name, orig_n, rend_n, require_in_both=True, min_orig=5, min_rend=5):
    """agree = both sides same presence/absence"""
    orig_has = orig_n >= min_orig
    rend_has = rend_n >= min_rend
    ok = (orig_has and rend_has) if require_in_both else (orig_has == rend_has)
    checks.append((name, orig_n, rend_n, ok))
    return ok

# --- 1. decoder MHA SOLID red border (960-space): top y277, bottom y309.5, right x820.5
# original m17: top 70/70 bot 70/70 right 28/28 (solid); render_2: top 1/70 right 15/28 (absent)
check("decMHA top border y276-279 x750-820 red ink",
      count(oimg_region(750, 275, 820, 280), red_ink),
      count(rimg_region(750, 275, 820, 280), red_ink))
check("decMHA bottom border y308-311 x750-820 red ink",
      count(oimg_region(750, 307, 820, 312), red_ink),
      count(rimg_region(750, 307, 820, 312), red_ink))
check("decMHA right border x819-822 y278-309 red ink",
      count(oimg_region(818, 278, 823, 309), red_ink),
      count(rimg_region(818, 278, 823, 309), red_ink))
# left border must be ABSENT in both (m17: 0/28)
check("decMHA LEFT border x747-750 y278-309 (must be absent in both)",
      count(oimg_region(746, 279, 751, 308), red_ink),
      count(rimg_region(746, 279, 751, 308), red_ink),
      require_in_both=False, min_orig=8, min_rend=8)

# --- 2. navy inter-layer chevrons (m16/m18): (781-786, y197-205), (781-786, y253-261), (767-777, y311-321)
check("navy chevrons dec-top y195-206 x779-788",
      count(oimg_region(779, 195, 788, 206), navy_ink),
      count(rimg_region(779, 195, 788, 206), navy_ink))
check("navy chevrons dec-mid y252-261 x779-788",
      count(oimg_region(779, 252, 788, 261), navy_ink),
      count(rimg_region(779, 252, 788, 261), navy_ink))
check("navy chevrons dec-low y310-322 x766-778",
      count(oimg_region(766, 310, 778, 322), navy_ink),
      count(rimg_region(766, 310, 778, 322), navy_ink))

# --- 3. leader arrowheads into FF boxes (m16 y=302-305 x644-648 dark; m18 y=235-238 x742-745 dark)
check("leader3 arrowhead into dec FF x741-746 y234-239 dark ink",
      count(oimg_region(741, 234, 746, 239), dark_ink),
      count(rimg_region(741, 234, 746, 239), dark_ink))
check("leader4 arrowhead into enc FF x643-649 y301-306 dark ink",
      count(oimg_region(643, 301, 649, 306), dark_ink),
      count(rimg_region(643, 301, 649, 306), dark_ink))

# --- 4. green residual buses (enc x637 y277-405; dec x834 y210-404)
check("enc green bus x635-640 y280-403 green ink",
      count(oimg_region(635, 280, 640, 403), green_ink),
      count(rimg_region(635, 280, 640, 403), green_ink))
check("dec green trunk x832-837 y212-403 green ink",
      count(oimg_region(832, 212, 837, 403), green_ink),
      count(rimg_region(832, 212, 837, 403), green_ink))
# horizontal connector bands (m16: y253-261 jog x781-786; y264 band x765-805; y324-325 x785-793)
check("dec green band y256-260 x790-834 green ink",
      count(oimg_region(790, 256, 834, 260), green_ink),
      count(rimg_region(790, 256, 834, 260), green_ink))
check("dec green band y318-322 x790-834 green ink",
      count(oimg_region(790, 318, 834, 322), green_ink),
      count(rimg_region(790, 318, 834, 322), green_ink))

# --- 5. legend callout boxes exist in both (sanity, inherited-ok region)
def blue_ink(p):
    r, g, b = p
    return b > 150 and b > r + 30 and g > 100

check("legend1 fill y105-127 x150-330 light-blue fill",
      count(oimg_region(150, 105, 330, 127), blue_ink),
      count(rimg_region(150, 105, 330, 127), blue_ink))

fails = [c for c in checks if not c[3]]
for name, o, r, ok in checks:
    print(f"{'PASS' if ok else 'FAIL'}  orig={o:5d} render={r:5d}  {name}")
print(f"\nTOTAL: {len(checks) - len(fails)}/{len(checks)} PASS")
sys.exit(1 if fails else 0)
