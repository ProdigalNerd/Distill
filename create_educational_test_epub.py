#!/usr/bin/env python3
"""
Create a sample EPUB with educational content for testing improved summarization.
"""

import os
import zipfile
from pathlib import Path
from ebooklib import epub

def create_educational_epub():
    """Create an EPUB with educational content."""
    
    # Create book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('sample-educational-book-123')
    book.set_title('Advanced Python Programming Concepts')
    book.set_language('en')
    book.add_author('Dr. Jane Smith')
    
    # Create chapters with educational content
    
    # Chapter 1: Object-Oriented Programming
    chapter1 = epub.EpubHtml(
        title='Object-Oriented Programming Fundamentals',
        file_name='chapter1.xhtml',
        lang='en'
    )
    chapter1.content = '''
    <?xml version='1.0' encoding='utf-8'?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>Object-Oriented Programming Fundamentals</title>
    </head>
    <body>
        <h1>Object-Oriented Programming Fundamentals</h1>
        
        <h2>Introduction to OOP</h2>
        <p>Object-Oriented Programming (OOP) is a programming paradigm that organizes code into objects, which are instances of classes. This approach helps create more modular, reusable, and maintainable code.</p>
        
        <h2>Core Principles</h2>
        <p>The four fundamental principles of OOP are encapsulation, inheritance, polymorphism, and abstraction. Each principle serves a specific purpose in creating robust software architectures.</p>
        
        <h3>Encapsulation</h3>
        <p>Encapsulation is the practice of bundling data and methods that operate on that data within a single unit or class. It restricts direct access to some of the object's components, which is a means of preventing accidental interference and misuse.</p>
        
        <h3>Inheritance</h3>
        <p>Inheritance allows a class to inherit properties and methods from another class, promoting code reuse and establishing hierarchical relationships between classes. The child class can extend or override parent class functionality.</p>
        
        <h3>Polymorphism</h3>
        <p>Polymorphism enables objects of different types to be treated as instances of the same type through a common interface. This allows for flexible and dynamic code that can work with objects of various types.</p>
        
        <h3>Abstraction</h3>
        <p>Abstraction involves hiding complex implementation details while exposing only the essential features of an object. This simplifies the interface and reduces complexity for users of the class.</p>
        
        <h2>Benefits in Software Development</h2>
        <p>OOP provides numerous advantages including improved code organization, enhanced code reusability, easier maintenance and debugging, and better modeling of real-world entities. These benefits make OOP particularly valuable for large-scale software projects.</p>
        
        <h2>Common Design Patterns</h2>
        <p>Design patterns are reusable solutions to common problems in software design. Popular OOP patterns include Singleton, Factory, Observer, and Strategy patterns. Understanding these patterns helps developers write more efficient and maintainable code.</p>
    </body>
    </html>
    '''
    
    # Chapter 2: Data Structures and Algorithms
    chapter2 = epub.EpubHtml(
        title='Data Structures and Algorithms',
        file_name='chapter2.xhtml',
        lang='en'
    )
    chapter2.content = '''
    <?xml version='1.0' encoding='utf-8'?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>Data Structures and Algorithms</title>
    </head>
    <body>
        <h1>Data Structures and Algorithms</h1>
        
        <h2>Understanding Data Structures</h2>
        <p>Data structures are specialized formats for organizing, processing, retrieving, and storing data. The choice of data structure depends on the specific requirements of the application and the operations that need to be performed efficiently.</p>
        
        <h2>Linear Data Structures</h2>
        <p>Linear data structures store elements in a sequential manner. Arrays provide constant-time access to elements by index but have fixed size. Linked lists offer dynamic sizing with efficient insertion and deletion, but require sequential access to reach specific elements.</p>
        
        <h3>Stacks and Queues</h3>
        <p>Stacks follow the Last-In-First-Out (LIFO) principle and are essential for function calls, expression evaluation, and backtracking algorithms. Queues implement First-In-First-Out (FIFO) behavior and are crucial for breadth-first search, scheduling, and buffering operations.</p>
        
        <h2>Non-Linear Data Structures</h2>
        <p>Trees are hierarchical structures with a root node and child nodes, forming a branching structure. Binary search trees enable efficient searching, insertion, and deletion operations with O(log n) average time complexity.</p>
        
        <h3>Hash Tables</h3>
        <p>Hash tables provide near constant-time average case performance for insertions, deletions, and lookups by using hash functions to map keys to array indices. However, they may suffer from hash collisions which require resolution strategies.</p>
        
        <h2>Algorithm Analysis</h2>
        <p>Algorithm efficiency is measured using Big O notation, which describes how the runtime or space requirements of an algorithm scale with input size. Common complexities include O(1) constant time, O(log n) logarithmic, O(n) linear, and O(n²) quadratic time.</p>
        
        <h2>Sorting and Searching</h2>
        <p>Fundamental algorithms include sorting techniques like quicksort and mergesort, which have O(n log n) average complexity. Binary search provides O(log n) searching in sorted arrays. Understanding these algorithms is essential for optimizing program performance.</p>
        
        <h2>Graph Algorithms</h2>
        <p>Graph algorithms solve problems involving networks of connected nodes. Depth-first search explores as far as possible along each branch before backtracking. Breadth-first search explores neighbor nodes first before moving to the next level. Dijkstra's algorithm finds shortest paths in weighted graphs.</p>
    </body>
    </html>
    '''
    
    # Chapter 3: Concurrency and Parallel Programming
    chapter3 = epub.EpubHtml(
        title='Concurrency and Parallel Programming',
        file_name='chapter3.xhtml',
        lang='en'
    )
    chapter3.content = '''
    <?xml version='1.0' encoding='utf-8'?>
    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>Concurrency and Parallel Programming</title>
    </head>
    <body>
        <h1>Concurrency and Parallel Programming</h1>
        
        <h2>Concurrency vs Parallelism</h2>
        <p>Concurrency involves dealing with multiple tasks at once, while parallelism involves executing multiple tasks simultaneously. Concurrent programming manages the complexity of multiple threads of execution, even if they don't run simultaneously. Parallel programming leverages multiple processors or cores to execute tasks truly simultaneously.</p>
        
        <h2>Threading Fundamentals</h2>
        <p>Threads are lightweight processes that share memory space within a program. Thread creation and management involve considerations of thread safety, synchronization, and communication between threads. The Global Interpreter Lock (GIL) in Python affects true parallelism for CPU-bound tasks.</p>
        
        <h3>Synchronization Primitives</h3>
        <p>Locks, semaphores, and condition variables are essential synchronization mechanisms. Mutex locks ensure exclusive access to shared resources, preventing race conditions. Semaphores control access to a limited number of resources. Condition variables allow threads to wait for specific conditions to be met.</p>
        
        <h2>Multiprocessing</h2>
        <p>Multiprocessing creates separate processes with independent memory spaces, avoiding the GIL limitation. Inter-process communication occurs through pipes, queues, or shared memory. Process pools enable efficient distribution of work across multiple CPU cores for CPU-intensive tasks.</p>
        
        <h2>Asynchronous Programming</h2>
        <p>Asynchronous programming uses event loops and coroutines to handle I/O-bound tasks efficiently. The async/await syntax provides a clean way to write asynchronous code that appears synchronous. This approach is particularly effective for network operations and file I/O where waiting time can be utilized for other tasks.</p>
        
        <h2>Common Concurrency Patterns</h2>
        <p>Producer-consumer patterns coordinate threads that generate and process data. Thread pools manage a fixed number of worker threads for task execution. Message passing architectures promote loose coupling between concurrent components. Understanding these patterns helps design robust concurrent systems.</p>
        
        <h2>Performance Considerations</h2>
        <p>Concurrent programming introduces overhead from context switching and synchronization. Profiling tools help identify bottlenecks and contention points. Load balancing strategies ensure work is distributed evenly across available resources. Proper design prevents deadlocks and minimizes contention for shared resources.</p>
    </body>
    </html>
    '''
    
    # Add chapters to book
    book.add_item(chapter1)
    book.add_item(chapter2)
    book.add_item(chapter3)
    
    # Define table of contents
    book.toc = (
        epub.Link("chapter1.xhtml", "Object-Oriented Programming Fundamentals", "chap1"),
        epub.Link("chapter2.xhtml", "Data Structures and Algorithms", "chap2"),
        epub.Link("chapter3.xhtml", "Concurrency and Parallel Programming", "chap3"),
    )
    
    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define spine
    book.spine = ['nav', chapter1, chapter2, chapter3]
    
    # Create output directory
    output_dir = Path("test_files")
    output_dir.mkdir(exist_ok=True)
    
    # Write EPUB file
    output_path = output_dir / "educational_book.epub"
    epub.write_epub(str(output_path), book, {})
    
    print(f"Educational EPUB created: {output_path}")
    return str(output_path)

if __name__ == "__main__":
    create_educational_epub()