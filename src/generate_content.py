import re
from block_markdown import markdown_to_html_node


def extract_title(markdown):
    pattern = r"(\#)(\s+)(\w.*)"

    lines = markdown.split("\n")
    for line in lines:
        match = re.match(pattern, line)
        if match:
            return match.group(3).strip()
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        src_file = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    title = extract_title(src_file)
    node = markdown_to_html_node(src_file)
    content = node.to_html()

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(dest_path, "w") as file:
        file.write(template)
        file.write("\n")
    print(f"Generated {title} at {dest_path}")
