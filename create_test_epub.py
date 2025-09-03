#!/usr/bin/env python3
"""
Create a sample EPUB file for testing the distill tool.
"""

import os
from ebooklib import epub


def create_sample_epub():
    """Create a simple test EPUB file."""
    
    # Create a new book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('test-book-123')
    book.set_title('Sample Test Book')
    book.set_language('en')
    book.add_author('Test Author')
    
    # Create chapters
    chapters = []
    
    # Chapter 1
    c1 = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='en')
    c1.content = '''
    <html>
    <head><title>Introduction</title></head>
    <body>
    <h1>Introduction</h1>
    <p>This is the <strong>introduction</strong> chapter of our sample book.</p>
    <p>It contains some <em>basic HTML tags</em> for testing.</p>
    <nav>
        <a href="#section1">Go to Section 1</a>
    </nav>
    </body>
    </html>
    '''
    book.add_item(c1)
    chapters.append(c1)
    
    # Chapter 2
    c2 = epub.EpubHtml(title='Main Content', file_name='main.xhtml', lang='en')
    c2.content = '''
    <html>
    <head><title>Main Content</title></head>
    <body>
    <h1 id="section1">Main Content</h1>
    <p>This is the main content chapter.</p>
    <ul>
        <li>First item</li>
        <li>Second item</li>
        <li>Third item</li>
    </ul>
    <p>Some more content with <a href="http://example.com">external link</a>.</p>
    </body>
    </html>
    '''
    book.add_item(c2)
    chapters.append(c2)
    
    # Chapter 3
    c3 = epub.EpubHtml(title='Conclusion', file_name='conclusion.xhtml', lang='en')
    c3.content = '''
    <html>
    <head><title>Conclusion</title></head>
    <body>
    <h1>Conclusion</h1>
    <p>This is the <strong>conclusion</strong> of our sample book.</p>
    <blockquote>
        <p>"A sample quote to test HTML formatting."</p>
    </blockquote>
    </body>
    </html>
    '''
    book.add_item(c3)
    chapters.append(c3)
    
    # Define table of contents
    book.toc = (
        epub.Link("intro.xhtml", "Introduction", "intro"),
        epub.Link("main.xhtml", "Main Content", "main"),
        epub.Link("conclusion.xhtml", "Conclusion", "conclusion")
    )
    
    # Add default NCX and Nav files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define CSS style
    style = '''
    body { font-family: Times, serif; }
    h1 { color: #333; }
    p { text-align: justify; }
    '''
    nav_css = epub.EpubItem(uid="nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Create spine
    book.spine = ['nav'] + chapters
    
    # Write EPUB file
    output_path = 'test_files/sample_book.epub'
    epub.write_epub(output_path, book, {})
    
    print(f"Sample EPUB created: {output_path}")
    return output_path


if __name__ == "__main__":
    create_sample_epub()