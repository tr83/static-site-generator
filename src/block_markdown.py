from enum import Enum
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    HEADING = 'heading'
    PARAGRAPH = 'paragraph'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for raw_block in raw_blocks:
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

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING.value
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE.value
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH.value
        return BlockType.QUOTE.value
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH.value
        return BlockType.UNORDERED_LIST.value
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH.value
        return BlockType.UNORDERED_LIST.value
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH.value
            i += 1
        return BlockType.ORDERED_LIST.value
    return BlockType.PARAGRAPH.value

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    childNodes = []

    for block in blocks:
        type = block_to_block_type(block)
        node_as_html = block_to_html(block, type)
        childNodes.append(node_as_html)
    
    html_node = create_parent_html_tag(childNodes)
    return html_node.to_html()

def create_parent_html_tag(children = []):
    return ParentNode('html', children, { 'lang': 'en' })

def block_to_html(block_text, type):
    match type:
        case BlockType.HEADING.value:
            splits = block_text.split(' ', 1)
            children = text_to_children(splits[1])
            return ParentNode(f'h{splits[0].count('#')}', children)
        case BlockType.PARAGRAPH.value:
            children = text_to_children(block_text)
            return ParentNode('p', children)
        case BlockType.CODE.value:
            text = block_text.strip('```')
            return ParentNode('pre', [LeafNode('code', text)])
        case BlockType.QUOTE.value:
            text = block_text.strip('>')
            return LeafNode('blockquote', text)
        case _:
            children = text_to_children(block_text)
            return ParentNode('p', children)
            # raise Exception('block_to_html: Unknown block type')

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(node.text_node_to_html_node())
    return children

def main():
    markdown = '### Heading with **bold** section\n\nThis is a paragraph of text. It doesn\'t have any bold or italic words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item\
\n\n[link](https://www.boot.dev)\n\n![image](https://www.boot.dev/image.png)\n\n```python\nprint("Hello, world!")\n```\n\n> This is a quote\n\n**bold**\n\n*italic*\n\n> This is a quote with multiple lines\n> This is the second line of the quote'

    print(markdown_to_html_node(markdown))

main()