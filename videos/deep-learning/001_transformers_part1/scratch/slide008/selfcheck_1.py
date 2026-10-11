#!/usr/bin/env python3
"""Closed-loop self-check: render_1.png (150dpi, ~2000px wide) vs slide_008.jpg measurements.
Frame px -> render px: * (2000/960) = 1.875? No — render is 150dpi over 13.33in = 2000px;
frame is 960px over 13.33in => factor = 2000/960 = 2.0833. Report deltas per element."""
from PIL import Image
import sys

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "recreated_pptx/qa/slide008/render_1.png").convert("RGB")
print("render size:", im.size)
ld = im.load()
W, H = im.size
F = W / 960.0
print(f"scale factor frame->render: {F:.4f}")

def blueink(p):
    r, g, b = p
    return b > 110 and b - r > 40 and g < 140

def lightblue(p):
    r, g, b = p
    return b > 200 and b - r > 12 and g > 190 and r > 170

def bbox(pred, x0, y0, x1, y1):
    minx, miny, maxx, maxy, n = 10**9, 10**9, -1, -1, 0
    for y in range(int(y0), int(y1)):
        for x in range(int(x0), int(x1)):
            if pred(ld[x, y]):
                n += 1
                minx = min(minx, x); maxx = max(maxx, x)
                miny = min(miny, y); maxy = max(maxy, y)
    return (minx, miny, maxx, maxy, n) if n else None

def cmp(tag, measured_frame, got, tol=8):
    if got is None:
        print(f"  {tag}: MISSING (want {measured_frame})")
        return
    want = [round(v * F, 1) for v in measured_frame[:4]]
    d = [round(got[i] - want[i], 1) for i in range(4)]
    ok = all(abs(v) <= tol for v in d)
    print(f"  {tag}: got {got[:4]} want~{want} d={d} {'OK' if ok else '<< CHECK'}")

print("== callout box (frame 44,169..325,229) ==")
cb = bbox(lightblue, 0, int(160*F), int(480*F), int(250*F))
print("  box bbox:", cb)

print("== callout line1 ink (frame 77,183..293,196 underline 197) ==")
l1 = bbox(blueink, int(50*F), int(172*F), int(330*F), int(200*F))
cmp("line1 ink", (77, 183, 293, 196), l1, tol=10)
# underline row: densest row in y 195..201 band
best = None
for y in range(int(194*F), int(202*F)):
    n = sum(1 for x in range(int(60*F), int(320*F)) if blueink(ld[x, y]))
    if best is None or n > best[1]: best = (y, n)
print(f"  underline densest row: y={best[0]} n={best[1]} (frame 197 -> {197*F:.0f})")

print("== callout line2 ink (frame 59,202..313,213) ==")
l2 = bbox(blueink, int(50*F), int(200*F), int(330*F), int(218*F))
cmp("line2 ink", (59, 202, 313, 213), l2, tol=10)

print("== (Challenges) ink (frame 376,87..533,111) ==")
ch = bbox(blueink, int(300*F), int(80*F), int(640*F), int(118*F))
cmp("(Challenges)", (376, 87, 533, 111), ch, tol=10)

print("== wait boxes (frame (52,257..184,292) and (213,255..345,289)) ==")
w1 = bbox(lightblue, int(30*F), int(246*F), int(190*F), int(305*F))
cmp("wait1 box", (52, 257, 184, 292), w1, tol=8)
w2 = bbox(lightblue, int(195*F), int(246*F), int(360*F), int(305*F))
cmp("wait2 box", (213, 255, 345, 289), w2, tol=8)
t1 = bbox(blueink, w1[0], w1[1], w1[2], w1[3]) if w1 else None
cmp("wait1 text", (64, 261, 173, 289), t1, tol=10)
t2 = bbox(blueink, w2[0], w2[1], w2[2], w2[3]) if w2 else None
cmp("wait2 text", (225, 258, 334, 286), t2, tol=10)
# wait text line splits
for tag, t in (("wait1", t1), ("wait2", t2)):
    if not t: continue
    rows = [(y, sum(1 for x in range(t[0], t[2]+1) if blueink(ld[x, y]))) for y in range(t[1], t[3]+1)]
    rows = [r for r in rows if r[1]]
    ys = [y for y, _ in rows]
    g = sorted([(ys[i+1]-ys[i], ys[i]) for i in range(len(ys)-1)], reverse=True)
    print(f"  {tag} line gap: {g[:1]} (frame pitch 16 -> {16*F:.0f} render px)")

print("== leaders present? (frame: callout-leader (326,211)->(466,326.5); vert1 x207.5 286..305; vert2 x368 284..305) ==")
def anybluish(p):
    r, g, b = p
    return b - r > 18 and b > 150 and g < 225
# vert1: x 200..215, y 288..302
v1 = bbox(anybluish, int(200*F), int(288*F), int(216*F), int(303*F))
print("  vert1:", v1, f"(want x ~{207.5*F:.0f}, y {286*F:.0f}..{305*F:.0f})")
v2 = bbox(anybluish, int(360*F), int(286*F), int(376*F), int(303*F))
print("  vert2:", v2, f"(want x ~{368*F:.0f}, y {284*F:.0f}..{305*F:.0f})")
cl = bbox(anybluish, int(330*F), int(213*F), int(470*F), int(250*F))
print("  callout leader upper:", cl, f"(want ~(346..360)*F at y~(228..240)*F)")

print("== containment: delta ink inside boxes ==")
if cb:
    inside = bbox(blueink, cb[0]-2, cb[1]-2, cb[2]+3, cb[3]+3)
    print("  callout ink bbox:", inside, " box:", cb[:4], "OK" if inside and inside[0]>=cb[0]-1 and inside[1]>=cb[1]-1 and inside[2]<=cb[2]+1 and inside[3]<=cb[3]+1 else "<< OVERFLOW")
if w1:
    inside = bbox(blueink, w1[0]-2, w1[1]-2, w1[2]+3, w1[3]+3)
    print("  wait1 ink bbox:", inside, " box:", w1[:4], "OK" if inside and inside[0]>=w1[0]-1 and inside[1]>=w1[1]-1 and inside[2]<=w1[2]+1 and inside[3]<=w1[3]+1 else "<< OVERFLOW")
if w2:
    inside = bbox(blueink, w2[0]-2, w2[1]-2, w2[2]+3, w2[3]+3)
    print("  wait2 ink bbox:", inside, " box:", w2[:4], "OK" if inside and inside[0]>=w2[0]-1 and inside[1]>=w2[1]-1 and inside[2]<=w2[2]+1 and inside[3]<=w2[3]+1 else "<< OVERFLOW")
