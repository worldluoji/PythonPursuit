import sys 
sys.path.append('../src')
import config
from excel import excel_operator
import os

def test_write_to_single_cell():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_file_dir, config.template_dir, "demo.xlsx")
    sheetname = 'Sheet1'
    excel_operator.write_to_single_cell(filepath, sheetname, 3, 5, "pig", save_to="test.xlsx")
    try:
        assert excel_operator.read_successive_cells("test.xlsx", sheetname, "3", "E") == "pig"
    finally:
        os.remove("test.xlsx")