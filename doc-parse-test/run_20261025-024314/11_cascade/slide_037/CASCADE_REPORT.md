# CASCADE_REPORT — slide_037 (worker-slide_037_cascade, wave 5 v1)

**Recall trajectory: 79.3% (frozen wave-2, 23/29 GT labels) → 100% (29/29 union).**
8 crops · 9 doc-parse crop-parse call dirs (all EXIT 0; 8 primary + 1 corroborating
3000-token re-parse) · 0 new full-frame calls (the wave-2 pass1 transcript is the
region seed) · 1 vision probe + 6 judge transcripts (J2 banked by the prior worker,
J5/J4/J6/J7/J8 produced this session, all EXIT 0) · parallel parse speedup ~1.7×
(114 s serial vs 67 s batched) · every crop carries box + scale + transform + level +
stop_reason + judge in `manifest.json` (verified: no nulls).

## Inputs

- Source frame: `videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg` (960×540)
- Region seed (frozen, read-only): `03_parses/slide_037/call01_pass1/slide_037.parse.md`
  — 2 class blocks: `<class_Section-header>` (106,54)–(891,91) and mega `<class_Picture>`
  (60,99)–(879,505). No origin-only regions; no judge-defect/quadrant fallback needed.
- GT: `04_ground_truth/slide_037/inventory.md` — 29 unique labels; diagram-only slide;
  bottom strip y>516 is video-player UI (excluded from all crops by design).
- Wave-2 frozen recall 79.3% — NOT recomputed (per protocol).

## Crop tree (recursion until semantic stop)

```
full-frame pass1 (2 class blocks)
├── crop01_Section-header  level1 parse-driven  box (75,53)-(922,92)    scale 1.9646 1664×77
│     └── STOP leaf: single Page-header block; strings = GT-1 '37' + GT-2 title, exact;
│           no novel content → no judge needed
└── crop02_Picture         level1 parse-driven  box (27,83)-(912,516)  scale 1.8802 1664×814
      └── STOP no-internal-structure at level1: mega Picture block covering the whole crop
          again (self-referential), yet zoom added novel strings → split into 3 semantic
          children per judges/crop02_judge.md box correction
      ├── crop03_Picture_insetA   level2  box (51,194)-(228,497)   scale 3.0  531×909
      │     └── STOP recursed (body child block of call03) → crop06
      ├── crop04_Picture_insetB   level2  box (279,182)-(527,514) scale 3.0  744×996
      │     └── STOP recursed (body child block of call04) → crop07
      └── crop05_Picture_arch     level2  box (533,75)-(907,516)  scale 3.0  1122×1323
            └── STOP recursed (child block of call05) → crop08; corroborating re-parse
                call09 (--max-output-tokens 3000) itself stopped no-new-information
                (string-identical to call05)
            ├── crop06_Picture_insetA_body  level3  box (71,250)-(234,487)  scale 3.0  489×711
            │     └── STOP no-new-information: single whole-crop Picture block; every string
            │         already in the union ('Attention' = GT-3 header fragment); no nested coords
            ├── crop07_Picture_insetB_body  level3  box (269,226)-(537,507) scale 3.0  804×843
            │     └── STOP no-new-information: only delta vs parent call04 is garble '9' vs 'Q'
            └── crop08_Picture_arch_body    level3  box (518,57)-(917,516) scale 3.0 1197×1377
                  └── STOP no-new-information: deliberate ~whole-parent probe; only adds garbles
                      ('Multi-lead Attention', 'Fixed Forward') + title fragment already read
```

Recursion ended at semantic stop on every branch: backstop caps were never the reason
(8/16 crops, 9/24 parse calls). Level-2/3 boxes are judge/analysis-anchored semantic
subdivisions (doc-parse returned whole-crop Picture blocks without nested coordinates).

## Per-crop yield

| Crop | Level | Provenance call dir | Strings read | New GT ids vs pass1 | Judge verdict |
|---|---|---|---|---|---|
| crop01 Section-header | 1 | parses/call01_crop01 | 1 block: title + `37` (exact) | 0 (confirms GT-1, GT-2) | not needed (no novel strings) |
| crop02 Picture | 1 | parses/call02_crop02 | 24 lines | **GT-17, GT-21** | J2 (banked): `Output Decoder` = two labels; `Read Forward`/`Ad & Norm` = REAL misreads (GT-22/GT-21); `M Multi-Head Attention` = header + M artifact; `V K Q` = 3 separate circles |
| crop03 Picture_insetA | 2 | parses/call03_crop03 | 9 strings, all exact GT | 0 | not needed (no novel strings) |
| crop04 Picture_insetB | 2 | parses/call04_crop04 | 10 strings | **GT-15 (`h`)** | J4: all 8 strings CONFIRMED (h = brace label, crop-px (643,524)–(665,556)); Linear ×4; missed: none |
| crop05 Picture_arch | 2 | parses/call05_crop05 (+call09 corroborate) | 23 lines | **GT-5, GT-22, GT-26** (+clean GT-17/21) | J5 (attempt 2; attempt 1 killed by session exit): `Aad & Norm`→Add & Norm, `O`→Q, `We ARE HERE` casing slip; missed = duplicates + `Probabilities` (printed — doc-parse blind spot at zoom, no recall loss) |
| crop06 Picture_insetA_body | 3 | parses/call06_crop06 | 9 lines | 0 (`Attention` = GT-3 fragment) | J6: all 9 CONFIRMED; `Attention` = lower 60% of the clipped bold-italic red header; missed: none |
| crop07 Picture_insetB_body | 3 | parses/call07_crop07 | 9 lines | 0 (garble `9`) | J7: 8 of 9 CONFIRMED; `9` = NOT visible as 9, misread of the bottom-right Q circle; `h` 2nd confirmation; missed: 1 duplicate Linear box |
| crop08 Picture_arch_body | 3 | parses/call08_crop08 | 2 blocks, 24 lines | 0 (confirms GT-1/17/21/22/5) | J8: `ked over Multi-Head)` CONFIRMED (clipped title banner); `Multi-lead Attention`→Multi-Head Attention, `Fixed Forward`→Feed Forward; missed = duplicate labels only (Add & Norm ×5, V/K/Q ×3, Nx ×2) |

