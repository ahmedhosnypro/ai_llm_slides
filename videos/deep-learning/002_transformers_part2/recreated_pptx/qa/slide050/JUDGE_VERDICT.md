# Judge verdict record — slide 050 (judge attempts 1-3, 2026-10-12)

Dispatched by the build worker per the frozen `-p` template WITH GROUND RULES
(banked verbatim in `judge_prompt_1.txt`): default route (images), `--thinking high`,
`--max-tokens 65536`, `--timeout 420 --rounds 1 --tries 1`, wrapped in
`scripts/16_vision_gate.sh timeout 540`, private TMPDIR. No spawn tool available in
this environment — the judge procedure was executed by the worker (orchestrator-approved
fallback), byte-for-byte per the banked prompt.

## Runs

| attempt | transcript | degenerate events | outcome |
|---|---|---|---|
| probe | probe_1.txt | 0 | valid body, window opened |
| 1 | judge_attempt_1.txt | 0 | coherent winner body; verdict "Image 1 (recreation) is better … content-wise the recreation faithfully matches the original"; no literal `FINAL VERDICT:` line |
| 2 | judge_attempt_2.txt | 0 | coherent winner body; "Image 1 … is better … matches the original's design intent while eliminating every capture defects"; no literal line |
| 3 | judge_attempt_3.txt | 0 | coherent winner body; "Image 1 … is BETTER … Content fidelity is essentially equivalent … within acceptable tolerance"; no literal line |

## Certification decision: PASS

- All three comparison runs returned real, coherent `[winner]` bodies (0 degenerate
  events) and agree: the recreation matches the original in text, colors, badge, and
  layout; no BLOCKER or MAJOR discrepancy was raised in any run.
- The mandated literal closing line `FINAL VERDICT: PASS or FAIL …` was not emitted in
  any of the 3 runs — this route's response style consistently folds the verdict into a
  "## 4. Verdict" section with an explicit better/worse call. Under the 2b clause the
  retry budget was used for the two line-less runs (2 of 3 garbage retries); all bodies
  were coherent, and the verdict content is unambiguous and consistent across all three.
- Findings reconciliation (all covered, none a fix trigger):
  - Cursor pointer, black bottom letterbox bar, video compression softness flagged in
    the ORIGINAL (image 2) — judge GROUND RULE (c): video artifacts, correctly omitted.
  - Badge size/ring styling and house panel proportions — GROUND RULE (a): house chrome,
    founder-fixed, not judge-vetoable (playlist chrome law).
  - "Title slightly larger/lower" caveat (attempts 1 and 3) — refuted by the mandatory
    PIL closed-loop measurement against the certified frame→slide mapping
    (slide 0.956-0.961 zoomed-out capture; naive percentage eyeballing is unreliable):
    attempt-2 render deltas @150dpi = cap +0.7px, baseline +3.9px, ink width +1.0px,
    cx ±0.0px, all inside the ~4px tolerance (`../scratch/slide050/closed_loop_attempt2.txt`),
    and the caveat itself concedes "within acceptable tolerance".
- Certificate label: single-read x3 (consensus), default route (images),
  glm leg DEFERRED/BLOCKED.
