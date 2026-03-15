from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nods = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nods.append(node)
            continue

        parts = node.text.split(delimiter)

        if parts % 2 == 0:
            raise Exception(f"Invalid Markdown syntax: unmatched {delimiter}")

        for i in range(len(parts)):
            part = parts[i]
            if part == "":
                continue
            if i % 2 == 0:
                new_nods.append(TextNode(part, TextType.TEXT))
            else:
                new_nods.append(TextNode(part, text_type))
        