# SOURCES.md — slide 016 "L₁ and L₂ Regularization"

Preamble: mandated by `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`
§ "Web-source research mandate (founder in-session directive 2026-10-19)". Method: agy web
search (MCP `agy_web_search`) + live `curl -sL` fetch of every recorded URL in the same
work window that records it (+ `pdftotext` extraction of a downloaded source PDF). Frame
facts come from the slide's vision-analysis record (`analysis/slide_016_raw.json` — no
`_final` exists for this slide, so the raw is the record of the frame); NO vision calls
were made by this worker. Query economy: **0 new queries** — this slide's claims are
covered by the cluster's shared sources (the Ng 2004 paper was reached through the
`Ridge regression` article's own citation, i.e. via the shared first query, not a new one).

## Slide identity

- Frame file: `unique_slides/slide_016.jpg` (960×540, 1px = 1pt per the deck AGENTS).
- Badge number on the frame: **16** (yellow circle, black numeral). Deck rule: badge
  numeral = the file number N, no zero-padding.
- Numbering resolution: 51 founder-curated files numbered by the founder 2026-10-19; the
  pre-curation state is intentionally unrecoverable. A recovered pre-curation provenance
  value IS present in `_meta`: `source_timestamps.precuration_slide = 31` (kept frame
  `frame_01086.jpg`, t = 1085 s, `provenance: "founder-curated kept frame"`). One of the
  35 with recovered provenance; NOT in the 16-slide unrecoverable list. File number 016
  and badge "16" agree; pre-curation 31 is historical only.
- Analysis record used: `analysis/slide_016_raw.json` (final absent — raw used per the
  mandate's fallback rule).

## Primary source(s)

| URL | What it is | Fetched-live status |
|---|---|---|
| `https://icml.cc/Conferences/2004/proceedings/papers/354.pdf` | **Andrew Y. Ng, "Feature selection, L1 vs. L2 regularization, and rotational invariance", Proc. 21st ICML, Banff, 2004** — the paper the `Ridge regression` article itself cites for the "L₂ regularization" naming ("{{cite conference |first1=Andrew Y. |last1=Ng |year=2004 |title=Feature selection, L1 vs. L2 regularization, and rotational invariance |conference=Proc. ICML |url=https://icml.cc/Conferences/2004/proceedings/papers/354.pdf}}"). This is the primary source for the slide's L₁/L₂ terminology and for its final bullet. | **CONFIRMED** — downloaded live 2026-10-20 in this work window (172 KB / 174,127 bytes, 8-page PDF, PDF version 1.2); text extracted with `pdftotext -layout`. Two independent downloads in the same window are byte-identical (see Figures section). |
| `https://en.wikipedia.org/wiki/Lasso_(statistics)` | Wikipedia article **"Lasso (statistics)"**, § *Basic form → Least squares* — the L₁ penalty in both its constrained and Lagrangian forms. | **CONFIRMED** — fetched live 2026-10-20 in this work window (`action=raw` wikitext, 56,860 bytes). Quotes below. |
| `https://en.wikipedia.org/wiki/Ridge_regression` | Wikipedia article **"Ridge regression"** — the L₂/ridge naming and the estimator. | **CONFIRMED (origin-level)** — banked in `sources/slide_014_source/SOURCES.md` and `slide_015_source/SOURCES.md`. **No new query spent.** |
| `https://en.wikipedia.org/wiki/Overfitting` | Wikipedia article **"Overfitting"** — overfitting and the remedy list. | **CONFIRMED (origin-level)** — banked in `sources/slide_010_source/SOURCES.md`. **No new query spent.** |

Nothing above was recorded from an unfetched search snippet.

## Figures used by this slide

**No hosted figure is used by this slide** — it is a text/box panel (title, a blue-bordered
rectangle, and six lines of body text with color-coding). One **source document** was
downloaded into this directory and is banked here as reference-grade provenance for the
slide's terminology:

- `354.pdf` — the Ng 2004 ICML paper itself (the source, not a figure within it), saved
  under the filename as served. 174,127 bytes, md5 `7580d4458726a0305f204cfb629567f2`,
  sha256 `16e7a881a1800caa281091a877d2e73341e589d1df91e71ea451b59dee3cf9df`. Re-fetch
  byte-identity: **IDENTICAL** (two independent downloads in the same work window).
  The paper's own figure (a single line-chart figure of sample complexity vs. dimension)
  is not used by this slide and was not extracted separately.

## What the source(s) CONFIRM

The slide's five body lines, verbatim from the record:

```
Regularizers are based on:
Penalize large values of W (model parameters)
This has the effect of better generalization of the model
Since there is a contradiction between model training (using training dataset) and model
generalization, the generalization term is added to the objective loss function with a
customized weigh factor (do regularization to what extent)
Penalization may be applied on the Squared Norm of the Weight Vector This is called L₂
regularization (also known as Ridge Regularization)
Penalization may also be applied on the sum of Absolute values of the Weight Vector This
is called L₁ regularization
Regularization is particularly important for Small number of samples (N) and Large vector
Length (d)
```

1. **"Regularizers are based on: Penalize large values of W (model parameters)".** Source,
   verbatim (Ng 2004, §2, introducing Eq. (2)):
   > "One way to describe regularized logistic regression is as the finding the parameters
   > θ that solve following optimization problem: … arg max_θ Σ_i log p(y⁽ⁱ⁾|x⁽ⁱ⁾; θ) −
   > αR(θ), where R(θ) is a regularization term that is used to **penalize large
   > weights/parameters**."
   Confirmed, including the slide's "model parameters" gloss.
2. **"This has the effect of better generalization of the model".** Source, verbatim
   (Ng 2004, Abstract):
   > "We consider supervised learning in the presence of very many irrelevant features,
   > and study two different regularization methods **for preventing overfitting**."
   and verbatim (§1): "Thus, unless the training set size is large relative to the
   dimension of the input, some special mechanism—such as regularization, which
   **encourages the fitted parameters to be small**—is usually needed to prevent
   overfitting." Confirmed.
3. **The "contradiction … with a customized weigh factor (do regularization to what
   extent)" line.** Source, verbatim (Ng 2004, §2):
   > "In the optimization problem in Equation (2), the parameter α ≥ 0 **controls a
   > tradeoff between fitting the data well, and having well-regularized/small
   > parameters**."
   This is the source's exact form of the slide's claim: the trade-off is controlled by a
   scalar weighting factor. The slide's "customized weigh factor" [sic] is Ng's α and the
   deck's λ. (Ng also gives the constrained form, verbatim: "max_θ Σ_i log p(y⁽ⁱ⁾|x⁽ⁱ⁾; θ)
   subject to R(θ) ≤ B" — with "B" the second, equivalent way to parameterize the same
   trade-off: "these are two equivalent reparameterizations of the same problem".)
