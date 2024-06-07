import sys 
sys.path.append('../src')
import config
from excel import excel_operator
import os

def test_write_to_cells():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_file_dir, config.template_dir, "demo.xlsx")
    print(filepath)
    sheetname = 'Sheet1'
    ret = excel_operator.write_to_cells(filepath, sheetname, [(3, 5, "cat"), (3, 4, "41")], save_to="test.xlsx")
    try:
        assert ret is not None
        assert excel_operator.read_successive_cells("test.xlsx", sheetname, "3", "D:E", "&&") == "41&&cat"
    finally:
        os.remove("test.xlsx")

def test_write_to_cells_alphabet():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_file_dir, config.template_dir, "demo.xlsx")
    print(filepath)
    sheetname = 'Sheet1'
    ret = excel_operator.write_to_cells(filepath, sheetname, [(3, 'E', "cat"), (3, 'D', "41")], save_to="test.xlsx")
    try:
        assert ret is not None
        assert excel_operator.read_successive_cells("test.xlsx", sheetname, "3", "D:E", "&&") == "41&&cat"
    finally:
        os.remove("test.xlsx")