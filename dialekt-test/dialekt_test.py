# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "numpy",
#     "pandas",
#     "plotly>=5.24",
# ]
# ///
"""Interactive Swiss German dialect test (marimo notebook).

Inspired by the Tages-Anzeiger "Dialekt-Test". The underlying data are the
digitised maps of the *Sprachatlas der deutschen Schweiz* (SDS) published by
Yves Scherrer et al. on https://dialektkarten.ch (version 3, 289 maps,
565 survey locations).

Run with:  marimo edit --sandbox dialekt_test.py   (or: marimo run ...)
"""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Dialekt-Test")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🇨🇭 Dialekt-Test: Woher stammen Sie?

    Wählen Sie für jede Frage die Form, die Sie selbst sagen würden.
    **Jede Auswahl aktualisiert die Karte sofort**: Je dunkler ein Ort,
    desto besser passen seine Dialektformen zu Ihren Antworten.

    Die Daten stammen aus dem *Sprachatlas der deutschen Schweiz* (SDS),
    digitalisiert und frei publiziert auf
    [dialektkarten.ch](https://dialektkarten.ch) (Scherrer, Kellerhals, Weiss).
    Die Idee folgt dem
    [Dialekt-Test des Tages-Anzeigers](https://www.tagesanzeiger.ch/dialekt-test-wir-wissen-woher-sie-stammen-jetzt-noch-genauer-205060715129).
    """)
    return


@app.cell
def _():
    import json
    import pathlib
    import sys
    import urllib.request

    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go

    return go, json, mo, np, pathlib, pd, sys, urllib


@app.cell
def _(json, mo, pathlib, sys, urllib):
    # Mirror of the dialektkarten.ch files in this repo: GitHub serves them with
    # CORS headers, so the notebook also works in the browser (marimo.app/WASM).
    MIRROR_URL = (
        "https://raw.githubusercontent.com/observingClouds/observingClouds/"
        "ccr-88fa4154-ofsc6h/dialekt-test/sds_v3/"
    )
    ORIGINAL_URL = "https://dialektkarten.ch/static/geojson/swg_v3/"

    def fetch_json(name):
        """Load an SDS file: local copy, else GitHub mirror (WASM), else original."""
        try:
            local = pathlib.Path(mo.notebook_dir()) / "sds_v3" / name
            if local.exists():
                return json.loads(local.read_text(encoding="utf-8"))
        except Exception:
            pass
        if "pyodide" in sys.modules:
            from pyodide.http import open_url

            return json.loads(open_url(MIRROR_URL + name).getvalue())
        req = urllib.request.Request(
            ORIGINAL_URL + name, headers={"User-Agent": "marimo-dialekt-test"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))

    featuremaps_raw = fetch_json("featuremaps.json")
    points_raw = fetch_json("points.geojson")
    return featuremaps_raw, points_raw


@app.cell
def _(featuremaps_raw, np, pd, points_raw):
    # --- survey locations -------------------------------------------------
    points = pd.DataFrame(
        [
            {
                "point": f["id"],
                "ort": f["properties"]["name"],
                "kanton": "".join(c for c in f["id"] if c.isalpha()),
                "lon": f["geometry"]["coordinates"][0],
                "lat": f["geometry"]["coordinates"][1],
            }
            for f in points_raw["features"]
        ]
    ).set_index("point")

    # --- long table: one row per (map, variant, point) -----------------------
    maps = {m["fileid"]: m for m in featuremaps_raw}
    observations = pd.DataFrame(
        [
            {"map": m["fileid"], "variant": v["id"], "point": p}
            for m in featuremaps_raw
            for v in m["variants"]
            for p in v["points"]
        ]
    )
    observations = observations[observations["point"].isin(points.index)]

    # --- pairwise distances (km) for the spatial smoothing -----------------
    _lat = np.radians(points["lat"].to_numpy())
    _lon = np.radians(points["lon"].to_numpy())
    _a = (
        np.sin((_lat[:, None] - _lat[None, :]) / 2) ** 2
        + np.cos(_lat[:, None])
        * np.cos(_lat[None, :])
        * np.sin((_lon[:, None] - _lon[None, :]) / 2) ** 2
    )
    dist_km = 2 * 6371.0 * np.arcsin(np.sqrt(_a))
    return dist_km, maps, observations, points


@app.cell
def _(maps):
    # A Tagi-style default questionnaire: mostly lexical items that are easy
    # to answer. Any of the 289 SDS maps can be added below.
    DEFAULT_QUESTIONS = [
        "4071_Schluckauf",
        "4029_Splitter",
        "4067_niesen",
        "4019_Zahn",
        "4013_Augenbrauen",
        "4007_Zöpfe",
        "1160_Apfel",
        "1061_Abend",
        "1138_Knie",
        "4155_ein_wenig",
        "4167_nicht",
        "4181_sonst",
        "6026_immer",
        "6027_jeweils",
        "6029_früher",
        "6042_Wolke",
        "5059_Christbaum",
        "5112_gruss",
        "7076_flicken",
        "7089_Seife",
    ]
    DEFAULT_QUESTIONS = [q for q in DEFAULT_QUESTIONS if q in maps]
    map_titles = {m["title"]: fid for fid, m in maps.items()}
    return DEFAULT_QUESTIONS, map_titles


@app.cell(hide_code=True)
def _(DEFAULT_QUESTIONS, map_titles, maps, mo, points):
    question_picker = mo.ui.multiselect(
        options=map_titles,
        value=[maps[q]["title"] for q in DEFAULT_QUESTIONS],
        label="Fragen (SDS-Karten)",
        full_width=True,
    )
    _place_options = {
        f"{row.ort} ({pid})": pid
        for pid, row in points.sort_values("ort").iterrows()
    }
    prefill = mo.ui.dropdown(
        options=_place_options,
        value=None,
        searchable=True,
        label="Antworten vorausfüllen wie in … (optional, zum Ausprobieren)",
    )
    smoothing = mo.ui.slider(
        start=0, stop=30, step=1, value=8, show_value=True,
        label="Räumliche Glättung (km)",
    )
    mo.vstack(
        [
            mo.md("## 1 · Fragebogen zusammenstellen"),
            question_picker,
            mo.hstack([prefill, smoothing], justify="start", gap=2, wrap=True),
        ]
    )
    return prefill, question_picker, smoothing


@app.cell
def _(maps, mo, observations, prefill, question_picker):
    NO_ANSWER = "– keine Angabe –"

    _prefill_variant = {}
    if prefill.value is not None:
        _obs = observations[observations["point"] == prefill.value]
        # first attested variant of that place per map
        _prefill_variant = _obs.groupby("map")["variant"].first().to_dict()

    _dropdowns = {}
    for _fid in question_picker.value:
        _m = maps[_fid]
        _opts = {NO_ANSWER: None}
        for _v in _m["variants"]:
            _opts[_v["name"]] = _v["id"]
        _default = NO_ANSWER
        if _fid in _prefill_variant:
            _default = next(
                lbl for lbl, vid in _opts.items() if vid == _prefill_variant[_fid]
            )
        _dropdowns[_fid] = mo.ui.dropdown(
            options=_opts, value=_default, label=f"**{_m['title']}**",
            full_width=True,
        )
    answers = mo.ui.dictionary(_dropdowns)
    return (answers,)


@app.cell(hide_code=True)
def _(answers, mo):
    _items = list(answers.elements.values())
    _rows = [mo.hstack(_items[i : i + 3], widths="equal", gap=1) for i in range(0, len(_items), 3)]
    mo.vstack(
        [
            mo.md(
                "## 2 · Ihre Antworten\n"
                "Bei lautlichen Fragen bezieht sich die Auswahl auf den Laut in "
                "eckigen Klammern, z. B. `[A]pfel` → *ö* = «Öpfel»."
            ),
            *_rows,
        ]
    )
    return


@app.cell
def _(answers, dist_km, np, observations, pd, points, smoothing):
    chosen = {fid: vid for fid, vid in answers.value.items() if vid is not None}

    n_pts = len(points)
    hits = np.zeros(n_pts)
    counts = np.zeros(n_pts)
    _pidx = pd.Series(np.arange(n_pts), index=points.index)

    for _fid, _vid in chosen.items():
        _obs = observations[observations["map"] == _fid]
        _attested = _pidx[_obs["point"].unique()].to_numpy()
        _match = _pidx[_obs.loc[_obs["variant"] == _vid, "point"].unique()].to_numpy()
        counts[_attested] += 1
        hits[_match] += 1

    # Spatially smoothed share of matching answers (Gaussian kernel)
    if smoothing.value > 0:
        _w = np.exp(-0.5 * (dist_km / smoothing.value) ** 2)
    else:
        _w = np.eye(n_pts)
    with np.errstate(invalid="ignore", divide="ignore"):
        raw_score = np.where(counts > 0, hits / np.maximum(counts, 1), np.nan)
        score = (_w @ hits) / (_w @ counts)

    result = points.assign(
        treffer=hits.astype(int),
        fragen=counts.astype(int),
        anteil=raw_score,
        score=score,
    )
    n_answered = len(chosen)
    return chosen, n_answered, result


@app.cell(hide_code=True)
def _(go, mo, n_answered, result):
    BLUE_RAMP = [
        [0.0, "#cde2fb"], [0.25, "#86b6ef"], [0.5, "#3987e5"],
        [0.75, "#1c5cab"], [1.0, "#0d366b"],
    ]

    def score_map(df):
        df = df.dropna(subset=["score"]).sort_values("score")
        best = df.iloc[-1] if len(df) else None
        fig = go.Figure()
        fig.add_trace(
            go.Scattermap(
                lon=df["lon"], lat=df["lat"], mode="markers",
                marker=dict(
                    size=9, color=df["score"] * 100, colorscale=BLUE_RAMP,
                    cmin=float(df["score"].min() * 100) if len(df) else 0,
                    cmax=100,
                    colorbar=dict(title="Übereinstimmung %", thickness=12),
                ),
                customdata=df[["ort", "kanton", "treffer", "fragen"]].to_numpy(),
                hovertemplate=(
                    "<b>%{customdata[0]}</b> (%{customdata[1]})<br>"
                    "geglättet: %{marker.color:.0f} %<br>"
                    "Treffer am Ort: %{customdata[2]} / %{customdata[3]}"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )
        if best is not None:
            fig.add_trace(
                go.Scattermap(
                    lon=[best["lon"]], lat=[best["lat"]], mode="markers+text",
                    marker=dict(size=18, color="#eb6834"),
                    text=[f"  {best['ort']}"], textposition="middle right",
                    textfont=dict(size=14, color="#0b0b0b"),
                    hoverinfo="skip", showlegend=False,
                )
            )
        fig.update_layout(
            map=dict(style="carto-positron", center=dict(lat=46.85, lon=8.2), zoom=6.4),
            margin=dict(l=0, r=0, t=0, b=0), height=520,
        )
        return fig

    if n_answered == 0:
        _out = mo.callout(
            mo.md("Beantworten Sie mindestens eine Frage – die Karte erscheint sofort."),
            kind="info",
        )
    else:
        _top = result.dropna(subset=["score"]).sort_values("score", ascending=False)
        _best = _top.iloc[0]
        _table = (
            _top.head(10)
            .assign(**{"Übereinstimmung %": lambda d: (d["score"] * 100).round(1)})
            [["ort", "kanton", "Übereinstimmung %"]]
            .rename(columns={"ort": "Ort", "kanton": "Kt."})
            .reset_index(drop=True)
        )
        _out = mo.vstack(
            [
                mo.md(
                    f"## 3 · Resultat\n"
                    f"Nach **{n_answered}** Antworten stammen Sie am ehesten aus "
                    f"**{_best['ort']} ({_best['kanton']})** – "
                    f"{_best['score'] * 100:.0f} % Übereinstimmung."
                ),
                mo.hstack(
                    [
                        mo.ui.plotly(score_map(result)),
                        mo.vstack([mo.md("**Top 10 Orte**"), mo.ui.table(_table, selection=None, page_size=10, show_column_summaries=False)]),
                    ],
                    widths=[2, 1], align="start",
                ),
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _(chosen, maps, mo, question_picker):
    _opts = {maps[f]["title"]: f for f in question_picker.value}
    _default = None
    if chosen:
        _default = maps[list(chosen)[-1]]["title"]
    elif _opts:
        _default = next(iter(_opts))
    detail_picker = mo.ui.dropdown(
        options=_opts, value=_default, label="Karte einer einzelnen Frage anzeigen",
        searchable=True,
    )
    mo.vstack([mo.md("## 4 · Einzelne Frage im Detail"), detail_picker])
    return (detail_picker,)


@app.cell(hide_code=True)
def _(chosen, detail_picker, go, maps, mo, observations, points):
    SLOTS = ["#2a78d6", "#eb6834", "#1baf7a"]  # validated all-pairs (first 3)
    OTHER = "#a3a29c"

    def variant_map(fid, chosen_vid):
        m = maps[fid]
        variants = sorted(m["variants"], key=lambda v: -v["nbpoints"])
        if chosen_vid is not None:
            variants = [v for v in variants if v["id"] == chosen_vid] + [
                v for v in variants if v["id"] != chosen_vid
            ]
        shown = variants[:3]
        obs = observations[observations["map"] == fid]
        # first-listed variant per point decides its colour
        order = {v["id"]: i for i, v in enumerate(variants)}
        obs = obs.assign(rank=obs["variant"].map(order)).sort_values("rank")
        first = obs.drop_duplicates("point").set_index("point")["variant"]
        names = {v["id"]: v["name"] for v in m["variants"]}
        all_variants = obs.groupby("point")["variant"].apply(
            lambda s: ", ".join(names[x] for x in s)
        )
        df = points.join(first.rename("variant"), how="inner")
        df["alle"] = all_variants

        fig = go.Figure()
        groups = [(v["id"], v["name"], SLOTS[i]) for i, v in enumerate(shown)]
        shown_ids = {g[0] for g in groups}
        others = df[~df["variant"].isin(shown_ids)]
        if len(others):
            fig.add_trace(make_trace(others, "Andere", OTHER, 7))
        for vid, name, color in reversed(groups):
            sub = df[df["variant"] == vid]
            label = name + (" ← Ihre Antwort" if vid == chosen_vid else "")
            fig.add_trace(make_trace(sub, label, color, 10 if vid == chosen_vid else 8))
        fig.update_layout(
            map=dict(style="carto-positron", center=dict(lat=46.85, lon=8.2), zoom=6.4),
            margin=dict(l=0, r=0, t=0, b=0), height=480,
            legend=dict(y=0.98, yanchor="top", x=0.01, xanchor="left",
                        traceorder="reversed", bgcolor="rgba(255,255,255,0.85)"),
        )
        return fig

    def make_trace(sub, name, color, size):
        return go.Scattermap(
            lon=sub["lon"], lat=sub["lat"], mode="markers", name=name,
            marker=dict(size=size, color=color),
            customdata=sub[["ort", "kanton", "alle"]].to_numpy(),
            hovertemplate="<b>%{customdata[0]}</b> (%{customdata[1]})<br>"
            "%{customdata[2]}<extra></extra>",
        )

    if detail_picker.value is None:
        _out = mo.md("_Keine Frage ausgewählt._")
    else:
        _fid = detail_picker.value
        _m = maps[_fid]
        _notes = "<br>".join(_m["comments"]) if _m["comments"] else ""
        _out = mo.vstack(
            [
                mo.ui.plotly(variant_map(_fid, chosen.get(_fid))),
                mo.md(f"<small>{_notes}</small>") if _notes else mo.md(""),
            ]
        )
    _out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    **Methode.** Für jede beantwortete Frage erhält jeder SDS-Ort eine 1,
    wenn dort Ihre Variante belegt ist, sonst eine 0 (Orte ohne Beleg zählen
    nicht). Der Anteil der Treffer wird mit einem Gauss-Kern (Breite = Glättung)
    über benachbarte Orte gemittelt; der Ort mit dem höchsten Wert ist die
    Schätzung. Die SDS-Erhebungen stammen aus den 1940er/50er-Jahren und bilden
    die traditionellen Ortsdialekte ab – moderne Sprecher weichen davon oft ab.

    **Quelle:** Sprachatlas der deutschen Schweiz (SDS), digitalisierte Karten
    v3 von [dialektkarten.ch](https://dialektkarten.ch/mapviewer/swg/index.de.html)
    (Y. Scherrer, S. Kellerhals, R. Weiss).
    """)
    return


if __name__ == "__main__":
    app.run()
