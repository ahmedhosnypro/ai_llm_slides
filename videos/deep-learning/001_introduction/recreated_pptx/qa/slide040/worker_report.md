# Worker report — slide 040 "How many filters we should apply" (deep-learning/001_introduction)

**Outcome: CERTIFIED (PASS).** Single-version deliverable:
`videos/deep-learning/001_introduction/recreated_pptx/slide_040_recreated.pptx`
Certificate transcript: `videos/deep-learning/001_introduction/recreated_pptx/qa/slide040/judge_attempt_2.txt`
(genuine comparison winner body, `FINAL VERDICT: PASS`).

## Resume context

This worker resumed after a host interruption killed the previous worker mid-judge-loop.
State found on disk: DB `gen_status=judging`, `visual_attempts=3`; 38 banked qa files.

## Attempts (3 banked; certification stands on attempt 2)

| Attempt | Build | Judge | Result |
|---|---|---|---|
| 1 | build_attempt_1.js (04:47) | judge_attempt_1.txt (04:48) | **PASS** — 3 MINOR (serif-vs-sans font family, image proportions, grid re-capture) |
| 2 | build_attempt_2.js (04:56) | judge_attempt_2.txt (05:01) | **PASS** — 3 MINOR (title typeface serif-vs-sans ~85%, cat image aspect ~65%, box-border hue ~60%); no MAJOR/BLOCKER |
| 3 | build_attempt_3.js (05:07) | never dispatched — host died after banking judge_prompt_3.txt/judge_p_payload_3.txt (05:08) | unjudged discretionary polish (title font re-derived to Arial Bold 34.8pt via word-width fingerprint + y recalibration) |

Both banked transcripts were verified genuine: coherent ground-rule dispositions,
element-by-element tables, MINOR-only discrepancy lists, real `FINAL VERDICT: PASS` lines —
not degenerate garbage.

## Resume decision (per resume law: banked comparison-PASS certifies as-is, no re-judge)

The latest banked comparison transcript (attempt 2) is a PASS, so the slide certifies
as-is with NO re-judge. But the certificate binds to the render it judged
(`render_2.png` ← build_attempt_2.js), while the on-disk deliverable was the
**unjudged** attempt-3 build. Actions taken (copy-then-modify; zero banked evidence
deleted):

1. Restored the live build script to the certified state:
   `build/slide_040.js` := `qa/slide040/build_attempt_2.js`.
2. Rebuilt `slide_040_recreated.pptx` from the certified script (assets
   cat_photo/dog_photo/filter_grid unchanged since 04:41).
3. Re-rendered 150 dpi (`qa/slide040/render_2_revert_check.png`, deck-scoped scratch,
   TMPDIR exported, absolute `-env:UserInstallation`).
4. `house_chrome_check.py`: **PASS** (panel x 89–1913, y 95-bottom; badge center
   (1860,148) d=70; tol 8) — banked as `house_chrome_check_revert_out.txt`.
5. PIL pixel comparison rebuilt-render vs certified `render_2.png`: **0 of 2,251,125
   pixels differ** (>30/765 threshold) — the deliverable is exactly the certified
   artifact. Banked as `verify_revert_out.txt`.

