import sys
sys.path.append('../src')
from word import word_operator
from docx import Document
from docx.shared import RGBColor
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def test_add_to_end():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    doc = Document(os.path.join(current_file_dir, 'data', 'demo.docx'))

    TEXT = '你好 Python!!!'
    styles = {'font': {'name': '宋体', 'color': RGBColor(255,0,0), 'bold': True, 'underline': True, 'size': Pt(12)},
    'paragraph_format': {'alignment': WD_ALIGN_PARAGRAPH.LEFT, 'left_indent': Pt(2)}}
    word_operator.add_to_end(doc, TEXT, save_to="test.docx", styles=styles)

    os.remove("test.docx")
    assert doc.paragraphs[-1].text == TEXT
