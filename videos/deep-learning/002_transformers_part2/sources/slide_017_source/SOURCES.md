# SOURCES.md — slide 017 "Multi Head Self Attention of Word X_2" (cascaded, with Concat + Linear Transformation)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Vision transcript of record: `transcripts/slide_017_webverify.txt` (2026-10-11,
default `images` route, `--thinking high`, via `scripts/16_vision_gate.sh`).

## CROSS-VIDEO RECAP (founding rule for this slide)

`slide_dependencies.json`: **17 ← deep-learning/001_transformers_part1:43**.
Parent record: `../001_transformers_part1/slide_043_source/SOURCES.md`
(verified 2026-10-11): paper §3.2.2 + Bloem confirm the multi-head semantics;
course "Wide" vocabulary originates from Bloem's post; course-vs-paper mapping
table there (per-head projections → dot/scale/softmax/weighted-sum → concat →
linear transformation). Per the recap rule that verification CARRIES — both
parent sources were additionally re-confirmed live this session (slide-016
record: §3.2.2 verbatim excerpts + Bloem per-head W_q^r/W_k^r/W_v^r, k×k wide
matrices). Only new visual differences are assessed below.

## Slide identity

- Frame `unique_slides/slide_017.jpg`, badge "17" (timeline: t≈632–637 s, old
  extraction 28).
- Frame facts (vision transcript, ground truth): title "Multi Head Self
  Attention of Word X_2" (top-right; X_2 red). FIVE stacked cascade panels
  h=1 (red, front) .. h=5 (orange/tan, rear), each a full copy of the
  single-head pipeline: X_1..X_4 token columns (left = key path via yellow
  W_k^h boxes → K_1..K_4 [?tiny]; right = value path via yellow W_v^h boxes →
  V_1..V_4; bottom row = query path via red W_q¹ [?superscript]) → tan "Dot
  Product" box ("K: q" label) → pink "Scaling by √d" (label "K:q/√d") →
  lavender "Soft max" → "Probabilities" oval → blue Σ with red ⊗ nodes →
  "Weighted SUM" oval. Thick red curved arrow "+H Heads" sweeps to the h=2..5
  panels (with small per-head W_q^h/W_k^h/W_v^h yellow boxes [?tiny]). Upward:
  per-head outputs → "Concatenated Vector" bar labeled **"1×dH"** (5 colored
  segments Y_1¹..Y_5¹ [?tiny]) → white box **"Linear Transformation [ T ]"**
  with edge label **"d×H×d"** [?] → top token strip "1×d". Bottom-right inset
  legend (light green, dashed): 1×d strip · W (d×d box) = 1×d strip, caption
  "d : Embedding Length".
- Video artifacts (do not recreate): black letterbox bar across the frame
  bottom. Tiny glyphs at legibility edge: K_1..K_4 squares, W-box superscripts,
  the small dashed Y token boxes under the concat bar.

## Primary sources (carried from parent; re-confirmed live 2026-10-11)

- **Vaswani et al. 2017** — https://arxiv.org/html/1706.03762v7 §3.2.2
  (live-confirmed this session): "linearly project the queries, keys and
  values h times with different, learned linear projections"; head_i =
  Attention(QW^Q_i, KW^K_i, VW^V_i); MultiHead(Q,K,V) = Concat(head_1,...,
  head_h)W^O; h=8. CONFIRMED — the slide's whole pipeline (per-head
  projections → scaled dot-product → softmax → weighted sum → concat → final
  linear map) is exactly §3.2.2's computation, with head-INDEXED weight
  symbols (W_k^h/W_v^h/W_q^h) matching the paper's W_i^Q/W_i^K/W_i^V style.
- **Peter Bloem, "Transformers from scratch"** —
  https://peterbloem.nl/blog/transformers (live-confirmed this session):
  heads indexed r "each with different matrices W_q^r, W_k^r, W_v^r";
  per-head outputs concatenated then linearly mapped back; k×k (wide) per-head
  matrices — the provenance of the course's d×d squared-W convention
  (inset legend: W is d×d, "d : Embedding Length"). CONFIRMED.

## Figures used by this slide

**None — course-authored diagram.** The cascaded h=1..h=5 panel composition
with the "+H Heads" arrow and the W(d×d) inset legend matches no published
figure (transcript's explicit finding: same math as Vaswani §3.2.2, but NOT a
copy of Fig 1/2, Bloem, or Alammar layouts). Download decision: nothing
downloaded into this dir.

## What the sources CONFIRM (carried + this session's live re-checks)

