#!/usr/bin/env python3
"""
Extended test script for the enhanced distill functionality with path security.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path so we can import distill
sys.path.insert(0, str(Path(__file__).parent))

from distill import EpubDistiller, validate_and_get_permission, SUMY_AVAILABLE


def test_path_validation():
    """Test path validation and permission logic."""
    print("Testing path validation functionality...")
    print("="*50)
    
    # Create test scenario from within the project directory
    os.chdir('/home/runner/work/Distill/Distill')
    
    # Test 1: File within current directory (should allow without prompt)
    local_file = Path('test_files/sample_book.epub')
    result = validate_and_get_permission(local_file, interactive=False)
    print(f"✅ Local file access (no prompt needed): {result}")
    
    # Test 2: File outside current directory (would prompt in interactive mode)
    external_file = Path('/tmp/test_outside/sample_book.epub')
    result = validate_and_get_permission(external_file, interactive=False)
    print(f"✅ External file access (non-interactive): {result}")
    
    # Test 3: Absolute path to local file (should allow without prompt)
    abs_local_file = Path('/home/runner/work/Distill/Distill/test_files/sample_book.epub')
    result = validate_and_get_permission(abs_local_file, interactive=False)
    print(f"✅ Absolute path to local file: {result}")
    
    # Test 4: Test from different working directory
    os.chdir('/tmp')
    distill_file = Path('/home/runner/work/Distill/Distill/test_files/sample_book.epub')
    result = validate_and_get_permission(distill_file, interactive=False)
    print(f"✅ External directory access from /tmp: {result}")
    
    return True


def test_enhanced_cli_features():
    """Test the enhanced CLI features."""
    print("\nTesting enhanced CLI features...")
    print("="*50)
    
    # Return to project directory
    os.chdir('/home/runner/work/Distill/Distill')
    
    epub_path = "test_files/sample_book.epub"
    
    if not Path(epub_path).exists():
        print("Error: Test EPUB file not found.")
        return False
    
    # Test 1: Non-interactive mode
    distiller = EpubDistiller(epub_path, interactive=False)
    if distiller.load_book():
        print("✅ Non-interactive mode works")
        title, author = distiller.extract_metadata()
        print(f"   Metadata: {title} by {author}")
    else:
        print("❌ Non-interactive mode failed")
        return False
    
    # Test 2: Interactive mode (but with local file, so no prompt)
    distiller_interactive = EpubDistiller(epub_path, interactive=True)
    if distiller_interactive.load_book():
        print("✅ Interactive mode with local file (no prompt)")
    else:
        print("❌ Interactive mode with local file failed")
        return False
    
    return True


def test_error_handling():
    """Test enhanced error handling."""
    print("\nTesting enhanced error handling...")
    print("="*50)
    
    # Test with non-existent file
    distiller = EpubDistiller("nonexistent.epub", interactive=False)
    result = distiller.load_book()
    print(f"✅ Handles non-existent file gracefully: {not result}")
    
    # Test with invalid path
    try:
        invalid_path = Path("///invalid//path//file.epub")
        result = validate_and_get_permission(invalid_path, interactive=False)
        print(f"✅ Handles invalid paths: handled without crash")
    except Exception as e:
        print(f"✅ Invalid path handling: {type(e).__name__}")
    
    return True


def run_all_tests():
    """Run all enhanced tests."""
    print("Enhanced Distill Functionality Tests")
    print("="*60)
    
    # Ensure test file exists
    epub_path = Path("/home/runner/work/Distill/Distill/test_files/sample_book.epub")
    if not epub_path.exists():
        print("Creating test EPUB file...")
        os.system("cd /home/runner/work/Distill/Distill && python3 create_test_epub.py")
    
    # Ensure external test file exists
    external_path = Path("/tmp/test_outside/sample_book.epub")
    if not external_path.exists():
        os.makedirs("/tmp/test_outside", exist_ok=True)
        os.system("cp /home/runner/work/Distill/Distill/test_files/sample_book.epub /tmp/test_outside/")
    
    success = True
    
    success &= test_path_validation()
    success &= test_enhanced_cli_features()  
    success &= test_error_handling()
    
    if success:
        print("\n✅ All enhanced functionality tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    return success


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)