# Worker report — slide 019 (Encoder – Decoder Transformer), deep-learning/001_transformers_part1

Resume worker for the judge leg + certification. Dispatched 2026-10-12 after the previous
builder died in a provider storm AFTER building but BEFORE judging (visual_attempts was 0).

## Resumed from

- Banked state on arrival: `build/slide_019.js` (v2, 01:15), `slide_019_recreated.pptx`
  (01:01), component v1 banked (`build/components/slide_019.js`, 00:59), `qa/slide019/`
  had render_1.png + render_2.png, NO judge transcripts.
- Key finding on resume: the banked component (v1) and the current build script (v2) were
  DIFFERENT compositions. Timeline reconstructed from scratch/slide019/ evidence: the
  builder rendered render_2 (01:01), ran closed-loop crop comparisons on it
  (cropcmp_enc_2.txt FAIL, cropcmp_dec_2.txt FAIL — green residual routing MAJOR, missing
  inter-layer chevrons MEDIUM, dashed-vs-solid decoder-MHA border HIGH), did deeper PIL
  scans m15–m18 (finished 01:11), and completed a v2 rewrite of the build script (01:15)
  fixing exactly those findings — then died before rebuilding.

## Steps taken (resume procedure, dispatch steps 1–5)

1. **Re-render of the banked pptx** → pixel-identical to render_2 (PIL diff bbox None,
   md5 match). Pptx intact; render_2 was the current deliverable state.
2. **Fresh pre-judge self-checks on that state** (scratch/slide019_resume/selfcheck_resume.py;
   house_chrome_check.py PASS): PIL ink-agreement vs the original FAILED 10/14 — four
   elements have ink in the original and ZERO in the render (both navy inter-layer chevron
   pairs, leader arrowheads into the encoder and decoder Feed Forward boxes), corroborating
   the builder's cropcmp FAILs. Per the pre-judge law: fix before judging.
3. **Fix = the dead builder's completed v2 script** (not a new invention): rebuilt →
   render_3. Fresh self-check then caught one residual v2 bug: z-order. DELTA_BLOCKS drew
   `leader4` (arrowhead at x642–648, y300–306) BEFORE `enc_repaint` (tan patch x631–725,
   y268–353), so the patch buried the head (0 dark px vs orig 18). Fixed by drawing the
   container repaint patches first (Z-ORDER LAW comment added in the script) → rebuild →
   **render_4: self-checks 14/14 PASS + house_chrome_check PASS**.
4. **Judge attempt 1** on render_4 (frozen `-p` template with GROUND RULES prelude,
   banked as judge_prompt_1.txt; shared-base fact in `--view`; default route, no
   `--models`; W4 wall `--timeout 420` wrapped in `timeout 540`, `--thinking high
   --max-tokens 65536`). Both short-wall probes hung (rc 124; probe ladder: probe →
   sleep 300 → re-probe once → hang) while other fleet workers' comparisons were landing
   (gateway alive, HTTP 401 on /models), so the comparison was dispatched directly — it
   landed first try.
5. **Verdict (from the banked winner body, verbatim): FINAL VERDICT: PASS** for 'faithful,
   usable recreation'. Harness evidence: `[winner] images (round 1, attempt 1)`,
   `degenerate events: 0`, transcript written (validated winner, atomic).
   Findings: 4 × MINOR only (h-circle placement medium; SDPA top-MatMul shadow-stack
   low; leader-arrowhead faintness low; ~1–2% inset scale medium). No BLOCKER/MAJOR.
   All v2 delta fixes verified present by the judge (steel-blue A&N, dark-gray FF,
   indigo decoder-low A&N, green buses with stub arrowheads/pickups, navy chevrons,
   solid decoder-MHA border, green encoder V circle).
6. **DB**: `visual_check=PASS`, `visual_transcript=videos/deep-learning/001_transformers_part1/
   recreated_pptx/qa/slide019/judge_attempt_1.txt`, `visual_attempts=1`, `gen_status=passed`.
7. **Component re-banked** (the composition changed from the banked v1): components form of
   the certified v2+z-order script generated programmatically (body byte-identical to the
   judged build script; require retargeted to `./slide_018.js`; runnable entry removed;
   bank contract + z-order law documented). `build/slide_019.js` converted to the
   018-style thin wrapper. Verification: wrapper rebuild → render → **0-pixel-diff vs
   render_4** (diff bbox None; component_verify.txt + component_verify_render.png).
