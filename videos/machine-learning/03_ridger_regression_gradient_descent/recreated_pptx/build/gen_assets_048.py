#!/usr/bin/env python3
"""Driver: render every equation PNG for slide 048 via render_stackeq.py.
Writes eq_*.json sidecars next to each PNG (contract of render_eq.py).
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)
S = {"fontsize": 13, "color": "000000"}

V4 = ["4", "-2", "-2"]      # [4; -2; -2]
V5 = ["5", "-1", "-1"]      # [5; -1; -1]
V11 = ["1", "1", "1"]       # [1; 1; 1]


def eq(name, segments, fontsize=13):
    spec = {"segments": segments, "fontsize": fontsize, "color": "000000"}
    out = os.path.join(ASSETS, name + ".png")
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, "render_stackeq.py"),
         json.dumps(spec), out],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAIL {name}: {r.stderr[-500:]}")
    info = json.loads(r.stdout.strip().splitlines()[-1])
    info.pop("path", None)
    with open(os.path.join(ASSETS, name + ".json"), "w") as f:
        json.dump(info, f, indent=2)
    print(f"{name}: {info['w_in']}x{info['h_in']} in, baseline_frac={info['baseline_frac']}")
    return info


# --- top-centre: Initial W vector, drawn on its own line (stacked) ---
eq("eq_initial_w_col", [
    {"col": V4},
])

# --- Initial W label (plain text, drawn as pptx text) ---
# --- REPEAT line (red text, drawn as pptx text) ---

# --- six calculation rows ---
for i, (vec, res, nxt) in enumerate([
        (["1", "1", "1"], "0", "1"),
        (["1", "2", "1"], "2", None),
        (["1", "1", "2"], "2", None),
        (["1", "5", "4"], "-4", None),
        (["1", "6", "5"], "-6", None),
        (["1", "6", "6"], "-7", None)]):
    segs = [{"t": f"d(x_{{{i + 1}}}) = "}, {"row": vec},
            {"t": " \\cdot "}, {"col": V4 if i == 0 else V5},
            {"t": f" = {res}"}]
    eq(f"eq_r{i+1}_l", segs)

# right-hand W updates
eq("eq_r1_w", [
    {"t": "W = "}, {"col": V4}, {"t": " + 1 \\cdot "}, {"col": V11},
    {"t": " = "}, {"col": V5},
])
eq("eq_r_kw", [
    {"t": "W = "}, {"col": V5},
])
print("done")
