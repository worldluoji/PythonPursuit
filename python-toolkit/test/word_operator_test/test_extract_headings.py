import sys,os
sys.path.append('../src')
from docx import Document
from word import word_operator

def test_extract_headings():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    doc = Document(os.path.join(current_file_dir, 'data', 'heading_test.docx'))

    headings = word_operator.extract_headings(doc)
    for item in headings:
        print(f"level: {item.get('level', '')}, 内容: {item['content']}")