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

class CodebookLIFEGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.assistant = CodebookLIFEAssistant()
        self.current_category = None
        self.current_item_index = None
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
        
        for category in categories:
            self.category_listbox.insert(tk.END, category)
    
    def on_category_select(self, event):
        """Behandelt Kategorieauswahl"""
        selection = self.category_listbox.curselection()
        if selection:
            category = self.category_listbox.get(selection[0])
            self.current_category = category
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
