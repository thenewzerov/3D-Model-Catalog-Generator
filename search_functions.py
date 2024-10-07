# List of common image file extensions
import os

from PIL import Image

# Valid image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.avif'}
# List of valid file extensions to check for
VALID_FILE_EXTENSIONS = {'.stl', '.zip'}


def directory_contains_image_file(folder_path):
    """Check if there is any image file in the folder."""
    for file_name in os.listdir(folder_path):
        if any(file_name.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            return True
    return False

def is_valid_image_file(file):
    try:
        # Skip the file if it does not have an image extension
        if not any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            return False
        Image.open(file)
        return True
    except:
        return False


def contains_valid_file(folder_path):
    """Check if the folder contains a file with '.stl' or '.zip' extension (case insensitive)."""
    for file_name in os.listdir(folder_path):
        if any(file_name.lower().endswith(ext) for ext in VALID_FILE_EXTENSIONS):
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
    return directory_contains_image_file(folder_path) and contains_valid_subfolder(folder_path)


def contains_stl_folder(folder):
    # Check if the path contains the following folders.  Ignore Case:
    # 'STL', 'Zips', 'Renders'
    # If it does, return True.  Otherwise, return False.
    for root, dirs, files in os.walk(folder):
        for subfolder in dirs:
            if subfolder.lower() == 'stl':
                return True
            if subfolder.lower() == 'zips':
                return True
            if subfolder.lower() == 'renders':
                return True


def find_directories(base_dir):
    """Find folders that do not match valid criteria, considering parent folder validity."""
    invalid_folders = set()
    valid_folders = set()

    # First pass to identify valid folders
    for root, dirs, files in os.walk(base_dir, followlinks=True):
        if is_valid_folder(root):
            valid_folders.add(root)

    # Second pass to identify invalid folders
    for root, dirs, files in os.walk(base_dir, followlinks=True):
        # Skip if it's a known valid folder
        if root in valid_folders:
            continue

        # Skip if the folder is named "zips" (case-insensitive)
        if os.path.basename(root).lower() == 'zips':
            continue

        # Check if any parent of the current folder is valid
        current_folder = root
        valid_parent_found = False

        while current_folder != base_dir:
            current_folder = os.path.dirname(current_folder)
            if current_folder in valid_folders:
                valid_parent_found = True
                break

        if valid_parent_found:
            continue

        # If no valid parent found, check for images, STL, or ZIP files
        if directory_contains_image_file(root) or contains_valid_file(root):
            invalid_folders.add(root)

    return invalid_folders, valid_folders