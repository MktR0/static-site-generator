import os
import shutil
from copystatic import copy_contents_recursive
from generate_content import generate_page

source = "./static"
destination = "./public"

from_path = "./content/index.md"
dest_path = "./public/index.html"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(destination):
        shutil.rmtree(destination)

    print("Copying static files to public directory...")
    copy_contents_recursive(source, destination)
    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
