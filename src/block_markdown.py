from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []

    for block in blocks:
        strip_block = block.strip()
        if len(strip_block) == 0:
            continue
        clean_blocks.append(strip_block)

    return clean_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    # HEADING
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    # CODE
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    # QUOTE
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    # UNORDERED LIST
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    
    # ORDERED LIST
    number = 1
    is_ordered = True
    for line in lines:
        if not line.startswith(f"{number}. "):
            is_ordered = False
            break
        number += 1
    if is_ordered:
        return BlockType.ORDERED_LIST

    # PARAGRAPH
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes

def get_heading_level(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break
    return count

def strip_code_block(block):
    lines = block.split("\n")

    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]

    return "\n".join(lines) + "\n"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = " ".join(line.strip() for line in block.split("\n"))
            node = ParentNode(
                tag="p",
                children=text_to_children(text)
            )
        
        elif block_type == BlockType.HEADING:
            level = get_heading_level(block)
            text = block[level + 1:]
            node = ParentNode(
                tag=f"h{level}",
                children=text_to_children(text)
            )
        
        elif block_type == BlockType.CODE:
            code_content = strip_code_block(block)
            text_node = TextNode(code_content, TextType.TEXT)
            code_html = text_node_to_html_node(text_node)
            node = ParentNode(
                tag="pre",
                children=[
                    ParentNode(tag="code", children=[code_html])
                ]
            )

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            parts = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("Invalid quote block")
                clean_line = line.lstrip(">").strip()
                parts.append(clean_line)
            cleaned = " ".join(parts)
            node = ParentNode(
                tag="blockquote",
                children=text_to_children(cleaned)
            )

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                text = item[2:]
                li_nodes.append(
                    ParentNode(tag="li", children=text_to_children(text)))
            node = ParentNode(tag="ul", children=li_nodes)
        
        elif block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                text = item.split(". ", 1)[1]
                li_nodes.append(ParentNode(tag="li", children=text_to_children(text)))
            node = ParentNode(tag="ol", children=li_nodes)
        
        else:
            raise ValueError(f"Unknown block type: {block_type}")
        
        children.append(node)
    
    return ParentNode(tag="div", children=children)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line [2:].strip()
    raise Exception("No h1 header found in markdown")