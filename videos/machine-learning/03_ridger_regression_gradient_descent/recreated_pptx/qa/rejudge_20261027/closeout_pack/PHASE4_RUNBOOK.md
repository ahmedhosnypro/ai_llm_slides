# PHASE4_RUNBOOK.md — deck 03 final closeout gate (Phase 4)

Prepared 2026-11-01 by the closeout-pack worker. **Prep only**: this runbook was
authored WITHOUT running the gate. The gate is gated on 51/51 DB certification
(slide 25 still open at prep time) plus all OMML wraps landed and restaged.

Paths (absolute):

```
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$NS/recreated_pptx/build/final_deck
RP=$NS/recreated_pptx
DECK=$RP/03_ridger_regression_gradient_descent_final.pptx
LEDGER=$RP/final_deck_state.json
DB=$NS/slides_progress.db
export TMPDIR=$ROOT/scratch/tmp
```

Tooling facts (measured from source, 2026-11-01):

- `final_deck_tool.py` subcommands: `verify-structure`, `init-ledger`,
  `update <pages...>` (ascending ints; NO all-pages mode — pass all 51 numbers
  explicitly), `mark-render <pages...> PASS|FAIL <detail>`. `update` refuses any
  page whose DB row is not `gen_status='passed' AND visual_check='PASS'`.
- `render_check_pages.py <page> [<page>...]` — positional page numbers only,
  `--help` crashes it. One LO session (profile `scratch/tmp/s21_lo_profile_299640`),
  deck PDF page count must be 51, 150 dpi `pdftoppm`, PIL `ImageChops.difference`
  0 px required. Exit 0 = PASS (marks ledger PASS), exit 1 = FAIL (marks ledger
  FAIL, stop-and-fix law). Writes
  `$RP/qa/final_deck_updates/gate_<stamp>_p<N...>/gate_report.txt`.
- `closeout_finalize.py` write guards: (1) DB census
  `COUNT(*) WHERE gen_status='passed' AND visual_check='PASS'` == 51;
  (2) `$RJ/merge_gate_FINAL.md` exists AND carries a PASS verdict line (a line
  containing `PASS` and one of verdict/result/gate/overall, with no
  corresponding FAIL line). Only then does it write `$NS/CLOSEOUT_REPORT.md`.

## Preconditions (all must hold immediately before step A)

0. DB census is 51:
   `sqlite3 "file:$DB?mode=ro" "SELECT COUNT(*) FROM slides WHERE gen_status='passed' AND visual_check='PASS';"` → `51`.
1. Ledger: all 51 `pages[*].status == "certified"`; derive the restage list at
   gate time (do NOT trust a stale plan file) — any page whose on-disk
   `slide_NNN_recreated.pptx` md5 differs from the ledger `source_md5` (path
   prefix `/home/ahmed/Projects/ai_llm_slides` must be remapped to
   `/home/codespace/ai_llm_slides`) or whose `render_check != "PASS"`:
   ```bash
   python3 - <<'EOF'
   import json, hashlib, os
   s=json.load(open("/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/final_deck_state.json"))
   def md5(p):
       h=hashlib.md5()
       with open(p,'rb') as f:
           for c in iter(lambda:f.read(1<<20),b''): h.update(c)
       return h.hexdigest()
   need=[]
   for k,v in sorted(s["pages"].items(), key=lambda kv:int(kv[0])):
       n=int(k); p=v["source_pptx"].replace("/home/ahmed/Projects/ai_llm_slides","/home/codespace/ai_llm_slides")
       if (not os.path.exists(p)) or md5(p)!=v["source_md5"] or v.get("render_check")!="PASS": need.append(n)
   print(" ".join(map(str,need)))
   EOF
   ```
   → `RESTAGE="<that list>"` (at prep time ~47 pages were not PASS).
2. All OMML wraps finished per `$RJ/OMML_WRAP_LOG.md` / `OMML_WRAP_PLAN_r4.md`
   (every wrap changes slide-pptx bytes → those pages are in RESTAGE by rule 1).
3. On-disk deck md5 == ledger `deck_md5` after the last update; no `update-page`
   events after the last gate run.
