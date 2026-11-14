#!/usr/bin/env python3
# Fix for 02:42 FAIL on slide 038: top vectors must not carry ^T (original
# top box shows plain column vectors; only the middle matrix blocks use x_i^T),
# and the bottom QP expansion must be 2 bracketed lines (alpha1/alpha3 red,
# alpha2/alpha4 blue) with the subtracted alpha sum as a separate green row.
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
                [f"CC0000:\\left(\\substack{{{a}\\\\{b}}}\\right)"], 24, 0.55, 0.55)
    r4.emit("rb6_qp", [
        r"CC0000:\mathrm{Minimize:}\ \left[+4.5\alpha_1^{2} + 12.5\alpha_1\alpha_2"
        r" - 72\alpha_1\alpha_3 - 84.5\alpha_1\alpha_4\right."
        r"||0000CC:\quad +12.5\alpha_2\alpha_1 + 40.5\alpha_2^{2}"
        r" - 264.5\alpha_2\alpha_3 - 312.5\alpha_2\alpha_4",
        r"CC0000:-72\alpha_3\alpha_1 - 264.5\alpha_3\alpha_2 + 2178\alpha_3^{2}"
        r" + 2664.5\alpha_3\alpha_4"
        r"||0000CC:\quad \left.-84.5\alpha_4\alpha_1 - 312.5\alpha_4\alpha_2"
        r" + 2664.5\alpha_4\alpha_3 + 3280.5\alpha_4^{2}\right]",
    ], 20, 10.6, 0.62, left=True, rowgap=4)
    r4.emit("rb6_qp_sum", [
        r"00B050:-\left[\alpha_1 + \alpha_2 + \alpha_3 + \alpha_4\right]",
    ], 20, 3.2, 0.3)
    with open(os.path.join(OUT, "rb3_manifest.json"), "w") as fh:
        json.dump(MAN, fh, indent=1)
    print("manifest updated")
