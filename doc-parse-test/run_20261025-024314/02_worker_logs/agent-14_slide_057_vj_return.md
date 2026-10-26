**Scope `slide_057_vj` complete — closed via `scope-done`: recall 12.5% → 46.9% over 3 rounds, 12 crop calls.**

## Headline

Union text recall against the 48-string GT inventory rose **12.5% → 46.9% (+34.4 pp)**, and the central wave-4 question is answered decisively: **region-targeted crop parsing escapes the full-frame `Decoder` repetition loop** — all 12 crop calls finished `finish_reason=stop` (output 6–92 tokens, avg 9.2 s) vs 6/6 full-frame calls dying in `finish=length` (including both 9000-token wave-3 calls, which looped ×4477). The loop is a full-frame phenomenon, not a budget problem. Final composition: 14 EXACT + 8 NORMALIZED + 1 PARTIAL (0.5) = 22.5/48; 17 new GT strings from 12 crop calls (1.42 strings/call, 110 s total latency).

## What was done

- Read protocol + visual-judge doctrine + wave-2 register/scores + all 6 full-frame transcripts. Wave-3's `call05_t9k`/`call06_t9k_retry` exist and prove the loop is budget-independent.
- **Tier-1 constraint:** this subagent's model lacks image input (`missing image_in`) — per the visual-judge fallback ladder I ran the visual reads on the **Tier-2 host gateway** (`image-analysis/analyze_image.py`, default `images` route), probe-first, paced, transcripts banked. Disclosed in every banked record.
- **3 rounds** (2 full judge rounds + round 3 whose judge step reused round-2's per-region assessment — deviation disclosed): round 1 (+8 strings: encoder bars M/1/0, embedding box, Attention, Word and Position Encoding, Encoder Decoder Attention PARTIAL), round 2 (+9: Y_0..Y_5, Y_{N-1}, K, V), round 3 (+0 → stop condition).
- Observed **crop-scale law**: mid-size anchored crops and ~46 px row-strips read tiny text; anchor-less strips and single-glyph crops return empty `<class_Picture>` shells with corner coordinates (crop parsing buys text, not geometry). Parked as below-source-legibility (never dropped): Softmax blob, lavender Multi-Head/Self-Attention 2-line text, tiny Q's.

## Artifacts (all under `$RUN/10_visual_judge/slide_057/`)

`judge/round{1,2}_prompt.txt` + gateway transcripts + synthesized `round{1,2}_transcript.md` (defect lists, terminal `FINAL VERDICT: FAIL` lines) · `crops/round1..3/` (13 pre-checked PNGs) · `parses/call01_round1…call12_round3/` (12 dirs × 5 files, all EXIT=0 finish=stop) · `ledger.md` (3 rows) · `VJ_IMPROVEMENT_REPORT.md`. Commands logged to `02_worker_logs/slide_057_commands.log`; nothing written outside `$RUN`; frozen wave-2/3 artifacts untouched; one numeric correction applied post-bank (t9k loop = 4477 bare `Decoder` lines).

## Follow-up candidates for the orchestrator

The remaining 25.5 weighted strings (X-chips ×8, word row ×8, bottom tokens ×5, Y_{N-2}, Q, Softmax, Multi-Head Self-Attention) are blocked by parser anchor-dependence and sub-5px ink, not by crop targeting — a possible wave-5 lever is supplying synthetic anchor context alongside crops, which the current write-frozen parse script cannot do.