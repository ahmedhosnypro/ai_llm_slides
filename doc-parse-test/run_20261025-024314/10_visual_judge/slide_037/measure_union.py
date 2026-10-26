#!/usr/bin/env python3
"""Union recall of ALL banked slide_037 transcripts vs the 29-string GT inventory.

Text prep: coordinate/class tokens (<x_..>, <class_..>) and markdown emphasis are
stripped before matching. Classification:
  EXACT      - GT token sequence appears verbatim (word-boundary) in a transcript
  NORMALIZED - equal after a stated collapse (case/punct/space; e.g. "Nx" vs "N x")
  PARTIAL    - >=60% shared tokens (Jaccard)
Union: a string counts once if ANY banked transcript captures it.
"""
import json
import re
import sys
from pathlib import Path

RUN = Path("/home/ahmed/Projects/ai_llm_slides/doc-parse-test/run_20261025-024314")
VJ = RUN / "10_visual_judge/slide_037"

GT = [
    "37", "Transformer Blocks (stacked over Multi-Head)",
    "Scaled Dot-Product Attention", "Multi-Head Attention",
    "Masked Multi-Head Attention", "Q", "K", "V", "MatMul", "Scale",
    "Mask (opt.)", "SoftMax", "Concat", "Linear", "h", "Encoder", "Decoder",
    "Output", "Probabilities", "Softmax", "Add & Norm", "Feed Forward", "N x",
    "Positional Encoding", "Input Embedding", "Output Embedding", "Inputs",
    "Outputs (shifted right)", "WE ARE HERE",
]
assert len(GT) == 29

# stated normalizations (collapsed forms that still count as the GT string)
NORMALIZED_VARIANTS = {
    "N x": ["Nx"],  # whitespace collapse (inventory: analysis JSON writes it Nx)
}


def clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)          # coordinate/class tokens
    text = re.sub(r"[*_`]+", " ", text)            # markdown emphasis
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)        # punctuation -> spaces
    return re.sub(r"\s+", " ", text)


def toks(s: str):
    s = s.lower().replace("&", " and ")
    return re.findall(r"[a-z0-9]+", s)


def classify(gt: str, text: str):
    t = " " + clean(text) + " "
    g = toks(gt)
    gseq = " " + " ".join(g) + " "
    # verbatim token-sequence containment (word-bounded)
    if gseq in t:
        return "EXACT"
    for var in NORMALIZED_VARIANTS.get(gt, []):
        v = " " + " ".join(toks(var)) + " "
        if v in t:
            return "NORMALIZED"
    # single-token GT: no fuzzier match allowed
    if len(g) <= 1:
        return None
    tt = set(toks(text))
    inter = len(set(g) & tt) / len(set(g) | tt) if (set(g) | tt) else 0
    if inter >= 0.6 and set(g) & tt:
        return "PARTIAL"
    return None


def transcripts():
    out = []
    for rel in [
        "03_parses/slide_037/call01_pass1/slide_037.parse.md",
        "03_parses/slide_037/call02_pass2/slide_037.parse.md",
        "03_parses/slide_037/call05_t9k/slide_037.parse.md",
        "03_parses/slide_037/call06_t9k_retry/slide_037.parse.md",
    ]:
        p = RUN / rel
        if p.exists():
            out.append((rel, p.read_text()))
    for p in sorted(VJ.glob("parses/call*/*.parse.md")):
        out.append((str(p.relative_to(RUN)), p.read_text()))
    return out


def main():
    banks = transcripts()
    print(f"banked transcripts: {len(banks)}")
    union = {}
    for gt in GT:
        hits = []
        for name, text in banks:
            c = classify(gt, text)
            if c:
                hits.append((name.split("/")[-2], c))
        if hits:
            order = {"EXACT": 0, "NORMALIZED": 1, "PARTIAL": 2}
            best = sorted((c for _, c in hits), key=lambda c: order[c])[0]
            union[gt] = (best, hits)
    exact = sum(1 for gt in GT if gt in union and union[gt][0] == "EXACT")
    normd = sum(1 for gt in GT if gt in union and union[gt][0] == "NORMALIZED")
    partial = sum(1 for gt in GT if gt in union and union[gt][0] == "PARTIAL")
    missing = [gt for gt in GT if gt not in union]
    recall = (exact + normd + 0.5 * partial) / len(GT) * 100
    print(f"union: EXACT={exact} NORMALIZED={normd} PARTIAL={partial} "
          f"MISSING={len(missing)} recall={recall:.1f}%")
    for gt in GT:
        if gt in union:
            best, hits = union[gt]
            srcs = ",".join(sorted({s for s, _ in hits}))
            print(f"  [{best}] {gt!r} <- {srcs}")
        else:
            print(f"  [MISSING] {gt!r}")
    # per-transcript solo contributions (which transcript first unlocks a string)
    solo = {}
    for gt in GT:
        if gt not in union:
            continue
        for name, _ in union[gt][1]:
            solo.setdefault(name, set()).add(gt)
    print("\nper-transcript GT captures:")
    for name in sorted(solo):
        print(f"  {name}: {len(solo[name])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
