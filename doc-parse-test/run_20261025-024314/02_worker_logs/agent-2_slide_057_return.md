

Wave-1 for slide_057 is complete. Final report:

## What I did

1. **DB claim** — `pool-db.sh scope-claim` as `worker-slide_057` (verified: `slide_057 | in_work | worker-slide_057`).
2. **Ground truth** — read the binding rules (project/course/lecture AGENTS.md), then the full require() chain: `build/slide_057.js` → `slide_049.js` → `components/slide_026.js` + `components/slide_047.js` (SUBS law) + `shared_patterns/house_chrome.js`. Froze all 6 files to `04_ground_truth/slide_057/` + wrote `inventory.md` (48 build-GT strings + 8 analysis-only divergent strings; 6 layout regions; 113 helper-call sites ≈ 820 primitives; ~60 palette hexes; Arial + Times New Roman; no charts/tables/equations).
3. **doc-parse calls** — per-call dirs, all commands logged to `02_worker_logs/slide_057_commands.log` (13 lines), Bash timeout 240–420s for every parse.

## Key numbers

**The parse endpoint failed on this slide — deterministically.** All 4 calls ended `finish_reason=length` inside a `"Decoder"` repetition loop:

| call | budget | out_tokens | chars | latency | loop |
|---|---|---|---|---|---|
| call01_pass1 | 1024 | 1024 | 4123 | 64.0s | `Decoder` ×482 |
| call02_pass2 | 3000 | 3000 | 12027 | 109.0s | `Decoder` ×1470 |
| call03_retry_pass1 (retry) | 1024 | 1024 | 4123 | 66.4s | ×482 |
| call04_retry_pass2 (retry) | 3000 | 3000 | 12027 | 115.3s | ×1470 |

Only **6 unique lines** survive in every transcript: `57`, `Encoder`, `Decoder`, `Encoder Block 2`, `Feed Forward Networks / One Hidden with RELL Activation`, `Residual Connection and Layer Normalization`. Pass2's two transcripts are byte-identical to each other; the failure is budget-independent, so per protocol these are FAILED CALLs kept as evidence with fresh-dir retries.

**Measured fidelity** (identical across all calls): EXACT 5, NORMALIZED 1 (RELU→RELL / `-`→`/`), PARTIAL 0, MISSING 42 → **text_recall = 12.5%** (6/48 build-GT). Layout: 1 positioned item total (`57` at 56.3,42.6px ≈ **837px from the badge's true center** — mis-anchored, 0/1 within tolerance); 0 class tokens; build ≈820 primitives/6 regions vs parse 1 item. Hallucination candidates: none (repetition, not invention). Reliability: 0/4 finish=stop, Jaccard of detected sets 1.000 (degenerately corroborated). Comparison file ends with 10 image-adjudication claims (build-vs-analysis wording divergences included: `Word and Position Encoding`/`Embedding`, `Multi-Head Self-Attention`/`Masked Multi-Headed Attention`, last-chip `N-1` vs `N`).

## DB state

- `slide_057 | done` (worker-slide_057), task-added blocker: `parse_loop_finish_length` (finish!=stop ×4 → wave-2 `finish_all_stop=0` must be scored against the truncated transcripts).
- Wave-2 (`07_registers`, `08_final`) untouched, awaiting vision verdicts as instructed.

**Caveat for the parent:** done-criteria item 1 (EXIT=0 + finish stop in the two named dirs) could not be met — the endpoint deterministically truncates on this image at both protocol-fixed budgets; the blocker task records this. Whether any of that needs a driver change (e.g. a dedicated prompt/budget for the densest slides) is outside my scope.