# Distill - EPUB Content Extractor

Distill is a Python CLI tool that extracts metadata, table of contents, and chapter content from EPUB files. It provides a clean interface for programmatic access to EPUB data with HTML tag preservation.

**ALWAYS** reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Setup (First Time)
1. Ensure Python 3.12+ is available: `python3 --version`
2. Install dependencies: `pip3 install -r requirements.txt` -- takes 5 seconds
3. Create test environment: `mkdir -p test_files && python3 create_test_epub.py` -- takes <1 second
4. Validate setup: `python3 test_distill.py` -- takes <1 second

### Running Tests
- **ALWAYS** run tests after making any code changes: `python3 test_distill.py` -- takes <1 second
- Create fresh test EPUB if needed: `python3 create_test_epub.py` -- takes <1 second
- Test demo functionality: `python3 demo_mapping.py` -- takes <1 second

### Using the CLI
- Basic usage: `python3 distill.py path/to/book.epub` -- takes <1 second
- Verbose output: `python3 distill.py --verbose path/to/book.epub` -- takes <1 second
- Help: `python3 distill.py --help` -- takes <1 second
- Test with sample: `python3 distill.py test_files/sample_book.epub` -- takes <1 second

### Code Validation
- **ALWAYS** check Python syntax: `python3 -m py_compile *.py` -- takes <1 second
- No linting tools are configured - rely on manual code review and syntax checking
- All operations are extremely fast (under 5 seconds each) - no special timeout handling needed

## Validation Scenarios

**CRITICAL**: After making any changes to the code, ALWAYS run this complete validation sequence:

1. **Syntax Check**: `python3 -m py_compile distill.py test_distill.py create_test_epub.py demo_mapping.py`
2. **Test Suite**: `python3 test_distill.py` -- should show "✅ All tests passed!"
3. **CLI Functionality**: `python3 distill.py test_files/sample_book.epub` -- should display book metadata and 3 chapters
4. **Error Handling**: `python3 distill.py nonexistent.epub` -- should show "File 'nonexistent.epub' does not exist."
5. **Demo Script**: `python3 demo_mapping.py` -- should show chapter mapping with 3 entries

**Expected CLI Output** (for validation):
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

## Repository Structure

### Key Files
- `distill.py` - Main CLI application and EpubDistiller class
- `requirements.txt` - Python dependencies (ebooklib>=0.18, beautifulsoup4>=4.11.0)
- `test_distill.py` - Comprehensive test suite
- `create_test_epub.py` - Creates sample EPUB for testing
- `demo_mapping.py` - Demonstrates chapter ID → text mapping functionality
- `test_files/` - Directory for test EPUB files (created by setup)

### Core Functionality
The `EpubDistiller` class in `distill.py` provides:
- `load_book()` - Loads EPUB file and validates format
- `extract_metadata()` - Gets title and author from EPUB metadata
- `extract_table_of_contents()` - Parses TOC with chapter IDs and filenames
- `extract_chapter_text()` - Extracts text content while preserving HTML tags
- `build_chapter_mapping()` - Creates chapter ID → content mapping

## Common Tasks

### Adding New Features
1. Make changes to `distill.py`
2. Update tests in `test_distill.py` if needed
3. Run validation sequence (see above)
4. Test with actual EPUB files beyond the sample

### Troubleshooting
- **"Bad Zip file" error**: EPUB file is corrupted or not a valid EPUB
- **Dependencies missing**: Run `pip3 install -r requirements.txt`
- **Test files missing**: Run `python3 create_test_epub.py` to recreate
- **Permission errors**: Check write permissions on `test_files/` directory

### Working with Real EPUB Files
- The tool handles various EPUB formats and metadata variations
- Error handling is comprehensive for malformed files
- HTML content preservation allows navigation link analysis
- Chapter IDs are auto-generated as `chapter_001`, `chapter_002`, etc.

## Development Workflow

**Complete development cycle** (runs in ~5 seconds total):
```bash
# Install/update dependencies
pip3 install -r requirements.txt

# Create test environment
python3 create_test_epub.py

# Run tests
python3 test_distill.py

# Test CLI
python3 distill.py test_files/sample_book.epub
```

**NEVER CANCEL** any commands - all operations complete in under 5 seconds. No special timeout handling required.

## Repository Quick Reference

### Listing root directory
```
.
├── .git/
├── .github/
│   └── copilot-instructions.md
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── distill.py              # Main CLI application
├── test_distill.py         # Test suite
├── create_test_epub.py     # Test EPUB generator
├── demo_mapping.py         # Demo script
└── test_files/             # Created by setup
    └── sample_book.epub    # Sample test file
```

### Dependencies (requirements.txt)
```
ebooklib>=0.18
beautifulsoup4>=4.11.0
```

**Remember**: All operations are extremely fast. Always run the complete validation sequence after changes. The tool is robust and handles errors gracefully.