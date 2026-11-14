#!/usr/bin/env python3
import json
import subprocess
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
OUT = V / "recreated_pptx/build/assets"
RENDER_EQ = "/home/codespace/ai_llm_slides/scripts/render_eq.py"
OUT.mkdir(parents=True, exist_ok=True)

for name, mathtext, color in [
    ("d1", r"d_{1}(x)", "#CC2222"),
    ("d2", r"d_{2}(x)", "#0000FF"),
    ("d3", r"d_{3}(x)", "#00A000"),
]:
    stem = f"eq_008_{name}"
    png = OUT / f"{stem}.png"
    sidecar = OUT / f"{stem}.json"
    result = subprocess.run(
        ["python3", RENDER_EQ, mathtext, str(png), "12", color],
        check=True, capture_output=True, text=True,
    )
    info = json.loads(result.stdout)
    info["mathtext"] = mathtext
    sidecar.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    a = np.asarray(Image.open(png).convert("RGBA"))
    ink = a[a[..., 3] > 100, :3]
    dominant = Counter(map(tuple, ink)).most_common(1)[0]
    expected = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
    if dominant[0] != expected:
        raise SystemExit(f"{stem}: dominant ink {dominant[0]} != {expected}")
    print(stem, info["w_px"], info["h_px"], info["baseline_frac"], dominant)
