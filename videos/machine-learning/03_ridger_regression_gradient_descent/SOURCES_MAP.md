# SOURCES_MAP.md — machine-learning lecture 03: Ridge Regression & Gradient Descent

Fleet-level map for the web-source research mandate (founder directive 2026-10-19).
Contract: `~/.zcode/skills/slide-recreation/references/source-research.md`.
Per-slide records: `sources/slide_NNN_source/SOURCES.md` (no SOURCES.md = the leg
did not happen). This map is APPEND-ONLY; rows are added by the orchestrator as
per-slide records land. Never edit or delete a row once written.

## Method + query budget

- Search: agy CLI (`agy -p "<query>"`; token mint `agy -p "hi"` on auth errors).
- Fetch: WebFetch live in the same work window that records the URL; figures
  downloaded as-served, hash-verified (re-fetch byte-compare).
- Query budget disclosure lives in each worker's final report; totals appended
  here per wave by the orchestrator.

## Confidence legend

- **CONFIRMED** — fetched + verified against the live source, quotes recorded.
- **origin-level** — provenance known from a banked record (sibling SOURCES.md).
- **[?]** — unresolved; debt-recorded; re-runs when the window reopens.

## Slide → source table (appended as research lands)

| Slide | Title (short) | Source(s) | Level | SOURCES.md |
|---|---|---|---|---|
| 001 | Ridge Regression, Gradient Descent, And Perceptron | Zewail City course-catalog CMS API (`zcadminpanel.zewailcity.edu.eg/api/courses/264` + member 53), fetched live HTTP 200 | CONFIRMED | `sources/slide_001_source/SOURCES.md` |
| 002 | Revision of Standard Linear Regression Model | none needed (section divider, no external claims) — cross-referenced slide 001 | origin-level | `sources/slide_002_source/SOURCES.md` |
| 008 | [1] Ridge Regularizer to Minimize Overfitting | Wikipedia Ridge regression (re-fetched live this window, HTTP 200) + origin-level cross-refs to Overfitting (slide_007_source) and Euclidean norm (slide_004_source) | CONFIRMED | `sources/slide_008_source/SOURCES.md` |
| 009 | Overfit vs. Generalized | Wikipedia Overfitting (banked slide_007_source, re-confirmed live) + Ridge regression (origin-level ref), fetched live | CONFIRMED | `sources/slide_009_source/SOURCES.md` |
| 010 | Overfit vs. Generalized Model Fits | Wikipedia Overfitting + Ridge regression/Tikhonov regularization, fetched live | CONFIRMED | `sources/slide_010_source/SOURCES.md` |
| 003 | Matrix Notation for Linear Regression and Classification | CS229 lecture notes (`cs229-notes1.pdf`, serve.stanford.edu), fetched live HTTP 200 | CONFIRMED | `sources/slide_003_source/SOURCES.md` |
| 011 | Example of Overfitting due to outlier in data | Wikipedia Robust regression (+ Overfitting/Outlier origin-level refs), fetched live | CONFIRMED | `sources/slide_011_source/SOURCES.md` |
| 012 | Effect of Overfitting on model parameter "W" | Wikipedia Robust regression + Outlier (+ Ridge regression origin-level ref), fetched live | CONFIRMED | `sources/slide_012_source/SOURCES.md` |
| 004 | Concept of LOSS Function | UPenn CIS5150 slides + CS229 notes1 + Wikipedia Euclidean norm / Ridge regression, fetched live | CONFIRMED | `sources/slide_004_source/SOURCES.md` |
| 013 | (ridge inverse-problem table slide) | Wikipedia Ridge regression (+ Robust regression/Overfitting origin-level refs), fetched live | CONFIRMED | `sources/slide_013_source/SOURCES.md` |
| 019 | (ridge solution slide) | Wikipedia Ridge regression + Gradient descent, fetched live HTTP 200 | CONFIRMED | `sources/slide_019_source/SOURCES.md` |
| 020 | [2] Ridge Regularization to overcome Inverse Problem of Singular Matrix | Wikipedia Ridge regression + Invertible matrix + CS229 2021 notes1, fetched live | CONFIRMED | `sources/slide_020_source/SOURCES.md` |
| 021 | Inverse Problem of Singular Matrix | Wikipedia Invertible matrix + Ridge regression (origin-level) + CS229 2021 notes1, fetched live | CONFIRMED | `sources/slide_021_source/SOURCES.md` |
| 005 | Minimization of Loss function to obtain BEST model parameters | CS229 notes1 (cs229.stanford.edu + see.stanford.edu), fetched live | CONFIRMED | `sources/slide_005_source/SOURCES.md` |
| 006 | Problems of Linear Regression | none needed (section divider, course-authored labels) | origin-level | `sources/slide_006_source/SOURCES.md` |
| 014 | (sources slide 014) | Wikipedia Lasso/Overfitting/Ridge regression (incl. Tikhonov anchor), fetched live | CONFIRMED | `sources/slide_014_source/SOURCES.md` |
| 015 | (sources slide 015) | Wikipedia Matrix calculus / Ridge regression / Tikhonov regularization, fetched live | CONFIRMED | `sources/slide_015_source/SOURCES.md` |
| 016 | (sources slide 016) | Wikipedia Lasso/Overfitting/Ridge regression + ICML 2004 paper (Lasso/Tikhonov comparison), fetched live | CONFIRMED | `sources/slide_016_source/SOURCES.md` |
| 022 | [3] Inverse of High Dimension | CS229 2021 notes1 + Wikipedia Gaussian elimination / Invertible matrix, fetched live | CONFIRMED | `sources/slide_022_source/SOURCES.md` |
| 023 | Inverse of High Dimension Matrix | CS229 main notes PDF + CS229 2021 fall notes1 + Wikipedia Gaussian elimination / Computational complexity (×3) / Gradient descent / Ridge regression, fetched live | CONFIRMED | `sources/slide_023_source/SOURCES.md` |
| 037 | (perceptron/GD slide 037) | Illinois CS440 lecture notes + Wikipedia Gradient descent / Perceptron + NEU MLcourse perceptron PDF, fetched live | CONFIRMED | `sources/slide_037_source/SOURCES.md` |
| 038 | Gradient Descent (GD) vs Stochastic Gradient Descent (SGD) | CS231n optimization-1 + Wikipedia GD/SGD + scikit-learn SGD docs, fetched live | CONFIRMED | `sources/slide_038_source/SOURCES.md` |
| 039 | (perceptron slide 039) | CS231n optimization-1 + Wikipedia Perceptron/SGD + scikit-learn SGD docs + NEU MLcourse PDF, fetched live | CONFIRMED | `sources/slide_039_source/SOURCES.md` |
| 040 | (perceptron slide 040) | Wikipedia Perceptron/SGD + scikit-learn SGD docs + NEU MLcourse PDF, fetched live | CONFIRMED | `sources/slide_040_source/SOURCES.md` |
| 007 | Problems of Linear Regression | Wikipedia Multicollinearity + Numerical methods for linear least squares + Overfitting, fetched live | CONFIRMED | `sources/slide_007_source/SOURCES.md` |
| 017 | (perceptron/GD tables slide 017) | Wikipedia Ridge regression/Robust regression + ICML 2004 paper #354, fetched live | CONFIRMED | `sources/slide_017_source/SOURCES.md` |
| 018 | (weight-update worked example) | Wikipedia Matrix calculus/Ridge regression/Robust regression, fetched live | CONFIRMED | `sources/slide_018_source/SOURCES.md` |
| 024 | Gradient Descent (GD) | CS229 2021 notes1 + Wikipedia Gradient descent/Loss function, fetched live | CONFIRMED | `sources/slide_024_source/SOURCES.md` |
| 025 | Types of Loss function shapes | Wikipedia Convex function + Gradient descent + Linear least squares + Loss function, all fetched live this window (hash-verified) | CONFIRMED | `sources/slide_025_source/SOURCES.md` |
| 027 | Follow Negative Direction of Gradient with Selected Learning Rate | Wikipedia Convex function (banked, byte-identical to sibling copy) + Gradient descent + Linear least squares, all fetched live, re-fetch byte-identical | CONFIRMED | `sources/slide_027_source/SOURCES.md` |
| 028 | Effect of small and large Learning Rate | arXiv 1609.04747 + CS229 2020 notes1, fetched live | CONFIRMED | `sources/slide_028_source/SOURCES.md` |
| 029 | Example: gradient descent minima | none needed (course-authored worked example) | origin-level | `sources/slide_029_source/SOURCES.md` |
| 030 | Convex Function, Learning Rate=0.2, Start at X=3 | arXiv 1609.04747 + CS229 2020 notes1, fetched live | CONFIRMED | `sources/slide_030_source/SOURCES.md` |
| 031 | (GD example slide 031) | none needed (course-authored worked example) | origin-level | `sources/slide_031_source/SOURCES.md` |
| 032 | (perceptron slide 032) | none needed (course-authored worked example) | origin-level | `sources/slide_032_source/SOURCES.md` |
| 033 | (perceptron slide 033) | none needed (course-authored worked example) | origin-level | `sources/slide_033_source/SOURCES.md` |
| 034 | (perceptron slide 034) | none needed (course-authored worked example) | origin-level | `sources/slide_034_source/SOURCES.md` |
| 035 | Using Gradient Descent to train Linear Regression Model | Wikipedia GD/Loss cluster + arXiv 1609.04747 + CS229 notes (economy-law cross-reference), fetched live | origin-level | `sources/slide_035_source/SOURCES.md` |
| 036 | (GD/learning-rate slide 036) | arXiv 1609.04747 + CS229 notes, fetched live | CONFIRMED | `sources/slide_036_source/SOURCES.md` |
| 041 | (perceptron slide 041) | Wikipedia Perceptron/SGD + NEU MLcourse perceptron PDF, fetched live | CONFIRMED | `sources/slide_041_source/SOURCES.md` |
| 042 | (perceptron slide 042) | Illinois CS440 lect26 + Wikipedia Perceptron + NEU MLcourse PDF, fetched live | CONFIRMED | `sources/slide_042_source/SOURCES.md` |
| 043 | (perceptron slide 043) | Illinois CS440 lect26 + Wikipedia Perceptron + NEU MLcourse PDF, fetched live | CONFIRMED | `sources/slide_043_source/SOURCES.md` |
| 044 | (perceptron slide 044) | Illinois CS440 lect26 + Wikipedia Perceptron + NEU MLcourse PDF, fetched live | CONFIRMED | `sources/slide_044_source/SOURCES.md` |
| 045 | (perceptron slide 045) | CMU 07-815 Perceptron Learning Algorithm & Convergence PDF + Wikipedia Perceptron + UPenn CIS5190 lecture, fetched live | CONFIRMED | `sources/slide_045_source/SOURCES.md` |
| 046 | (perceptron slide 046) | CMU 07-815 PDF + Wikipedia Perceptron + UPenn CIS5190 lecture, fetched live | CONFIRMED | `sources/slide_046_source/SOURCES.md` |
| 047 | (perceptron slide 047) | CMU 07-815 PDF + Wikipedia Perceptron + UPenn CIS5190 lecture, fetched live | CONFIRMED | `sources/slide_047_source/SOURCES.md` |
| 048 | Iteration 1: Weight Update using Step η = 1 | CMU 07-815 PDF + Wikipedia Perceptron + UPenn CIS5190 lecture, fetched live | CONFIRMED | `sources/slide_048_source/SOURCES.md` |
| 049 | (perceptron slide 049) | CMU 07-815 PDF + Wikipedia Perceptron + UPenn CIS5190 lecture, fetched live | CONFIRMED | `sources/slide_049_source/SOURCES.md` |
| 050 | (perceptron decision slide 050) | CMU 07-815 PDF + Wikipedia Perceptron + UPenn CIS5190 lecture, fetched live | CONFIRMED | `sources/slide_050_source/SOURCES.md` |
| 051 | (perceptron decision slide 051) | CMU 07-815 PDF + Wikipedia Perceptron + UPenn CIS5190 lecture, fetched live | CONFIRMED | `sources/slide_051_source/SOURCES.md` |
| (pending — rows appended as per-slide records land) | | | | |

## Failed findings / do-not-reuse (hallucinated or dead URLs)

- `https://www.eecs189.org/static/notes/n5.pdf` — dead (reported by wave-1 001-009; fetch failure).
- `https://lcnwww.epfl.ch/gerstner/PUBLICATIONS/01Lecture02Perceptron.pdf` — unreachable from this host (curl 000; wave-2 028-036 substituted Cornell CS4780 lectures + Wikipedia Perceptron + CS229 notes §6).
- `https://stats.stackexchange.com/questions/475517/...` — NOT dead, but fetch-blocked by a Cloudflare interstitial twice; unverifiable content, debt-recorded in `sources/slide_011_source/SOURCES.md` — treat as unverified, do not cite without a live re-fetch.
