import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nods = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nods.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: unmatched {delimiter}")

        for i in range(len(parts)):
            part = parts[i]
            if part == "":
                continue
            if i % 2 == 0:
                new_nods.append(TextNode(part, TextType.TEXT))
            else:
                new_nods.append(TextNode(part, text_type))
    return new_nods

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)

        if not matches:
            new_nodes.append(node)
            continue

        remaining = node.text

        for alt_text, url in matches:
            before, remaining = remaining.split(f"![{alt_text}]({url})", 1)

            if before == "":
                continue

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        
        remaining = node.text
        for alt, url in matches:
            before, remaining = remaining.split(f"[{alt}]({url})", 1)

            if before == "":
                continue

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            
            new_nodes.append(TextNode(alt, TextType.LINK, url))
        
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes
