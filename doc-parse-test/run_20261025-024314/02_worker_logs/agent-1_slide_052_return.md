## Wave-1 report — slide_052 (doc-parse accuracy audit)

**DB state:** `slide_052` = **done**, agent `worker-slide_052`, note logged; 0 open tasks/blockers. Other scopes untouched (`slide_037/057/059` still in_work by their workers).

**Deliverables (all under `doc-parse-test/run_20261025-024314/`):**
- `03_parses/slide_052/call01_pass1/` + `call02_pass2/` — both EXIT=0, finish=stop, 145 out tokens, 645 content chars, 0 stderr lines; each dir has the five per-call files. Latency 16.7 s / 52.2 s (spread = shared-endpoint contention, not content).
- `04_ground_truth/slide_052/` — frozen `slide_052.js` + required `house_chrome.js` + `slide_052_final.json` (md5-verified) + `inventory.md` (22 dedup GT units, 9 regions, palette/fonts, quantitative diagram data).
- `05_comparison/slide_052_comparison.md` — four measured sections + 11 claims.
- `02_worker_logs/slide_052_commands.log` — 8 logged commands.

**Key numbers:**
- **text_recall = 75.0%** (16 EXACT + 0 NORMALIZED + 0.5×1 PARTIAL) / 22 GT. Missing: `SOS = Start Of Sentence` legend, `K`, `V`, `Y` (×3 tags), `52` badge. PARTIAL: `Encode Decoder Attention` (5 stacked 3-line box labels shredded into 9 fragment lines).
- **Passes byte-identical** (same md5) → corroboration Jaccard **1.00**, zero single-read strings; raising 1024→3000 tokens changed nothing — lossiness is model reading behavior, not budget truncation.
- **Layout: 2 positioned items vs 256 build elements (0.8%)** — census from an instrumented run of the frozen builder with a recording stub (218 shapes: 137 rect/82 line/15 triangle/8 ellipse + 38 texts; run under `$RUN`, repo namespace verified untouched). Matchable pair 1/2 at 35.6 px from GT; one trailing `<class_Picture>` at frame (906.5, 517.6) matching nothing.
- **Structure: exactly 1 class token** (`class_Picture`); no section/list/table/chart/equation classes; count fidelity lost across the board (Q 5→2, input words 3 boxes→1 line).
- **1 hallucination candidate**: standalone `Encoder` ×3 — suspected mis-OCR of the boxes' verbatim `Encode` (no "r", per certified analysis); awaiting Phase 3, not yet labeled.

**Wave-2 not started** (register/scores await vision verdicts, per instructions). One protocol-judgment call for the record: I interpreted the protocol's EXACT rule ("case/whitespace-insensitive equality") as token-boundary matching after stripping format tokens — required here because single-letter GT strings (`K`, `V`, `Y`, `I`) otherwise falsely match inside words; the rule and both matching sides are documented in the comparison file.