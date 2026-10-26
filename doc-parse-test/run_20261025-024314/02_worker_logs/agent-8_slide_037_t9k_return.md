# agent-8 wave-3 return — slide_037_t9k (banked verbatim from task agent-zrywa9dh, 2026-10-25)

Scope complete and closed. Final handoff:

## slide_037_t9k — done (wave-3 t9k retry)

**Headline:** t9k calls finished `stop` (2/2), but **t9k recall = 6.9% (2/29) vs the frozen wave-2 79.3%** — 9000 tokens changed nothing; the parser used only **27 of 9000** output tokens.

**What was done**
1. **Claimed** `slide_037_t9k` (DB confirms `done` now, worker `worker-slide_037_t9k`).
2. **call05_t9k** (`03_parses/slide_037/call05_t9k/`, 5 files): EXIT 0, `finish_reason=stop`, 27 out tokens, 166 chars, 3.7 s. Valid per protocol, but returned the *title + badge + one mega-`<class_Picture>`* read — byte-identical to the wave-2 3000-token pass (verified with `diff`).
3. **call06_t9k_retry** (fresh dir, since call05 was suspiciously identical at 1/35 the latency of pass2): EXIT 0, stop, 27 tokens, 166 chars, 5.8 s — **byte-identical again**. Two independent t9k calls plus pass2 produce the exact same bytes while latencies vary 128.3 s → 3.7 s (logged as a ledger `observation`, event id 28: minimal read is deterministic; consistent with an endpoint cache on the repeated request — hypothesis, not confirmed).
4. **Delta report** written: `05_comparison/slide_037_t9k_delta.md` — all 4 addendum sections (call record; delta: 0 NEW strings, 0 NOT-IN-GT, 21 GT labels lost vs the 1024 pass; recall 2/29 = 6.9% transcript-level next to frozen 79.3%; verdict). Not a 057-type repetition failure — no loop to break.
5. **Commands logged** (appended, date-stamped) to `02_worker_logs/slide_037_commands.log`; **scope-done** with the headline note.

**Key finding:** the token ceiling is not the binding constraint for this dense 3-diagram slide — the parser's own decision to collapse the diagram field into one `class_Picture` is. The rich read came from the *low* 1024 pass; both high-ceiling reads (3000, 9000 ×2) emit the minimal title+badge. Recreation power from a t9k transcript alone ≈ 1/10 (wave-2's frozen 2/10 stands untouched; no frozen artifacts modified, no images read, no writes outside `$RUN`, no git).
