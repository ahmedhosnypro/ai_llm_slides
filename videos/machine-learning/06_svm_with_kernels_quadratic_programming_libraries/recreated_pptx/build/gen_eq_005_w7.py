#!/usr/bin/env python3
"""Wave-4 math assets for slide 005, content from qa/reanalysis2/slide_005_analysis.txt only.
Color correction vs w3, verified by PIL sampling of unique_slides/slide_005.jpg:
E1/E2 black; E3 body red (#C00000) with red arrow and GREEN "Quadratic form";
definition lines: black LHS, red arrow, red RHS; matrix/grid labels black.
Assets: build/eq_005/w7_*.png + .json sidecars + w7_manifest.json (inches).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_005")
RENDER = os.path.join(HERE, "render_math.py")

BLACK = "#000000"
RED = "#C00000"
GREEN = "#008000"
BLUE = "#0000FF"
V3 = r"\left(\overset{\overset{x_1}{x_2}}{x_3}\right)"

A = []


def add(name, box, size, maxh, rows, rowgap=10):
    A.append((name, box, size, maxh, rows, rowgap))


add("w7_e1", [0.030, 0.080, 0.972, 0.215], 18, 1.0125, [
    BLACK + r":\left(x_1\ \ x_2\ \ x_3\right)\ \left(\overset{\overset{a_{11}\ \ a_{12}\ \ a_{13}}{a_{21}\ \ a_{22}\ \ a_{23}}}{a_{31}\ \ a_{32}\ \ a_{33}}\right)\ " + V3 +
    r"\ =\ \left(\overset{\overset{(a_{11}x_1{+}a_{21}x_2{+}a_{31}x_3)}{(a_{12}x_1{+}a_{22}x_2{+}a_{32}x_3)}}{(a_{13}x_1{+}a_{23}x_2{+}a_{33}x_3)}\right)\ " + V3 + r"\ =",
])
add("w7_e2", [0.030, 0.222, 0.972, 0.288], 14, 0.22, [
    BLACK + r":(a_{11}x_1{+}a_{21}x_2{+}a_{31}x_3)x_1 + (a_{12}x_1{+}a_{22}x_2{+}a_{32}x_3)x_2 + (a_{13}x_1{+}a_{23}x_2{+}a_{33}x_3)x_3 =",
    BLACK + r":a_{11}x_1^2 + a_{21}x_1x_2 + a_{31}x_1x_3 + a_{12}x_1x_2 + a_{22}x_2^2 + a_{32}x_2x_3 + a_{13}x_1x_3 + a_{23}x_2x_3 + a_{33}x_3^2 =",
], rowgap=6)
E3_ROW = (RED + r":a_{11}x_1^2 + a_{22}x_2^2 + a_{33}x_3^2 + (a_{21}{+}a_{12})x_1x_2 + "
          r"(a_{31}{+}a_{13})x_1x_3 + (a_{32}{+}a_{23})x_1x_3||" +
          RED + r":\ \Rightarrow\ ||" + GREEN + r":\mathrm{Quadratic\ form}")
add("w7_e3", [0.030, 0.295, 0.972, 0.350], 22, 0.4125, [E3_ROW])
DEFS = [
    ("w7_d1", 0.445, r"a_{11}", r"x_1^2", None),
    ("w7_d2", 0.500, r"a_{22}", r"x_2^2", None),
    ("w7_d3", 0.555, r"a_{33}", r"x_3^2", None),
    ("w7_d4", 0.605, r"a_{21}{+}a_{12}", r"x_1x_2", (r"a_{12}{=}a_{21}{=}\frac{1}{2}\ \mathrm{coefficinet\ of\ }", r"x_1x_2")),
    ("w7_d5", 0.647, r"a_{13}{+}a_{31}", r"x_1x_3", (r"a_{13}{=}a_{31}{=}\frac{1}{2}\ \mathrm{coefficinet\ of\ }", r"x_1x_3")),
    ("w7_d6", 0.692, r"a_{32}{+}a_{23}", r"x_2x_3", (r"a_{32}{=}a_{23}{=}\frac{1}{2}\ \mathrm{coefficinet\ of\ }", r"x_2x_3")),
]
for name, y0, lhs, var, extra in DEFS:
    row = (BLACK + ":" + lhs + "||" + BLUE + r":\ \Rightarrow\ ||" + BLACK + r":\mathrm{Coefficient\ of\ }||" + RED + ":" + var)
    if extra:
        row += ("||" + BLUE + r":\ \Rightarrow\ ||" + BLACK + ":" + extra[0] + "||" + RED + ":" + extra[1])
    add(name, [0.070, y0, 0.610, y0 + 0.055], 14, 0.4125, [row])

add("w7_hdr", [0.100, 0.762, 0.250, 0.822], 18, 0.45,
    [RED + r":x_1\ \ \ x_2\ \ \ x_3"])
MATS = [
    ("w7_m1", 0.815, r"x_1\ \ \ a_{11}\ \ \ a_{12}\ \ \ a_{13}"),
    ("w7_m2", 0.865, r"x_2\ \ \ a_{21}\ \ \ a_{22}\ \ \ a_{23}"),
    ("w7_m3", 0.915, r"x_3\ \ \ a_{31}\ \ \ a_{32}\ \ \ a_{33}"),
]
for name, y0, latex in MATS:
    add(name, [0.080, y0, 0.230, y0 + 0.057], 13, 0.4275, [RED + ":" + latex])

def g(var):
    return BLACK + r":\mathrm{coef\ of\ }||" + RED + ":" + var
def g5(var):
    return BLUE + r":0.5\ ||" + BLACK + r":\mathrm{coef\ of\ }||" + RED + ":" + var
GRID = [
    g(r"x_1^2"), g5(r"x_1x_2"), g5(r"x_1x_3"),
    g5(r"x_1x_2"), g(r"x_2^2"), g5(r"x_2x_3"),
    g5(r"x_1x_3"), g5(r"x_2x_3"), g(r"x_3^2"),
]
COLS = [(0.390, 0.500), (0.500, 0.630), (0.630, 0.790)]
ROWS = [(0.815, 0.845), (0.875, 0.905), (0.935, 0.965)]
for i, latex in enumerate(GRID):
    r, c = divmod(i, 3)
    add("w7_b%d" % (i + 1), [COLS[c][0], ROWS[r][0], COLS[c][1], ROWS[r][1]], 10, 0.225,
        [latex])


def main():
    os.makedirs(EQDIR, exist_ok=True)
    man = {}
    bad = []
    for name, box, size, maxh, rows, rowgap in A:
        x0, y0, x1, y1 = box
        maxw = (x1 - x0) * 13.33
        boxh = (y1 - y0) * 7.5
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".json")
        cmd = [sys.executable, RENDER, "--out", out, "--size", str(size),
               "--maxw", str(maxw), "--maxh", str(maxh),
               "--rowgap", str(rowgap), "--out-json", js]
        for r in rows:
            cmd += ["--row", r]
        subprocess.run(cmd, check=True, cwd=HERE)
        with open(js) as fh:
            info = json.load(fh)
        ok = info["w_in"] <= maxw + 0.03 and info["h_in"] <= boxh + 0.03
        if not ok:
            bad.append(name)
        print(name, info["w_in"], "x", info["h_in"], "box", round(maxw, 3), "x", round(boxh, 3),
              "OK" if ok else "OVERFLOW")
        man[name] = {"image": name + ".png", "x": round(x0 * 13.33, 4), "y": round(y0 * 7.5, 4),
                     "w": round(maxw, 4), "h": round(boxh, 4),
                     "w_in": info["w_in"], "h_in": info["h_in"]}
    with open(os.path.join(EQDIR, "w7_manifest.json"), "w") as fh:
        json.dump(man, fh, indent=2)
    if bad:
        raise SystemExit("OVERFLOW: %s" % ", ".join(bad))


if __name__ == "__main__":
    main()
