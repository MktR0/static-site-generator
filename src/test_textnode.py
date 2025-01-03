from typing import Text
import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_empty_text(self):
        node = TextNode("", TextType.BOLD)
        node2 = TextNode("", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_default_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)
        self.assertIsNone(node2.url)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("A different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD, url="")
        self.assertNotEqual(node, node2)

    def test_not_eq_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode(
            "This is a text node",
            TextType.TEXT,
            "https://docs.python.org/3/howto/enum.html",
        )
        self.assertEqual(
            "TextNode(This is a text node, text, https://docs.python.org/3/howto/enum.html)",
            repr(node),
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_all_types(self):
        for text_type in TextType:
            if text_type == TextType.TEXT:
                node = TextNode(text="Sample", text_type=text_type)
                html_node = text_node_to_html_node(node)
                self.assertIsNone(html_node.tag)
                self.assertEqual(html_node.value, "Sample")

            elif text_type == TextType.BOLD:
                node = TextNode("This is bold", TextType.BOLD)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, "b")
                self.assertEqual(html_node.value, "This is bold")

            elif text_type == TextType.ITALIC:
                node = TextNode("This is italic", TextType.ITALIC)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, "i")
                self.assertEqual(html_node.value, "This is italic")

            elif text_type == TextType.CODE:
                node = TextNode("This is code", TextType.CODE)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, "code")
                self.assertEqual(html_node.value, "This is code")

            elif text_type == TextType.LINK:
                node = TextNode(
                    "This is a link",
                    TextType.LINK,
                    url="https://en.ac-illust.com/clip-art/24690570/free-cut-picture-material-cute-penguin",
                )
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, "a")
                self.assertEqual(html_node.value, "This is a link")
                self.assertEqual(
                    html_node.props,
                    {
                        "href": "https://en.ac-illust.com/clip-art/24690570/free-cut-picture-material-cute-penguin"
                    },
                )

            elif text_type == TextType.IMAGE:
                node = TextNode(
                    "This is an image",
                    TextType.IMAGE,
                    url="https://en.ac-illust.com/clip-art/24690570/free-cut-picture-material-cute-penguin",
                )
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, "img")
                self.assertEqual(html_node.value, "")
                self.assertEqual(
                    html_node.props,
                    {
                        "src": "https://en.ac-illust.com/clip-art/24690570/free-cut-picture-material-cute-penguin",
                        "alt": "This is an image",
                    },
                )

    def test_missing_url_image(self):
        node = TextNode(text="missing url test", text_type=TextType.IMAGE, url="")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_missing_url_link(self):
        node = TextNode(text="Missing url test", text_type=TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_missing_alt_image(self):
        node = TextNode(text="", text_type=TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_invalid_text_type(self):
        # Assumption "InvalidType" is not part of the TextType enum
        node = TextNode(text="Invalid type test", text_type="InvalidType")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
