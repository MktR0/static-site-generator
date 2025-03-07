import os
import shutil
from copystatic import copy_contents_recursive

source = "./static"
destination = "./public"


def main():
    print("Deleting public directory...")
    if os.path.exists(destination):
        shutil.rmtree(destination)

    print("Copying static files to public directory...")
    copy_contents_recursive(source, destination)


if __name__ == "__main__":
    main()
