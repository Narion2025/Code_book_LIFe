# 📚 Codebook LIFE - Framework Management System

Ein strukturiertes System zur Verwaltung und Dokumentation des LIFE Frameworks mit benutzerfreundlicher GUI.

## 🎯 Überblick

Das Codebook LIFE System ermöglicht es, das LIFE Framework strukturiert zu dokumentieren, zu verwalten und zu erweitern. Es bietet eine hierarchische Struktur für:

- **Prinzipien** - Kernprinzipien des LIFE Frameworks
- **Regeln** - Explizite Do's & Don'ts
- **Heuristiken** - Praxistipps und Daumenregeln
- **Rollen** - Beteiligte und ihre Aufgaben
- **Prozesse** - Standardabläufe und Workflows
- **Beispiele** - Konkrete Anwendungsfälle
- **Transferbeispiele** - Übertragung auf neue Kontexte
- **Semantic Gaps** - Verständnisprobleme und Lösungen
- **Lessons Learned** - Erfahrungen und Best Practices

## 🚀 Schnellstart

### Installation

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# GUI starten
python start_codebook_life.py
```

### Erste Schritte

1. **GUI starten**: `python start_codebook_life.py`
2. **Kategorie wählen**: Links eine Framework-Kategorie auswählen
3. **Item erstellen**: "Neues Item" klicken und Template ausfüllen
4. **Framework exportieren**: Rechts "📤 YAML Export" für Backup

## 🏗️ Framework-Struktur

### Hierarchie

```yaml
framework:
  meta:                    # Metadaten
    name: "LIFE"
    version: "1.0"
    autor: "Anonymous Developer"
    
  prinzipien:              # Kernprinzipien
    - id: "USM"
      name: "User Story Mapping"
      beschreibung: "..."
      hauptziele: [...]
      schritte: [...]
      regeln: [...]
      heuristiken: [...]
      narrative_beispiele: [...]
      transferbeispiele: [...]
      semantic_gaps: [...]
      lessons_learned: [...]
      
  regeln:                  # Explizite Regeln
    - id: "regel_1"
      text: "..."
      kontext: "..."
      beispiel: "..."
      
  # ... weitere Kategorien
```

### Datentypen

| Kategorie | Beschreibung | Hauptfelder |
|-----------|-------------|-------------|
| `prinzipien` | Kernprinzipien des Frameworks | `id`, `name`, `beschreibung`, `hauptziele`, `schritte` |
| `regeln` | Explizite Do's & Don'ts | `id`, `text`, `kontext`, `beispiel` |
| `heuristiken` | Praxistipps, Daumenregeln | `regel`, `wann`, `beispiel` |
| `rollen` | Beteiligte/Rollen | `name`, `aufgaben`, `verantwortlichkeiten` |
| `prozesse` | Standardabläufe | `name`, `schritte`, `beteiligte`, `ziele` |
| `beispiele` | Konkrete Anwendungsfälle | `name`, `ausgangslage`, `transformation` |
| `transferbeispiele` | Übertragung auf neue Kontexte | `kontext`, `regel`, `beispiel` |
| `semantic_gaps` | Verständnisprobleme | `beschreibung`, `schwellenwert`, `lösung` |
| `lessons_learned` | Erfahrungen & Best Practices | `kategorie`, `erfahrung`, `empfehlung` |

## 🎨 GUI-Features

### Hauptfunktionen

- **📋 Kategorie-Navigation**: Einfache Navigation durch Framework-Kategorien
- **✏️ Item-Editor**: YAML-basierter Editor mit Templates
- **🔍 Suche**: Volltextsuche im gesamten Framework
- **📤 Export/Import**: YAML-basierte Datensicherung
- **📊 Struktur-Analyse**: Überblick über Framework-Vollständigkeit
- **🔍 Lücken-Analyse**: Identifikation fehlender Komponenten

### Bedienung

1. **Linke Spalte**: Kategorie- und Item-Navigation
2. **Mittlere Spalte**: Suchfunktion und Inhaltsanzeige
3. **Rechte Spalte**: Export/Import und Analyse-Tools

## 🔧 Erweiterte Funktionen

### Templates

Für jede Kategorie gibt es vordefinierte YAML-Templates:

```yaml
# Beispiel: Prinzip-Template
id: ""
name: ""
beschreibung: ""
hauptziele:
  - ""
