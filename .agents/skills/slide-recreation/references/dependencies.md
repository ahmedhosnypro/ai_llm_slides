# Dependencies — dependent-slide build gating & shared component builds

Founder directive 2026-10-11, first binding on
`videos/deep-learning/001_transformers_part1/` (45-slide Transformers deck); extended
same day (v2) with CROSS-VIDEO edges and PATTERN GROUPS, first binding on
`videos/deep-learning/002_transformers_part2/`. General law for ANY deck whose
advanced slides re-use a previous slide's composition — same video or not.

## What a dependency is

A dependent slide ("child") is its parent's composition **plus a delta**: extra
blocks, removed blocks, or blocks replaced by different ones. The founder supplies
the graph — curation of what depends on what is human-owned, like the frame set
itself. Edges are direct-parent (child → the slide it builds on); chains compose
transitively (30 ← 29 ← 26 means 30's composition contains 26's via 29).

## What a dependency is NOT

- A **pattern group** (v2) is NOT a dependency: members share reusable patterns
  (e.g. the same diagram family), not identical compositions. Pattern groups build
  STRICTLY sequentially (verify the pattern, then reuse it) but imply no component
  import and no content identity.
- A playlist pattern-library entry (house chrome etc.) is shared chrome, not a
  slide dependency.

## Canonical storage

- `videos/<VIDEO>/slide_dependencies.json` — founder's edge list (source of truth).
  v1 (same-video only):

  ```json
  {"edges": {"7": [6], "8": [6], "30": [29]},
   "shared_image_sources": {"14": ["slide_18_source/"]}}
  ```

  v2 adds qualified cross-video parent refs and pattern groups (first: 002):

  ```json
  {"edges": {"4": ["deep-learning/001_transformers_part1:15",
                   "deep-learning/001_transformers_part1:18"],
             "10": [9]},
   "pattern_groups": {"P1": [9, 10, 12, 14, 16]},
   "special": {"57": "encoder+decoder composition rule"},
   "shared_image_sources": {"51": ["001_transformers_part1/slide_18_source/"]}}
  ```

- Progress DB: `depends_on` column (csv of parent tokens, `''`/NULL = root) plus
  `pattern_group`/`pattern_seq`. Token grammar: bare int = same-video parent;
  `<namespace>:<slide_id>` (e.g. `deep-learning/001_transformers_part1:15`) =
  cross-video parent. `python3 scripts/15_progress.py register` applies edges and
  groups automatically; `deps` prints per-slide `root | blocked | unblocked` with
  what each blocked slide is waiting on; `buildable` prints the exact dispatch
  list (content gate + dep gate + pattern gate + not-yet-built).

## The gate (what is blocked and what is not)

- **Analysis (script 12) and validation (13) are NEVER blocked** — by dependencies
  OR pattern groups. Every slide, dependent or not, can be analyzed and validated
  in parallel.
- **BUILDS are gated**: a dependent slide's build may start ONLY when every
  dependency is **certified** — `gen_status='passed'` AND `visual_check='PASS'`.
  Cross-video parents certify in THEIR OWN video's DB (`deps` resolves them
  read-only across namespaces — never write outside your video). Before
  dispatching or starting a build, run `15_progress.py deps`; if your slide shows
  `blocked`, do NOT build (report and stop — the orchestrator re-dispatches when
  the parent lands).
- **Siblings unblock together**: one parent's certification unblocks ALL its
  children at once (e.g. slide 6 certifying unblocks 7, 8, 9, 10 simultaneously —
  dispatch them in parallel). Cross-video certification cascades the same way
  across namespaces.
- **Pattern groups gate sequentially**: member k waits for member k−1's
  certification, in the founder's listed order. Dispatchers must NOT fan a whole
  group out in parallel.

## Shared component builds (the "u-components" model)

Child builds MUST import the parent's certified composition as a shared module —
**never copy-paste it, never re-derive its geometry**:

