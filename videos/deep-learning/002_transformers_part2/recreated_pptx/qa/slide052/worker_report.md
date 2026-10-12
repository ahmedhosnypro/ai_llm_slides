# Worker report — slide 052 (002_transformers_part2, deep-learning)

**Slide:** 52 — "Transformer Decoder: Encoder-Decoder Attention and Masked Multi-Head
Self-Attention Blocks" (pure schematic, no title bar). **Verdict: PASS** (visual judge,
comparison transcript `judge_attempt_2.txt`). DB row: `gen_status=passed`,
`visual_check=PASS`, `visual_attempts=2`.

## Deliverables

- **PPTX (single-version law):** `videos/deep-learning/002_transformers_part2/recreated_pptx/slide_052_recreated.pptx`
- **Build script:** `videos/deep-learning/002_transformers_part2/recreated_pptx/build/slide_052.js`
- **Final render:** `recreated_pptx/qa/slide052/render_5.png` (150 dpi, LibreOffice headless,
  private profile, TMPDIR under scratch — quota-safe)
- **Comparison transcript (certifying):** `recreated_pptx/qa/slide052/judge_attempt_2.txt`
- **Judge prompts banked:** `judge_prompt_1.txt` (attempt 1), `judge_prompt_2.txt` (attempt 2)
- **Per-attempt build copies:** `build_attempt_1.js`, `build_attempt_2.js`
- **Pre-judge crop checks:** `cropcheck_maskedrow_1..4.txt` (dense-region loop on the masked row)
- **Self-checks:** `selfcheck_attempt_1.py/_out.txt`, `selfcheck_attempt_2.py/_out.txt`,
  `selfcheck_attempt_4.py/_out.txt`, plus measurement evidence in
  `scratch/slide052/` (chrome2/chrome3, content, colormap, scanlines, box_ascii,
  box1_zone, tipzones, tipcount, detail*, text_extents, yborder_grid).

## Attempts

- **Judge attempt 1** (`judge_attempt_1.txt`, render_4.png): FAIL — 1 BLOCKER
  ("missing decoder-column token strips" between the Masked blocks and the purple
  bar) + minors (missing down-arrows under the top token groups — spec step 9,
  which I had indeed omitted; Y-group enclosure border; FFN italic claim; masked-3D note;
  unconfirmed bottom-containment flag at conf 0.35).
- **Judge attempt 2** (`judge_attempt_2.txt`, render_5.png): **PASS** — "all textual
  content, layout regions, colors, and structural elements match", no blockers, no
  quality defects. Two MAJOR polish notes at low confidence (~55–60%), overridden by
  pixel measurement (below). Four minors accepted as cosmetic.

## Fixes applied across the pre-judge loop (evidence-backed)

1. **Masked-box text sizes** — systematic frame-px→pt correction (÷0.95556): all
   captions/labels re-derived from measured ink extents (bars 15.5pt, FFN 15pt with
   Courier RELU, purple 15.5pt, upper labels 13pt/16 pitch, masked 9.5pt/12 bottom-aligned,
   encoder 19pt, callouts 14.5pt/18, inputs 15pt, word boxes 12.5pt, legend 12.5pt, Y 13pt).
2. **3D box icons** (pixel maps `box_ascii.txt`, `box1_zone.txt`): royal faces at the
   measured positions (upper y178–243, masked y344–384), navy slab-edge stripes at the
   text-line boundaries, white top strips, side slivers, dark bottom shadows.
