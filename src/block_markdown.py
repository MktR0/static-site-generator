import re 

def markdown_to_blocks(markdown):
    # This would normalize line endings before splitting
    markdown = re.sub(r'\r\n', '\n', markdown)
    markdown_block = re.split(r'\n\n+', markdown)
    markdown_block = list(filter(lambda a: a != "", markdown_block))

    def stripper(line):
        return "\n".join(re.split(r'\n\s+^\t',line)).strip()
    
    return list(map(stripper,markdown_block))
