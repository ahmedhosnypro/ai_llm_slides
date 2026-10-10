# Judging — the visual verdict law

A slide is done ONLY when a real comparison transcript from the vision model contains a
winner-body PASS. Everything else is a FAIL (or a re-try), no exceptions:

- Timeout / empty stream / probe-only read / degenerate garbage output → recorded FAIL.
- A worker's or peer's "looks good" → not a verdict.
- A PASS obtained with a prompt that omits the ground rules → re-judge.

## Invocation pattern

All vision calls go through the flock gate (`scripts/16_vision_gate.sh`, 16 slots —
fleet-global across all workers/videos). Default route = the `images` model; **never
pass a `--models` flag** (routes to the wrong upstream).

Comparison (the real judge):
```
scripts/16_vision_gate.sh analyze_image.py comparison \
    <render_K.png> <original_frame.jpg> \
    --view <banked context> --capture <banked context> \
    --thinking high --max-tokens 65536 --timeout 420     # wrapped in `timeout 540`
```

Probe first (short wall) to warm/verify the route:
```
... --timeout 120 --rounds 1 --tries 1    # in `timeout 150`
```
If the probe hangs: `sleep 300`, re-probe ONCE, then proceed.

- W4 retry: one hard-wall HangError retry is part of the protocol (not an attempt).
- **3 garbage re-invokes** allowed (degenerate output = the call didn't happen), and
  **6 judge attempts per slide** before parking the row as failed for review.

## The ground-rules prelude (mandatory in the judge prompt)

The judge sees two images (recreation first, original second) and tends to flag
intentional differences as defects. Prepend a GROUND RULES prelude stating, in the
deck's terms:

(a) the house template (frame/badge/title geometry) is intentional — findings about
    it are overridden;
(b) contentless originals are matched by contentless recreations;
(c) lecture-video artifacts (cursors, player chrome, watermarks, capture glitches)
    are correctly OMITTED from the recreation;
(d) typed-vs-handwritten renderings of the same text are MINOR;
(e) equations in the recreation are rendered in PROFESSIONAL 2D FORMAT (stacked
    fractions, large Σ with limits, aligned sub/superscripts) — if the original shows
    the same equation in linear/typed notation, that difference is a mandated format
    upgrade, NOT a discrepancy;
(f) the verdict is about fidelity of renderable content only.

End the prompt with: `FINAL VERDICT: PASS or FAIL for 'faithful, usable recreation'`
and require the winner body to name the winning image explicitly. The full template is
in `scripts/17_worker_instructions.md` — use it verbatim.

## Verdict handling

- PASS from a real winner body → bank transcript, set `visual_check=PASS`.
- FAIL with findings → apply fixes (measured, per building.md discipline), re-render,
  re-judge, increment attempt number.
- Keep counting; at 6 attempts park the slide and report — never silently drop it.

## Judge limitations to remember

- The judge can MISREAD small numerals (one read a badge as "16" on slide 19 —
  house-rule override won, but note close-out deviations).
- A judge PASS does NOT override measured geometry: founder feedback on position
  defects (see equations.md alignment law) wins over the judge.
- Judge findings at "low-medium confidence" about the template/border shade are
  pre-existing MINOR items, not new defects — read the transcript, don't react blindly.
