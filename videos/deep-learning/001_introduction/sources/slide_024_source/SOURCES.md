# SOURCES.md — slide 024 ("Neural Network Model")

Research date: 2026-10-12. Worker: web-research lane, slides 021–030 (reverse run).

## Slide nature

Multi-layer version of the lecturer's Σ-S NN diagram (three rows × five columns): input
dots → gray Σ|S neurons → **layer i** (blue, O_i) → **layer j** (green, O_j) → **layer k**
(orange, O_k) → gray Σ|S neurons → black "Output 1/2/m" boxes; vertical red "Error" bar;
green "Class 1/2/m" boxes. Red connection lines fully mesh i→j, j→k AND i→k
(**skip connections**, weight labels `w_ji`, `w_kj`, `w_ki` — one w_ki rotated ~90° on
the i→k skip line). Bottom callouts: "Previous Layer Layer (i)" (blue), "Current Layer
(You are here)" (green), "Next Layer Layer (K)" (orange), each with an up-arrow (i, j, k).
Top strip: magenta "Input Samples" — dashed magenta line — "Sample Label".
No equations on this slide (the equations arrive on slide 025/026).

## Source URLs

1. **Rumelhart, Hinton & Williams (1986), "Learning representations by
   back-propagating errors", Nature 323:533–536** — notation + connectivity source.
   - PDF banked this run at `../slide_026_source/naturebp.pdf`
     (https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf, fetched & confirmed).
   - CONFIRMED (agy search, 2026-10-12): backpropagation computes the gradient for ANY
     network of neuron-like units whose connectivity pattern forms a **directed acyclic
     graph (no loops)** — connectivity need NOT be restricted to adjacent layers, so
     non-adjacent (skip) connections, e.g. a layer-i unit sending weights directly to a
     layer-k unit, are inside the RHW86 framework. **The slide's i→k skip connections
     with weight `w_ki` are therefore mathematically legitimate**, and the Net_j/O_j/
     w_ji labels continue the RHW86 notation established on slide 025 (q.v.).
   - Caution recorded for the build owner: in the STRICT vanilla-MLP textbook picture
     (Nielsen ch.1/d2l §5.1) layers connect only adjacently; the lecturer's diagram
     deliberately shows the more general RHW wiring (skip connections), which matches
     the RHW86 primary source. Frame wins for recreation; source explains it.

2. **Nielsen — *Neural Networks and Deep Learning*, ch. 1** (multilayer perceptrons;
   Σ→sigmoid neuron depiction)
   - URL: http://neuralnetworksanddeeplearning.com/chap1.html — FETCHED and CONFIRMED
     earlier this run (see slide 025 SOURCES.md): neurons as weighted-sum + sigmoid
     units; σ(z) ≡ 1/(1+e^(−z)). Confirms the "Σ|S" split-circle neuron glyph (summation
     half + sigmoid half).

## Downloaded files

None new. Primary document (RHW 1986) already banked at `../slide_026_source/naturebp.pdf`
(referenced, not duplicated). The diagram is the lecturer's own live-lecture construction —
no external figure is reused on the slide.

## Confirmed / corrected vs the slide

- Skip connections (i→k, `w_ki`) CONFIRMED as within the canonical framework (RHW86:
  any loop-free connectivity; gradient computable through skip paths).
- RHW86 notation (Net_i/j/k, O_i/j/k, w_ji/w_kj/w_ki) CONFIRMED — consistent with slide
  025 and 026 (one notation chain across the section).
- Σ|S split-circle neuron CONFIRMED as the standard weighted-sum-then-sigmoid neuron
  depiction (Nielsen ch.1; d2l §5.1 for the layer view).
- Relationship to sibling slides CONFIRMED by numbering (new2old mapping): new 24 ←
  old 29 and new 25 ← old 30 are successive annotation states of the same "Neural
  Network Model" base (old 29/30 flagged as near-duplicates in the review packet
  README). Slide 024 = 3-layer overview (i, j, k + skips); slide 025 = two-layer zoom
  (i, j) + the three equations; slide 026 = the weight-update derivation. Builds should
  treat 024's composition as the base diagram of this family (see also
  slide_dependencies.json for gated build relationships).
- Fidelity notes: raw JSON flags a mouse cursor near the middle green neuron and a
  bottom black bar as recording artifacts. Typo-level verbatim items to preserve:
  "Previous Layer Layer (i)", "Next Layer Layer (K)" (doubled "Layer"), and capital "K"
  in "Layer (K)" vs lowercase k in the arrow — keep as measured.

## Open questions

- [?] Exact upstream deck of the lecturer's Σ-S diagram family (as on slide 025) —
  unresolved; frame is ground truth.
- [?] Whether the "Next Layer Layer (K)" box's capital K is intentional or a slide typo
  — keep verbatim either way (fidelity law).
