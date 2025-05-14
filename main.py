# Write a program to go through all subdirectories of a given directory.
# If the directory contains an image, and a folder called 'STL' under it, print the name of the folder.
import argparse
import base64
import os
from io import BytesIO
from pickletools import optimize

from PIL import Image

from search_functions import contains_stl_folder, is_valid_image_file

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

# Method to read files
def read_file(file):
    with open(file, 'r') as f:
        data = f.read()
    return data

# Method to read an image, resize it, and convert it to base64 to embed in the html file
def get_image_base64_data(file, max_height=200):

    # Check if a file named 'file.resized.jpg' exists
    # Remove the extension from the file name
    # Check to make sure there's not more than one '.' in the file name
    file_parts = file.split('.')
    if len(file_parts) > 2:
        file_name = '.'.join(file_parts[:-1])
    else:
        file_name = file_parts[0]

    # Add the resized file extension
    resized_file = file_name + '.resized.jpg'

    if os.path.exists(resized_file):
        # If it does, return the base64 data from that file
        # This is to prevent resizing the same image multiple times
        with open(resized_file, 'rb') as f:
            img_str = base64.b64encode(f.read()).decode('utf-8')
        return img_str

    with Image.open(file) as img:
        # Resize the image to a max height of 200px
        # Calculate the new size while maintaining aspect ratio
        aspect_ratio = img.width / img.height
        new_height = min(max_height, img.height)
        new_width = int(new_height * aspect_ratio)

        # Resize the image
        resized_img = img.resize((new_width, new_height))
        resized_img = resized_img.convert('RGB')

        buffered = BytesIO()
        resized_img.save(buffered, format="JPEG", quality=60, optimize=True)
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Save the resized image to a file
        with open(resized_file, 'wb') as f:
            f.write(buffered.getvalue())
    return img_str


# Write the header of the html file
def write_header(f, total_models):

    # Read in all the template files
    css = read_file('style.css')
    header = read_file('htmlHeaderTemplate.html')

    # Replace the CSS data in the html template
    header = header.replace('{{style}}', css)
    header = header.replace('{{TotalModels}}', str(total_models))

    f.write(header)

# Write the filters to the html file
def write_filters(f, all_tags):
    # Write the filters to the html file
    for tag in all_tags:
        if tag != '':

            f.write(f'<div>'
                    
                    f'<label id={tag}-count type="count" value="{tag}">'
                    f'</label>'
    
                    f'<label>'
                    f'<input type="radio" name="{tag}" value="include" checked onclick="filterTable()">'
                    f'Include {tag}'
                    f'</label>'
    
                    f'<label>'
                    f'<input type="radio" name="{tag}" value="only" onclick="filterTable()">'
                    f'Only {tag}'
                    f'</label>'
    
                    f'<label>'
                    f'<input type="radio" name="{tag}" value="exclude" onclick="filterTable()">'
                    f'Exclude {tag}'
                    f'</label>'
    
                    f'</div>')

# Write the table to the html file
def write_table(f, models, custom_tags):
    table = read_file('htmlTableTemplate.html')
    f.write(table)

    # Write the table rows to the html file
    for model in models:
        # Check if the model has any of the custom tags in the model name
        if custom_tags:
            for tag in custom_tags:
                if tag.lower() in model['model_name'].lower():
                    # If the model tags don't contain the custom tag, add it to the model tags
                    if tag not in model['tags']:
                        if model['tags'] == '':
                            model['tags'] += tag
                        else:
                            model['tags'] += ', ' + tag

        f.write(f'<tr>'
                f'<td>{model["character_name"]}</td>'
                f'<td>{model["model_name"]}</td>'
                f'<td>{model["series_name"]}</td>'
                f'<td>{model["category"]}</td>'
                f'<td>{model["tags"]}</td>'
                f'<td><img loading="lazy" src="data:image/jpeg;base64,{model["image_base64_data"]}" /></td>'
                f'</tr>')

# Write the closing tags to the html file
def write_close(f):
    script = read_file('script.js')
    f.write('</tbody></table><script>')
    f.write(script)
    f.write('</script></body></html>')

