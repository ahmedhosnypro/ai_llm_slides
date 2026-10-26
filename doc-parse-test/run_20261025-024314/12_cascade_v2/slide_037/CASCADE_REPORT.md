# CASCADE_REPORT — slide_037 (worker-slide_037_cascade_v2, wave 5B)

**Recall trajectory: 79.3% (frozen wave-2, 23/29 GT labels) → 100% (29/29 union).**
7 crops · 7 doc-parse parse calls + 5 vision-gateway judge transcripts · parallel
speedup ~2.5× · all crops carry box + scale + transform + level + stop_reason in
`manifest.json` (verified: no nulls).

## Inputs

- Source frame: `videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg` (960×540)
- Region source (frozen, read-only): `03_parses/slide_037/call01_pass1/slide_037.parse.md` — the 79.3% pass1 read. It returns exactly 2 class blocks: `<class_Section-header>` (title, origin (0.1104,0.1) → close (0.9277,0.168)) and `<class_Picture>` (origin (0.0625,0.1828) → close (0.916,0.9344)) — normalized coords × (960,540) → frame-px boxes (106,54)–(891,91) and (60,99)–(879,505). No origin-only regions; no judge-defect supplement or quadrant fallback needed (≥2 usable regions).
- GT: `04_ground_truth/slide_037/inventory.md` — 29 unique labels; diagram-only slide (no charts/tables/equations); bottom strip y>516 is video-player UI.

## Crop tree (recursion until semantic stop)

```
full-frame pass1 (2 class blocks)
├── crop01_Section-header   level1  parse-driven  box (74.6,52.5)-(922.0,92.2)   scale 1.9646  1664×77
│     └── STOP leaf: single Page-header block spanning the crop; strings = GT-1 + GT-2 exact; no novel content → no judge needed
└── crop02_Picture          level1  parse-driven  box (27.2,82.5)-(912.1,516)    scale 1.8802  1664×816
      └── STOP recursed: mega Picture block (frame (55,83)-(884,516)) with no nested
          coords, yet strings still garbled/merged → split by GT layout regions
      ├── crop03_Picture_insetA   level2  semantic (estimated:true)  box (51.1,194.0)-(227.3,497.2)   scale 3.0  528×909
      │     └── STOP no-new-information: 9 clean GT strings at 3× (GT-3,9,12,11,10,6);
      │           zero new lines vs union (v1 prior-art level3 probe call06 corroborates)
      ├── crop04_Picture_insetB   level2  semantic (estimated:true)  box (278.8,182.1)-(527.6,514.5)  scale 3.0  747×999
      │     └── STOP no-new-information: header + body read clean; only new string is GT-15 'h'
      │           (v1 prior-art call07 corroborates: body-only re-crop adds nothing)
      └── crop05_Picture_arch     level2  semantic (estimated:true)  box (533.4,74.7)-(906.6,516)    scale 3.0  1122×1323
            └── STOP recursed: strings still garbled ('Aad & Norm', 'O'), decoder-top
                cluster under-read → split at the encoder/decoder boundary
            ├── crop06_Picture_encoder  level3  semantic (estimated:true)  box (539.3,74.7)-(752.9,516)  scale 3.0  642×1323
            │     └── STOP no-new-information: zero new GT strings; garbles only
            │         ('October 1 March' hallucination, 'And & Home' → GT-21)
            └── crop07_Picture_decoder  level3  semantic (estimated:true)  box (723.5,74.7)-(899.3,516)  scale 3.0  528×1323
                  └── STOP no-new-information: zero new GT strings; all novel strings are
                      OCR misreads mapped to GT-21/4/5/6 by judge_crop07
```

