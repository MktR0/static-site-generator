import os
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


def generate_pages_recursive(
    dir_path_content, dest_dir_path, template_path, ignore_list=None
):

    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    directory_contents = os.listdir(dir_path_content)
    if ignore_list is not None:
        directory_contents = [
            file
            for file in os.listdir(dir_path_content)
            if file not in ignore_list and not file.startswith((".", ""))
        ]

    for item in directory_contents:
        source_content = os.path.join(dir_path_content, item)
        dest_content = os.path.join(dest_dir_path, item)
        print(f" {source_content} -> {dest_content}")

        if os.path.isfile(source_content) and source_content.endswith(".md"):
            dest_content = dest_content[:-3] + ".html"
            generate_page(source_content, template_path, dest_content)
        elif os.path.isdir(source_content):
            generate_pages_recursive(
                source_content, dest_content, template_path, ignore_list
            )
        else:
            print(f"Non-markdown content detect: {source_content}")
