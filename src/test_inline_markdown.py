import unittest
from textnode import TextNode, TextType
import inline_markdown

class TestInlineMarkdown(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_delimiter([node], "`", TextType.CODE)
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
        new_nodes = inline_markdown.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [TextNode("Just text", TextType.TEXT)],
        )

    def test_unmatched_delimeter(self):
        node = TextNode("Text with `unmatched delimeter", TextType.TEXT)
        with self.assertRaises(Exception):
            inline_markdown.split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_code(self):
        node = TextNode("This is text with `code1` and `code2` block", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
                TextNode(" block", TextType.TEXT),
            ],
        )

    def test_non_text_node(self):
        node = TextNode("already code", TextType.CODE)
        new_nodes = inline_markdown.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes, [node])

    def test_delim_bold_italic(self):
        node = TextNode("Text with **bold** and _italic_", TextType.TEXT)
        new_nodes = inline_markdown.split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = inline_markdown.split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ]
        )

    def test_extract_markdown_images(self):
        matches = inline_markdown.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = inline_markdown.extract_markdown_links(
            "This is text with an [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = inline_markdown.split_nodes_image([node])
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
            "This is text with an [link](https://www.boot.dev) and another [second link](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = inline_markdown.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_full_markdown_parsing(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        nodes = inline_markdown.text_to_textnodes(text)

        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_image_not_parsed_as_link(self):
        text = "Here is an image ![alt](img.png)"

        nodes = inline_markdown.text_to_textnodes(text)

        self.assertListEqual(
            nodes,
            [
                TextNode("Here is an image ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "img.png"),
            ],
        )

if __name__ == "__main__":
    unittest.main()