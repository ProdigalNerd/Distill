#!/usr/bin/env python3
"""
Distill - E-book content extractor
CLI tool to extract metadata, table of contents, and chapter text from EPUB files.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# Summarization imports (optional, only used when --summary flag is provided)
try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
    import nltk
    SUMY_AVAILABLE = True
except ImportError:
    SUMY_AVAILABLE = False


class EpubDistiller:
    """Extract and organize content from EPUB files."""
    
    def __init__(self, epub_path: str):
        """Initialize with path to EPUB file."""
        self.epub_path = Path(epub_path)
        self.book = None
        self.chapter_mapping: Dict[str, str] = {}
        
    def load_book(self) -> bool:
        """Load the EPUB file."""
        try:
            self.book = epub.read_epub(str(self.epub_path))
            return True
        except Exception as e:
            print(f"Error loading EPUB file: {e}", file=sys.stderr)
            return False
    
    def extract_metadata(self) -> Tuple[str, str]:
        """Extract book metadata (title, author)."""
        if not self.book:
            return "", ""
        
        # Get title
        title = self.book.get_metadata('DC', 'title')
        title_str = title[0][0] if title else "Unknown Title"
        
        # Get author
        author = self.book.get_metadata('DC', 'creator')
        author_str = author[0][0] if author else "Unknown Author"
        
        return title_str, author_str
    
    def extract_table_of_contents(self) -> List[Tuple[str, str, str]]:
        """
        Extract table of contents (chapters).
        Returns list of tuples: (chapter_id, chapter_title, href)
        """
        toc_entries = []
        
        if not self.book:
            return toc_entries
        
        # Get table of contents
        toc = self.book.toc
        
        def process_toc_item(item, level=0):
            """Recursively process TOC items."""
            if isinstance(item, tuple):
                # item is (Section, [children])
                section, children = item
                if hasattr(section, 'title') and hasattr(section, 'href'):
                    chapter_id = f"chapter_{len(toc_entries) + 1:03d}"
                    toc_entries.append((chapter_id, section.title, section.href))
                
                # Process children
                for child in children:
                    process_toc_item(child, level + 1)
            elif hasattr(item, 'title') and hasattr(item, 'href'):
                # item is a Section object
                chapter_id = f"chapter_{len(toc_entries) + 1:03d}"
                toc_entries.append((chapter_id, item.title, item.href))
        
        # Process all TOC items
        for item in toc:
            process_toc_item(item)
        
        return toc_entries
    
    def extract_chapter_text(self, href: str) -> str:
        """
        Extract chapter text while keeping HTML tags for navigation.
        """
        if not self.book:
            return ""
        
        # Find the item by href
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Check if this item matches the href
                if item.get_name() == href or item.get_name().endswith(href):
                    content = item.get_content().decode('utf-8')
                    
                    # Parse with BeautifulSoup to clean up and preserve structure
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Remove unnecessary elements but keep structure
                    for element in soup.find_all(['script', 'style']):
                        element.decompose()
                    
                    # Return the cleaned HTML content
                    return str(soup)
        
        return ""
    
    def html_to_plain_text(self, html_content: str) -> str:
        """
        Convert HTML content to plain text for summarization.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for element in soup.find_all(['script', 'style', 'meta', 'link']):
            element.decompose()
        
        # Get text with spaces between elements
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def summarize_text(self, text: str, sentences_count: int = 2) -> List[str]:
        """
        Summarize text using Sumy library.
        Returns a list of summary sentences.
        """
        if not SUMY_AVAILABLE:
            return ["Summarization not available. Install required dependencies: pip install sumy nltk numpy"]
        
        if not text or len(text.strip()) < 100:
            return ["Chapter too short for meaningful summarization."]
        
        try:
            # Initialize NLTK data if not already done
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
                nltk.download('punkt_tab', quiet=True)
            
            # Parse the text
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            
            # Use LSA summarizer (works well for most content)
            summarizer = LsaSummarizer()
            
            # Get summary
            summary = summarizer(parser.document, sentences_count)
            
            # Convert to list of strings
            return [str(sentence) for sentence in summary]
            
        except Exception as e:
            return [f"Summarization error: {str(e)}"]
    
    def build_chapter_mapping(self) -> Dict[str, str]:
        """
        Build mapping: chapter_id → text content.
        """
        toc_entries = self.extract_table_of_contents()
        
        for chapter_id, title, href in toc_entries:
            text_content = self.extract_chapter_text(href)
            self.chapter_mapping[chapter_id] = text_content
        
        return self.chapter_mapping
    
    def print_chapter_info(self, include_summary: bool = False):
        """Print chapter numbers and names, optionally with summaries."""
        toc_entries = self.extract_table_of_contents()
        
        print("\n" + "="*60)
        print("TABLE OF CONTENTS")
        print("="*60)
        
        for i, (chapter_id, title, href) in enumerate(toc_entries, 1):
            print(f"{i:3d}. {title}")
            print(f"     ID: {chapter_id}")
            print(f"     File: {href}")
            
            if include_summary:
                # Extract and summarize chapter content
                html_content = self.extract_chapter_text(href)
                if html_content:
                    plain_text = self.html_to_plain_text(html_content)
                    summary_sentences = self.summarize_text(plain_text)
                    
                    print(f"     Summary:")
                    for sentence in summary_sentences:
                        print(f"       • {sentence}")
                else:
                    print(f"     Summary: [Could not extract content]")
            
            print()
    
    def distill(self, include_summary: bool = False):
        """Main extraction process."""
        if not self.load_book():
            return False
        
        # Extract metadata
        title, author = self.extract_metadata()
        print(f"Title: {title}")
        print(f"Author: {author}")
        
        # Build chapter mapping
        self.build_chapter_mapping()
        
        # Print chapter information
        self.print_chapter_info(include_summary)
        
        print(f"\nTotal chapters extracted: {len(self.chapter_mapping)}")
        
        return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract content from EPUB files",
        prog="distill"
    )
    parser.add_argument(
        "epub_file",
        help="Path to the EPUB file to process"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Include chapter summaries in the output"
    )
    
    args = parser.parse_args()
    
    # Check if file exists
    epub_path = Path(args.epub_file)
    if not epub_path.exists():
        print(f"Error: File '{epub_path}' does not exist.", file=sys.stderr)
        return 1
    
    if not epub_path.suffix.lower() in ['.epub']:
        print(f"Error: File '{epub_path}' is not an EPUB file.", file=sys.stderr)
        return 1
    
    # Check if summarization is requested but dependencies are missing
    if args.summary and not SUMY_AVAILABLE:
        print("Error: Summarization requested but required dependencies are not installed.", file=sys.stderr)
        print("Please install with: pip install sumy nltk numpy", file=sys.stderr)
        return 1
    
    # Process the EPUB file
    distiller = EpubDistiller(str(epub_path))
    
    try:
        success = distiller.distill(include_summary=args.summary)
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())