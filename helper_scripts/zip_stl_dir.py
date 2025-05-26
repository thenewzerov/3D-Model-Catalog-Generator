import argparse
import os
import zipfile
import shutil

from utils.file_utils import find_stl_folders
from utils.search_utils import find_directories


def dry_run(model_dir):
    stl_folder_path = os.path.join(model_dir, 'STL')
    if not os.path.exists(stl_folder_path):
        print(f"No 'STL' folder found in {model_dir}")
        return

    zip_dir = os.path.join(model_dir, 'Zips')
    zip_file_path = os.path.join(zip_dir, 'STL.zip')

    print(f"   Will create zip file: {zip_file_path}")
    print("    Contents:")
    for root, dirs, files in os.walk(stl_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"       {file_path}")

    print(f"   Will delete folder: {stl_folder_path}")
    print("\n")


def zip_stl_folder(model_dir):
    stl_folder_path = os.path.join(model_dir, 'STL')
    if not os.path.exists(stl_folder_path):
        print(f"No 'STL' folder found in {model_dir}")
        return

    zip_dir = os.path.join(model_dir, 'Zips')
    os.makedirs(zip_dir, exist_ok=True)
    zip_file_path = os.path.join(zip_dir, 'STL.zip')

    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(stl_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, stl_folder_path))

    print(f"Created zip file: {zip_file_path}")


def main():
    parser = argparse.ArgumentParser(description="Find folders containing .stl files and zip the STL folder.")
    parser.add_argument("path", help="Path to the root directory to search.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actually zipping or deleting.")
    args = parser.parse_args()

    path = args.path
    dry_run_flag = args.dry_run

    invalid_folders, valid_folders = find_directories(path)

    print(f"Invalid Directories: {len(invalid_folders)}   Valid Directories: {len(valid_folders)}")

    stl_folders = []
    for model_dir in valid_folders:
        dir_with_stl = find_stl_folders(model_dir)
        if len(dir_with_stl) > 0:
            stl_folders.append(model_dir)

    print(f"Folders Containing STL files: {len(stl_folders)}")

    folders_to_clean = []

    for model_dir in stl_folders:
        print(model_dir)
        if dry_run_flag:
            dry_run(model_dir)
        else:
            zip_stl_folder(model_dir)
            folders_to_clean.append(model_dir)

    if not dry_run_flag:
        print("\n\nFolders to clean:")
        for model_dir in folders_to_clean:
            print(f"{model_dir}")

if __name__ == "__main__":
    main()