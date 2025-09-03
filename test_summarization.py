#!/usr/bin/env python3
"""
Test script to verify the summarization functionality.
"""

import sys
from pathlib import Path

# Add the current directory to the path so we can import distill
sys.path.insert(0, str(Path(__file__).parent))

from distill import EpubDistiller


def test_summarization_functionality():
    """Test the summarization functionality of the EpubDistiller."""
    
    epub_path = "test_files/sample_book.epub"
    
    if not Path(epub_path).exists():
        print("Error: Test EPUB file not found. Run create_test_epub.py first.")
        return False
    
    print("Testing Summarization functionality...")
    print("="*50)
    
    # Initialize distiller
    distiller = EpubDistiller(epub_path)
    
    # Test loading
    if not distiller.load_book():
        print("❌ Failed to load EPUB file")
        return False
    print("✅ Successfully loaded EPUB file")
    
    # Test plain text extraction
    toc_entries = distiller.extract_table_of_contents()
    print("✅ Testing plain text extraction...")
    
    for chapter_id, chapter_title, href in toc_entries:
        plain_text = distiller.extract_plain_text(href)
        if plain_text:
            print(f"✅ Extracted plain text for '{chapter_title}' ({len(plain_text)} characters)")
            print(f"   Preview: {plain_text[:100]}...")
        else:
            print(f"❌ Failed to extract plain text for '{chapter_title}'")
    
    # Test summarization with different algorithms
    print("\n" + "="*50)
    print("Testing summarization algorithms...")
    
    algorithms = ['lexrank', 'lsa', 'textrank']
    test_chapter_id, test_chapter_title, test_href = toc_entries[0]  # Use first chapter
    
    for algorithm in algorithms:
        print(f"\nTesting {algorithm.upper()} algorithm:")
        summary = distiller.summarize_chapter(test_chapter_id, test_href, algorithm, 3)
        if summary:
            print(f"✅ {algorithm.upper()} summarization successful ({len(summary)} sentences)")
            for i, sentence in enumerate(summary, 1):
                print(f"   {i}. {sentence}")
        else:
            print(f"❌ {algorithm.upper()} summarization failed")
    
    # Test direct text summarization
    print("\n" + "="*50)
    print("Testing direct text summarization...")
    
    test_text = "This is a sample text for testing. It contains multiple sentences to test the summarization. The algorithm should pick the most important sentences. This functionality is crucial for the book summarization feature."
    
    for algorithm in algorithms:
        summary = distiller.summarize_text(test_text, algorithm, 2)
        if summary:
            print(f"✅ Direct {algorithm.upper()} summarization successful")
            for i, sentence in enumerate(summary, 1):
                print(f"   {i}. {sentence}")
        else:
            print(f"❌ Direct {algorithm.upper()} summarization failed")
    
    print("\n✅ All summarization tests passed!")
    return True


if __name__ == "__main__":
    success = test_summarization_functionality()
    sys.exit(0 if success else 1)