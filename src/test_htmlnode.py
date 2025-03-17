import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_eq(self):
        node = HTMLNode(props={"href": "https://www.google.com","target": "_blank",})
        text = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), text)

    def test_props_not_eq(self):
        node = HTMLNode(props={"href": "https://www.google.com","target": "_blank",})
        text = "href=\"https://www.brondby.com\" target=\"_blank\""
        self.assertNotEqual(node, text)

    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.__repr__(), "HTMLNode(p, This is a paragraph, None, None)")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

if __name__ == "__main__":
    unittest.main()