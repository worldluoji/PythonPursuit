import sys 
sys.path.append('../src')
from excel import excel_operator

def test_get_src_column_info():
    assert excel_operator.excel_column_alphabet_to_num("A") == 1
    assert excel_operator.excel_column_alphabet_to_num("AB") == 28
    assert excel_operator.excel_column_alphabet_to_num("ABA") == 729

    total, start = excel_operator.get_src_column_info("A:B")
    assert total == 2
    assert start == 0