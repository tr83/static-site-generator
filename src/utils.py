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