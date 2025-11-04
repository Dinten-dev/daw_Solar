# Anleitung zur Ausführung

## Schnellstart

### 1. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 2. Pipeline ausführen

Die einfachste Methode ist, die gesamte Pipeline mit einem Befehl auszuführen:

```bash
python run_pipeline.py
```

Dies führt automatisch alle Schritte aus:
- ✅ Import & Bereinigung der Daten
- ✅ Transformation & Merge
- ✅ Korrelationsanalyse
- ✅ Visualisierung

## Schritt-für-Schritt Anleitung

### Schritt 1: Vorbereitung

Stellen Sie sicher, dass Sie im Hauptverzeichnis sind:

```bash
cd /Users/noaj2/PycharmProjects/daw_Solar
```

### Schritt 2: Dependencies installieren

```bash
pip install -r requirements.txt
```

Oder mit pip3:

```bash
pip3 install -r requirements.txt
```

### Schritt 3: Pipeline ausführen

**Option A: Vollständige Pipeline (empfohlen)**

```bash
python run_pipeline.py
```

**Option B: Einzelne Schritte**

1. Datenimport und Bereinigung:
```bash
python scripts/cleaning.py
```

2. Visualisierung:
```bash
python scripts/visualization.py
```

### Schritt 4: Ergebnisse prüfen

Nach der Ausführung finden Sie:

- **Verarbeitete Daten** in `data/processed/`:
  - `master_monthly_merged.csv` - Master-Dataset mit allen Variablen
  - Tägliche und monatliche Datensätze

- **Analyseergebnisse** in `data/results/`:
  - `correlation_matrix_main.csv` - Korrelationsmatrix
  - `correlation_lags_kp.csv` - Lag-Korrelationen für Kp
  - `correlation_lags_ap.csv` - Lag-Korrelationen für Ap

- **Visualisierungen** in `plots/`:
  - `timeseries_all_variables.png` - Zeitreihenplots
  - `correlation_scatterplots.png` - Scatterplots
  - `correlation_heatmap.png` - Korrelationsmatrix
  - `lag_correlations_kp.png` - Lag-Analyse

### Schritt 5: Jupyter Notebook (optional)

Für interaktive Analyse:

```bash
jupyter notebook notebooks/eda_analysis.ipynb
```

Oder mit JupyterLab:

```bash
jupyter lab notebooks/eda_analysis.ipynb
```

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'pandas'"

**Lösung:** Installieren Sie die Dependencies:
```bash
pip install -r requirements.txt
```

### Problem: "FileNotFoundError: data/raw/SN_d_tot_V2.0.csv"

**Lösung:** Stellen Sie sicher, dass:
1. Sie im Hauptverzeichnis sind (`/Users/noaj2/PycharmProjects/daw_Solar`)
2. Die Rohdaten in `data/raw/` vorhanden sind

### Problem: "Permission denied" beim Ausführen

**Lösung:** Machen Sie die Skripte ausführbar:
```bash
chmod +x run_pipeline.py
```

Oder verwenden Sie Python explizit:
```bash
python3 run_pipeline.py
```

## Projektstruktur nach Ausführung

Nach erfolgreicher Ausführung sollte die Struktur so aussehen:

```
daw_Solar/
├── data/
│   ├── raw/                    # Rohdaten (unverändert)
│   ├── processed/              # Verarbeitete Daten (NEU)
│   │   ├── *_daily_clean.csv
│   │   ├── *_monthly_clean.csv
│   │   └── master_monthly_merged.csv
│   └── results/                # Analyseergebnisse (NEU)
│       └── correlation_*.csv
├── plots/                      # Visualisierungen (NEU)
│   └── *.png
└── ...
```

## Nächste Schritte

1. **Visualisierungen ansehen**: Öffnen Sie die PNG-Dateien in `plots/`
2. **Korrelationsanalysen prüfen**: Öffnen Sie die CSV-Dateien in `data/results/`
3. **Master-Dataset analysieren**: Verwenden Sie `data/processed/master_monthly_merged.csv` für weitere Analysen
4. **Jupyter Notebook**: Führen Sie das EDA-Notebook aus für interaktive Analyse

## Git-Status prüfen

Nach der ersten Ausführung können Sie den Status prüfen:

```bash
git status
```

Die neuen Dateien in `data/processed/`, `data/results/` und `plots/` sollten als "untracked" erscheinen.

