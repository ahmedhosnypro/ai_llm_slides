#!/usr/bin/env python3
"""Level-3 crop prep for slide_052 cascade v2 (same rules as prep_crops.py)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prep_crops import TREE, prep

CROPS = [
    ("crop14", "k_band", 3, "crop09", "level3", (170, 155, 320, 225), False,
     "K circle (309,180) alone: kv_band read 'Y1 Y2' (glyph confusion with K/V/Y3 competing); single-glyph band at compliant 162px width"),
    ("crop15", "v_band", 3, "crop09", "level3", (170, 210, 320, 270), False,
     "V circle (310,231) alone: same isolation logic as crop14"),
    ("crop16", "inputs_row", 3, "crop05", "level3", (40, 425, 240, 480), False,
     "I/feel/Sick input boxes: crop05 read feel+Sick but dropped 'I' instance (wave-4 leftpanel read all 3 split)"),
]

if __name__ == "__main__":
    rows = prep(CROPS)
    with open(os.path.join(TREE, "crops", "prep_rows_l3.json"), "w") as f:
        json.dump(rows, f, indent=2)
    print(f"OK {len(rows)} level-3 crops", file=sys.stderr)
