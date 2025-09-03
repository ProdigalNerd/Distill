#!/usr/bin/env python3
"""
Distill - E-book content extractor and summarizer
CLI tool to extract metadata, table of contents, and chapter text from EPUB files.
Now includes chapter summarization using Sumy library.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# Sumy imports for summarization
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer


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
    
    def extract_plain_text(self, href: str) -> str:
        """
        Extract plain text from chapter (for summarization).
        """
        html_content = self.extract_chapter_text(href)
        if not html_content:
            return ""
        
        # Parse HTML and extract plain text
        soup = BeautifulSoup(html_content, 'html.parser')
        plain_text = soup.get_text()
        
        # Clean up the text - remove extra whitespace
        lines = [line.strip() for line in plain_text.split('\n') if line.strip()]
        return ' '.join(lines)
    
    def summarize_text(self, text: str, algorithm: str = 'lexrank', sentence_count: int = 5) -> List[str]:
        """
        Summarize text using specified algorithm.
        
        Args:
            text: The text to summarize
            algorithm: Summarization algorithm ('lexrank', 'lsa', 'textrank')
            sentence_count: Number of sentences in summary
            
        Returns:
            List of summary sentences
        """
        if not text.strip():
            return []
        
        try:
            # Parse text with Sumy
            parser = PlaintextParser.from_string(text, Tokenizer('english'))
            
            # Choose summarizer based on algorithm
            if algorithm.lower() == 'lsa':
                summarizer = LsaSummarizer()
            elif algorithm.lower() == 'textrank':
                summarizer = TextRankSummarizer()
            else:  # Default to lexrank
                summarizer = LexRankSummarizer()
            
            # Generate summary
            summary = summarizer(parser.document, sentence_count)
            
            # Convert to list of strings
            return [str(sentence) for sentence in summary]
            
        except Exception as e:
            print(f"Error summarizing text: {e}", file=sys.stderr)
            return []
    
    def summarize_chapter(self, chapter_id: str, href: str, algorithm: str = 'lexrank', sentence_count: int = 5) -> List[str]:
        """
        Summarize a single chapter.
        
        Args:
            chapter_id: Chapter identifier
            href: Chapter file reference
            algorithm: Summarization algorithm
            sentence_count: Number of sentences in summary
            
        Returns:
            List of summary sentences
        """
        plain_text = self.extract_plain_text(href)
        return self.summarize_text(plain_text, algorithm, sentence_count)
    
    def build_chapter_mapping(self) -> Dict[str, str]:
        """
        Build mapping: chapter_id → text content.
        """
        toc_entries = self.extract_table_of_contents()
        
        for chapter_id, title, href in toc_entries:
            text_content = self.extract_chapter_text(href)
            self.chapter_mapping[chapter_id] = text_content
        
        return self.chapter_mapping
    
    def print_chapter_info(self, include_summaries: bool = False, algorithm: str = 'lexrank', sentence_count: int = 5):
        """Print chapter numbers and names, optionally with summaries."""
        toc_entries = self.extract_table_of_contents()
        
        print("\n" + "="*60)
        print("TABLE OF CONTENTS")
        print("="*60)
        
        for i, (chapter_id, title, href) in enumerate(toc_entries, 1):
            print(f"{i:3d}. {title}")
            print(f"     ID: {chapter_id}")
            print(f"     File: {href}")
            
            if include_summaries:
                print(f"     Summary ({algorithm.upper()}, {sentence_count} sentences):")
                summary = self.summarize_chapter(chapter_id, href, algorithm, sentence_count)
                if summary:
                    for j, sentence in enumerate(summary, 1):
                        print(f"       {j}. {sentence}")
                else:
                    print("       (No summary available)")
            
            print()
    
    def distill(self, include_summaries: bool = False, algorithm: str = 'lexrank', sentence_count: int = 5):
        """Main extraction process with optional summarization."""
        if not self.load_book():
            return False
        
        # Extract metadata
        title, author = self.extract_metadata()
        print(f"Title: {title}")
        print(f"Author: {author}")
        
        # Build chapter mapping
        self.build_chapter_mapping()
        
        # Print chapter information (with optional summaries)
        self.print_chapter_info(include_summaries, algorithm, sentence_count)
        
        print(f"\nTotal chapters extracted: {len(self.chapter_mapping)}")
        
        return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract content from EPUB files with optional chapter summarization",
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
        "--summarize", "-s",
        action="store_true",
        help="Include chapter summaries in output"
    )
    parser.add_argument(
        "--algorithm", "-a",
        choices=['lexrank', 'lsa', 'textrank'],
        default='lexrank',
        help="Summarization algorithm to use (default: lexrank)"
    )
    parser.add_argument(
        "--sentences", "-n",
        type=int,
        default=5,
        metavar="N",
        help="Number of sentences per chapter summary (default: 5)"
    )
    
    args = parser.parse_args()
    
    # Validate sentence count
    if args.sentences < 1:
        print("Error: Number of sentences must be at least 1.", file=sys.stderr)
        return 1
    
    if args.sentences > 20:
        print("Warning: Large number of sentences may not provide effective summarization.", file=sys.stderr)
    
    # Check if file exists
    epub_path = Path(args.epub_file)
    if not epub_path.exists():
        print(f"Error: File '{epub_path}' does not exist.", file=sys.stderr)
        return 1
    
    if not epub_path.suffix.lower() in ['.epub']:
        print(f"Error: File '{epub_path}' is not an EPUB file.", file=sys.stderr)
        return 1
    
    # Process the EPUB file
    distiller = EpubDistiller(str(epub_path))
    
    try:
        success = distiller.distill(
            include_summaries=args.summarize,
            algorithm=args.algorithm,
            sentence_count=args.sentences
        )
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())