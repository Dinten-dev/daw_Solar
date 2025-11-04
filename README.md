# Solar Activity Data Wrangling

## Projektthema

Untersuchung des Zusammenhangs zwischen Sonnenaktivität (Sonnenflecken), Funkstrahlungsfluss (F10.7) und geomagnetischem Kp-Index. Ziel ist es, anhand von Zeitreihenanalysen und Korrelationen zu zeigen, ob sich aus der Sonnenaktivität Rückschlüsse auf den Kp-Index ziehen lassen, der für geomagnetische Störungen auf der Erde relevant ist.

## Fragestellung

Wie stark hängen Sonnenflecken, der Funkstrahlungsfluss (F10.7) und der geomagnetische Kp-Index miteinander zusammen? Lassen sich aus der Sonnenaktivität Rückschlüsse auf den Kp-Index ziehen?

## Datenquellen

- **Sonnenfleckenzahlen**: [SILSO (Sunspot Index and Long-term Solar Observations)](https://www.sidc.be/SILSO/datafiles), Royal Observatory of Belgium
- **F10.7 Radio Flux**: [Space Weather Canada](https://spaceweather.gc.ca/solar_flux_data/daily_flux_values/fluxtable.txt), NOAA
- **Kp-Index**: [GFZ Helmholtz Centre for Geosciences](https://www.gfz-potsdam.de/en/kp-index/), Geomagnetic Observatory Niemegk

Alle drei Datenquellen sind öffentlich zugänglich und liefern Zeitreihen über mehrere Jahrzehnte.

## Installation

### Voraussetzungen

- Python 3.7 oder höher
- pip (Python Package Manager)

### Dependencies installieren

```bash
pip install -r requirements.txt
```

## Verwendung

### Vollständige Pipeline ausführen

Die einfachste Methode ist, die gesamte Pipeline mit einem Befehl auszuführen:

```bash
python run_pipeline.py
```

Dieses Skript führt automatisch alle Schritte aus:
1. Import & Bereinigung der Daten
2. Transformation & Merge
3. Korrelationsanalyse
4. Visualisierung

### Einzelne Skripte ausführen

#### Datenimport, Bereinigung und Transformation

```bash
python scripts/cleaning.py
```

**Wichtig:** Dieses Skript muss vom Hauptverzeichnis ausgeführt werden, damit die relativen Pfade funktionieren.

Dieses Skript:
- Importiert die Rohdaten (Sunspots, F10.7, Kp/ap)
- Bereinigt die Daten (fehlende Werte, Duplikate, Ausreißer)
- Transformiert auf monatliche Frequenz
- Erstellt Lag-Features (1, 3, 6 Monate)
- Führt die Datensätze zusammen
- Berechnet Korrelationen

**Erzeugte Dateien:**
- `data/processed/sunspots_daily_clean.csv` / `sunspots_monthly_clean.csv`
- `data/processed/f107_daily_clean.csv` / `f107_monthly_clean.csv`
- `data/processed/kp_daily_clean.csv` / `kp_monthly_clean.csv`
- `data/processed/master_monthly_merged.csv`
- `data/results/correlation_matrix_main.csv`
- `data/results/correlation_lags_kp.csv` / `correlation_lags_ap.csv`

#### Visualisierung

```bash
python scripts/visualization.py
```

Dieses Skript erstellt:
- `plots/timeseries_all_variables.png` - Zeitreihenplots aller Variablen
- `plots/correlation_scatterplots.png` - Scatterplots für Korrelationen
- `plots/correlation_heatmap.png` - Korrelationsmatrix als Heatmap
- `plots/lag_correlations_kp.png` - Lag-Korrelationen für Vorhersagekraft

#### Jupyter Notebook (EDA)

```bash
jupyter notebook notebooks/eda_analysis.ipynb
```

Oder mit JupyterLab:
```bash
jupyter lab notebooks/eda_analysis.ipynb
```

## Projektstruktur

```
daw_Solar/
├── README.md                    # Diese Datei
├── requirements.txt             # Python Dependencies
├── run_pipeline.py              # Haupt-Pipeline-Skript
├── .gitignore                   # Git ignore rules
│
├── data/                        # Datenverzeichnis
│   ├── raw/                     # Rohdaten (nicht verändern!)
│   │   ├── SN_d_tot_V2.0.csv   # Sunspots
│   │   ├── fluxtable.txt        # F10.7
│   │   └── Kp_ap_since_1932.txt # Kp/ap
│   │
│   ├── processed/               # Verarbeitete Daten
│   │   ├── sunspots_daily_clean.csv
│   │   ├── sunspots_monthly_clean.csv
│   │   ├── f107_daily_clean.csv
│   │   ├── f107_monthly_clean.csv
│   │   ├── kp_daily_clean.csv
│   │   ├── kp_monthly_clean.csv
│   │   └── master_monthly_merged.csv
│   │
│   └── results/                 # Analyseergebnisse
│       ├── correlation_matrix_main.csv
│       ├── correlation_lags_kp.csv
│       └── correlation_lags_ap.csv
│
├── scripts/                     # Python-Skripte
│   ├── cleaning.py              # Import, Bereinigung, Transformation
│   └── visualization.py         # Visualisierungen
│
├── notebooks/                   # Jupyter Notebooks
│   └── eda_analysis.ipynb       # Explorative Datenanalyse
│
└── plots/                       # Visualisierungen (PNG)
    ├── timeseries_all_variables.png
    ├── correlation_scatterplots.png
    ├── correlation_heatmap.png
    └── lag_correlations_kp.png
```

## Geplanter Ablauf (LE1-LE6)

### LE1: Importieren
- Daten in Python einlesen (CSV/TXT)
- Prüfen auf Encodings, Formate und Zeitindizes

### LE2: Bereinigen
- Umgang mit fehlenden Werten
- Duplikate entfernen
- Ausreißer behandeln (z.B. Ausreißer bei geomagnetischen Stürmen)
- Filtern nach definitiven Werten

### LE3: Transformieren
- Zeitreihen auf einheitliche Frequenz bringen (monatlich)
- Variablen reskalieren
- Lag-Variablen bilden (1, 3, 6 Monate)

### LE4: Verknüpfen
- Zusammenführen der drei Datensätze über Zeitstempel
- Erstellung des Master-Datasets

### LE5: Datenpipelines
- Skripte so strukturieren, dass Import, Bereinigung und Transformation reproduzierbar laufen
- Haupt-Pipeline-Skript (`run_pipeline.py`)

### LE6: Reproduzierbarkeit
- Nutzung von Git (inkl. sauberer Commits)
- README mit Anleitung
- requirements.txt für Dependencies

## Erwartete Ergebnisse

1. **Visualisierung**: Zeitreihenplots, die typische 11-Jahres-Zyklen der Sonnenaktivität zeigen und deren Einfluss auf F10.7 und Kp-Index verdeutlichen.

2. **Korrelationsanalyse**: Statistische Auswertung der Zusammenhänge (Pearson-Korrelation), mit Zeitverzögerungen (Lag-Analyse).

3. **Interpretation**: Diskussion, wie gut sich aus Sonnenflecken- und F10.7-Daten geomagnetische Aktivität (Kp) vorhersagen lässt.

## Zitierung der Datenquellen

Wenn Sie dieses Projekt oder die Daten verwenden, bitte zitieren Sie:

- **Sunspots**: SILSO World Data Center — The International Sunspot Number, Royal Observatory of Belgium, on-line Sunspot Number catalogue: http://www.sidc.be/silso/datafiles

- **F10.7**: Space Weather Canada, Natural Resources Canada, https://spaceweather.gc.ca

- **Kp-Index**: Matzka, J., Stolle, C., Yamazaki, Y., Bronkalla, O. and Morschhauser, A., 2021. The geomagnetic Kp index and derived indices of geomagnetic activity. Space Weather, https://doi.org/10.1029/2020SW002641

## Git Workflow & Reproduzierbarkeit (LE6)

### Repository initialisieren

```bash
git init
git add .
git commit -m "Initial commit: Solar Activity Data Wrangling Projekt"
```

### Saubere Commits

Für jeden logischen Schritt sollte ein separater Commit erstellt werden:

```bash
# 1. Datenimport und Bereinigung
git add scripts/cleaning.py data/raw/
git commit -m "LE1-LE2: Import und Bereinigung der Datenquellen"

# 2. Transformation und Merge
git add data/processed/master_monthly_merged.csv
git commit -m "LE3-LE4: Transformation auf monatliche Frequenz und Merge"

# 3. Analyse und Visualisierung
git add scripts/visualization.py data/results/ plots/
git commit -m "LE5: Korrelationsanalyse und Visualisierungen"

# 4. Pipeline-Struktur
git add run_pipeline.py requirements.txt README.md .gitignore
git commit -m "LE6: Pipeline-Struktur und Dokumentation"

# 5. EDA Notebook
git add notebooks/eda_analysis.ipynb
git commit -m "EDA: Jupyter Notebook für explorative Analyse"
```

### Branching (optional)

Für größere Änderungen können Branches verwendet werden:

```bash
git checkout -b feature/new-analysis
# ... Änderungen machen ...
git add .
git commit -m "Neue Analyse hinzugefügt"
git checkout main
git merge feature/new-analysis
```

### Git Best Practices

1. **Sinnvolle Commit-Messages**: Beschreiben Sie klar, was geändert wurde
2. **Häufige Commits**: Committen Sie nach jedem logischen Schritt
3. **README aktualisieren**: Bei Änderungen am Workflow README aktualisieren
4. **requirements.txt versionieren**: Damit andere die gleichen Dependencies haben

### Reproduzierbarkeit sicherstellen

1. Alle Skripte sollten idempotent sein (mehrfach ausführbar ohne Fehler)
2. Rohdaten sollten versioniert oder klar dokumentiert sein
3. Alle Ergebnisse sollten aus den Skripten reproduzierbar sein
4. Dependencies sollten in `requirements.txt` festgelegt sein

## Lizenz

Die Datenquellen haben ihre eigenen Lizenzen. Bitte beachten Sie die jeweiligen Nutzungsbedingungen.

## Autor

Data Wrangling Projekt - Solar Activity Analysis
