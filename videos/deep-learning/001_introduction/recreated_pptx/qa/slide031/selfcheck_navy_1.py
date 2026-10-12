"""Re-measure body lines + label with a STRICT navy mask (periwinkle borders polluted
the blueish mask in attempt 1). Also bullet text-only (exclude dot)."""
from PIL import Image
import numpy as np

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide031/render_1.png"
im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
S = W / 960.0
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
# navy text: saturated dark blue, R,G near 0 (borders are ~(153,153,204) -> R>100)
navy = (R < 90) & (G < 90) & (B > 95) & (B - R > 60)

def bbox(x0, x1, y0, y1, label, target=None):
    m = navy[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    rows = np.where(m.any(axis=1))[0]; cols = np.where(m.any(axis=0))[0]
    if not len(rows):
        print(f"  {label}: EMPTY"); return None
    fx0, fy0 = x0 + cols[0]/S, y0 + rows[0]/S
    fx1, fy1 = x0 + cols[-1]/S, y0 + rows[-1]/S
    line = f"  {label}: x {fx0:.1f}..{fx1:.1f}  y {fy0:.1f}..{fy1:.1f}"
    if target: line += f"   target {target}   d=({fx0-target[0]:+.1f},{fy0-target[1]:+.1f},{fx1-target[2]:+.1f},{fy1-target[3]:+.1f})"
    print(line)

print("== BODY (strict navy) ==")
bbox(95, 890, 132, 180, "L1", (109, 142, 677, 160))
bbox(95, 890, 182, 216, "L2", (109, 195, 239, 211))
bbox(95, 890, 216, 244, "L3a", (108, 220, 759, 242))
bbox(95, 890, 244, 275, "L3b", (109, 246, 486, 268))
print("== LABEL TEXT (strict navy; window inside box borders) ==")
bbox(382, 602, 438, 473, "label", (388, 445, 596, 464))
