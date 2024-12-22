import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "test value", None, { "display": "none" })
        node2 = HTMLNode("p", "test value", None, { "display": "none" })
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, { "display": "none" })
        self.assertEqual(node.props_to_html(), ' display="none"')

    def test_props_to_html_1(self):
        node = HTMLNode('a', 'Link', None, { "padding-top": "2em", "padding-bottom": "2em" })
        self.assertEqual(node.props_to_html(), ' padding-top="2em" padding-bottom="2em"')

    def test_props_to_html_2(self):
        node = HTMLNode('p', 'Normal paragraph', HTMLNode('a', 'Link', None, None), { "padding-left": "2em", "padding-right": "2em" })
        self.assertEqual(node.props_to_html(), ' padding-left="2em" padding-right="2em"')

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        leaf = LeafNode('p', 'Normal paragraph')
        leaf2 = LeafNode('p','Normal paragraph')
        self.assertEqual(leaf, leaf2)

    def test_to_html(self):
        leaf = LeafNode('p', 'Normal paragraph')
        self.assertEqual(leaf.to_html(), '<p>Normal paragraph</p>')

        leaf2 = LeafNode('a', 'A link to another dimension')
        self.assertEqual(leaf2.to_html(), '<a>A link to another dimension</a>')

        leaf3 = LeafNode(None, 'Without tag')
        self.assertEqual(leaf3.to_html(), 'Without tag')
    
    def test_repr(self):
        leaf = LeafNode('p', 'Normal paragraph')
        self.assertEqual(leaf.__repr__(), 'LeafNode(p, Normal paragraph, None)')

if __name__ == "__main__":
    unittest.main()