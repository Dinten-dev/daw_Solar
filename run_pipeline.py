#!/usr/bin/env python3
"""
Haupt-Pipeline-Skript für das Solar Activity Data Wrangling Projekt

Dieses Skript orchestriert die gesamte Datenverarbeitungspipeline:
1. Import & Bereinigung (cleaning.py)
2. Transformation & Merge (cleaning.py)
3. Visualisierung (visualization.py)

Ausführung:
    python run_pipeline.py
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    # Stelle sicher, dass wir im Hauptverzeichnis des Projekts sind
    # Finde das Verzeichnis, in dem dieses Skript liegt
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print("="*70)
    print("SOLAR ACTIVITY DATA WRANGLING - PIPELINE")
    print("="*70)
    print(f"Working Directory: {os.getcwd()}")
    
    scripts = [
        ("Import & Bereinigung", "scripts/cleaning.py"),
        ("Visualisierung", "scripts/visualization.py")
    ]
    
    for step_name, script in scripts:
        print(f"\n{'='*70}")
        print(f"Schritt: {step_name}")
        print(f"Skript: {script}")
        print(f"{'='*70}\n")
        
        if not os.path.exists(script):
            print(f"FEHLER: Skript '{script}' nicht gefunden!")
            sys.exit(1)
        
        try:
            result = subprocess.run(
                [sys.executable, script],
                check=True,
                capture_output=False
            )
            print(f"\n✓ {step_name} erfolgreich abgeschlossen")
        except subprocess.CalledProcessError as e:
            print(f"\n✗ FEHLER in {step_name}: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"\n✗ FEHLER: Python nicht gefunden. Bitte installieren Sie Python.")
            sys.exit(1)
    
    print("\n" + "="*70)
    print("PIPELINE ERFOLGREICH ABGESCHLOSSEN")
    print("="*70)
    print("\nErzeugte Dateien:")
    print("  - Tägliche Daten (data/processed/):")
    print("    * sunspots_daily_clean.csv")
    print("    * f107_daily_clean.csv")
    print("    * kp_daily_clean.csv")
    print("  - Monatliche Daten (data/processed/):")
    print("    * sunspots_monthly_clean.csv")
    print("    * f107_monthly_clean.csv")
    print("    * kp_monthly_clean.csv")
    print("  - Master-Dataset (data/processed/):")
    print("    * master_monthly_merged.csv")
    print("  - Korrelationsanalysen (data/results/):")
    print("    * correlation_matrix_main.csv")
    print("    * correlation_lags_kp.csv")
    print("    * correlation_lags_ap.csv")
    print("  - Visualisierungen (plots/):")
    print("    * timeseries_all_variables.png")
    print("    * correlation_scatterplots.png")
    print("    * correlation_heatmap.png")
    print("    * lag_correlations_kp.png")

if __name__ == "__main__":
    main()

