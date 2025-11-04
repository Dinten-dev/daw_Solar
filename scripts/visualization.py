# Visualisierung der Sonnenaktivitäts-Daten
# Erstellt Zeitreihenplots, die den 11-Jahres-Zyklus und Zusammenhänge zeigen

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Setze Stil für bessere Plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Lade Master-Dataset
master = pd.read_csv("data/processed/master_monthly_merged.csv")
master["date"] = pd.to_datetime(master["date"])

# -------------------------
# Plot 1: Zeitreihen aller Variablen (11-Jahres-Zyklus)
# -------------------------
fig, axes = plt.subplots(4, 1, figsize=(16, 12), sharex=True)

# Sunspots
axes[0].plot(master["date"], master["sn"], color="tab:blue", linewidth=1.5, alpha=0.8)
axes[0].set_ylabel("Sunspot Number", fontsize=12, fontweight="bold")
axes[0].set_title("Zeitreihen der Sonnenaktivität und geomagnetischen Indizes", 
                  fontsize=14, fontweight="bold", pad=20)
axes[0].grid(True, alpha=0.3)

# F10.7
axes[1].plot(master["date"], master["fluxadjflux"], color="tab:orange", linewidth=1.5, alpha=0.8)
axes[1].set_ylabel("F10.7 (adjusted)", fontsize=12, fontweight="bold")
axes[1].grid(True, alpha=0.3)

# Kp-Index
axes[2].plot(master["date"], master["kp"], color="tab:red", linewidth=1.5, alpha=0.8)
axes[2].set_ylabel("Kp Index", fontsize=12, fontweight="bold")
axes[2].grid(True, alpha=0.3)

# Ap-Index
axes[3].plot(master["date"], master["ap"], color="tab:green", linewidth=1.5, alpha=0.8)
axes[3].set_ylabel("Ap Index", fontsize=12, fontweight="bold")
axes[3].set_xlabel("Jahr", fontsize=12, fontweight="bold")
axes[3].grid(True, alpha=0.3)

# Formatierung der x-Achse
for ax in axes:
    ax.tick_params(labelsize=10)
    # Zeige alle 5 Jahre auf x-Achse
    years = pd.date_range(start=master["date"].min(), end=master["date"].max(), freq="5YS")
    ax.set_xticks(years)
    ax.set_xticklabels([y.strftime("%Y") for y in years], rotation=45, ha="right")

plt.tight_layout()
plt.savefig("plots/timeseries_all_variables.png", dpi=300, bbox_inches="tight")
print("Gespeichert: plots/timeseries_all_variables.png")
plt.close()

