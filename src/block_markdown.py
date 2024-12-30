from enum import Enum
import re

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

def block_to_block_type(markdown):
    if markdown.startswith('# ') or markdown.startswith('## ') or markdown.startswith('### ') or markdown.startswith('#### ') or markdown.startswith('##### ') or markdown.startswith('###### '):
        return BlockType.HEADING.value
    elif markdown.startswith('```') and markdown.endswith('```'):
        return BlockType.CODE.value
    
    lines = markdown.split('\n')

    type = None
    for line in lines:
        if (type == None or type == BlockType.QUOTE.value) and line.startswith('>'):
            type = BlockType.QUOTE.value
        elif (type == None or type == BlockType.UNORDERED_LIST.value) and (line.startswith('* ') or line.startswith('- ')):
            type = BlockType.UNORDERED_LIST.value
        elif re.match(r'^\d+\.', line):
            type = BlockType.ORDERED_LIST.value
            # Validate the ordered list block
            for j, line in enumerate(lines):
                expected_number = j + 1
                if not re.match(rf'^{expected_number}\. ', line):
                    type = BlockType.PARAGRAPH.value
            if type == BlockType.ORDERED_LIST.value:
                # Correct the ordered list block
                for j, line in enumerate(lines):
                    expected_number = j + 1
                    lines[j] = f'{expected_number}. ' + line.lstrip('0123456789. ')
                markdown = '\n'.join(lines)
        else:
            type = BlockType.PARAGRAPH.value

    return type