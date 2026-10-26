# VJ improvement report — slide_057 (doc-parse wave-4)

Scope `slide_057_vj` · worker `worker-slide_057_vj` · 2026-10-25 · run `doc-parse-test/run_20261025-024314`
Source frame: `videos/deep-learning/002_transformers_part2/unique_slides/slide_057.jpg` (960×540, md5 `d785db85444cb3377818caafc05f80a8`).

## Headline

**Union text recall 12.5% → 46.9% (+34.4 pp)** over 3 improvement rounds and 12 crop-parse calls, with **every one of the 12 crop calls finishing `stop`** — the full-frame `Decoder` repetition loop (`finish=length`, 6/6 full-frame calls incl. both 9000-token wave-3 calls) **does not survive region-targeted input**. Efficiency: 17 new GT strings from 12 crop calls (1.42 strings/call; 1.29 recall-weighted/call), 110 s total crop-parse latency (avg 9.2 s/call) vs the full-frame calls' 88.7 s avg for 12.5%.

Honesty note (per addendum): doc-parse's prompt was never editable (wire contract carries `decoding` only). Every gain came from **input-form engineering** (judged-defect-targeted PIL crops, LANCZOS 3×, ≤1664×2048) + **judge-driven targeting** (visual-judge rounds deciding where to crop).

## Recall trajectory

| stage | union recall (48-string GT) | detail |
|---|---|---|
| wave-2 frozen baseline (4 full-frame calls) | 12.5% (6/48: 5 EXACT + 1 NORM) | all finish=length, `Decoder` ×482/×1470 |
| wave-3 t9k pair (2 more full-frame, 9000 tok) | 12.5% (unchanged) | same 6-unique-line loop, ×4477 bare-`Decoder` lines (4490-line file) — loop is budget-independent |
| round 1 (+4 crops: encoder bars/Y-chips, embedding/X+word, decoder top, decoder bottom) | 28.1% (13.5/48) | +8 strings: Encoder Block M/1/0, Word Embedding, Positional Encoding/Embedding, Attention, Word and Position Encoding, Encoder Decoder Attention (PARTIAL 0.5) |
| round 2 (+4 crops: Y-row strip, X+word strip, token strip, K/V column) | 46.9% (22.5/48) | +9 strings: Y_0..Y_5, Y_{N-1} (7 NORM), K, V (EXACT) |
| round 3 (+4 crops: X+word strip w/o title, tight tokens, big-Q, Y_{N-2} chip) | 46.9% (unchanged) | +0 — STOP condition (round added <2; also 3-round cap) |

Final composition: **14 EXACT + 8 NORMALIZED + 1 PARTIAL (0.5)** = 22.5/48 = 46.9%.

## Does crop parsing escape the repetition loop? YES — measured

- Full-frame: 6/6 calls `finish_reason=length`, 6 unique lines then bare `Decoder` ×482 (1024 tok) / ×1470 (3000 tok) / ×4489 (9000 tok). Deterministic; byte-identical pass-2 pairs.
- Crops: 12/12 calls `finish_reason=stop`, output_tokens 6–92, latencies 2.9–24.6 s. Zero loop events; zero invented content (misreads only: "RELL"→RELU corrected in crops, "Wired"≈"Word", "Encode"≈"Encoder", "Yo"≈Y_0, "YsN"/"YN"≈Y_{N-2}).
- The loop is therefore a **full-frame phenomenon** of this parser+model on this slide, not a budget or prompt-surface problem — the single most actionable finding of this wave.

## What worked / what didn't (crop-scale law observed on this parser)

- Worked: mid-size panel crops with readable anchor text (encoder bars table, embedding box, decoder bar stack, K/V column ~115×165 px source); single-row strips ~46 px tall with box structure (Y-chip row → 7/8 chips).
- Failed: anchor-less strips (X+word row without the embedding title → empty `<class_Picture>` + corner coords, 6 tokens; tight token strip → same; 50×50 big-Q badge → same) — the parser needs in-crop anchors; with an anchor present it may latch onto it and drop the target rows (crop06: chart scaffold around the embedding title, "Wired N" rows).
- Below source legibility (parked, never dropped; judge + wave-2 ink-map agreement): "Softmax" (~25×5 px blob), lavender "Multi-Head / Self-Attention" 2-line (~4–5 px ink), tiny mid-column Q's. Upscaling cannot recover unrendered information.
- Coordinates: corner artifacts on every crop (x_0/y_0 ↔ x_0.999/y_0.999) — crop parsing buys TEXT, not geometry; region targeting does not fix the coordinate head.

## Remaining misses (25.5 weighted / 48) — parked with labels

- X-chips ×8, word row ×8 — anchor-dependence (empty or scaffold outputs; "Wired" near-miss below the ≥60% PARTIAL threshold)
- bottom tokens ×5 (SOS/Je/ne/suis/faisait) — sub-5px glyphs, skipped in all 3 attempts
- Y_{N-2} ×1 — garbled 3× ("YsN", "YN"); `Y_{N-1}` corroborated twice ("Yn1", "YN.I")
- Q ×1 — big-Q badge (judge: legible) returned an empty shell; tiny Q's below legibility
- Softmax ×1, Multi-Head Self-Attention ×1 — below source legibility
- `Encoder Decoder Attention` counted at 0.5 (PARTIAL: "Encode" truncation, corroborated 9× across crop03/crop04)

## Judge efficiency

- 2 judged rounds (gateway Tier-2 legs, route `images`, analysis mode): round 1 (2 attempts — one `Response ended prematurely`, paced retry after 60 s + re-probe) + round 2. Round 3's judge step reused round-2's per-region assessment (the judge had already answered, per region, whether tighter crops would recover the text); the 4 round-3 crops were the direct test — deviation banked here.
- Probe discipline held: 2 probes (legend crop), both <4 s. All judge legs ended in coherent bodies with terminal `FINAL VERDICT: FAIL for 'parse captures the slide's renderable text'` lines.
- Tier-1 disclosure: this subagent's model lacks image input (`missing image_in`); per the fallback ladder the visual reads ran on the Tier-2 host gateway (`image-analysis/analyze_image.py`, default route) + banked wave-2 pixel measurement; nothing was faked at Tier 1.

## Artifacts (all under `$RUN/10_visual_judge/slide_057/`)

- `judge/round1_prompt.txt` (frozen vj-r1), `round1_gateway_transcript.txt`, `round1_transcript.md`; `round2_prompt.txt` (vj-r2), `round2_gateway_transcript.txt`, `round2_transcript.md`; `probe*_transcript.txt`
- `crops/round1/` (crop00_probe_legend, crop01–04), `crops/round2/` (crop05–08), `crops/round3/` (crop09–12) — 13 PNGs, pre-checked (dims + nonzero mean)
- `parses/call01_round1 … call12_round3/` — 12 call dirs, 5-file convention, all EXIT=0 finish=stop
- `ledger.md` — 3 append-only rows
