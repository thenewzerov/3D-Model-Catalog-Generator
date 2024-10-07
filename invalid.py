import os
import sys

from search_functions import find_directories


def find_invalid_folders(base_path):
    """Find folders that do not match valid criteria, considering parent folder validity."""

    invalid_folders, valid_folders = find_directories(base_path)
    return invalid_folders


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <base_path>")
        sys.exit(1)

    base_path = sys.argv[1]
    if not os.path.isdir(base_path):
        print(f"Error: The directory {base_path} does not exist.")
        sys.exit(1)

    invalid_folders = find_invalid_folders(base_path)

    if invalid_folders:
        print("Invalid folders with images, STL, or ZIP files:")
        for folder in sorted(invalid_folders):
            print(folder)
    else:
        print("No invalid folders with images, STL, or ZIP files found.")


if __name__ == "__main__":
    main()