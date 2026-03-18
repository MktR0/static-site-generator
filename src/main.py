import os
import shutil
import sys
from copystatic import copy_contents_recursive
from generate_content import generate_pages_recursive

source = "./static"
destination = "./docs"

from_path = "./content"
dest_path = "./docs"
template_path = "./template.html"


def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    print("Deleting public directory...")
    if os.path.exists(destination):
        shutil.rmtree(destination)

    print("Copying static files to public directory...")
    copy_contents_recursive(source, destination)

    print("Generating content...")
    generate_pages_recursive(from_path, dest_path, template_path,base_path="/")


if __name__ == "__main__":
    main()
