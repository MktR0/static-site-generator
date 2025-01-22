import re

block_type_heading = "heading"
block_type_paragraph = "paragraph"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    # This would normalize line endings before splitting
    normalized_content = re.sub(r'\r\n', '\n', markdown)
    raw_blocks = re.split(r'\n\n+', normalized_content)
    non_empty_blocks = list(filter(lambda a: a != "", raw_blocks))

    # TODO: Consider extracting this function
    def normalize_whitespace(line):
        return "\n".join(re.split(r'\n\s+^\t',line)).strip()

    return list(map(normalize_whitespace,non_empty_blocks))


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

    return len(list(filter(check_match,inner_blocks))) == len(inner_blocks)

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

    return len(list(filter(check_match,inner_blocks))) == len(inner_blocks)

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
            return False
        return matches.group()


    inner_blocks = split_inner_text(block)
    # checks 1st exists and is '1' 
    if not get_match(inner_blocks[0]) or get_match(inner_blocks[0])[:1] != "1":
        return False
    # increment by '1' 
    for line in range(1, len(inner_blocks)):
        if get_match(inner_blocks[line])[:1] != str(line+1):
            return False
    return True
