# Patterns — reusable example-script library (pointer doc)

The patterns live in the **library**: `../patterns/` (one subdirectory per
pattern, each containing a runnable, self-contained example script; the laws
are comments inside the scripts). The global index is
[`../patterns/index.json`](../patterns/index.json) — `name`, `file`,
`language`, `description` per pattern.

**This file deliberately contains NO code, NO measured data, and NO slide
references.** Real constructions, numbers and laws live in the library scripts;
slide-specific war stories live in `../memory/lessons.md`.

## How to use (mandatory on every recreation)

1. Read `../patterns/index.json` FIRST (see `references/patterns.md` duty in
   SKILL.md and the pre-judge checklist in the worker instructions).
2. Open the example script of every applicable pattern; adapt its parameters
   from YOUR original's measurements; run its companion checker where present
   (containment, alignment, cell assertions) as part of the closed loop.
3. Never improvise a variant of something a pattern already solves.

## Adding a pattern (after it is vision-certified working)

1. Create `../patterns/<kebab-name>/` with a runnable, self-contained example
   script (generic parameters, laws as comments, no slide references).
2. Append the entry to `../patterns/index.json`.
3. Bank the slide-specific story that proved it in `../memory/lessons.md`.

## Pattern index (see index.json for descriptions)

| Name | Entry point |
|---|---|
| house-chrome | `patterns/house-chrome/example.js` |
| inner-frame-budget | `patterns/inner-frame-budget/example.js` (+ `check_containment.py`) |
| explicit-line-spacing | `patterns/explicit-line-spacing/example.js` |
| delimiters-spanning-arc | `patterns/delimiters-spanning-arc/example.js` |
| delimiters-bezier-png | `patterns/delimiters-bezier-png/gen_delimiter.py` (+ `example.js`) |
| delimiters-stretched-glyph | `patterns/delimiters-stretched-glyph/gen_delimiter.py` (+ `example.js`) |
| equations-mathtext-png | `patterns/equations-mathtext-png/example.sh` (+ `align_check.py`) |
| highlight-box | `patterns/highlight-box/example.js` |
| graph-panel-generated | `patterns/graph-panel-generated/example.py` |
| table-from-dataset | `patterns/table-from-dataset/example.js` (+ `assert_cells.py`) |
| judge-invocation | `patterns/judge-invocation/example.sh` |
| dense-region-crop-compare | `patterns/dense-region-crop-compare/example.sh` |
| omml-wrap | `patterns/omml-wrap/example.sh` (+ `skeleton.xml`) |
| final-deck-merge | `patterns/final-deck-merge/example.sh` |
