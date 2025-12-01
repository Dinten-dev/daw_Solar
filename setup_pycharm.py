#!/usr/bin/env python3
"""
Setup-Skript für PyCharm-Konfiguration
Erstellt automatisch die richtige Interpreter-Konfiguration
"""

import os
import sys
from pathlib import Path

def setup_pycharm():
    """Erstellt PyCharm-Konfigurationsdateien"""
    
    project_dir = Path(__file__).parent.absolute()
    venv_python = project_dir / "venv" / "bin" / "python3"
    
    # Prüfe ob venv existiert
    if not venv_python.exists():
        print("❌ FEHLER: Virtuelle Umgebung nicht gefunden!")
        print(f"   Erwartet: {venv_python}")
        print("\nBitte zuerst ausführen:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r requirements.txt")
        return False
    
    # Erstelle .idea Verzeichnis
    idea_dir = project_dir / ".idea"
    idea_dir.mkdir(exist_ok=True)
    
    run_config_dir = idea_dir / "runConfigurations"
    run_config_dir.mkdir(exist_ok=True)
    
    # Erstelle Run-Konfiguration
    run_config = run_config_dir / "Run_Pipeline.xml"
    
    config_content = f'''<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="Run Pipeline" type="PythonConfigurationType" factoryName="Python" nameIsGenerated="true">
    <module name="daw_Solar" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="PARENT_ENVS" value="true" />
    <envs>
      <env name="PYTHONUNBUFFERED" value="1" />
    </envs>
    <option name="SDK_HOME" value="{venv_python}" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="IS_MODULE_SDK" value="false" />
    <option name="ADD_CONTENT_ROOTS" value="true" />
    <option name="ADD_SOURCE_ROOTS" value="true" />
    <option name="SCRIPT_NAME" value="$PROJECT_DIR$/run_pipeline.py" />
    <option name="PARAMETERS" value="" />
    <option name="SHOW_COMMAND_LINE" value="false" />
    <option name="EMULATE_TERMINAL" value="false" />
    <option name="MODE" value="run" />
    <option name="USE_CYTHON" value="false" />
    <option name="USE_RUNCONFIG" value="true" />
    <option name="USE_LOGGING" value="false" />
    <option name="USE_LOGGING_OPTIONS" value="false" />
    <method v="2" />
  </configuration>
</component>'''
    
    run_config.write_text(config_content, encoding='utf-8')
    
    # Erstelle misc.xml für Interpreter
    misc_xml = idea_dir / "misc.xml"
    misc_content = '''<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectRootManager" version="2" project-jdk-name="Python 3 (venv)" project-jdk-type="Python SDK" />
</project>'''
    
    misc_xml.write_text(misc_content, encoding='utf-8')
    
    print("✅ PyCharm-Konfiguration erstellt!")
    print(f"\n📁 Konfigurationsdateien:")
    print(f"   - {run_config}")
    print(f"   - {misc_xml}")
    print(f"\n🐍 Python Interpreter: {venv_python}")
    print(f"\n📝 Nächste Schritte:")
    print("   1. PyCharm neu starten (File → Invalidate Caches / Restart)")
    print("   2. File → Settings → Project → Python Interpreter")
    print("   3. Wählen Sie: 'Python 3 (venv)' oder den Pfad:", venv_python)
    print("   4. Run → 'Run Pipeline' sollte jetzt verfügbar sein")
    
    return True

if __name__ == "__main__":
    setup_pycharm()