4. **"Penalization may be applied on the Squared Norm of the Weight Vector This is called
   L₂ regularization (also known as Ridge Regularization)".** Source, verbatim (Ng 2004,
   §2, defining the R(θ) cases):
   > "If R(θ) = ‖θ‖₂² = Σ_{i=1}^{n} θ_i², this is **L2 regularized** logistic regression."
   and verbatim (§1, the same term in words):
   > "The second, **L2 regularization, encourages the sum of the squares of the
   > parameters to be small**."
   The "(also known as Ridge Regularization)" gloss is confirmed by the `Ridge regression`
   article, verbatim: "in machine learning it and its modifications are known as weight
   decay, and with multiple independent discoveries, it is also variously known as the
   Tikhonov–Miller method, the Phillips–Twomey method, … **L₂ regularization**".
5. **"Penalization may also be applied on the sum of Absolute values of the Weight Vector
   This is called L₁ regularization".** Source, verbatim (Ng 2004, §1):
   > "The first, **L1 regularization, uses a penalty term which encourages the sum of the
   > absolute values of the parameters to be small**."
   and verbatim (§2):
   > "If R(θ) = ‖θ‖₁ = Σ_{i=1}^{n} |θ_i|, then this is **L1 regularized** logistic
   > regression."
   So the slide's "sum of Absolute values of the Weight Vector" is the source's
   `‖θ‖₁ = Σ|θᵢ|`. Confirmed word-for-word in the same order.
6. **The L₁ penalty as a norm in its own right (supporting the slide's framing of L₁ and
   L₂ as the two norm choices).** Source, verbatim (*Lasso*, *Least squares*):
   > "`$\sum_{j=1}^p |\beta_j| \leq t,$`" (the constrained form) and
   > "`$\min_{ \beta \in \mathbb{R}^p } \left\{ \frac{1}{N} \left\| y - X \beta \right\|_2^2 + \lambda \| \beta \|_1 \right\}$`"
   with "where `$ \| u \|_p = \biggl( \sum_{i=1}^N | u_i |^p \biggr)^{1/p} $` is the
   standard ℓᵖ norm" and "the exact relationship between t and λ is data dependent". This
   is the source's L₁/L₂ pair in the same objective-function shape the deck uses on slides
   014/015 (`fit term + λ · penalty`), which ties slide 016 back to slides 014–018.
