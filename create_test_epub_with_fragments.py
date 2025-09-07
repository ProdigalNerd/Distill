#!/usr/bin/env python3
"""
Create a sample EPUB file with fragments for testing the distill tool's
ability to handle chapter sections that point to different parts of the same file.
"""

import os
from ebooklib import epub


def create_sample_epub_with_fragments():
    """Create a test EPUB file with fragments that simulate real EPUB structure."""
    
    # Create a new book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('test-book-fragments-123')
    book.set_title('Sample Book with Fragments')
    book.set_language('en')
    book.add_author('Test Author')
    
    # Create a single large chapter file with multiple sections
    large_chapter = epub.EpubHtml(title='Large Chapter', file_name='large_chapter.xhtml', lang='en')
    large_chapter.content = '''
    <html>
    <head><title>Large Chapter</title></head>
    <body>
    <h1 id="intro">Introduction Section</h1>
    <p>This is the introduction section of the large chapter. It discusses the fundamentals of machine learning and artificial intelligence. Machine learning is a subset of AI that focuses on algorithms that can learn from data without being explicitly programmed.</p>
    <p>The field has evolved significantly over the past decades, with breakthroughs in neural networks, deep learning, and natural language processing transforming how we approach complex problems.</p>
    
    <h1 id="methods">Methods and Approaches</h1>
    <p>This section covers various machine learning methods and approaches. Supervised learning involves training algorithms on labeled data to make predictions on new, unseen data. Common supervised learning algorithms include linear regression, decision trees, and support vector machines.</p>
    <p>Unsupervised learning, on the other hand, works with unlabeled data to discover hidden patterns or structures. Clustering algorithms like K-means and hierarchical clustering are popular unsupervised learning techniques.</p>
    
    <h1 id="applications">Real-world Applications</h1>
    <p>Machine learning has found applications in numerous fields including healthcare, finance, transportation, and entertainment. In healthcare, ML algorithms can assist in medical diagnosis, drug discovery, and personalized treatment plans.</p>
    <p>In finance, machine learning powers fraud detection systems, algorithmic trading, risk assessment, and credit scoring. The technology has revolutionized how financial institutions operate and make decisions.</p>
    
    <h1 id="future">Future Directions</h1>
    <p>The future of machine learning holds exciting possibilities including explainable AI, quantum machine learning, and more efficient algorithms. As computational power continues to grow, we can expect more sophisticated models and applications.</p>
    <p>Ethical considerations and responsible AI development are becoming increasingly important as these technologies become more prevalent in society. Ensuring fairness, transparency, and accountability in AI systems is crucial for their successful adoption.</p>
    </body>
    </html>
    '''
    book.add_item(large_chapter)
    
    # Create a simple conclusion chapter
    conclusion = epub.EpubHtml(title='Conclusion', file_name='conclusion.xhtml', lang='en')
    conclusion.content = '''
    <html>
    <head><title>Conclusion</title></head>
    <body>
    <h1>Final Thoughts</h1>
    <p>This concludes our exploration of machine learning concepts and applications. The field continues to evolve rapidly, offering new opportunities and challenges for researchers and practitioners alike.</p>
    </body>
    </html>
    '''
    book.add_item(conclusion)
    
    # Define table of contents with fragments pointing to different sections of the same file
    book.toc = (
        epub.Link("large_chapter.xhtml#intro", "Introduction", "chapter1"),
        epub.Link("large_chapter.xhtml#methods", "Methods and Approaches", "chapter2"),
        epub.Link("large_chapter.xhtml#applications", "Applications", "chapter3"),
        epub.Link("large_chapter.xhtml#future", "Future Directions", "chapter4"),
        epub.Link("conclusion.xhtml", "Conclusion", "chapter5")
    )
    
    # Add default NCX and Nav files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define CSS style
    style = '''
    body { font-family: Times, serif; }
    h1 { color: #333; margin-top: 2em; }
    p { text-align: justify; margin: 1em 0; }
    '''
    nav_css = epub.EpubItem(uid="nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Create spine
    book.spine = ['nav', large_chapter, conclusion]
    
    # Write EPUB file
    output_path = 'test_files/sample_book_fragments.epub'
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    epub.write_epub(output_path, book, {})
    
    # Verify the file was actually created
    if os.path.exists(output_path):
        print(f"Sample EPUB with fragments created: {output_path}")
    else:
        print(f"Error: Failed to create EPUB file at {output_path}")
        return None
    
    return output_path


if __name__ == "__main__":
    create_sample_epub_with_fragments()