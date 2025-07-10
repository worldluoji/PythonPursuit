import sys 
sys.path.append('../src')
import config
from excel import excel_operator
import os


def test_copy_sheet():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_file_dir, config.template_dir, config.project_completion_status_cfg["src_file"])
    src_sheetname = config.project_completion_status_cfg["src_sheetname"]
    dst_dir = os.path.join(current_file_dir, config.template_dir, config.project_completion_status_cfg["dst_file"])
    dst_sheetname = config.project_completion_status_cfg["dst_sheetname"]
    
    excel_operator.copy_sheet(src_dir, src_sheetname,
        config.project_completion_status_cfg["src_copy_row"],
        config.project_completion_status_cfg["src_copy_column"],
        dst_dir, dst_sheetname,
        config.project_completion_status_cfg["dst_start_row"],
        config.project_completion_status_cfg["dst_start_column"]
    )