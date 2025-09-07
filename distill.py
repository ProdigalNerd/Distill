#!/usr/bin/env python3
"""
Distill - E-book content extractor
CLI tool to extract metadata, table of contents, and chapter text from EPUB files.
"""

import argparse
import os
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


def validate_and_get_permission(epub_path: Path, interactive: bool = True) -> bool:
    """
    Validate the EPUB path and get user permission if needed.
    
    Args:
        epub_path: Path to the EPUB file
        interactive: Whether to prompt user for permission (False for testing)
    
    Returns:
        bool: True if path is allowed, False if access should be denied
    """
    # Convert to absolute path and resolve any symlinks
    try:
        canonical_path = epub_path.resolve()
    except (OSError, RuntimeError) as e:
        print(f"Error resolving path: {e}", file=sys.stderr)
        return False
    
    # Get current working directory
    current_dir = Path.cwd().resolve()
    
    # Check if the file is outside the current working directory
    try:
        canonical_path.relative_to(current_dir)
        # File is within current directory or subdirectory
        return True
    except ValueError:
        # File is outside current directory
        if not interactive:
            return True  # Allow in non-interactive mode (for testing)
        
        print(f"\n⚠️  Security Notice:")
        print(f"You are trying to access a file outside the current directory:")
        print(f"  Current directory: {current_dir}")
        print(f"  Target file: {canonical_path}")
        print()
        
        # Check if it's on a different drive (Windows)
        if os.name == 'nt':  # Windows
            if canonical_path.anchor != current_dir.anchor:
                print(f"⚠️  The file is on a different drive ({canonical_path.anchor} vs {current_dir.anchor})")
                print()
        
        response = input("Do you want to continue? [y/N]: ").strip().lower()
        return response in ('y', 'yes')


