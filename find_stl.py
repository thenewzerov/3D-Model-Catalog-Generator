import os
import argparse

def find_stl_folders(path):
    stl_folders = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".stl"):
                stl_folders.append(root)
                break  # Stop searching the current folder after finding one STL file
    return stl_folders

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