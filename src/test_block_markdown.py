import unittest

from block_markdown import markdown_to_blocks, block_to_block_type


class TestBlockMarkdown(unittest.TestCase):
    def test_block_markdown_base_case(self):
        text = '''
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item'''
        self.assertEqual(markdown_to_blocks(text), [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '''* This is the first list item in a list block\n* This is a list item\n* This is another list item'''
        ])

    def test_block_markdown_remove_extra_empty_lines(self):
        text = '''
# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.


* This is the first list item in a list block
* This is a list item
* This is another list item'''
        self.assertEqual(markdown_to_blocks(text), [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '''* This is the first list item in a list block\n* This is a list item\n* This is another list item'''
        ])

    def test_block_markdown_strip_extra_whitespace(self):
        text = '''
    # This is a heading



 This is a paragraph of text. It has some **bold** and *italic* words inside of it.


 * This is the first list item in a list block    
    * This is a list item                            
* This is another list item '''
        self.assertEqual(markdown_to_blocks(text), [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '''* This is the first list item in a list block\n* This is a list item\n* This is another list item'''
        ])

    def test_block_to_block_type_heading(self):
        text = '# This is a heading'
        self.assertEqual(block_to_block_type(text), 'heading')
        text = '## This is a heading'
        self.assertEqual(block_to_block_type(text), 'heading')
        text = '### This is a heading'
        self.assertEqual(block_to_block_type(text), 'heading')
        text = '#### This is a heading'
        self.assertEqual(block_to_block_type(text), 'heading')
        text = '##### This is a heading'
        self.assertEqual(block_to_block_type(text), 'heading')
        text = '###### This is a heading'
        self.assertEqual(block_to_block_type(text), 'heading')

    def test_block_to_block_type_invalid_heading(self):
        text = '#This will end up being a paragraph'
        self.assertEqual(block_to_block_type(text), 'paragraph')

    def test_block_to_block_type_code(self):
        text = '''```
This is a code block
```'''
        self.assertEqual(block_to_block_type(text), 'code')
        text = '''```python
print("Hello, world!")

```'''
        self.assertEqual(block_to_block_type(text), 'code')
        text = '''```python
def hello_world():
    print("Hello, world!")
````````'''
        self.assertEqual(block_to_block_type(text), 'code')

    def test_block_to_block_type_invalid_code(self):
        text = ' ```This will end up being a paragraph``` '
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = '``This will end up being a paragraph```'
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = '```This will end up being a paragraph```.'
        self.assertEqual(block_to_block_type(text), 'paragraph')

    def test_block_to_block_type_quote(self):
        text = '>This is a quote'
        self.assertEqual(block_to_block_type(text), 'quote')
        text = '> This is a quote'
        self.assertEqual(block_to_block_type(text), 'quote')
        text = '> This is a quote\n> with multiple lines'
        self.assertEqual(block_to_block_type(text), 'quote')
    
    def test_block_to_block_type_invalid_quote(self):
        text = ' >This will end up being a paragraph'
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = '> This will end up being a paragraph\nThis is not a quote'
        self.assertEqual(block_to_block_type(text), 'paragraph')

    def test_block_to_block_type_unordered_list(self):
        text = '* This is an unordered list item'
        self.assertEqual(block_to_block_type(text), 'unordered_list')
        text = '- This is an unordered list item'
        self.assertEqual(block_to_block_type(text), 'unordered_list')
        text = '* This is an unordered list item\n* Another item'
        self.assertEqual(block_to_block_type(text), 'unordered_list')
        text = '- This is an unordered list item\n- Another item'
        self.assertEqual(block_to_block_type(text), 'unordered_list')

    def test_block_to_block_type_invalid_unordered_list(self):
        text = ' *This will end up being a paragraph'
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = '*This will end up being a paragraph'
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = '* This will end up being a paragraph\nThis is not a list item'
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = '-This will end up being a paragraph'
        self.assertEqual(block_to_block_type(text), 'paragraph')

    def test_block_to_block_type_ordered_list(self):
        text = '1. This is an ordered list item'
        self.assertEqual(block_to_block_type(text), 'ordered_list')
        text = '1. This is an ordered list item\n2. Another item'
        self.assertEqual(block_to_block_type(text), 'ordered_list')
        text = '1. This is an ordered list item\n2. Another item\n3. Yet another item'
        self.assertEqual(block_to_block_type(text), 'ordered_list')

    def test_block_to_block_type_invalid_ordered_list(self):
        text = '1.This will end up being a paragraph'
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = '1. This will end up being a paragraph\n2.This is not a list item'
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = '1. This will end up being a paragraph\n3. This is not a list item'
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = '1. This will end up being a paragraph\n2 This is not a list item'
        self.assertEqual(block_to_block_type(text), 'paragraph')

    def test_block_to_block_type_paragraph(self):
        text = 'This is a paragraph of text.'
        self.assertEqual(block_to_block_type(text), 'paragraph')
        text = 'This is a paragraph\nwith multiple lines.'
        self.assertEqual(block_to_block_type(text), 'paragraph')