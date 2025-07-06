import os
from pathlib import Path
import sys

# Ensure repository root is on PYTHONPATH for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from codebook_life_gui import CodebookLIFEAssistant


def test_add_export_import(tmp_path):
    assistant = CodebookLIFEAssistant(codebook_directory=tmp_path)
    assistant.add_item_to_category('prinzipien', {'id': 'T1', 'name': 'Temp'})
    assert len(assistant.get_category_items('prinzipien')) == 1
    export_path = assistant.export_framework_to_yaml('export.yaml')
    assert Path(export_path).exists()
    assistant.import_framework_from_yaml(export_path)
    assert len(assistant.get_category_items('prinzipien')) == 1


def test_analyze_content(tmp_path):
    assistant = CodebookLIFEAssistant(codebook_directory=tmp_path)
    data = assistant.import_file_content('start_codebook_life.py')
    assert data['suggested_category']
