import unittest
from textnode import TextNode, TextType
from inline import split_nodes_delimiter, split_nodes_image, split_nodes_link
class TestInline(unittest.TestCase):

    def test_one_inlines(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        cmp = [TextNode("This is a text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), cmp)

    def test_two_inlines(self):
        node = TextNode("This is a text with a `code block` word and another `code block`", TextType.TEXT)
        cmp = [TextNode("This is a text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word and another ", TextType.TEXT), TextNode("code block", TextType.CODE)]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), cmp)

    def test_inline_bold(self):
        node = TextNode("This is a text with a **bold block** word", TextType.TEXT)
        cmp = [TextNode("This is a text with a ", TextType.TEXT), TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), cmp)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ], new_nodes)
    
    def test_split_images_no_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)
    
    def test_split_links_no_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([], new_nodes)
    
    def test_split_images_no_image(self):
        node = TextNode("This is a text with no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with no image", TextType.TEXT)
            ], new_nodes)
    
    def test_split_links_no_link(self):
        node = TextNode("This is a text with no image", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with no image", TextType.TEXT)
            ], new_nodes)
