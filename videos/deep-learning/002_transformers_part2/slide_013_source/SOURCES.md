# SOURCES.md — slide 013 "Self Attention Mechanism (Linear Transformation of Inputs) — Self Attention of word X_2 w.r.t All words in Sentence (X_1..X_4)"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Vision transcript of record: `transcripts/slide_013_webverify.txt` (2026-10-11,
default `images` route, `--thinking high`, via `scripts/16_vision_gate.sh`).

## CROSS-VIDEO RECAP (founding rule for this slide)

`slide_dependencies.json`: **13 ← deep-learning/001_transformers_part1:33**.
Parent record: `../001_transformers_part1/slide_033_source/SOURCES.md`
(same composition, verified 2026-10-11): the paper (§3.2 / §3.2.1) + Bloem
confirm the three-stage semantics; the diagram is COURSE-AUTHORED (no
published figure redrawn); numeric verification of the (1×d)·W(d×d)=(1×d)
legend is recorded there. Per the recap rule, that verification CARRIES; only
new visual differences were re-checked here (no new web downloads needed —
none exist for a course-authored diagram).

## Slide identity

- Frame `unique_slides/slide_013.jpg`, badge "13". Title (two lines, blue
  bold): "Self Attention Mechanism (Linear Transformation of Inputs)" /
  "(Self Attention of word X_2 w.r.t All words in Sentence (X_1, X_2, X_3,
  X_4)" (X tokens in red; unbalanced closing paren as printed — verbatim).
- Frame facts (vision transcript): same left-to-right dataflow composition as
  the 001 parent — input-embedding column → four W_k boxes (K_1..K_4) → gray
  **"Dot Product"** box with four result dots labeled **K_1.q / K_2.q /
  K_3.q [?] / K_4.q [?]** → purple **"Soft max"** bar → four ⊗ nodes fed by
  **V_4..V_1** from a right-hand W_v column → cyan **Σ** → dashed output
  vector box (green-striped, "V" cell label [?]). Stage pills **Similarity /
  Probabilities / Weighted SUM** (green/white/yellow). Query rail at bottom
  center: X_2 (magenta-highlighted) → **W_q^(r)** → **q_2**. Bottom-right
  green-dashed inset: [1×d vector] · **W** (d×d) = [1×d vector], caption
  **"d: Embedding Length"**. Bottom sentence row X_1..X_4, X_2 highlighted.
- Video artifacts (do not recreate): thick red presenter arrow pointing at
  X_2; a gray diagonal stroke between W_k rows; a small white mouse cursor at
  the left edge (x≈120, y≈300); hand-routed red dashed long-range connectors
  partially overlapping elements.

## Primary sources (recap — carried + re-confirmed this session)

- **Vaswani et al. 2017** — https://arxiv.org/html/1706.03762v7, §3.2 /
  §3.2.1. Parent SOURCES.md quotes §3.2.1 verbatim: dot products of the query
  with all keys → softmax → weighted sum of the values. Re-confirmed live
  2026-10-11 (this session's WebFetch of the same page for the multi-head
  projection wording, slide-012 record) + agy recap check: attention output =
  weighted sum of values with softmax(query·keys) weights → "scaled
  dot-product attention". CONFIRMED.
- **Peter Bloem, "Transformers from scratch"** —
  https://peterbloem.nl/blog/transformers. Re-confirmed live 2026-10-11
  (slide-012 record): per-head W_q^r, W_k^r, W_v^r. Relevant to the W boxes'
  superscript (see below). CONFIRMED.

## New visual differences vs the 001 parent (fresh-verification notes)

- **Dot-product callouts read "K_i.q"** (key · dot · query, four of them
  K_1.q..K_4.q); the parent's frame showed a single "K₂q" label on the box.
  Same course pattern (key-before-query dot-product ordering); commutative —
  paper writes q·k. Notation provenance, not a discrepancy (parent's record
  covers this; here it is printed four times, one per result dot).
