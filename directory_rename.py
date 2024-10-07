import argparse
import os

from search_functions import find_directories


def rename_dirs(base_dir):
    changed_dirs = []
    unchanged_dirs = []

    invalid_folders, valid_folders = find_directories(base_dir)

    # Walk through all directories and subdirectories
    for model_dir in valid_folders:

        parent_folder = os.path.dirname(model_dir)
        dirname = os.path.basename(model_dir)

        # Look for the tags in the directory name
        # These are the only tags I have, so set your own here if you need to.
        # Also, might want to jump down a few lines and add your own tags to the character_name and model_version
        tags = []
        if 'chibi' in dirname.lower():
            tags.append('Chibi')
        if 'nsfw' in dirname.lower():
            tags.append('NSFW')

        character_name = ''
        model_version = ''

        # Check if ' - ' is in the directory name
        if ' - ' in dirname:
            # Split the directory name by ' - ', take the first part as the character name
            # and the second part as the model version
            character_name, model_version = dirname.split(' - ')

        else:
            character_name = dirname

        # Replace the word 'chibi' and 'nsfw' with an empty string.
        # Leave the rest of the directory name as is, including case.
        # Also do the same for any custom tags here.
        character_name = (character_name.replace('chibi', '')
                  .replace('nsfw', '')
                  .replace('Chibi', '')
                  .replace('Nsfw', '')
                  .replace('CHIBI', '')
                  .replace('NSFW', '')
                  .strip())

        model_version = (model_version.replace('chibi', '')
                  .replace('nsfw', '')
                  .replace('Chibi', '')
                  .replace('Nsfw', '')
                  .replace('CHIBI', '')
                  .replace('NSFW', '')
                  .strip())

        # If the character name has a number at the end, remove it and trim the whitespace.
        # Only do this if it's a single number (for now).
        version = ''
        if character_name[-1].isdigit():
            if character_name[-2].isspace():
                version = character_name[-1]
                character_name = character_name[:-1]


        # Rebuild the directory name as
        # <character_name>_<model_version> <number> - <tags>

        newdir = f"{character_name.strip()}"
        if model_version:
            newdir = f"{newdir.strip()}_{model_version.strip()}"
        if version:
            newdir = f"{newdir.strip()} {version.strip()}"
        if tags:
            newdir = f"{newdir.strip()} - {' '.join(tags)}"

        newdir = newdir.strip()

        newdir = os.path.join(parent_folder, newdir)

        # If the new directory name is the same as the old one, skip it
        if model_dir == newdir:
            unchanged_dirs.append(newdir)
            continue
        else:
            changed_dirs.append({"old": model_dir, "new": newdir})

    # Print the results
    # Sort unchanged_dirs alphabetically
    unchanged_dirs.sort()

    # Convert the set to a list and sort it alphabetically
    invalid_dirs = list(invalid_folders)
    invalid_dirs.sort()

    # Sort changed_dirs alphabetically by old directory name
    changed_dirs.sort(key=lambda x: x['old'])

    print(f"Invalid Directories:")
    for bad_dir in invalid_dirs:
        print(bad_dir)

    print(f"\nUnchanged directories: {len(unchanged_dirs)}")
    for unchanged_dir in unchanged_dirs:
        print(unchanged_dir)

    print(f"\nChanged directories: {len(changed_dirs)}")
    for changed_dir in changed_dirs:
        print(f"{changed_dir['old']} ->")
        print(f"\t{changed_dir['new']}")

    # Rename the directories
    for changed_dir in changed_dirs:
        try:
            # os.rename(changed_dir['old'], changed_dir['new'])
            print(f"Renamed: {changed_dir['old']} -> {changed_dir['new']}")
        except OSError as e:
            print(f"Error renaming {changed_dir['old']}: {e}")


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

        rename_dirs(path)

    except Exception as e:
        print(e)


# Run the main function
if __name__ == '__main__':
    main()
