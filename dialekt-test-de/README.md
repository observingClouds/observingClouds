# Dialekt-Test Deutschland (marimo)

An interactive dialect test for Germany, built as a [marimo](https://marimo.io) notebook.
It's the German counterpart to `../dialekt-test` (Switzerland). Pick the word you use for each
of 14 everyday things (Pfannkuchen, Frikadelle, Brotanschnitt, …). **Every selection updates the
choropleth map of all 434 districts right away**, along with the most likely district and a top-10 list.

```bash
uvx marimo run --sandbox dialekt-test-de/dialekt_test_de.py
```

It also runs in the browser via marimo.app (WASM). The data is loaded from this repository's raw GitHub URL.

## Data

- **Answers:** 674,000 participants from Germany in the *Grüezi, Moin, Servus!* app.
  Leemann, Derungs & Elspaß (2019), PLoS ONE 14(12): e0225399, data at <https://osf.io/49tcj/>.
  `prepare_data.py` counts the answers per district (`data/answers.csv`).
- **District boundaries:** simplified from [deutschlandGeoJSON](https://github.com/isellsoap/deutschlandGeoJSON)
  (GADM, `data/kreise.geojson`). These are older district boundaries, from before the reforms in Saxony,
  Saxony-Anhalt and Mecklenburg-Vorpommern.

## Method

The notebook treats each district's answer shares as probabilities and scores your answers with naive Bayes,
with additive smoothing toward the national average. The map shows the per-answer geometric-mean likelihood
relative to the best district.

**Check:** answering with each district's most common words recovers the exact district (out of 434) 35% of the
time and the right Bundesland 91% of the time.
