#!/usr/bin/env python3
"""render_tokens_045.py v2 — FINAL token set for slide 045 equations.
Split tokens (Σ glyph + small limits; x + small sub) where matplotlib's built-in
script-size proportions overshoot the measured boxes. Solves each token's size from
its measured ink box (frame px = pt). Writes eq_045_manifest.json for the build.
Placement data (left, top in frame px) also stored here — single source of truth."""
import json, subprocess, sys

SCRIPT = "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py"
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets"
PAD_PT = 8 * 72.0 / 600.0  # render_eq PAD_PX=8 at 600dpi -> 0.96pt on each side

# name: (mathtext, place_left, place_top, target_ink_w_pt, target_ink_h_pt, solve)
# solve: 'h' = match height (width floats), 'w' = match width, 'wh' = height then verify
TOKENS = [
    # ---- eq(a): a_{r,c} = SUM_i SUM_j x_{r-i,c-j} . theta_{ij}   (x471..694, y312..366) ----
    ("a_rc",    r"a_{r,c}",                 471.0, 335.5, 24, 12,  "wh"),
    ("eq_a",    r"=",                       502.5, 337.0, 11,  8,  "w"),
    ("sum1",    r"\sum",                    524.0, 324.0, 24, 32,  "wh"),
    ("lim1u",   r"a",                       533.5, 312.0,  9,  7,  "h"),
    ("lim1l",   r"i=-a",                    522.0, 356.0, 31.4, 8.5,  "h"),
    ("sum2",    r"\sum",                    563.5, 324.0, 21, 32,  "wh"),
    ("lim2u",   r"b",                       571.5, 312.0,  6,  7,  "h"),
    ("lim2l",   r"j=-b",                    564.5, 357.0, 29.2, 9.3,  "h"),
    ("x_a",     r"x",                       595.0, 335.5, 10, 11,  "h"),
    ("sub_a",   r"r-i,\,c-j",               607.0, 346.5, 36,  9,  "w"),
    ("dot_a",   r"\cdot",                   646.5, 341.5,  6,  7,  "h"),
    ("theta_a", r"\theta",                  662.5, 331.5, 11, 15,  "wh"),
    ("ij_a",    r"ij",                      674.0, 345.5, 5.1, 9.5,  "h"),
    # ---- eq(b): a_{r,c} ~ x_{region}^{T} . theta   (x522..644, y392..413) ----
    ("a_b",     r"a",                       522.0, 397.5,  9,  9,  "h"),
    ("rc_b",    r"r,c",                     531.5, 406.0, 11,  7,  "h"),
    ("sim_b",   r"\sim",                    547.5, 403.0, 13,  4,  "w"),
    ("x_b",     r"x",                       562.5, 397.5, 11, 13,  "h"),
    ("region_b", r"region",                 575.5, 405.5, 34,  8,  "w"),
    ("T_b",     r"T",                       569.5, 391.5,  9,  5,  "h"),
    ("dot_b",   r"\cdot",                   613.5, 402.0,  6,  7,  "h"),
    ("theta_b", r"\theta",                  628.0, 395.5, 11.0, 14.0,  "h"),
    # ---- eq(c): frac = SUM_r SUM_c x_{r-i,c-j}   (x479..677, y437..490) ----
    ("frac_c",  r"\frac{\partial a_{r,c}}{\partial \theta_{i,j}}", 479.5, 445.0, 40, 41, "wh"),
    ("eq_c",    r"=",                       522.5, 461.5, 13.7, 6.1, "h"),
    ("sum3",    r"\sum",                    546.0, 448.0, 21, 33,  "wh"),
    ("lim3u",   r"N-2a",                    546.5, 437.5, 27,  8,  "w"),
    ("lim3l",   r"r=0",                     547.0, 482.0, 25,  9,  "w"),
    ("sum4",    r"\sum",                    584.0, 448.0, 21, 33,  "wh"),
    ("lim4u",   r"N-2b",                    583.5, 437.5, 29,  8,  "w"),
    ("lim4l",   r"c=0",                     584.0, 482.0, 24,  9,  "w"),
    ("x_c",     r"x",                       621.0, 461.5, 15, 13.0,  "h"),
    ("sub_c",   r"r-i,\,c-j",               639.0, 464.5, 38, 10,  "w"),
]

manifest = {}
for name, latex, L, T, tw, th, solve in TOKENS:
    trial_png = f"{ASSETS}/eq_045_{name}_trial.png"
    out = subprocess.run([sys.executable, SCRIPT, latex, trial_png, "16", "#000000"],
                         capture_output=True, text=True, check=True)
    t = json.loads(out.stdout)
    ink_w = (t["w_px"] - 16) * 72.0 / 600.0
    ink_h = (t["h_px"] - 16) * 72.0 / 600.0
    size_h = 16.0 * th / ink_h
    size_w = 16.0 * tw / ink_w
    size = round(size_h if solve in ("h", "wh") else size_w, 1)
    final_png = f"{ASSETS}/eq_045_{name}.png"
    out2 = subprocess.run([sys.executable, SCRIPT, latex, final_png, str(size), "#000000"],
                          capture_output=True, text=True, check=True)
    f = json.loads(out2.stdout)
    f["ink_w_pt"] = round((f["w_px"] - 16) * 72.0 / 600.0, 2)
    f["ink_h_pt"] = round((f["h_px"] - 16) * 72.0 / 600.0, 2)
    f["target_w"], f["target_h"] = tw, th
    f["place_left"], f["place_top"] = L, T
    f["solve"] = solve
    f["size_by_alt"] = round(size_w if solve in ("h", "wh") else size_h, 1)
    manifest[name] = f
    flag = ""
    if solve == "wh" and (abs(f["ink_w_pt"] - tw) > 4 or abs(f["ink_h_pt"] - th) > 4):
        flag = "  <-- ASPECT MISMATCH (alt size %s)" % f["size_by_alt"]
    print(f"{name:9s} size={size:5.1f}  ink {f['ink_w_pt']:5.1f}x{f['ink_h_pt']:4.1f}  target {tw:4.0f}x{th:3.0f}{flag}")

with open(f"{ASSETS}/eq_045_manifest.json", "w") as fp:
    json.dump(manifest, fp, indent=1)
print("wrote eq_045_manifest.json")
