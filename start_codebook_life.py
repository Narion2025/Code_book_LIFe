#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Codebook LIFE - Starter Script
==============================
Startet die Codebook LIFE GUI mit allen notwendigen Initialisierungen
"""

import sys
import os
from pathlib import Path

# Pfad zum aktuellen Verzeichnis hinzufügen
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Hauptfunktion zum Starten der Codebook LIFE GUI"""
    print("🚀 Starte Codebook LIFE GUI...")
    print("=" * 50)
    
    try:
        # Importiere und starte die GUI
        from codebook_life_gui import CodebookLIFEGUI
        
        print("✅ GUI-Module erfolgreich geladen")
        print("🎯 Initialisiere Codebook LIFE System...")
        
        # Erstelle und starte die GUI
        app = CodebookLIFEGUI()
        
        print("✅ Codebook LIFE GUI gestartet!")
        print("💡 Verwende die GUI um das LIFE Framework zu verwalten")
        print("=" * 50)
        
        # GUI starten
        app.run()
        
    except ImportError as e:
        print(f"❌ Fehler beim Importieren der Module: {e}")
        print("💡 Stelle sicher, dass alle Abhängigkeiten installiert sind:")
        print("   pip install -r requirements.txt")
        return 1
        
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 