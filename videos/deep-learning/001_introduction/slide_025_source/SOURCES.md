# SOURCES.md — slide 025 ("Neural Network Model")

Research date: 2026-10-12. Worker: web-research lane, slides 021–030 (reverse run).

## Slide nature

Annotated lecture diagram of a feedforward NN seen as a PAIR of layers: a beige panel
with three rows of Σ-S neurons — magenta input dots → white "Σ S" neurons (column tagged
**O_i**, layer **i**, "Previous Layer") → fully-connected red arrows labeled **w_ji** →
green "Σ S" neurons (column tagged **O_j**, layer **j**, "Current Layer (You are here)")
— feeding white "Output 1/2/m" boxes, a vertical red "Error" bar, and green "Class
1/2/m" boxes. Top strip: pink "Input Samples" → dotted magenta arrow → "Sample Label".
Bottom strip: three cream equation boxes:

1. `Net_j = Σ ( w_ji O_i )`
2. `O_j = f ( Net_j ) = 1/(1+e^(−Net_j))` (stacked fraction)
3. `E = ½ Σ_j ( t_j − O_j )²`

## Source URLs

1. **Rumelhart, Hinton & Williams (1986), "Learning representations by
   back-propagating errors", Nature 323:533–536** — the notation source for this slide.
   - PDF banked THIS RUN at `../slide_026_source/naturebp.pdf`
     (https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf, fetched & confirmed;
     scanned letter — equations verified via search synthesis, 2026-10-12).
   - CONFIRMED (agy search, 2026-10-12): RHW86's exact notation is
     `net_j = Σ_i w_ji o_i` and `o_j = f(net_j) = 1/(1+e^(−net_j))` (logistic sigmoid),
     with targets t and SSE-style error at the output. **The slide's notation — Net_j,
     O_i/O_j, the distinctive w_ji subscript ORDER (weight from unit i INTO unit j), and
     the sigmoid f — is RHW86's notation verbatim.** The E = ½Σ_j(t_j−O_j)² output error
     is the same quantity RHW86's δ_j = (t_j−o_j)f′(net_j) derives from. This slide and
     slide 026 (the weight-update slide) form one RHW-notation derivation chain.

2. **Nielsen — *Neural Networks and Deep Learning*, ch. 1 "Using neural nets to recognize
   handwritten digits" (sigmoid neurons)**
   - URL: http://neuralnetworksanddeeplearning.com/chap1.html
   - Status: FETCHED and CONFIRMED (2026-10-12, 191 KB HTML).
   - Confirms the Σ→S neuron depiction: a neuron computes a weighted sum
     (σ(w·x+b)) followed by the sigmoid σ(z) ≡ 1/(1+e^(−z)) ("logistic neurons");
     the standard textbook account of the same per-neuron computation the slide's
     "Σ S" circles depict (summation symbol + S for the sigmoid step).

3. **UvA Deep Learning Course 2016, Lecture 2 "Learning with Neural Networks"
   (Gavves & Welling)** — https://uvadlc.github.io/lectures/nov2016/lecture2.pdf
   (FETCHED this run; not banked — content checked via pdftotext).
   - Related but NOT the source of this diagram: its "Neural network models" pages draw
     the architecture as hierarchically connected functions h1..h5 with a Loss node
     (feedforward / DAG / recurrent variants), a different composition. Its sigmoid
     module and gradient-descent content is thematically parallel. Provenance of the
     DSAI lecturer's own Σ-S layer-pair figure remains [?] (see slide 026 SOURCES.md —
     the whole old-21..31 family was not found verbatim in the checked UvA decks).

## Downloaded files

None new. The one genuinely relevant primary document (RHW 1986) is already banked this
run at `../slide_026_source/naturebp.pdf` and is referenced here rather than duplicated.
The network diagram itself is the lecturer's own construction (frame is ground truth) —
no external figure is reused on the slide.

## Confirmed / corrected vs the slide

- Equations CONFIRMED verbatim against RHW86's notation: `Net_j = Σ(w_ji O_i)`,
  `O_j = f(Net_j) = 1/(1+e^(−Net_j))`, `E = ½Σ_j(t_j−O_j)²` — content and subscript
  conventions match the primary source; the math is standard (Nielsen ch.1/2, d2l).
- The layer-pair reading CONFIRMED as the standard "two adjacent layers of an MLP"
  exposition: previous layer i's outputs O_i are the weighted inputs to current layer j
  (fully connected, weight w_ji) — the setup slide 026 then uses to derive Δw_ji.
- "Error at output / per-class Output→Error→Class flow" — consistent with RHW86's
  output-error framing; the Error bar sits between Outputs and Classes as a teaching
  device (no external source needed; lecturer's own motif).
- Notation cross-slide note: slide 026's derivation box repeats these three equations
  plus the update — the two slides must agree (they do, as read).
- Fidelity note: "Previous Layer Layer (i)" (doubled "Layer") is as-read by the vision
  analysis — re-verify against the frame at build time [?]; raw JSON also flags a mouse
  cursor on the middle equation box and a bottom black bar as artifacts.

## Open questions

- [?] Exact upstream deck of the lecturer's Σ-S layer-pair figure (RHW-notation slides
  of this family are widespread in 1990s NN courseware; not pinned down; does not affect
  recreation).
- [?] Whether the "S" glyph in the Σ-S neurons is "S" for sigmoid or a stylized step
  symbol — frame is ground truth; treated as S (sigmoid) per the equation context.