3. **Causal-mask arrow tips** (`tipzones.txt`): counts [1,2,3,4,5] per masked box
   (1+2+3+4+5 = the spec's 15 arrows), colors [magenta, red, blue, orange, dark-red],
   tiny solid tips + hairline washed stems — replaced my initial uniform 5× thick
   straight RGB arrows (crop-check MAJOR).
4. **Token-cell grids** on the five decoder strips (main-judge BLOCKER): tan rules
   (#C2B498) at y423.5/439 + six verticals at 12px pitch + outer rails to the purple bar.
5. **Y-group enclosure rectangle** (x57–295, y257–279) and **down-arrows** under the
   five top token groups (spec step 9).
6. **Chrome gate fix:** cream strip 5's right edge pulled from measured fx858 to fx839 —
   its antialiased edge (render x~1819) fell inside `house_chrome_check.py`'s badge
   window and tripped the yellow mask; documented in the build header.

## Overridden judge notes (documented, not fixed)

- Attempt-2 MAJOR 1 (~60%): "token cells inside the panel, arrows point up" — the pixel
  map shows the token squares at frame y54–67, ABOVE the container top border (y72–78);
  drawn as measured. The ~10px arrows' direction is not resolvable in the JPEG at judge
  confidence; measured geometry wins (fidelity law).
- Attempt-2 MAJOR 2 (~55%): "missing red arrows from I/feel/Sick to the token cells" —
  no such element in the pixel maps (would have to cross the Transformer Encoder box);
  no saturated red trace in y425–480 outside the word boxes. Treated as unconfirmed.
- Main-judge minor "FFN caption italic" (0.7/0.85): spec says bold white with Courier
  RELU; kept spec typography.
- Main-judge minor "stack/shadow simplified" (0.8) and crop-attempt-4 MEDIUM "3D offset
  outlines vs stripes": the masked-row crop check (2x, attempt 4) PASSED the stripe
  approximation after three prior fix rounds; left as the certified dense-region read.
- Attempt-1 "bottom containment" flag (0.35, self-unconfirmed): the original's lower
  container also abuts the slide bottom (measured y516); chrome check passes.

## Banking

No component export: slide 52 has NO dependents in either deck's dependency graph
(checked `slide_dependencies.json` of 002 and 001 — no `52`/`002:52` refs; not in any
pattern group). The banking obligation is vacuous for this slide.

## Process notes

- Judge procedure executed by the worker via Bash (no subagent-spawn tool in this
  environment) — orchestrator-approved fallback per `scripts/17_worker_instructions.md` §7.
- Gate probes hung 3× at the 120s wall (fleet congestion; peers' 420s-wall comparisons
  were landing concurrently) — proceeded to the wide-wall comparison per the storm
  protocol; both judge comparisons landed first-try with zero degenerate events.
- Certificate: single-read, default route (`images`, no `--models`), glm leg
  DEFERRED/BLOCKED per the routing law; streaming; `--thinking high --max-tokens 65536`.
- Render lineage: renders 1–4 were pre-judge self-check/crop iterations of the same
  build lineage; the certifying judge saw render_5.png (attempt 2).

---

## APPEND — second dispatched worker (verification + double-dispatch record), 2026-10-12 ~10:00

A SECOND worker instance was dispatched for this same slide (orchestrator double-dispatch
after the "builder died on provider timeout — reset for re-dispatch" reset; the first
builder had in fact survived and kept building). To avoid corrupting a live worker's
artifacts, the second instance YIELDED the build and acted as an independent monitor +
verifier. Its contributions, all read-only on shared artifacts:

- **Independent PIL measurement of the original frame** (own scratch files:
  `scratch/slide052/worker2_render2_pil_check.txt`, crops `crop_kvq/callouts/leftpanel/
  right_out/lower_left/lower_right.png`): confirmed the slide-002 chrome transform
  (`sx=(fx-18.63)/0.96123, sy=fy/0.95556`), the measured element geometry (containers,
  bars, token columns, K/V rails exiting right as the pink/green arrows, cream columns,
  Q letters), and the washed color cores. Independently found the same two facts the
  primary builder used for its judge-note overrides: token squares sit ABOVE the upper
  container's top border (frame y54..68 vs top y72), and there is NO red word->cell arrow
  ink above the I/feel/Sick boxes.
- **Independent verification of the certified state:** `house_chrome_check.py` PASS run
  by the second instance on `render_2.png`, `render_4.png` and the certifying
  `render_5.png`; PIL color-region check of render_2 vs original 10/12 (both "fails"
  were the checker's own probe points landing on matching text ink in both images).
- **No shared artifact was written by the second instance** (no DB writes after the
  primary took over; no build/render/judge interference). My own early crop-vision batch
  died on the congested fleet gate (HangError at the 270s wall) and was abandoned rather
  than compete with the primary's judge traffic.

Second-instance verification of the certificate: `judge_attempt_2.txt` is a substantive
element-by-element comparison body (grounded in IMG1/IMG2, attempt-5-specific content);
`FINAL VERDICT: PASS` present; `house_chrome_check.py` PASS on render_5; deliverable
`slide_052_recreated.pptx` (09:50:20) matches render_5's build; DB row
`gen_status=passed, visual_check=PASS, visual_attempts=2,
visual_transcript=.../judge_attempt_2.txt`. One formality gap, recorded for the record:
the two judge transcripts bank body-only text (no `[winner]`/`models:` header lines and
no probe transcripts banked) — the verdicts are substantively real comparison reads but
do not carry the §V winner-marker header. Certification stands on the DB fields above.

---

## APPEND — third dispatched worker (independent verification; no rebuild), 2026-10-12 ~11:00

A THIRD worker instance was dispatched for this same slide with the same stale premise
("two previous builders died BEFORE producing anything — row reset; no artifacts"). The
filesystem and DB disproved that premise on arrival (this report, the full evidence trail,
and the certified DB row all predate the dispatch), so per the resume rule and the
never-delete-evidence law this instance did NOT rebuild, touch any shared artifact, or
write the DB. It ran its own independent verification instead; all outputs banked as
`worker3_*` files in this dir:

1. **Certifying transcript read in full by the third instance** (`judge_attempt_2.txt`):
   a substantive element-by-element comparison body (ground rules acknowledged, IMG1/IMG2
   grounded, attempt-5-specific content) ending `FINAL VERDICT: PASS` — two MAJOR notes at
   ~55–60% confidence are the ones the primary builder already measured-and-overrode
   (documented above). Attempt 1 (`judge_attempt_1.txt`) is a real FAIL body (missing
   decoder-column token strips, BLOCKER) — the fail-then-fix-then-pass loop is genuine.
2. **Chrome gate re-run by the third instance**: `house_chrome_check.py` on the certifying
   `render_5.png` → **PASS** (panel x 89–1913, y 95–bottom; badge center (1860,148) d=70,
   all within tol 8) — banked as `worker3_chrome_check_render5.txt`.
3. **Build/deliverable integrity**: `build/slide_052.js` is byte-identical to the banked
   `build_attempt_2.js`; `slide_052_recreated.pptx` passes `unzip -t`; the build contains
   **zero `addImage` calls** (pure shapes) — no LibreOffice red-"Image 0 1"-placeholder
   exposure on this slide.
4. **Independent PIL corroboration** (`scratch/slide052/worker3_pil_check.py` +
   `qa/.../worker3_pil_check_out.txt`): same-content-point sampling through the measured
   capture transform (frame→slide `sx=(fx−18.63)/0.96123, sy=fy/0.95556`) shows
   orig≈render hue agreement at every saturated point (white/white, FFN-green/green,
   dark-red/red, blue/blue at three row points, purple/purple at the word-row line,
   cream/cream container fill); the original's JPEG-washed cores explain the saturation
   deltas (spec hexes are the hashed/cleaned values per deck color law). Corroboration
   only — the certifying evidence remains the judge comparison + chrome check.
5. **Dependency audit note for the founder (52←51 suggestion)**: the suggestion does NOT
   hold compositionally. Slide 051 = "Encoder – Decoder Transformer": title bar + two
   side-by-side rounded panels (peach encoder / orange decoder) + full-width black bottom
   bar. Slide 052 = no title bar; two STACKED containers (beige cross-attention+FFN over
   pink masked-self-attention) + a left encoder panel + two red callout boxes + the
   I/feel/Sick → SOS/Je/me/sens/malade walkthrough. No shared blocks, no shared geometry;
   the standalone build from this slide's own frame was correct. `slide_dependencies.json`
   has no edges or pattern groups touching 52 (re-verified), so no component banking
   obligation exists (consistent with the primary builder's finding).

**Status after the third instance: unchanged — certified.** DB row remains
`gen_status=passed, visual_check=PASS, visual_attempts=2,
visual_transcript=.../judge_attempt_2.txt`; deliverable
`recreated_pptx/slide_052_recreated.pptx`. The orchestrator's "reset" bookkeeping for this
slide is stale and can be cleared.
