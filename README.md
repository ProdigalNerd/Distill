# Distill
Parse an e-book into chapter summarizations and key information

## Overview
Distill is a CLI tool that extracts content from EPUB files, providing:
- Book metadata (title, author)
- Table of contents (chapters)
- Chapter text with HTML tags preserved for navigation
- Chapter ID to text content mapping
- **NEW**: Chapter summarization using advanced algorithms (LexRank, LSA, TextRank)

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

### With chapter summaries
```bash
# Generate 5-sentence summaries using LexRank algorithm (default)
python3 distill.py --summarize path/to/your/book.epub

# Use different algorithm and sentence count
python3 distill.py --summarize --algorithm lsa --sentences 3 path/to/your/book.epub
```

### Available summarization algorithms
- **LexRank** (default): Graph-based extractive summarization
- **LSA**: Latent Semantic Analysis summarization
- **TextRank**: PageRank-inspired text summarization

### With verbose output
```bash
python3 distill.py --verbose path/to/your/book.epub
```

### Help
```bash
python3 distill.py --help
```

## Example Output

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

### With Summarization
```
Title: Sample Test Book
Author: Test Author

============================================================
TABLE OF CONTENTS
============================================================
  1. Introduction
     ID: chapter_001
     File: intro.xhtml
     Summary (LEXRANK, 5 sentences):
       1. Introduction This is the introduction chapter of our sample book.
       2. It contains some basic HTML tags for testing.
       3. Go to Section 1

  2. Main Content
     ID: chapter_002
     File: main.xhtml
     Summary (LEXRANK, 5 sentences):
       1. Main Content This is the main content chapter.
       2. First item Second item Third item Some more content with external link.

Total chapters extracted: 3
```

## Features

- **Metadata Extraction**: Automatically extracts book title and author from EPUB metadata
- **Table of Contents**: Parses and displays the book's table of contents with chapter IDs
- **HTML Preservation**: Maintains HTML tags in chapter content for navigation links and formatting
- **Chapter Mapping**: Creates a mapping from chapter IDs to text content for programmatic access
- **Chapter Summarization**: Generate summaries for each chapter using advanced algorithms:
  - **LexRank**: Graph-based extractive summarization using sentence similarity
  - **LSA**: Latent Semantic Analysis for topic-based summarization
  - **TextRank**: PageRank-inspired algorithm for text summarization
- **Configurable Output**: Control summarization algorithm and length (5-10 sentences per chapter recommended)
- **Error Handling**: Robust error handling for missing files and invalid EPUB formats

## Testing

Run the test suite:
```bash
# Create a sample EPUB for testing
python3 create_test_epub.py

# Run the basic test suite
python3 test_distill.py

# Run the summarization test suite
python3 test_summarization.py

# Test with the sample EPUB
python3 distill.py test_files/sample_book.epub

# Test summarization functionality
python3 distill.py --summarize --algorithm lexrank --sentences 3 test_files/sample_book.epub
```

## Dependencies

- `ebooklib>=0.18` - For EPUB file parsing
- `beautifulsoup4>=4.11.0` - For HTML content processing
- `sumy>=0.11.0` - For text summarization algorithms
- `lxml_html_clean>=0.4.0` - For HTML cleaning (required by sumy)
- `numpy>=1.24.0` - For numerical computations (required by LSA algorithm)

## License

See LICENSE file for details.
