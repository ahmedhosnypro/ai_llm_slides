# m13_arrows.py — PIL forensics of every connector arrow on the ORIGINAL frame
# slide_005.jpg (960x540). Frame->build mapping (certified, build header):
#   frame_x = 18.0787 + 0.961084*build_x ; frame_y = 0.4700 + 0.957187*build_y
# Build targets: h circle (484.5,357.5,d19) c=(494,367); MHA inset frame (300..508, 246..515);
# SDPA inset frame (59..189, 269..491); red rect inset B (303..475, 354..396);
# enc MHA box (650..722, 355..387); banner1 (71..488,104..146); banner2 (109..415,157..199).
from PIL import Image
import sys

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_005.jpg").convert("RGB")
W, H = F.size
print("frame size", W, H)
px = F.load()

FX0, FY0, SX, SY = 18.0787, 0.4700, 0.961084, 0.957187
def to_build(fx, fy): return ((fx - FX0)/SX, (fy - FY0)/SY)
def to_frame(bx, by): return (FX0 + SX*bx, FY0 + SY*by)

def ink(x, y, maxlum=200):
    if x < 0 or y < 0 or x >= W or y >= H: return False
    r, g, b = px[int(x), int(y)]
    return (0.299*r + 0.587*g + 0.114*b) < maxlum

def is_col(x, y, rgb, tol):
    if x < 0 or y < 0 or x >= W or y >= H: return False
    r, g, b = px[int(x), int(y)]
    return abs(r-rgb[0]) <= tol and abs(g-rgb[1]) <= tol and abs(b-rgb[2]) <= tol

def scan_line(x0, y0, x1, y1, n=400):
    """walk a line, return list of (t, x, y, rgb) of ink samples"""
    out = []
    for i in range(n+1):
        t = i/n
        x = x0 + (x1-x0)*t; y = y0 + (y1-y0)*t
        if ink(x, y):
            r, g, b = px[int(x), int(y)]
            out.append((round(t,3), round(x,1), round(y,1), (r,g,b)))
    return out

def col_runs(x, y0, y1, rgb=None, tol=None, maxlum=200):
    """vertical scan at column x: list of (ystart, yend) ink runs"""
    runs = []; cur = None
    for y in range(int(y0), int(y1)+1):
        if rgb is not None:
            hit = is_col(x, y, rgb, tol)
        else:
            hit = ink(x, y, maxlum)
        if hit and cur is None: cur = y
        if not hit and cur is not None: runs.append((cur, y-1)); cur = None
    if cur is not None: runs.append((cur, int(y1)))
    return runs

def row_runs(y, x0, x1, rgb=None, tol=None, maxlum=200):
    runs = []; cur = None
    for x in range(int(x0), int(x1)+1):
        if rgb is not None:
            hit = is_col(x, y, rgb, tol)
        else:
            hit = ink(x, y, maxlum)
        if hit and cur is None: cur = x
        if not hit and cur is not None: runs.append((cur, x-1)); cur = None
    if cur is not None: runs.append((cur, int(x1)))
    return runs

print("\n=== A. banner1 bottom edge & banner2 edges (targets of the pink connectors) ===")
# banner1: build (71..488, 104..146) -> frame
b1 = [to_frame(71,104), to_frame(488,146)]
print("banner1 frame bbox:", [round(v,1) for v in b1[0]], [round(v,1) for v in b1[1]])
b2 = [to_frame(109,157), to_frame(415,199)]
print("banner2 frame bbox:", [round(v,1) for v in b2[0]], [round(v,1) for v in b2[1]])

print("\n=== B. pink connector 1 (connect_h): from banner1 bottom (build 481,146) downward ===")
# expected pink C47070 -> JPEG ~ (196,112,112) family; scan columns 455..500 in frame rows 140..250
PINK = (196,112,112); TOL = 60
def pink_hit(x,y):
    r,g,b = px[int(x),int(y)]
    return r>150 and g<160 and b<160 and (r-g)>30 and (r-b)>30
for fy in range(138, 260):
    runs = [x for x in range(430, 520) if pink_hit(x, fy)]
    if runs:
        # group consecutive
        groups=[]; s=runs[0]; p=runs[0]
        for x in runs[1:]:
            if x-p>2: groups.append((s,p)); s=x
            p=x
        groups.append((s,p))
        print("fy",fy, "pink runs:", groups)
