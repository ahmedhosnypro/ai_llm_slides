# Iteration ledger — slide_059_vj (wave-4 visual-judge loop)

Append-only, one row per round. Recall = weighted union (EXACT 1.0 + NORMALIZED 1.0 +
PARTIAL 0.5) of ALL banked transcripts for this slide vs the frozen 46-string inventory
(`04_ground_truth/slide_059/inventory.md`), measured by `measure_recall.py` — a
deterministic matcher encoding the wave-2 comparison contract, validated to reproduce
the frozen wave-2 score (27/46 = 58.7%) on `call01_pass1` before any wave-4 measurement.
Disclosed normalizations: subscript Unicode→ASCII, underscore/dash/slash deletion,
glyph confusions ∑/σ→Σ, and a symbol-only fold (I/L/l→1, O→0; case-aware, ≤5-char
symbols, never fires on ≥6-char words; does NOT fold i→1).

Baseline (frozen wave 2): 27/46 = 58.7% — 9 EXACT + 17 NORMALIZED + 2 PARTIAL over
call01_pass1 ∪ call02_pass2 (byte-identical; call05_t9k also byte-identical → all three
full-frame transcripts carry the same 27.0).

## Row 1 — round 1 (2026-10-25)

- **Verdict**: `FINAL VERDICT: FAIL for 'doc-parse full-frame transcript fidelity vs the original slide_059 frame'` — `judge/round1_transcript.md` (single-read, unconfirmed; Tier-2 gateway leg; arbitrations banked there: 2 judge findings dismissed as transcript misreads, pooled-row cell count 7–8 dismissed vs wave-2 measured 20).
- **Crops**: 4 planned (`crops/round1/`, boxes in round1_transcript.md); pre-checks OK (dims ≤1664×2048, nonzero mean, `crops/round1/precheck.txt`).
- **Crop parses**: 3 OK + 1 FAILED — call04_round1 (pooled row) failed 3× with `Remote end closed connection without response` (retry dirs banked; no 429/5xx text, so the 60s backoff never applied; failure recorded for task-add). Doc-parse latencies: 14 s / 4 s / 8 s / ~1 s×3 (failures).
- **Gateway calls**: probe 1.4 s + round-1 judge 13.4 s.
- **New GT strings this round (13; +12.5 weighted)**: Σ (#6, EXACT via call01_round1) · C₃ (#11, PARTIAL via `1C3` — same leading-1 hallucination family as C₁/C₂) · X₂ X₃ X₄ X₅ (#14–17, NORMALIZED via call02_round1 one-line) · X_{N-2} (#18, NORMALIZED via `XN2`) · X_{N-1} (#19, NORMALIZED via fold on `XNI`) · Y₂ Y₃ Y₄ Y₅ (#22–25, EXACT, one-per-line in call03_round1) · Y_{N-2} (#26, NORMALIZED via `YN/2`) · Y_{N-1} (#27, NORMALIZED via `YN-1`).
- **Recall trajectory**: 58.7% → **88.0%** (40.5/46; EXACT 14 + NORMALIZED 25 + PARTIAL 3). **Delta +29.3 points.**
- **Still MISSING (4)**: X₀, X₁, Y₀, Y₁ — the round-1 crops read them as `Xi □ Xi` (X row) / `Yq` + nothing (Y row); the 0/1 subscripts are unresolved at this crop scale.
- **Efficiency**: 3 successful crop-parse calls → 12.5 weighted strings = **4.2 strings/call marginal yield** (the marginal yield of any further full-frame call is 0.0 — call02/call05 both reproduced call01 byte-for-byte). Gateway: 2 calls for the round.
- **Hallucination candidates added**: `1C3` leading-1 (extends the adjudicated 1C1/1C2 pattern — advisory) · fragments `es`, `Z` (Z is a probable Σ mangle — GT#6 already matched by the real Σ) · box/bullet glyphs `□ ○ ⊗ •` (non-text decoration).

## Row 2 — crop04 disposition (2026-10-25, wave-4 continuation)

- **4th attempt: SUCCESS** — `call04_round1_retry4` (default config budget: `--timeout 300`, no token override), EXIT 0, `finish_reason=stop`, 4.1 s, 6 output tokens, transcript `<x_0.0><y_0.0><x_0.998><y_0.9891><class_Picture>`. Banked: call.log + stdout.log (empty stderr).
- **Root cause of the 3 earlier failures**: infrastructure, not content — `call04_round1_retry3/stderr.log` banks `<urlopen error [Errno 111] Connection refused>` (doc-parse endpoint down at 08:21; same instant-fail signature on retry2). Endpoint recovered by 20:03.
- **Interpretation**: crop04 is the pooled cell row (~fy 149–164) — a TEXTLESS region. The transcript carries corner coordinates + a `<class_Picture>` token and ZERO text tokens: the correct output for a region with no text (the round-2 judge template's TEXTLESS-OK state). The 3× failure masked a faithful-empty result, not a missed-text one.
- **Gate effect**: nonempty parse transcripts 3 → **4** (>=4 threshold CLEARED). Union recall unchanged **88.0%** (40.5/46; retry4 adds 0 strings — the region carries no GT text). Still missing: X₀, X₁, Y₀, Y₁.

## Row 3 — round-2 judge leg: BLOCKED (2026-10-25 evening, ~20:12–21:34)

- **Round-2 judged round NOT ACHIEVED — infrastructure blocker.** Round-2 prompt design banked (`judge/round2_prompt.txt`, template v2 full, 9845 B; `judge/round2_prompt_v21_compact.txt`, 6448 B; full-v2 copy `round2_prompt_v2_full_hung_variant.txt`); no round-2 verdict exists — nothing fabricated.
- **Attempt log** (all in `judge/round2_call.log` + `judge/round2_stderr.log`): attempt 1 (20:12, parity flags) EmptyStreamError + HTTP 502 `upstream_unreachable` (Nvidia candidate) · attempt 2 (20:17, instructed command verbatim, CLI defaults) hang >7 min → killed at 600 s bg wall; stderr banks EmptyStream ×2 + HTTP 504 `upstream_timeout` · attempt 3 (20:34, post-60 s-wait contract retry, parity flags) 3× `HangError` hard-wall 270 s, EXIT 1 · attempt 4 (20:52, DISCLOSED fallback `--models GLM-5.3` per AGENTS.md fallback note) read-timeout 240 s — and the GLM-5.3 TINY PROBE also read-timed-out (120 s) → GLM serving independently dead · probe3 (20:56, images route) PASSED 42 s, transcript `59.` → recovery declared · attempt 5 (21:00) 2× HangError 270 s, killed · attempt 6 (21:10, compact v2.1, `--timeout 300`) HangError at 330 s wall, killed · attempt 7 (21:21, PROBE-GATED: gate probe PASSED ~2 s, `probe/probe4_gate.txt` = `59.`; audit fired in the same serving window) HangError at 360 s wall; retry-2 stopped as predetermined.
- **A/B finding (the round's hard evidence)**: tiny probe (93 B prompt, same image) served 3/3 (2 s / 42 s / 2 s); audit-shaped requests (6.4–9.8 KB prompt, same image, same route) served 0/8 with ZERO stream deltas across 270/300/330/360/480 s walls — thinking disabled, `stream:true` hardcoded (no non-streaming path in the CLI). The wedge is request-class-specific at the upstream serving layer, not prompt-content-, image-, or route-health-flap-specific. Lane served the 6.5 KB round-1 audit in 13.4 s at 08:16; doc-parse (separate service) recovered by 20:03 — the vision lane did not within this window.
- **Gates**: parse gate CLEARED (4 nonempty transcripts, row 2). Judged-rounds gate 1/2 → BLOCKED. VJ report written with BLOCKED labeling (`VJ_IMPROVEMENT_REPORT.md`).
- **Retry recipe for the next window**: probe gate (tiny probe, `--timeout 90`) → on pass, fire `judge/round2_prompt.txt` (v2 full) `--timeout 240 --rounds 1 --tries 1`; fall back to v2.1 compact. Healthy-lane reference: 08:16 round-1 call (13.4 s) and 08:13 probe (2 s).
