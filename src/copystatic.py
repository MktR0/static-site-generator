import os
import shutil


def ignore():
    try:
        with open(".gitignore", "r") as f:
            read = f.read().splitlines()
            return [file.strip("/") for file in read if file]
    except FileNotFoundError:
        return []


def copy_contents_non_recursive(source, destination, ignore_list=None):

    for source_dir, _, files in os.walk(source):
        destination_dir = os.path.join(destination, os.path.relpath(source_dir, source))
        os.makedirs(destination_dir)

        if ignore_list is not None:
            files = [
                file
                for file in files
                if file not in ignore_list and not file.startswith((".", ""))
            ]

        for file in files:
            source_file = os.path.join(source_dir, file)
            destination_file = os.path.join(destination_dir, file)
            print(f" {source_file} -> {destination_file}")
            shutil.copy(source_file, destination_file)


def copy_contents_recursive(source, destination, ignore_list=None):
    if not os.path.exists(destination):
        os.makedirs(destination)

    directory_contents = os.listdir(source)
    if ignore_list is not None:
        directory_contents = [
            file
            for file in os.listdir(source)
            if file not in ignore_list and not file.startswith((".", ""))
        ]

    for item in directory_contents:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        print(f" {source_path} -> {destination_path}")

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        else:
            copy_contents_recursive(source_path, destination_path, ignore_list)