The attempt-3 font forensics (title = Arial per word-width fingerprint, contradicting
the judges' serif read) remains banked as qa evidence but is NOT part of the
deliverable — it was never judged, and the judges twice ruled the font deviation MINOR
(non-blocking).

## DB final row

`gen_status=passed`, `visual_check=PASS`,
`visual_transcript=qa/slide040/judge_attempt_2.txt`, `visual_attempts=3`, `last_error=null`.

## Banking

`slide_dependencies.json` has no edges touching slide 40 (not a parent, not in a
pattern group) — no component bank required.

## Judge procedure note

No judge subagent was spawned by THIS worker (no re-judge was needed under the resume
law). The banked attempts' judge procedure was executed by the previous worker through
`scripts/16_vision_gate.sh` (fallback mode, no spawn tool) — both transcripts are gate
comparison winner bodies on the default route (images model).

## Evidence inventory (qa/slide040/)

- `judge_attempt_1.txt`, `judge_attempt_2.txt` — PASS certificates (attempt 2 = DB certificate)
- `probe_1.txt`, `probe_2.txt` — gate window probes
- `judge_prompt_{1,2,3}.txt`, `judge_p_payload_{1,2,3}.txt` — banked prompts (3 = never dispatched)
- `build_attempt_{1,2,3}.js` — per-attempt build provenance (2 = certified build, now live)
- `render_{1,2,3}.png` — per-attempt renders (2 = certified); `render_2_revert_check.png` — rebuild verification render
- `house_chrome_check_attempt3_out.txt`, `house_chrome_check_revert_out.txt` — chrome checks (all PASS)
- `selfcheck_attempt_{1,2,3}_out.txt` — PIL self-checks (ALL PASS)
- `measure_original{,2,3,4}_out.txt` + scripts — PIL ink forensics of the original
- `title_font_forensics_out.txt`, `title_wordwidths_out.txt` — attempt-3 title-font evidence (banked, not shipped)
- `verify_revert_out.txt` — 0-pixel rebuild verification

---

## Resume addendum — second resumed worker (2026-10-12 ~06:23)

A second worker instance was dispatched to resume this slide and worked CONCURRENTLY
with the certifying worker above (race observed live: the certifying worker reverted
`build/slide_040.js` to the certified attempt-2 state and rebuilt the pptx at 06:15,
while the second worker was mid-judge on the superseded attempt-3/Arial render).

Second worker's independent verification of the final state:

1. `build/slide_040.js` md5 == `qa/slide040/build_attempt_2.js` (6801812dfeddf5f72afa9f99aeec54f1) — live script IS the certified build.
2. Fresh 150 dpi re-render of the on-disk deliverable `slide_040_recreated.pptx`
   (private scratch, TMPDIR + absolute `-env:UserInstallation`) md5 ==
   `qa/slide040/render_2.png` (2761dabf66415767ffc8fce7b4e4114d) — the deliverable
   renders EXACTLY the image banked `judge_attempt_2.txt` PASSed.
3. `house_chrome_check.py` on the fresh render: PASS (panel x 89-1913, y 95-bottom;
   badge center (1860,148) d=70, tol 8).
4. `selfcheck_attempt_2_out.txt` (ALL PASS, banked 04:57) applies verbatim to this
   render (md5-identical).
5. DB row re-read at 06:23: `gen_status=passed`, `visual_check=PASS`,
   `visual_transcript=qa/slide040/judge_attempt_2.txt`, `visual_attempts=3`,
   `last_error=null` — concurs with the certifying worker's final row; left unchanged.

### Authenticated-transcript note (second worker)

The banked attempt-1/2 transcripts were initially suspected inauthentic on timing
(1-2 min after banking vs the 2026-10-09 "thinking-high reliably exceeds 240s"
congested-window measurement). Two facts defused that: (a) `analyze_image.py` A4b
transcript hygiene writes a transcript ONLY for a validated, non-degenerate winner
body (atomic rename; failed/degenerate runs never write), so the coherent bodies are
gate-written artifacts; (b) the second worker's own `--thinking high` comparison on a
healthy window completed in ~2 min (06:17->06:19), proving sub-4-min completions are
normal when the gateway is not congested. Verdict: banked transcripts genuine.

### Second worker's invalid dispatch (honest record)

The second worker's attempt-3 judge dispatch (06:17, backgrounded) accidentally
OMITTED the `-p "$(cat judge_p_payload_3.txt)"` GROUND RULES argument, so the gate ran
`analyze_image.py`'s default comparison prompt. The resulting `judge_attempt_3.txt`
(06:19) is a "which image is BETTER" body with NO ground rules, NO severity list and
NO `FINAL VERDICT:` line — it is NOT a valid judge verdict under the frozen template
and carried no weight in certification. It also judged the superseded attempt-3/Arial
render, not the deliverable. Banked as-is (never delete banked evidence); counted as
a consumed attempt with no verdict. Judge attempts consumed: 1, 2 (banked, PASS) + 3
(invalid dispatch, no verdict) = 3 of 6. Attempt-3 build/render (Arial 34.8pt title)
remain banked as unshipped discretionary polish, as the certifying worker documented.

FINAL STATE: slide 040 CERTIFIED (PASS on banked attempt-2 comparison transcript,
deliverable == certified render, 0-pixel rebuild + md5 verified twice independently).
