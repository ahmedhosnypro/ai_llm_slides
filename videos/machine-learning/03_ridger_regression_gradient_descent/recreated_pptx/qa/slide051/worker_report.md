# Slide 051 — "Check Classes" (machine-learning/03_ridger_regression_gradient_descent)

Worker: `w051-finish-20261024` | frame: `unique_slides/slide_051.jpg` (960x540, 1px=1pt)
Claimed **with --force**: took over from `worker-fresh-051` (heartbeat 293m stale,
`visual_attempts=1`, `gen_status=building`).

## 1. TRIAGE of the prior lane's bank

Bank contents verified with md5/TZ=UTC stat (chain coherent: script 04:17:30 → pptx
04:18:22 → pdf 04:18:32 → render 04:18:38):

| artifact | md5 | state |
|---|---|---|
| `recreated_pptx/build/slide_051.js` | `60bd2f6d…` | reused as attempt 1 |
| `recreated_pptx/slide_051_recreated.pptx` | `4a0fc3a9…` | banked as attempt 1 |
| `qa/slide051/render_1.png` | `a207cd37…` | 2001×1125, currency confirmed |
| `qa/slide051/judge_prompt_1.txt` | `9387f5fb…` | byte-identical to Template A |

⚠️ **The prior report is WRONG.** It claims a "Stage 2b fix" rewrote all three matrices
as tall bracket pairs. The banked script still draws per-digit short round parens
(`"(" + v + ")"` at `build/slide_051.js:60-68, 161-170, 216-225`). `measurements_051.json`
contradicts the report too — it says `right_z_matrix.cells_in_parens: true` and reports
the sample brackets as "vertical strokes at sample x90/97", which is a mis-read:
x90/97 are the **edges of two different cells' strokes**, not a matched pair.

### Root cause of the mis-read
All three matrices in the original are **tall bracket column vectors** — one vertical
stroke pair per COLUMN spanning all rows of that column, with digits stacked BETWEEN
them. The prior worker's x90/97 finding came from a run-detection pass at threshold
`<130` on a JPEG frame, which bifurcated every bracket into two separate runs and hid
the real pairs; the real pairs only appear at threshold `<205`:

```
sample brackets  (frame px): (90,102) (111,124) (134,147) (156,170) (179,192) (202,214)
aug brackets            : (94,107) (115,128) (137,151) (160,173) (182,195) (205,218)
Z brackets              : (598,612) (621,634) (643,656)
```
Left-to-right pairing is decisive proof: the first stroke of pair *k+1* always falls
between the two strokes of pair *k*, and every pair's interior holds exactly the digit
lines measured independently (sample y80..88 / y96..105; aug y184..192/199..207/214..222;
Z y83..91 / y99..107). A per-row `(v)` glyph layout cannot produce this.

### Defect title (measured on the banked render_1.png)
Every one of the 15 bracketed cells rendered as a **short round paren around a single
digit** — a delimiter that does not span its enclosed lines. Protocol clause (7) makes
this MAJOR. Measurement (`scripts/judging.md` "before you edit" order run first — the
comparison below is the defect measurement):

```
cell interior ink ratio, banked render_1 vs original (thr<170):
  sample_col1 0.535   Z1 0.667   sample_col4 0.791
  ... all 15 below 1.0, none above 1.10 — the render has LESS ink, because a
  10pt "(1)" glyph is far lighter than a 1px vertical stroke 25-43px tall.
```

## 2. REBUILD (attempt 2) — `build/slide_051.js`

Rewrote the three matrices as tall bracket column vectors via one helper
(`bracketColumn(L, R, yTop, yBot, vals, digitCentres, opts)`) that draws two
straight vertical strokes spanning ALL enclosed lines and centres each entry in the
interior (`build/slide_051.js:66-89`). Geometry — all measured in the previous
section, digit lines verified 1px-accurate against the frame.

The **Z matrix orientation is confirmed** by the decision rows, not by OCR:
`analysis/slide_051_final.json`'s "3 rows × 3 columns: Row1 (0)(0)(0) / Row2 (7)(6)(2) /
Row3 (3)(2)(2)" is a grid mis-read. The DEC interiors and the printed arithmetic both
require `Z1=(0,0)`, `Z2=(7,6)`, `Z3=(3,2)` — three 2-entry columns. The banked
attempt-1 build already had this right; it was kept.