7. **"Regularization is particularly important for Small number of samples (N) and Large
   vector Length (d)"** — this is the slide's most specific quantitative-sounding claim and
   it is strongly confirmed. Source, verbatim (Ng 2004, Abstract):
   > "we show that using L1 regularization of the parameters, the sample complexity (i.e.,
   > the number of training examples required to learn "well,") grows only logarithmically
   > in the number of irrelevant features. This logarithmic rate matches the best known
   > bounds for feature selection, and indicates that L1 regularized logistic regression
   > can be effective even if there are exponentially many irrelevant features as there are
   > training examples."
   and verbatim (§1):
   > "This suggests that these algorithms may not be effective in settings where only a few
   > features are relevant, and the number of training examples is significantly smaller
   > than the input dimension."
   and verbatim (§1, Introduction):
   > "unless the training set size is large relative to the dimension of the input, some
   > special mechanism—such as regularization, which encourages the fitted parameters to be
   > small—is usually needed to prevent overfitting."
   In the paper's own variables: *m* training examples, *n* input features — i.e. exactly
   the slide's "Small number of samples (N)" and "Large vector Length (d)".
8. **Sparsity as the L₁/L₂ behavioral difference** (context the slide does not state, but
   which explains why the deck later renames L₂ "Ridge"). Source, verbatim (Ng 2004, §1):
   > "It has frequently been observed that L1 regularization in many models causes many
   > parameters to equal zero, so that the parameter vector is sparse. … For example,
   > linear least-squares regression with L1 regularization is called the Lasso algorithm
   > (Tibshirani, 1996), which is known to generally give sparse feature vectors."

## Course-authored elements (no source counterpart — do NOT "fix" to source)

- The whole layout and presentation: a centered dark-red title, a large blue-bordered
  white content panel, a red bold header line and a blue bold sub-header, then five
  black bullets with color runs — a course-authored slide, not a figure from any source.
- The specific color-coding on bullets (c) and (d): "Squared Norm of the Weight Vector"
  in red and "L₂ regularization" in blue; "sum of Absolute values of the Weight Vector" in
  red and "L₁ regularization" in blue.
- The yellow highlight behind "better generalization", the red underline beneath
  "customized weigh factor", and the black underlines beneath "Small number of samples (N)"
  and "Large vector Length (d)" — all course emphasis chrome.
- **The course's spelling "customized weigh factor"** (should be "weight") and **the space
  before ")" patterns** — transcribed frame text, preserved exactly. Do not correct to
  "weight".
- The one-sentence style of bullets (c)/(d) ("Penalization may be applied on … This is
  called L₂ regularization …") — course phrasing; the source states the same facts in a
  different register ("If R(θ) = ‖θ‖₂² = Σθᵢ², this is L2 regularized logistic
  regression").
- The mouse-pointer cursor over the fourth bullet — a live-presentation capture artifact
  (the raw's own animation note says so); the raw's recreation brief step 8 makes it
  optional. Not slide content.
- The narrowing of the source's logistic-regression framing to linear regression /
  weight vectors W: the deck applies the L₁/L₂ definitions to its W vectors, which is the
  standard transfer and is confirmed by the *Lasso* article's own least-squares form
  (see §6). Recorded, not "fixed".
- **Chrome note (deck law):** the raw reports background `#FFFFFF`, agreeing with the
  deck's mandated white canvas. No divergence.

## [?] Uncertain items

| # | Item | Resolution path |
|---|---|---|
| 1 | The bullet (c)/(d) color-run assignment — which exact phrase is red and which is blue | frame-only measurement (the raw's recreation brief states the assignment, which this worker took as the record; image input is unavailable to this worker's model so no re-read was possible) |
| 2 | Whether the L₁/L₂ subscripts are true subscripts or plain "L1"/"L2" | frame-only measurement; the raw records subscript numerals ("L₁ and L₂") and its equations list uses "L₂"/"L₁" |
| 3 | Exact font sizes (title ~30–34 pt, bullets ~14–16 pt) | frame-only measurement |
| 4 | Whether the content panel's border is exactly `#0000FF` 1pt | frame-only measurement |
| 5 | Whether the deck's N (samples) and d (vector length) are the paper's *m* and *n* | **RESOLVED**: the paper's *m* = number of training examples, *n* = input dimension ("we are given a set S = {(x⁽ⁱ⁾, y⁽ⁱ⁾)}ᵐᵢ₌₁ of m training examples … x⁽ⁱ⁾ ∈ [−1,1]ⁿ are the n-dimensional inputs"), matching the slide's N and d |
| 6 | Whether "Regularizers are based on:" is the slide's own heading or a source's | frame-only: it is a course-authored header line; the source's corresponding framing is "R(θ) is a regularization term that is used to penalize large weights/parameters" |

## Corrections

**None applied; one annotation CONFIRMED (no patch needed).** The annotation that the
slide's "customized weigh factor" is a scalar trade-off weighting parameter (the deck's λ,
Ng's α, the Lasso article's λ) is confirmed by the source's own "controls a tradeoff
between fitting the data well, and having well-regularized/small parameters" and by the
λ = 3 / λ = 10 re-derivations on slides 017/018. No analysis JSON was edited by this
worker, and no transcribed frame text is contradicted by any source.

## Law reminder

The frame wins for recreation; the source wins for understanding. Discrepancies above are
recorded, never silently applied.
