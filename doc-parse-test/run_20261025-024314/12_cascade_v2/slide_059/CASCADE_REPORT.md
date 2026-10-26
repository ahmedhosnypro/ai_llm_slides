# CASCADE_REPORT — slide_059 (wave 5B requirement-compliant crop cascade)

- Scope: `slide_059_cascade_v2` · agent `worker-slide_059_cascade_v2` · 2026-10-25.
- Source frame: `videos/deep-learning/002_transformers_part2/unique_slides/slide_059.jpg`
  (960×540, md5 `fb03ceaae946177062b7e097d68ffde3`).
- Brief: `01_prompts/worker_slide_059_cascade_v2.md` · protocol: MISSION_PROTOCOL.md
  WAVE-5B ADDENDUM (authoritative) · GT: `04_ground_truth/slide_059/inventory.md` (46 strings).

## Headline

**Union recall: 58.7% → 100% (46/46 GT strings) · 16 crops · 16 doc-parse parse calls ·
13 vision-judge legs · parallel speedup ≈ 2.6×**

- Frozen wave-2 recall: 27/46 = 58.7% (full-frame transcript only, 3× byte-identical reads).
- Cascade union: 46/46 = 100% — every GT row recovered at transcript level; C₁/C₂ PARTIAL
  (0.5 credit) upgraded to full.
- Route split: doc-parse crop parses alone → 42/46 = 91.3%; vision-gateway crop judges
  added X₁, X₄, X₅, Y₀ (requirement-2 judge leg as a first-class recovery route).

## Recall trajectory

| Stage | Credit | Recall | Evidence |
|---|---|---|---|
| Wave-2 frozen (full-frame, 119-token self-stop) | 27/46 | 58.7% | 05_comparison/slide_059_comparison.md |
| + Level-1 crops (6) | +11 | 82.6% | Σ(call01) · C₃-partials→wait: X-tails(call06), Y₂–Y₅(call03), Σ(call01), in-circle Softmax(call01/08) — see table below |
| + Level-2 crops (7) | +5.5 | 94.6% | C₁C₂C₃ clean + C-upgrades (call07), X₀X₂X₃ (call09), Y-tails (call11), Y₁ (call16), X₁-slot read (judges) |
| + Level-3 crops (3) | +1 | 96.7% | Y₁ confirmed (call16 pictogram), chart structures |
| + Vision-judge leg (13) | +2 | **100%** | Y₀ (crop12+crop16), X₁ (crop02+crop13), X₄/X₅ (crop02) |

Per-row credit ledger is in `compose/COMPOSED_ANALYSIS.md` (§Recall accounting).

## Tree (manifest.json is authoritative; boxes in frame px, scale, transform per crop)

```
full-frame call05_t9k (region source: 1 class_Picture block, origin-only)
├─ crop01_softmax_cluster      L1 judge-supplement (390,36,655,139)×3   → no-internal-structure
│  ├─ crop07_labels_row_l2     L2 semantic trigger: IC1/IC2/IC3 garble  → no-internal-structure  [C1 C2 C3 CLEAN]
│  └─ crop08_circles_l2        L2 semantic trigger: 2/3 Softmax+Σ pairs → no-new-information     [Σ→Z misread; judges confirm Σ×3]
├─ crop02_xrow_labels          L1 judge-supplement (168,400,897,452)×2  → no-new-information
│  ├─ crop09_xrow_left_l2      L2 semantic trigger: Xl/Xj head garbles  → no-new-information
│  │  └─ crop15_x12_l3         L3 trigger: dup X3, X1 slot unresolved   → no-new-information     [bare X]
│  └─ crop10_xrow_mid_l2       L2 semantic trigger: O fragment @ X4/X5  → no-new-information
│     └─ crop14_x345_l3        L3 trigger: bare X X @ X4/X5             → no-new-information     [bare X ×4]
├─ crop03_yrow_labels          L1 judge-supplement (168,206,897,264)×2  → no-new-information
│  ├─ crop11_yrow_tail_l2      L2 semantic trigger: YNz/YNI tail garbles→ no-internal-structure  [Y N-2 / YN-1]
│  └─ crop12_yrow_head_l2      L2 semantic trigger: Yd head garble      → no-new-information     [X1 X2 misread; judges: Y0 Y1 Y2]
│     └─ crop16_y012_l3        L3 trigger: Y0/Y1 zone unresolved        → no-internal-structure  [Y1 + pictogram chart]
├─ crop04_pooled_row           L1 judge-supplement (369,137,656,176)×3  → no-new-information     [textless; judge: ~20 cells, no text]
├─ crop05_annotation_stack     L1 judge-supplement (51,115,299,525)×2   → no-new-information
│  └─ crop13_annot_lower_l2    L2 semantic trigger: 1/5 stacks read     → no-internal-structure  [ranked_table chart; judge reads X₁ on cell strip]
└─ crop06_class_picture_est    L1 parse-class-block (710,400,960,540)×3 estimated:true → no-internal-structure [XN2 XN1 Vector PN-2 PN-1]
```

