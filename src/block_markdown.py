def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []

    for block in blocks:
        strip_block = block.strip()
        if len(strip_block) == 0:
            continue
        clean_blocks.append(strip_block)

    return clean_blocks