## Parallel speedup (parse calls, from call.log STARTED/FINISHED timestamps)

| Batch | Calls (concurrent) | Sum of latencies | Wall clock | Speedup |
|---|---|---|---|---|
| batch1 | call01+call02 (crop01, crop02) | 7+23 = 30 s | 23 s (08:28:11→08:28:34) | 1.3× |
| batch2 | call03+call04+call05 (3 level-2 crops) | 5+15+21 = 41 s | 21 s (08:36:31→08:36:52) | 2.0× |
| batch3 | call06+call07+call08 (3 level-3 crops) | 11+9+18 = 38 s | 18 s (08:42:13→08:42:31) | 2.1× |
| solo | call09 (corroboration re-parse) | 5 s | 5 s | 1.0× |
| **Overall** | 9 calls in ≤4-concurrent batches | **114 s** | **67 s** | **~1.7×** |

Judges ran strictly sequentially (1 in flight at a time, per the Tier-2 cap): probe 15 s
(banked, EXIT 0 PROBE-OK) · J2 422 s (banked) · J5 attempt 1 killed by the prior
worker's session exit (no FINISHED/EXIT) · J5 attempt 2 144 s · J4 72 s · J6 49 s ·
J7 116 s · J8 191 s — 572 s for the 5 judges this session.

## Stop reasons (all nodes, from manifest.json recursion[])

leaf ×1 (crop01) · no-internal-structure ×1 (crop02, then recursed via judge-corrected
semantic split) · recursed ×3 (crop03→crop06, crop04→crop07, crop05→crop08) ·
no-new-information ×3 (crop06, crop07, crop08) · too-small ×0 · backstop ×0.

## Findings

- Union recall 100%: the 6 labels missing from pass1 (GT-5 Masked Multi-Head Attention,
  GT-15 h, GT-17 Decoder, GT-21 Add & Norm, GT-22 Feed Forward, GT-26 Output Embedding)
  are recovered by C2 (GT-17, GT-21), C4 (GT-15), C5 (GT-5, GT-22, GT-26; call09
  corroborates GT-26 at the 3000-token budget). C8 independently confirms GT-1/17/21/22/5.
- 0 hallucination candidates survived judging: every novel parsed string mapped to a
  real GT label (OCR misread, label merge, or segmentation artifact). The v2 prior-art
  run caught 2 hallucinations (`Create`, `October 1 March`) on different crop boundaries;
  the v1 crop set never produced them.
- 0 GT-gaps: judges found no printed string the inventory lacks (J5/J8 "missed text"
  lists are duplicate instances of known labels, plus the `Probabilities` crop-zoom
  blind spot — GT-19 is covered by P1/C2/C8).
- 16 garble strings across P1 + crops are all mapped to GT ids in
  `compose/COMPOSED_ANALYSIS.md` (garble ledger).
- Budgets: crop parses used config-default (no --max-output-tokens) except the call09
  corroboration (3000). No HTTP 429/5xx, 0 retries. No new crops (8/16 cap), no new
  full-frame calls.

## Tree

```
11_cascade/slide_037/
├── manifest.json                     (8 crops: id, class, box, scale, transform, level,
│                                      precheck, provenance, estimated, source_call_dir,
│                                      parse_result, stop_reason, judge + recursion[])
├── crops/crop01..crop08/crop.png     (8 pre-checked PNGs)
├── parses/call01..call09/            (5-file call dirs: call.log[+EXIT], stdout.log,
│                                      stderr.log, crop.parse.md, crop.parse.json)
├── judges/probe_*, crop02_judge.* (banked), crop04/05/06/07/08_judge.*
│                                      (.md + _call.log[COMMAND/PROMPT/STARTED/FINISHED/EXIT] + _stderr.log)
├── compose/COMPOSED_ANALYSIS.md
└── CASCADE_REPORT.md
```

Blockers: none. All 9 parse call dirs record EXIT 0; all 7 vision-gateway runs record
EXIT 0; every crop has box/scale/transform/stop_reason/judge in manifest.json (no nulls);
nothing deleted; writes confined to `11_cascade/slide_037/` +
`02_worker_logs/slide_037_cascade_v1_commands.log`.
