# Operations — endpoint quirks, retries, coordination traps

## Model endpoint facts (hard-won)

- **Always stream.** The upstream gateway cuts non-streaming responses at ~60s
  (`ServiceTimeout` on every key while the router churns its pool). Streaming works.
- `finish_reason=length` + `content=null` + filled `reasoning_content` = the model spent
  its whole budget thinking → raise max_tokens (analysis 16k default; validation via
  `IR_MAX_TOKENS` env 32000–65536).
- glm-5.3 sometimes returns empty content with parse error "Expecting value: line 1
  column 1" — transient; re-run the script (it retries only missing outputs).
- ~540 vision tokens/frame at 960px JPEG q4.

## Retry/idempotency patterns

- Scripts 12/13 are idempotent (skip existing outputs) — the documented retry path is
  just re-running them; delete a slide's raw to force that slide's re-analysis.
- Ranged script-13 runs clobber `slides_final.json` → repair by re-aggregating on-disk
  finals in slide order.
- **`find -newermt '-60 minutes'` silently returns nothing** — compute an explicit
  timestamp: `SINCE=$(date -d '-60 minutes' '+%Y-%m-%d %H:%M')` then
  `find ... -newermt "$SINCE"`.

## Background-worker fleet patterns

- One slide = one worker, `run_in_background: true`; all vision calls flock through
  the gate, so worker count is not the bottleneck.
- **Watchdog duties** (every ~30 min): sync+report the DB; a row stuck in
  building/judging with no file mtime movement for >60 min = dead worker → re-dispatch
  (resume rule: banked artifacts and attempt numbering are preserved, a fresh worker
  MUST verify the banked state against its own ground-truth frame before continuing);
  content gate enforcement; house-frame conformance sweep on PASSed builds.
- **A worker reported done but shows "running" → check before re-dispatching**: the UI
  state can be stale (TaskStop returning "not running (status: completed)" proved
  several "stuck" workers were actually done). Verify with file mtimes and DB rows.
- **Dual-worker collisions**: a silently-resumed original worker + a re-dispatched
  resume worker can both own one slide. They overwrite each other's DB writes and
  bank evidence into different dirs (padded vs unpadded QA paths). Recovery: let both
  finish, then reconcile the DB row from the transcripts and bank BOTH evidence tracks.
- **Provider failures kill workers** (TLS failure, upstream timeout). The work isn't
  lost — re-dispatch a resume worker with a state summary (what's banked, what
  attempt number is next, what doesn't count as a spent attempt, e.g. a judge prompt
  banked without a transcript).

## Renumbering / curation traps

Curated decks get renamed ("the badge numeral = the number printed on the original"),
and old numbering leaves landmines:
- Banked QA evidence under an old slide number may belong to a DIFFERENT slide after
  curation (slide 53's banked evidence belonged to current slide 41). Always verify
  banked evidence against your own ground-truth frame before resuming.
- A prior worker's build may be from the OLD deck entirely (slide 64's was). Resume
  rule: verify the build matches your ground truth, not just the file name.
- Never delete old-numbered artifacts — archive them (`analysis_old104/`,
  `*_old104.db.bak`, old builds, old QA dirs) and keep a new2old mapping JSON.

## Misc

- All DB commands: `VIDEO=<id> python3 scripts/15_progress.py <cmd>`; per-video
  namespaces under `videos/<VIDEO>/` so parallel videos never collide.
- API key file `.analyze-image-key` (mode 600) at project root; `IR_API_KEY` env
  overrides; never commit or log it.
- Web research: `agy -p "<query>"`; 401/403 → `agy -p "hi"` to refresh, retry.
- `frames/` is gitignored and huge — never re-extract or re-download.
