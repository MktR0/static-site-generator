import re

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

block_type_heading = "heading"
block_type_paragraph = "paragraph"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    """ """
    # This would normalize line endings before splitting
    normalized_content = re.sub(r"\r\n", "\n", markdown)
    raw_blocks = re.split(r"\n\n+", normalized_content)
    non_empty_blocks = list(filter(lambda a: a != "", raw_blocks))

    # TODO: Consider extracting this function
    def normalize_whitespace(line):
        return "\n".join(re.split(r"\n\s+^\t", line)).strip()

    return list(map(normalize_whitespace, non_empty_blocks))


def block_to_block_type(block):
    # returns the appropriate string type
    # if none of the above conditions are met, the block is a normal paragraph.
    if is_heading(block):
        return block_type_heading
    if is_code_block(block):
        return block_type_code
    if is_quote_block(block):
        return block_type_quote
    if is_olist(block):
        return block_type_olist
    if is_ulist_block(block):
        return block_type_ulist
    else:
        return block_type_paragraph


def is_heading(block):
    """
    Headings start with 1-6 "#" characters,
    followed by a space and then the heading text.
    """
    pattern = r"\#{1,6}\s.*"
    return bool(re.match(pattern, block))


def is_code_block(block):
    """
    Code blocks must start with 3 backticks
    and end with 3 backticks.
    """
    # captures any amount of space between backticks
    pattern = r"(?s)\`{3}.*?\`{3}$"
    return bool(re.match(pattern, block))


def is_quote_block(block):
    """
    Every line in a quote block must
    start with a ">" character.
    """

    # captures various amounts of space
    # ignores blank lines when processing data
    def split_inner_text(block):
        split_block = block.split("\n")
        non_empty_blocks = list(filter(lambda a: a != "", split_block))
        return non_empty_blocks

    def check_match(block):
        pattern = r"(?s)\>+.*?$"
        return bool(re.match(pattern, block))

    inner_blocks = split_inner_text(block)

    return len(list(filter(check_match, inner_blocks))) == len(inner_blocks)


def is_ulist_block(block):
    """
    Every line in an unordered list block must
    start with a "*" or "-" character, followed by a space."""

    def split_inner_text(block):
        split_block = block.split("\n")
        non_empty_blocks = list(filter(lambda a: a != "", split_block))
        return non_empty_blocks

    def check_match(block):
        pattern = r"(?s)[\*\-]\s.*?$"
        return bool(re.match(pattern, block))

    inner_blocks = split_inner_text(block)

    return len(list(filter(check_match, inner_blocks))) == len(inner_blocks)


def is_olist(block):
    """
    Every line in an ordered list block must
    start with a number followed by a "." character and a space.
    The number must start at 1 and increment by 1 for each line.
    """

    def split_inner_text(block):
        split_block = block.split("\n")
        non_empty_blocks = list(filter(lambda a: a != "", split_block))
        return non_empty_blocks

    def get_match(block):
        pattern = r"^\d\.\s"
        matches = re.search(pattern, block)
        if not matches:
            return ""
        return matches.group()

    inner_blocks = split_inner_text(block)

    # checks 1st block exists and starts with '1'
    first_match = get_match(inner_blocks[0])
    if not first_match or first_match[:1] != "1":
        return False

    # increment by '1'
    for line in range(1, len(inner_blocks)):
        match = get_match(inner_blocks[line])
        if not match or match[:1] != str(line + 1):
            return False
    return True


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children = []
    for markdown_block in markdown_blocks:
        html_node = markdown_block_to_html(markdown_block)
        children.append(html_node)
    return ParentNode("div", children, None)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_block_to_html(markdown_block):
    markdown_block_type = block_to_block_type(markdown_block)
    match markdown_block_type:
        case "heading":
            return heading_to_html_node(markdown_block)
        case "paragraph":
            return paragraph_to_html_node(markdown_block)
        case "code":
            return code_to_html_node(markdown_block)
        case "ordered_list":
            return olist_to_html_node(markdown_block)
        case "unordered_list":
            return ulist_to_html_node(markdown_block)
        case "quote":
            return quote_to_html_node(markdown_block)
        case _:
            raise ValueError("Invalid type!")


