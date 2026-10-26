#!/usr/bin/env python3
"""Level-2 crop prep for slide_052 cascade v2 (same rules as prep_crops.py)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prep_crops import TREE, prep

# id, class, level, parent, provenance, requested(x0,y0,x1,y1), estimated, note
CROPS = [
    ("crop09", "kv_band", 2, "crop07", "level2", (170, 155, 320, 275), False,
     "K circle (309,180) + V circle (310,231) right-anchored band, box labels excluded (crop07/crop07 read only box1 label at 172px context width; wave-4: K/V readable only in low-context crops)"),
    ("crop10", "y_left", 2, "crop08", "level2", (45, 228, 195, 292), False,
     "Y tags 1-2 (x85/163) isolated from row garble Ya/Y2 (crop08)"),
    ("crop11", "y_right", 2, "crop08", "level2", (165, 228, 315, 292), False,
     "Y tag 3 (x239) + enclosure right (crop08 garbled row)"),
    ("crop12", "q_context", 2, "crop02", "level2", (500, 170, 890, 300), False,
     "boxes 3-5 bottoms + Q row context (crop02 at 2x read 5x EDA but zero Q; wave-4 q_context recipe read Q with label context)"),
    ("crop13", "box5", 2, "crop03", "level2", (700, 335, 890, 425), False,
     "5th masked box (crop03 returned only 4 of 5 instances; v1 crop10 recipe)"),
]

if __name__ == "__main__":
    rows = prep(CROPS)
    with open(os.path.join(TREE, "crops", "prep_rows_l2.json"), "w") as f:
        json.dump(rows, f, indent=2)
    print(f"OK {len(rows)} level-2 crops", file=sys.stderr)