Stop reasons: 5× no-internal-structure · 11× no-new-information · 0× leaf · 0× too-small ·
0× backstop. Caps: 16/16 crops (at cap) · 16/24 parse calls. Every stop reason is semantic —
the crop cap bound the tree size, not its depth.

## Per-crop yield

| Crop | L | Scale | Parse novel strings | Judge verdict (novel-string crops) |
|---|---|---|---|---|
| crop01_softmax_cluster | 1 | 3× | `Σ`×2 (verbatim glyph!), in-circle `Softmax`×2, `IC1/IC2/IC3` | C₁C₂C₃ char-exact; Σ in all 3 circles; Softmax in all 3 |
| crop02_xrow_labels | 1 | 2× | `Xl Xj X3 X4 O` (garbles) | **Full X-row read: X₀–X₅ + X_{N-2}/X_{N-1}, digits explicit** |
| crop03_yrow_labels | 1 | 2× | `Y2 Y3 Y4 Y5` | Y-row 8 labels w/ subscripts (Y₀ read "i" `[?]`, superseded) |
| crop04_pooled_row | 1 | 3× | — (textless) | ~20 pastel cells, 5-color cycle, **no text in cells** |
| crop05_annotation_stack | 1 | 2× | — (same stack line) | not judged (no novel strings) |
| crop06_class_picture_est | 1 | 3× | `XN2 XN1 Vector PN-2 Vector PN-1` | X_{N-2}/X_{N-1}/Vector tails confirmed ("N-3" slip `[?]`) |
| crop07_labels_row_l2 | 2 | 3× | `C1 C2 C3` clean | char-exact C₁C₂C₃ + stray "s" (= "Classes" bleed, real ink) |
| crop08_circles_l2 | 2 | 3× | `Softmax Z` ×2 | per-circle: Softmax + Σ ×3 |
| crop09_xrow_left_l2 | 2 | 3× | `X0 X2 X3` | 4 heads w/ middle-digit shuffle `[?]` (superseded by crop02 judge) |
| crop10_xrow_mid_l2 | 2 | 3× | — (bare X) | not judged (no novel strings) |
| crop11_yrow_tail_l2 | 2 | 3× | `Y N-2`, `YN-1` | Y_{N-2} confirmed; "N-3" slip `[?]` |
| crop12_yrow_head_l2 | 2 | 3× | `X1 X2` (misreads) | **same box = Y₀ Y₁ Y₂** (letter+digit explicit) |
| crop13_annot_lower_l2 | 2 | 2× | `ranked_table` chart (class_Chart) | panel structure + **X₁ read on cell strip** + Vector_P0/P1 |
| crop14_x345_l3 | 3 | 3× | — (bare X ×4) | **CONFIRMS X₃ X₄ X₅, digits 3/4/5 "clearly readable", slot-consistent (retry after 1 gateway timeout)** |
| crop15_x12_l3 | 3 | 3× | — (bare X ×2) | not judged (no novel strings) |
| crop16_y012_l3 | 3 | 3× | `Y1` + pictogram chart (class_Chart) | **Y₀ Y₁ Y₂ Y₃ explicit** + partial Y₄ |

