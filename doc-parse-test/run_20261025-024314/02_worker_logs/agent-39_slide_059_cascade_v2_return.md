## MISSION COMPLETE — slide_059_cascade_v2 · scope-done EXECUTED (DB: `done`)

**Headline: union recall 58.7% → 100% (46/46 GT strings) · 16 crops · 16/24 parse calls · parallel speedup ≈2.6×**

### Recovery from the app exit
DB confirmed my claim was intact (`in_work`, mine); the output tree was empty except dirs; the command log showed only claim+init had run. Restarted the mission from the beginning per the brief.

### What was executed
- **Region extraction**: the full-frame parse (call05_t9k) yielded exactly ONE class block (`class_Picture`, origin-only → estimated quadrant box `crop06`, marked `estimated: true`); <2 usable regions → supplemented with the wave-4 arbitrated CROP PLAN boxes (judge-supplement provenance) + register M4/A8 annotation band.
- **3-level cascade, 16 crops, 16 parse calls in 3 parallel batches** (`&`+`wait`, max 4 concurrent; wall ≈23 s vs 60 s Σ-latency): L1 6 crops → L2 7 (parse-garble triggers) → L3 3; every node stop-reasoned (5× no-internal-structure, 11× no-new-information; crop cap 16/16 reached, call budget 16/24).
- **13 vision-gateway judges** (probe `PROBE-OK` first, max 1 in-flight; one judge lost to a fleet-gateway timeout and retried successfully).

### How 100% was reached
- doc-parse crop parses recovered: **Σ verbatim**, C₁/C₂/C₃ clean (killing the `1C1/1C2` hallucination), X₀/X₂/X₃, X_{N-2}/X_{N-1}, Y₂–Y₅, Y-tails, **Y₁** — 42/46 (91.3%).
- The vision-judge leg recovered the last 4 doc-parse-provably-impossible strings: **Y₀** (2 reads), **X₁** (2 reads, slot-consistent), **X₄/X₅** (2 independent judges, digits "clearly readable", positions matching wave-2 pixel adjudication) + upgraded C₁/C₂ partials to full.
- The "unread 20-cell table row" is structurally recovered and explained: judge counts ~20 pastel cells, **no text in any cell** — a textless-region omission, not a read failure. Chart-class blocks (`ranked_table`, `pictogram_percentage`) emerged only at crop scale.

### Artifacts (`$RUN/12_cascade_v2/slide_059/`)
`manifest.json` (16 crops, **0 null boxes/stop_reasons**, transforms + provenance + judge wiring), 16 five-file parse call dirs, 13 judge transcripts + probe, `compose/COMPOSED_ANALYSIS.md` (46/46, position-tracked, y-ordered, provenance + hallucination/GT-gap sections), `CASCADE_REPORT.md` (trajectory, tree, per-crop yield, speedup, compliance checklist). Commands appended to `02_worker_logs/slide_059_cascade_v2_commands.log`.

**Follow-up worth noting**: the doc-parse subscript-digit failure mode at ≤3× (4/5 digits, Y-head zone) is a systematic model limitation — the judge leg is the only recovery route at permitted zoom; relevant doctrine candidate for the skill corpus.