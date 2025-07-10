import sys
sys.path.append('../src')
from word import word_operator
from docx import Document
import os

def test_replace_paragraph_text():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    doc = Document(os.path.join(current_file_dir, 'data', 'demo.docx'))
    TEXT = 'Change 级别 1'
    ret = word_operator.replace_paragraph_text(doc, 'Heading, level 1', TEXT, save_to="text.docx")
    os.remove("text.docx")
    assert ret == 0

def test_replace_table_cell_text():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    doc = Document(os.path.join(current_file_dir, 'data', 'demo.docx'))
    TEXT = '363'
    ret = word_operator.replace_table_cell_text(doc, '422', TEXT, save_to="text.docx")
    os.remove("text.docx")
    assert ret == 0