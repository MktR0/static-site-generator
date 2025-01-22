from textnode import TextNode, TextType


def main():
    sample_text_node = TextNode(
        "This is a test of the text node system", TextType.BOLD, "helloWorld.com"
    )
    print(sample_text_node)


main()
