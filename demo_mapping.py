#!/usr/bin/env python3
"""
Demonstration script showing the chapter mapping functionality.
"""

import sys
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from distill import EpubDistiller


def demonstrate_chapter_mapping():
    """Demonstrate the chapter_id → text mapping functionality."""
    
    epub_path = "test_files/sample_book.epub"
    
    if not Path(epub_path).exists():
        print("Creating sample EPUB...")
        import create_test_epub
        create_test_epub.create_sample_epub()
    
    print("Demonstrating Chapter Mapping Functionality")
    print("="*60)
    
    # Initialize and load
    distiller = EpubDistiller(epub_path)
    distiller.load_book()
    
    # Get metadata
    title, author = distiller.extract_metadata()
    print(f"Book: {title} by {author}")
    print()
    
    # Build chapter mapping
    chapter_mapping = distiller.build_chapter_mapping()
    
    print("Chapter ID → Text Content Mapping:")
    print("-" * 40)
    
    for chapter_id, content in chapter_mapping.items():
        print(f"\n[{chapter_id}]")
        print(f"Content length: {len(content)} characters")
        
        # Extract readable text (remove HTML tags for preview)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text().strip()
        
        # Show first few lines
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        preview_lines = lines[:3]  # First 3 non-empty lines
        
        print("Preview:")
        for line in preview_lines:
            print(f"  {line}")
        
        if len(lines) > 3:
            print(f"  ... ({len(lines) - 3} more lines)")
    
    print(f"\nTotal chapters mapped: {len(chapter_mapping)}")


if __name__ == "__main__":
    demonstrate_chapter_mapping()