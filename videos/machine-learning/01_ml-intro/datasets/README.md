# Canonical IRIS dataset (founder directive 2026-10-10)

- `iris.csv` — THE canonical file (150 rows: sepal_length, sepal_width, petal_length,
  petal_width, species). Generated from `sklearn.datasets.load_iris()` and round-trip
  verified against it. Every table AND every graph script for slides 60-64 reads THIS
  file — no hardcoded rows, no other snapshot.
- `iris.data` — raw UCI download (https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data),
  kept as provenance only. NOTE: UCI's file carries the two famous Fisher data-entry
  errata (0-indexed rows 34 and 37); sklearn's dataset has them corrected, so UCI and
  sklearn differ in exactly those 2 rows. sklearn's corrected values are canonical here
  because all graphgen scripts already run on sklearn data — using the UCI errata would
  make tables and graphs inconsistent.
