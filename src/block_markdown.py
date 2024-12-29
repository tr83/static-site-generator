def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for i, raw_block in enumerate(raw_blocks):
        stripped_block = raw_block.strip()
        if stripped_block == '' or stripped_block == '\n':
            continue

        lines = stripped_block.split('\n')

        if len(lines) == 1:
            blocks.append(lines[0])
            continue

        block_string = ''
        for line in lines:
            isLastLine = line == lines[-1]
            block_string += line.strip() + ('' if isLastLine else '\n')
        
        blocks.append(block_string)

    return blocks

# Remove and finish the section with tests
def main():
    markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    

   * This is the first list item in a list block
* This is a list item
* This is another list item"""
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        print(block)

main()