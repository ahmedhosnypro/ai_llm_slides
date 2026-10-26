**MISSION COMPLETE — slide_037_cascade_v2 · `scope-done` EXECUTED and confirmed in DB (`slide_037_cascade_v2 | done`).**

**Headline: recall 79.3% → 100% (29/29 GT labels), 7 crops, speedup ~2.5×**

**What was done (recovery → close, all in-tree):**

- **Region extraction**: pass1 parse yields exactly 2 class blocks with origin+close coords — `Section-header` (106,54)–(891,91) and `Picture` (60,99)–(879,505). Both cropped (requirement 1); no origin-only regions, no fallback needed.
- **Crop tree / recursion until semantic stop**: crop01 Section-header (leaf) + crop02 Picture (recursed → level2 insets crop03 insetA / crop04 insetB / crop05 arch from GT layout regions, `estimated: true`) → crop05 recursed → level3 crop06 encoder / crop07 decoder. Stops: leaf ×1, recursed ×2, no-new-information ×4; backstop never approached (7/16 crops, 7/24 parse calls).
- **Position tracking**: `manifest.json` has all 7 crops with id, class, frame-px box, scale, transform, level, stop_reason, provenance, source call dir — programmatic check: PASS, zero nulls.
- **Parallel calls**: 7 doc-parse parses in 2 Bash invocations, `&`+`wait`/`wait -n`, max 4 concurrent; latency sum 49 s vs wall 20 s → **~2.5×** (batch1 38→13 s = 2.9×; batch2 11→7 s). All EXIT 0, no retries needed.
- **Judges**: doc-parse crop re-parse = primary for all 7; 5 vision-gateway transcripts banked for the novel-string crops. Verdicts: 2 hallucinations caught (`Create`, `October 1 March` — excluded from union); 12 garble strings all mapped to real GT ids; `h`, `Add & Norm`, `Feed Forward`, `Masked MHA`, `Decoder`, `Output Embedding` recoveries confirmed.
- **Union recall 100%**: the 6 labels missing from pass1 (GT-5, 15, 17, 21, 22, 26) all recovered by crops 02/04/05. Zero GT-gaps.
- **Composed**: `compose/COMPOSED_ANALYSIS.md` — 27 merged element rows ordered by frame y with classification, GT id, provenance, plus hallucination / GT-gap / garble-ledger sections.

**Deliverables**: `12_cascade_v2/slide_037/{manifest.json, crops/ (7), parses/ (7 call dirs + 2 timing logs), judges/ (probe + 5 transcripts), compose/COMPOSED_ANALYSIS.md, CASCADE_REPORT.md}`. Command log appended throughout at `02_worker_logs/slide_037_cascade_v2_commands.log`. Nothing written outside my tree + logs; wave-5 v1 tree used read-only as prior art only.