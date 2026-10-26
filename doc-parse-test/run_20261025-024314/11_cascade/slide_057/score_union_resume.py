#!/usr/bin/env python3
"""Verify wave-5 cascade union transcript recall for slide_057 (print-only)."""
GT = [
    "57", "Encoder Block M", "Encoder Block 2", "Encoder Block 1", "Encoder Block 0",
    "Y_0", "Y_1", "Y_2", "Y_3", "Y_4", "Y_5", "Y_{N-2}", "Y_{N-1}",
    "X_0", "X_1", "X_2", "X_3", "X_4", "X_5", "X_{N-2}", "X_{N-1}",
    "Word 0", "Word 1", "Word 2", "Word 3", "Word 4", "Word 5", "Word N-2", "Word N-1",
    "Word Embedding", "Positional Encoding / Embedding",
    "Residual Connection and Layer Normalization",
    "Feed Forward Networks - One Hidden with RELU Activation", "Softmax",
    "Encoder Decoder Attention", "Multi-Head Self-Attention",
    "K", "V", "Q", "Encoder", "Decoder", "Attention",
    "Word and Position Encoding",
    "SOS", "Je", "ne", "suis", "faisait",
]
# every distinct string emitted by call01_pass1 + the 17 crop parses, with its
# GT target (or None) and score class (exact=1.0, norm=0.5, miss=0.0)
EMITTED = [
    ("57", "57", 1.0, "pass1;crop05-judge-badge"),
    ("Encoder", "Encoder", 1.0, "pass1;crop03,04,07,09"),
    ("Decoder", "Decoder", 1.0, "pass1;crop04,07,09"),
    ("Encoder Block 2", "Encoder Block 2", 1.0, "pass1;crop03"),
    ("Feed Forward Networks / One Hidden with RELL Activation",
     "Feed Forward Networks - One Hidden with RELU Activation", 0.5, "pass1 (RELL)"),
    ("Residual Connection and Layer Normalization",
     "Residual Connection and Layer Normalization", 1.0, "pass1;crop05,06,19"),
    ("Encoder Block M", "Encoder Block M", 1.0, "crop01; judge VERIFIED exact"),
    ("Encoder Block 1", "Encoder Block 1", 1.0, "crop03"),
    ("Encoder Block 0", "Encoder Block 0", 1.0, "crop03"),
    ("Word Embedding", "Word Embedding", 1.0, "crop02; judge VERIFIED"),
    ("Positional Encoding / Embedding", "Positional Encoding / Embedding", 1.0, "crop02; judge VERIFIED"),
    ("Word 0", "Word 0", 1.0, "crop02; judge VERIFIED"),
    ("Word 1", "Word 1", 1.0, "crop02; judge VERIFIED"),
    ("Word 2", "Word 2", 1.0, "crop02; judge VERIFIED"),
    ("Word 3", "Word 3", 1.0, "crop02; judge VERIFIED"),
    ("Word 4", "Word 4", 1.0, "crop02; judge VERIFIED"),
    ("Word 5", "Word 5", 1.0, "crop02; judge VERIFIED"),
    ("Word N2", "Word N-2", 0.5, "crop02; judge: ink reads 'Word N-2', hyphen dropped"),
    ("Attention", "Attention", 1.0, "crop07;crop14"),
    ("Word and Position Encoding", "Word and Position Encoding", 1.0, "crop06;crop13; judge VERIFIED (settles Encoding-vs-Embedding)"),
    ("Encode Decoder Attention", "Encoder Decoder Attention", 0.5, "crop05 x6;crop09;crop19; judge: 3-line Encode/Decoder/Attention ink, 10 boxes in crop"),
    ("Multi-Head Self Attention", "Multi-Head Self-Attention", 0.5, "crop06;crop14; judge VERIFIED ink 2-line, no hyphen"),
    ("K", "K", 1.0, "crop09"),
    ("Yo", "Y_0", 0.5, "crop08 (o/0 confusion)"),
    ("Y1", "Y_1", 0.5, "crop08 (subscript marker dropped)"),
    ("Y2", "Y_2", 0.5, "crop08"),
    ("Y3", "Y_3", 0.5, "crop08"),
    ("Y5", "Y_5", 0.5, "crop08"),
    # misses / hallucination candidates (0.0)
    ("Y6", None, 0.0, "crop08 garble"),
    ("Yx1", None, 0.0, "crop08 garble x2"),
    ("Wired 0", None, 0.0, "crop10 (X-chip row garble family)"),
    ("Wired 1", None, 0.0, "crop10"),
    ("Wired 2", None, 0.0, "crop10"),
    ("Wired 3", None, 0.0, "crop10"),
    ("Wired 4", None, 0.0, "crop10"),
    ("Wired 5", None, 0.0, "crop10"),
    ("Wired M2", None, 0.0, "crop10"),
    ("Wind 4", None, 0.0, "crop16 (same family)"),
    ("Wind 5", None, 0.0, "crop16"),
    ("Wind M2", None, 0.0, "crop16"),
    ("SOHmax", None, 0.0, "crop12 (Softmax ligature garble; judge crop05 read ink 'Softmax')"),
    ("Read Forw", None, 0.0, "crop09 (judge adjudicating)"),
    ("Read Forward", None, 0.0, "crop09 x2"),
    ("T", None, 0.0, "crop14 edge partial"),
    ("0", None, 0.0, "crop02/10/14 table scaffold"),
    ("rmalization", None, 0.0, "crop14 edge-truncated"),
    ("X1", None, 0.0, "crop03 scaffold header"),
    ("X2", None, 0.0, "crop03"),
    ("X3", None, 0.0, "crop03"),
    ("X4", None, 0.0, "crop03"),
    ("X5", None, 0.0, "crop03"),
]
assert len(GT) == 48, len(GT)
scored = {g: s for _, g, s, _ in EMITTED if g}
best = {}
for _, g, s, _ in EMITTED:
    if g:
        best[g] = max(best.get(g, 0.0), s)
total = sum(best.values())
n_exact = sum(1 for v in best.values() if v == 1.0)
n_norm = sum(1 for v in best.values() if v == 0.5)
print(f"GT strings: {len(GT)}  hit: {len(best)}  EXACT: {n_exact}  NORM: {n_norm}")
print(f"union recall = {total}/48 = {100*total/48:.1f}%  (frozen wave-2: 12.5%)")
missed = [g for g in GT if g not in best]
print(f"remaining misses ({len(missed)}, weighted {48-total}):")
for g in missed:
    print("  -", g)
