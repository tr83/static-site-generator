import unittest

from textnode import TextNode, TextType


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
        node = TextNode("This is text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_missing_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC, 'https://www.url.com')
        self.assertIsNone(node.url)
        self.assertIsNotNone(node2.url)


if __name__ == "__main__":
    unittest.main()