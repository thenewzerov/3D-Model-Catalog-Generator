import os
import sys

# List of common image file extensions
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.avif'}
# List of valid file extensions to check for
valid_extensions = {'.stl', '.zip'}


def has_image_file(folder_path):
    """Check if there is any image file in the folder."""
    for file_name in os.listdir(folder_path):
        if any(file_name.lower().endswith(ext) for ext in image_extensions):
            return True
    return False


def contains_valid_file(folder_path):
    """Check if the folder contains a file with '.stl' or '.zip' extension (case insensitive)."""
    for file_name in os.listdir(folder_path):
        if any(file_name.lower().endswith(ext) for ext in valid_extensions):
            return True
    return False


def contains_valid_subfolder(folder_path):
    """Check if the folder contains a subfolder named 'STL' or 'Zips' (case insensitive)."""
    valid_subfolder_names = {'stl', 'zips'}
    for subfolder in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, subfolder)) and subfolder.lower() in valid_subfolder_names:
            return True
    return False


def is_valid_folder(folder_path):
    """Check if the folder meets the criteria for being valid."""
    return has_image_file(folder_path) and contains_valid_subfolder(folder_path)


def find_invalid_folders(base_path):
    """Find folders that do not match valid criteria, considering parent folder validity."""
    invalid_folders = set()
    valid_folders = set()

    # First pass to identify valid folders
    for root, dirs, files in os.walk(base_path, followlinks=True):
        if is_valid_folder(root):
            valid_folders.add(root)

    # Second pass to identify invalid folders
    for root, dirs, files in os.walk(base_path, followlinks=True):
        # Skip if it's a known valid folder
        if root in valid_folders:
            continue

        # Skip if the folder is named "zips" (case-insensitive)
        if os.path.basename(root).lower() == 'zips':
            continue

        # Check if any parent of the current folder is valid
        current_folder = root
        valid_parent_found = False

        while current_folder != base_path:
            current_folder = os.path.dirname(current_folder)
            if current_folder in valid_folders:
                valid_parent_found = True
                break

        if valid_parent_found:
            continue

        # If no valid parent found, check for images, STL, or ZIP files
        if has_image_file(root) or contains_valid_file(root):
            invalid_folders.add(root)

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