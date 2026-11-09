"""Aggregate the raw "Grüezi, Moin, Servus!" answers to German districts.

Input (not in this repo, ~700 MB):
  - LeemannEtAl_LingVar_data.zip from https://osf.io/49tcj/ (Leemann, Derungs &
    Elspaß 2019, PLoS ONE 14(12): e0225399)
  - Kreis boundaries (GADM-based) from
    https://github.com/isellsoap/deutschlandGeoJSON  (4_kreise/4_niedrig.geo.json)

Output (in ./data):
  - kreise.geojson   simplified district polygons with id, name, Bundesland
  - answers.csv      question, kreis, answer, n  (number of quiz participants)
  - questions.csv    question id, short title, original question text

Usage: python prepare_data.py <data.zip> <kreise.geo.json>
"""

import html
import json
import pathlib
import re
import sys
import zipfile

import numpy as np
import pandas as pd
import shapely
from shapely.geometry import mapping, shape

ZIP, KREISE = sys.argv[1], sys.argv[2]
OUT = pathlib.Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)

QUESTIONS = {  # id: (file stem, short title)
    1: ("1_Fussball", "Fußball spielen (in der Freizeit)"),
    2: ("2_vormittagsfruhstuck", "Frühstück am Arbeitsplatz"),
    4: ("4_Pfannekuchen", "Pfannkuchen"),
    5: ("5_Teigfigur", "Gebäckmann (St. Martin / Nikolaus)"),
    6: ("6_Frikadelle", "Frikadelle"),
    7: ("7_sich_unterhalten", "sich unterhalten"),
    8: ("8_Hausschuh", "Hausschuhe"),
    9: ("9_615", "Uhrzeit 10:15"),
    11: ("11_Steinschleuder", "Steinschleuder"),
    14: ("14_Schluckauf", "Schluckauf (zu Kindern)"),
    16: ("16_Geldborse", "Geldbörse"),
    18: ("18_Kartoffelbrei", "Kartoffelbrei"),
    21: ("21_Federetui", "Federmäppchen"),
    23: ("23_Kanten", "Anfangs-/Endstück des Brotes"),
}
MIN_ANSWERS_DE = 150  # drop variants (mostly Swiss/Austrian) rarely chosen in Germany

# --- districts --------------------------------------------------------------
gj = json.loads(pathlib.Path(KREISE).read_text(encoding="utf-8"))
feats = [f for f in gj["features"] if f["properties"]["TYPE_3"] != "Water body"]
# GADM names partly carry English exonyms and a "Städte" suffix
RENAME = {
    "Cologne": "Köln", "Cleves": "Kleve", "Munich": "München",
    "Nuremberg": "Nürnberg", "Hanover": "Region Hannover",
    "Hamelin-Pyrmont": "Hameln-Pyrmont", "Koblenz Coblenz": "Koblenz",
    "Speyer Spires": "Speyer", "Heilbronn city": "Heilbronn",
    "Main-Taunus-Kreis": "Main-Taunus-Kreis",
}
polys, kreise = [], []
for i, f in enumerate(feats):
    p = f["properties"]
    geom = shape(f["geometry"]).buffer(0)
    polys.append(geom)
    typ = "Stadt" if "Städte" in (p["TYPE_3"] or "") else "Kreis"
    name = p["NAME_3"].removesuffix(" Städte")
    name = RENAME.get(name, name)
    if name == "Main-Taunus-Kreis":
        typ = "Kreis"
    kreise.append({"id": i, "name": name, "typ": typ, "land": p["NAME_1"]})
_dups = pd.Series([k["name"] for k in kreise]).value_counts()
for k in kreise:
    k["label"] = k["name"]
    if _dups[k["name"]] > 1:
        k["label"] += " (Stadt)" if k["typ"] == "Stadt" else " (Landkreis)"
tree = shapely.STRtree(polys)

simplified = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": k["id"],
            "properties": k,
            "geometry": mapping(shapely.set_precision(g.simplify(0.008), 0.001)),
        }
        for k, g in zip(kreise, polys)
    ],
}
(OUT / "kreise.geojson").write_text(json.dumps(simplified, separators=(",", ":")))

# --- answers ----------------------------------------------------------------
z = zipfile.ZipFile(ZIP)
qtext = pd.read_csv(z.open("output/01/templateQuestions.csv"), encoding="latin-1")
qtext = qtext.set_index("uid")["name"].map(
    lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
)

rows = []
for qid, (stem, _) in QUESTIONS.items():
    df = pd.read_csv(
        z.open(f"output/01/allAnswer_{stem}.csv"),
        encoding="latin-1",
        usecols=["Antwort", "UserID", "lat", "lng"],
    ).drop_duplicates("UserID")
    df = df[df.lat.between(47.2, 55.1) & df.lng.between(5.8, 15.1)]
    pts = shapely.points(df.lng.to_numpy(), df.lat.to_numpy())
    ip, ik = tree.query(pts, predicate="within")
    kreis = np.full(len(df), -1)
    kreis[ip] = ik
    df = df.assign(kreis=kreis)
    df = df[df.kreis >= 0]
    tot = df.Antwort.value_counts()
    keep = tot[tot >= MIN_ANSWERS_DE].index
    agg = (
        df[df.Antwort.isin(keep)]
        .groupby(["kreis", "Antwort"])
        .size()
        .rename("n")
        .reset_index()
    )
    agg.insert(0, "frage", qid)
    rows.append(agg)
    print(f"{qid:>2} {stem:<24} {len(df):>8} answers in DE, {len(keep)} variants")

answers = pd.concat(rows).rename(columns={"Antwort": "antwort"})
answers.to_csv(OUT / "answers.csv", index=False)
pd.DataFrame(
    [{"frage": q, "titel": t, "text": qtext[q]} for q, (_, t) in QUESTIONS.items()]
).to_csv(OUT / "questions.csv", index=False)
print("rows:", len(answers))
