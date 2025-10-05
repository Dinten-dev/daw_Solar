#Source:https://www.sidc.be/SILSO/datafiles

import pandas as pd

# 1) Laden (Separator ist ;)
cols = ["year","month","day","year_frac","sn","sn_std","n_obs","definitive"]
df = pd.read_csv("SN_d_tot_V2.0.csv", sep=";", header=None, names=cols,
                 na_values={"sn": [-1]})  # -1 als fehlend behandeln

# 2) Datumsfeld bauen
df["date"] = pd.to_datetime(df[["year","month","day"]], errors="coerce")

# 3) Filtern: nur gültige, definitive Beobachtungen
mask = (
    df["sn"].notna() &        # keine -1 / NaN
    df["n_obs"].fillna(0) > 0 &
    (df["definitive"] == 1) & # nur definitive Werte
    df["date"].notna()
)
df_clean = df.loc[mask, ["date","sn","sn_std","n_obs"]].sort_values("date").reset_index(drop=True)

# 4) Optional: Typen hübsch machen
df_clean = df_clean.astype({"n_obs": "Int64"})

# 5) Speichern
df_clean.to_csv("sunspots_daily_clean.csv", index=False)

print(df_clean.head())
print(len(df_clean), "Zeilen behalten")

