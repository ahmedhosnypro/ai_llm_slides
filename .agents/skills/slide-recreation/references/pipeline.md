# Pipeline — extraction → analysis → validated specs

## Frame extraction

`ffmpeg` at 1 FPS into `<video>/frames/` (gitignored; never re-download the video).
YouTube source: use `--cookies /tmp/yt-cookies.txt` (exported from a logged-in Chrome) —
anonymous downloads from datacenter/rate-limited IPs are blocked.

## Slide dedup (phash)

`python3 scripts/11_unique_slides.py <frames_dir> <unique_slides_dir> --threshold 8`

- Threshold 8 groups slide-build animations/repeated builds reliably.
- **Keep the LAST frame of each group**, not the first — slides animate into their
  fully-built state; the first frame is a partial slide.
- Local CPU, deterministic, idempotent — safe to re-run over the whole frame set.

## Vision analysis (per unique slide)

`python3 scripts/12_analyze_slides.py <unique_slides_dir> <analysis_dir> --slides N
[--from A --to B] --max-tokens 32000`

- Model `images`, **streaming** (non-streaming requests die as `ServiceTimeout` at the
  upstream ~60s cut while the router churns its key pool — streaming always works).
- ~540 tokens/frame at 960px JPEG q4 — budget vision calls accordingly.
- Slow: ~3–5 min/slide including upstream key churn. Check the log for `finish=stop`
  per slide; `finish_reason=length` with `content=null` + filled reasoning means the
  model spent the whole budget thinking → raise `--max-tokens`.
- Idempotent (skips existing outputs). To retry ONE slide: delete its
  `slide_XXX_raw.json` and re-run range-scoped.

## Text validation

`python3 scripts/13_validate_slides.py <analysis_dir> --slides N [--from A --to B]`

- Model `glm-5.3` (text only — never use it for visual checks).
- Empty content / "Expecting value: line 1 column 1" → transient, just re-run 13; it
  retries only missing finals.
- Persistent stalls: glm-5.3 burns its whole token budget on reasoning — raise
  `IR_MAX_TOKENS` env var (32000 proven; 49152/65536 as one-offs).
- **TRAP: ranged runs clobber the combined `slides_final.json` to `[]`.** After ranged
  runs, repair by aggregating all on-disk `slide_XXX_final.json` in slide order:
  sort by `int(re.match(r'.*slide_(\d+)_final', p).group(1))` and `json.dump(finals,
  f, indent=2)`.

## Content gate (before any build)

Ready iff `validation.verdict ∈ {PASS, PASS_WITH_FIXES}` AND
`validation.recreatability_score ≥ 8`. Otherwise delete that slide's raw+final and
re-run 12 then 13 (range-scoped), cap 3 retries, then report/block with the error in
the row's `last_error`. Judge-certified acceptance of a score-7 slide is a documented
deviation, not a silent pass — record it.

## Output contract

`slides_final.json` — array of slide objects: `slide_title`, `verbatim_text` (VERBATIM —
no paraphrasing; equations and labels included), `layout` (arrangement + regions),
`visual_elements` (type, chart data values, colors, position), `imagery`, `colors`
(approx hex), `typography_notes`, `recreation_brief` (numbered checklist), and
`validation` block (verdict, fixes, `[?]`-marked uncertain items, recreatability score).
Uncertain content keeps its `[?]` marker — never invent facts.