- **W boxes carry a superscript the parent's frame did not have**: the
  transcript reads "W_k^(r)" / "W_v^(r)" / "W_q^(r)" with the superscript
  PARTIALLY ILLEGIBLE at JPEG resolution — could be a literal "(r)"
  (Bloem's head index) on each box, or per-box indices (1)..(4). Marked
  **[?] superscript text**. If per-head indices, this would be the course's
  multi-head foreshadowing (slides 15/17 re-use this figure family per
  deps 15/17 ← 001:43); if "(r)", it matches Bloem's head-index notation.
  Recreation should zoom the source video frame to settle it.
- **Output vector box label**: the transcript reads a "V"-ish cell in the
  final dashed vector [?]; the parent's frame showed a green dashed "Y_2"
  output. Same role (the new representation of X_2). Tiny-text [?]; zoom
  needed.
- **Inset position**: the (1×d)·W(d×d)=(1×d) legend sits in a bottom-right
  green-dashed panel (parent: legend strip along the bottom). Same content,
  "d: Embedding Length" caption verbatim — matches the parent's numerically
  verified identity.

## What the sources CONFIRM (carried from parent + re-verified)

- Similarity = K_i · q_2 → Probabilities = softmax → Weighted SUM =
  Σᵢ softmaxᵢ ⊗ Vᵢ: paper §3.2.1/§3.2 (CONFIRMED). Note: NO scaling √d on
  this slide — same deliberate pedagogical order as the parent (scaling is
  introduced later in the course; 002's later slides re-add it).
- K and V from every word; q from the queried word X_2 only: paper §3.2.2 +
  Bloem (CONFIRMED, carried).
- (1×d)·W(d×d)=(1×d) with "d: Embedding Length": numerically verified in the
  parent's record (numpy, 2026-10-11). Carried.

## Figures used by this slide

**None — course-authored diagram** (parent's conclusion stands). Nothing
downloaded into this dir.

## Open questions

- [?] W-box superscript: "(r)" vs (1)..(4) vs other — tiny text; settle by
  zooming the video frame at t≈slides_index(slide_013) before building.
- [?] final output vector cell label ("V"-like vs "Y_2") — tiny text.
- [?] K_3.q / K_4.q callouts partially obscured by connector arrows —
  presumed K_3.q/K_4.q by pattern with K_1.q/K_2.q.

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw landed
after this file's research; the record's frame facts were transcript-based)

- `analysis/slide_013_raw.json` read in full (model `images`; old extraction 19;
  kept_frame frame_00491, 29 frames). Composition confirmed (parent-001:33
  family: embeddings → W_k → K → Dot Product → Soft max → ⊗×4 → Σ → output;
  stage pills Similarity/Probabilities/Weighted SUM; dimension note
  "1*d → W (d*d) = 1*d", "d: Embedding Length").
- [?] NARROWED (W superscript): raw reads "W_k^(r)" / "W_q^(r)" / "W_v^(r)" with
  the superscript "reads '(r)', possibly '(1)'" — leans (r) (Bloem's head
  index), same lean as the record; tiny-glyph zoom glance stands.
- [?] RESOLVED (output label): raw reads the final output as a green-dashed box
  labeled "V" (green bold) — resolves the record's "V-ish cell vs Y_2" toward
  "V" on THIS frame (course variant vs the parent's Y₂; frame wins).
- [?] CONTESTED (K callouts): raw's label list carries a single "K.q" at the
  Dot Product top-right, while the record's transcript read per-dot
  K_1.q / K_2.q / K_3.q [?] / K_4.q [?]. Both reads recorded; per-dot callouts
  remain a build-time zoom item.
- Raw additions: K₁..K₄ vectors in GREEN text; the four W_k boxes sit inside a
  bright-green ellipse; q₂ beside a 2-cell vector; TWO cursor artifacts (black
  arrow over the third W_k box, red pointer at X₂) — do not recreate.
- Script-13 final: NOT YET LANDED for 013. Corrections: none yet — verify against
  script-13 final when it lands.
