#!/usr/bin/env python3
"""Emit slide 017's judge dispatch payloads (byte-for-byte from the frozen
shared_patterns/judge_protocol_03.md templates) + re-cut the Procedure-B crop
pairs. kimi-slide017, 2026-10-24 (copy of the banked emit_payloads.py, re-aimed
at attempt K=4: render_3.png is byte-current, so K=4 is the next attempt slot;
the void attempt_3 body consumed a garbage re-invoke, not an attempt).

Substitutions (ONLY these, per law):
  slideNNN -> slide017   |   "Slide NNN"/"slide NNN" -> "Slide 017"/"slide 017"
  \\bK\\b    -> 4          (attempt/render number: judge_attempt_4, crop_4_*, ...)
  NAME     -> region slug (Template B crop file names / view / capture)
  <one-line description of what the region contains> -> the region's description

Reverse byte-check: re-substituting the emitted values back must reproduce the
template block exactly. Bank: qa/slide017/emit_payloads_kimi.py + *.txt + crops.
"""
import os
import re
import shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DECK = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PROTO = os.path.join(DECK, "shared_patterns", "judge_protocol_03.md")
RENDER = os.path.join(HERE, "render_3.png")
ORIG = os.path.join(DECK, "unique_slides", "slide_017.jpg")

K = "4"          # judged attempt number (render is the current render_3.png)
TXT = open(PROTO).read()

def fenced_block(header):
    """Extract the fenced code block that follows `header`."""
    i = TXT.index(header)
    j = TXT.index("```", i)
    k = TXT.index("\n", j) + 1
    e = TXT.index("```", k)
    return TXT[k:e]

blockA = fenced_block("Comparison (the real judge")
blockB = fenced_block("Template B — crop-pair judge")

def subst(t, name=None, desc=None):
    t = t.replace("slideNNN", "slide017")
    t = t.replace("Slide NNN", "Slide 017")
    t = t.replace("slide NNN", "slide 017")
    t = re.sub(r"\bK\b", K, t)
    if name:
        t = t.replace("NAME", name)
    if desc:
        t = t.replace("<one-line description of what the region contains>", desc)
    return t

def unsubst(t, name=None, desc=None):
    t = t.replace("slide017", "slideNNN").replace("Slide 017", "Slide NNN").replace("slide 017", "slide NNN")
    t = re.sub(r"\b%s\b" % K, "K", t)
    if name:
        t = t.replace(name, "NAME")
    if desc:
        t = t.replace(desc, "<one-line description of what the region contains>")
    return t

outA = subst(blockA)
assert unsubst(outA) == blockA, "Template A reverse byte-check FAILED"
with open(os.path.join(HERE, "judge_prompt_%s.txt" % K), "w") as f:
    f.write(outA)
print("banked judge_prompt_%s.txt (%d bytes; reverse byte-check OK)" % (K, len(outA)))

ri = Image.open(RENDER).convert("RGB")
oi = Image.open(ORIG).convert("RGB")
S = ri.height / 540.0
print("render %dx%d  scale %.6f" % (ri.width, ri.height, S))

# Procedure-B regions picked from the ORIGINAL frame (dense regions, ~8px pad):
#  wbox  = W-box band 1 (red-bordered box: W, =, parenthesised vector, ||W||^2)
#  band1 = full band-1 strip (Train table, arrows, W box, Test table + mint y row)
#  test  = the three Test tables' y-column + mint y-rows (the void-judge's claim site)
REGIONS = [
    ("wbox",  (497, 119, 632, 259),
     "slide 017 W-box band 1: red italic W with underline, black '=' bars, the "
     "parenthesised 3-value vector (0.1; 1.95; 0.03) and the blue ||W||^2 = 3.8 "
     "norm line inside the red-bordered white box"),
    ("band1", (84, 118, 880, 258),
     "slide 017 band-1 strip: Train table (X1..X8 header, rows X1/X2/y, "
     "alternating blue/red ink), the two blue arrows, the W box, and the Test "
     "table (label column X1/X2/y + Test1..Test3, mint y row)"),
    ("test",  (660, 88, 880, 258),
     "slide 017 Test side: the blue Test label box, the Test1..Test3 header row "
     "with alternating red/blue ink, the test table's 4 columns including the "
     "black label column, and the mint-green y row (26.2 / 34.4 / 42.5)"),
]

for name, (x0, y0, x1, y1), desc in REGIONS:
    rc = ri.crop((int(x0 * S), int(y0 * S), int(x1 * S) + 1, int(y1 * S) + 1))
    oc = oi.crop((x0, y0, x1 + 1, y1 + 1))
    # match effective scale: LANCZOS-upscale the original crop by S
    oc2 = oc.resize((round(oc.width * S), round(oc.height * S)), Image.LANCZOS)
    rc.save(os.path.join(HERE, "crop_%s_%s_render.png" % (K, name)))
    oc2.save(os.path.join(HERE, "crop_%s_%s_orig.png" % (K, name)))
    pr = rc.width / (x1 - x0); po = oc2.width / (x1 - x0)
    print("crop %-5s frame(%d..%d, %d..%d) render %dx%d (%.4f px/frame-px) orig-upscaled %dx%d (%.4f)  match=%s"
          % (name, x0, x1, y0, y1, rc.width, rc.height, pr, oc2.width, oc2.height, po, abs(pr - po) < 0.01))
    outB, posB = subst(blockB, name=name, desc=desc)
    assert unsubst(outB, name=name, desc=desc) == blockB, "Template B(%s) reverse byte-check FAILED" % name
    with open(os.path.join(HERE, "crop_%s_%s_judge_prompt_%s.txt" % (K, name, K)), "w") as f:
        f.write(outB)
    print("  banked crop_%s_%s_judge_prompt_%s.txt (%d bytes; reverse byte-check OK)" % (K, name, K, len(outB)))

# probe command (Template A's probe block, K substituted)
probe = fenced_block("Probe first")
probe_k = subst(probe)
assert unsubst(probe_k) == probe, "probe reverse byte-check FAILED"
with open(os.path.join(HERE, "probe_cmd_%s.txt" % K), "w") as f:
    f.write(probe_k)
print("banked probe_cmd_%s.txt" % K)

shutil.copy(os.path.join(DECK, "recreated_pptx", "build", "components", "slide_017.js"),
            os.path.join(HERE, "component_attempt_%s.js" % K))
shutil.copy(os.path.join(DECK, "recreated_pptx", "build", "slide_017.js"),
            os.path.join(HERE, "build_entry_attempt_%s.js" % K))
print("banked component_attempt_%s.js + build_entry_attempt_%s.js" % (K, K))
