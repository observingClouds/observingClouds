# Dialekt-Test (marimo)

An interactive Swiss German dialect test, built as a [marimo](https://marimo.io)
notebook and inspired by the
[Tages-Anzeiger Dialekt-Test](https://www.tagesanzeiger.ch/dialekt-test-wir-wissen-woher-sie-stammen-jetzt-noch-genauer-205060715129).

Pick the form you would say for each question. **Every selection updates the
map right away.** It shows how well each place's traditional dialect matches
your answers, and it names the most likely place of origin.

```bash
uvx marimo run --sandbox dialekt-test/dialekt_test.py    # app view
uvx marimo edit --sandbox dialekt-test/dialekt_test.py   # edit the notebook
```

## Data

The data comes from the digitized maps of the *Sprachatlas der deutschen Schweiz* (SDS), version 3:
289 maps and 565 survey locations, published by Y. Scherrer, S. Kellerhals and R. Weiss on
[dialektkarten.ch](https://dialektkarten.ch/mapviewer/swg/index.de.html).
The notebook downloads `featuremaps.json` and `points.geojson` on its first run
and caches them in `dialekt-test/data/`, which is git-ignored.

## Features

- 20 default questions in Tagi style (Schluckauf, Splitter, Zahn, Apfel, …).
  You can add or remove any of the 289 SDS maps.
- A match score for each location, with optional Gaussian spatial smoothing,
  plus a map, the best guess and a top-10 table.
- A detail map for each question that shows the distribution of variants and highlights your answer.
- "Antworten vorausfüllen wie in …" fills in all answers as a chosen village would give them.
  Use it to try the test out.