def heading_to_html_node(block):
    def get_match(block):
        block = block.strip()
        level = 0
        pattern = r"(\#+)(\s.*)"
        if not is_heading(block):
            raise ValueError("Not a valid code block")

        matches = re.search(pattern, block)
        level = len(matches.group(1))
        text = block[level + 1 :].strip()
        return level, text

    level, text = get_match(block)

    if len(block) <= level or level > 6:
        raise ValueError(f"Not a valid heading level: {level}")
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def paragraph_to_html_node(block):
    # completed
    lines = block.split("\n")
    non_empty_lines = list(filter(lambda a: a != "", lines))
    paragraph = " ".join(non_empty_lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def code_to_html_node(block):
    # interesting bit more robust

    def get_match(block):
        block = block.strip()

        # TODO: update to allow for syntax highlighting options
        # pattern = r"(?s)\`{3}(\w+\s*)?(.*?)\`{3}$"
        # language = matches.group(1).strip() or "text"
        # code = matches.group(2)

        pattern = r"(?s)\`{3}(?:\w+\s*)?(.*?)\`{3}$"
        matches = re.search(pattern, block)
        if not matches:
            raise ValueError("Not a valid code block")
        return matches.group(1)

    text = get_match(block)
    # text_to_children is not used
    # create a textnode to represent the children
    # to maintain any markdown withiin code block
    children = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(children)
    code = ParentNode("code", [children])
    return ParentNode("pre", [code])


def quote_to_html_node(block):

    def split_inner_text(block):
        split_block = block.split("\n")
        non_empty_lines = list(filter(lambda a: a != "", split_block))
        return non_empty_lines

    def check_match(block):
        # TODO: add nesting functionality to quotes
        # create separate capture group, count the level of >
        #
        pattern = r"(?s)\>+.*?$"
        matches = re.match(pattern, block)
        if not matches:
            raise ValueError("Not a valid quote block")
        return block.lstrip(">").strip()

    def get_match(block):
        inner_blocks = split_inner_text(block)
        content = " ".join(list(map(check_match, inner_blocks)))
        return content

    content = get_match(block)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):

    def split_inner_text(block):
        split_block = block.split("\n")
        non_empty_blocks = list(filter(lambda a: a != "", split_block))
        return non_empty_blocks

    def check_match(block):
        pattern = r"(^[\*\-]\s+)(.*?$)"
        matches = re.match(pattern, block)
        if not matches:
            raise ValueError("Not a valid list block")
        return matches.group(2).strip()

    def get_match(block):
        inner_blocks = split_inner_text(block)
        items = list((map(check_match, inner_blocks)))
        create_node = lambda text: ParentNode("li", text_to_children(text))
        return list(map(create_node, items))

    children = get_match(block)
    return ParentNode("ul", children)


def olist_to_html_node(block):

    def split_inner_text(block):
        split_block = block.split("\n")
        non_empty_blocks = list(filter(lambda a: a != "", split_block))
        return non_empty_blocks

    def check_match(block):
        pattern = r"(^\d+\.\s+\t?)(.*?$)"
        matches = re.match(pattern, block)
        if not matches:
            raise ValueError("Not a valid list block")
        return matches.group(2).strip()

    def get_match(block):
        inner_blocks = split_inner_text(block)
        items = list((map(check_match, inner_blocks)))
        create_node = lambda text: ParentNode("li", text_to_children(text))
        return list(map(create_node, items))

    children = get_match(block)
    return ParentNode("ol", children)


# split markdown into blocks, using markdown_to_blocks
# loop over the markdown blocks
# create an htmlnode for each of the markdown blocks
# check the type with markdown_block_type
# conversion functions will:
# use text_to_children on the text
# use text_to_children to get children
# return an htmlnode with tag (from conversion function) and children from text_to_children
# wrap everything in a div and return
