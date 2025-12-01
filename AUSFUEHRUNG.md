# Anleitung zur Ausführung

## Schnellstart

### 1. Virtuelle Umgebung erstellen (empfohlen)

```bash
python3 -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

### 2. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 3. Pipeline ausführen

Die einfachste Methode ist, die gesamte Pipeline mit einem Befehl auszuführen:

```bash
python run_pipeline.py
```

**In PyCharm:** Einfach auf "Play" drücken (nach Setup, siehe unten)

Dies führt automatisch alle Schritte aus:
- ✅ Import & Bereinigung der Daten
- ✅ Transformation & Merge
- ✅ Korrelationsanalyse
- ✅ Visualisierung

## Schritt-für-Schritt Anleitung

### Schritt 1: Vorbereitung

Stellen Sie sicher, dass Sie im Hauptverzeichnis sind:

```bash
cd /Pfad/zum/daw_Solar  # Anpassen an Ihren Pfad
```

### Schritt 2: Virtuelle Umgebung erstellen (empfohlen)

```bash
python3 -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

### Schritt 3: Dependencies installieren

```bash
pip install -r requirements.txt
```

Oder mit pip3 (falls nicht in venv):

```bash
pip3 install -r requirements.txt
```

### Schritt 4: Pipeline ausführen

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

### Schritt 5: Ergebnisse prüfen

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

### Schritt 6: PyCharm-Konfiguration (optional)

Für automatische Interpreter-Auswahl in PyCharm:

```bash
python setup_pycharm.py
```

Danach:
1. PyCharm neu starten (File → Invalidate Caches / Restart)
2. Run → "Run Pipeline" sollte verfügbar sein
3. Einfach auf "Play" drücken

### Schritt 7: Jupyter Notebook (optional)

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
1. Sie im Hauptverzeichnis sind (wo `run_pipeline.py` liegt)
2. Die Rohdaten in `data/raw/` vorhanden sind
3. Das Skript automatisch ins richtige Verzeichnis wechselt (siehe `run_pipeline.py`)

### Problem: "Permission denied" beim Ausführen

**Lösung:** Verwenden Sie Python explizit:
```bash
python3 run_pipeline.py
```

Oder mit virtueller Umgebung:
```bash
source venv/bin/activate
python run_pipeline.py
```

### Problem: PyCharm verwendet falschen Interpreter

**Lösung:** 
1. Führen Sie `python setup_pycharm.py` aus
2. File → Settings → Project → Python Interpreter
3. Wählen Sie: `venv/bin/python3` oder den vollständigen Pfad
4. Apply → OK

Oder: Run → Edit Configurations → Python interpreter auf `venv/bin/python3` setzen

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

**Hinweis:** Die Dateien in `data/processed/`, `data/results/` und `plots/` werden normalerweise nicht versioniert (siehe `.gitignore`), da sie aus den Skripten reproduzierbar sind.

