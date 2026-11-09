# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "numpy",
#     "pandas",
#     "plotly>=5.24",
# ]
# ///
"""Dialekt-Test für Deutschland (marimo notebook).

Inspired by the Tages-Anzeiger "Dialekt-Test". Data: the "Grüezi, Moin,
Servus!" app (Leemann, Derungs & Elspaß 2019, PLoS ONE, https://osf.io/49tcj/),
aggregated to German districts with prepare_data.py. Runs locally and in the
browser (marimo.app / WASM).
"""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Dialekt-Test Deutschland")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🇩🇪 Dialekt-Test: Woher in Deutschland kommen Sie?

    Wählen Sie bei jeder Frage das Wort, das Sie selbst verwenden.
    **Jede Auswahl aktualisiert die Karte sofort.** Je dunkler ein Kreis,
    desto typischer sind Ihre Antworten für die Menschen dort.

    Datengrundlage: 674 000 Teilnehmende aus Deutschland der App
    *Grüezi, Moin, Servus!* ([Leemann, Derungs & Elspaß 2019](https://doi.org/10.1371/journal.pone.0225399),
    Daten: [osf.io/49tcj](https://osf.io/49tcj/)), ausgezählt pro Land- bzw. Stadtkreis.
    Idee nach dem [Dialekt-Test des Tages-Anzeigers](https://www.tagesanzeiger.ch/dialekt-test-wir-wissen-woher-sie-stammen-jetzt-noch-genauer-205060715129).
    """)
    return


@app.cell
def _():
    import io
    import json
    import sys

    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    return go, io, json, mo, np, pd, sys


@app.cell
def _(io, json, mo, pd, sys):
    DATA_URL = (
        "https://raw.githubusercontent.com/observingClouds/observingClouds/"
        "ccr-88fa4154-ofsc6h/dialekt-test-de/data/"
    )

    def read_text(name):
        """Local file if available, otherwise download (works in WASM too)."""
        try:
            local = mo.notebook_dir() / "data" / name
            if local.exists():
                return local.read_text(encoding="utf-8")
        except Exception:
            pass
        if "pyodide" in sys.modules:
            from pyodide.http import open_url

            return open_url(DATA_URL + name).getvalue()
        import urllib.request

        with urllib.request.urlopen(DATA_URL + name, timeout=60) as r:
            return r.read().decode("utf-8")

    kreise_geo = json.loads(read_text("kreise.geojson"))
    answers = pd.read_csv(io.StringIO(read_text("answers.csv")))
    questions = pd.read_csv(io.StringIO(read_text("questions.csv")))
    return answers, kreise_geo, questions


@app.cell
def _(answers, kreise_geo, pd):
    kreise = pd.DataFrame([f["properties"] for f in kreise_geo["features"]]).set_index("id")

    # counts[frage] -> DataFrame (kreis x antwort), all kreise present
    counts = {
        q: g.pivot_table(index="kreis", columns="antwort", values="n", fill_value=0)
        .reindex(kreise.index, fill_value=0)
        for q, g in answers.groupby("frage")
    }
    # answer options ordered by overall frequency in Germany
    options = {
        q: list(c.sum().sort_values(ascending=False).index) for q, c in counts.items()
    }
    return counts, kreise, options


@app.cell(hide_code=True)
def _(kreise, mo):
    prefill = mo.ui.dropdown(
        options={
            f"{r.label} – {r.land}": i for i, r in kreise.sort_values("label").iterrows()
        },
        value=None,
        searchable=True,
        label="Antworten vorausfüllen wie in … (typischste Antworten eines Kreises)",
    )
    alpha = mo.ui.slider(
        start=1, stop=200, step=1, value=20, show_value=True,
        label="Glättung (Pseudo-Antworten aus Deutschland-Mittel)",
    )
    mo.vstack([mo.md("## 1 · Einstellungen"), mo.hstack([prefill, alpha], wrap=True, justify="start", gap=2)])
    return alpha, prefill


@app.cell
def _(counts, mo, options, prefill, questions):
    NO_ANSWER = "– keine Angabe –"
    _dropdowns = {}
    for _, _q in questions.iterrows():
        _fid = int(_q["frage"])
        _default = NO_ANSWER
        if prefill.value is not None:
            _default = counts[_fid].loc[prefill.value].idxmax()
        _dropdowns[str(_fid)] = mo.ui.dropdown(
            options=[NO_ANSWER] + options[_fid],
            value=_default,
            label=f"**{_q['titel']}**",
            full_width=True,
        )
    answer_ui = mo.ui.dictionary(_dropdowns)
    return NO_ANSWER, answer_ui


@app.cell(hide_code=True)
def _(answer_ui, mo):
    _items = list(answer_ui.elements.values())
    _rows = [mo.hstack(_items[i : i + 3], widths="equal", gap=1) for i in range(0, len(_items), 3)]
    mo.vstack([mo.md("## 2 · Ihre Antworten"), *_rows])
    return


@app.cell
def _(NO_ANSWER, alpha, answer_ui, counts, kreise, np):
    chosen = {int(k): v for k, v in answer_ui.value.items() if v and v != NO_ANSWER}

    def share(fid, answer, a):
        """Smoothed share of `answer` per Kreis: (n + a*p_DE) / (N + a)."""
        c = counts[fid]
        n = c[answer].to_numpy(float)
        tot = c.sum(axis=1).to_numpy(float)
        p_de = c[answer].sum() / c.to_numpy().sum()
        return (n + a * p_de) / (tot + a)

    loglik = np.zeros(len(kreise))
    for _fid, _ans in chosen.items():
        loglik += np.log(share(_fid, _ans, alpha.value))

    k = max(len(chosen), 1)
    post = np.exp(loglik - loglik.max())
    post /= post.sum()
    result = kreise.assign(
        # geometric-mean likelihood per answer, relative to the best Kreis
        aehnlichkeit=np.exp((loglik - loglik.max()) / k),
        wahrscheinlichkeit=post,
    )
    return chosen, result, share


@app.cell(hide_code=True)
def _(chosen, go, kreise_geo, mo, result):
    BLUE = [[0.0, "#f1f6fd"], [0.2, "#cde2fb"], [0.4, "#86b6ef"], [0.6, "#3987e5"],
            [0.8, "#1c5cab"], [1.0, "#0d366b"]]

    def choropleth(z, df, colorbar_title, hover_value, height=600, zmin=None, zmax=None,
                   colorscale=BLUE):
        fig = go.Figure(
            go.Choroplethmap(
                geojson=kreise_geo, locations=df.index, z=z, featureidkey="id",
                colorscale=colorscale, zmin=zmin, zmax=zmax,
                marker=dict(line=dict(width=0.3, color="white"), opacity=0.9),
                colorbar=dict(title=colorbar_title, thickness=12, len=0.7),
                customdata=df[["label", "land"]].to_numpy(),
                hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>"
                + hover_value + "<extra></extra>",
            )
        )
        fig.update_layout(
            map=dict(style="carto-positron", center=dict(lat=51.2, lon=10.4), zoom=4.9),
            margin=dict(l=0, r=0, t=0, b=0), height=height,
        )
        return fig

    if not chosen:
        _out = mo.callout(mo.md("Beantworten Sie mindestens eine Frage – die Karte erscheint sofort."), kind="info")
    else:
        _top = result.sort_values("wahrscheinlichkeit", ascending=False)
        _best = _top.iloc[0]
        _fig = choropleth(
            result["aehnlichkeit"] * 100, result, "Ähnlichkeit %",
            "Ähnlichkeit: %{z:.0f} %", zmin=0, zmax=100,
        )
        _table = (
            _top.head(10)
            .assign(**{"Wahrsch. %": lambda d: (d["wahrscheinlichkeit"] * 100).round(1)})
            [["label", "land", "Wahrsch. %"]]
            .rename(columns={"label": "Kreis", "land": "Bundesland"})
            .reset_index(drop=True)
        )
        _out = mo.vstack([
            mo.md(
                f"## 3 · Resultat\nNach **{len(chosen)}** Antworten kommen Sie am "
                f"ehesten aus **{_best['label']}** ({_best['land']})."
            ),
            mo.hstack(
                [mo.ui.plotly(_fig),
                 mo.vstack([mo.md("**Top 10 Kreise**"),
                            mo.ui.table(_table, selection=None, page_size=10,
                                        show_column_summaries=False)])],
                widths=[3, 2], align="start",
            ),
        ])
    _out
    return (choropleth,)


@app.cell(hide_code=True)
def _(chosen, mo, questions):
    _opts = {r.titel: int(r.frage) for r in questions.itertuples()}
    _default = None
    if chosen:
        _default = questions.set_index("frage").loc[list(chosen)[-1], "titel"]
    else:
        _default = next(iter(_opts))
    detail_q = mo.ui.dropdown(options=_opts, value=_default, label="Frage", searchable=True)
    mo.vstack([mo.md("## 4 · Einzelne Frage im Detail"), detail_q])
    return (detail_q,)


@app.cell(hide_code=True)
def _(detail_q, mo, options):
    detail_a = mo.ui.dropdown(options=options[detail_q.value], value=options[detail_q.value][0],
                              label="Antwort", searchable=True)
    return (detail_a,)


@app.cell(hide_code=True)
def _(chosen, choropleth, counts, detail_a, detail_q, kreise, mo, questions):
    _fid = detail_q.value
    # follow the user's answer for this question if given, otherwise the dropdown
    _ans = chosen.get(_fid, detail_a.value)
    _c = counts[_fid]
    _share = _c[_ans] / _c.sum(axis=1) * 100
    _qtext = questions.set_index("frage").loc[_fid, "text"]
    _note = "(Ihre Antwort)" if _fid in chosen else ""
    mo.vstack([
        mo.md(f"*{_qtext}*"),
        detail_a if _fid not in chosen else mo.md(f"Antwort: **{_ans}** {_note}"),
        mo.md(f"Anteil der Teilnehmenden, die **{_ans}** sagen:"),
        mo.ui.plotly(choropleth(_share, kreise, "Anteil %", "Anteil: %{z:.0f} %",
                                height=520, zmin=0)),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    **Methode.** Für jede Frage wird pro Kreis der Anteil der Teilnehmenden mit Ihrer Antwort
    berechnet (geglättet mit Pseudo-Antworten aus dem Deutschland-Mittel). Das Produkt dieser
    Anteile ist die Wahrscheinlichkeit Ihrer Antwortkombination in jedem Kreis (naiver Bayes,
    gleiche Vorab-Wahrscheinlichkeit für alle Kreise). Die Karte zeigt die *Ähnlichkeit*:
    das geometrische Mittel pro Antwort relativ zum besten Kreis.

    **Quellen:** Leemann A, Derungs C, Elspaß S (2019): *Analyzing linguistic variation and change
    using gamification web apps: The case of German-speaking Europe.* PLoS ONE 14(12): e0225399 –
    Daten [osf.io/49tcj](https://osf.io/49tcj/). Kreisgrenzen:
    [deutschlandGeoJSON](https://github.com/isellsoap/deutschlandGeoJSON) (GADM).
    """)
    return


if __name__ == "__main__":
    app.run()
