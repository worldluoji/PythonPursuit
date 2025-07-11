import sys,os
sys.path.append('../src')
from docx import Document

def test_extract_headings():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    doc = Document(os.path.join(current_file_dir, 'data', 'heading_test.docx'))

    for para in doc.paragraphs:
        print(para.style.name, para.text)