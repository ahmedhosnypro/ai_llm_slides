# Wave-3 worker prompt (t9k retry) — sent to 4 parallel background agents

Per-scope prompt (identical except the slide number); each worker reads
MISSION_PROTOCOL.md including the WAVE-3 ADDENDUM and follows it exactly.

- agent-8  → slide_037_t9k (task agent-zrywa9dh)
- agent-9  → slide_052_t9k (task agent-oq4ywtru)
- agent-10 → slide_057_t9k (task agent-77emiuvf)
- agent-11 → slide_059_t9k (task agent-nhz0j8y7)

Common shape of each prompt:
1. Claim scope (worker-slide_NNN_t9k).
2. Parse into $RUN/03_parses/slide_NNN/call05_t9k with
   --max-output-tokens 9000 --timeout 300 (5-file call.log convention;
   failed call retried once into call06_t9k_retry).
3. Delta analysis -> 05_comparison/slide_NNN_t9k_delta.md (call record;
   NEW/LOST strings vs the 1024/3000 passes, classified REAL-GT vs
   NOT-IN-GT single-read; transcript-level recall estimate vs frozen
   wave-2 recall; verdict). 057-specific question: does 9000 break the
   Decoder repetition loop?
4. Command log appended to 02_worker_logs/slide_NNN_commands.log.
5. scope-done with one-line note (or scope-fail with exact reason).

Full verbatim prompts were passed to each Agent call; this file records
their shared contract and the agent↔scope↔task-id map (also in mission.db
events).
