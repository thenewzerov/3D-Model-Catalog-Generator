import argparse

from utils.file_utils import find_stl_folders


def main():
    parser = argparse.ArgumentParser(description="Find folders containing .stl files.")
    parser.add_argument("path", help="Path to the root directory to search.")
    args = parser.parse_args()

    stl_folders = find_stl_folders(args.path)

    if stl_folders:
        print("Folders containing .stl files:")
        for folder in stl_folders:
            print(folder)
    else:
        print("No folders with .stl files found.")

if __name__ == "__main__":
    main()