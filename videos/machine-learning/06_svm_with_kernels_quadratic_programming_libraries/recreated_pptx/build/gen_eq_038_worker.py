#!/usr/bin/env python3
import json
import os
import gen_eq_038_r4 as r4

OUT = r4.OUT
MAN = r4.MAN

if __name__ == "__main__":
    vectors = {
        "x1": ["1", "1"], "x2": ["2", "2"], "x3": ["7", "4"], "x4": ["8", "4"],
        "T1": ["2", "3"], "T2": ["4", "5"], "T3": ["6", "2"],
    }
    for name, values in vectors.items():
        r4.colvec("rb5_vec_" + name, values, "C00000", 15, row_h=0.17, pad=0.04)
    for i, value in enumerate(["1", "1", "-1", "-1"], 1):
        r4.emit(f"rb5_ylab_{i}", [f"000000:y_{i} = {value}"], 18, 1.0, 0.32)
    r4.emit("rb5_topcons", [
        r"000000:\alpha_1 y_1 + \alpha_2 y_2 + \alpha_3 y_3 + \alpha_4 y_4 = 0",
        r"000000:0 \leq \alpha_1 \leq C,\ 0 \leq \alpha_2 \leq C,\ 0 \leq \alpha_3 \leq C,\ 0 \leq \alpha_4 \leq C,",
    ], 22, 3.86, 1.0)
    r4.emit("rb5_dual", [
        r"0000CC:\mathrm{Minimize}\ \mathcal{L}_D(\alpha) = \frac{1}{2}"
        r"\overset{N}{\underset{j=1}{\sum}}\overset{N}{\underset{i=1}{\sum}}"
        r"\alpha_i\alpha_j y_i y_j \left[x_i^{T} x_j + 1\right]^2"
        r" - \overset{N}{\underset{i=1}{\sum}}\alpha_i",
    ], 24, 10.6, 0.58)
    r4.emit("rb5_blockA", [
        r"000000:x_1^{T}\ \left(1\ 1\right)", r"000000:x_2^{T}\ \left(2\ 2\right)",
        r"000000:x_3^{T}\ \left(7\ 4\right)", r"000000:x_4^{T}\ \left(8\ 4\right)",
    ], 20, 2.2, 1.5)
    r4.emit("rb5_blockB", [
        r"000000:x_1\ x_2\ x_3\ x_4", r"000000:\left(1\ 2\ 7\ 8\right)",
        r"000000:\left(1\ 2\ 4\ 4\right)",
    ], 20, 2.4, 1.5)
    r4.emit("rb5_blockC", [
        r"000000:x_1^{T}\ \left(2\ 4\ 11\ 12\right)", r"000000:x_2^{T}\ \left(4\ 8\ 22\ 24\right)",
        r"000000:x_3^{T}\ \left(11\ 22\ 65\ 72\right)", r"000000:x_4^{T}\ \left(12\ 24\ 72\ 80\right)",
    ], 20, 2.3, 1.5)
    r4.emit("rb5_blockD", [
        r"000000:\left[x_i^{T} x_j + 1\right]^2", r"000000:\left(3^{2}\ 5^{2}\ 12^{2}\ 13^{2}\right)",
        r"000000:\left(5^{2}\ 9^{2}\ 23^{2}\ 25^{2}\right)", r"000000:\left(12^{2}\ 23^{2}\ 66^{2}\ 73^{2}\right)",
        r"000000:\left(13^{2}\ 25^{2}\ 73^{2}\ 81^{2}\right)",
    ], 20, 2.15, 1.5)
    r4.emit("rb5_qp", [
        r"CC0000:\mathrm{Minimize:}\ \left[+4.5\alpha_1^{2} + 12.5\alpha_1\alpha_2 - 72\alpha_1\alpha_3 - 84.5\alpha_1\alpha_4 + 12.5\alpha_2\alpha_1 + 40.5\alpha_2^{2} - 264.5\alpha_2\alpha_3 - 312.5\alpha_2\alpha_4\right.",
        r"CC0000:\left.-72\alpha_3\alpha_1 - 264.5\alpha_3\alpha_2 + 2178\alpha_3^{2} + 2664.5\alpha_3\alpha_4 - 84.5\alpha_4\alpha_1 - 312.5\alpha_4\alpha_2 + 2664.5\alpha_4\alpha_3 + 3280.5\alpha_4^{2}\right]",
        r"CC0000:-\left[\alpha_1 + \alpha_2 + \alpha_3 + \alpha_4\right]",
    ], 20, 10.6, 1.0, left=True, rowgap=4)
    r4.emit("rb5_cons_l", [
        r"000000:\sum\alpha_i y_i = 0", r"000000:\alpha_i \leq C", r"000000:\alpha_i \geq 0",
    ], 16, 1.9, 0.66, left=True, rowgap=5)
    r4.emit("rb5_cons_r", [
        r"000000:\alpha_1 + \alpha_2 - \alpha_3 - \alpha_4 = 0",
        r"000000:\alpha_1 \leq 1,\ \alpha_2 \leq 1,\ \alpha_3 \leq 1,\ \alpha_4 \leq 1",
        r"000000:\alpha_1 \geq 0,\ \alpha_2 \geq 0,\ \alpha_3 \geq 0,\ \alpha_4 \geq 0",
    ], 16, 3.4, 0.66, left=True, rowgap=5)
    with open(os.path.join(OUT, "rb3_manifest.json"), "w") as fh:
        json.dump(MAN, fh, indent=1)
