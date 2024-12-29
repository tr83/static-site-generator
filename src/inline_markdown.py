from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if delimiter not in ['`', '*', '**']:
            raise Exception('Unknown delimiter')

        if node.text_type == TextType.TEXT:
            starting_delimiter_index = node.text.find(delimiter)
            ending_delimiter_index = node.text[starting_delimiter_index:].find(delimiter)

            if starting_delimiter_index == -1:
                new_nodes.append(node)
                continue
            if ending_delimiter_index == -1:
                raise Exception('Invalid delimiter sequence')
            
            splits = node.text.split(delimiter)
            
            if splits[0] != '':
                new_nodes.append(TextNode(splits[0], TextType.TEXT))

            new_nodes.append(TextNode(splits[1], text_type))

            if splits[2] != '':
                new_nodes.append(TextNode(splits[2], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image_or_link(old_nodes, textType):
    if textType not in [TextType.IMAGE, TextType.LINK]:
            raise ValueError('textType must be either TextType.IMAGE or TextType.LINK')
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            extracted_parts = []

            if textType == TextType.IMAGE:
                extracted_parts = extract_markdown_images(text)
                to_markdown = image_to_markdown
            elif textType == TextType.LINK:
                extracted_parts = extract_markdown_links(text)
                to_markdown = link_to_markdown
            
            number_of_parts = len(extracted_parts)

            if number_of_parts == 0:
               new_nodes.append(node) 

            for i in range(0, number_of_parts):
                markdown = to_markdown(extracted_parts[i][0], extracted_parts[i][1])
                start = text.find(markdown)
                end = start + len(markdown)

                if start != 0:
                    new_nodes.append(TextNode(text[0:start], TextType.TEXT))

                new_nodes.append(TextNode(extracted_parts[i][0], textType, extracted_parts[i][1]))

                if i == number_of_parts - 1 and end < len(text):
                    new_nodes.append(TextNode(text[end:], TextType.TEXT))

                text = text[end:]
        else:
            new_nodes.append(node)
    return new_nodes

def image_to_markdown(alt, url):
    return f'![{alt}]({url})'

def link_to_markdown(text, url):
    return f'[{text}]({url})'

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image_or_link(nodes, TextType.IMAGE)
    nodes = split_nodes_image_or_link(nodes, TextType.LINK)

    return nodes