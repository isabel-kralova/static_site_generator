from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    TEXT = "text"       # text (plain)
    BOLD = "bold"       # **Bold text**
    ITALIC = "italic"   # _Italic text_
    CODE = "code"       # `Code text`
    LINK = "link"       # [anchor text](url)
    IMAGE = "image"     # ![alt text](url)

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(self):
    if self.text_type == TextType.TEXT:
        return LeafNode(None, self.text)
    elif self.text_type == TextType.BOLD:
        return LeafNode("b", self.text)
    elif self.text_type == TextType.ITALIC:
        return LeafNode("i", self.text)
    elif self.text_type == TextType.CODE:
        return LeafNode("code", self.text)
    elif self.text_type == TextType.LINK:
        return LeafNode("a", self.text, {"href": self.url})
    elif self.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": self.url, "alt": self.text})
    else:
        raise Exception("Invalid TextType")
    