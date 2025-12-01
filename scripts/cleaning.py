"""
Datenimport, Bereinigung und Transformation für Solar Activity Data Wrangling

Dieses Skript führt folgende Schritte aus:
1. Import & Bereinigung (LE1, LE2):
   - Sunspots: Einlesen, Filtern nach definitiven Werten, Missing Values
   - F10.7: Einlesen, Parsing, Aggregation auf Tagesebene
   - Kp/ap: Einlesen, Parsing, Filtern nach definitiven Werten, Aggregation auf Tagesebene

2. Transformation (LE3):
   - Resampling auf monatliche Frequenz für alle Datensätze
   - Erstellung von Lag-Features (1, 3, 6 Monate)

3. Verknüpfung (LE4):
   - Merge der drei Datensätze auf Tages- und Monatsebene
   - Erstellung des Master-Datasets

4. Analyse (LE5):
   - Korrelationsanalyse (Pearson)
   - Korrelationen mit Lag-Features

Quellen:
- Sunspots: https://www.sidc.be/SILSO/datafiles
- F10.7:    https://spaceweather.gc.ca/solar_flux_data/daily_flux_values/fluxtable.txt
- Kp/ap:    GFZ Helmholtz Centre for Geosciences (Kp_ap_since_1932.txt)
"""

import pandas as pd
import numpy as np

