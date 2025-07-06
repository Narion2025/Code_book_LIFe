#!/bin/bash
echo "=========================================="
echo "   Codebook LIFE - Framework Management"
echo "=========================================="
echo

# Wechsle ins Skript-Verzeichnis
cd "$(dirname "$0")"

# Prüfe Python Installation
if ! command -v python3 &> /dev/null; then
    echo "FEHLER: Python 3 ist nicht installiert"
    echo "Bitte installiere Python 3.7+ von https://python.org"
    read -p "Drücke Enter zum Beenden..."
    exit 1
fi

# Prüfe ob wir im richtigen Verzeichnis sind
if [ ! -f "codebook_life_gui.py" ]; then
    echo "FEHLER: codebook_life_gui.py nicht gefunden"
    echo "Bitte führe dieses Skript im Code_book_Life Verzeichnis aus"
    read -p "Drücke Enter zum Beenden..."
    exit 1
fi

# Installiere Dependencies falls nötig
echo "Prüfe Python-Abhängigkeiten..."
python3 -c "import yaml, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installiere fehlende Abhängigkeiten..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "FEHLER: Konnte Abhängigkeiten nicht installieren"
        read -p "Drücke Enter zum Beenden..."
        exit 1
    fi
fi

echo "Starte Codebook LIFE GUI..."
echo
python3 start_codebook_life.py

# Warte auf Benutzer-Eingabe bei Fehlern
if [ $? -ne 0 ]; then
    echo
    echo "Fehler beim Starten der Anwendung"
    read -p "Drücke Enter zum Beenden..."
fi 