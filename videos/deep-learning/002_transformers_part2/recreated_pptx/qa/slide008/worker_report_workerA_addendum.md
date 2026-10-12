# WORKER A VERIFICATION ADDENDUM — slide 008 (dual-dispatch collision resolution)

Written 2026-10-12 ~10:25 by Worker A ("main dispatch") of the 002:8 dual dispatch.
This is an APPEND-ONLY addendum per the collision protocol — it certifies nothing new;
the certificate binds to the JUDGED chain (Worker B's attempt 2).

## Resolution of record

- Two workers were dispatched for 002:8. Worker A started ~07:14 (clean collision sweep
  at start: empty scratch/qa, no build file, DB pending). Worker B's artifacts appeared
  from 07:51. Collision detected 08:44 (live vision-gate process) → Worker A stood down
  READ-ONLY per protocol; orchestrator confirmed the refinement (no path fights; the
  certificate binds to whichever chain actually gets judged).
- Worker B continued the attempt chain as ATTEMPT 2 (qa/slide008/collision_notice.txt),
  preserved Worker A's attempt-1 evidence untouched, folded in Worker A's PIL-verified
  corrections (K.q position/size, title L1 +3px, W_q box geometry, sentence container
  top y477, legend W-border color, block-arrow geometry) and corrected/refuted others
  by its own frame measurements and gated zoom reads.

## The judged chain (Worker B, attempt 2) — what Worker A verified

- Canonical chain coherence: `build/slide_008.js` (10:02, 15803B) == `qa/slide008/build_attempt_2.js`;
  `slide_008_recreated.pptx` (10:03, 186602B, single plain-named deliverable);
  `qa/slide008/render_2.png` (10:03) — the judged artifact.
- Dependency law: attempt-2 build requires the parent's certified component
  (`001_transformers_part1/recreated_pptx/build/components/slide_033.js`) by ABSOLUTE
  PATH, calls renderBase with this slide's delta blocks skipped, draws deltas at measured
  geometry, chrome via the shared house-chrome chain with badge numeral 8. Compliant.
- Vision evidence: `scratch/slide008/judge2_run2.log` documents the gated full-slide
  comparison (default route, images model): attempt 1 echo-aborted by the gate itself
  (GarbageError, script-recovered), attempt 2 validated winner written atomically to
  `qa/slide008/judge_attempt_2.txt` — FINAL VERDICT: PASS, verdict line
  `{"page": 1, "verdict": "pass", "issues": []}`. The winner body's gate-log shape is the
  frozen template's mandated FINAL MESSAGE format (the template names the transcript path).
- Corroborating gated evidence banked by Worker B: `qa/slide008/crops_compare_2.txt`
  (dense-region crop-pair comparison, image-grounded per-panel findings, all MINOR,
  FINAL VERDICT PASS) and the frame zoom-label reads `qa/slide008/zoomread_orig.txt` /
  `zoomread_zoom8.txt`.
- DB row (read 10:24): gen_status=passed, visual_check=PASS, visual_attempts=2,
  visual_transcript=qa/slide008/judge_attempt_2.txt, pptx_path/build_script = the
  attempt-2 chain. Verdict-law current.
- Caveat noted for the record: the winner body cites `probe_2.txt`, which is not banked
  in qa/slide008/ (the probe only opens the gateway window; the comparison is the
  evidence, and its run + validation are documented in judge2_run2.log).

## Banking obligation (Worker A's dispatch step)

Checked BOTH decks' dependency graphs for 002:8 as a PARENT:
`001_transformers_part1/slide_dependencies.json` and `002_transformers_part2/slide_dependencies.json`
— no edge references `002_transformers_part2:8`. Per the banking rule ("export
recreated_pptx/build/components/slide_008.js ONLY if referenced"), NO component export
is required. 002:8 is itself a CHILD of 001:33, whose playlist-scoped banking is 001's
obligation (already discharged there).

## Worker A's preserved evidence (attempt 1 — banked, never deleted)

- `qa/slide008/build_attempt_1.js` (copy of Worker A's build; identical bytes to the
  build it wrote at 08:36 before the peer's takeover)
- `qa/slide008/render_1.png` (150dpi render of attempt 1)
- `qa/slide008/selfcheck_attempt_1.py` + `selfcheck_attempt_1_output.txt` (28/28
  closed-loop checks PASS vs the remapped frame targets; house_chrome_check PASS)
- `qa/slide008/judge_prompt_1.txt` (banked prompt; attempt 1 never dispatched a judge —
  the stand-down landed before the probe wrote its transcript, so attempt 1 has no
  vision evidence by design of the collision, not by omission of the law)
- scratch/slide008: landmarks.py, delta.py, probe.py, measure2-6.py, monitor_peer.py/log
- Worker A's independent measurements that Worker B re-verified TRUE and folded into
  attempt 2 are documented in the attempt-2 build header.

No further action by Worker A. Certificate: single-read, default route (images),
glm leg DEFERRED/BLOCKED — binds to the judged attempt-2 chain.
