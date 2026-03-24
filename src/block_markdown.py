from enum import Enum

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
    if block.startswith("```\n") and block.endswith("```"):
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