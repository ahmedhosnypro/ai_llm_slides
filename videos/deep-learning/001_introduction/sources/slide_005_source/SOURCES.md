# slide_005 — "What is Machine Learning?" — SOURCES

Slide content (from slide_005_raw.json, frame = ground truth):
- "Machine Learning:" header + 3 bullets:
  1. "Designing algorithms that can learn patterns from data (and exploit them)"
     [blue: "learn patterns from data"]
  2. "Approach: human supplies training examples, the machine learns"
  3. "Example: Show the machine a bunch of spam and legitimate emails and let it
     learn to predict if a new email is spam or not" [blue tail]

## What the web confirmed (fetched 2026-10-12 via curl)

1. **Tom Mitchell, "Machine Learning" (McGraw Hill, 1997), Chapter 1** — FULL BOOK
   PDF downloaded from Mitchell's own CMU page into this directory:
   - `MachineLearningTomMitchell.pdf` (60,363,034 bytes; the complete 1997 book,
     free official download from http://www.cs.cmu.edu/~tom/mlbook.html ->
     http://www.cs.cmu.edu/~tom/files/MachineLearningTomMitchell.pdf)
   - VERBATIM (Ch.1, p.2/5 of PDF text): "A computer program is said to learn
     from experience E with respect to some class of tasks T and performance
     measure P, if its performance at tasks in T, as measured by P, improves
     with experience E." — the canonical Mitchell definition.
   - Mitchell's own book page (fetched): "Machine Learning is the study of
     computer algorithms that improve automatically through experience."
   - Ch.1 also decomposes learning problems into Task T / Performance measure P /
     Training experience E (checkers, handwritten words, robot driving), with
     "Training experience E: a database of handwritten words with given
     classifications" — i.e., HUMAN-SUPPLIED LABELED EXAMPLES, matching the
     slide's bullet 2 ("human supplies training examples, the machine learns").

2. **Wikipedia, "Machine learning"** (fetched): field definition matches the
   slide's paraphrase: "...development and study of statistical algorithms that
   can learn from data and generalize to unseen data, and thus perform tasks
   without being explicitly programmed." Also banks the term's 1959 coinage by
   Arthur Samuel. (Same article quotes the Mitchell T/E/P definition above.)

3. **Stanford CS229 Lecture Notes 1 (Andrew Ng)** (fetched PDF:
   https://see.stanford.edu/materials/aimlcs229/cs229-notes1.pdf):
   "if we are trying to build a spam classifier for email, then x(i) may be some
   features of a piece of email, and y may be 1 if it is a piece of spam mail,
   and 0 otherwise." — confirms the slide's spam/legitimate-email example as the
   canonical supervised-learning teaching example.

## Figures downloaded

- `MachineLearningTomMitchell.pdf` — Tom Mitchell's complete "Machine Learning"
  textbook (official free PDF from the author's CMU page). Primary source for the
  definition; chapter 1 covers what this slide teaches.

## Corrections / disagreements with the slide

- The slide does NOT quote Mitchell verbatim — it uses a compressed paraphrase
  ("learn patterns from data"). Content-wise consistent with Mitchell's
  definition and the Wikipedia field definition. No factual error.
- Slide's example (spam vs legitimate email) matches CS229's canonical framing.

## Open questions

- [?] Slide phrasing "Designing algorithms that can learn patterns from data
  (and exploit them)" — close to wording used in several intro decks (e.g.,
  Andrew Ng's CS229 lecture-1 slide "What is Machine Learning?"). Exact deck not
  verified this run (search engines blocked); content is standard regardless.
