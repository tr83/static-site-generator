import unittest

from textnode import TextNode, TextType
from utils import extract_markdown_links, split_nodes_delimiter, extract_markdown_images


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

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_images_and_ignore_links(self):
        text = "Rock'n'Roll ![Rock'n'Roll](https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg/250px-Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg) with Lemmy [lemmy kilmister](https://i.imgur.com/KKAOEnG.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("Rock'n'Roll", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg/250px-Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg")])
    
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_links_and_ignore_images(self):
        text = "Rock'n'Roll ![Rock'n'Roll](https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg/250px-Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg) with Lemmy [lemmy kilmister](https://i.imgur.com/KKAOEnG.jpeg)"
        self.assertEqual(extract_markdown_links(text), [("lemmy kilmister", "https://i.imgur.com/KKAOEnG.jpeg")])