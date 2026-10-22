# SOURCES.md — slide 048 "Iteration 1: Weight Update using Step η = 1"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19); binding contract
`~/.zcode/skills/slide-recreation/references/source-research.md` (read before this work).
Method: agy web search (MCP `agy_web_search`) for discovery + **live fetch of every recorded URL
in this same work window** (`curl -sL`; WebFetch returned timeouts on this host) + verification
against the fetched text. Frame facts come from the slide's vision-analysis records
`analysis/slide_048_final.json` (exists — verdict PASS_WITH_FIXES, 8/10, fixes applied by the
validator; title/subtitle reconstructed, not drawn) and `analysis/slide_048_raw.json`. NO vision
calls were made by this worker (no `scripts/16_vision_gate.sh`, no vision model, no local frame
view — web + local-file work only, per the mandate).

## Slide identity

- Frame file: `unique_slides/slide_048.jpg` (960×540, 1px = 1pt per the deck AGENTS.md).
  Badge numeral on the frame: **48** (yellow circle, thin black border; `labels` contains
  "48"). Deck rule: badge numeral = file number N, no zero-padding.
- Numbering resolution: founder-curated set (51 files, 2026-10-19). `_meta.source_timestamps`:
  `precuration_slide = 159`, kept frame `frame_05674.jpg`, t = 5673 s,
  `provenance: "founder-curated kept frame"`, md5 snapshot
  `aaa2e585ea5b8a58de38ab8af7875aa3`. File number 048 and badge "48" agree; pre-curation 159
  is historical only (the pre-curation index was intentionally removed by the founder).
- Analysis records used: `analysis/slide_048_final.json` (validated) +
  `analysis/slide_048_raw.json`. The final's reconstructed catalog title ("Iteration 1: Weight
  Update using Step η = 1") is catalog metadata composed from on-slide strings; the slide has
  no title bar and none must be drawn.

## Primary source(s)

All URLs **fetched live in this work window (HTTP 200)**, sizes and full hashes recorded; none
recorded from an unfetched snippet. Query budget: this worker spent **1** agy search in total
for the whole 045–051 cluster (the perceptron-PLA query); every other recorded URL was then
reached directly from its canonical location (no additional queries — ECONOMY LAW).

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://deeplearning.cs.cmu.edu/S26/documents/readings/Perceptron_Learning_Algorithm_and_Convergence.pdf` | CMU reading "The Perceptron Learning Algorithm and its Convergence" (Shivaram Kalyanakrishnan, 2017; based on a Collins note) — THE canonical pseudocode of this slide's computation. Banked byte-identical in this directory as `cmu_perceptron_pla.pdf` (+ `cmu_perceptron_pla_extract.txt`, pdftotext-derived quote trail). | **CONFIRMED** — fetched live this window, HTTP 200, 193,758 bytes, sha256 `de8b549f66d9f9c9627826628ec0bba0b7e4cb6595651698576be6c228605688` (banked copy verified identical by hash). |
| `https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote03.html` | Cornell CS 4780 Lecture 3 "The Perceptron" — sign(wᵀx+b) classifier; bias absorbed via the appended constant dimension; strict "classified correctly iff y_i(wᵀx_i) > 0"; the update geometry (w_{t+1} = w_t ± x); finite-updates convergence. | **CONFIRMED** — fetched live this window, HTTP 200, HTML 11,759 bytes, sha256 `016a9af244c34f3870f11f00e85996f699c723ef9ae147b8bbdec794af74011d`. |
| `https://en.wikipedia.org/wiki/Perceptron` | Wikipedia "Perceptron" §4 — update `w_i(t+1) = w_i(t) + r·(d_j − y_j(t))·x_{j,i}` (r = learning rate); `x_{j,0} = 1`; "the weights remain unchanged whenever d_j = y_j(t)"; "If the training set is linearly separable, then the perceptron is guaranteed to converge after making finitely many mistakes"; Rosenblatt (1958) ref. | **CONFIRMED** — fetched live this window, HTTP 200, HTML 511,237 bytes, sha256 `ab8b324c8e78c181f50078b5ed0fa7886e5380f9e434f1367491dec38fafa9a3`. |
| `https://www.cis.upenn.edu/~cis5190/fall2015/lectures/04_LinearClassificationPerceptron.pdf` | UPenn CIS 5190 "Linear Classification: The Perceptron" (Eaton, after Rai slides) — "The perceptron uses the following update rule each time it receives a new training instance (x(i), y(i)) … Perceptron update rule: If x(i) is misclassified, do w ← w + y(i)x(i)"; online pseudocode with the `y(i)x(i)ᵀw ≤ 0 // prediction is incorrect` branch; "If the prediction matches the label, make no change"; α-elimination remark. | **CONFIRMED** — fetched live this window, HTTP 200, PDF 3,126,847 bytes, sha256 `a045390ab90326904197323e7bf26d5d4e09df6eefb04af713549906793489e4` (text layer quote-verified via pdftotext). |
| `https://www.geeksforgeeks.org/deep-learning/perceptron-convergence-theorem-in-neural-networks/` | GeeksforGeeks "Perceptron Convergence Theorem in Neural Networks" — the C1/C2-classed update rule verbatim: "If a sample is correctly classified, no update is made: w(n+1) = w(n). Otherwise, the weights are adjusted: … w(n+1) = w(n) + ηx(n), if w^T(n)x(n) ≤ 0 and x(n) ∈ C1." — i.e. the course's exact case, learning rate η and all. | **CONFIRMED** — fetched live this window, HTTP 200, HTML 321,706 bytes, sha256 `b6acf2e8fbde41aaaffb2143b44a621166fdccc7d6b820e2363612db7a663e7d`. |