schritte:
  - ""
regeln:
  - id: ""
    text: ""
heuristiken:
  - ""
# ... weitere Felder
```

### Import/Export

- **Export**: Framework als YAML-Datei exportieren
- **Import**: Bestehende YAML-Dateien importieren
- **Backup**: Automatische Datensicherung

### Analyse-Tools

- **Struktur-Analyse**: Zeigt Kategorien und Item-Anzahl
- **Lücken-Analyse**: Identifiziert fehlende kritische Komponenten
- **Empfehlungen**: Vorschläge zur Framework-Verbesserung

## 📁 Dateistruktur

```
Code_book_Life/
├── codebook_life_gui.py          # Haupt-GUI
├── start_codebook_life.py        # Start-Skript
├── requirements.txt              # Python-Abhängigkeiten
├── README.md                     # Diese Dokumentation
└── codebook_data/               # Datenverzeichnis
    └── life_framework.yaml      # Framework-Daten
```

## 🔄 Workflow

### Typischer Arbeitsablauf

1. **Framework initialisieren**: GUI starten, Grundstruktur wird automatisch erstellt
2. **Prinzipien definieren**: Kernprinzipien des LIFE Frameworks hinzufügen
3. **Regeln dokumentieren**: Explizite Do's & Don'ts formulieren
4. **Rollen definieren**: Beteiligte und ihre Aufgaben beschreiben
5. **Prozesse dokumentieren**: Standardabläufe strukturieren
6. **Beispiele sammeln**: Konkrete Anwendungsfälle hinzufügen
7. **Transfer dokumentieren**: Übertragungsregeln für neue Kontexte
8. **Lücken schließen**: Regelmäßige Analyse und Ergänzung

### Best Practices

- **Konsistente IDs**: Eindeutige Identifikatoren verwenden
- **Klare Beschreibungen**: Verständliche, präzise Formulierungen
- **Beispiele hinzufügen**: Konkrete Anwendungsfälle dokumentieren
- **Regelmäßige Analyse**: Lücken-Analyse zur Qualitätssicherung
- **Backup erstellen**: Regelmäßige YAML-Exports

## 🛠️ Technische Details

### Abhängigkeiten

- **Python 3.7+**
- **tkinter** (GUI-Framework)
- **PyYAML** (YAML-Verarbeitung)
- **pathlib** (Dateisystem-Operationen)

### Datenformat

Alle Daten werden im YAML-Format gespeichert für:
- **Menschliche Lesbarkeit**
- **Versionskontrolle**
- **Einfache Bearbeitung**
- **Strukturierte Hierarchie**

## 📈 Roadmap

### Geplante Features

- [ ] **PDF-Import**: Automatische Extraktion aus LIFE-Dokumenten
- [ ] **GPT-Integration**: KI-gestützte Analyse und Vorschläge
- [ ] **Visualisierung**: Grafische Darstellung der Framework-Struktur
- [ ] **Kollaboration**: Multi-User-Funktionalität
- [ ] **Validierung**: Automatische Konsistenzprüfung
- [ ] **Export-Formate**: HTML, PDF, Markdown

### Nächste Schritte

1. **Basis-Framework** mit vorhandenen LIFE-Dokumenten befüllen
2. **Templates** für spezifische LIFE-Komponenten erstellen
3. **Analyse-Tools** erweitern
4. **Import-Funktionen** für PDF-Dokumente

## 🤝 Nutzung

Das System ist darauf ausgelegt, das LIFE Framework strukturiert zu dokumentieren und kontinuierlich zu erweitern. Es unterstützt sowohl die initiale Erfassung als auch die laufende Pflege und Weiterentwicklung.

### Zielgruppen

- **Framework-Entwickler**: Strukturierte Dokumentation
- **Anwender**: Nachschlagewerk und Leitfaden
- **Trainer**: Schulungsmaterial und Beispiele
- **Berater**: Transferhilfen für neue Kontexte

---

**Codebook LIFE** - Strukturierte Dokumentation für bessere Framework-Anwendung 🚀 