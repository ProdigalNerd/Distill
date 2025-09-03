# Distill
Parse an e-book into chapter summarizations and key information

## Overview
Distill is a CLI tool that extracts content from EPUB files, providing:
- Book metadata (title, author)
- Table of contents (chapters)
- Chapter text with HTML tags preserved for navigation
- Chapter ID to text content mapping

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python3 distill.py path/to/your/book.epub
```

### With verbose output
```bash
python3 distill.py --verbose path/to/your/book.epub
```

### Help
```bash
python3 distill.py --help
```

## Example Output
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

## Features

- **Metadata Extraction**: Automatically extracts book title and author from EPUB metadata
- **Table of Contents**: Parses and displays the book's table of contents with chapter IDs
- **HTML Preservation**: Maintains HTML tags in chapter content for navigation links and formatting
- **Chapter Mapping**: Creates a mapping from chapter IDs to text content for programmatic access
- **Error Handling**: Robust error handling for missing files and invalid EPUB formats

## Testing

Run the test suite:
```bash
# Create a sample EPUB for testing
python3 create_test_epub.py

# Run the test suite
python3 test_distill.py

# Test with the sample EPUB
python3 distill.py test_files/sample_book.epub
```

## Dependencies

- `ebooklib>=0.18` - For EPUB file parsing
- `beautifulsoup4>=4.11.0` - For HTML content processing

## License

See LICENSE file for details.
