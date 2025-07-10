import sys 
sys.path.append('../src')
import config
from excel import excel_operator
import os

def test_read_successive_cells():
    # 这样获取的是当前文件所在目录，os.getcwd()获取的是执行脚本的命令行在目录
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_file_dir, config.template_dir, config.project_completion_status_cfg["src_file"])
    sheetname = config.project_completion_status_cfg['src_sheetname']
    expected = '''AC米兰\r\n国际米兰'''
    assert excel_operator.read_successive_cells(filepath, sheetname, "2:3", "B") == expected
    