#!/usr/bin/env python3
"""Fix-cycle-2 math assets for slide 027 per judge findings. Writes eq_027/f2_*.png."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_027")
RENDER = os.path.join(HERE, "render_math.py")
BLACK, RED, BLUE = "#000000", "#C00000", "#2F2FD3"

A = []
def add(name, size, maxw, maxh, rows):
    A.append((name, size, maxw, maxh, rows))

def col(items, bar=False):
    inner = items[-1]
    for it in reversed(items[:-1]):
        inner = r"\overset{" + it + r"}{\underset{}{" + inner + "}}"
    return (r"\left\vert" + inner + r"\right\vert") if bar else (r"\left(" + inner + r"\right)")

# top-left vector definitions (red a row x blue b column, |a^T b|^2 expansion)
add("f2_def", 13, 3.2, 1.3, [
    BLACK + r":\left[a^{T}b\right]^{2}=\left[a_{1}\ a_{2}\right]" + col([r"b_{1}", r"b_{2}"]),
])
add("f2_def2", 13, 3.2, 0.35, [
    BLACK + r":=\left(a_{1}b_{1}+a_{2}b_{2}\right)^{2}=a_{1}^{2}b_{1}^{2}+a_{2}^{2}b_{2}^{2}+2a_{1}b_{1}a_{2}b_{2}",
])
# Remember line with overbrace label |a^T b|^2
add("f2_rem", 13, 8.0, 0.35, [
    BLACK + r":\mathrm{Remember:}\ \left[a^{T}b+1\right]^{2}=\left(a^{T}b\right)^{2}+2a^{T}b+1=\left(a_{1}b_{1}+a_{2}b_{2}\right)^{2}=",
])
add("f2_rem2", 13, 8.0, 0.35, [
    BLACK + r":a_{1}^{2}b_{1}^{2}+a_{2}^{2}b_{2}^{2}+2a_{1}b_{1}a_{2}b_{2}\ ^{|a^{T}b|^{2}}+2\left(a_{1}b_{1}+a_{2}b_{2}\right)+1",
])
# peach expansion (3 lines incl. intermediate step) + continuation
add("f2_l1", 13, 10.5, 0.32, [
    BLACK + r":\left[a^{T}b+1\right]^{2}=\left(a^{T}b\right)^{2}+2a^{T}b+1",
])
add("f2_l2", 13, 10.5, 0.32, [
    BLACK + r":=\left(a_{1}b_{1}+a_{2}b_{2}\right)^{2}=a_{1}^{2}b_{1}^{2}+a_{2}^{2}b_{2}^{2}+2a_{1}b_{1}a_{2}b_{2}+2\left(a_{1}b_{1}+a_{2}b_{2}\right)+1",
])
add("f2_l3", 13, 10.5, 0.32, [
    BLACK + r":=a_{1}^{2}b_{1}^{2}+a_{2}^{2}b_{2}^{2}+2a_{1}b_{1}a_{2}b_{2}+2a_{1}b_{1}+2a_{2}b_{2}+1",
])
# lower: tan label + red phi(a) row + blue phi(b) column + = phi(a)^T phi(b)
add("f2_tan", 13, 1.6, 0.32, [RED + r":\left[a^{T}b+1\right]^{2}="])
add("f2_arow", 13, 3.4, 0.32, [
    RED + r":\left(a_{1}^{2}\ a_{2}^{2}\ \sqrt{2}a_{1}a_{2}\ \sqrt{2}a_{1}\ \sqrt{2}a_{2}\ 1\right)",
])
add("f2_bcol", 13, 1.2, 1.6, [BLUE + ":" + col([r"b_{1}^{2}", r"b_{2}^{2}", r"\sqrt{2}b_{2}b_{1}", r"\sqrt{2}b_{1}", r"\sqrt{2}b_{2}", r"1"], bar=True)])
add("f2_eq", 13, 2.0, 0.32, [BLACK + r":=\ \phi(a)^{T}\phi(b)"])
add("f2_whereab", 12, 2.4, 0.3, [BLACK + r":\mathrm{Where:}\ \phi(a)^{T}\phi(b)"])
add("f2_wherex", 12, 3.4, 0.3, [BLACK + r":\mathrm{Where:}\ \phi(x)\equiv\left(\overset{x_{1}}{x_{2}}\right)\Rightarrow"])
add("f2_xcol", 13, 1.2, 1.6, [BLACK + ":" + col([r"x_{1}^{2}", r"x_{2}^{2}", r"\sqrt{2}x_{1}x_{2}", r"\sqrt{2}x_{1}", r"\sqrt{2}x_{2}", r"1"], bar=True)])

def main():
    man = {}
    for name, size, maxw, maxh, rows in A:
        out = os.path.join(EQDIR, name + ".png")
        cmd = [sys.executable, RENDER, "--out", out, "--out-json", out + ".json",
               "--size", str(size), "--maxw", str(maxw), "--maxh", str(maxh)]
        for r in rows:
            cmd += ["--row", r]
        subprocess.run(cmd, check=True, cwd=HERE, capture_output=True)
        info = json.load(open(out + ".json"))
        man[name] = {"image": name + ".png", "w_in": info["w_in"], "h_in": info["h_in"]}
        print(name, info["w_in"], "x", info["h_in"])
    json.dump(man, open(os.path.join(EQDIR, "fix2_manifest.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
