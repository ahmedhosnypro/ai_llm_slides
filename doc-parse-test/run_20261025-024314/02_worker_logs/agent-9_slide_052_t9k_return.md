# agent-9 wave-3 return — slide_052_t9k (banked verbatim from task agent-oq4ywtru, 2026-10-25)

All deliverables verified. Task complete — final hand-off:

## slide_052_t9k — DONE (DB status `done`, both items `parse_t9k,delta_vs_passes` closed)

**Headline: 9000-token retry changes nothing for slide_052.** The t9k output is **byte-identical to both wave-2 passes** (md5 `bdb0e649c4ba8572201ff35d90e80950` across call01_pass1@1024, call02_pass2@3000, call05_t9k@9000 — a three-way byte identity). Transcript-level recall stays **75.0%** (16 EXACT + 0.5 PARTIAL of 22 GT units; frozen wave-2 = 75.0%, Δ = 0.0 pp).

**Call record** (`03_parses/slide_052/call05_t9k/`): EXIT 0, finish_reason `stop`, 145 output tokens, 645 chars, 31 lines / 20 unique, latency 4.2 s (uncontended endpoint vs 16.7/52.2 s in wave 2), stderr 0 lines. Valid on first attempt → no `call06_t9k_retry` (addendum reserves it for failed calls only). The 9000-token ceiling was never approached — the model stops itself at 145 tokens at every budget level, proving the output budget was never the binding constraint.

**Every wave-2 finding reproduces exactly at t9k** (re-verified by direct greps, not assumed from the md5): `K`, `V`, `Y`×3, the `SOS = Start Of Sentence` legend, and badge numeral `52` all still dropped; `Q` still 2 of 5; the 5×3 stacked box labels still shredded (`Encode Decoder` merged line + `Encoder`×3/`Decoder`×2/`Attention`×3 fragments); `I feel Sick` still merged; FFN double-space still collapsed; still exactly one trailing `<class_Picture>` region and no structure tokens; the wave-2-adjudicated `Encoder`×3 hallucination (original reads `Encode`, no "r") still present ×3. New strings: none (REAL-GT ∅, NOT-IN-GT ∅); lost strings: none. The J=1.00 corroboration now demonstrably measures deterministic repetition of the parser's systematic blind spots, not independent confirmations.

**Files written** (all under `$RUN`, nothing else touched; frozen wave-2 artifacts untouched):
- `03_parses/slide_052/call05_t9k/` — the five call files
- `05_comparison/slide_052_t9k_delta.md` — 4 addendum sections (call record / delta / recall estimate marked transcript-level / verdict)
- `02_worker_logs/slide_052_commands.log` — 5 appended entries (claim, launch, call result, verification greps, report write)

**DB**: `scope-claim` → `scope-done` with note "finish=stop (EXIT 0), t9k recall 75.0% (frozen wave-2 75.0%, delta 0.0pp); t9k output byte-identical to both 1024/3000 passes (md5 bdb0e649...), no new/lost strings — 9000 changes nothing". Row verified: status `done`, no open tasks. No blockers; no `.doc-parse-config` access; no image ever read; no git/deletes.
