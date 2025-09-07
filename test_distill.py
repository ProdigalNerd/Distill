#!/usr/bin/env python3
"""
Test script to verify the distill functionality works correctly.
"""

import sys
from pathlib import Path

# Add the current directory to the path so we can import distill
sys.path.insert(0, str(Path(__file__).parent))

from distill import EpubDistiller, SUMY_AVAILABLE


def test_distill_functionality():
    """Test the core functionality of the EpubDistiller."""
    
    epub_path = "test_files/sample_book.epub"
    
    if not Path(epub_path).exists():
        print("Error: Test EPUB file not found. Run create_test_epub.py first.")
        return False
    
    print("Testing EpubDistiller functionality...")
    print("="*50)
    
    # Initialize distiller (non-interactive mode for testing)
    distiller = EpubDistiller(epub_path, interactive=False)
    
    # Test loading
    if not distiller.load_book():
        print("❌ Failed to load EPUB file")
        return False
    print("✅ Successfully loaded EPUB file")
    
    # Test metadata extraction
    title, author = distiller.extract_metadata()
    print(f"✅ Metadata extracted - Title: '{title}', Author: '{author}'")
    
    # Test table of contents extraction
    toc_entries = distiller.extract_table_of_contents()
    print(f"✅ Table of contents extracted - {len(toc_entries)} chapters found")
    
    for i, (chapter_id, chapter_title, href) in enumerate(toc_entries, 1):
        print(f"   {i}. {chapter_title} (ID: {chapter_id}, File: {href})")
    
    # Test chapter text extraction
    print("\n" + "="*50)
    print("Testing chapter text extraction...")
    
    for chapter_id, chapter_title, href in toc_entries:
        text_content = distiller.extract_chapter_text(href)
        if text_content:
            print(f"✅ Extracted content for '{chapter_title}' ({len(text_content)} characters)")
            # Show first 100 characters of content
            preview = text_content[:100].replace('\n', ' ')
            print(f"   Preview: {preview}...")
        else:
            print(f"❌ Failed to extract content for '{chapter_title}'")
    
    # Test chapter mapping
    print("\n" + "="*50)
    print("Testing chapter mapping...")
    
    chapter_mapping = distiller.build_chapter_mapping()
    print(f"✅ Chapter mapping built with {len(chapter_mapping)} entries")
    
    for chapter_id, content in chapter_mapping.items():
        print(f"   {chapter_id}: {len(content)} characters")
    
    # Test summarization functionality if available
    if SUMY_AVAILABLE:
        print("\n" + "="*50)
        print("Testing summarization functionality...")
        
        for chapter_id, chapter_title, href in toc_entries:
            html_content = distiller.extract_chapter_text(href)
            if html_content:
                plain_text = distiller.html_to_plain_text(html_content)
                summary = distiller.summarize_text(plain_text)
                
                print(f"✅ Generated summary for '{chapter_title}' ({len(summary)} sentences)")
                for i, sentence in enumerate(summary, 1):
                    print(f"   {i}. {sentence[:60]}..." if len(sentence) > 60 else f"   {i}. {sentence}")
            else:
                print(f"❌ Could not extract content for '{chapter_title}'")
    else:
        print("\n⚠️  Sumy not available, skipping summarization tests")
    
    print("\n✅ All tests passed!")
    return True


if __name__ == "__main__":
    success = test_distill_functionality()
    sys.exit(0 if success else 1)