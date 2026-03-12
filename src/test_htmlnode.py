import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    #HTMLNode
    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://www.google.com"'
        )

    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_multiple(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank"
        })
        result = node.props_to_html()

        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)


    #LeafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            node.to_html(), 
            "<p>Hello, world!</p>",
        )

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(), 
            "<a>This is a paragraph of text.</a>",
        )

    def test_leaf_to_html_a_pr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.google.com">Click me!</a>',
        )
    
    #ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), 
            "<div><span>child</span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        child1 = LeafNode("a", "child1")
        child2 = LeafNode("b", "child2")
        child3 = LeafNode("c", "child3")
        parent_node = ParentNode("p", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<p><a>child1</a><b>child2</b><c>child3</c></p>",
        )

    def test_to_html_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(
            parent_node.to_html(),
            "<div></div>",
        )

    def test_to_html_none_tag(self):
        child_node = LeafNode("p", "child_node")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()