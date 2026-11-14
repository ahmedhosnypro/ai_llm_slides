#!/usr/bin/env python3
import json
import os
import gen_eq_038_r4 as r4

OUT = r4.OUT
MAN = r4.MAN

if __name__ == "__main__":
    vectors = {
        "x1": ("1", "1"), "x2": ("2", "2"), "x3": ("7", "4"), "x4": ("8", "4"),
        "T1": ("2", "3"), "T2": ("4", "5"), "T3": ("6", "2"),
    }
    for name, (a, b) in vectors.items():
        r4.emit("rb6_vec_" + name,
                [f"CC0000:\\left(\\substack{{{a}\\\\{b}}}\\right)^{{T}}"], 24, 0.55, 0.55)
    r4.emit("rb6_dual", [
        r"CC0000:\mathrm{Minimize}||0000CC:\ \mathcal{L}_D(\alpha) = \frac{1}{2}"
        r"\overset{N}{\underset{j=1}{\sum}}\overset{N}{\underset{i=1}{\sum}}"
        r"\alpha_i\alpha_j y_i y_j \left[x_i^{T} x_j + 1\right]^2"
        r" - \overset{N}{\underset{i=1}{\sum}}\alpha_i",
    ], 24, 10.6, 0.58)
    r4.emit("rb6_qp", [
        r"CC0000:\mathrm{Minimize:}\ \left[+4.5\alpha_1^{2} + 12.5\alpha_1\alpha_2 - 72\alpha_1\alpha_3 - 84.5\alpha_1\alpha_4\right.",
        r"CC0000:+12.5\alpha_2\alpha_1 + 40.5\alpha_2^{2} - 264.5\alpha_2\alpha_3 - 312.5\alpha_2\alpha_4",
        r"CC0000:-72\alpha_3\alpha_1 - 264.5\alpha_3\alpha_2 + 2178\alpha_3^{2} + 2664.5\alpha_3\alpha_4",
        r"CC0000:\left.-84.5\alpha_4\alpha_1 - 312.5\alpha_4\alpha_2 + 2664.5\alpha_4\alpha_3 + 3280.5\alpha_4^{2}\right]",
        r"CC0000:-\left[\alpha_1 + \alpha_2 + \alpha_3 + \alpha_4\right]",
    ], 20, 10.6, 0.95, left=True, rowgap=3)
    r4.emit("rb6_cons_l", [
        r"000000:\sum\alpha_i y_i = 0", r"000000:\alpha_i \leq C", r"000000:\alpha_i \geq 0",
    ], 16, 1.9, 0.55, left=True, rowgap=4)
    r4.emit("rb6_cons_r", [
        r"000000:\alpha_1 + \alpha_2 - \alpha_3 - \alpha_4 = 0",
        r"000000:\alpha_1 \leq 1,\ \alpha_2 \leq 1,\ \alpha_3 \leq 1,\ \alpha_4 \leq 1",
        r"000000:\alpha_1 \geq 0,\ \alpha_2 \geq 0,\ \alpha_3 \geq 0,\ \alpha_4 \geq 0",
    ], 16, 3.4, 0.55, left=True, rowgap=4)
    with open(os.path.join(OUT, "rb3_manifest.json"), "w") as fh:
        json.dump(MAN, fh, indent=1)