8. Judge procedure executed by worker via Bash — no Agent/Task tool available in this
   environment (orchestrator-approved fallback per scripts/17_worker_instructions.md §7).

## Attempts used

| Attempt | Render | Self-checks | Judge | Verdict |
|---|---|---|---|---|
| (dead builder) | render_1, render_2 | cropcmp_enc_2 FAIL, cropcmp_dec_2 FAIL | none (died) | — |
| 1 | render_3 (v2, z-order bug) → render_4 (fixed) | 13/14 → 14/14 + chrome PASS | judge_attempt_1.txt | **PASS** |

## Deliverable

- `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_019_recreated.pptx`
  (single version, built by `build/slide_019.js` wrapper from `build/components/slide_019.js`)
- Certified render: `qa/slide019/render_4.png`; judged composition == component output
  (0-pixel-diff). No equations on this slide → no OMML wrap. No advanced-graph generation
  (the figure insets are the parent chain's certified composition).

## Evidence bank (qa/slide019/)

- judge_prompt_1.txt, judge_attempt_1.txt (comparison transcript, PASS), probe_1.txt ABSENT
  (both probes hung rc 124 — noted honestly; not evidence, not an attempt)
- render_1..4.png (render_3 kept as the z-order-bug demonstration)
- build_attempt_1.js (verbatim build script at judge time), build_attempt_3.js +
  judge_prompt_3.txt (foreign concurrent session's files, 01:30; never executed; its target
  render_3 is superseded — see COORDINATION_NOTE.txt)
- selfcheck_attempt_1.{py,txt}, house_chrome_attempt_1.txt, component_verify.txt,
  component_verify_render.png, COORDINATION_NOTE.txt

## Cross-video note

Lecture 002's slides 19 and 37 will import
`videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_019.js`
(playlist-scoped bank contract; certified PASS 2026-10-12, slide 019 of 001 is now a valid
cross-video dependency parent in the 001 DB).

---

## Co-worker addendum (the concurrent first-dispatch session, 2026-10-12 ~23:40–01:55)

For the record — this report's "dead builder" and "foreign concurrent session" were the
same two facts seen from the other side; this session was the FIRST dispatch for slide 019
and ran concurrently with the resume worker until the COORDINATION_NOTE protocol resolved
the overlap (this session stood down from judging and adopted the resume worker's certified
state; no double judge was dispatched):

- Independent delta measurement of `unique_slides/slide_019.jpg`: PIL scans
  `scratch/slide019/m0..m7` (+ m4/m5/m7 color-mode passes) and 4 vision probes through the
  gate — `probe_callouts.txt` (callout fills/text/borders/leaders), `probe_enc.txt`
  (blue rounded A&N, gray FF, GREEN encoder V circle, 2-loop encoder bypass),
  `probe_dec.txt` (3-loop decoder bypass, blue/blue/red V-K/Q rows, gray-green FF),
  `probe_dectop.txt` (decoder-top band unchanged). These corroborate the builder's
  m0–m14 findings; measurements agree within JPEG tolerance.
- Banked a v1 component draft at 00:59 (`components/slide_019.js`) from its own
  measurements — SUPERSEDED by the resume worker's certified re-bank (the v1 was written
  before m15–m18 existed; its leader model was 3 lines vs the certified 5).
- Built render_3 from the dead builder's v2 draft + ran the full pre-judge self-check
  suite (`scratch/slide019/selfcheck_3.py` → `selfcheck_3_out.txt`: house_chrome_check
  PASS, containment 0 violations, inheritance diff confined to the legend/stack delta
  zones, A&N/FF text bands inside boxes, all delta-zone inks present). Superseded by
  render_4 (z-order fix) per the coordination note.
- Banked judge_prompt_3.txt / build_attempt_3.js (never executed — render_3 superseded;
  documented above and in COORDINATION_NOTE.txt).
- DB milestones: gen_status=building + build_script (23:5x), judging (01:30), and the
  terminal verdict-law fields (visual_check=PASS / visual_transcript / visual_attempts=1 /
  gen_status=passed) matching the resume worker's step 6.
- Post-certification banking verification (independent re-run):
  `component_bank_pixelcheck.txt` — rebuild through the thin wrapper + certified component,
  150dpi render vs `render_4.png`: **0 of 2,251,225 pixels differ**. Consistent with the
  resume worker's component_verify.txt.
- Final state verified by this session: DB row gen_status=passed, visual_check=PASS,
  deliverable single-version, component banked and pixel-verified. Slide 019 is DONE.
