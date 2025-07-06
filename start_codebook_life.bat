@echo off
echo ==========================================
echo    Codebook LIFE - Framework Management
echo ==========================================
echo.

REM Prüfe Python Installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH
    echo Bitte installiere Python 3.7+ von https://python.org
    pause
    exit /b 1
)

REM Prüfe ob wir im richtigen Verzeichnis sind
if not exist "codebook_life_gui.py" (
    echo FEHLER: codebook_life_gui.py nicht gefunden
    echo Bitte fuehre dieses Skript im Code_book_Life Verzeichnis aus
    pause
    exit /b 1
)

REM Installiere Dependencies falls nötig
echo Prüfe Python-Abhängigkeiten...
python -c "import yaml, tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installiere fehlende Abhängigkeiten...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo FEHLER: Konnte Abhängigkeiten nicht installieren
        pause
        exit /b 1
    )
)

echo Starte Codebook LIFE GUI...
echo.
python start_codebook_life.py

REM Warte auf Benutzer-Eingabe bei Fehlern
if %errorlevel% neq 0 (
    echo.
    echo Fehler beim Starten der Anwendung
    pause
) 