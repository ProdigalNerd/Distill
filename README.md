# Distill - EPUB Content Extractor

Parse an e-book into chapter summarizations and key information

## Overview
Distill is a Python CLI tool that extracts content from EPUB files, providing:
- Book metadata (title, author)
- Table of contents (chapters with IDs)
- Chapter text with HTML tags preserved for navigation
- Chapter ID to text content mapping
- Optional AI-powered chapter summaries

## Requirements

- **Python**: 3.12+ (recommended) or 3.8+ (minimum)
- **Platform**: Cross-platform (Linux, macOS, Windows)

## Installation

### Option 1: Install from requirements.txt (Recommended)
```bash
pip install -r requirements.txt
```

### Option 2: Manual installation
```bash
# Core dependencies (required)
pip install ebooklib>=0.18 beautifulsoup4>=4.11.0

# Optional dependencies (for summarization)
pip install sumy>=0.11.0 numpy>=1.21.0 nltk>=3.6
```

## Usage

### Command Syntax
```bash
python3 distill.py [OPTIONS] EPUB_FILE
```

### Command Options

| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Show help message and exit |
| `--verbose` | `-v` | Enable verbose output for debugging |
| `--summary` | `-s` | Include AI-powered chapter summaries |

### Usage Examples

**Basic extraction:**
```bash
python3 distill.py book.epub
```

**With verbose output (shows debugging information):**
```bash
python3 distill.py --verbose book.epub
```

**Include chapter summaries:**
```bash
python3 distill.py --summary book.epub
```

**Combine options:**
```bash
python3 distill.py --verbose --summary book.epub
```

**Get help:**
```bash
python3 distill.py --help
```

## Output Format

### Basic Output
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

### With Summaries (--summary flag)
```
Title: Sample Test Book
Author: Test Author

============================================================
TABLE OF CONTENTS
============================================================
  1. Introduction
     ID: chapter_001
     File: intro.xhtml
     Summary:
       • This chapter introduces the main concepts of the book.
       • It provides an overview of what readers can expect to learn.

  2. Main Content
     ID: chapter_002
     File: main.xhtml
     Summary:
       • The main content covers the core principles and methodologies.
       • Practical examples are provided to illustrate key points.

Total chapters extracted: 3
```

## Features

- **📚 Metadata Extraction**: Automatically extracts book title and author from EPUB metadata
- **📋 Table of Contents**: Parses and displays the book's table of contents with unique chapter IDs
- **🔗 HTML Preservation**: Maintains HTML tags in chapter content for navigation links and formatting
- **🗺️ Chapter Mapping**: Creates a programmatic mapping from chapter IDs to text content
- **🤖 AI Summarization**: Optional intelligent chapter summaries using advanced NLP techniques
- **🔍 Verbose Mode**: Detailed debugging output for troubleshooting EPUB parsing issues
- **⚡ Fast Processing**: Efficient extraction suitable for large EPUB files
- **🛡️ Error Handling**: Robust error handling for missing files and invalid EPUB formats

## Testing and Development

### Quick Start
```bash
# Create test environment
python3 create_test_epub.py

# Run test suite
python3 test_distill.py

# Test with sample EPUB
python3 distill.py test_files/sample_book.epub
```

### Available Demo Scripts
- **`demo_mapping.py`** - Demonstrates chapter ID → text mapping
- **`create_test_epub.py`** - Creates sample EPUB files for testing
- **`demo_improved_summarization.py`** - Shows summarization capabilities
- **`test_distill.py`** - Comprehensive test suite

### Development Workflow
```bash
# Install dependencies
pip install -r requirements.txt

# Create test EPUB
python3 create_test_epub.py

# Run tests
python3 test_distill.py

# Test CLI functionality
python3 distill.py test_files/sample_book.epub

# Run demos
python3 demo_mapping.py
```

## Dependencies

### Core Dependencies (Required)
These packages are essential for basic EPUB processing:

- **`ebooklib>=0.18`** - EPUB file parsing and manipulation
- **`beautifulsoup4>=4.11.0`** - HTML content processing and cleaning

### Optional Dependencies (For Summarization)
These packages are only required if you use the `--summary` flag:

- **`sumy>=0.11.0`** - Text summarization algorithms
- **`numpy>=1.21.0`** - Numerical computing (required by sumy)
- **`nltk>=3.6`** - Natural language processing toolkit

### Installation Notes
- If you don't need summarization, you can install only the core dependencies
- The `--summary` flag will show an error if optional dependencies are missing
- All dependencies are automatically installed when using `pip install -r requirements.txt`

## Troubleshooting

### Common Issues

**"Bad Zip file" or "Not a valid EPUB" errors:**
```bash
# Check if file is corrupted
file book.epub

# Try with verbose output for more details
python3 distill.py --verbose book.epub
```

**"ModuleNotFoundError" errors:**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Or install manually
pip install ebooklib beautifulsoup4
```

**Summarization not working:**
```bash
# Install optional dependencies
pip install sumy nltk numpy

# Or check if dependencies are installed
python3 -c "import sumy, nltk, numpy; print('All summarization dependencies installed')"
```

**No content extracted:**
- Some EPUBs use non-standard file structures
- Try `--verbose` flag to see parsing details
- Check if EPUB has DRM protection (not supported)

**Permission errors:**
```bash
# Ensure write permissions for test files
chmod +w test_files/
```

### Getting Help

1. Run with `--verbose` for detailed debugging information
2. Check that your EPUB file is not DRM-protected
3. Verify Python version: `python3 --version` (3.8+ required)
4. Test with the sample EPUB: `python3 distill.py test_files/sample_book.epub`

## Programmatic Usage

You can also use Distill as a Python library:

```python
from distill import EpubDistiller

# Initialize
distiller = EpubDistiller("path/to/book.epub")
distiller.load_book()

# Extract metadata
title, author = distiller.extract_metadata()

# Get table of contents
toc = distiller.extract_table_of_contents()

# Build chapter mapping
chapter_mapping = distiller.build_chapter_mapping()

# Access specific chapter content
chapter_content = chapter_mapping.get("chapter_001", "")
```

## License

See LICENSE file for details.
