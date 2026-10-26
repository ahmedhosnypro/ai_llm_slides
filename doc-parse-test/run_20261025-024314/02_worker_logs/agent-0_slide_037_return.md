

Wave-1 deliverables for slide_037 are complete and the scope is closed in the DB.

## What I did

**1. Setup & dependency handling**
- Read `MISSION_PROTOCOL.md` in full, then the binding AGENTS chain (project root, `videos/deep-learning/`, lecture 002). Claimed `slide_037` as `worker-slide_037` **before any work**.
- The build's parent is the cross-video component chain `37 ← 001:19 → 001:18 → 001:17 → shared house_chrome`; followed it read-only and froze all 5 build files + the analysis JSON into `04_ground_truth/slide_037/` (md5s recorded in `inventory.md`).

**2. Two doc-parse calls** (`03_parses/slide_037/`, five files each, all commands logged to `02_worker_logs/slide_037_commands.log`):

| Call | EXIT | finish | out_tokens | content | latency | stderr |
|---|---|---|---|---|---|---|
| `call01_pass1` (1024) | 0 | stop | 133 | 535 ch | 51.8 s | 0 |
| `call02_pass2` (3000) | 0 | stop | 27 | 166 ch | 128.3 s | 0 |

Pass1 extracted title+badge plus a 27-line text blob of diagram labels; pass2 (more tokens, less output) collapsed to title+badge and ONE `class_Picture` covering everything — zero diagram text. Notable pass1 output: reading is noisy (4 hallucination candidates: `Scalar Dot-Product Attention`, `Mult-Head Attention`, `Math-Head Attention`, `Max`), blob anchored at (60, 99) — empty panel, 128 px from the nearest real text; `Add & Norm`, `Feed Forward`, `Output Embedding`, `Decoder`, `h`, `Masked Multi-Head Attention` entirely missing.

**3. GT inventory** — built by executing the frozen build under a stubbed-pptxgenjs recorder (`_sim/`, `writeFile` no-op; the real deliverable pptx's mtime is verified unchanged): **29 unique GT labels** (54 visible instances), **202 shapes + 66 text boxes**, 7 analysis regions, **75 palette hexes**, Arial only (6.5–35.5 pt), no equations/charts/tables, plus z-order/occlusion facts (one `Add & Norm` sits under the red disc; 017-chain strings hidden under repaint patches).

**4. Comparison** (`05_comparison/slide_037_comparison.md`, four measured sections):
- Text fidelity: pass1 = **22 EXACT + 1 NORMALIZED (`N x`→`Nx`) + 0 PARTIAL + 6 MISSING → recall 79.3%**; pass2 = 2/29 = 6.9%.
- Layout: pass1 4 anchors — 3/4 within ~80 px of nearest GT content element (blob fails); `Section-header` misanchored at the badge; pass2's one Picture box under-segments 3 diagram regions and over-extends 162 px left / 61 px above the true frame.
- Structure: diagrams demoted to `Picture`; no equations or chart/table classes (GT has none — correct); catalogued what the parse cannot carry (colors, px geometry, fonts, z-order/occlusion, dashes, 342° pin rotation).
- Reliability: avg latency 90.05 s, avg out tokens 80, **corroboration Jaccard 2/23 = 0.087** — title/badge is the only byte-identical overlap; 21 GT strings + all 4 hallucination candidates are single-read.
- **11 claims for image adjudication** at the end of the file (hallucination candidates, the 6 missing labels, blob-anchor/reading-order anomalies, mega-Picture bounds, badge-vs-Section-header, title placement, progress-bar exclusion, disc-occlusion leniency).

## DB state
`slide_037 | done | worker-slide_037`, milestone event id 9 recorded, one-line note: *"Wave-1 done: 2 parse calls banked (both stop/EXIT0), GT inventory + frozen copies, comparison (text_recall 79.3%, corroboration Jaccard 0.087) + 11 adjudication claims; wave-2 register/scores pending vision verdicts."* **Zero open tasks** — no blockers (no 401/429/DB-lock events, no retries needed). Per the prompt I did **not** start the wave-2 `07_registers/` + `08_final/scores` items; those await the vision verdicts.