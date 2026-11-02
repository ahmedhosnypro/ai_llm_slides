# preflight_r2.md — Phase-4 closeout gate preflight, deck 03 (2026-11-01)

Read-only preflight for the runbook in `PHASE4_RUNBOOK.md`. NS =
`videos/machine-learning/03_ridger_regression_gradient_descent`,
RJ = `recreated_pptx/qa/rejudge_20261027`, OUT = `$RJ/closeout_pack`.

## 1. Tool availability (all commands in the runbook)

| Tool | Status | Version / path |
|---|---|---|
| soffice | OK | LibreOffice 24.2.7.2 420(Build:2), `/usr/bin/soffice` |
| pdftoppm | OK | `/usr/bin/pdftoppm` |
| pdfinfo | OK | `/usr/bin/pdfinfo` (used by render_check_pages.py) |
| sqlite3 (CLI) | OK | `/opt/conda/bin/sqlite3` |
| python3 | OK | 3.15.2 (pyenv shim) |
| md5sum | OK | `/usr/bin/md5sum` |
| python3 stdlib (json, hashlib, sqlite3, zipfile, re, datetime) | OK | sqlite 3.45.1 |
| PIL (Image, ImageChops) | OK | PIL 13.0.0 |

No missing tools. `render_check_pages.py` needs no flags support (`--help`
crashes it — positional pages only; noted in runbook).

## 2. Environment hazards checked

- `TMPDIR` law: runbook exports `TMPDIR=$ROOT/scratch/tmp` (overlayfs, 13G free
  on /home/codespace). `/tmp` is a separate smaller ext2 — the 01 closeout hit
  ENOSPC rendering there; the runbook never uses /tmp.
- LO shared gate profile `scratch/tmp/s21_lo_profile_299640`: `pgrep -af` at
  preflight showed no live soffice on it (only the probe's own shell matched).
  Runbook requires a quiescence check before the full gate (deck_gate_r25 died
  on profile contention, not pixels).
- `scratch/tmp` currently 9.8M / 28 entries — room for gate artifacts.

## 3. Dry-run r2 (captured to `dryrun_r2.txt`, stderr in `dryrun_r2.stderr.txt`)

`python3 $RJ/closeout_finalize.py --dry-run` → exit 0, 143-line report printed,
**nothing written**:

- `$NS/CLOSEOUT_REPORT.md` mtime unchanged (2026-11-01 19:16:12) after the run.
- A `-newer` marker sweep over `$NS` found no file modified outside `$OUT`
  except `slides_progress.db-shm` (mtime only). Cause: the script opens the DB
  with `mode=ro` in WAL mode, which touches the shared-memory sidecar. Main DB
  bytes untouched: `slides_progress.db` still 57,344 B, mtime 2026-11-01
  19:16:28; `slides_progress.db-wal` is 0 B. No data write occurred.
- stderr guard line: `[dry-run] guards: DB 50/51 passed; merge_gate_FINAL.md
  MISSING -> real mode would REFUSE TO WRITE`.

## 4. Write-guard state at preflight (both currently BLOCK)

1. **DB guard**: `SELECT COUNT(*) FROM slides WHERE gen_status='passed' AND
   visual_check='PASS'` → **50/51**. Open row: `slide_id=25, gen_status=building,
   visual_check=''`. Real mode would exit 2 (REFUSE).
2. **Gate-file guard**: `$RJ/merge_gate_FINAL.md` does not exist. Real mode
   would exit 3 (REFUSE). (Would also exit 4 if the file existed without a
   PASS verdict line.)

Ledger context (read-only): `final_deck_state.json` — 51/51 pages `certified`,
but `render_check` census at preflight was FAIL=40 / PASS=11, 233 events, last a
`render-check FAIL` for page 37 at 2026-11-01T20:45Z, `deck_md5
1966dcc3c489600da188df2b781a1d8c`. The deck is still mutating → the full gate
in runbook step B is genuinely still pending, as expected.

## 5. Closed-deck conventions verified for runbook steps C/D/E/F

- **md5 sidecar**: 02 keeps `recreated_pptx/02_linear-regression-classification-MSSE_final.pptx.md5`
  next to the deck, content `md5  recreated_pptx/<final>.pptx` (path relative
  to NS root; `md5sum -c` from `$NS` OK). (01 instead put `ml-intro_final.pptx.md5`
  at the NS root — the 02 `recreated_pptx/` location is the convention used.)
- **Certified render PDF**: 01 has `ml-intro_final_render_certified.pdf` at the
  namespace root → deck-03 analog `03_ridger_regression_gradient_descent_final_render_certified.pdf`
  at `$NS` root. Currently NO pdf at `$NS` root (confirmed).
- **Root pixel-gate record**: 01 has `final_deck_pixel_gate_2026-10-10.txt` at
  root → deck-03 analog `final_deck_pixel_gate_<date>.txt` at `$NS` root.
  Currently none (confirmed).
- **db_sync_final.txt**: 02 §9 banked it as `scratch/ml02/merge_gate_final/db_sync_final.txt`;
  runbook banks deck 03's at `$RJ/db_sync_final.txt` (scratch is transient).
- **Gate report banking**: `render_check_pages.py` writes
  `$RP/qa/final_deck_updates/gate_<stamp>_p<N...>/gate_report.txt`; dirs are
  immutable evidence.

## 6. Stray files inventory for runbook step G (single-version disposition)

Present in `$RP/` at preflight (never delete; runbook moves them to
`$RP/qa/single_version_disposition_20261101/`):

- `slide_015_recreated_v2.pptx` (546,389 B), `slide_015_recreated_v3.pptx` (578,060 B)
- `slide_014_recreated.pptx.bak_prefix3` (183,393 B)
- `slide_015_recreated.pdf`, `slide_015_recreated_v2.pdf`, `slide_015_recreated_v3.pdf`, `slide_025_recreated.pdf`

Plain `slide_001..051_recreated.pptx` all present (51 deliverables) plus the
final deck `03_ridger_regression_gradient_descent_final.pptx`.

## 7. Missing / not-yet items (expected — gate not run)

- `$RJ/merge_gate_FINAL.md` — to be written by runbook step B.
- `$NS` root: no certified PDF, no pixel-gate record — steps D/E.
- No `.md5` sidecar anywhere under `$NS` — step C.
- `$RP/qa/s9_prep_20261031/` exists but is empty (GAPLIST checklist item 9).
- DB 50/51 (slide 25 open) — external in-flight work, not fixable from here.
