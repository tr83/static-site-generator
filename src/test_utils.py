import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class UtilsTest(unittest.TestCase):
    def test_split_nodes_delimiter_with_invalid_delimiter(self):
        nodes = [
            TextNode("test value", TextType.TEXT)
        ]
        self.assertRaises(Exception, split_nodes_delimiter, (nodes, "", TextType.TEXT) )

    def test_split_nodes_delimiter_without_delimiter(self):
        nodes = [
            TextNode("Testing text without delimiter", TextType.TEXT)
        ]
        self.assertRaises(Exception, split_nodes_delimiter, (nodes, "**", TextType.BOLD))
        
    def test_split_nodes_delimiter_with_text_node_italic(self):
        nodes = [
            TextNode("Text with *italic* text", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "*", TextType.ITALIC), 
            [
                TextNode("Text with ", TextType.TEXT), 
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT)
            ]
        )

    def test_split_nodes_delimiter_with_text_node_bold(self):
        nodes = [
            TextNode("Text with **bold** text", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "**", TextType.BOLD), 
            [
                TextNode("Text with ", TextType.TEXT), 
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
        )

    def test_split_nodes_delimiter_whole_text(self):
        nodes = [
            TextNode("`Code block as a whole given text`", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE), 
            [
                TextNode("Code block as a whole given text", TextType.CODE)
            ]
        )
