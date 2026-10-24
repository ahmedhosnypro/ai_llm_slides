# Slide 003 worker report — resume lane (worker w003-root-20261024)

Slide: `videos/machine-learning/03_ridger_regression_gradient_descent` slide 003
(house-frame REFERENCE slide — the deck's outer template was measured from it).
Title: "Matrix Notation for Linear Regression and Classification (N- Samples)".

## What I did

1. **Claimed** slide 3 as `w003-root-20261024` (auto-took-over the stale
   `worker-fresh-003b`, heartbeat 75m).
2. **Verified the previous lane's build reproduces**: rebuilt from
   `build/slide_003.js`, converted with LibreOffice → PDF, rasterised at 150dpi
   (2001×1125) with `pdftoppm -r 150`. The fresh render was **pixel-identical
   (max diff 0)** to banked `render_8.png`. Banked as `render_9.png`; banked a
   pptx copy as `pptx_bank_w003resume.pptx`.
3. **PIL-first adjudication** against `unique_slides/slide_003.jpg` with 9 banked
   measurement scripts. Found 6 real defects (all measured, see below), fixed
   them copy-then-modify, and re-measured after each rebuild.
4. **house_chrome_check PASS** on every render (9/10/11/12/13/14/15).

## Lineage (previous lane, banked — never deleted)

- renders 1-4: chrome FAILs (bogus badge cy, Remember box occluding badge) — fixed.
- attempt-5/6/7 judge verdicts judged a STALE render (proven by PIL:
  `adjudicate_6.py`); take-6 adjudication settled each claim against the ORIGINAL
  and rebuilt as attempt 8 (banked `build_attempt_8.js`).

## Defects I found (PIL, matched-scale) and FIXED

| # | defect | measured (ORIG → REN before) | fix |
|---|---|---|---|
| 1 | title too small | cap 16.8px → 15px @21pt; ink w 744 → 693 | 21pt → **23pt**, box 752→800px wide (advance 761.8px so no wrap). Now cap 15.8px, ink w 743 (ratio 1.05) |
| 2 | top-box entries too small / sparse | zone ink 2624 → 536 @8pt; only 2 of 4 rows | each entry its own text box @11pt at measured rows y160/189/226/243 (LO ignores lineSpacing on inline runs). Now ink 1330, 4 rows present |
| 3 | top-box column brackets missing | bar ink 186px at x296..298 | tall vertical lines drawn at x331.5/414.5/556.5 spanning y155..259 |
| 4 | X_1/X_2/X_n headers too small | glyph h 19.7px → 14.4px @13pt | 13pt → **18pt** (height now 19.7px both) |
| 5 | red y-labels too small | glyph h 16.3 → 11.0 @11pt | 11pt → **12pt** |
| 6 | br-box `Y=XW` + Where lines too high | Y glyphs y360..371 vs REN y348..353; where1 y382 vs 397 | Y=XW moved to y365; where1 to br_y+74, where2 to br_y+120 (ratios now 3.14→1.01 on where1) |
| 7 | arrow head wrong shape | original: thin line x531..533 + head x569..572 y402..407 | re-anchored line x532 w40 |

Note on #7: the original's arrow is a thin gray line whose head is a small tab
at x569..572 y402..407; the tall chevron earlier builds drew was wrong.

## Attempt artifacts (banked in this dir)

- builds: `build/slide_003.js` (current); pre-change banks
  `build_attempt_8.js` (previous lane), `build_attempt_10.js` (mine)
- pptx: `recreated_pptx/slide_003_recreated.pptx` + `pptx_bank_w003resume.pptx`
- renders: `render_9` … `render_15.png` (150dpi, 2001×1125)
- crops for leg B (matched eff scale 2.0833): `crop_15_{matrix_stack,eq_bl,eq_br,side_boxes}_{render,orig}.png`
- tools: `crop_attempt_14.py` (parameterised to any render_K), plus the resume
  measurement scripts listed below

## Judge legs — leg A dispatched, leg B pending

Protocol: `shared_patterns/judge_protocol_03.md` Template A (full-slide) +
Procedure B (crop-pair) via `scripts/16_vision_gate.sh` with
`--thinking high --max-tokens 65536` inside `timeout 1700`.

- **Probe**: hung at the 150s wall (gate held 21-41 concurrent calls all
  session). Per protocol: sleep 300, re-probe once.
- **Leg A** (Template A, K=16): dispatched as a background task against
  `render_15.png` with the byte-verified payload `judge_prompt_14.txt`
  (NNN/K substituted; verified byte-identical to the protocol template).
  Transcript target `judge_attempt_16.txt`. NOTE: an earlier dispatch
  (`judge_attempt_15.txt`) was killed by the worker shell's own 600s timeout
  before the model returned — it produced NO transcript and was NOT a judge
  attempt; the protocol's `timeout 1700` wrapper is what governs, so the call
  was re-dispatched as K=16 with a longer shell budget.
- **Leg B** (Procedure B, K=15): 4 crop pairs cut (matrix_stack, eq_bl, eq_br,
  side_boxes) at matched effective scale; dispatch follows leg A.

## NEXT COMMANDS (exact, run from `/worksp/codespaces-blank/ai_llm_slides`)

```
# 1. leg A already dispatched. Read its transcript; only a real
#    "FINAL VERDICT:" line counts:
grep -i "FINAL VERDICT" videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/judge_attempt_15.txt

# 2. leg B — one call per crop pair, payload byte-for-byte from Template B
#    (substitute NNN=003, K=15, NAME=<region slug>; the region description for
#    each: matrix_stack = "top matrix-notation box: column headers, coloured
#    bands, entry stacks, ellipsis column"; eq_bl = "bottom-left expanded
#    equation box"; eq_br = "bottom-right compact form box with Where lines";
#    side_boxes = "Remember and In General annotation boxes"):
bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/crop_15_NAME_render.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/crop_15_NAME_orig.png \
  --view "Slide 003 zoomed crop NAME — render vs original at matched scale (attempt 15)" \
  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: <desc>" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/crop_15_NAME_judge.txt \
  -p "$(sed -n '/^GROUND RULES/,$p' <protocol Template B with NNN/K/NAME/desc substituted>)"

# 3. certify (only after BOTH legs PASS / are PIL-adjudicated):
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 3 visual_check PASS --worker w003-root-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 3 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/judge_attempt_15.txt --worker w003-root-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 3 gen_status passed --worker w003-root-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 3 w003-root-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py release 3 w003-root-20261024
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py get 3
```

## DB state

`gen_status=building`, `visual_attempts=3` (attempts 5/6/7 from the previous
lane; my judge attempts counted from 15 per the protocol's K = render index),
worker `w003-root-20261024`. No `visual_check`/`gen_status` change by me.

## Resume scripts banked

`measure_slide003_resume.py`, `measure2_slide003_resume.py`,
`calib_slide003_resume.py`, `probe_slide003_resume.py`,
`probe2_slide003_resume.py`, `runs_slide003_resume.py`,
`block_slide003_resume.py`, `ascii_slide003_resume.py`,
`textsize_slide003_resume.py`, `crop_attempt_14.py`.

---

# Attempt-19 judge/certify lane — worker judge-slide003-att19 (2026-10-24, 12:00-13:30 wall)

## State taken over
- DB row 3: `gen_status=building`, `visual_check=""`, `visual_attempts=18`,
  `worker_id=w003-fix-20261024` (claim --force takeover, heartbeat 24m stale).
- Fix lane claim `w003-fix-20261024` had banked the attempt-16 ellipsis fix and
  re-rendered, but hit the 2h wall with `visual_check=""` — nothing certified.

## 1. Render currency — PROVEN, not assumed
`render_16/17/18.png` all carry md5 `7afc5d9056ad725cbf7b6f5d9a29e20a`
(suspicious: three renders, one hash, three different timestamps 09:16/09:29/10:59).
Per the never-judge-a-stale-render law I did NOT trust them: copied the CURRENT
`slide_003_recreated.pptx` (126351 B, 10:59:33) to `scratch/tmp/r19`, converted
with `soffice --headless` (isolated profile) → PDF → `pdftoppm -r 150 -png`.
The fresh render is md5-identical to render_18 — LibreOffice's render is
deterministic, so **render_18 IS the current render of the current pptx** and the
10:59 pptx is byte-identical in rendering behaviour to the 09:16 one.
Banked as `render_19.png` + `render_19.pdf` + `currency_check_att19.txt`.

## 2. PIL-first adjudication of the pending defect — FIX CONFIRMED PRESENT
`judge_attempt_16.txt`'s real FAIL was "the bottom design matrix drops one
ellipsis cell in its middle row". Verified twice before spending any vision:

**(a) pptx ground truth** (`ppt/slides/slide1.xml` shape geometry, EMU→frame):
design-matrix row3 y=426.75 now carries FOUR ellipsis cells at exactly the same
four x as rows 1/2/4 (181.5 / 225.75 / 270 / 313.5); the weight vector at x=462
now reads `b(349.5) w1(387.75) w2(415.5) ...(453) wd(469.5)` — all lowercase w
with the ellipsis restored as the 3rd entry. Both attempt-16 defects are fixed
in the source.

**(b) rendered-pixel census** (`matrixprofile_att19.py`, `inkcells_att19.py`):
dark-ink (<100) per 3px band per matrix column, frame coords:

| | row1 | row2 | row3 | row4 |
|---|---|---|---|---|
| ORIG | 4/13/10/11 | 8/15/18/15 | 2/12/13/14 | 11/22/20/18 |
| RENDER_19 | 8/8/3/12 | 5/5/3/5 | **3/3/2/3** | 5/36/3/10 |

ORIG row3 carries ink in ALL FOUR columns; RENDER_19 row3 carries ink in ALL
FOUR columns — the 4-cell middle row now reproduces the original's structure
(full-res per-cell census: 10/10/10/10 dark px, four uniform ellipsis cells).
Weight vector full-res dark ink: b 150/93, w1 121/75, w2 126/37, ellipsis 20/24,
wd 355/67 — every cell including the ellipsis has ink.
Banked: `pil_ellipsis_evidence_att19.txt`.

## 3. Payload forensics — the attempt-16 leg ran a CORRUPTED payload
Extracted the frozen templates from `shared_patterns/judge_protocol_03.md` and
diffed every banked prompt: `judge_prompt_14.txt` (the payload behind
`judge_attempt_16.txt`) has **four `BLOC14ER`** where the protocol says
`BLOCKER` — a bare `s/K/14/` substitution hit the K inside BLOCKER, silently
deleting the BLOCKER severity class. `judge_prompt_8.txt` is byte-identical to
the protocol (clean); `judge_prompt_14_crop.txt` is likewise corrupted.
So attempt-16's verdict rests on a non-frozen payload. Banked:
`payload_corruption_evidence_att19.txt`; rebuilt clean payloads
`judge_prompt_19.txt` (4115 B, 4 BLOCKER, byte-identical to `judge_prompt_8.txt`)
and `judge_prompt_19_crop.txt` (1914 B, Template B with NNN→003 only).

## 4. Legs dispatched (attempt K=19, continuing the bank's numbering)
- **Leg A** — Template A, `render_19.png` vs `unique_slides/slide_003.jpg`,
  payload `judge_prompt_19.txt`, transcript `judge_attempt_19.txt`.
- **Leg B** — Procedure B crop pairs at matched effective scale (LANCZOS
  x H_render/540 = 2.0833, `cut_attempt_19.sh`): `crop_19_matrix`,
  `crop_19_topbox`, `crop_19_sideboxes`, `crop_19_bottomright`.
  Judging `crop_19_matrix` first (the densest region and the fixed one).

## House chrome
`house_chrome_check.py` on render_19: **PASS** (panel x112-1882 y94-bottom,
strokes L/R/bottom present, top bare, badge (1824,152) d=68, within tol 8).

## NEXT COMMANDS (exact, run from the project root)
```bash
# read the two in-flight transcripts (only a real "FINAL VERDICT:" line counts):
grep -i "FINAL VERDICT" videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/judge_attempt_19.txt
grep -i "FINAL VERDICT" videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/crop_19_matrix_judge.txt

# remaining leg-B regions, same payload (judge_prompt_19_crop.txt), each its own task:
#   topbox / sideboxes / bottomright  (crop_19_<name>_{render,orig}.png)
```

## 5. Vision legs — BLOCKED BY FLEET GATEWAY CONGESTION (PARKED, NOT CERTIFIED)

Five calls were dispatched this window; **none produced a FINAL VERDICT**:

| leg | task | outcome |
|---|---|---|
| A full-slide | bash-y8iejudv | killed by the harness's default 600s background-task cap at 600.252s, mid-request, no body |
| B matrix | bash-log092ps | same harness 600s cap, no body |
| re-dispatch A + B + topbox + bottomright (no harness cap) | bash-jqys564r / bash-53jsx6px / bash-5psebpvq / bash-oxdopuzj | all stopped on the script's **own** hard wall: `ABORT HangError: hard wall-clock 630s exceeded` (650-855s elapsed); no verdict, no attempt consumed |
| B sideboxes | bash-f7cruisa | transient upstream `HTTP 504 upstream_timeout` (Nvidia) — no body |
| final retry A + B matrix, `--timeout 1200` | bash-lk5c9li5 / bash-ko76qbf8 | STILL IN FLIGHT at park time; no body yet |

Fleet congestion throughout: 32-50 concurrent `analyze_image.py` processes
(measured at 24, 29, 38, 39, 44, 49, 50 across the window). The analyzer itself
warns at >600s: "the gateway at localhost:17844 is shared (Stitch proxy +
vision). Long-timeout retry loops SATURATE it for everyone — prefer one modest
call and retry later."

**No verdict was fabricated.** Per the standing law the row is left
un-certified: `visual_check=""` (untouched), `gen_status=building`,
`visual_attempts=18` (unchanged — no judge attempt completed). The claim is
left held by `judge-slide003-att19` with the last heartbeat stamped; it will go
stale within 40 min and the next worker takes it over cleanly with
`claim 3 --force`.

## 6. NEXT COMMANDS (exact, run from the project root)

```bash
# the two in-flight tasks may still land transcripts; check first:
grep -i "FINAL VERDICT" videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/judge_attempt_19.txt
grep -i "FINAL VERDICT" videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/crop_19_matrix_judge.txt

# if the gateway has cooled (pgrep -c -f analyze_image.py < 8), re-run Leg A at the
# protocol default --timeout 600 (payload already byte-verified and banked):
bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/render_19.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg \
  --view "Slide 003 recreation attempt 19 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/judge_attempt_19.txt \
  -p "$(cat videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/judge_prompt_19.txt)"

# then the crop pairs, two at a time (4 are already cut, at matched 2.0833 scale):
#   crop_19_matrix / crop_19_topbox / crop_19_sideboxes / crop_19_bottomright
#   payload: judge_prompt_19_crop.txt  (Template B, NNN->003, byte-verified)
```

## 7. What is already PROVEN and needs no re-verification by the next worker
- `render_19.png` IS the render of the current pptx (deterministic re-render,
  md5-identical to render_18). Do not re-render unless the pptx changes.
- House chrome PASS on render_19.
- The attempt-16 ellipsis defect is FIXED and visible in the render, verified
  twice (pptx shape geometry + rendered-pixel census). No rebuild is needed on
  its account.