Recursion ended at semantic stop on every branch: backstop caps were never the reason
(7/16 crops, 7/24 parse calls). Level2/level3 sub-region boxes are `estimated: true`
(semantic subdivisions from GT layout regions + parent-parse garble evidence, since
doc-parse returned whole-crop Picture blocks without nested coordinates — the
requirement's origin-only/estimated provision applied to sub-region seeds).

## Per-crop yield

| Crop | Level | Provenance call dir | Strings read | New GT ids vs pass1 | Judge |
|---|---|---|---|---|---|
| crop01 Section-header | 1 | parses/call_crop01 | 1 block: title + `37` (exact) | 0 (confirms GT-1, GT-2) | not needed |
| crop02 Picture | 1 | parses/call_crop02 | 29 lines | **GT-17, GT-21, GT-26** | judge_crop02 (Create = hallucination) |
| crop03 insetA | 2 | parses/call_crop03 | 9 strings, all clean GT | 0 | not needed |
| crop04 insetB | 2 | parses/call_crop04 | 10 strings | **GT-15 (`h`)** | judge_crop04 (h CONFIRMED) |
| crop05 arch | 2 | parses/call_crop05 | 23 lines | **GT-5, GT-22** (+clean GT-17/20/26) | judge_crop05 (Probabilities printed; O = Q misread) |
| crop06 encoder | 3 | parses/call_crop06 | 10 lines | 0 (garbles only) | judge_crop06 (October 1 March = hallucination) |
| crop07 decoder | 3 | parses/call_crop07 | 19 lines | 0 (garbles only) | judge_crop07 (all 5 garbles mapped to GT) |

Every class block the parse returned was cropped (both level-1 blocks; every nested
block with coordinates was either re-cropped or covered by a semantic child whose
parent block it spans). The doc-parse re-parse of each crop served as the primary
judge; the vision gateway classified each novel string REAL / NOT-IN-GT with crop-px
positions (transcripts banked under `judges/`).

## Parallel speedup

| Batch | Calls (concurrent) | Sum of latencies | Wall clock | Speedup |
|---|---|---|---|---|
| batch1 | crop01+crop02+crop03+crop04 (4) then crop05 (slot freed by `wait -n`) | 7+9+7+9+6 = 38 s | 13 s | 2.9× |
| batch2 | crop06+crop07 (2) | 4+7 = 11 s | 7 s | 1.6× |
| **Overall** | 7 calls in 2 Bash invocations, ≤4 concurrent | **49 s** | **20 s** | **~2.5×** |

(Per-call latencies from the STARTED/FINISHED lines in each call dir's `call.log`;
batch walls from `parses/batch1_timing.log` / `batch2_timing.log`.) Judges ran
sequentially afterward (1 in-flight, ~4.5 min total) per the in-flight cap.

## Stop reasons (all nodes)

leaf ×1 (crop01) · recursed ×2 (crop02 → 3 children; crop05 → 2 children) ·
no-new-information ×4 (crop03, crop04, crop06, crop07) · too-small ×0 · backstop ×0.

## Findings

- Union recall 100%: the 6 labels missing from pass1 (GT-5 Masked Multi-Head Attention,
  GT-15 h, GT-17 Decoder, GT-21 Add & Norm, GT-22 Feed Forward, GT-26 Output Embedding)
  are all recovered by crops 02/04/05.
- 2 hallucination candidates caught by judges and excluded from the union: `Create`
  (C2), `October 1 March` (C6). Zero GT-gaps (nothing printed that the inventory lacks).
- `Probabilities` (GT-19) is read only by the full-frame pass1 among doc-parse calls;
  judge_crop05 confirms it is printed in the arch region too — a stable parser blind
  spot at crop zoom, not a recall loss.
- 12 garble strings (incl. 4 from pass1) are OCR misreads of real GT text; all mapped
  to GT ids in `compose/COMPOSED_ANALYSIS.md` (garble ledger).
- Budgets: crop parses used config-default (no --max-output-tokens); no corroborating
  3000-token re-parse was needed — the vision judges resolved all novel strings. No
  429/5xx encountered (0 retries).

## Tree

```
12_cascade_v2/slide_037/
├── manifest.json                     (7 crops: id, class, box, scale, transform, level,
│                                      precheck, provenance, estimated, source_call_dir,
│                                      stop_reason, parse_result, judge, totals)
├── crops/crop01..crop07/crop.png     (7 pre-checked PNGs)
├── parses/call_crop01..07/           (5-file call dirs: call.log[+EXIT], stdout.log,
│                                      stderr.log, crop.parse.* + slide_037.parse.*)
├── parses/batch{1,2}_timing.log
├── judges/probe.log, judge_crop02/04/05/06/07.md (+ .call.log, .stderr.log)
├── compose/COMPOSED_ANALYSIS.md
└── CASCADE_REPORT.md
```

Wave-5 v1 tree (`11_cascade/slide_037/`) was read as prior art only (their call03–09
evidence corroborates two stop decisions); all crops/parses/judges here were produced
fresh by this worker.
