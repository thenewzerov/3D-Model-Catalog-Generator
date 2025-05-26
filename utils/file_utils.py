import os


def find_stl_folders(path):
    stl_folders = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".stl"):
                stl_folders.append(root)
                break  # Stop searching the current folder after finding one STL file
    return stl_folders

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


# Read the model info from the model-info.txt file
def parse_model_info(file_path):
    """Parse model-info.txt file and return a dictionary with model details."""
    model_info = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line at the first colon to get key and value
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()  # Remove any extra spaces from the key
                    value = value.strip()  # Remove any extra spaces from the value

                    # Add the parsed data to the dictionary
                    if key == 'Tags':
                        # Split tags by comma and strip spaces
                        model_info[key] = [tag.strip() for tag in value.split(',')]
                    else:
                        model_info[key] = value
    except FileNotFoundError:
        print(f"File {file_path} not found.")

    return model_info