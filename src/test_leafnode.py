import unittest
from leafnode import LeafNode

def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

def test_leaf_to_html_a(self):
    node = LeafNode("a", "This is a paragraph of text.")
    self.assertEqual(node.to_html(), "<a>This is a paragraph of text.</a>")

def test_leaf_to_html_a_pr(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(node.to_html, '<a href="https://www.google.com">Click me!</a>')