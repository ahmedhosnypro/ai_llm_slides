#!/usr/bin/env python3
"""Generate all mathtext equation PNGs for slide 031 (600dpi, transparent, fitted).

Each asset is fitted so its INK WIDTH matches the measured ink width of the
corresponding region in the original frame (960x540, 1px = 1pt). Placement is
recorded as the INK top-left (px) in the manifest; the build script subtracts
the 8px@600dpi pad when calling addImage.
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD = 8
ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets"

COLORS = {"red": "C00000", "blue": "0000CC", "black": "000000",
          "navy": "0A0A66", "dark": "262626"}

def render(latex, color, fontsize, out):
    fig = plt.figure(figsize=(20, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    eq = fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color="#" + color,
                  ha="center", va="baseline")
    probe = fig.text(0.15, 0.5, "x", fontsize=fontsize, color="#" + color,
                     ha="center", va="baseline")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pb = probe.get_window_extent(renderer=renderer)
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    px0, px1 = max(int(pb.x0) - 2, 0), int(pb.x1) + 2
    noProbe = ink.copy()
    noProbe[:, px0:px1 + 1] = False
    left = np.where(noProbe.any(axis=0))[0]
    if left.size and left[0] <= px1 + 20:
        raise SystemExit(f"probe overlap for {latex!r}")
    baseline_row = int(np.where(ink[:, px0:px1].any(axis=1))[0][-1])
    ink[:, :px1 + 20] = False
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, buf.shape[0])
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    h = y1 - y0; w = x1 - x0
    plt.close(fig)
    return {"w_px": int(w), "h_px": int(h),
            "baseline_frac": round(float(baseline_row - y0) / float(h), 5)}

def fit(latex, color, target_w, name, fs=12.0):
    """Iterate fontsize so ink width ~= target_w (ORIGINAL px == pt).

    The canvas renders at 600dpi, so a target of N original-px (= N pt) is
    N * 600/72 = N * 8.3333 canvas px.
    """
    target_canvas = target_w * DPI / 72.0
    out = f"{ASSETS}/{name}.png"
    for _ in range(6):
        info = render(latex, color, fs, out)
        err = target_canvas - info["w_px"]
        if abs(err) <= max(2.0, target_canvas * 0.012):
            break
        fs = fs * target_canvas / info["w_px"]
    info = render(latex, color, fs, out)
    info.update({"name": name, "latex": latex, "color": color,
                 "fontsize_pt": round(fs, 2), "target_w_px": target_w})
    print(f"  {name:12s} fs={fs:5.2f} ink={info['w_px']}px (target {target_canvas:.0f}) h={info['h_px']}px")
    return info

manifest = {}

print("== LEFT PANEL vector rows (red) ==")
manifest["lv1_r1"] = fit(r"\mathrm{sin}(\omega t)", "C00000", 58, "lv1_r1")
manifest["lv1_r2"] = fit(r"\mathrm{cos}(\omega t)", "C00000", 61, "lv1_r2")
manifest["lv2_r1"] = fit(r"\mathrm{sin}(a)", "C00000", 44, "lv2_r1")
manifest["lv2_r2"] = fit(r"\mathrm{cos}(a)", "C00000", 49, "lv2_r2")

print("== MIDDLE PANEL vector A rows (black) ==")
manifest["mva_r1"] = fit(r"\mathrm{Sin}\;(\omega(t{+}\delta))", "000000", 99, "mva_r1")
manifest["mva_r2"] = fit(r"\mathrm{cos}\,(\omega(t{+}\delta))", "000000", 96, "mva_r2")

print("== MIDDLE PANEL vector B segments (red/blue/black) ==")
manifest["mvb1_s1"] = fit(r"\mathrm{sin}(\omega t)", "C00000", 56, "mvb1_s1")
manifest["mvb1_s2"] = fit(r"\mathrm{cos}(\omega \delta)", "0000CC", 66, "mvb1_s2")
manifest["mvb1_s3"] = fit(r"+", "000000", 10, "mvb1_s3")
manifest["mvb1_s4"] = fit(r"\mathrm{cos}(\omega t)", "C00000", 61, "mvb1_s4")
manifest["mvb1_s5"] = fit(r"\mathrm{sin}(\omega \delta)", "0000CC", 61, "mvb1_s5")
manifest["mvb2_s1"] = fit(r"\mathrm{cos}(\omega t)", "C00000", 58, "mvb2_s1")
manifest["mvb2_s2"] = fit(r"\mathrm{cos}(\omega \delta)", "0000CC", 67, "mvb2_s2")
manifest["mvb2_s3"] = fit(r"-", "000000", 6, "mvb2_s3")
manifest["mvb2_s4"] = fit(r"\mathrm{sin}(\omega t)", "C00000", 56, "mvb2_s4")
manifest["mvb2_s5"] = fit(r"\mathrm{sin}(\omega \delta)", "0000CC", 61, "mvb2_s5")

print("== MIDDLE PANEL result vector segments ==")
manifest["mvr1_s1"] = fit(r"\mathrm{sin}(a)", "C00000", 46, "mvr1_s1")
manifest["mvr1_s2"] = fit(r"\mathrm{cos}(b)", "0000CC", 56, "mvr1_s2")
manifest["mvr1_s3"] = fit(r"+", "000000", 10, "mvr1_s3")
manifest["mvr1_s4"] = fit(r"\mathrm{cos}(a)", "C00000", 52, "mvr1_s4")
manifest["mvr1_s5"] = fit(r"\mathrm{sin}(b)", "0000CC", 47, "mvr1_s5")
manifest["mvr2_s1"] = fit(r"\mathrm{cos}(a)", "C00000", 51, "mvr2_s1")
manifest["mvr2_s2"] = fit(r"\mathrm{cos}(b)", "0000CC", 52, "mvr2_s2")
manifest["mvr2_s3"] = fit(r"-", "000000", 6, "mvr2_s3")
manifest["mvr2_s4"] = fit(r"\mathrm{sin}(a)", "C00000", 46, "mvr2_s4")
manifest["mvr2_s5"] = fit(r"\mathrm{sin}(b)", "0000CC", 46, "mvr2_s5")

print("== DEFINITION BOXES ==")
manifest["db1_let"] = fit(r"\mathrm{Let}", "000000", 23, "db1_let")
manifest["db1_a"] = fit(r"\omega t=a\;,", "C00000", 46, "db1_a")
manifest["db1_b"] = fit(r"\omega \delta=b", "0000CC", 41, "db1_b")
manifest["db2"] = fit(r"\mathrm{sin}^{2}(a)+\mathrm{cos}^{2}(a)=1", "000000", 148, "db2")

print("== CALLOUT ==")
manifest["callout"] = fit(r"\mathbf{=2}\,(\mathbf{1-cos}(\omega\delta))", "0A0A66", 135, "callout")

print("== DERIVATION ROWS (R2..R6 single black images) ==")
manifest["dR2"] = fit(
    r"[\,\mathrm{sin}(a)\,(\mathrm{cos}(b)-1)+\mathrm{cos}(a)\,\mathrm{sin}(b)\,]^{2}"
    r"+\,[\,-\mathrm{sin}(a)\,\mathrm{sin}(b)+\mathrm{cos}(a)\,(\mathrm{cos}(b)-1)\,]^{2}",
    "000000", 662, "dR2")
manifest["dR3"] = fit(
    r"[\,\mathrm{sin}(a)^{2}(\mathrm{cos}(b)-1)^{2}+\mathrm{cos}^{2}(a)\,\mathrm{sin}^{2}(b)"
    r"+\,2\,\mathrm{sin}(a)\,\mathrm{cos}(a)\,\mathrm{sin}(b)\,(\mathrm{cos}(b)-1)\,]\,+",
    "000000", 608, "dR3")
manifest["dR4"] = fit(
    r"[\,\mathrm{sin}^{2}(a)\,\mathrm{sin}^{2}(b)+\mathrm{cos}^{2}(a)\,(\mathrm{cos}(b)-1)^{2}"
    r"-\,2\,\mathrm{sin}(a)\,\mathrm{cos}(a)\,\mathrm{sin}(b)\,(\mathrm{cos}(b)-1)\,]",
    "000000", 571, "dR4")
manifest["dR5"] = fit(
    r"\mathrm{sin}(a)^{2}\,(\mathrm{cos}(b)-1)^{2}+\mathrm{cos}^{2}(a)\,\mathrm{sin}^{2}(b)"
    r"+\mathrm{sin}^{2}(a)\,\mathrm{sin}^{2}(b)+\mathrm{cos}^{2}(a)\,(\mathrm{cos}(b)-1)^{2}",
    "000000", 596, "dR5")
manifest["dR6"] = fit(
    r"[\,\mathrm{sin}(a)^{2}+\mathrm{cos}^{2}(a)\,]\,(\mathrm{cos}(b)-1)^{2}"
    r"+\,[\,\mathrm{sin}(a)^{2}+\mathrm{cos}^{2}(a)\,]\,(\mathrm{sin}^{2}(b)\,)"
    r"=(\mathrm{cos}(b)-1)^{2}+\mathrm{sin}^{2}(b)",
    "000000", 652, "dR6")

print("== R7 segments (black) ==")
manifest["dR7_s1"] = fit(r"\mathrm{cos}^{2}(b)", "000000", 54, "dR7_s1")
manifest["dR7_s2"] = fit(r"-2\,\mathrm{cos}(b)\,+1\,+", "000000", 119, "dR7_s2")
manifest["dR7_s3"] = fit(r"\mathrm{sin}^{2}(b)", "000000", 51, "dR7_s3")
manifest["dR7_s4"] = fit(r"=\,2\,-2\,\mathrm{cos}(b)\,=\,2(1-\mathrm{cos}(b)\,)", "000000", 211, "dR7_s4")

print("== R1 mixed segments ==")
# BLUE bracket-open, RED sin(a), BLUE cos(b) + , RED cos(a), BLUE sin(b) - ,
# RED sin(a) [highlight], BLUE ]2 + [ - , RED sin(a), BLUE sin(b) + , RED cos(a),
# BLUE cos(b) - , RED cos(a) [highlight], BLUE ]2
_i = render(r"[", "0000CC", 22.2, f"{ASSETS}/r1_s01.png")
_i.update({"name": "r1_s01", "latex": "[", "color": "0000CC", "fontsize_pt": 22.2, "target_w_px": 5})
manifest["r1_s01"] = _i
print(f"  r1_s01       fs=22.2 fixed ink={_i['w_px']}px h={_i['h_px']}px")
manifest["r1_s02"] = fit(r"\mathrm{sin}(a)", "C00000", 42, "r1_s02")
manifest["r1_s03"] = fit(r"\mathrm{cos}(b)\,+", "0000CC", 62, "r1_s03")
manifest["r1_s04"] = fit(r"\mathrm{cos}(a)", "C00000", 46, "r1_s04")
manifest["r1_s05"] = fit(r"\mathrm{sin}(b)\,-", "0000CC", 55, "r1_s05")
manifest["r1_s06"] = fit(r"\mathrm{sin}(a)", "C00000", 44, "r1_s06")
manifest["r1_s07"] = fit(r"]^{2}\,+\,[\,-", "0000CC", 70, "r1_s07")
manifest["r1_s08"] = fit(r"\mathrm{sin}(a)", "C00000", 42, "r1_s08")
manifest["r1_s09"] = fit(r"\mathrm{sin}(b)\,+", "0000CC", 59, "r1_s09")
manifest["r1_s10"] = fit(r"\mathrm{cos}(a)", "C00000", 45, "r1_s10")
manifest["r1_s11"] = fit(r"\mathrm{cos}(b)\,-", "0000CC", 58, "r1_s11")
manifest["r1_s12"] = fit(r"\mathrm{cos}(a)", "C00000", 47, "r1_s12")
_i = render(r"]^{2}", "0000CC", 18.2, f"{ASSETS}/r1_s13.png")
_i.update({"name": "r1_s13", "latex": "]^{2}", "color": "0000CC", "fontsize_pt": 18.2, "target_w_px": 17})
manifest["r1_s13"] = _i
print(f"  r1_s13       fs=18.2 fixed ink={_i['w_px']}px h={_i['h_px']}px")
manifest["dEqMid"] = fit(r"=", "000000", 16, "dEqMid")
_i = render(r"=", "0000CC", 16, f"{ASSETS}/dEq.png")
_i.update({"name": "dEq", "latex": "=", "color": "0000CC", "fontsize_pt": 16, "target_w_px": 11})
manifest["dEq"] = _i
print(f"  dEq          fs=16 fixed ink={_i['w_px']}px h={_i['h_px']}px")

# placement table (ink top-left px in original frame coordinates)
P = {
    # left panel vector 1 (brackets x88..89 / ~x167, y71..134; rows y76..94, y110..128)
    "lv1_r1": (100, 76), "lv1_r2": (100, 110),
    # left panel vector 2 (rows inside highlights)
    "lv2_r1": (112, 150), "lv2_r2": (112, 186),
    # middle vector A rows
    "mva_r1": (226, 78), "mva_r2": (226, 112),
    # middle vector B row1 y80..99 / row2 y114..132
    "mvb1_s1": (371, 81), "mvb1_s2": (434, 81), "mvb1_s3": (507, 84),
    "mvb1_s4": (524, 81), "mvb1_s5": (592, 81),
    "mvb2_s1": (374, 115), "mvb2_s2": (439, 115), "mvb2_s3": (512, 120),
    "mvb2_s4": (524, 115), "mvb2_s5": (587, 115),
    # result vector rows y156..174 / y188..206
    "mvr1_s1": (396, 157), "mvr1_s2": (449, 157), "mvr1_s3": (508, 160),
    "mvr1_s4": (524, 157), "mvr1_s5": (582, 157),
    "mvr2_s1": (392, 189), "mvr2_s2": (450, 189), "mvr2_s3": (514, 194),
    "mvr2_s4": (526, 189), "mvr2_s5": (579, 189),
    # def boxes
    "db1_let": (703, 134), "db1_a": (735, 134), "db1_b": (787, 134),
    "db2": (692, 176),
    # callout text
    "callout": (584, 472),
    # derivation rows (ink top)
    "dR2": (85, 299), "dR3": (88, 338), "dR4": (88, 359), "dR5": (89, 397),
    "dR6": (83, 431),
    # R7 segments
    "dR7_s1": (77, 473), "dR7_s2": (136, 473), "dR7_s3": (250, 473), "dR7_s4": (306, 473),
    # R1 segments (y-band 265..288, core text top ~267)
    "r1_s01": (85, 266), "r1_s02": (96, 267), "r1_s03": (144, 267),
    "r1_s04": (212, 267), "r1_s05": (264, 267), "r1_s06": (325, 267),
    "r1_s07": (374, 267), "r1_s08": (445, 267), "r1_s09": (493, 267),
    "r1_s10": (559, 267), "r1_s11": (610, 267), "r1_s12": (674, 267),
    "r1_s13": (723, 267),
    "dEqMid": (348, 111),
    # trailing '=' column (vertically centered per row at placement time in JS)
    "dEq": (767, 270),
}
for k, (x, y) in P.items():
    manifest[k]["ink_x"] = x
    manifest[k]["ink_y"] = y

with open(f"{ASSETS}/eq_manifest.json", "w") as f:
    json.dump(manifest, f, indent=1)
print(f"\nwrote {ASSETS}/eq_manifest.json with {len(manifest)} assets")
