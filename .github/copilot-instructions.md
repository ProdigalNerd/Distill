# Distill EPUB Content Extractor

Distill is a Python CLI tool that extracts metadata, table of contents, and chapter text from EPUB files. The tool processes EPUB files and provides structured output with chapter IDs mapped to content for programmatic access.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap and Setup
- Install Python dependencies: `pip install -r requirements.txt`
  - Installs: ebooklib>=0.18, beautifulsoup4>=4.11.0 (plus lxml, soupsieve dependencies)
  - Installation takes ~10 seconds. NEVER CANCEL.
- Verify installation: `python3 distill.py --help`
- Create test directory: `mkdir -p test_files` (if not exists)

### Build and Test
- **Create test EPUB**: `python3 create_test_epub.py`
  - Creates `test_files/sample_book.epub` for testing
  - Takes ~0.1 seconds. NEVER CANCEL.
- **Run test suite**: `python3 test_distill.py`
  - Comprehensive tests of all functionality
  - Takes ~0.2 seconds. NEVER CANCEL. Set timeout to 30+ seconds.
- **Test CLI functionality**: `python3 distill.py test_files/sample_book.epub`
  - Tests main CLI interface with sample EPUB
  - Takes ~0.2 seconds. NEVER CANCEL.

### Run the Application
- **Basic usage**: `python3 distill.py path/to/book.epub`
- **Verbose output**: `python3 distill.py --verbose path/to/book.epub`
- **Demo chapter mapping**: `python3 demo_mapping.py`
  - Shows chapter ID → text content mapping functionality
  - Takes ~0.2 seconds. NEVER CANCEL.

## Validation

### Manual Testing Requirements
ALWAYS manually validate any new code by running these complete scenarios:

1. **Full CLI Workflow Test**:
   ```bash
   python3 create_test_epub.py
   python3 distill.py test_files/sample_book.epub
   python3 distill.py --verbose test_files/sample_book.epub
   ```
   - Verify metadata extraction (title, author)
   - Verify table of contents with 3 chapters
   - Verify chapter IDs and file names are displayed

2. **Error Handling Test**:
   ```bash
   python3 distill.py nonexistent.epub  # Should show file not found error
   echo "invalid" > test.txt && python3 distill.py test.txt  # Should show not EPUB error
   rm test.txt
   ```

3. **Complete Test Suite**:
   ```bash
   python3 test_distill.py
   ```
   - Must show "✅ All tests passed!" at the end
   - All extraction steps must succeed

4. **Programmatic API Test**:
   ```bash
   python3 demo_mapping.py
   ```
   - Verify chapter mapping functionality
   - Check content length reporting
   - Verify text preview extraction

### Build Validation
- Syntax check: `find . -name "*.py" -exec python3 -m py_compile {} \;`
- No linting tools are configured in this repository

## Common Tasks

### File Structure Overview
```
.
├── distill.py              # Main CLI tool
├── test_distill.py         # Test suite
├── create_test_epub.py     # Test EPUB generator
├── demo_mapping.py         # Chapter mapping demo
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── test_files/            # Generated test files
│   └── sample_book.epub   # Test EPUB (created by create_test_epub.py)
└── .github/
    └── copilot-instructions.md  # This file
```

### Key Components
- **EpubDistiller class** in `distill.py`: Core functionality for EPUB parsing
- **CLI interface**: Argument parsing, error handling, main entry point
- **Test infrastructure**: Automated test creation and validation
- **Chapter mapping**: ID-based content access for programmatic use

### Expected Output Examples

#### CLI Output Format:
```
Title: Sample Test Book
Author: Test Author

============================================================
TABLE OF CONTENTS
============================================================
  1. Introduction
     ID: chapter_001
     File: intro.xhtml

  2. Main Content
     ID: chapter_002
     File: main.xhtml

  3. Conclusion
     ID: chapter_003
     File: conclusion.xhtml

Total chapters extracted: 3
```

#### Test Suite Success Output:
```
Testing EpubDistiller functionality...
==================================================
✅ Successfully loaded EPUB file
✅ Metadata extracted - Title: 'Sample Test Book', Author: 'Test Author'
✅ Table of contents extracted - 3 chapters found
[... detailed chapter listing ...]
✅ All tests passed!
```

## Timing and Timeouts

All operations in this repository are extremely fast:
- **Dependency installation**: ~10 seconds
- **EPUB creation**: ~0.1 seconds  
- **CLI processing**: ~0.2 seconds
- **Test suite**: ~0.2 seconds
- **Demo scripts**: ~0.2 seconds

**NEVER CANCEL** any operation. Set timeouts to 30+ seconds for safety, though operations typically complete in under 1 second.

## Error Handling and Troubleshooting

### Common Issues and Solutions:
1. **Missing dependencies**: Run `pip install -r requirements.txt`
2. **File not found errors**: Ensure EPUB file exists and path is correct
3. **Invalid EPUB errors**: Verify file has .epub extension and valid format
4. **Test failures**: Ensure `test_files/sample_book.epub` exists (run `python3 create_test_epub.py`)

### Exit Codes:
- `0`: Success
- `1`: Error (file not found, invalid format, processing error)

## Development Guidelines

### Making Changes:
- ALWAYS run the full validation scenarios after any code changes
- Test both CLI interface and programmatic API usage
- Verify error handling still works correctly
- Run syntax compilation check before committing
- No specific formatting or linting requirements (none configured)

### Testing Strategy:
- Use `create_test_epub.py` to generate consistent test data
- Test with both valid and invalid inputs
- Verify all error conditions are handled gracefully
- Check both metadata extraction and content processing

### Python Environment:
- Requires Python 3.12.3 (or compatible)
- Dependencies: ebooklib>=0.18, beautifulsoup4>=4.11.0
- No virtual environment setup required (uses system Python)
- Compatible with standard Python package installation