import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_1(self):
        node = TextNode("This is a text node", TextType.IMAGE, 'https://www.url.com')
        node2 = TextNode("This is a text node", TextType.IMAGE, 'https://www.url.com')
        self.assertEqual(node, node2)
    
    def test_eq_2(self):
        node = TextNode("This is a text node", TextType.CODE, 'https://www.url.com')
        node2 = TextNode("This is a text node", TextType.CODE, 'https://www.url.com')
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_1(self):
        node = TextNode("This is text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_missing_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC, 'https://www.url.com')
        self.assertIsNone(node.url)
        self.assertIsNotNone(node2.url)

    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'This is a text node')
        self.assertIsNone(html_node.props)

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is an alt text", TextType.IMAGE, 'https://www.url.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props_to_html(), ' src="https://www.url.com" alt="This is an alt text"')

    def test_text_node_to_html_node_missing_type(self):
        node = TextNode("This is an alt text", None, None)
        self.assertRaises(Exception, text_node_to_html_node, node)

if __name__ == "__main__":
    unittest.main()