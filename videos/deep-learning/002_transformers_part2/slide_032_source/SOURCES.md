# SOURCES.md — slide 032 "Sin/Cos Positional Encoder" (dimension-2 toy vector, 4 properties)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_032_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner) cross-checked against `analysis/slide_032_raw.json` (raw
agrees: same vector, same four property bullets). Web evidence from the
already-live banked sources (paper §3.5 in `scratch/webverify/paper_v7.html`;
Kazemnejad page on slide 027's run, `scratch/webverify/kazemnejad_pe.html`).
No new agy query spent — the slide's claims are fully covered by the two
live-verified sources and by slide 031's derivation record.

## Slide identity

- New (curated) slide **032** ← old extraction **64** —
  `unique_slides/new2old_mapping.json`, frame `unique_slides/slide_032.jpg`.
- Frame facts (vision transcript): title "Sin/Cos Positional Encoder" (red);
  subtitle "Vector of Dimension "2" to define Position" (blue); badge "32".
  Left red-bordered box: the stacked 2-row column vector
  [ sin(ωt) ; cos(ωt) ]; adjacent yellow callout: "Where "t" is the step
  (position) and ω is the frequency of trigonometric function Sine/Cosine".
  Light-blue properties panel: "This vector can be used to define word
  position at step "t" , t=0,1,2,3,4,5,6,7,…." plus four bullets:
  1. "Values are between -1 and 1 (bounded values)"
  2. "Distance between vectors representing positions "t" and "t+1"  is
     constant irrespective of "t"  [Distance (Pos1, Pos2) = Distance
     (Pos90, Pos91)]"
  3. ""t" may take any positive value (No limitation of length of Sequence )"
  4. "Position Vector Length = 2  (Cannot be combined with Word Embedding
     Vector) ??"
  - Artifacts: mouse cursor near the bracketed distance example; bottom
    letterbox band (recording artifacts).

## Primary sources

1. **arXiv 1706.03762v7 §3.5** (live curl 2026-10-11,
   `scratch/webverify/paper_v7.html`) — verbatim:
   - "we use sine and cosine functions of different frequencies:
     PE_(pos,2i)=sin(pos/10000^(2i/d_model)), PE_(pos,2i+1)=cos(...)" — the
     scheme the slide's 2-D toy vector is the first pair of.
   - "The positional encodings have the same dimension d_model as the
     embeddings, so that the two can be summed." — the exact background of
     bullet 4: a length-2 vector CANNOT be summed with a d-dim word
     embedding; the paper's full scheme fills d_model dimensions. The
     slide's trailing "??" is rhetorical and is answered by slide 033 (the
     d-dim generalization with K=d/2 pairs).
2. **Kazemnejad, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (live curl 2026-10-11, banked HTML). The properties checklist, verbatim:
   "Distance between any two time-steps should be consistent across sentences
   with different lengths. Our model should generalize to longer sentences
   without any efforts. Its values should be bounded. It must be
   deterministic." — bullets 1–3 mirror this checklist item for item (bounded
   values ∈ [−1,1]; constant distance irrespective of t; no
   sequence-length limitation). The ω-as-frequency framing and the
   [sin(ωt);cos(ωt)] unit-circle pair are the blog's 2-D building block.
- Bullets 1–3 are arithmetically grounded by slide 031's record
  (`../slide_031_source/SOURCES.md`): squared distance = 2(1−cos(ωδ)),
  independent of t; sin/cos are bounded in [−1,1]; t unbounded.

## What the sources CONFIRM (bullet by bullet)

- Vector [sin(ωt); cos(ωt)] as the position encoder — paper §3.5 (first
  sin/cos pair), Kazemnejad (2-D building block p_t).
- "Values are between -1 and 1 (bounded values)" — paper (sin/cos range),
  Kazemnejad criterion "Its values should be bounded".
- "Distance between vectors representing positions "t" and "t+1" is constant
  irrespective of "t"" — slide 031's derivation (2(1−cos(ω·1)), independent
  of t); Kazemnejad criterion "Distance between any two time-steps should be
  consistent across sentences with different lengths" + dot-product figure
  (banked `../slide_027_source/time-steps_dot_product.png`). The numeric
  example [Distance (Pos1, Pos2) = Distance (Pos90, Pos91)] is
  course-authored illustration (correct under the property).
- ""t" may take any positive value (No limitation of length of Sequence)" —
  Kazemnejad criterion "Our model should generalize to longer sentences
  without any efforts"; paper §3.5 "may allow the model to extrapolate to
  sequence lengths longer than the ones encountered during training" (same
  banked fetch).
- "Position Vector Length = 2 (Cannot be combined with Word Embedding
  Vector) ??" — paper §3.5 d_model-equality sentence (a PE must share the
  embedding's dimension to be summable; length 2 ≠ d). The "??" tension is
  resolved by the paper's multi-pair scheme (slide 033).

## Figures used by this slide

- **None.** Course-authored explanatory composition; no published figure
  reproduced (vision transcript: no resemblance to Vaswani Fig 1/2, Bloem,
  or Alammar artwork).

## Course-authored elements

- The boxed layout (vector box + definition callout + properties panel),
  the "Sin/Cos Positional Encoder" title, the dimension-2 subtitle, the
  Pos1/Pos2 vs Pos90/Pos91 example, the yellow-highlight emphases, and the
  trailing "??" — keep verbatim (including "??" and the double space in the
  distance bullet) for recreation; badge "32".

## [?] Uncertain items

- none. (All four bullets confirmed against the two live sources; the "??" is
  a deliberate course rhetorical device, not an uncertainty.)

## Corrections

- none — vision transcript and script-12 raw agree; sources confirm.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. Sources
confirm/correct DATA and record provenance; they never license inventing or
"improving" content the slide doesn't show.