**Attribution trail (canonical references named by the fetched sources):** Rosenblatt, F.
(1957), "The Perceptron—a perceiving and recognizing automaton", Report 85-460-1, Cornell
Aeronautical Laboratory (cited as [2] by the CMU note); Rosenblatt, F. (1958), "The perceptron:
A probabilistic model for information storage and organization in the brain", Psychological
Review 65(6):386–408, doi:10.1037/h0042519 (Wikipedia ref [11]; Wikipedia also states "The
theorem is proved by Rosenblatt et al."). Both are second-hand here (cited inside fetched
pages); the shipped pages themselves are the fetched-live sources of record.

Origin-level cross-references (sibling banked records, no re-fetch by this worker):
`sources/slide_037_source/` (banked Duda–Hart–Stock *Pattern Classification* 2nd ed. Ch. 5 PDF,
md5 `47235972a70be5152744c50b8a64f77d` — fixed-increment rules, Algorithm 4),
`sources/slide_039_source/SOURCES.md` (course rule W(updated) = W(old) − η δᵢ Xᵢ against
DHS/Wikipedia), `sources/slide_045_source/SOURCES.md` (same cluster's fetched evidence). Sister
records 041–044 were still in progress at write time; nothing here depends on them.

## Figures used by this slide

The slide reuses/redraws **no source figure** (its tables, boxes and arrows are course-built).
For provenance-grade algorithm reference the source page's own figure files were downloaded
as-served and banked in this directory (never renamed), re-fetched once for byte-identity:

- `perceptron_img1.png` — Cornell lecture note's Figure "perceptron_img1" (the perceptron
  diagram, weights × inputs → sign). 64,501 bytes, PNG 1080×687, sha256
  `ee1fd095f6ee84947c99edf1045b3f67`. Re-fetch: byte-identical.
- `PconstantDim.png` — Cornell figure "PconstantDim" (the 1-D/2-D example showing that adding
  a constant dimension makes a separating hyperplane through the origin exist). 458,707 bytes,
  PNG 3616×2250, sha256 `ebcdd55ab839ba6f36c64de1299eb040`. Re-fetch: byte-identical.
- `perceptron_algo.png` — Cornell figure "perceptron_algo" (the Perceptron Algorithm box).
  93,662 bytes, PNG 1235×421, sha256 `382e50014d2b78a261da75690d4af42b`. Re-fetch: byte-identical.
- `PerceptronUpdate.png` — Cornell figure "PerceptronUpdate" (illustration of a Perceptron
  update: the hyperplane tilts after the update). 33,723 bytes, PNG 918×366, sha256
  `5699a092be36895ee56565fd82f70dbc`. Re-fetch: byte-identical.
- `cmu_perceptron_pla.pdf` + `cmu_perceptron_pla_extract.txt` — the CMU source document of
  record for the pseudocode (193,758 bytes, sha256 `de8b549f66d9f9c9627826628ec0bba0…` full
  hash above; the `.txt` is a derived pdftotext extract kept for the quote trail).

