#!/usr/bin/env python3
"""fix_tokens_045.py — attempt-5 token corrections from clean forensics16/17 + cluster
profiles (banked forensics13..17_out.txt). The attempt<=4 targets for these tokens were
derived from windows contaminated by neighboring ink (dot/ij/theta overlap); clean
original measurements:
  sub_a    ink x607..652  y339..349   (38-45w x 10h; j-tail incl)  -> target 42x10.5 @(608.5,339.25) w
  dot_a    ink x659..662  y338..340   (3x3 interpunct)             -> target 3x3   @(659,338)   w
  theta_a  ink x668..676  y333..343   (9x11)                       -> target 9x11  @(668.25,332.75) h
  ij_a     ink x678..688  y339..349   (10x10, wide gap)            -> 'i\\,j' 9.5x10 @(679.5,339) h
  sim_b    ink x548..558  y401..403   (11x3)                       -> keep size, top 400.75
  x_b      ink x561..568  y398..407   (8x9.5)                      -> target 8x9.5 @(559.5,397.75) h
  T_b      ink x571..578  y393..404   (7.5x11.5 bar+stem)          -> target 7.5x11.5 @(569.6,393) h
  region_b ink x560..612  y405..413   (52x9, letter-spaced)        -> spaced variant, h-fit <=54w @(560,404.5)
  dot_b    ink x619..621  y401..403   (3x3)                        -> target 3x3   @(619,401)   w
  theta_b  ink x629..637  y396..407   (9x12)                       -> target 9x12  @(629,395.75) h
Dots keep the dotfix dejavuserif rc (CWD with matplotlibrc); all other tokens keep the
deck's default mathtext fontset (CWD plain) to stay glyph-consistent with their siblings.
"""
import json, subprocess, sys, os

SCRIPT = "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py"
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
MANIFEST = f"{ASSETS}/eq_045_manifest.json"
CWD_PLAIN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide045/tokfix_plain"
CWD_SERIF = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide045/tokfix_serif"
for d in (CWD_PLAIN, CWD_SERIF):
    os.makedirs(d, exist_ok=True)
open(f"{CWD_SERIF}/matplotlibrc", "w").write("mathtext.fontset: dejavuserif\nfont.family: serif\n")

man = json.load(open(MANIFEST))

def render(latex, png, size, cwd):
    out = subprocess.run([sys.executable, SCRIPT, latex, png, str(size), "#000000"],
                         capture_output=True, text=True, check=True, cwd=cwd)
    return json.loads(out.stdout)

def ink_of(f):
    return (f["w_px"] - 16) * 72.0 / 600.0, (f["h_px"] - 16) * 72.0 / 600.0

def solve_token(name, latex, L, T, tw, th, solve, cwd):
    t = render(latex, f"{cwd}/{name}_trial.png", 16, cwd)
    iw, ih = ink_of(t)
    size_h = 16.0 * th / ih
    size_w = 16.0 * tw / iw
    size = round(size_h if solve in ("h", "wh") else size_w, 1)
    f = render(latex, f"{ASSETS}/eq_045_{name}.png", size, cwd)
    fw, fh = ink_of(f)
    f["ink_w_pt"] = round(fw, 2)
    f["ink_h_pt"] = round(fh, 2)
    f["target_w"], f["target_h"] = tw, th
    f["place_left"], f["place_top"] = L, T
    f["solve"] = solve
    f["size_by_alt"] = round(size_w if solve in ("h", "wh") else size_h, 1)
    man[name] = f
    flag = "  <-- ASPECT" if solve == "wh" and (abs(fw - tw) > 4 or abs(fh - th) > 4) else ""
    print(f"{name:9s} '{latex}' size={size:5.1f}  ink {fw:5.2f}x{fh:5.2f}  target {tw:5.1f}x{th:5.1f}  place ({L},{T}){flag}")

# --- region_b: pick the spaced variant whose h-solved width lands closest to 52 (cap 54.5) ---
best = None
for lat in ("region", r"r\,e\,g\,i\,o\,n", r"r\;e\;g\;i\;o\;n", r"r\;\;e\;\;g\;\;i\;\;o\;\;n"):
    t = render(lat, f"{CWD_PLAIN}/region_trial.png", 16, CWD_PLAIN)
    iw, ih = ink_of(t)
    size = round(16.0 * 9.0 / ih, 1)
    w_at = iw * size / 16.0
    print(f"  region variant '{lat}': at h=9 size {size} -> w {w_at:.1f}")
    if w_at <= 54.5 and (best is None or w_at > best[1]):
        best = (lat, w_at, size)
lat, wbest, sizeb = best
print(f"  region_b chosen: '{lat}' (w {wbest:.1f} at size {sizeb})")
f = render(lat, f"{ASSETS}/eq_045_region_b.png", sizeb, CWD_PLAIN)
fw, fh = ink_of(f)
f["ink_w_pt"], f["ink_h_pt"] = round(fw, 2), round(fh, 2)
f["target_w"], f["target_h"] = 52, 9
f["place_left"], f["place_top"] = 560, 404.5
f["solve"] = "h"
f["size_by_alt"] = round(16.0 * 52.0 / fw, 1)
man["region_b"] = f
print(f"region_b FINAL size={sizeb} ink {fw:.2f}x{fh:.2f} target 52x9 place (560,404.5)")

solve_token("sub_a",   r"r-i,\,c-j",  608.5, 339.25, 42, 10.5, "w", CWD_PLAIN)
solve_token("dot_a",   r"\cdot",      659.0, 338.0,   3,  3,    "w", CWD_SERIF)
solve_token("theta_a", r"\theta",     668.25, 332.75, 9, 11,    "h", CWD_PLAIN)
solve_token("ij_a",    r"i\,j",       679.5, 339.0,  9.5, 10,   "h", CWD_PLAIN)
solve_token("x_b",     r"x",          559.5, 397.75, 8,  9.5,  "h", CWD_PLAIN)
solve_token("T_b",     r"T",          569.6, 393.0,  7.5, 11.5, "h", CWD_PLAIN)
solve_token("dot_b",   r"\cdot",      619.0, 401.0,   3,  3,    "w", CWD_SERIF)
solve_token("theta_b", r"\theta",     629.0, 395.75, 9, 12,    "h", CWD_PLAIN)
# sim_b: size/width already correct (13.08x3.48 vs org 11x3) — only lift 2.25pt
man["sim_b"]["place_top"] = 400.75
print(f"sim_b     place_top -> 400.75 (was 403.0)")

with open(MANIFEST, "w") as fp:
    json.dump(man, fp, indent=1)
print("wrote " + MANIFEST)