class EpubDistiller:
    """Extract and organize content from EPUB files."""
    
    def __init__(self, epub_path: str, interactive: bool = True):
        """
        Initialize with path to EPUB file.
        
        Args:
            epub_path: Path to the EPUB file
            interactive: Whether to prompt for permissions (False for testing)
        """
        self.epub_path = Path(epub_path)
        self.interactive = interactive
        self.book = None
        self.chapter_mapping: Dict[str, str] = {}
        
    def load_book(self) -> bool:
        """Load the EPUB file after validating permissions."""
        # Validate path and get permission if needed
        if not validate_and_get_permission(self.epub_path, self.interactive):
            print("Access denied by user.", file=sys.stderr)
            return False
        
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
    
    def extract_chapter_text(self, href: str, debug: bool = False) -> str:
        """
        Extract chapter text while keeping HTML tags for navigation.
        Now handles fragment identifiers to extract specific sections.
        """
        if not self.book:
            return ""
        
        # Parse href to separate file and fragment
        if '#' in href:
            clean_href, fragment = href.split('#', 1)
        else:
            clean_href, fragment = href, None
        
        if debug:
            print(f"\n[DEBUG] Looking for href: '{href}'")
            print(f"[DEBUG] Clean href: '{clean_href}', Fragment: '{fragment}'")
            print("[DEBUG] Available EPUB items:")
            for item in self.book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    print(f"  - {item.get_name()}")
            print()
        
        # Find the item by href with improved matching
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                item_name = item.get_name()
                
                # Try multiple matching strategies:
                # 1. Exact match
                if item_name == clean_href:
                    if debug:
                        print(f"[DEBUG] Match found (exact): '{item_name}' == '{clean_href}'")
                    return self._extract_content_from_item(item, fragment, debug)
                
                # 2. Item name ends with the href (for cases like "OEBPS/Text/chapter1.xhtml" vs "chapter1.xhtml")
                if item_name.endswith(clean_href):
                    if debug:
                        print(f"[DEBUG] Match found (endswith): '{item_name}' ends with '{clean_href}'")
                    return self._extract_content_from_item(item, fragment, debug)
                
                # 3. href ends with item name (for cases where href has path prefix)
                if clean_href.endswith(item_name):
                    if debug:
                        print(f"[DEBUG] Match found (reverse endswith): '{clean_href}' ends with '{item_name}'")
                    return self._extract_content_from_item(item, fragment, debug)
                
                # 4. Base filename match (extract just the filename from both)
                import os
                href_basename = os.path.basename(clean_href)
                item_basename = os.path.basename(item_name)
                if href_basename and item_basename and href_basename == item_basename:
                    if debug:
                        print(f"[DEBUG] Match found (basename): '{href_basename}' == '{item_basename}'")
                    return self._extract_content_from_item(item, fragment, debug)
        
        if debug:
            print(f"[DEBUG] No match found for href: '{href}'")
        return ""
    
    def _extract_content_from_item(self, item, fragment: str = None, debug: bool = False) -> str:
        """
        Helper method to extract and clean content from an EPUB item.
        If fragment is provided, try to extract only that specific section.
        """
        try:
            content = item.get_content().decode('utf-8')
            
            # Parse with BeautifulSoup to clean up and preserve structure
            soup = BeautifulSoup(content, 'html.parser')
            
            # Remove unnecessary elements but keep structure
            for element in soup.find_all(['script', 'style']):
                element.decompose()
            
            # If we have a fragment identifier, try to extract specific content
            if fragment:
                if debug:
                    print(f"[DEBUG] Trying to extract fragment: '{fragment}'")
                
                # Look for element with matching id
                target_element = soup.find(id=fragment)
                if target_element:
                    if debug:
                        print(f"[DEBUG] Found element with id='{fragment}'")
                    
                    # Try to get meaningful content around the target
                    # Strategy 1: If it's a heading, get content until the next heading of same level
                    if target_element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        return self._extract_section_content(target_element, debug)
                    
                    # Strategy 2: If it's a container (div, section, etc), get its content
                    elif target_element.name in ['div', 'section', 'article', 'main']:
                        return str(target_element)
                    
                    # Strategy 3: Get the element and some following content
                    else:
                        return self._extract_surrounding_content(target_element, debug)
                
                else:
                    if debug:
                        print(f"[DEBUG] No element found with id='{fragment}', using full content")
            
            # Return the full cleaned HTML content if no fragment or fragment not found
            return str(soup)
        except Exception as e:
            if debug:
                print(f"[DEBUG] Error extracting content: {e}")
            return ""
    
    def _extract_section_content(self, heading_element, debug: bool = False) -> str:
        """
        Extract content from a heading until the next heading of the same or higher level.
        """
        try:
            # Determine the heading level
            heading_level = int(heading_element.name[1])  # h1 -> 1, h2 -> 2, etc.
            
            if debug:
                print(f"[DEBUG] Extracting section content from {heading_element.name} (level {heading_level})")
            
            # Collect all elements from this heading until the next heading of same/higher level
            section_elements = [heading_element]
            current = heading_element.next_sibling
            
            while current:
                # If it's a heading of same or higher level, stop
                if current.name and current.name.startswith('h'):
                    try:
                        current_level = int(current.name[1])
                        if current_level <= heading_level:
                            break
                    except (ValueError, IndexError):
                        pass
                
                # Add non-empty elements
                if current.name or (hasattr(current, 'strip') and current.strip()):
                    section_elements.append(current)
                
                current = current.next_sibling
            
            # Create a new soup with just the section content
            section_soup = BeautifulSoup('', 'html.parser')
            for element in section_elements:
                if hasattr(element, 'extract'):
                    # Clone the element to avoid modifying the original
                    element_copy = BeautifulSoup(str(element), 'html.parser')
                    section_soup.append(element_copy)
                elif hasattr(element, 'strip') and element.strip():
                    section_soup.append(element)
            
            result = str(section_soup)
            
            if debug:
                print(f"[DEBUG] Extracted section content ({len(result)} chars)")
            
            return result
            
        except Exception as e:
            if debug:
                print(f"[DEBUG] Error in section extraction: {e}")
            return str(heading_element)
    
    def _extract_surrounding_content(self, target_element, debug: bool = False) -> str:
        """
        Extract the target element and some surrounding content.
        """
        try:
            # Get the parent container if available
            parent = target_element.parent
            if parent and parent.name in ['div', 'section', 'article', 'main', 'body']:
                if debug:
                    print(f"[DEBUG] Using parent container: {parent.name}")
                return str(parent)
            else:
                if debug:
                    print(f"[DEBUG] Using target element: {target_element.name}")
                return str(target_element)
        except Exception as e:
            if debug:
                print(f"[DEBUG] Error in surrounding content extraction: {e}")
            return str(target_element)
    
    def html_to_plain_text(self, html_content: str) -> str:
        """
        Convert HTML content to plain text for summarization.
        Enhanced to better handle educational content structure.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for element in soup.find_all(['script', 'style', 'meta', 'link']):
            element.decompose()
        
        # Extract text content while preserving paragraph structure
        text_parts = []
        
        # Process body content, skipping main title
        body = soup.find('body') or soup
        skip_first_h1 = True
        
        for element in body.descendants:
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # Skip the first h1 (main title) but include section headers
                if element.name == 'h1' and skip_first_h1:
                    skip_first_h1 = False
                    continue
                text_parts.append(f"\n\n{element.get_text(strip=True)}\n")
            elif element.name == 'p':
                para_text = element.get_text(strip=True)
                if para_text:
                    text_parts.append(f"{para_text}\n\n")
            elif element.name in ['div', 'section'] and element.get_text(strip=True):
                # Only add if it's not just containing other elements
                direct_text = ''.join([str(x) for x in element.contents if isinstance(x, str)]).strip()
                if direct_text:
                    text_parts.append(f"{direct_text}\n\n")
        
        # If no structured content found, fall back to simple extraction
        if not text_parts:
            text_parts.append(soup.get_text(separator=' ', strip=True))
        
        # Join and clean up
        text = ''.join(text_parts)
        
        # Clean up extra whitespace and normalize
        import re
        text = re.sub(r'\n\s*\n+', '\n\n', text)  # Normalize paragraph breaks
        text = re.sub(r' +', ' ', text)  # Remove extra spaces
        text = text.strip()
        
        return text
    
    def _score_sentence_importance(self, sentence: str, position: int, total_sentences: int, paragraph_first: bool = False) -> float:
        """
        Score sentence importance for educational content.
        Higher scores indicate more important sentences for summarization.
        """
        score = 0.0
        sentence_lower = sentence.lower().strip()
        
        # Skip very short sentences
        if len(sentence_lower) < 20:
            return 0.0
        
        # Position-based scoring (first and second sentences are often important)
        if position == 0:
            score += 3.0  # First sentence often contains main topic
        elif position == 1:
            score += 2.0  # Second sentence often expands on topic
        elif position < 3:
            score += 1.0
        
        # Paragraph-first sentences are important
        if paragraph_first:
            score += 2.0
        
        # Educational keyword scoring - definitions and concepts
        definition_patterns = [
            r'\bis a\b', r'\bare\b.*\bthat\b', r'\brefers to\b', r'\bdefined as\b', 
            r'\bmeans\b', r'\binvolves\b', r'\benables\b', r'\ballows\b'
        ]
        
        concept_keywords = [
            'concept', 'principle', 'fundamental', 'basic', 'essential',
            'important', 'key', 'main', 'primary', 'core', 'crucial'
        ]
        
        introduction_keywords = [
            'introduction', 'overview', 'fundamentals', 'basics',
            'understanding', 'approach', 'method', 'technique'
        ]
        
        benefit_keywords = [
            'benefits', 'advantages', 'purpose', 'goal', 'objective',
            'helps', 'provides', 'offers', 'improves', 'enhances'
        ]
        
        # Score for definition patterns (high value)
        import re
        for pattern in definition_patterns:
            if re.search(pattern, sentence_lower):
                score += 3.0
                break
        
        # Score for concept keywords
        for keyword in concept_keywords:
            if keyword in sentence_lower:
                score += 2.0
                break
        
        # Score for introduction keywords
        for keyword in introduction_keywords:
            if keyword in sentence_lower:
                score += 1.5
        
        # Score for benefit keywords
        for keyword in benefit_keywords:
            if keyword in sentence_lower:
                score += 1.0
        
        # Penalize very technical implementation details
        technical_penalties = [
            'syntax', 'parameter', 'variable', 'function', 'method',
            'implementation', 'code', 'example', 'instance'
        ]
        
        penalty_count = 0
        for penalty in technical_penalties:
            if penalty in sentence_lower:
                penalty_count += 1
        
        score -= penalty_count * 0.5
        
        # Penalize sentences with too many technical terms or symbols
        if len(re.findall(r'[(){}[\]]', sentence)) > 2:
            score -= 1.0
        
        # Sentence length scoring (moderate length preferred for readability)
        words = len(sentence.split())
        if 15 <= words <= 30:
            score += 1.0
        elif 10 <= words <= 35:
            score += 0.5
        elif words < 8 or words > 45:
            score -= 1.0
        
        # Boost sentences that explain "what" something is
        if re.search(r'\bwhat\b.*\bis\b', sentence_lower) or re.search(r'\b(this|that|these|those)\b.*\b(is|are)\b', sentence_lower):
            score += 1.5
        
        # Boost sentences that explain processes or workflows
        if any(word in sentence_lower for word in ['process', 'step', 'method', 'approach', 'way', 'how']):
            score += 0.5
        
        return max(0.0, score)
    
    def _extract_educational_summary(self, text: str, sentences_count: int = 2) -> List[str]:
        """
        Extract educationally relevant sentences using custom scoring.
        """
        import re
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        scored_sentences = []
        
        for para in paragraphs:
            # Check if this paragraph starts with a heading (short line followed by longer content)
            lines = para.split('\n')
            if len(lines) >= 2 and len(lines[0]) < 50 and len(lines[1]) > 50:
                # This is a section with heading, use content after the heading
                content = '\n'.join(lines[1:])
            else:
                content = para
            
            # Split content into sentences
            sentences = re.split(r'[.!?]+', content)
            sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 15]
            
            for i, sentence in enumerate(sentences):
                # Check if this is the first sentence of a paragraph/section
                paragraph_first = (i == 0)
                
                # Score the sentence
                score = self._score_sentence_importance(
                    sentence, i, len(sentences), paragraph_first
                )
                
                if score > 0:
                    # Clean sentence and ensure it ends with period
                    clean_sentence = sentence.strip()
                    if not clean_sentence.endswith('.'):
                        clean_sentence += '.'
                    scored_sentences.append((clean_sentence, score))
        
        # Sort by score (descending) and take top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Return top sentences, maintaining some order preference
        selected = scored_sentences[:min(sentences_count * 2, len(scored_sentences))]
        
        # If we have too many, prefer those that appear earlier in text
        if len(selected) > sentences_count:
            # Sort by position in original text to maintain flow
            original_order = []
            for sentence, score in selected:
                # Find position in original text (approximately)
                pos = text.find(sentence.rstrip('.'))
                if pos >= 0:
                    original_order.append((sentence, score, pos))
                else:
                    # If not found exactly, try finding a portion
                    words = sentence.split()[:5]  # First 5 words
                    search_phrase = ' '.join(words)
                    pos = text.find(search_phrase)
                    if pos >= 0:
                        original_order.append((sentence, score, pos))
            
            original_order.sort(key=lambda x: x[2])  # Sort by position
            selected = [(s, sc) for s, sc, pos in original_order[:sentences_count]]
        
        return [sentence for sentence, score in selected]

    def summarize_text(self, text: str, sentences_count: int = 2) -> List[str]:
        """
        Summarize text using improved educational-focused approach.
        Returns a list of summary sentences prioritizing key concepts and definitions.
        """
        if not text or len(text.strip()) < 100:
            return ["Chapter too short for meaningful summarization."]
        
        # Try custom educational summarization first
        try:
            educational_summary = self._extract_educational_summary(text, sentences_count)
            if educational_summary:
                return educational_summary
        except Exception:
            pass  # Fall back to LSA if custom approach fails
        
        # Fallback to LSA summarization if available
        if not SUMY_AVAILABLE:
            return ["Summarization not available. Install required dependencies: pip install sumy nltk numpy"]
        
        try:
            # Initialize NLTK data if not already done
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
                nltk.download('punkt_tab', quiet=True)
            
            # Parse the text
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            
            # Use LSA summarizer as fallback
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
    
    def print_chapter_info(self, include_summary: bool = False, verbose: bool = False):
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
                html_content = self.extract_chapter_text(href, debug=verbose)
                if html_content:
                    plain_text = self.html_to_plain_text(html_content)
                    summary_sentences = self.summarize_text(plain_text)
                    
                    print(f"     Summary:")
                    for sentence in summary_sentences:
                        print(f"       • {sentence}")
                else:
                    print(f"     Summary: [Could not extract content]")
            
            print()
    
    def distill(self, include_summary: bool = False, verbose: bool = False):
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
        self.print_chapter_info(include_summary, verbose)
        
        print(f"\nTotal chapters extracted: {len(self.chapter_mapping)}")
        
        return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract content from EPUB files (supports both relative and absolute paths)",
        prog="distill"
    )
    parser.add_argument(
        "epub_file",
        help="Path to the EPUB file to process (relative or absolute path)"
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
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Disable permission prompts (automatically allow all paths)"
    )
    
    args = parser.parse_args()
    
    # Check if file exists
    epub_path = Path(args.epub_file)
    if not epub_path.exists():
        # Provide more detailed error message
        try:
            canonical_path = epub_path.resolve()
            print(f"Error: File '{canonical_path}' does not exist.", file=sys.stderr)
        except (OSError, RuntimeError):
            print(f"Error: File '{epub_path}' does not exist or path is invalid.", file=sys.stderr)
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
    interactive = not args.no_interactive
    distiller = EpubDistiller(str(epub_path), interactive=interactive)
    
    try:
        success = distiller.distill(include_summary=args.summary, verbose=args.verbose)
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())