**Palette forensics note:** the banked originals' palettes (Cornell figures use their own
course-deck colors; none matches this slide's #E9F2F9/#8FB3CC blue boxes, #FF0000 red accents,
#1E8449 green arrow) confirm that every colored container on the slide is course-authored —
nothing was copied from a source figure.

## What the source(s) CONFIRM

Frame facts (from `analysis/slide_048_final.json` / `_raw.json` verbatim text): "Initial W =
[4; −2; −2]", red "REPEAT using Step η = 1", "C1 positive, C2 negative, Zero is unaccepted",
"Ugmented Vectors (from Top)", red-boxed "Iteration 1", and six calculation rows — row 1
`d(x₁) = [1 1 1]·[4; −2; −2] = 0 ⇒ Update Weight; W = [4; −2; −2] + 1·[1; 1; 1] = [5; −1; −1]`;
rows 2–6 `d(xᵢ) = [1 · ·]·[5; −1; −1] ⇒ Keep same Weight; W = [5; −1; −1]` with results
2, 2, −4, −6, −7.

1. **The row-1 computation `d(x₁) = [1 1 1]·[4; −2; −2] = 0`** — the decision function is the
   dot product of the augmented sample with the weight vector, bias first. CONFIRMED
   (Wikipedia "Linear combiner output: v(n) = Σ w_i(n)x_i(n) = w^T(n)x(n)" with "x_{j,0} = 1";
   Cornell "[x_i; 1]ᵀ[w; b] = wᵀx_i + b"; UPenn "we incorporated bias term w₀ into it by
   x₀ = 1"). The arithmetic itself recomputes exactly: 1·4 + 1·(−2) + 1·(−2) = 0. CONFIRMED.
2. **`d(x₁) = 0 ⇒ Update Weight` with x₁ a Class-I (C₁) sample** — a zero score is treated as
   unclassified/misclassified and fires the update. CONFIRMED: Cornell "y_i(wᵀx_i) > 0 ⟺ x_i is
   classified correctly" (strict — zero is NOT correct); CMU's loop condition is
   "y_i(w_k·x_i) ≤ 0" (zero included) with the explicit note that "the Perceptron's predictions
   for these points would depend on whether we assign sign(0) to be 0 or 1—which seems an
   arbitrary choice"; UPenn's online algorithm: "if y(i)x(i)ᵀw ≤ 0 // prediction is incorrect".
   GfG's verbatim C1 case: "w(n+1) = w(n) + ηx(n), if w^T(n)x(n) ≤ 0 and x(n) ∈ C1" — the
   slide's row 1 is exactly this line with η = 1. CONFIRMED.
3. **`W = [4; −2; −2] + 1·[1; 1; 1] = [5; −1; −1]`** — the update adds the learning rate times
   the (correctly-signed) sample to the weights; equivalently the canonical `w ← w + y·x` with
   y = +1 for the C₁ point and η = 1. CONFIRMED: UPenn "Perceptron update rule: If x(i) is
   misclassified, do w ← w + y(i)x(i)" (and "Can eliminate α … its only effect is to scale w by
   a constant"); CMU pseudocode "w_{k+1} ← w_k + y_j x_j"; Wikipedia
   "w_i(t+1) = w_i(t) + r·(d_j − y_j(t))·x_{j,i}". The arithmetic recomputes exactly:
   (4,−2,−2) + (1,1,1) = (5,−1,−1). CONFIRMED.
4. **Rows 2–6 `Keep same Weight` with W = [5; −1; −1] and the printed results 2, 2, −4, −6, −7** —
   when the score is already correctly signed, no update is made and the weight vector is
   carried forward. CONFIRMED: Wikipedia "the weights remain unchanged whenever d_j = y_j(t)";
   GfG "If a sample is correctly classified, no update is made: w(n+1) = w(n)"; UPenn "If the
   prediction matches the label, make no change". And the arithmetic recomputes exactly all five
   values with W = (5,−1,−1): x₂=(1,2,1) ⇒ 2 ✓; x₃=(1,1,2) ⇒ 2 ✓; x₄=(1,5,4) ⇒ −4 ✓;
   x₅=(1,6,5) ⇒ −6 ✓; x₆=(1,6,6) ⇒ −7 ✓. CONFIRMED.
5. **"Iteration 1" / "REPEAT using Step η = 1"** — one pass over the training set with
   single-sample updates, then repeat. CONFIRMED: Wikipedia's step 2 loops "For each example j
   in our training set D" and CMU/UPenn give the loop structure (repeat while any point is
   misclassified; the course's "REPEAT" names the re-run). The course's per-point
   "Update/Keep same Weight" presentation is the standard single-sample ("online") mode —
   UPenn: "Online learning – the learning mode where the model update is performed each time a
   single observation is received". CONFIRMED.
6. **Step η = 1 as the run's learning rate** — CONFIRMED as the standard hyperparameter:
   Wikipedia "Learning rate is a positive number usually chosen to be less than 1"; UPenn's α
   "its only effect is to scale w by a constant, which doesn't affect performance" (η = 1 is
   the canonical default where the scaling is unity — Cornell's convergence statement and the
   CMU note's theorem are all stated for unit step). CONFIRMED.
7. **The augmented "Ugmented Vectors (from Top)" matrix (bias row of ones + the two feature
   rows)** — CONFIRMED as the standard augmentation: Wikipedia "x_{j,0} = 1"; Cornell "we
   'absorb' [the bias] into the feature vector w by adding one additional constant dimension";
   UPenn "x₀ = 1"; CMU "transforming the d-dimensional input into a (d+1)-dimensional one".
   CONFIRMED.
8. **Convergence outlook for this example:** with the canonical rule the second pass changes
   nothing (all six scores 3, 2, 2, −4, −6, −7 are correctly signed), so the run stops after
   Iteration 1 — matching the sibling frames' "Iteration 2 / No change in W / Stop Iterations".
   The finite-termination behavior is canonical (CMU "While there exists i … such that
   y_i(w_k·x_i) ≤ 0 … Return w_k"; Wikipedia "guaranteed to converge after making finitely
   many mistakes"; Cornell "will find a separating hyperplane in a finite number of updates").
   CONFIRMED.

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The dataset (six 2-D points), W₀ = (4,−2,−2), η = 1, the Z test points, and the whole
  worked example: course-authored; no textbook carries it.
- "Update Weight" / "Keep same Weight" phrasing, the "Check classes of" precomputation, the
  legend "C1 positive, C2 negative, Zero is unaccepted", "REPEAT using Step η = 1": course
  pedagogy wording (underlying conventions standard, as confirmed above).
- The light-blue calculation boxes (#E9F2F9 / #8FB3CC), the dark-red #8B0000 action phrases,
  the green #1E8449 double arrow, the red Iteration-1 box, the yellow badge, the mouse-pointer
  cursor artifact: deck chrome/capture artifacts.
- Frame spelling "Ugmented Vectors (from Top)" preserved verbatim (the final's fix list
  deliberately keeps it; no research correction applies).

## [?] Uncertain items

- **The input data table's third numeric row `(1 2 2 4 5 6)`** — flagged uncertain by the final
  validation itself ("used nowhere else … either a genuine unused table row or a misextraction").
  Source-side evidence: every equation on every sibling frame uses 3-component vectors
  [1; f₁; f₂] (bias + TWO features), the augmented matrix has exactly a bias row + two feature
  rows, and the scatter plots are 2-D — so a third feature row cannot participate in the
  computation. Conclusion recorded: **most plausibly a misextraction**; resolution path:
  build-time pixel check of the cell against `unique_slides/slide_048.jpg` (builder-side; no
  vision call by this worker). Frame wins for recreation: if the pixel check confirms the
  string, it is reproduced verbatim.
- **The green arrow's exact glyph (𝔼/double-lined ⇐ vs ⇒) and size**, **exact box y-bands**,
  **cursor icon position/size**: frame-only measurements (the final's own uncertain list
  carries them); not web facts.
- All other frame-level numbers (positions, colors, fonts) are measurements with no web
  resolution path and stay as measured.

## Corrections

**None applied.** No dimension annotation, attribute guess, or provenance guess in
`analysis/slide_048_raw.json` or `analysis/slide_048_final.json` is contradicted by the fetched
sources. This worker made **no edit** to any analysis JSON. The one substantive source-side
finding (the third table row is almost certainly a misextraction, per the two-feature structure
of every equation) concerns transcribed frame text and is therefore NOT patchable under the
corrections clause — it is recorded under [?] with its build-time resolution path, and the
final's existing uncertain_items entry stands for the builder to adjudicate against the frame.

## Law reminder

The frame wins for recreation; the source wins for understanding.
