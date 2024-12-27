import unittest

from textnode import TextNode, TextType
from utils import extract_markdown_links, split_nodes_delimiter, extract_markdown_images, split_nodes_image_or_link, text_to_textnodes


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

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image of Lemmy ![lemmy kilmister](https://i.imgur.com/KKAOEnG.jpeg) and Rock'n'Roll Hall of Fame ![rock'n'roll](https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg/250px-Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image_or_link([node], TextType.IMAGE),
            [
                TextNode("This is text with an image of Lemmy ", TextType.TEXT),
                TextNode("lemmy kilmister", TextType.IMAGE, "https://i.imgur.com/KKAOEnG.jpeg"),
                TextNode(" and Rock'n'Roll Hall of Fame ", TextType.TEXT),
                TextNode("rock'n'roll", TextType.IMAGE, "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg/250px-Rock_and_Roll_Hall_of_Fame_-_Joy_of_Museums_1.jpg")
            ]
        )

    def test_split_nodes_image_starting(self):
        node = TextNode(
            "![programmer](https://i.imgur.com/ZOxlV9f.jpeg) with ![brains](https://i.imgur.com/51zkgMs.png)...",
            TextType.TEXT
        )
        self.assertEqual(
            split_nodes_image_or_link([node], TextType.IMAGE),
            [
                TextNode("programmer", TextType.IMAGE, "https://i.imgur.com/ZOxlV9f.jpeg"),
                TextNode(" with ", TextType.TEXT),
                TextNode("brains", TextType.IMAGE, "https://i.imgur.com/51zkgMs.png"),
                TextNode("...", TextType.TEXT),
            ]
        )

    def test_split_nodes_image_without_image(self):
        node = TextNode(
            "This is text without an image",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image_or_link([node], TextType.IMAGE),
            [
                TextNode("This is text without an image", TextType.TEXT),
            ]
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image_or_link([node], TextType.LINK),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                )
            ]
        )

    def test_split_nodes_link_with_unsupported_texttype(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertRaises(
            ValueError,
            split_nodes_image_or_link,
            [node], TextType.BOLD
        )

    def test_text_to_textnodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        self.assertEqual(text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ])
        
    def test_text_to_textnodes_one_bold_node(self):
        text = '**THE WHOLE THING AS BOLD TEXT**'
        self.assertEqual(text_to_textnodes(text),
            [
                TextNode("THE WHOLE THING AS BOLD TEXT", TextType.BOLD)
            ])
        
    def test_text_to_textnodes_2(self):
        text = 'An ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) *and a* [link](https://boot.dev)!'
        self.assertEqual(text_to_textnodes(text),
            [
                TextNode("An ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" ", TextType.TEXT),
                TextNode("and a", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("!", TextType.TEXT),
            ])