# Method to generate the html file from the directory structure
def gen_from_directory_structure(path):
    total_models = 0
    models = []
    all_tags = []

    # Get the last folder name in the path
    folder_name = os.path.basename(path)

    for root, dirs, files in os.walk(path):
        for file in files:
            if is_valid_image_file(os.path.join(root, file)):
                if contains_stl_folder(root):
                    # Break the path up into tokens separated by '/'
                    tokens = root.split('\\')

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
                        print("Splitting model tags")
                        model_tags = model_tags.split(' ')
                        for tag in model_tags:
                            if tag == '2B':
                                print(root)
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

                    # Get the image base64 data
                    image_base64_data = get_image_base64_data(os.path.join(root, file))

                    for tag in tags:
                        if tag not in all_tags:
                            all_tags.append(tag)

                    # Write the output to the html file
                    # Embed the image data in the html file as a base64 string
                    model = {
                        'character_name': character_name,
                        'model_name': model_name,
                        'series_name': series_name,
                        'category': category,
                        'tags': ", ".join(tags),
                        'image_base64_data': image_base64_data
                    }
                    models.append(model)

                    total_models += 1
                    break

    return total_models, models, all_tags

# Method to generate the html file from the model-info.txt file
def gen_from_model_info_file(file_path):
    total_models = 0
    models = []
    all_tags = []

    # Starting at the base directory, find all files named 'model-info.txt'
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file == 'model-info.txt':
                # Parse the model info from the file
                model_info = parse_model_info(os.path.join(root, file))

                # Check the directory for an image file
                # Name could be anything, so check each file in the directory
                image_found = False

                for image_file in os.listdir(root):
                    if image_found:
                        continue
                    if not is_valid_image_file(os.path.join(root, image_file)):
                        continue

                    image_found = True
                    image_base64_data = get_image_base64_data(os.path.join(root, image_file))

                    # Add the tags to the all_tags list
                    for tag in model_info['Tags']:
                        if tag not in all_tags and tag != '':
                            if tag == '2':
                                print(root)
                            all_tags.append(tag)

                    # Write the output to the html file
                    # Embed the image data in the html file as a base64 string
                    model = {
                        'character_name': model_info['Character Name'],
                        'model_name': model_info['Model Name'],
                        'series_name': model_info['Series'],
                        'category': model_info['Model Category'],
                        'tags': ", ".join(model_info['Tags']),
                        'image_base64_data': image_base64_data
                    }
                    models.append(model)
                    total_models += 1


    return total_models, models, all_tags


# Main function
def main():
    try:
        # Create the argument parser
        parser = argparse.ArgumentParser(description="Model Info Program")

        # Add a flag for using model-info.txt
        parser.add_argument('path', type=str, help="Path to the root models directory")
        parser.add_argument('--use-model-info', action='store_true', help="Use model-info.txt file")
        parser.add_argument('--custom-tags', type=str, help="Comma separated list of custom tags")

        # Parse the arguments
        args = parser.parse_args()

        path = args.path
        # Make sure the path is a directory
        if not os.path.isdir(path):
            print('Invalid path')
            return

        # Parse the custom tags
        if args.custom_tags:
            custom_tags = args.custom_tags.split(',')
        else:
            custom_tags = []


        # Create an html file to write the output to
        # Embed the CSS data in the html file
        with open('output.html', 'w') as f:

            # Check if the flag is triggered
            if args.use_model_info:
                print("Using model-info.txt...")
                total_models, models, all_tags = gen_from_model_info_file(path)
            else:
                print("Flag not triggered, no model-info.txt used.")
                total_models, models, all_tags = gen_from_directory_structure(path)

            print('Total Models:', total_models)
            print('All Tags Found:', all_tags)

            print('Writing to html file...')

            # Write the header of the html file
            write_header(f, total_models)

            # Write the filters to the html file

            # If custom tags are provided, include them in the filters
            if custom_tags:
                for tag in custom_tags:
                    if tag not in all_tags:
                        all_tags.append(tag)

            write_filters(f, all_tags)

            # Write the table to the html file
            write_table(f, models, custom_tags)

            # Write the closing tags to the html file
            write_close(f)

            print('Done!')
            print(f'Total Models: {total_models}')
    except Exception as e:
        print(e)


# Run the main function
if __name__ == '__main__':
    main()
