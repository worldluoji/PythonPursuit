# py-toolkit
python toolkits
```
src/excel: .xlsx excel operator
src/word: .doc or .docx document  operator
```

---

## run testcases
run all testcases
```
cd test
uv run pytest
```
run a testcase
```
cd test
uv run pytest -s excel_operator_test/test_read_successive_cells.py
```
'-s' means that print function has effect

---

## reference
- https://python-docx.readthedocs.io/en/latest/