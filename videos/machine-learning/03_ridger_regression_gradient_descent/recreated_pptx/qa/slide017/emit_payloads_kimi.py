#!/usr/bin/env python3
"""Emit slide 017's judge dispatch payloads (byte-for-byte from the frozen
shared_patterns/judge_protocol_03.md templates) + re-cut the Procedure-B crop
pairs. kimi-slide017, 2026-10-24.

Substitutions (ONLY these, per law):
  slideNNN -> slide017   |  "Slide NNN"/"slide NNN" -> "Slide 017"/"slide 017"
  \\bK\\b    -> 4          (attempt/render number)
  NAME     -> region slug (Template B crop file names / view)
  <one-line description of what the region contains> -> the region's description

K is scoped to the COMMAND part of each template block (before `-p "`). The
-p payload prose contains no K token (it does contain bare numbers such as
"(3)"/"(4)"), so applying \\bK\\b there and reverse-substituting later would
corrupt the prose. Each part is therefore byte-checked separately.

Reverse byte-check: re-substituting the emitted values back must reproduce the
template block exactly. Bank: qa/slide017/*.txt + crops.
"""
import os
import re
import shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PROTO = os.path.join(DECK, "shared_patterns", "judge_protocol_03.md")
RENDER = os.path.join(HERE, "render_3.png")
ORIG = os.path.join(DECK, "unique_slides", "slide_017.jpg")

K = "4"
TXT = open(PROTO).read()

def fenced_block(header):
    i = TXT.index(header)
    j = TXT.index("```", i)
    k = TXT.index("\n", j) + 1
    e = TXT.index("```", k)
    return TXT[k:e]

def subst_nnn(t):
    t = t.replace("slideNNN", "slide017")
    t = t.replace("Slide NNN", "Slide 017")
    t = t.replace("slide NNN", "slide 017")
    return t

def unsubst_nnn(t):
    t = t.replace("slide017", "slideNNN")
    t = t.replace("Slide 017", "Slide NNN")
    t = t.replace("slide 017", "slide NNN")
    return t

def split_cmd_payload(block):
    """Return (head, tail) split at the `-p "` opener, keeping the opener."""
    m = re.search(r'-p "', block)
    if not m:
        return None
    i = m.end()
    return block[:i], block[i:]

def emit_template(block, header, name=None, desc=None, outfile=None, label=""):
    """Byte-exact emit with K scoped to the command part."""
    sp = split_cmd_payload(block)
    assert sp is not None, "no -p opener in %s" % label
    head, tail = sp
    assert not re.search(r"\bK\b", tail), "%s: K token inside -p payload" % label
    head_k = re.sub(r"\bK\b", K, head)
    tail_n = subst_nnn(tail)
    if name:
        tail_n = tail_n.replace("NAME", name)
    if desc:
        tail_n = tail_n.replace("<one-line description of what the region contains>", desc)
    out = head_k + tail_n
    # reverse byte-checks, per part
    back_head = unsubst_nnn(re.sub(r"\b%s\b" % K, "K", head_k))
    back_tail = unsubst_nnn(tail_n)
    if name:
        back_tail = back_tail.replace(name, "NAME")
    if desc:
        back_tail = back_tail.replace(desc, "<one-line description of what the region contains>")
    assert back_head == head, "%s: command-part reverse byte-check FAILED" % label
    assert back_tail == tail, "%s: payload-part reverse byte-check FAILED" % label
    if outfile:
        with open(outfile, "w") as f:
            f.write(out)
        print("banked %s (%d bytes; per-part reverse byte-check OK)" % (os.path.basename(outfile), len(out)))
    return out

blockA = fenced_block("Comparison (the real judge")
blockB = fenced_block("Template B — crop-pair judge")
emit_template(blockA, "Template A", outfile=os.path.join(HERE, "judge_prompt_%s.txt" % K), label="Template A")

ri = Image.open(RENDER).convert("RGB")
oi = Image.open(ORIG).convert("RGB")
S = ri.height / 540.0
print("render %dx%d  scale %.6f  (render_3.png md5-proven current)" % (ri.width, ri.height, S))

# Procedure-B regions picked from the ORIGINAL frame (dense regions, ~8px pad):
#  wbox  = W-box band 1 (red-bordered box: W, =, parenthesised vector, ||W||^2)
#  band1 = full band-1 strip (Train table, arrows, W box, Test table + mint y row)
#  test  = the three Test tables' label column + mint y-rows
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
    oc2 = oc.resize((round(oc.width * S), round(oc.height * S)), Image.LANCZOS)
    rc.save(os.path.join(HERE, "crop_%s_%s_render.png" % (K, name)))
    oc2.save(os.path.join(HERE, "crop_%s_%s_orig.png" % (K, name)))
    pr = rc.width / (x1 - x0); po = oc2.width / (x1 - x0)
    print("crop %-5s frame(%d..%d, %d..%d) render %dx%d (%.4f px/frame-px) orig-upscaled %dx%d (%.4f)  match=%s"
          % (name, x0, x1, y0, y1, rc.width, rc.height, pr, oc2.width, oc2.height, po, abs(pr - po) < 0.01))
    emit_template(blockB, "Template B", name=name, desc=desc,
                  outfile=os.path.join(HERE, "crop_%s_%s_judge_prompt_%s.txt" % (K, name, K)),
                  label="Template B(%s)" % name)

probe = fenced_block("Probe first")
probe_out = subst_nnn(probe)
probe_out = re.sub(r"\bK\b", K, probe_out)
probe_back = unsubst_nnn(probe_out)
probe_back = re.sub(r"\b%s\b" % K, "K", probe_back)
assert probe_back == probe, "probe reverse byte-check FAILED"
with open(os.path.join(HERE, "probe_cmd_%s.txt" % K), "w") as f:
    f.write(probe_out)
print("banked probe_cmd_%s.txt (%d bytes; reverse byte-check OK)" % (K, len(probe_out)))

shutil.copy(os.path.join(DECK, "recreated_pptx", "build", "components", "slide_017.js"),
            os.path.join(HERE, "component_attempt_%s.js" % K))
shutil.copy(os.path.join(DECK, "recreated_pptx", "build", "slide_017.js"),
            os.path.join(HERE, "build_entry_attempt_%s.js" % K))
print("banked component_attempt_%s.js + build_entry_attempt_%s.js" % (K, K))
print("ALL PAYLOAD FILES EMITTED FOR K=%s" % K)