### Verification of attempt 2 (all measured, not asserted)

| check | result |
|---|---|
| tall strokes, SAMPLE, render y78..106 | 12 strokes at x89.2/90.2/101.2/102.2/110.3/111.3/123.3/124.3/133.4/134.x/146.3/147.3/155.4/156.x/169.4/170.x/178.5/179/191.4/192/201.5/202/213.5/214 — **every bracket of the original present, h=59 render-px = 28.3 frame-px vs original 23-27** |
| tall strokes, Z, render y79.6..107.9 | 598/612, 621/634, 643/656 all present (original 598/612, 621/634, 643/656) |
| tall strokes, AUG, render y180.9..224.0 | 12 strokes at 94/107, 115/128, 137/151, 160/173, 182/195, 205/218 (original same) |
| sample digit values | 1,2,1,5,6,6 / 1,1,2,4,5,6 — **byte-correct on all 6 cells**, both rows |
| sample class tags | C1×3 at c96/117.5/140.5, C2×3 at c163/185.5/208, y113..123 |
| house_chrome_check.py render_2.png 51 | **PASS** (panel x112-1882; L/R/bottom strokes; top bare; badge (1824,152) d68) |
| frame containment (ink outside x54..903 / y45..540) | render **0 px** in every band; original 0 px |
| DEC card right edge (card x853) | ink beyond x854 is only the house right stroke at x901 (n_cols=2, same as original's x901) |
| red box / pale card geometry | x78..239 y277..305 and x68..720 y54..130, unchanged |

Deliverables:
- `recreated_pptx/slide_051_recreated.pptx` (md5 in the DB `set` calls below)
- `recreated_pptx/build/slide_051.js` (md5 `e213e905…`, 334 lines)
- `recreated_pptx/qa/slide051/render_2.png` (2001×1125, md5 `015c587b…`)
- banked attempt-1 copies: `qa/slide051/build_attempt_1_banked.js`,
  `slide_051_recreated_attempt_1.pptx`, `render_1_banked.png`,
  `judge_prompt_1_banked.txt` — **never delete**.
- crops at matched effective scale: `crop_2_{mats,aug,dec}_{render,orig}.png`
- payloads: `judge_attempt_2_promptA.txt` (Template A, byte-identical to the protocol),
  `crop_attempt_2_promptB.txt` (Template B, `slide NNN`→`slide051`)
- dispatch scripts: `dispatch_legA_attempt2.sh`, `dispatch_legB_attempt2.sh`

## 3. JUDGE LEGS — **PARKED, gateway congestion**

`pgrep -c -f analyze_image.py` before every probe:

| time (UTC) | procs |
|---|---|
| 11:12:38 | 10 |
| 11:16:50 | 13 |
| 11:22:40 | 24 |
| 11:31:42 | **28** (peak) |
| 11:40:42 | 24 |
| 11:46:59 | 20 |

Load peaked at 28 and is now draining monotonically. Per gate law (do not start a leg
at ≥8) no judge was dispatched yet and **no verdict exists for attempt 2**.
Nothing was fabricated; the row is left honestly `building`.

### Exact wall evidence
The analyzer's internal client wall is 600s (real judge) inside the gate's 1650s
wrapper, inside the 1700s outer `timeout`. With 28 concurrent analyzers on the shared
localhost:17844 gateway, a leg dispatched now would most likely die at the analyzer's
630s client wall or the outer 1700s wrapper — i.e. it would produce no verdict at all,
which is the same outcome as not dispatching but with a wasted attempt slot and no
evidence. The prior lane (`worker-fresh-051`) parked on exactly this condition.

## 4. RESUME — exact next commands (nothing else to decide first)

Run in this order, from `/home/ahmed/Projects/ai_llm_slides`:

```bash
# 0) Gate probe. Repeat until it prints 7 or less — do NOT dispatch at >=8.
while :; do n=$(pgrep -c -f analyze_image.py); echo "$(date -u +%H:%M:%S) procs=$n"; [ "$n" -lt 8 ] && break; sleep 240; done

# 1) Leg A (full-slide) — the ONLY mandatory leg; dispatch it first.
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 51 w051-finish-20261024
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide051/dispatch_legA_attempt2.sh
```

Then check `judge_attempt_2.txt` (or re-cut from a newer render) and, per the protocol's
cert law, re-run **both** legs from the same render (crop pairs must be re-cut after any
rebuild):

```bash
# 2) Leg B (zoomed crop-pair certificates) — one per dense region.
while :; do n=$(pgrep -c -f analyze_image.py); echo "$(date -u +%H:%M:%S) procs=$n"; [ "$n" -lt 8 ] && break; sleep 240; done
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide051/dispatch_legB_attempt2.sh
```

On a clean **FINAL VERDICT: PASS** in `judge_attempt_2.txt` **and** every crop
transcript (or a PIL-refutation record banked for each finding):

```bash
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
python3 scripts/15_progress.py set 51 pptx_path videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_051_recreated.pptx --worker w051-finish-20261024
python3 scripts/15_progress.py set 51 build_script videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_051.js --worker w051-finish-20261024
python3 scripts/15_progress.py set 51 visual_check PASS --worker w051-finish-20261024
python3 scripts/15_progress.py set 51 visual_transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide051/judge_attempt_2.txt --worker w051-finish-20261024
python3 scripts/15_progress.py set 51 visual_attempts 2 --worker w051-finish-20261024
python3 scripts/15_progress.py set 51 gen_status passed --worker w051-finish-20261024
python3 scripts/15_progress.py heartbeat 51 w051-finish-20261024
python3 scripts/15_progress.py release 51 w051-finish-20261024
# 3) RE-READ the row: claim()/set() can reset gen_status (15_progress.py:337-339).
#    The final row MUST read gen_status=passed AND visual_check=PASS AND worker_id="".
$VIDEO python3 scripts/15_progress.py get 51
```

If a leg FAILs, PIL-adjudicate every finding against BOTH images before editing
(`scripts/judging.md` order), fix only real defects, re-render as `render_3.png`,
re-cut the crops, and re-run **both** legs. Never edit geometry on a finding the
original already satisfies.

## 5. What is NOT done (honest)
- No judge was run; no transcript, no FINAL VERDICT, no `visual_check`.
- Row 51 remains `gen_status=building`, `worker_id=w051-finish-20261024`
  (heartbeat alive; claim not released — it will auto-take-over after 40 min).
- `visual_attempts` stays 1 (no leg was dispatched), but the build is already at
  attempt 2 and `render_2.png` is the artifact the resume commands above judge.

---

# RESUME LOG — 2026-10-24 (worker `w051-finish-20261026`)

## Timeout-resume history (this worker, third run)

| run | claimed as | outcome |
|---|---|---|
| 1 | `w051-finish-20261024` @ 11:12 | triaged bank, proved the prior report false, rebuilt attempt 2, banked crops/payloads, then **parked on gateway congestion** — never dispatched a leg |
| 2 | (heartbeat went stale 11:40) | no legs dispatched |
| 3 | `w051-finish-20261026` @ 15:07 (re-claimed) | legacy transcript adjudicated invalid; gate cleared to 5 procs; **Leg A dispatched** |

## Validity ruling on the LEGACY transcript (orchestrator question 1)

`qa/slide051/judge_attempt_2_promptA.txt` is **NOT a verdict — it is a payload
template. It does not satisfy Leg A, and neither leg is discharged.**

Proof (three independent checks):

1. **Content** — it opens with `GROUND RULES (founder-mandated, settle these FIRST
   and never raise them as discrepancies): (a) The recreation uses a house template…`
   and closes with the *imperative instruction* `… End with: FINAL VERDICT: PASS or
   FAIL for 'faithful, usable recreation'.` Its single `FINAL VERDICT` occurrence is
   the **instruction to emit one**, not the line itself. It contains no findings list,
   no per-item severities, no model reasoning — i.e. no analyzer stdout.
2. **Size / shape** — 4139 bytes, **0 newlines** (`wc -c -l` → `4139 0`): one long
   line. An analyzer transcript is multi-line prose. (`wc -c -l` proves this; the
   `1` a naive `grep -c FINAL VERDICT` returns comes from that one instruction.)
3. **Identity** — md5 `9387f5fbb94ef05a31db19f1e018dde1`, **byte-identical** to
   `qa/slide051/judge_prompt_1.txt`, which the prior lane generated itself from
   `shared_patterns/judge_protocol_03.md` line 71. So the file is the Template A
   payload as extracted, i.e. the `-p` argument, not the output.

Conclusion: this file was created at 11:10 by run 1 as the Leg-A payload
(`judge_attempt_2_promptA.txt`), never renamed to a transcript name, and **no
analyzer ever ran for slide 051 on either attempt**. There is no legacy comparison
verdict to reuse. Both legs remain due, and `visual_check` stays null.

## Build currency (verified, not asserted)

- DB row 51: `gen_status=building`, `pptx_path`/`build_script` both point at the
  attempt-2 artifacts, `visual_check=null`, `visual_attempts=1`, worker
  `w051-finish-20261026`.
- `recreated_pptx/build/slide_051.js` md5 `e213e905ee6d5368a5ed6e6707c4ff93`
- `recreated_pptx/slide_051_recreated.pptx` md5 `8af978080e6ae77f9b7910920140b99e`
- `recreated_pptx/qa/slide051/render_2.png` md5 `015c587b20449c62ff8c1e88e24f67bd`
  (2001×1125). Independent re-render of the current pptx (private LO profile
  `file:///tmp/lo_w051_v`, `soffice --convert-to pdf` → `pdftoppm -png -r 150`)
  is **pixel-identical to render_2** — `ImageChops.difference(...).getbbox()` is
  `None`, md5 `cd88cb66435ffb2f95b2b05f32454199`. Build/render currency proven.

## Gate evidence (2026-10-24)

Load oscillated 9–49 procs for ~3 h (peaks 48–49, troughs 5–9). `ps -eo etimes`
diagnosis: one **wedged analyzer at 5657 s (94 min)** that never exited, plus a
steady 10–16 healthy jobs (260–990 s) that other lanes kept refilling the 16-slot
flock with. The fleet pgrep of 40–42 referred to in the 043 evidence was not
reproduced here, but the same wedge behaviour was: the pool stuck at 11–20 while a
single stale job held a slot. Gate law was honoured throughout: no leg was
dispatched at ≥8. `pgrep` before every dispatch.

## Legs dispatched this run

| leg | script | wall | state |
|---|---|---|---|
| A — full-slide comparison | `dispatch_legA_attempt2.sh` | `timeout 1700`, analyzer `--timeout 1200` | **dispatched 15:07** → `qa/slide051/judge_attempt_2.txt` |
| B — crop pairs (mats/aug/dec) | `dispatch_legB_attempt2.sh` | same | pending after A |

Payloads, byte-for-byte and never retyped:
- `judge_attempt_2_promptA.txt` — Template A verbatim (no `\bK\b`, no `NNN` in
  Template A), md5 `9387f5fbb94ef05a31db19f1e018dde1`.
- `crop_attempt_2_promptB.txt` — Template B with the single permitted substitution
  `slide NNN`→`slide051` (no `\bK\b` in Template B). 1914 → 1913 chars, delta −1,
  `\bK\b`-token assertion passed, md5 `6ae2c27e0ac3c7f3716ae50f823ebb25`.

Crops at matched effective scale (render `x*2001/960, y*1125/540`; original
LANCZOS to identical output size — verified `render_banked_ok=True,
orig_banked_ok=True` for all three, i.e. they are cut from the current render_2):

| crop | frame bbox | output px | region |
|---|---|---|---|
| `crop_2_mats_*` | x78..668, y58..132 | 1230×154 | top band: sample 2×6 matrix + centre W/η/legend + Z matrix |
| `crop_2_aug_*` | x78..230, y140..250 | 317×229 | augmented 3×6 matrix + C1/C2 row |
| `crop_2_dec_*` | x276..862, y138..335 | 1221×410 | three d(Zn) decision rows |

## Resume / park commands (if this run ends with legs still open)

```bash
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
D="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide051"

# gate probe — must print < 8
pgrep -c -f analyze_image.py

# Leg A (full-slide)
bash "$D/dispatch_legA_attempt2.sh"

# Leg B (three crop pairs)
bash "$D/dispatch_legB_attempt2.sh"
```

On PASS of A and every crop: certify with `set 51 visual_check PASS`,
`set 51 visual_transcript $D/judge_attempt_2.txt`,
`set 51 visual_attempts 2`, `set 51 gen_status passed`, `heartbeat`,
`release 51 w051-finish-20261026`, then re-read `get 51` (claim()/set() can reset
gen_status, 15_progress.py:337-339).
