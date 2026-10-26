# agent-10 wave-3 return — slide_057_t9k (banked verbatim from task agent-77emiuvf, 2026-10-25)

Scope complete and verified in the DB. Final handoff:

## Result — slide_057_t9k (wave-3 t9k retry)

**Headline: the 9000-token budget does NOT break the `Decoder` repetition loop.** Both t9k calls died at exactly the 9000-token cap with `finish_reason=length` — the failure is budget-independent and deterministic.

### What was done
1. **Claimed** `slide_057_t9k` as `worker-slide_057_t9k` (DBCTL scope-claim, exit 0).
2. **Parse calls** — both into fresh dirs, 5 files each (call.log, stdout.log, stderr.log, `.parse.md`, `.parse.json`):
   - `03_parses/slide_057/call05_t9k/` — EXIT=0, finish=**length**, 9000/9000 tokens, 36,027 chars, 71.5 s, stderr 0 lines → FAILED per protocol.
   - `03_parses/slide_057/call06_t9k_retry/` — the one allowed retry: EXIT=0, finish=**length**, 9000/9000 tokens, 36,027 chars, 74.9 s → **byte-identical** to call05 (same sha256).
3. **Delta analysis** written to `05_comparison/slide_057_t9k_delta.md` (all 4 addendum sections).
4. **Command log** appended to `02_worker_logs/slide_057_commands.log` (5 date-stamped lines).
5. **Closed** via scope-done; DB row `slide_057_t9k = done` carries the headline note.

### Key findings (measured, not estimated)
- **Zero NEW strings, zero LOST strings, zero wording changes** at 9000 tokens: the t9k unique-line set is set-equal to the 1024/3000 set (same 6 lines: `57`, `Encoder`, `Decoder`, `Encoder Block 2`, FFN-with-RELL string, Residual string).
- Stronger than set-equality: call05's transcript is **byte-for-byte the 3000-pass output plus exactly 3,000 more `Decoder\n` lines** (verified via startswith + tail histogram). The first 3,000 tokens of every call are deterministic; the budget only sets how long the loop runs (`Decoder` ×489 @1024, ×1477 @3000, **×4477 @9000**, + 9 `Encoder` lines in every call).
- **t9k transcript-level recall = 12.5%** (5 EXACT + 1 NORMALIZED of 48 GT strings) — identical to the frozen wave-2 recall (0.0 pp delta). No new pixel adjudication performed (addendum boundary).
- `finish_all_stop` stands at 0/6 for this slide across all budgets; the real diagram text beyond the 6 unique lines (31 further GT strings: chips, word rows, embeddings, K/V/Q, Softmax, bottom tokens, legend, attention-box labels) never emerges at any budget. Wave-2 frozen artifacts untouched (report-only, additive).

### Caveats for the orchestrator
- Both t9k calls are FAILED calls (finish≠stop) — banked as evidence per the addendum; they count out of done metrics. The 9k attempt tripled output cost (~4.3× tokens vs the 3000 pass) for zero information gain, confirming 057's degeneracy as generation-side (drop + loop), not budget-side. Whether any mitigation (e.g. repetition penalty) exists is outside this scope's tools.
- The `slide_057_vj` scope belongs to another worker — untouched.
