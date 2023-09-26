import os
import sys
import argparse

import string
import random
from pprint import pprint


# This constant defines what text editor will be used, feel free to change it.
EDITOR = "nvim"


def random_string(character_set: str, length: int, exclude: list[str] = None):
    while True:
        # Generate random string that isn't in the exclusion list of the specified length with the specific character set.
        rng_str = "".join(random.choice(character_set) for _ in range(length))
        if not(exclude) or not(any(rng_str in x for x in exclude)):
            return rng_str


def valid_file_name(file_name: str):
    # Go through each character in the bad character list, if it is in the file name, return False, if none of them are in it return True.
    bad_characters = r"\/:*?<>|" if sys.platform == "win32" else "\0/"
    return not(any(c in bad_characters for c in file_name))


def rename(path: str, quiet: bool):
    if not os.path.isdir(path):
        # If passed path isn't a directory inform the user if the quiet mode is off, exit the program regardless of that.
        if not quiet:
            print("You have specified invalid path. Try again.")
        return

    # Get the list of files/directories for the passed path.
    os.chdir(path)
    content = os.listdir()

    # Generate a unique name for the temporary file.
    available_characters = string.ascii_letters + string.digits
    temp_file_name = random_string(available_characters, length=max(len(file_name) for file_name in content), exclude=content) + ".tmp"

    # Create a temp file, write names of directories/files to it.
    with open(temp_file_name, 'w', encoding="UTF-8") as temp_file:
        print(*content, file=temp_file, sep='\n')

    # Open the text editor on that file to edit it.
    os.system(f"{EDITOR} {temp_file_name}")

    # If the file has been deleted exit the program, if the quiet mode is not turned on, inform the user of his mistake.
    if not os.path.exists(temp_file_name):
        if not quiet:
            print("The temporary file, that holds the file names of all the content of the current directory has been deleted. Try again.")
        return

    # After the file has been altered, read it.
    with open(temp_file_name, 'r', encoding="UTF-8") as temp_file:
        new_content = [x.removesuffix('\n') for x in temp_file.readlines()]

    # After the file has been read, we do not need it anymore, delete it.
    os.remove(temp_file_name)

    # Check if the new file/directory names are valid, if there are duplicates, if some got deleted, etc.
    if len(content) > len(new_content):
        if not quiet:
            print("Some file names have been deleted, to delete files do that manually. Try again.")
        return
    elif len(content) < len(new_content):
        if not quiet:
            print("There are some new file names, to create new files do that manually. Try again.")
        return
    elif len(content) != len(set(new_content)):
        if not quiet:
            print("There are some duplicate file names, each file must have a unique file name. Try again.")
        return
    elif not all(valid_file_name(file_name) for file_name in new_content):
        if not quiet:
            print("There are some file names, that cannot be used as file name. Try again.")
        return

    if not quiet:
        # If program isn't in quiet mode, print new changes, ask user if he accepts them, if not, exit program.
        pprint(dict(zip(content, new_content)))
        if input("Do you accept these new changes? (y/n): ").strip().lower() not in ('y', 'yes'):
            return

    # Dictionary in which we will store the the intermediate names.
    mid_changes = {}

    for old_name, new_name in zip(content, new_content):
        # Go through each pair of old and new name, create an intermediate name before making the final change, in case some file names got swapped, this will solve that problem.
        os.rename(old_name, mid_name := random_string(available_characters, length=max(len(file_name) for file_name in content + new_content), exclude=content + new_content + list(mid_changes.values())))
        mid_changes[mid_name] = new_name

    for mid_name, new_name in mid_changes.items():
        # Go through each pair of intermediate name and new name, make a final change.
        os.rename(mid_name, new_name)


def main():
    # Create parser to parse arguments passed to the program.
    parser = argparse.ArgumentParser(description="Python program for bulk renaming files, with the editor of choice.")
    parser.add_argument("-p", "--path", type=str, default=".", required=False, help="Path of directory where to perform the bulk renaming. If path isn't provided, the action will be performed on the current directory.")
    parser.add_argument("-q", "--quiet", action="store_true", required=False, help="Use this flag, to perform the action without any confirmation and output.")

    args = parser.parse_args()
    rename(args.path, args.quiet)


if __name__ == "__main__":
    main()