Judge coverage: 13 judged crops (11 required by the novel-strings rule + crop02 required +
crop14 corroboration) + 1 probe; 3 crops not judged (no novel strings — crop05/crop10/crop15,
noted in manifest). Probe: `PROBE-OK` (judges/probe/).

## Parallel speedup

| Batch | Calls (concurrency) | Wall | Σ latency | Speedup |
|---|---|---|---|---|
| L1 parses | 6 (4+2) | 8.2 s | 19 s | 2.3× |
| L2 parses | 7 (4+3) | 11.5 s | 33 s | 2.9× |
| L3 parses | 3 (3) | 3.2 s | 8 s | 2.5× |
| **Total** | **16** | **≈23 s** | **60 s** | **≈2.6×** |

Vision judges ran sequential (max 1 in-flight per brief); gateway latency degraded during
the run (13 s → ~9 min/call), so the judge leg is not parallel-speedup-relevant.

## Key findings

1. **Crop scale fixes the parser's subscript weakness selectively.** The full-frame parse
   lost all 16 X/Y subscript labels + Σ + C₃; crop parses recovered 12 of 16 X/Y labels,
   Σ (verbatim), C₁C₂C₃ — but the 4/5 subscript digits never survived doc-parse at ≤3×
   (bare `X` in every attempt), and the Y-head zone consistently misread (Yd, or X↔Y swap).
2. **The vision-judge leg is a first-class recovery route, not just a verifier** — it
   contributed 4 GT strings (X₁, X₄, X₅, Y₀) that doc-parse provably cannot emit at
   permitted zoom (X₄/X₅ double-confirmed by crop02+crop14 judges, positions slot-consistent
   with wave-2 pixel adjudication), plus the C₁/C₂ upgrades and all multiplicity
   confirmations (Σ×3, Softmax×3, Transformer Block×3).
3. **The unread 20-cell table row is structurally recovered and explained**: it carries no
   text at all (judge crop04 + register M3 pixel measurement) — the full-frame parse's
   silence on it was an inherent textless-region omission, not a read failure.
4. **Hallucination anatomy**: the full-frame's `1C1/1C2` leading-`1` recurred at crop scale
   (`IC1/IC2/IC3`) and was fixed only by the tightest labels-row crop (`C1 C2 C3` clean);
   the judge confirms the only leading glyph on the frame is a stray "s" — the tail of
   "Output Classes" bleeding into the crop.
5. **Chart-class blocks appear only at crop scale** (ranked_table, pictogram_percentage) —
   structure the full-frame parse never produces.

## Requirement compliance checklist

- [x] Crop EVERY class block the parse returns: the full-frame parse's single
      `class_Picture` block → crop06 (estimated box, `estimated: true`); all supplement
      regions cropped regardless of class.
- [x] Judge rerun per crop: doc-parse re-parse = primary judge (16/16); +13 vision-gateway
      judge legs; every novel string classified REAL / NOT-IN-GT / GT-gap
      (compose/COMPOSED_ANALYSIS.md).
- [x] Position tracking from the first write: manifest.json carries id, class, box (frame
      px), scale, source call dir, transform, level, stop_reason for all 16 crops —
      **zero null boxes**.
- [x] Parallel parse calls in ONE Bash invocation: 3 batches (`&` + `wait`, max 4
      concurrent), wall vs Σ-latency recorded above.
- [x] Recursive until semantic stop: 3 levels, 7 recursion edges, every node with a
      recorded stop reason; caps respected (16 crops, 16/24 calls).
- [x] One composed file: compose/COMPOSED_ANALYSIS.md — all strings deduped, frame
      positions, classifications, provenance call dirs, GT ids, ordered by frame y,
      hallucination + GT-gap sections.