# -------------------------
# Plot 2: Scatterplots - Korrelationen zwischen Variablen
# -------------------------
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Sunspots vs F10.7
axes[0, 0].scatter(master["sn"], master["fluxadjflux"], alpha=0.5, s=20, color="tab:blue")
axes[0, 0].set_xlabel("Sunspot Number", fontsize=11, fontweight="bold")
axes[0, 0].set_ylabel("F10.7 (adjusted)", fontsize=11, fontweight="bold")
axes[0, 0].set_title("Sunspots ↔ F10.7", fontsize=12, fontweight="bold")
corr_sn_f107 = master[["sn", "fluxadjflux"]].corr().iloc[0, 1]
axes[0, 0].text(0.05, 0.95, f"r = {corr_sn_f107:.3f}", 
                transform=axes[0, 0].transAxes, fontsize=10,
                verticalalignment="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
axes[0, 0].grid(True, alpha=0.3)

# Sunspots vs Kp
axes[0, 1].scatter(master["sn"], master["kp"], alpha=0.5, s=20, color="tab:red")
axes[0, 1].set_xlabel("Sunspot Number", fontsize=11, fontweight="bold")
axes[0, 1].set_ylabel("Kp Index", fontsize=11, fontweight="bold")
axes[0, 1].set_title("Sunspots ↔ Kp", fontsize=12, fontweight="bold")
corr_sn_kp = master[["sn", "kp"]].corr().iloc[0, 1]
axes[0, 1].text(0.05, 0.95, f"r = {corr_sn_kp:.3f}", 
                transform=axes[0, 1].transAxes, fontsize=10,
                verticalalignment="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
axes[0, 1].grid(True, alpha=0.3)

# F10.7 vs Kp
axes[1, 0].scatter(master["fluxadjflux"], master["kp"], alpha=0.5, s=20, color="tab:orange")
axes[1, 0].set_xlabel("F10.7 (adjusted)", fontsize=11, fontweight="bold")
axes[1, 0].set_ylabel("Kp Index", fontsize=11, fontweight="bold")
axes[1, 0].set_title("F10.7 ↔ Kp", fontsize=12, fontweight="bold")
corr_f107_kp = master[["fluxadjflux", "kp"]].corr().iloc[0, 1]
axes[1, 0].text(0.05, 0.95, f"r = {corr_f107_kp:.3f}", 
                transform=axes[1, 0].transAxes, fontsize=10,
                verticalalignment="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
axes[1, 0].grid(True, alpha=0.3)

# F10.7 vs Ap
axes[1, 1].scatter(master["fluxadjflux"], master["ap"], alpha=0.5, s=20, color="tab:green")
axes[1, 1].set_xlabel("F10.7 (adjusted)", fontsize=11, fontweight="bold")
axes[1, 1].set_ylabel("Ap Index", fontsize=11, fontweight="bold")
axes[1, 1].set_title("F10.7 ↔ Ap", fontsize=12, fontweight="bold")
corr_f107_ap = master[["fluxadjflux", "ap"]].corr().iloc[0, 1]
axes[1, 1].text(0.05, 0.95, f"r = {corr_f107_ap:.3f}", 
                transform=axes[1, 1].transAxes, fontsize=10,
                verticalalignment="top", bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle("Korrelationsanalyse: Sonnenaktivität ↔ Geomagnetische Indizes", 
             fontsize=14, fontweight="bold", y=0.995)
plt.tight_layout()
plt.savefig("plots/correlation_scatterplots.png", dpi=300, bbox_inches="tight")
print("Gespeichert: plots/correlation_scatterplots.png")
plt.close()

# -------------------------
# Plot 3: Korrelationsmatrix (Heatmap)
# -------------------------
corr_vars = ["sn", "fluxadjflux", "kp", "ap"]
corr_matrix = master[corr_vars].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".3f", cmap="coolwarm", center=0,
            square=True, linewidths=1, cbar_kws={"label": "Korrelation"})
ax.set_title("Korrelationsmatrix: Sonnenaktivität und geomagnetische Indizes", 
             fontsize=13, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig("plots/correlation_heatmap.png", dpi=300, bbox_inches="tight")
print("Gespeichert: plots/correlation_heatmap.png")
plt.close()

# -------------------------
# Plot 4: Lag-Korrelationen (wie gut können Sonnenflecken/F10.7 Kp vorhersagen?)
# -------------------------
lag_vars_kp = ["sn_lag_1m", "sn_lag_3m", "sn_lag_6m", "f107_lag_1m", "f107_lag_3m", "f107_lag_6m"]
lag_data = master[["kp"] + lag_vars_kp].dropna()

if len(lag_data) > 0:
    lag_corrs = lag_data.corr()["kp"].drop("kp")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["tab:blue" if "sn" in var else "tab:orange" for var in lag_corrs.index]
    bars = ax.barh(lag_corrs.index, lag_corrs.values, color=colors, alpha=0.7)
    ax.axvline(x=0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel("Korrelation mit Kp-Index", fontsize=12, fontweight="bold")
    ax.set_title("Vorhersagekraft: Lag-Features für Kp-Index", fontsize=13, fontweight="bold", pad=15)
    ax.grid(True, alpha=0.3, axis="x")
    
    # Werte auf Bars anzeigen
    for i, (bar, val) in enumerate(zip(bars, lag_corrs.values)):
        ax.text(val + 0.01 if val >= 0 else val - 0.01, i, f"{val:.3f}",
                va="center", ha="left" if val >= 0 else "right", fontsize=10)
    
    plt.tight_layout()
    plt.savefig("plots/lag_correlations_kp.png", dpi=300, bbox_inches="tight")
    print("Gespeichert: plots/lag_correlations_kp.png")
    plt.close()

print("\n=== Alle Visualisierungen erstellt ===")

