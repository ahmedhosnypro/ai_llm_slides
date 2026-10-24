# Slide 045 worker report — "legs-on" judge run (worker-fresh-045-legs)

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent`
Deliverable: `recreated_pptx/slide_045_recreated.pptx`
DB row: 45 — see the FINAL DB ROW section below.

## Status: IN PROGRESS — BLOCKED BY FLEET-WIDE GATEWAY STALL (as of 2026-10-24 08:2x UTC)

**No judge leg has a verdict transcript.** Template A was dispatched once and hung to
its outer wall; the protocol-sanctioned hard-wall retry was also lost to a router abort.
Two probes hung as well. The build, render, crop pairs and all payloads were re-verified
current THIS run — nothing needs rebuilding, re-rendering, or re-cutting.

## What this run verified fresh (all green)

Inputs were re-checked before any dispatch, because the task brief for this run
referenced artifacts that do not exist for slide 045 (see "NOMENCLATURE" below).

### NOMENCLATURE CORRECTION (important for the next worker)

The task brief for this run said "`render_6.png` is the current render" and
"`qa/slide045/worker_report.md`" at the namespace root, with "three Procedure B crop
pairs … banked scales 2.0812–2.0857". **None of those match the on-disk state.**

- `render_6.png` is slide 047's / slide 049's banked render — there is NO render_6.png
  under `recreated_pptx/qa/slide045/`.
- The worker report has always lived at `recreated_pptx/qa/slide045/worker_report.md`
  (this file), not at `qa/slide045/` (that only holds `slide013` today).
- The current Procedure B pairs carry the `_r2` suffix (`crop_1_r2_<name>_*`), scales
  2.0833–2.0840.

The currency-correct render for slide 045 is **`render_1.png`** — re-proven below.

### 1. Render currency (re-proven, 3-way md5)

Independent re-render this run: copied the on-disk pptx to
`scratch/tmp/045legs/`, `soffice --headless --convert-to pdf`, `pdftoppm -r 150 -png`:

```
md5(scratch/tmp/045legs/fresh-1.png)       = c41a7a11c8f8976bbfc31cadef99c0b1
md5(recreated_pptx/qa/slide045/render_1.png) = c41a7a11c8f8976bbfc31cadef99c0b1
md5(recreated_pptx/qa/slide045/verify2/r150-1.png) = c41a7a11c8f8976bbfc31cadef99c0b1
```

All three identical (169,129 B each). `render_1.png` IS the render of the shipped pptx;
the LO → PDF → 150dpi pipeline is deterministic for this build. Evidence:
`recreated_pptx/qa/slide045/render_currency_legsrun.txt`.

### 2. Build currency

```
md5(recreated_pptx/build/slide_045.js)          = 9ca5e8eb04cbd3ccd3442888104f63d8
md5(recreated_pptx/qa/slide045/build_attempt_2.js) = 9ca5e8eb04cbd3ccd3442888104f63d8
```

The shipped build script matches the last-supplied attempt-2 source. No rebuild needed.

### 3. House chrome (fresh run, on the verified render)

`python3 videos/.../shared_patterns/house_chrome_check.py <render_1.png>`:

```
HOUSE CHROME CHECK: PASS (panel x 112-1882, y 94-bottom; strokes L/R/bottom present,
top bare; badge center (1824,152) d=68; all within tol 8)
```

At 150dpi that is frame px x54..903 / y45..540 panel, C00000 strokes on LEFT x58.5,
RIGHT x901, BOTTOM y538.5 only (top bare, as mandated), badge centroid
(876, 72) frame px d≈32.6 — the FDFD96 fill with 6A5ACD ring is confirmed in
`scratch/tmp/adjudicate_045_legs.py badge`, which measures the ORIGINAL badge at
centroid (876.4, 73.5) d≈32.5. Both images agree; no defect.

### 4. Crop-pair currency (re-produced byte-identically)

Re-ran `build_crops_r2.py`'s exact logic against the verified render and md5-compared:

```
calcs     frame x266..861 y131..536 (595x405) -> 1240x844 | scale r=2.08403 o=2.08403 | both match
toppanel  frame x60..727  y46..137  (667x91)  -> 1390x189 | scale r=2.08396 o=2.08396 | both match
augtable  frame x62..254  y132..263 (192x131) ->  400x273 | scale r=2.08333 o=2.08333 | both match
```

All six files reproduce byte-for-byte from render_1.png. Evidence:
`recreated_pptx/qa/slide045/crop_payload_verification_legsrun.txt`.

### 5. Payload legality (re-derived byte-for-byte, not re-typed)

All four `-p` payloads re-derived from `shared_patterns/judge_protocol_03.md`
(fenced block [2] = Template A comparison, block [3] = Template B crop; NNN=045, K=1,
NAME + region description substituted only) and md5-compared:

```
judge_prompt_1.txt           md5 9387f5fbb94ef05a31db19f1e018dde1  MATCH (4115 chars)
crop_prompt_1_r2_calcs.txt   MATCH (1914 chars)
crop_prompt_1_r2_toppanel.txt MATCH (1914 chars)
crop_prompt_1_r2_augtable.txt MATCH (1914 chars)
```

No placeholder leftovers; the banked payloads are protocol-legal and were NOT edited.
The payloads contain no double quote / backslash / backtick / `$` and no trailing
newline, so `-p "$(cat FILE)"` delivers them verbatim.

## Verdict transcripts banked (the audit list)

NONE — for ANY run. Only prompt TEMPLATES contain the words `FINAL VERDICT:` (as
instruction text): `judge_prompt_1.txt`, `crop_prompt_1_augtable.txt`,
`crop_prompt_1_calcs.txt`, `crop_prompt_1_r2_augtable.txt`, `crop_prompt_1_r2_calcs.txt`,
`crop_prompt_1_r2_toppanel.txt`, `crop_prompt_1_toppanel.txt`. None of those is a
verdict; every one of them is a payload. No transcript with an actual verdict body
exists under `recreated_pptx/qa/slide045/`.

Verdict files owed, once the gateway drains:
- Template A full-slide: `judge_legs_next.txt`
- Procedure B crop pairs: `crop_calcs_judge_next.txt`, `crop_toppanel_judge_next.txt`,
  `crop_augtable_judge_next.txt`

## Judge legs — dispatch log

| # | When (UTC) | Leg | Outcome |
|---|---|---|---|
| 1 | ~07:12–07:42 | Template `analysis` probe (120s) on render_1.png | HangError 150s, no transcript |
| 2 | ~07:07–07:42 | **Template A comparison** render_1 vs original | 2× HangError 630s, outer wall 1700s, no transcript |
| 3 | 07:48–07:51 | probe re-attempt on `crop_1_r2_augtable_render.png` after `sleep 240` drain | HangError 150s, no transcript |
| 4 | 07:52–08:20 | **Template A hard-wall retry** (the one W4 sanctioned retry) | attempt 1 GarbageError (infinite/looping repetition in thinking stream), attempt 2 HangError 630s, outer wall 1700s, no transcript |
| — | — | Procedure B crop-pair legs (3) | blocked behind Template A; not started — no dispatch budget left after the retry |

Both Template A images are the correct ones: IMG1 = `render_1.png` (md5-verified current
150dpi PNG render of the shipped pptx); IMG2 = `unique_slides/slide_045.jpg` (960×540).

Raw wrapper logs are banked in `gate_logs/gate_legs_attempt1.log` with the exact abort
signatures plus the fleet state.

## Gateway blocker (why no verdict yet)

Fleet-wide router stall, identical in signature to the prior lane's blocker:

```
07:42 procs=15 | 07:47 procs=15 | 07:51 procs=17 | 08:04 procs=24 | 08:16 procs=33 | 08:21 procs=25
ironrouter pid 3035: ELAPSED 5955s+ CPU 0.3% STAT Ssl
```

The router process is essentially IDLE (0.3% CPU) while 15–33 vision processes sit in
it — it is accepting requests and not completing them. Competitors in flight at the
same time: slide 049 (running 1608s+), slide 044, slide 019, plus lane sleepers on
016/046/009. This is not payload- or thinking-budget-related: the cheapest possible
probe (a small crop, `--timeout 120`, default thinking) also hangs, the full-slide
retry produced an infinite/looping-thinking GarbageError, and no lane completed a
judge during this worker's 85-minute watch window (06:56–08:21 UTC).

Congestion never dropped below the 8-process gate threshold at any sampling point in
this run, so every dispatch went out into an over-capacity fleet.

Attempt accounting for this run, per the protocol's garbage-re-invoke rules: **0
coherent verdict bodies** produced, so 0 attempts consumed against the 6-attempt
budget. The Template A hard-wall HangError retry is protocol, not an attempt.

## Content fidelity baseline (no vision needed) — from the prior lane, still valid

`recreated_pptx/qa/slide045/content_check_045.out`: 221 text runs extracted from the
shipped pptx, 29 of 30 spec strings present. The single "MISSING" entry
(`Check classes of [0 7 3; 0 6 2] with column labels Z₁ Z₁ Z₁`) is a spec-form
artifact — the pptx holds those as separate runs (`Check classes of`, `Z 1 Z 1 Z 1`,
`(0) (7) (3)`, `(0) (6) (2)`), exactly as the frame renders a label + a 2×3 table.
All six calculation rows carry the verbatim
`d(xᵢ) = […] = <value> ⇒ Keep same Weight W = [14; -4; 0]`; badge numeral `45` present.

Also still banked and valid: `measurements_adjudicate_r2.txt` (`mean|diff|=12.71`;
the only red px in the top band are the two mandated vertical-stroke tops at x=58 and
x=900, hence **no top stroke — not a defect**), `selfcheck_attempt_1.txt` (43/43 PASS),
`adjudicate_calc_1.py/.out`, `metrics_1.py/.out`, `bands_final.py/.out`.

## Banked evidence added by THIS run

- `recreated_pptx/qa/slide045/render_currency_legsrun.txt` — 3-way md5 proof + nomenclature correction
- `recreated_pptx/qa/slide045/crop_payload_verification_legsrun.txt` — crop reproduction + payload legality
- `recreated_pptx/qa/slide045/gate_logs/gate_legs_attempt1.log` — abort signatures + fleet state
- `recreated_pptx/qa/slide045/adjudicate_045_legs.py` + `adjudicate_all_legs.out` — PIL-first
  adjudication helper and its output on all four regions (badge / redframe / calcs /
  toppanel / augtable) measured against BOTH images
- `scratch/tmp/adjudicate_045_legs.py` — PIL-first adjudication helper (badge / redframe / calcs / toppanel / augtable) for the next worker
- `scratch/tmp/045legs_dispatcher.sh` — Procedure B sequential dispatch script with gate law + heartbeats built in
- `scratch/tmp/045legs/` — the fresh LO→PDF→150dpi render chain used for the md5 proof

## FINAL DB ROW

- `gen_status`: building (not yet passed)
- `visual_check`: null
- `visual_transcript`: null
- `worker_id`: worker-fresh-045-legs (claimed 2026-10-24 06:56, heartbeated through 08:16+, released 08:2x with `gen_status` unchanged)
- `last_error`: set this run with the full honest blocker summary and a pointer to this report.

**Not finished.** Both judge legs must run and be clean (or findings PIL-adjudicated)
before `visual_check=PASS` + `gen_status=passed` + release. This worker left the row in
`building` with the claim released, per the protocol's "never silently drop" rule —
the row is honestly parked with a live resume recipe, not failed.

## RESUME INSTRUCTIONS for the next worker

Nothing needs rebuilding or re-rendering. Every input is md5-verified current:

```bash
cd /workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
VIDEO=machine-learning/03_ridger_regression_gradient_descent \
  python3 scripts/15_progress.py claim 45 <your-worker-id>
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045

