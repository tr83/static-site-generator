import unittest

from block_markdown import markdown_to_blocks


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