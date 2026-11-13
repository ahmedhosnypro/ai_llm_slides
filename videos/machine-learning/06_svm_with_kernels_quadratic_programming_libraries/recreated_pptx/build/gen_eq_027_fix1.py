#!/usr/bin/env python3
"""Fix-cycle-1 math assets for slide 027: 3 derivation lines w/ overbrace,
true stacked column vectors, collision-free layout. Writes eq_027/fix1_*.png."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_027")
RENDER = os.path.join(HERE, "render_math.py")
BLACK, RED, BLUE = "#000000", "#C00000", "#2F2FD3"

A = []
def add(name, size, maxw, maxh, rows):
    A.append((name, size, maxw, maxh, rows))

# 3 derivation lines (peach block), each one PNG
add("f1_l1", 15, 11.5, 0.34, [
    BLACK + r":\left[a^{T}b\right]^{2}=\left[a_{1}\ a_{2}\right]\left(\overset{b_{1}}{b_{2}}\right)=\left(a_{1}b_{1}+a_{2}b_{2}\right)^{2}",
])
add("f1_l2", 15, 11.5, 0.34, [
    BLACK + r":=a_{1}^{2}b_{1}^{2}+a_{2}^{2}b_{2}^{2}+2a_{1}b_{1}a_{2}b_{2}",
])
add("f1_l3", 15, 11.5, 0.34, [
    BLACK + r":\left[a^{T}b+1\right]^{2}=\left(a_{1}b_{1}+a_{2}b_{2}\right)^{2}+2\left(a_{1}b_{1}+a_{2}b_{2}\right)+1",
])
add("f1_l4", 15, 11.5, 0.34, [
    BLACK + r":=a_{1}^{2}b_{1}^{2}+a_{2}^{2}b_{2}^{2}+2a_{1}b_{1}a_{2}b_{2}+2a_{1}b_{1}+2a_{2}b_{2}+1",
])
# true stacked column vectors
def col(items):
    inner = items[-1]
    for it in reversed(items[:-1]):
        inner = r"\overset{" + it + r"}{\underset{}{" + inner + "}}"
    return r"\left(" + inner + r"\right)"

add("f1_bcol", 16, 1.2, 1.8, [
    BLUE + ":" + col([r"b_{1}^{2}", r"b_{2}^{2}", r"\sqrt{2}b_{2}b_{1}", r"\sqrt{2}b_{1}", r"\sqrt{2}b_{2}", r"1"]),
])
add("f1_xcol", 16, 1.2, 1.8, [
    BLACK + ":" + col([r"x_{1}^{2}", r"x_{2}^{2}", r"\sqrt{2}x_{1}x_{2}", r"\sqrt{2}x_{1}", r"\sqrt{2}x_{2}", r"1"]),
])
add("f1_head", 15, 1.6, 0.3, [
    BLACK + r":\left[a^{T}b+1\right]^{2}=",
])
add("f1_whereab", 13, 2.4, 0.3, [
    BLACK + r":\mathrm{Where:}\ \phi(a)^{T}\phi(b)",
])
add("f1_wherex", 13, 3.0, 0.3, [
    BLACK + r":\mathrm{Where:}\ \phi(x)\equiv\left(\overset{x_{1}}{x_{2}}\right)\Rightarrow",
])

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
    json.dump(man, open(os.path.join(EQDIR, "fix1_manifest.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
