import argparse
import os


def find_by_directory_property(path):
    dirs_with_bust = []

    # Find all directories that have the word 'bust' in the name
    for root, dirs, files in os.walk(path):
        for d in dirs:
            if 'bust' in d.lower() and d.lower() != 'bust':
                dirs_with_bust.append(os.path.join(root, d))

    # Find all directories that have a folder called 'bust' with files in it.
    for root, dirs, files in os.walk(path):
        for d in dirs:
            if 'bust' in d.lower():
                bust_dir = os.path.join(root, d)
                bust_files = os.listdir(bust_dir)
                if len(bust_files) > 1:

                    # Make sure the directory doesn't only contain a 'desktop.ini' file
                    if len(bust_files) == 1 and bust_files[0].lower() == 'desktop.ini':
                        continue

                    dirs_with_bust.append(bust_dir)

    # Find all zip files with the name 'bust' in them
    for root, dirs, files in os.walk(path):
        for f in files:
            if 'bust' in f.lower() and f.endswith('.zip'):
                dirs_with_bust.append(os.path.join(root, f))

    # Remove duplicates
    dirs_with_bust = list(set(dirs_with_bust))

    # Sort the list
    dirs_with_bust.sort()

    # Print the directories
    for d in dirs_with_bust:
        print(d)

    print(f"\nFound {len(dirs_with_bust)} directories with 'bust' in the name.")

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

        find_by_directory_property(path)

    except Exception as e:
        print(e)


# Run the main function
if __name__ == '__main__':
    main()