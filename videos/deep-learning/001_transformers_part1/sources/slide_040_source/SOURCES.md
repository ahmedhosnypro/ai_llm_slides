# SOURCES.md — slide 040 "Multi-Head Attention" (section divider: Wide / Narrow Architecture)

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
Peter Bloem's transformers post (current page + 2019 Wayback capture). No vision
calls run; no image access — frame facts below come from the script-12 raw
transcription, which is the record of the frame.

## Slide identity

- New (curated) slide **040** ← old extraction slide **83**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_040.jpg`,
  badge "40".
- Frame facts (raw transcription): light-gray content panel with dark-red
  border, flush to the bottom edge; centered bold red title "**Multi-Head
  Attention**" (double space between the words); two unbulleted bold blue
  lines: "**Wide Architecture**" and "**Narrow Architecture**"; yellow badge
  "40"; a mouse-cursor artifact above the title (recording overlay — exclude
  from recreation).
- Position in the course: section OPENER for the multi-head family — the two
  bullets name the two architectures the next three slides present (raws 44/45:
  "Multi Head Self Attention of Word X₂" — "Wide" Architecture / "Narrow"
  Architecture; dependency graph 44←43, 45←43).

## Primary sources

- **Peter Bloem, "Transformers from scratch" — section "Narrow and wide
  self-attention"**:
  - Current page https://peterbloem.nl/blog/transformers (verified live
    2026-10-11): the wide/narrow section is NO LONGER PRESENT (the March 2023
    rewrite moved the final self-attention to "the canonical form (rather than
    the earlier 'wide' variety we used for the sake of simplicity)"), but the
    page's Updates log still records "Added a section on the difference between
    wide and narrow self-attention" (19 Oct 2019).
  - **Wayback capture (verified live 2026-10-11) — the section's text**:
    https://web.archive.org/web/20191220000000/https://peterbloem.nl/blog/transformers
    — contains the section titled "Narrow and wide self-attention" with: "There
    are two ways to apply multi-head self-attention."; "The standard option is
    to cut the embedding vector into chunks"; the code "implements both methods
    (called **narrow and wide self-attention** respectively)."
- **Paper**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11) —
  §3.2.2 multi-head background (h=8 heads, per-head W_i^Q/W_i^K/W_i^V, concat +
  W^O). The paper itself never uses the words wide/narrow — that terminology
  enters this deck through Bloem's post.

## Figures used by this slide

**None** — text-only divider. Download decision: nothing downloaded into this
dir (no figure exists to claim).

## What the sources CONFIRM (data behind the slide)

- **The "Wide / Narrow" fork is Bloem's terminology**: his multi-head section
  states there are two ways to apply multi-head self-attention — **narrow**
  (the "standard option": cut each embedding vector into chunks — every head
  attends to its chunk of the sequence, per-head dimension = d/h) and **wide**
  (every head attends to the entire sequence with its own full-size W
  matrices). The course's two bullet lines name exactly this fork, and raws
  44/45 show the course then builds the Wide and Narrow versions separately —
  matching Bloem's "both methods".
- **Order note**: Bloem's section title lists "Narrow and wide"; the slide
  lists Wide first. Trivial ordering difference — the frame wins for
  recreation; no correction.
- **Which one the original transformer uses**: the 2019 capture does not state
  it explicitly; the paper's §3.2.2 config (h=8, d_k=d_v=d_model/h=64 — heads
  of REDUCED dimension, "due to the reduced dimension of each head the total
  computational cost is similar to single-head attention with full
  dimensionality") is the narrow-style projection-then-attend design. The
  course's own ordering (Wide presented first, at 43/44) is the instructor's
  pedagogy — record, don't judge.

## Course-authored elements (no source counterpart — do not "fix" to a source)

- The divider layout (red title, two blue lines, panel chrome), the exact
  bullet wording "Wide Architecture"/"Narrow Architecture" (Bloem's nouns are
  "self-attention", the course's is "Architecture"), the double space in the
  title, and the yellow badge — all instructor's own.

## [?] Uncertain items

- [?] Whether the instructor's Wide/Narrow split also leans on any other
  source (no public Zewail deck exists — SOURCES_MAP.md §1; Bloem's post is the
  only verified web source for this terminology in the deck's notation family).
  The frame itself is unambiguous; this [?] concerns provenance only.
- [?] Bullet glyph absence confirmed by raw ("no bullet characters") — nothing
  to verify externally; noted as frame fact.

## Corrections

- **Cross-check 2026-10-11 (W-G, post-banking):** none — consistent. No
  patches to `analysis/slide_040_raw.json`: text-only slide, transcription
  clean, and both [?]s are provenance/frame-note items the raw cannot answer.
  Frame facts in this file re-verified against the raw verbatim (title double
  space, both blue lines, badge 40, cursor artifact).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). The sources confirm/correct DATA and record
provenance; they never license inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy — the slide
wins for recreation, the source wins for understanding.