- Per-head learned W_q/W_k/W_v → scaled dot-product attention (K·q/√d →
  softmax → weighted sum of V) → concat → final linear transformation:
  paper §3.2.2 + §3.2.1. CONFIRMED.
- Course d×d per-head W bookkeeping (concat 1×dH → linear back to 1×d):
  Bloem's wide flavor (k×k matrices). CONFIRMED as course convention
  (parent's record §5 already records the course-vs-paper dimension
  difference — kept verbatim).

## New visual differences vs the 001 parent (fresh-verification notes)

- **Composition**: THIS frame is closer to the parent (001:43) than sibling
  002:015 was — the "Concatenated Vector 1×dH" bar and "Linear
  Transformation [T]" box ARE visible here (015's record flagged them [?absent]
  on that frame). Parent's linear label reads "dH×d"; THIS transcript reads
  **"d×H×d"** [? tiny glyph, "dxHxd" at the box edge]. If the frame really
  prints d×H×d (3-factor), that is a course bookkeeping variant vs the
  parent's dH×d 2-factor — [?] zoom the video frame (t≈632–637 s) before
  building; do not silently "fix" either way.
- **Per-head W symbols carry head superscripts** (W_k^h, W_v^h, W_q^h/W_q¹
  [?]): paper-style head indexing (W_i^Q...) — closer to the paper's notation
  than the parent's indexless W^Q/W^K/W^V legend. Per-head outputs labeled
  Y_i with superscripts [?tiny] (transcript reads Y_1¹..Y_5¹, i.e. head 1's
  outputs feeding the concat bar).
- **"+H Heads"** arrow label (sibling 015 read "H Heads"). Same semantics
  (replication across heads), different label text — frame wins.
- **Inset legend** (1×d · W d×d = 1×d, "d : Embedding Length"): the P1-family
  dimension legend (cf. 016's "Embedding Dimension=4" callout) — course-authored.

## Open questions

- [?] "d×H×d" vs parent's "dH×d" on the Linear Transformation box — tiny
  glyph; zoom t≈632–637 s before building.
- [?] K_1..K_4 key-token squares, W-box head superscripts, the small dashed
  Y-token boxes under the concat bar, and the Y-segment superscripts — all at
  the legibility edge in the JPEG; zoom before build if their exact glyphs
  matter.
- [?] W_q superscript (¹ vs ^h) on the red query box.

## Script-12 raw cross-check (raw-verification worker, 2026-10-11 — raw landed
after this file's research; the record's frame facts were transcript-based)

- `analysis/slide_017_raw.json` read in full (model `images`; old extraction 28;
  kept_frame frame_00638, 6 frames). Composition confirmed (five cascaded heads
  h=1..h=5; Concatenated Vector bar "1×dH"; "Linear Transformation [T]" box;
  "+H Heads"-style red arc; bottom-right dimension legend).
- [?] RESOLVED (Linear box edge label): raw reads "d×H·d" (red, at the
  "Linear Transformation [ T ]" box's bottom-right) — resolves the record's
  "d×H×d vs parent's dH×d" toward the 3-factor reading d×H·d on THIS frame
  (course bookkeeping variant vs the parent's 2-factor; frame wins).
- [?] RESOLVED (W_q superscript): raw reads "W_qᴴ" (subscript q + superscript
  H) on the red query box — resolves ¹-vs-^H toward ^H.
- [?] RESOLVED (concat segment superscripts): raw reads the five concat segments
  as Y₁ᴴ..Y₅ᴴ — superscript ᴴ (head index), matching the bar's "1×dH" label
  (the record's "Y_1¹..Y_5¹" read is superseded).
- [?] CONTESTED (per-head token count): raw reads h=1's pipeline with THREE
  keys (K₁·q, K₂·q, K₃·q callouts), THREE ⊗ nodes, V₁..V₃ and three W_kᴴ/W_vᴴ
  boxes — while the X strips read X₁..X₄. The record's transcript read
  K_1..K_4 / V_1..V_4. Both reads recorded; the 3-vs-4 micro-glyph question
  needs the standing build-time zoom (t≈632–637 s) — frame wins either way.
- Raw additions/refinements: top input strip is the current word's embedding
  with "Y₂" in its yellow cell (feeds Linear Transformation [T]); arc label
  reads "+H* Heads" (italic); legend glyphs read "1×1d [W] = 1×d·d" [?] (same
  content as the record's "1×d · W(d×d) = 1×d"; glyph-level zoom stands).
- Script-13 final: NOT YET LANDED for 017. Corrections: none yet — verify against
  script-13 final when it lands.