# -------------------------
# 1) SUNSPOTS laden + filtern
# -------------------------
cols_sn = ["year","month","day","year_frac","sn","sn_std","n_obs","definitive"]
sn = pd.read_csv(
    "data/raw/SN_d_tot_V2.0.csv",
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
    "data/raw/fluxtable.txt",               
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
# 3) Kp/ap laden + auf Tagesebene aggregieren
# -------------------------
# Format: Fixed-width, 30 Header-Zeilen mit #, dann: YYYY MM DD hh.h hh._m days days_m Kp ap D
cols_kp = ["year","month","day","hour_start","hour_mid","days","days_mid","kp","ap","definitive"]

kp_raw = pd.read_csv(
    "data/raw/Kp_ap_since_1932.txt",
    sep=r"\s+",  # whitespace-separated
    comment="#",
    header=None,
    names=cols_kp,
    skiprows=30  # 30 Header-Zeilen überspringen
)

# Datum aus Jahr/Monat/Tag erstellen
kp_raw["date"] = pd.to_datetime(kp_raw[["year","month","day"]], errors="coerce")

# Missing values: -1.000 für Kp, -1 für ap
kp_raw["kp"] = pd.to_numeric(kp_raw["kp"], errors="coerce")
kp_raw["ap"] = pd.to_numeric(kp_raw["ap"], errors="coerce")
kp_raw.loc[kp_raw["kp"] == -1.000, "kp"] = pd.NA
kp_raw.loc[kp_raw["ap"] == -1, "ap"] = pd.NA

# Nur definitive Werte (D=1) und gültige Daten behalten
mask_kp = (
    (kp_raw["definitive"] == 1) &
    (kp_raw["date"].notna()) &
    (kp_raw["kp"].notna()) &
    (kp_raw["ap"].notna())
)

kp_clean = (
    kp_raw.loc[mask_kp, ["date","kp","ap"]]
        .sort_values("date")
        .reset_index(drop=True)
)

# Auf Tagesebene aggregieren (Mittelwert der 3-stündlichen Werte)
kp_clean["date_str"] = kp_clean["date"].dt.date.astype(str)  # YYYY-MM-DD

kp_daily = (
    kp_clean.groupby(["date","date_str"], as_index=False)[["kp","ap"]]
        .mean(numeric_only=True)
        .sort_values("date")
        .reset_index(drop=True)
)

# -------------------------
# 4) Merge: Sunspots × F10.7 auf Datum
# -------------------------
merged = sn_clean.merge(
    f107_daily,
    on=["date","date_str"],
    how="inner"  # nur Tage, die beide haben; ggf. "left" wenn alle Sunspot-Tage behalten werden sollen
)

# -------------------------
# 5) Auf monatliche Frequenz resamplen
# -------------------------
# Setze date als Index für Resampling
sn_monthly = (
    sn_clean.set_index("date")
        [["sn","sn_std","n_obs"]]
        .resample("MS")  # MS = Month Start
        .agg({
            "sn": "mean",
            "sn_std": "mean",
            "n_obs": "sum"  # Summe der Beobachtungen pro Monat
        })
        .reset_index()
)
sn_monthly["date_str"] = sn_monthly["date"].dt.date.astype(str)

f107_monthly = (
    f107_daily.set_index("date")
        [["fluxobsflux","fluxadjflux","fluxursi"]]
        .resample("MS")
        .mean()
        .reset_index()
)
f107_monthly["date_str"] = f107_monthly["date"].dt.date.astype(str)

kp_monthly = (
    kp_daily.set_index("date")
        [["kp","ap"]]
        .resample("MS")
        .mean()
        .reset_index()
)
kp_monthly["date_str"] = kp_monthly["date"].dt.date.astype(str)

# -------------------------
# 6) Speichern (tägliche Daten)
# -------------------------
sn_clean[["date_str","sn","sn_std","n_obs"]].rename(columns={"date_str":"date"}) \
    .to_csv("data/processed/sunspots_daily_clean.csv", index=False)

f107_daily[["date_str","fluxobsflux","fluxadjflux","fluxursi"]].rename(columns={"date_str":"date"}) \
    .to_csv("data/processed/f107_daily_clean.csv", index=False)

kp_daily[["date_str","kp","ap"]].rename(columns={"date_str":"date"}) \
    .to_csv("data/processed/kp_daily_clean.csv", index=False)

merged[["date_str","sn","sn_std","n_obs","fluxadjflux","fluxursi"]].rename(columns={"date_str":"date"}) \
    .to_csv("data/processed/sunspots_f107_merged.csv", index=False)

# -------------------------
# 7) Speichern (monatliche Daten)
# -------------------------
sn_monthly[["date_str","sn","sn_std","n_obs"]].rename(columns={"date_str":"date"}) \
    .to_csv("data/processed/sunspots_monthly_clean.csv", index=False)

f107_monthly[["date_str","fluxobsflux","fluxadjflux","fluxursi"]].rename(columns={"date_str":"date"}) \
    .to_csv("data/processed/f107_monthly_clean.csv", index=False)

kp_monthly[["date_str","kp","ap"]].rename(columns={"date_str":"date"}) \
    .to_csv("data/processed/kp_monthly_clean.csv", index=False)

# -------------------------
# 8) Master-Dataset (monatlich): Alle drei Datensätze zusammenführen
# -------------------------
# Schrittweise mergen: Sunspots × F10.7, dann × Kp/ap
merged_monthly = sn_monthly.merge(
    f107_monthly,
    on=["date","date_str"],
    how="inner"
)

merged_monthly = merged_monthly.merge(
    kp_monthly,
    on=["date","date_str"],
    how="inner"
)

# -------------------------
# 9) Lag-Features hinzufügen
# -------------------------
# Lag-Variablen für Sunspots und F10.7 (1, 3, 6 Monate)
# Diese können verwendet werden, um zu untersuchen, ob Sonnenaktivität
# mit Verzögerung auf Kp-Index wirkt
lag_months = [1, 3, 6]

# Sortiere nach Datum für korrekte Lag-Berechnung
merged_monthly = merged_monthly.sort_values("date").reset_index(drop=True)

# Lag-Features für Sunspots
for lag in lag_months:
    merged_monthly[f"sn_lag_{lag}m"] = merged_monthly["sn"].shift(lag)

# Lag-Features für F10.7 (fluxadjflux)
for lag in lag_months:
    merged_monthly[f"f107_lag_{lag}m"] = merged_monthly["fluxadjflux"].shift(lag)

# Speichern des Master-Datasets (mit Lag-Features)
# Wähle relevante Spalten für die Ausgabe
output_cols = [
    "date_str", "sn", "sn_std", "n_obs",
    "fluxadjflux", "fluxursi",
    "kp", "ap",
    "sn_lag_1m", "sn_lag_3m", "sn_lag_6m",
    "f107_lag_1m", "f107_lag_3m", "f107_lag_6m"
]

merged_monthly[output_cols] \
    .rename(columns={"date_str":"date"}) \
    .to_csv("data/processed/master_monthly_merged.csv", index=False)

# -------------------------
# 10) Korrelationsanalyse
# -------------------------
# Pearson-Korrelationen zwischen den Variablen
print("\n" + "="*60)
print("KORRELATIONSANALYSE")
print("="*60)

# Hauptvariablen für Korrelationen
corr_vars = ["sn", "fluxadjflux", "kp", "ap"]
corr_data = merged_monthly[corr_vars].dropna()

if len(corr_data) > 0:
    corr_matrix = corr_data.corr()
    print("\n=== Pearson-Korrelationen (Hauptvariablen) ===")
    print(corr_matrix.round(3))
    
    # Speichern der Korrelationsmatrix
    corr_matrix.to_csv("data/results/correlation_matrix_main.csv")
    
    # Spezifische Korrelationen ausgeben
    print("\n=== Wichtige Korrelationen ===")
    print(f"Sunspots ↔ Kp:        {corr_matrix.loc['sn', 'kp']:.3f}")
    print(f"Sunspots ↔ F10.7:      {corr_matrix.loc['sn', 'fluxadjflux']:.3f}")
    print(f"F10.7 ↔ Kp:           {corr_matrix.loc['fluxadjflux', 'kp']:.3f}")
    print(f"F10.7 ↔ Ap:           {corr_matrix.loc['fluxadjflux', 'ap']:.3f}")
    
    # Korrelationen mit Lag-Features
    print("\n=== Korrelationen mit Lag-Features (Kp) ===")
    lag_vars = ["kp"] + [f"sn_lag_{lag}m" for lag in lag_months] + [f"f107_lag_{lag}m" for lag in lag_months]
    lag_corr_data = merged_monthly[lag_vars].dropna()
    
    if len(lag_corr_data) > 0:
        lag_corr = lag_corr_data.corr()["kp"].drop("kp").sort_values(ascending=False)
        print(lag_corr.round(3))
        lag_corr.to_csv("data/results/correlation_lags_kp.csv", header=["correlation"])
        
        print("\n=== Korrelationen mit Lag-Features (Ap) ===")
        lag_vars_ap = ["ap"] + [f"sn_lag_{lag}m" for lag in lag_months] + [f"f107_lag_{lag}m" for lag in lag_months]
        lag_corr_data_ap = merged_monthly[lag_vars_ap].dropna()
        
        if len(lag_corr_data_ap) > 0:
            lag_corr_ap = lag_corr_data_ap.corr()["ap"].drop("ap").sort_values(ascending=False)
            print(lag_corr_ap.round(3))
            lag_corr_ap.to_csv("data/results/correlation_lags_ap.csv", header=["correlation"])
else:
    print("Warnung: Keine Daten für Korrelationsanalyse verfügbar")

# Kurzer Check
print("\n=== TÄGLICHE DATEN ===")
print("\n=== Sunspots (daily) ===")
print(sn_clean.head())
print(f"\n=== F10.7 (daily) ===")
print(f107_daily.head())
print(f"\n=== Kp/ap (daily) ===")
print(kp_daily.head())
print(f"\n=== Merged (Sunspots × F10.7, daily) ===")
print(merged.head())

print("\n=== MONATLICHE DATEN ===")
print("\n=== Sunspots (monthly) ===")
print(sn_monthly.head())
print(f"\n=== F10.7 (monthly) ===")
print(f107_monthly.head())
print(f"\n=== Kp/ap (monthly) ===")
print(kp_monthly.head())

print(f"\n=== Master-Dataset (monthly) ===")
print(merged_monthly.head())

print(f"\n=== Row counts ===")
print(f"Sunspots daily: {len(sn_clean)} | monthly: {len(sn_monthly)}")
print(f"F10.7 daily: {len(f107_daily)} | monthly: {len(f107_monthly)}")
print(f"Kp/ap daily: {len(kp_daily)} | monthly: {len(kp_monthly)}")
print(f"Merged (Sunspots × F10.7, daily): {len(merged)}")
print(f"Master (Sunspots × F10.7 × Kp/ap, monthly): {len(merged_monthly)}")