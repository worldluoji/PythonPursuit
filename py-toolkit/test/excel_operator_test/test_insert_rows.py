import sys 
sys.path.append('../src')
import config
from excel import excel_operator
import os

def test_insert_rows():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_file_dir, config.template_dir, "demo.xlsx")
    print(filepath)
    sheetname = 'Sheet1'
    ret = excel_operator.insert_rows(filepath, sheetname, 3, 2,  [(3, 'A', 2), (3, 'B', "罗马"), (3, 'C', 44), (4, 'A', 3), (4, 'B', "拉齐奥"), (4, 'C', 43)], save_to="test.xlsx")
    try:
        assert ret is not None
    finally:
        os.remove("test.xlsx")