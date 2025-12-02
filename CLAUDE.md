# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PythonPursuit is a comprehensive Python learning repository with two main components:

1. **python-basic/** - Educational materials covering Python fundamentals to advanced topics
2. **python-toolkit/** - Practical Python utilities for document processing (Excel/Word operations)

The repository emphasizes modern Python development practices, Chinese-language documentation, and real-world application of architectural patterns.

## Development Environment Setup

### Package Management
This project uses `uv` (modern Python package manager) as the primary tool. Traditional `pip` may encounter PEP 668 errors on macOS/Linux systems.

**Install uv:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Set up Chinese mirror source (optional):**
```bash
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
```

### Python Version Requirement
- Python 3.13+ (specified in pyproject.toml files)
- Virtual environments are required due to PEP 668 restrictions

### Project Structure Setup
Each subproject (python-basic, python-toolkit) has its own `pyproject.toml` and should be treated as independent Python packages.

## Build and Development Commands

### Installing Dependencies
For each subproject directory:
```bash
cd python-toolkit  # or python-basic
uv pip install -e .
```

### Running Tests
**python-toolkit tests:**
```bash
cd python-toolkit/test
uv run pytest  # Run all tests
uv run pytest -s excel_operator_test/test_read_successive_cells.py  # Run single test
```
The `-s` flag enables print output in tests.

**Test structure:**
- Tests use `sys.path.append('../src')` to import source modules
- Test data paths are configured in `config.py` files
- Tests are organized by functionality (excel_operator_test/, word_operator_test/)

### Adding/Removing Dependencies
```bash
uv add "package-name"    # Add dependency
uv remove "package-name" # Remove dependency
```

## Codebase Architecture

### python-basic/ Structure
- **basics/** - Fundamental Python concepts with example code
  - `num/`, `time/`, `list/`, `class/`, `dict/`, `exception/`, etc.
- **advanced/** - Advanced Python topics
  - `1.1 performance/` - Concurrency, asyncio, multiprocessing
  - `1.2 memory/` - Memory management and optimization
  - `1.3 Metaprogramming and Reflection/` - Metaclasses, descriptors
  - `1.4 Design Patterns/` - Python design pattern implementations
  - `1.5 Big Project/` - Architecture patterns (DDD, CQRS, DI)
- **tools/** - Utility tools and libraries
- **dataAnalysis/** - Data analysis examples
- **Webframework-Compare/** - Web framework comparisons

### python-toolkit/ Structure
- **src/** - Source code for utilities
  - `excel/` - Excel file operations using openpyxl
  - `word/` - Word document operations using python-docx
  - `file_opener/` - Enhanced file/website/software opener
- **test/** - Comprehensive test suite using pytest

### Key Dependencies
**python-basic:**
- `memory-profiler` - Memory usage analysis
- `psutil` - System and process utilities

**python-toolkit:**
- `openpyxl` - Excel file operations
- `pandas` - Data manipulation
- `pytest` - Testing framework
- `python-docx` - Word document operations

## Learning Curriculum (python-basic)

The repository follows a structured learning path documented in `python-basic/advanced/Main Curriculum.md`:

1. **Advanced Concurrency** - asyncio, multiprocessing, thread pools
2. **Memory Management** - GC mechanisms, memory analysis, profiling
3. **Metaprogramming** - metaclasses, descriptors, dynamic class creation
4. **Design Patterns** - Implementation of creational, structural, behavioral patterns
5. **Large Project Architecture** - Modular design, DI, DDD, configuration management
6. **Database & ORM** - Connection pools, transactions, query optimization
7. **Network Programming** - RESTful APIs, WebSocket, message queues
8. **Security Practices** - Input validation, SQL injection prevention, auth
9. **Code Quality** - Refactoring, code review, documentation
10. **Real-world Projects** - Analysis of open-source architectures

## Important Notes

1. **Chinese Language** - Most documentation and code comments are in Chinese
2. **Modern Tooling** - Uses uv + pyproject.toml instead of pip + requirements.txt
3. **Practical Focus** - Emphasis on real-world applications over theoretical concepts
4. **Cross-Platform** - Setup guides for Windows, macOS, and Linux
5. **Architecture Patterns** - Includes implementations of DDD, CQRS, DI patterns

## Common Development Tasks

### Adding New Learning Materials
- Place in appropriate `python-basic/` subdirectory
- Include both `.md` documentation and `.py` example code
- Follow existing naming conventions (Chinese/English mixed)

### Adding New Utilities
- Place in `python-toolkit/src/` with appropriate subdirectory
- Write corresponding tests in `python-toolkit/test/`
- Update dependencies in `python-toolkit/pyproject.toml`

### Running Specific Examples
```bash
cd python-basic/basics/class
python3 example_file.py
```

### Troubleshooting PEP 668 Errors
If encountering "externally-managed-environment" errors:
1. Use virtual environments: `python3 -m venv venv && source venv/bin/activate`
2. Use uv as recommended: `uv pip install -e .`
3. Check `/installation/` directory for detailed guides