# agent-11 wave-3 return — slide_059_t9k (banked verbatim from task agent-nhz0j8y7, 2026-10-25)

Scope `slide_059_t9k` is complete and closed in the DB. Summary of the run:

## What was done

1. **Claimed** `slide_059_t9k` as `worker-slide_059_t9k` (mission.db → now `done` with the headline note recorded).
2. **Parse call** `03_parses/slide_059/call05_t9k/` (all 5 files): `--max-output-tokens 9000 --timeout 300` → EXIT=0, `finish_reason=stop`, **119 output tokens, 424 chars, 10.6 s**, 0 stderr lines. Call succeeded first attempt, so `call06_t9k_retry` was not needed (no retry spent).
3. **Byte-identity check**: the t9k transcript is **byte-identical** to both wave-2 passes — md5 `da4b6ab6fdd36c2400ca429b750d7fe1` across call01_pass1 / call02_pass2 / call05_t9k, empty diffs both ways. This is now a *triple* identical read at 1024 / 3000 / 9000 budgets.
4. **Delta report** written: `05_comparison/slide_059_t9k_delta.md` with all 4 required sections.

## Key findings (answers to the prompt's checks at t9k)

- **NEW strings**: none (0 REAL-GT, 0 NOT-IN-GT). **LOST strings**: none. **Changed wording**: none.
- Dropped Σ ×3, in-circle Softmax ×3, C₃, and the 20-cell pooled row: **all still dropped**.
- Leading "1" in `1C1`/`1C2` (wave-2-confirmed hallucination): **still present**, byte-identical.
- **Recall**: t9k = (9 EXACT + 17 NORMALIZED + 0.5·2 PARTIAL)/46 = 27/46 = **58.7%**, identical to the frozen wave-2 58.7% (a transcript-level re-derivation, not an independent measurement — no new pixel adjudication per addendum).
- **Verdict**: 9000 changes nothing. The model voluntarily stops at 119 tokens at every budget (119 ≪ 1024) — the ceiling was never binding; the failure mode is a rigid degenerate parse mode, and a bigger budget cannot recover content the model never attempts to emit. Corroboration value is further degraded (3 reads share every error; Jaccard 1.00 nominal).

## Files touched (all under $RUN, report-only respected)

- `03_parses/slide_059/call05_t9k/` — call.log, stdout.log, stderr.log, slide_059.parse.{md,json}
- `05_comparison/slide_059_t9k_delta.md` — new
- `02_worker_logs/slide_059_commands.log` — 7 appended date-stamped lines
- `mission.db` — scope-claim → scope-done (note: "finish=stop at 9000 too (119 tok, byte-identical to 1024/3000 passes); t9k recall 58.7% (= frozen 58.7%, 27/46); nothing changed vs 1024/3000 — ceiling never binding")

Frozen wave-2 artifacts (`07_registers/`, `08_final/scores*`) untouched. No image was opened, no git commands, nothing deleted.
