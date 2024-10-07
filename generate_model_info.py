# Write a program to go through all subdirectories of a given directory.
# If the directory contains an image, and a folder called 'STL' under it, print the name of the folder.
import argparse
import os

from search_functions import is_valid_folder, find_directories


# Method to read files
def read_file(file):
    with open(file, 'r') as f:
        data = f.read()
    return data

def create_model_info(file_path, model_name, character_name, series, tags, model_category):
    """Create a model-info.txt file with the provided model details."""
    # Overwrite the file if it already exists
    with open(file_path, 'w') as f:
        f.write(f"Model Name: {model_name}\n")
        f.write(f"Character Name: {character_name}\n")
        f.write(f"Series: {series}\n")
        f.write(f"Tags: {', '.join(tags)}\n")
        f.write(f"Model Category: {model_category}\n")

def print_model_info(file_path, model_name, character_name, series, tags, model_category):
    """Print the model details to the console."""
    print(f"\nDirectory: {file_path}")
    print("Model Info:")
    print(f"\tModel Name: {model_name}")
    print(f"\tCharacter Name: {character_name}")
    print(f"\tSeries: {series}")
    print(f"\tTags: {', '.join(tags)}")
    print(f"\tModel Category: {model_category}")


# Method to generate the html file from the directory structure
def gen_model_info_from_directory_structure(path):

    total_dirs = 0
    models_to_check = []
    invalid_folders, valid_folders = find_directories(path)

    for model_dir in valid_folders:

        # Break the path up into tokens separated by '/'
        tokens = model_dir.split('\\')
        folder_name = os.path.basename(path)

        category = ''

        # Start at the token that matches the folder name.
        # Could probably screw up here if the folder name is not unique to a subfolder.
        # But that doesn't sound like a "me" problem.
        for i in range(len(tokens)):
            if tokens[i] == folder_name:
                # Save the next token as the category.
                category = tokens[i + 1]
                break

        tags = []

        # Save the folder above the Model folder as 'Series Name'.
        series_name = tokens[-2]
        # Save the Name of the folder as 'Model Name'.
        model_name = tokens[-1]
        character_name = tokens[-1]

        # If the character name has a '-' in it, split it and take the first part.
        if ' - ' in character_name:
            model_tags = character_name.split(' - ')[1].strip()
            character_name = character_name.split(' - ')[0]
            character_name = character_name.strip()
            model_name = character_name

            # Get the model tags
            # Split the model_tags by spaces, and add them to the tags list.
            model_tags = model_tags.split(' ')
            for tag in model_tags:
                tags.append(tag)

        # If the character name has a number at the end, remove it and trim the whitespace.
        # Only do this if it's a single number (for now).
        if character_name[-1].isdigit():
            if character_name[-2] == ' ':
                character_name = character_name[:-1]

        # If the character name has an '_' in it, split it.
        # The first part becomes the character name, and the second part becomes the model name.
        if '_' in character_name:
            model_name = character_name.split('_')[1]
            character_name = character_name.split('_')[0]

            character_name = character_name.strip()
            model_name = character_name + ' - ' + model_name.strip()

        else:
            character_name = character_name.strip()

        # Print the model info to the console
        print_model_info(
            file_path=model_dir,
            model_name=model_name,
            character_name=character_name,
            series=series_name,
            tags=tags,
            model_category=category
        )

        # Write the output to the html file
        # Embed the image data in the html file as a base64 string
        create_model_info(
            file_path=os.path.join(model_dir, 'model-info.txt'),
            model_name=model_name,
            character_name=character_name,
            series=series_name,
            tags=tags,
            model_category=category
        )

        total_dirs += 1

        if character_name == series_name:
            models_to_check.append(model_dir)

    print(f"\nTotal Directories: {total_dirs}")

    # Sort the models to check
    models_to_check.sort()

    print("\nModels to Check:")
    for model in models_to_check:
        print(model)

# Main function
def main():
    try:
        # Create the argument parser
        parser = argparse.ArgumentParser(description="Generate Model Info")

        # Add a flag for using model-info.txt
        parser.add_argument('path', type=str, help="Path to the root models directory")

        # Parse the arguments
        args = parser.parse_args()

        path = args.path
        # Make sure the path is a directory
        if not os.path.isdir(path):
            print('Invalid path')
            return

        gen_model_info_from_directory_structure(path)

    except Exception as e:
        print(e)


# Run the main function
if __name__ == '__main__':
    main()
