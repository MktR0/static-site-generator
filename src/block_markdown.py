import re 

def markdown_to_blocks(markdown):
    # This would normalize line endings before splitting
    normalized_content = re.sub(r'\r\n', '\n', markdown)
    raw_blocks = re.split(r'\n\n+', normalized_content)
    non_empty_blocks = list(filter(lambda a: a != "", raw_blocks))

    # TODO: Consider extracting this function
    def normalize_whitespace(line):
        return "\n".join(re.split(r'\n\s+^\t',line)).strip()
    
    return list(map(normalize_whitespace,non_empty_blocks))


