#!/usr/bin/env python3
import json
import sys

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, "/home/codespace/ai_llm_slides/scripts")
from render_eq_wide import render

OUT = BUILD + "/eq_012"
RED = "#CC0000"

def make(name, latex, fontsize=15):
    info = render(latex, f"{OUT}/{name}.png", fontsize, RED)
    with open(f"{OUT}/{name}.json", "w") as fh:
        json.dump(info, fh)
    print(name, info["w_in"], "x", info["h_in"])

a = lambda i: rf"\alpha_{{{i}}}"
make("r1", r"[+1" + a(1) + r"^{2}+2" + a(1) + a(2) + r"-5.5" + a(1) + a(3)
    + r"-6" + a(1) + a(4) + r"+2" + a(2) + a(1) + r"+4" + a(2) + r"^{2}"
    + r"-11" + a(2) + a(3) + r"-12" + a(2) + a(4))
make("r2", r"-5.5" + a(3) + a(1) + r"-11" + a(3) + a(2) + r"+32.5" + a(3) + r"^{2}"
    + r"+36" + a(3) + a(4) + r"-6" + a(4) + a(1) + r"-12" + a(4) + a(2) + r"+36" + a(4)
    + a(3) + r"+40" + a(4) + r"^{2}]-[" + a(1) + r"+" + a(2) + r"+" + a(3) + r"+" + a(4) + r"]")
make("r10", r"[+2" + a(1) + r"^{2}+4" + a(1) + a(2) + r"-11" + a(1) + a(3)
    + r"-12" + a(1) + a(4) + r"+4" + a(2) + a(1) + r"+8" + a(2) + r"^{2}"
    + r"-22" + a(2) + a(3) + r"-24" + a(2) + a(4))
make("r11", r"-11" + a(3) + a(1) + r"-22" + a(3) + a(2) + r"+65" + a(3) + r"^{2}"
    + r"+72" + a(3) + a(4) + r"-12" + a(4) + a(1) + r"-24" + a(4) + a(2) + r"+72" + a(4)
    + a(3) + r"+80" + a(4) + r"^{2}]-[" + a(1) + r"+" + a(2) + r"+" + a(3) + r"+" + a(4) + r"]")
make("e3", r"\sum_{i}\alpha_{i}y_{i}=0", 11)
