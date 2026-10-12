# Close-out Report — ml-intro slide recreation program (FINAL, 2026-10-10)

## Final state (after the founder-defect rework + single-version consolidation)

| Deliverable | Count | Where |
|---|---|---|
| Single version per slide `slide_NNN_recreated.pptx` (NO suffix; graph/OMML baked in) | **64** | `videos/ml-intro/recreated_pptx/` |
| All-in-one deck `ml-intro_final.pptx` (md5 `ee5df825d81a33f799336a4a4303e03f`) | 1 | same dir |
| Original-slides PDF `ml-intro_unique_slides.pdf` (64 pages, all 960×540pt) | 1 | `videos/ml-intro/unique_slides/` |
| Canonical dataset | iris.csv + UCI provenance | `videos/ml-intro/datasets/` |
| Build scripts (one per slide) | 64 (+ gen_parens53/54.py) | `recreated_pptx/build/` |

Per-slide variant composition (baked into the single versions): 18 slides carry
AI-algorithm-generated graphs (15–19, 35, 43–51, 57, 63, 64), 5 carry PowerPoint-editable
OMML equations with certified PNG fallbacks (26, 42, 52, 54, 55), 41 are the certified
native builds. Pre-consolidation variant decks were byte-renamed, not re-encoded; the
superseded plain-named base pptx and base build scripts were deleted per founder
directive, with each base build archived to its slide's QA dir
(`qa/slideNNN/base_build_archived_single_version.js`).

## Verification

- **Final deck gate**: rendered merged deck + all 64 sources in one soffice session;
  PIL pixel-diff page N vs source N → **0/64 mismatched pages**
  (`qa/final_deck/verify_v2/pixel_diff_report.txt`). First attempt hit /tmp ENOSPC
  (tmpfs) and died mid-write — redone under project scratch; lesson banked.
- **Per-slide certification**: every slide judge-certified PASS (real comparison
  transcripts through `scripts/16_vision_gate.sh`, mandatory template). The 13 founder
  issues from the final-deck review are ALL resolved in
  `videos/ml-intro/slides_progress.db` (table `founder_issues`, 14 rows, 0 open);
  DB `gen_status` = passed 64/64.
- **OMML wrapper v2**: v1's Choice (LibreOffice-writer pattern) rendered NOTHING in
  PowerPoint — v2 mirrors a real PowerPoint-authored sample element-for-element
  (`qa/omml_v2/OMML_V2_REPORT.md`); all 5 wraps 0-px LO-identical; slide 54's rewrap
  caught a rel-id shift (rId1→rId43) via the fail-loud manifest derivation.
- **PowerPoint-vs-LO line-pitch divergence** (founder slide-5 screenshot evidence):
  fixed by pinning explicit `lineSpacing` on every multi-line box (slide 5: pinned to
  the original's measured pitch; PowerPoint auto was 31.64pt vs LO 25.61pt).

## Founder defect batch (all 13 resolved, 2026-10-10)

s5 inner-frame overflow + PowerPoint pitch re-fix · s15 graph-box overflow ·
s42/52/54/55 invisible equations (OMML v2) · s43/s44 deep verify+fix (crop-zoom
re-verification) · s52 yellow-frame width · s53 garbage parens (ARC presets banned;
Bézier-PNG delimiters) · s54 alignment/gaps + fonts + missing parens · s62 iris table
rebuilt from canonical data + frame overflow · s63/s64 spanning delimiters + frame
containment + z-parens visibility. The 053 Bézier paren pattern was reused by the 054
worker (pattern transfer requested by the founder).

## Permanent rules shipped with the program

- Judge template v3 (`scripts/17_worker_instructions.md`): frame containment, missing
  elements, delimiter geometry, table data + the founder precision clauses.
- MANDATORY PRE-JUDGE SELF-CHECK: patterns-first, PIL containment, equation-ink,
  delimiter closed loop, table values, zoomed crop comparisons, explicit lineSpacing
  (PowerPoint-vs-LO law), wrap checks.
- `references/patterns.md` P1–P10 confirmed patterns (every recreation must read first).
- SINGLE-VERSION LAW in AGENTS.md + 17_worker_instructions.md + skill: one pptx per
  slide, no `_graphed`/`_omml` suffixes, graph+OMML applied to the same deck.
- Canonical datasets law: one file per known dataset (`datasets/iris.csv`,
  sklearn-canonical; UCI copy kept as provenance with its 2 famous errata rows).

## Cleanup record (founder directive)

Deleted: scratch QA (`qa/scratch_math/` — live tooling relocated to `qa/math/` with doc
pointers updated; skill wrapper scripts retargeted + smoke-tested), old-104 build
scripts (backed up to `qa/old104_build_scripts_backup/` first), superseded per-slide
pptx (plain bases for the 23 variant slides + old-104 strays). Kept: current builds,
the single per-slide versions, the final deck, all QA judge transcripts and evidence,
datasets, analysis, docs.

## Post-close-out events (2026-10-10 evening)

1. **External intervention + recovery**: between ~22:14 and 22:31 (not this session) the 64
   certified per-slide pptx were deleted and ml-intro_final.pptx was overwritten with a
   WRONG-content deck (rebuilt from pre-fix sources: no slide-5 inner frame, gutted
   slide-62 table; all 64 pages differed from the certified render). Recovered by
   deterministic rebuild from the certified build scripts (59 direct + 5 equation slides
   base+wrapped via build/omml/), re-merged, and proven **0/64 pages identical** to the
   certified reference render. The rebuild also exercised the single-version build chain
   end-to-end (mixed CWD conventions in worker scripts normalized to project-root;
   graphed output filenames fixed to plain names).
2. **Workspace reorganization (founder directive)**: `qa/` REMOVED entirely; build/ now
   holds ONLY the final builds (64 slide_NNN.js + assets + gen_parens + build/omml chain
   + build_ml-intro_final.py + omml_wrapper.py + README.md). Gate references and program
   docs preserved at video level. Certified math tooling relocated to scripts/render_eq*.py.
