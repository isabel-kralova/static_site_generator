import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

def test_split(self):
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertListEqual(
        new_nodes,
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ],
    )

def test_no_delimeter(self):
    node = TextNode("Just text", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertListEqual(
        new_nodes,
        [TextNode("Just text", TextType.TEXT)],
    )

def test_unmatched_delimeter(self):
    node = TextNode("Text with `unmatched delimeter", TextType.TEXT)
    with self.assertRaises(Exception):
        split_nodes_delimiter([node], "`", TextType.CODE)

def test_multiple_code(self):
    node = TextNode("This is text with `code1` and `code2` block", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertListEqual(
        new_nodes,
        [
            [TextNode("This is text with ", TextType.TEXT)],
            [TextNode("code1", TextType.CODE)],
            [TextNode(" and ", TextType.TEXT)],
            [TextNode("code2", TextType.CODE)],
            [TextNode(" block", TextType.TEXT)],
        ],
    )

def test_non_text_node(self):
    node = TextNode("already code", TextType.CODE)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertListEqual(new_nodes, [node])

def test_delim_bold_italic(self):
    node = TextNode("Text with **bold** and _italic_", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    self.assertListEqual(
        new_nodes,
        [
            [TextNode("Text with ", TextType.TEXT)],
            [TextNode("bold", TextType.BOLD)],
            [TextNode(" and ", TextType.TEXT)],
            [TextNode("italic", TextType.ITALIC)],
        ]
    )

if __name__ == "__main__":
    unittest.main()