# Quellen:
# Sunspots: https://www.sidc.be/SILSO/datafiles
# F10.7:    https://spaceweather.gc.ca/solar_flux_data/daily_flux_values/fluxtable.txt

import pandas as pd

# -------------------------
# 1) SUNSPOTS laden + filtern
# -------------------------
cols_sn = ["year","month","day","year_frac","sn","sn_std","n_obs","definitive"]
sn = pd.read_csv(
    "SN_d_tot_V2.0.csv",
    sep=";", header=None, names=cols_sn,
    na_values={"sn": [-1]}
)
sn["date"] = pd.to_datetime(sn[["year","month","day"]], errors="coerce")

mask = (
    sn["sn"].notna() &
    sn["n_obs"].fillna(0) > 0 &
    (sn["definitive"] == 1) &
    sn["date"].notna()
)
sn_clean = (
    sn.loc[mask, ["date","sn","sn_std","n_obs"]]
      .sort_values("date")
      .reset_index(drop=True)
)
sn_clean = sn_clean.astype({"n_obs": "Int64"})
sn_clean["date_str"] = sn_clean["date"].dt.date.astype(str)  # YYYY-MM-DD

# -------------------------
# 2) F10.7 laden + Datum bauen
#    Erwartetes Format mit Spalten:
#    fluxdate, fluxtime, fluxjulian, fluxcarrington, fluxobsflux, fluxadjflux, fluxursi
# -------------------------
cols_f = ["fluxdate","fluxtime","fluxjulian","fluxcarrington","fluxobsflux","fluxadjflux","fluxursi"]

# Datei kann Leerzeichen- oder Semikolon-getrennt sein, mit evtl. Headerlinien.
f107 = pd.read_csv(
    "fluxtable.txt",               
    sep=r"\s+|;", engine="python",
    comment="#",
    names=cols_f,
    header=None
)

# Nur Zeilen behalten, wo fluxdate/fluxtime plausibel sind
f107 = f107.dropna(subset=["fluxdate","fluxtime"])
f107["fluxdate"] = f107["fluxdate"].astype(str).str.replace(r"\D","", regex=True)
f107["fluxtime"] = f107["fluxtime"].astype(str).str.pad(6, fillchar="0")

# Datum/Zeit parsen und Tagesdatum erzeugen
f107["datetime"] = pd.to_datetime(
    f107["fluxdate"] + f107["fluxtime"],
    format="%Y%m%d%H%M%S",
    errors="coerce"
)
f107 = f107.dropna(subset=["datetime"])
f107["date"] = f107["datetime"].dt.normalize()
f107["date_str"] = f107["date"].dt.date.astype(str)  # YYYY-MM-DD

# Zahlenfelder sauber casten
for c in ["fluxobsflux","fluxadjflux","fluxursi"]:
    f107[c] = pd.to_numeric(f107[c], errors="coerce")

# Auf Tagesebene mitteln (mehrere Messzeiten pro Tag)
f107_daily = (
    f107.groupby(["date","date_str"], as_index=False)[["fluxobsflux","fluxadjflux","fluxursi"]]
        .mean(numeric_only=True)
        .sort_values("date")
)

# -------------------------
# 3) Merge: Sunspots × F10.7 auf Datum
# -------------------------
merged = sn_clean.merge(
    f107_daily,
    on=["date","date_str"],
    how="inner"  # nur Tage, die beide haben; ggf. "left" wenn alle Sunspot-Tage behalten werden sollen
)

# -------------------------
# 4) Speichern
# -------------------------
sn_clean[["date_str","sn","sn_std","n_obs"]].rename(columns={"date_str":"date"}) \
    .to_csv("sunspots_daily_clean.csv", index=False)

f107_daily[["date_str","fluxobsflux","fluxadjflux","fluxursi"]].rename(columns={"date_str":"date"}) \
    .to_csv("f107_daily_clean.csv", index=False)

merged[["date_str","sn","sn_std","n_obs","fluxadjflux","fluxursi"]].rename(columns={"date_str":"date"}) \
    .to_csv("sunspots_f107_merged.csv", index=False)

# Kurzer Check
print(sn_clean.head())
print(f107_daily.head())
print(merged.head())
print("Rows -> sunspots:", len(sn_clean), "| f107_daily:", len(f107_daily), "| merged:", len(merged))