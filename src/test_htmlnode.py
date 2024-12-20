import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="a", value=None, children=None, props=None)

        self.assertEqual("HTMLNode(a, None, None, None)", repr(node))

    def test_no_props(self):
        node = HTMLNode(tag="h1", value="Welcome", children=None, props=None)

        self.assertEqual(node.props_to_html(), "")

    def test_single_prop(self):
        node = HTMLNode(
            tag="h1",
            value="Welcome",
            children=None,
            props={"href": "https://www.google.com"},
        )
        
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_multiple_prop(self):
        node = HTMLNode(
            tag="h1",
            value="Welcome",
            children=None,
            props={
                "class": "main-content",
                "id": "section1",
                "style": "color: red; font-size: 14px",
                "data-custom": "value",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' class="main-content" id="section1" style="color: red; font-size: 14px" data-custom="value"',
        )
