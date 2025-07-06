#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Codebook LIFE GUI - LIFE Framework Management Interface
======================================================
Benutzerfreundliche GUI für die Verwaltung des LIFE Framework Codebooks
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from datetime import datetime
from pathlib import Path
import re
import yaml
import json
import os
from typing import Dict, List, Any, Optional
from difflib import SequenceMatcher
import mimetypes

class CodebookLIFEAssistant:
    def __init__(self, codebook_directory="./codebook_data"):
        self.codebook_dir = Path(codebook_directory)
        self.codebook_dir.mkdir(exist_ok=True)
        self.pending_changes = []
        self.framework_file = self.codebook_dir / "life_framework.yaml"
        self.framework_data = self._load_framework_data()
        
    def _load_framework_data(self) -> Dict[str, Any]:
        """Lädt die LIFE Framework Daten"""
        if self.framework_file.exists():
            try:
                with open(self.framework_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Fehler beim Laden der Framework-Daten: {e}")
                return self._create_default_framework()
        else:
            return self._create_default_framework()
    
    def _create_default_framework(self) -> Dict[str, Any]:
        """Erstellt die Standard LIFE Framework Struktur"""
        return {
            "framework": {
                "meta": {
                    "name": "LIFE",
                    "version": "1.0",
                    "autor": "Anonymous Developer",
                    "stand": datetime.now().strftime("%Y-%m"),
                    "ziel": "Strukturiertes Codebook für LIFE Framework"
                },
                "prinzipien": [],
                "regeln": [],
                "heuristiken": [],
                "rollen": [],
                "prozesse": [],
                "beispiele": [],
                "transferbeispiele": [],
                "semantic_gaps": [],
                "lessons_learned": [],
                "open_questions": []
            }
        }
    
    def _save_framework_data(self):
        """Speichert die Framework Daten"""
        try:
            with open(self.framework_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.framework_data, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Framework-Daten: {e}")
    
    def get_framework_categories(self) -> List[str]:
        """Gibt alle Kategorien des Frameworks zurück"""
        if "framework" in self.framework_data:
            return [key for key in self.framework_data["framework"].keys() if key != "meta"]
        return []
    
    def get_category_items(self, category: str) -> List[Dict[str, Any]]:
        """Gibt alle Items einer Kategorie zurück"""
        if "framework" in self.framework_data and category in self.framework_data["framework"]:
            return self.framework_data["framework"][category]
        return []
    
    def add_item_to_category(self, category: str, item: Dict[str, Any]):
        """Fügt ein Item zu einer Kategorie hinzu"""
        if "framework" not in self.framework_data:
            self.framework_data = self._create_default_framework()
        
        if category not in self.framework_data["framework"]:
            self.framework_data["framework"][category] = []
        
        self.framework_data["framework"][category].append(item)
        self._save_framework_data()
    
    def update_item_in_category(self, category: str, index: int, item: Dict[str, Any]):
        """Aktualisiert ein Item in einer Kategorie"""
        if ("framework" in self.framework_data and 
            category in self.framework_data["framework"] and 
            0 <= index < len(self.framework_data["framework"][category])):
            
            self.framework_data["framework"][category][index] = item
            self._save_framework_data()
    
    def delete_item_from_category(self, category: str, index: int):
        """Löscht ein Item aus einer Kategorie"""
        if ("framework" in self.framework_data and 
            category in self.framework_data["framework"] and 
            0 <= index < len(self.framework_data["framework"][category])):
            
            del self.framework_data["framework"][category][index]
            self._save_framework_data()
    
    def export_framework_to_yaml(self, output_file: str = "life_framework_export.yaml"):
        """Exportiert das Framework als YAML"""
        try:
            export_path = self.codebook_dir / output_file
            with open(export_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.framework_data, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            return str(export_path)
        except Exception as e:
            print(f"Fehler beim Export: {e}")
            return None
    
    def import_framework_from_yaml(self, yaml_file: str):
        """Importiert Framework-Daten aus YAML"""
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                imported_data = yaml.safe_load(f)
            
            if "framework" in imported_data:
                self.framework_data = imported_data
                self._save_framework_data()
                return True
        except Exception as e:
            print(f"Fehler beim Import: {e}")
        return False
    
    def analyze_framework_structure(self) -> Dict[str, Any]:
        """Analysiert die Framework-Struktur"""
        if "framework" not in self.framework_data:
            return {}
        
        framework = self.framework_data["framework"]
        analysis = {
            "total_categories": len([k for k in framework.keys() if k != "meta"]),
            "categories": {},
            "total_items": 0
        }
        
        for category, items in framework.items():
            if category == "meta":
                continue
                
            if isinstance(items, list):
                analysis["categories"][category] = len(items)
                analysis["total_items"] += len(items)
            else:
                analysis["categories"][category] = 1
                analysis["total_items"] += 1
        
        return analysis
    
    def search_in_framework(self, search_term: str) -> List[Dict[str, Any]]:
        """Sucht nach einem Begriff im Framework"""
        results = []
        search_term = search_term.lower()
        
        if "framework" not in self.framework_data:
            return results
        
        for category, items in self.framework_data["framework"].items():
            if category == "meta":
                continue
                
            if isinstance(items, list):
                for i, item in enumerate(items):
                    if self._item_matches_search(item, search_term):
                        results.append({
                            "category": category,
                            "index": i,
                            "item": item,
                            "match_type": "content"
                        })
        
        return results
    
    def _item_matches_search(self, item: Dict[str, Any], search_term: str) -> bool:
        """Prüft ob ein Item den Suchbegriff enthält"""
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, str) and search_term in value.lower():
                    return True
                elif isinstance(value, list):
                    for list_item in value:
                        if isinstance(list_item, str) and search_term in list_item.lower():
                            return True
        elif isinstance(item, str) and search_term in item.lower():
            return True
        
        return False
    
    def analyze_content_for_category(self, content: str, file_extension: str = "") -> str:
        """Analysiert Inhalt und schlägt passende Kategorie vor"""
        content_lower = content.lower()
        
        # Keyword-basierte Kategorisierung
        category_keywords = {
            "prinzipien": ["prinzip", "grundsatz", "user story", "mapping", "slicing", "narrative", "persona"],
            "regeln": ["regel", "do", "don't", "nicht", "immer", "niemals", "muss", "soll"],
            "heuristiken": ["heuristik", "daumenregel", "faustregel", "wenn", "dann", "tipp", "trick"],
            "rollen": ["rolle", "verantwortung", "aufgabe", "owner", "manager", "team", "stakeholder"],
            "prozesse": ["prozess", "ablauf", "schritt", "workflow", "refinement", "replenishment", "daily"],
            "beispiele": ["beispiel", "case", "story", "anwendung", "projekt", "umsetzung"],
            "transferbeispiele": ["transfer", "übertragung", "anpassung", "kontext", "transformation"],
            "semantic_gaps": ["gap", "lücke", "problem", "verständnis", "missverständnis", "schwierigkeit"],
            "lessons_learned": ["lesson", "erfahrung", "gelernt", "erkenntnisse", "best practice", "fehler"],
            "open_questions": ["frage", "offen", "todo", "unklar", "klären", "diskussion"]
        }
        
        # Dateierweiterung berücksichtigen
        if file_extension:
            if file_extension.lower() in ['.py', '.python']:
                # Python-Dateien sind oft Beispiele oder Prozesse
                if any(keyword in content_lower for keyword in ["class", "def", "import"]):
                    return "beispiele"
            elif file_extension.lower() in ['.yaml', '.yml']:
                # YAML-Dateien können verschiedene Strukturen haben
                if "id:" in content_lower and "name:" in content_lower:
                    return "prinzipien"
            elif file_extension.lower() == '.txt':
                # Text-Dateien sind oft Dokumentation
                if any(keyword in content_lower for keyword in ["regel", "prinzip"]):
                    return "regeln" if "regel" in content_lower else "prinzipien"
        
        # Keyword-Matching
        category_scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                category_scores[category] = score
        
        # Beste Kategorie zurückgeben
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])[0]
            return best_category
        
        # Fallback
        return "unknown"
    
    def import_file_content(self, file_path: str) -> Dict[str, Any]:
        """Importiert Dateiinhalt und schlägt Kategorie vor"""
        try:
            file_path_obj = Path(file_path)
            extension = file_path_obj.suffix
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Kategorie analysieren
            suggested_category = self.analyze_content_for_category(content, extension)
            
            # Basis-Item erstellen
            item_data = {
                "name": file_path_obj.stem,
                "beschreibung": f"Importiert aus {file_path_obj.name}",
                "original_file": str(file_path_obj),
                "import_date": datetime.now().isoformat(),
                "suggested_category": suggested_category
            }
            
            # Je nach Dateityp spezifische Verarbeitung
            if extension.lower() in ['.yaml', '.yml']:
                try:
                    yaml_data = yaml.safe_load(content)
                    if isinstance(yaml_data, dict):
                        item_data.update(yaml_data)
                except:
                    item_data["raw_content"] = content
            elif extension.lower() == '.py':
                item_data["code"] = content
                item_data["language"] = "python"
            else:
                item_data["raw_content"] = content
            
            return item_data
            
        except Exception as e:
            raise Exception(f"Fehler beim Importieren der Datei: {str(e)}")
    
    def add_category(self, category_name: str, description: str = ""):
        """Fügt eine neue Kategorie hinzu"""
        if "framework" not in self.framework_data:
            self.framework_data = self._create_default_framework()
        
        category_key = category_name.lower().replace(" ", "_")
        
        if category_key not in self.framework_data["framework"]:
            self.framework_data["framework"][category_key] = []
            
            # Meta-Information über die neue Kategorie
            if "category_meta" not in self.framework_data["framework"]:
                self.framework_data["framework"]["category_meta"] = {}
            
            self.framework_data["framework"]["category_meta"][category_key] = {
                "display_name": category_name,
                "description": description,
                "created_date": datetime.now().isoformat(),
                "custom": True
            }
            
            self._save_framework_data()
            return True
        
        return False

class CodebookLIFEGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.assistant = CodebookLIFEAssistant()
        self.current_category = None
        self.current_item_index = None
        self.category_mapping = {}
        self.setup_gui()
        
    def setup_gui(self):
        """Erstellt die GUI"""
        self.root.title("Codebook LIFE - Framework Management")
        self.root.geometry("1400x900")
        
        # Hauptframe
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Linke Spalte - Navigation
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Kategorie-Auswahl
        ttk.Label(left_frame, text="Framework Kategorien", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        
        self.category_listbox = tk.Listbox(left_frame, width=25, height=12)
        self.category_listbox.pack(pady=(0, 10))
        self.category_listbox.bind('<<ListboxSelect>>', self.on_category_select)
        
        # Items in Kategorie
        ttk.Label(left_frame, text="Items in Kategorie", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        
        self.item_listbox = tk.Listbox(left_frame, width=25, height=15)
        self.item_listbox.pack(pady=(0, 10))
        self.item_listbox.bind('<<ListboxSelect>>', self.on_item_select)
        
        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Neues Item", command=self.create_new_item).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="📁 Datei importieren", command=self.import_file).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="➕ Neue Kategorie", command=self.add_new_category).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Item bearbeiten", command=self.edit_current_item).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Item löschen", command=self.delete_current_item).pack(fill=tk.X, pady=2)
        
        # Mittlere Spalte - Hauptinhalt
        middle_frame = ttk.Frame(main_frame)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Suchbereich
        search_frame = ttk.Frame(middle_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Suche im Framework:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.search_entry.bind('<Return>', self.search_framework)
        ttk.Button(search_frame, text="Suchen", command=self.search_framework).pack(side=tk.LEFT, padx=(5, 0))
        
        # Inhalt anzeigen
        content_frame = ttk.LabelFrame(middle_frame, text="Item Details")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.content_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, height=25)
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Rechte Spalte - Tools
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Label(right_frame, text="Framework Tools", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Framework Tools
        tools_frame = ttk.LabelFrame(right_frame, text="Export/Import")
        tools_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(tools_frame, text="📤 YAML Export", command=self.export_framework).pack(fill=tk.X, pady=2)
        ttk.Button(tools_frame, text="📥 YAML Import", command=self.import_framework).pack(fill=tk.X, pady=2)
        
        # Analyse Tools
        analysis_frame = ttk.LabelFrame(right_frame, text="Analyse")
        analysis_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(analysis_frame, text="📊 Struktur-Analyse", command=self.analyze_structure).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="🔍 Lücken-Analyse", command=self.analyze_gaps).pack(fill=tk.X, pady=2)
        
        # Semantic Grabber Tools
        grabber_frame = ttk.LabelFrame(right_frame, text="Semantic Grabber")
        grabber_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(grabber_frame, text="🔧 Grabber Library", command=self.open_grabber_library).pack(fill=tk.X, pady=2)
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Codebook LIFE bereit")
        status_label = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Daten laden
        self.refresh_categories()
    
    def refresh_categories(self):
        """Aktualisiert die Kategorienliste"""
        self.category_listbox.delete(0, tk.END)
        categories = self.assistant.get_framework_categories()
        
        # Füge "unknown" Kategorie hinzu, falls nicht vorhanden
        if "unknown" not in categories:
            categories.append("unknown")
        
        for category in categories:
            # Zeige benutzerfreundliche Namen für Kategorien
            display_name = category.replace("_", " ").title()
            self.category_listbox.insert(tk.END, display_name)
            
        # Speichere Mapping für interne Verwendung
        self.category_mapping = {category.replace("_", " ").title(): category for category in categories}
    
    def on_category_select(self, event):
        """Behandelt Kategorieauswahl"""
        selection = self.category_listbox.curselection()
        if selection:
            display_name = self.category_listbox.get(selection[0])
            self.current_category = self.category_mapping.get(display_name, display_name.lower().replace(" ", "_"))
            self.refresh_items()
    
    def refresh_items(self):
        """Aktualisiert die Item-Liste"""
        self.item_listbox.delete(0, tk.END)
        
        if self.current_category:
            items = self.assistant.get_category_items(self.current_category)
            
            for i, item in enumerate(items):
                if isinstance(item, dict):
                    name = item.get('name', item.get('id', f'Item {i+1}'))
                else:
                    name = str(item)[:50] + "..." if len(str(item)) > 50 else str(item)
                
                self.item_listbox.insert(tk.END, name)
    
    def on_item_select(self, event):
        """Behandelt Item-Auswahl"""
        selection = self.item_listbox.curselection()
        if selection and self.current_category:
            self.current_item_index = selection[0]
            self.show_item_content()
    
    def show_item_content(self):
        """Zeigt den Inhalt des ausgewählten Items"""
        if self.current_category and self.current_item_index is not None:
            items = self.assistant.get_category_items(self.current_category)
            
            if 0 <= self.current_item_index < len(items):
                item = items[self.current_item_index]
                
                self.content_text.delete(1.0, tk.END)
                
                if isinstance(item, dict):
                    content = yaml.dump(item, default_flow_style=False, allow_unicode=True)
                else:
                    content = str(item)
                
                self.content_text.insert(tk.END, content)
    
    def create_new_item(self):
        """Erstellt ein neues Item"""
        if not self.current_category:
            messagebox.showwarning("Warnung", "Bitte wählen Sie zuerst eine Kategorie aus.")
            return
        
        self.open_item_editor()
    
    def edit_current_item(self):
        """Bearbeitet das aktuelle Item"""
        if not self.current_category or self.current_item_index is None:
            messagebox.showwarning("Warnung", "Bitte wählen Sie zuerst ein Item aus.")
            return
        
        self.open_item_editor(edit_mode=True)
    
    def open_item_editor(self, edit_mode=False):
        """Öffnet den Item-Editor"""
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Item Editor")
        editor_window.geometry("800x600")
        
        # Aktueller Inhalt
        current_item = {}
        if edit_mode and self.current_item_index is not None:
            items = self.assistant.get_category_items(self.current_category)
            if 0 <= self.current_item_index < len(items):
                current_item = items[self.current_item_index]
        
        # Editor-Bereich
        ttk.Label(editor_window, text=f"Item für Kategorie: {self.current_category}", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # YAML Editor
        text_frame = ttk.Frame(editor_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        editor_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD)
        editor_text.pack(fill=tk.BOTH, expand=True)
        
        # Vorbefüllen mit Template oder aktuellem Inhalt
        if current_item:
            editor_text.insert(tk.END, yaml.dump(current_item, default_flow_style=False, allow_unicode=True))
        else:
            template = self.get_template_for_category(self.current_category)
            editor_text.insert(tk.END, template)
        
        # Buttons
        button_frame = ttk.Frame(editor_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def save_item():
            try:
                yaml_content = editor_text.get(1.0, tk.END).strip()
                item_data = yaml.safe_load(yaml_content)
                
                if edit_mode:
                    self.assistant.update_item_in_category(self.current_category, self.current_item_index, item_data)
                else:
                    self.assistant.add_item_to_category(self.current_category, item_data)
                
                self.refresh_items()
                self.update_status("Item erfolgreich gespeichert")
                editor_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")
        
        ttk.Button(button_frame, text="Speichern", command=save_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Abbrechen", command=editor_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def get_template_for_category(self, category: str) -> str:
        """Gibt ein Template für die jeweilige Kategorie zurück"""
        templates = {
            "prinzipien": """id: ""
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
narrative_beispiele:
  - ""
transferbeispiele:
  - kontext: ""
    regel: ""
    beispiel: ""
semantic_gaps:
  - beschreibung: ""
    schwellenwert: ""
    lösung: ""
lessons_learned:
  - ""
""",
            "regeln": """id: ""
text: ""
kontext: ""
beispiel: ""
""",
            "heuristiken": """regel: ""
wann: ""
beispiel: ""
""",
            "rollen": """name: ""
aufgaben:
  - ""
verantwortlichkeiten:
  - ""
interaktionen:
  - ""
""",
            "prozesse": """name: ""
schritte:
  - ""
beteiligte:
  - ""
ziele:
  - ""
""",
            "beispiele": """name: ""
ausgangslage: ""
transformation: ""
lessons_learned:
  - ""
""",
            "transferbeispiele": """kontext: ""
regel: ""
beispiel: ""
""",
            "semantic_gaps": """beschreibung: ""
schwellenwert: ""
lösung: ""
""",
            "lessons_learned": """kategorie: ""
erfahrung: ""
empfehlung: ""
""",
            "open_questions": """frage: ""
kontext: ""
priorität: ""
"""
        }
        
        return templates.get(category, "# Neues Item\nname: \"\"\nbeschreibung: \"\"\n")
    
    def delete_current_item(self):
        """Löscht das aktuelle Item"""
        if not self.current_category or self.current_item_index is None:
            messagebox.showwarning("Warnung", "Bitte wählen Sie zuerst ein Item aus.")
            return
        
        if messagebox.askyesno("Bestätigung", "Möchten Sie das ausgewählte Item wirklich löschen?"):
            self.assistant.delete_item_from_category(self.current_category, self.current_item_index)
            self.refresh_items()
            self.content_text.delete(1.0, tk.END)
            self.current_item_index = None
            self.update_status("Item gelöscht")
    
    def search_framework(self, event=None):
        """Sucht im Framework"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            return
        
        results = self.assistant.search_in_framework(search_term)
        
        if results:
            self.show_search_results(results)
        else:
            messagebox.showinfo("Suche", f"Keine Ergebnisse für '{search_term}' gefunden.")
    
    def show_search_results(self, results):
        """Zeigt Suchergebnisse an"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Suchergebnisse")
        result_window.geometry("800x600")
        
        ttk.Label(result_window, text=f"Gefunden: {len(results)} Ergebnisse", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Ergebnisliste
        results_frame = ttk.Frame(result_window)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        results_text.pack(fill=tk.BOTH, expand=True)
        
        for result in results:
            category = result["category"]
            item = result["item"]
            
            results_text.insert(tk.END, f"Kategorie: {category}\n")
            results_text.insert(tk.END, "-" * 50 + "\n")
            
            if isinstance(item, dict):
                content = yaml.dump(item, default_flow_style=False, allow_unicode=True)
            else:
                content = str(item)
            
            results_text.insert(tk.END, content + "\n\n")
    
    def export_framework(self):
        """Exportiert das Framework"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        
        if filename:
            export_path = self.assistant.export_framework_to_yaml(filename)
            if export_path:
                messagebox.showinfo("Export", f"Framework erfolgreich exportiert nach:\n{export_path}")
                self.update_status("Framework exportiert")
            else:
                messagebox.showerror("Fehler", "Fehler beim Export")
    
    def import_framework(self):
        """Importiert ein Framework"""
        filename = filedialog.askopenfilename(
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        
        if filename:
            if self.assistant.import_framework_from_yaml(filename):
                self.refresh_categories()
                messagebox.showinfo("Import", "Framework erfolgreich importiert")
                self.update_status("Framework importiert")
            else:
                messagebox.showerror("Fehler", "Fehler beim Import")
    
    def analyze_structure(self):
        """Analysiert die Framework-Struktur"""
        analysis = self.assistant.analyze_framework_structure()
        
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Struktur-Analyse")
        analysis_window.geometry("600x400")
        
        ttk.Label(analysis_window, text="Framework Struktur-Analyse", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        analysis_text = scrolledtext.ScrolledText(analysis_window, wrap=tk.WORD)
        analysis_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Analyse-Ergebnisse anzeigen
        analysis_text.insert(tk.END, f"Gesamt-Kategorien: {analysis.get('total_categories', 0)}\n")
        analysis_text.insert(tk.END, f"Gesamt-Items: {analysis.get('total_items', 0)}\n\n")
        
        analysis_text.insert(tk.END, "Kategorien im Detail:\n")
        analysis_text.insert(tk.END, "=" * 30 + "\n")
        
        for category, count in analysis.get('categories', {}).items():
            analysis_text.insert(tk.END, f"{category}: {count} Items\n")
        
        # Empfehlungen
        analysis_text.insert(tk.END, "\nEmpfehlungen:\n")
        analysis_text.insert(tk.END, "=" * 30 + "\n")
        
        for category, count in analysis.get('categories', {}).items():
            if count == 0:
                analysis_text.insert(tk.END, f"⚠️ {category}: Keine Items vorhanden\n")
            elif count < 3:
                analysis_text.insert(tk.END, f"💡 {category}: Könnte mehr Items vertragen ({count} vorhanden)\n")
    
    def analyze_gaps(self):
        """Analysiert Lücken im Framework"""
        gap_window = tk.Toplevel(self.root)
        gap_window.title("Lücken-Analyse")
        gap_window.geometry("600x400")
        
        ttk.Label(gap_window, text="Framework Lücken-Analyse", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        gap_text = scrolledtext.ScrolledText(gap_window, wrap=tk.WORD)
        gap_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lücken-Analyse
        categories = self.assistant.get_framework_categories()
        essential_categories = [
            "prinzipien", "regeln", "heuristiken", "rollen", 
            "prozesse", "beispiele", "transferbeispiele"
        ]
        
        gap_text.insert(tk.END, "Fehlende kritische Kategorien:\n")
        gap_text.insert(tk.END, "=" * 35 + "\n")
        
        missing_categories = []
        for cat in essential_categories:
            if cat not in categories:
                missing_categories.append(cat)
                gap_text.insert(tk.END, f"❌ {cat}\n")
        
        if not missing_categories:
            gap_text.insert(tk.END, "✅ Alle kritischen Kategorien vorhanden\n")
        
        gap_text.insert(tk.END, "\nSchwach besetzte Kategorien:\n")
        gap_text.insert(tk.END, "=" * 35 + "\n")
        
        for category in categories:
            items = self.assistant.get_category_items(category)
            if len(items) < 2:
                gap_text.insert(tk.END, f"⚠️ {category}: Nur {len(items)} Item(s)\n")
        
        gap_text.insert(tk.END, "\nEmpfohlene nächste Schritte:\n")
        gap_text.insert(tk.END, "=" * 35 + "\n")
        
        if missing_categories:
            gap_text.insert(tk.END, f"1. Fehlende Kategorien ergänzen: {', '.join(missing_categories)}\n")
        
        gap_text.insert(tk.END, "2. Mehr Beispiele und Transferfälle hinzufügen\n")
        gap_text.insert(tk.END, "3. Semantic Gaps dokumentieren\n")
        gap_text.insert(tk.END, "4. Lessons Learned sammeln\n")
    
    def import_file(self):
        """Importiert eine Datei und erstellt automatisch ein Item"""
        file_path = filedialog.askopenfilename(
            title="Datei für Import auswählen",
            filetypes=[
                ("Alle unterstützten", "*.txt;*.yaml;*.yml;*.py"),
                ("Text-Dateien", "*.txt"),
                ("YAML-Dateien", "*.yaml;*.yml"),
                ("Python-Dateien", "*.py"),
                ("Alle Dateien", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Datei importieren und analysieren
                item_data = self.assistant.import_file_content(file_path)
                suggested_category = item_data.get("suggested_category", "unknown")
                
                # Dialog für Kategorie-Bestätigung
                self.show_import_dialog(item_data, suggested_category)
                
            except Exception as e:
                messagebox.showerror("Import-Fehler", f"Fehler beim Importieren der Datei:\n{str(e)}")
    
    def show_import_dialog(self, item_data: Dict[str, Any], suggested_category: str):
        """Zeigt Dialog für Import-Bestätigung"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Datei-Import")
        dialog.geometry("600x500")
        
        # Header
        ttk.Label(dialog, text="Datei-Import", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Vorgeschlagene Kategorie
        category_frame = ttk.Frame(dialog)
        category_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(category_frame, text="Vorgeschlagene Kategorie:").pack(side=tk.LEFT)
        
        category_var = tk.StringVar(value=suggested_category)
        category_combo = ttk.Combobox(category_frame, textvariable=category_var, width=20)
        category_combo['values'] = list(self.category_mapping.keys())
        category_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Item-Vorschau
        ttk.Label(dialog, text="Item-Vorschau:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        preview_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, height=15)
        preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Vorschau befüllen
        preview_content = yaml.dump(item_data, default_flow_style=False, allow_unicode=True)
        preview_text.insert(tk.END, preview_content)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def import_item():
            selected_category = self.category_mapping.get(category_var.get(), category_var.get())
            
            # Item-Daten aus Vorschau lesen
            try:
                updated_content = preview_text.get(1.0, tk.END).strip()
                final_item_data = yaml.safe_load(updated_content)
                
                # Item hinzufügen
                self.assistant.add_item_to_category(selected_category, final_item_data)
                
                # GUI aktualisieren
                self.refresh_categories()
                if self.current_category == selected_category:
                    self.refresh_items()
                
                self.update_status(f"Datei erfolgreich importiert in Kategorie '{selected_category}'")
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Importieren: {str(e)}")
        
        ttk.Button(button_frame, text="Importieren", command=import_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Abbrechen", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def add_new_category(self):
        """Fügt eine neue Kategorie hinzu"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Neue Kategorie")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Neue Kategorie erstellen", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Name
        name_frame = ttk.Frame(dialog)
        name_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(name_frame, text="Name:").pack(side=tk.LEFT)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=name_var, width=30)
        name_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Beschreibung
        ttk.Label(dialog, text="Beschreibung:").pack(pady=(10, 5))
        desc_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, height=8)
        desc_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def create_category():
            name = name_var.get().strip()
            description = desc_text.get(1.0, tk.END).strip()
            
            if not name:
                messagebox.showwarning("Warnung", "Bitte geben Sie einen Namen ein.")
                return
            
            if self.assistant.add_category(name, description):
                self.refresh_categories()
                self.update_status(f"Kategorie '{name}' erstellt")
                dialog.destroy()
            else:
                messagebox.showwarning("Warnung", "Kategorie existiert bereits.")
        
        ttk.Button(button_frame, text="Erstellen", command=create_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Abbrechen", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def open_grabber_library(self):
        """Öffnet die Semantic Grabber Library"""
        grabber_window = tk.Toplevel(self.root)
        grabber_window.title("Semantic Grabber Library")
        grabber_window.geometry("1000x700")
        
        # Header
        ttk.Label(grabber_window, text="Semantic Grabber Library", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Hauptframe
        main_frame = ttk.Frame(grabber_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Linke Spalte - Grabber Liste
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Label(left_frame, text="Grabber", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        
        grabber_listbox = tk.Listbox(left_frame, width=25, height=20)
        grabber_listbox.pack(pady=(0, 10))
        
        # Grabber-Buttons
        grabber_button_frame = ttk.Frame(left_frame)
        grabber_button_frame.pack(fill=tk.X)
        
        ttk.Button(grabber_button_frame, text="Neuer Grabber").pack(fill=tk.X, pady=2)
        ttk.Button(grabber_button_frame, text="Bearbeiten").pack(fill=tk.X, pady=2)
        ttk.Button(grabber_button_frame, text="Löschen").pack(fill=tk.X, pady=2)
        
        # Rechte Spalte - Grabber Details
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_frame, text="Grabber Details", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        
        # Grabber Editor
        grabber_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD)
        grabber_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Control Buttons
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="Speichern").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Export").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Import").pack(side=tk.LEFT, padx=5)
        
        # Beispiel-Grabber laden
        example_grabber = """# Beispiel Semantic Grabber
id: example_grabber
name: "Beispiel Grabber"
description: "Ein Beispiel für einen Semantic Grabber"
patterns:
  - "user story"
  - "mapping"
  - "slicing"
keywords:
  - "prinzip"
  - "regel"
  - "heuristik"
semantic_rules:
  - if_contains: ["user", "story"]
    then_category: "prinzipien"
  - if_contains: ["regel", "do", "don't"]
    then_category: "regeln"
"""
        grabber_text.insert(tk.END, example_grabber)
        
        # Grabber-Liste befüllen
        grabber_listbox.insert(tk.END, "Example Grabber")
        grabber_listbox.insert(tk.END, "LIFE Framework Grabber")
        grabber_listbox.insert(tk.END, "Process Grabber")
    
    def update_status(self, message: str):
        """Aktualisiert die Statuszeile"""
        self.status_var.set(f"{message} - {datetime.now().strftime('%H:%M:%S')}")
    
    def run(self):
        """Startet die GUI"""
        self.root.mainloop()

def main():
    """Hauptfunktion"""
    app = CodebookLIFEGUI()
    app.run()

if __name__ == "__main__":
    main()