4. LO profile quiescent — the shared profile has died under fleet contention
   before (deck_gate_r25): `pgrep -af 's21_lo_profile_299640'` must show no live
   soffice (ignore the probe's own shell); if busy, wait for quiescence.
5. `export TMPDIR=$ROOT/scratch/tmp` — never run LO with TMPDIR on the small
   /tmp (the 01 closeout hit ENOSPC there).

## Ordered gate commands

Run from `cd $D`.

### A. Full deck refresh (restage every stale page)

```bash
python3 final_deck_tool.py verify-structure                 # pre-check, must pass
python3 final_deck_tool.py update $RESTAGE                  # ascending; refuses uncertified pages
python3 render_check_pages.py $RESTAGE                      # exit 0 = 0 px per page; per-page retry on FAIL
```

There is no all-pages mode for `update`; if every page must be restaged pass all
51 explicitly: `python3 final_deck_tool.py update 1 2 3 ... 51`.

### B. Full 51-page render gate + merge_gate_FINAL.md

```bash
python3 render_check_pages.py 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51
# expect exit 0, "render gate PASSED for pages [1..51]", 0/51 mismatched pages
python3 final_deck_tool.py verify-structure                 # post-check
```

Then write `$RJ/merge_gate_FINAL.md` (the file `closeout_finalize.py` guard 2
reads). It must contain a PASS verdict line matching its parser, e.g.:

```
# merge_gate_FINAL.md — deck 03 final merge gate
Gate result: PASS — verdict PASS, 0/51 mismatched pages
Exit code: 0
Mismatched pages: [] (0/51)
Gate report: $RP/qa/final_deck_updates/gate_<stamp>_p1-...-p51/gate_report.txt
Deck md5: <md5>
Method: one LO session, deck PDF (51 pages) vs each source pptx, 150dpi, PIL diff 0 px
```

Canonical gate artifacts stay in their `gate_<stamp>_p1-...-p51/` dir (never
move/delete gate dirs); `merge_gate_FINAL.md` is the pointer + verdict copy.

### C. md5 sidecar (closed-deck convention per 02)

02 banks the sidecar NEXT TO THE DECK in `recreated_pptx/`, md5sum format with
the path relative to the namespace root (verified `md5sum -c` from `$NS`):

```bash
cd $NS
md5sum recreated_pptx/03_ridger_regression_gradient_descent_final.pptx \
  > recreated_pptx/03_ridger_regression_gradient_descent_final.pptx.md5
md5sum -c recreated_pptx/03_ridger_regression_gradient_descent_final.pptx.md5   # → OK
```

(Note: 01_ml-intro kept its sidecar at the namespace root instead; the 02
`recreated_pptx/` location is the convention this runbook follows.)

### D. Certified final render PDF at namespace root (01 convention)

01 has `videos/machine-learning/01_ml-intro/ml-intro_final_render_certified.pdf`
at the root. Deck-03 analog:

```bash
export TMPDIR=$ROOT/scratch/tmp
soffice --headless -env:UserInstallation=file://$TMPDIR/phase4_lo_profile \
  --convert-to pdf --outdir $TMPDIR $DECK
mv $TMPDIR/03_ridger_regression_gradient_descent_final.pdf \
   $NS/03_ridger_regression_gradient_descent_final_render_certified.pdf
pdfinfo $NS/03_ridger_regression_gradient_descent_final_render_certified.pdf | grep Pages   # → 51
```

Use a private LO profile (not the shared s21 profile) for this convert.
Never LO-resave the pptx itself (drops OMML).

### E. Root pixel-gate record (01 analog `final_deck_pixel_gate_2026-10-10.txt`)

```bash
cat > $NS/final_deck_pixel_gate_2026-11-01.txt <<EOF
Final-deck pixel gate (Phase 4 closeout, 2026-11-01)
Deck: recreated_pptx/03_ridger_regression_gradient_descent_final.pptx (md5 <md5>)
Method: render_check_pages.py full run, one LO session, 150 dpi, PIL ImageChops page N vs source N
Gate result: PASS — 0/51 mismatched pages, exit code 0
Gate report: recreated_pptx/qa/final_deck_updates/gate_<stamp>_p1-...-p51/gate_report.txt
EOF
```

(Date in the filename = gate date; rename if the gate lands on another day.)

### F. DB sync snapshot — db_sync_final.txt (02 §9 analog)

02 banked it as `db_sync_final.txt`; for deck 03 bank it with the closeout
evidence under RJ (project scratch copies are transient):

```bash
{
  echo "db_sync_final — deck 03 — $(date -u +%FT%TZ)"
  sqlite3 "file:$DB?mode=ro" "SELECT COUNT(*) FROM slides; SELECT COUNT(*) FROM slides WHERE gen_status='passed' AND visual_check='PASS';"
  sqlite3 "file:$DB?mode=ro" "SELECT slide_id, pptx_path FROM slides ORDER BY slide_id;"
  for n in $(seq -w 1 51); do
    p=$RP/slide_0${n}_recreated.pptx
    [ -f "$p" ] && md5sum "$p" || echo "MISSING $p"
  done
  md5sum $DECK
  python3 -c "import json; l=json.load(open('$LEDGER')); print('ledger deck_md5:', l['deck_md5'])"
} > $RJ/db_sync_final.txt
# Verify: 51 rows, 51 passed&PASS, all pptx_path canonical (recreated_pptx/slide_NNN_recreated.pptx),
# all 51 slide md5s == ledger pages[N].source_md5, disk deck md5 == ledger deck_md5.
```

### G. Single-version disposition (NEVER delete — move into a qa evidence dir)

Strays at prep time in `$RP/`: `slide_015_recreated_v2.pptx`,
`slide_015_recreated_v3.pptx`, `slide_014_recreated.pptx.bak_prefix3`,
`slide_015_recreated.pdf`, `slide_015_recreated_v2.pdf`,
`slide_015_recreated_v3.pdf`, `slide_025_recreated.pdf`.

```bash
mkdir -p $RP/qa/single_version_disposition_20261101
mv $RP/slide_015_recreated_v2.pptx $RP/slide_015_recreated_v3.pptx \
   $RP/slide_014_recreated.pptx.bak_prefix3 \
   $RP/slide_015_recreated.pdf $RP/slide_015_recreated_v2.pdf \
   $RP/slide_015_recreated_v3.pdf $RP/slide_025_recreated.pdf \
   $RP/qa/single_version_disposition_20261101/
ls $RP/slide_*_recreated*.pptx | grep -v '/slide_[0-9][0-9][0-9]_recreated.pptx$' || echo "single-version clean"
```

List the moved files in the closeout record (GAPLIST E7 / checklist item 7).

### H. Real closeout run

```bash
python3 $RJ/closeout_finalize.py
# exit 0 + "wrote .../CLOSEOUT_REPORT.md" only when DB==51/51 AND merge_gate_FINAL.md has a PASS verdict.
# Refusal exits: 2 = DB below 51, 3 = gate file missing, 4 = no PASS marker.
# Safe to re-run; --dry-run prints the report and writes nothing.
```

### I. CLOSEOUT_REPORT final numbers

`closeout_finalize.py` fills `$NS/CLOSEOUT_REPORT.md` from live DB + ledger +
REJUDGE_REGISTER/VERDICT_CENSUS + OMML_WRAP_LOG + zip scan + merge_gate_FINAL.md.
After it writes, confirm the report shows 51/51 in §1, gate PASS in §5, and the
per-slide table in §6; then fill the skeleton TBDs (GAPLIST §3 item 8: §3
rejudge census, §5 merge-gate verdict, §6 OMML counts, §7 query budgets) and the
missing sections M1–M14 from `$RJ/CLOSEOUT_GAPLIST.md` §1, recording the
disposition of the moved strays (step G) and the S9 prep dir
(`$RP/qa/s9_prep_20261031/`, empty at prep time — populate or reference it,
GAPLIST checklist item 9).

## Laws

- Everything stays inside the `$NS` namespace; TMPDIR=$ROOT/scratch/tmp.
- Never delete banked evidence; never git; never LO-resave a wrapped deck.
- Gate dirs under `qa/final_deck_updates/` are immutable evidence.
- `closeout_finalize.py` is the ONLY writer of `$NS/CLOSEOUT_REPORT.md`; the
  merge gate itself is run via `render_check_pages.py`, never inside the
  finalizer.