```
videos/<VIDEO>/recreated_pptx/build/
  components/                    # shared, importable, certified building blocks
    house_chrome.js              # primitives: frame + badge + title (house rule)
    slide_006.js                 # a parent slide's FULL certified composition,
    ...                          #   exporting e.g. renderBase(pptx, slide, opts)
  slide_007.js                   # child build: require('./components/slide_006'),
  slide_008.js                   #   call the parent render, then apply the delta
```

- A child build = `require` the parent component → render base → draw ONLY the
  child's own delta (its extra/replaced blocks, at the child's measured geometry).
- **Deltas can REMOVE or REPLACE parent blocks** (measured on the deep-learning deck:
  6 of 15 children — 9, 10, 15, 18, 19, 45 — drop or replace inherited blocks; only
  the rest are pure supersets). So export the parent at BLOCK granularity: one
  function per visual block (e.g. `drawContextVectorCallout(slide)`) plus a
  convenience `renderBase(pptx, slide, opts)` that draws them all, optionally with
  `opts.skip`/`opts.only` selectors. A child composes selectively per-block — NEVER
  draws the full base and tries to erase. The child's own frame is ground truth for
  what survives, moves, or changes.
- Components are **certified single-source-of-truth artifacts**: once the parent is
  judge-certified, its component is frozen. Copy-then-modify; never overwrite a
  certified component in place.
- **Cascade law**: editing a certified component re-opens EVERY descendant —
  rebuild and re-judge the whole subtree, or (better) leave the component alone and
  express the change in the child's delta.
- Chains compose naturally: slide 30's build imports slide 29's component, which
  itself imports slide 26's — the composition is the import graph.
- **Cross-video children** (v2) import the parent video's component by ABSOLUTE
  path (`require("/abs/path/videos/<playlist>/<video>/recreated_pptx/build/components/slide_NNN.js")`).
  Identical recap slides are typically `parent.renderBase(...)` + the child's own
  badge numeral + a tiny measured delta. The multi-video isolation rule is intact:
  the child READS the parent's banked artifacts; it never writes into the parent's
  namespace.
- **Playlist-scoped banking obligation** (v2): bank a component at certification
  when ANY slide in ANY video's graph references you — even with no same-video
  dependents (precedent: deep-learning 001's slides 15/19/33 were childless in 001
  but are parents for 002). A certified slide without a needed component must be
  retro-banked additively (derive the per-block module from its build script,
  verify 0-pixel-diff against the certified render, never touch the certified pptx).

## QA implications for dependent slides

- The child's **closed-loop PIL self-check covers its delta regions**; inherited
  regions are re-verified cheaply (they should be pixel-comparable to the parent's
  certified render — same component, same draw) but the mandatory checks still run
  on the full slide (containment, wrap, etc. apply to everything the child draws).
- Judge dispatch: keep the frozen `-p` template VERBATIM; carry the shared-base
  fact in the worker-editable `--view` context, e.g. "the base composition is
  slide 6's judge-certified component (imported, not re-drawn); the expected
  difference is exactly this slide's delta". A judge finding about an inherited
  region is handled like the W5-inheritance law: if the pixels are identical to
  the certified parent's, the finding is judge variance (document, override) —
  unless the CHILD's own draw broke the region, which is a real fix trigger.
- House chrome is drawn ONCE in the component (or the shared primitive) — children
  must not re-draw it on top.

## Onboarding a new dependent deck

1. Founder curates the frame set (HARD STOP gate) and supplies the edge list
   (in-video edges, cross-video qualified edges, pattern groups, special notes).
2. Machine writes `slide_dependencies.json`, reconciles index/mapping
   (`new2old_mapping.json`, rewritten `slides_index.json`, old index + DB preserved
   as evidence), and `15_progress.py init && register` seeds rows WITH edges and
   groups. Placeholder covers (missing frames) get `analysis_status='n/a-placeholder'`,
   `validation_status='ready'` and skip scripts 12/13 entirely.
3. Analysis/validation fan out over ALL slides; build dispatch fans out only over
   `15_progress.py buildable` output, in waves driven by certification events
   (including cross-video parents certifying in their own video's waves); pattern
   groups dispatch one member at a time in listed order.
