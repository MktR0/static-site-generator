import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode

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

    def test_none_value_raise_error(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_children_starts_none(self):
        node = LeafNode(tag="p", value="This is text")
        self.assertIsNone(node.children)

    def test_cannot_add_children(self):
        node = LeafNode(tag="p", value="This is text")
        with self.assertRaises(AttributeError):
            node.children = [LeafNode("a", "unacceptable text")]

    def test_only_value(self):
        node = LeafNode(tag="p", value="This is a paragraph of text")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text</p>")

    def test_one_leaf(self):
        node = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_no_tag(self):
        node = LeafNode(None, "Hello, Buddy!")
        self.assertEqual(node.to_html(), "Hello, Buddy!")

    def test_initialization(self):
        # Create a ParentNode and ensure attributes are set correctly
        children = [
            LeafNode(tag="b", value="Bold Text"),
            LeafNode(tag=None, value="Text"),
        ]
        node = ParentNode(tag="p", children=children)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children, children)

    def test_no_tag_raises_error(self):
        child_node = [LeafNode(tag="b", value="Bold Text")]
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=child_node).to_html()

    def test_no_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=None).to_html()

    def test_cannot_set_value(self):
        child_node = [LeafNode(tag="b", value="Bold Text")]
        node = ParentNode(tag="div", children=child_node)
        with self.assertRaises(AttributeError):
            node.value = "some value"

    def test_to_html_with_children(self):
        child_node = [LeafNode("span", "child")]
        parent_node = ParentNode("div", children=child_node)
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = [LeafNode("b", "grandchild")]
        child_node = [ParentNode("span", children=grandchild_node)]
        parent_node = ParentNode("div", children=child_node)
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )



if __name__ == "__main__":
    unittest.main()