# 0. Read this report + render_currency_legsrun.txt + crop_payload_verification_legsrun.txt.

# 1. GATE LAW (mandatory before EVERY vision call): if the fleet is saturated,
#    heartbeat + sleep 240 and re-probe. Never retry-loop a vision call.
c=$(pgrep -c -f analyze_image.py)
echo "fleet procs: $c"          # want < 8 before a real judge

# 2. Template A — payload from $Q/judge_prompt_1.txt (md5 9387f5fbb94ef05a31db19f1e018dde1)
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_1.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_045.jpg \
  --view "Slide 045 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript $Q/judge_legs_next.txt -p "$(cat $Q/judge_prompt_1.txt)"

# 3. Procedure B — three pairs already cut at matched scale (or use the banked script):
#    bash scratch/tmp/045legs_dispatcher.sh        # sequential, gate-aware
#    Otherwise, per leg:
for n in calcs toppanel augtable; do
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/crop_1_r2_${n}_render.png $Q/crop_1_r2_${n}_orig.png \
    --view "Slide 045 zoomed crop $n — render vs original at matched scale" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    --transcript $Q/crop_${n}_judge_next.txt -p "$(cat $Q/crop_prompt_1_r2_${n}.txt)"
done
```

**Do NOT re-cut crops, do NOT re-render, do NOT rebuild.**

Adjudicate any FAIL/MINOR PIL-first against BOTH images before touching the build —
`recreated_pptx/qa/slide045/adjudicate_045_legs.py <region>` (or the scratch copy)
prints the measurements. Known refutation material already banked: no-top-stroke
(`measurements_adjudicate_r2.txt`), the `[0 7 3; 0 6 2]` spec-form artifact
(`content_check_045.out`), typed-vs-handwritten (GROUND RULES clause (d)), and
linear-vs-2D equations (clause (e)) are all protocol-mandated non-discrepancies.
