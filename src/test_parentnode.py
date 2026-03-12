import unittest
from parentnode import ParentNode
from leafnode import LeafNode

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
    self.assertEqual(
        parent_node.to_html(),
        "ValueError: ParentNode must have children",
    )

def test_to_html_empty_children(self):
    parent_node = ParentNode("div", [])
    self.assertEqual(
        parent_node.to_html(),
        "<div></div>",
    )

def test_to_html_none_tag(self):
    child_node = LeafNode("p", "child_node")
    parent_node = ParentNode(None, [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "ValueError: ParentNode must have a tag",
    )