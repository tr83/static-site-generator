from textnode import TextNode, TextType

def main():
    textNode = TextNode('Test text', TextType.BOLD, 'https://www.boot.dev')
    print(textNode)

main()