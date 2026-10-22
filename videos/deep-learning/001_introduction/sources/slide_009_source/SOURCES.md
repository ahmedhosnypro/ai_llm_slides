# slide_009 — "The Complete ML Classification Process" — SOURCES

Slide content (from slide_009_raw.json, frame = ground truth):
Flowchart: peach ellipse "Training Data" -> Pre processing -> Feature Extraction ->
Feature Selection -> Classification -> Post processing -> yellow ellipse "Final Result".
Gray sub-labels under the first four chain boxes: Cleaned Data, Feature Vectors,
Final Features, Predicted Class.

## What the web confirmed

1. **Wikipedia, "Pattern recognition"** (fetched via curl 2026-10-12, saved text):
   https://en.wikipedia.org/wiki/Pattern_recognition
   - CONFIRMS the stage vocabulary and ordering as the classic pattern-recognition
     system pipeline: "Pattern recognition systems are commonly trained from labeled
     \"training\" data."
   - CONFIRMS feature extraction as a distinct pipeline stage: "Techniques to transform
     the raw feature vectors (feature extraction) are sometimes used prior to application
     of the pattern-matching algorithm. Feature extraction algorithms attempt to reduce a
     large-dimensionality feature vector into a smaller-dimensionality vector..."
   - CONFIRMS the slide's SEPARATE "Feature Extraction" and "Feature Selection" stages
     are canonical, distinct concepts: "The distinction between feature selection and
     feature extraction is that the resulting..." (selection keeps a subset; extraction
     transforms).

2. **Wiley publisher page, Duda / Hart / Stork, "Pattern Classification", 2nd ed.**
   (fetched via curl 2026-10-12):
   https://www.wiley.com/en-us/Pattern+Classification%2C+2nd+Edition-p-9780471056690
   - CONFIRMS the classic textbook (Richard O. Duda, Peter E. Hart, David G. Stork,
     ISBN 978-0-471-05669-0, November 2000, 688 pp; "The first edition, published in
     1973, has become a classic reference in the field").
   - agy knowledge synthesis names this book's Ch.1 "components of a pattern
     recognition system" block diagram (sensing -> preprocessing -> feature
     extraction -> classification -> post processing) as the canonical ancestor of
     flowcharts like this slide's — see open question below.

## Figures downloaded

None. The canonical ancestor figure is inside a copyrighted book (not openly
downloadable); the slide's own diagram is an instructor adaptation. No site figure
applies.

## Corrections / disagreements with the slide

None. Stage names and order match the classic pipeline. The slide's diagram is a
legitimate teaching variant of it.

## Open questions

- [?] EXACT FIGURE SOURCE: agy (knowledge mode; its live web search was 403-blocked
  this run) attributes the canonical block diagram to Duda/Hart/Stork "Pattern
  Classification" Ch.1 (claimed Figure 1.1 "Components of a Pattern Recognition
  System") — figure NUMBER and exact wording NOT verified against the book (Google
  Books API daily quota exhausted; archive.org full-text endpoint unusable; search
  engines blocked). Whether the instructor copied Duda's figure or a lecture variant
  of it is unconfirmed. TO RE-VERIFY: `agy -p "components of a pattern recognition
  system duda figure 1.1"` once search access returns, and fetch a university-hosted
  reproduction PDF.
- The gray sub-labels ("Cleaned Data", "Feature Vectors", "Final Features",
  "Predicted Class") as rendered annotations under the chain — consistent with the
  classic pipeline's stage outputs, but no fetched page shows that exact annotation
  layout; likely instructor's own addition.
