# Write a program to go through all subdirectories of a given directory.
# If the directory contains an image, and a folder called 'STL' under it, print the name of the folder.
import base64
import os
import sys
from ctypes.wintypes import tagSIZE
from io import BytesIO

from PIL import Image


# Read in a CSS file and minify it.  Return the minified CSS.
def read_file(file):
    with open(file, 'r') as f:
        data = f.read()
    return data


def check_image(file):
    try:
        # Skip the file if it does not have an image extension
        if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', 'webp', 'svg')):
            return False
        Image.open(file)
        return True
    except:
        return False


def check_stl(folder):
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


def get_image_base64_data(file, max_height=200):
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
        resized_img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str


def main():
    try:
        css = read_file('style.css')
        header = read_file('htmlHeaderTemplate.html')
        table = read_file('htmlTableTemplate.html')
        script = read_file('script.js')

        # Replace the CSS data in the html template
        header = header.replace('{{style}}', css)

        # Create an html file to write the output to
        # Embed the CSS data in the html file
        with open('output.html', 'w') as f:

            f.write(header)

            # Read the folder as the first argument
            path = sys.argv[1]
            total_models = 0
            models = []
            all_tags = []

            # Make sure the path is a directory
            if not os.path.isdir(path):
                print('Invalid path')
                return

            # Get the last folder name in the path
            folder_name = os.path.basename(path)

            for root, dirs, files in os.walk(path):
                for file in files:
                    if check_image(os.path.join(root, file)):
                        if check_stl(root):
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
                                model_name = character_name + ' - ' +  model_name.strip()

                            else:
                                character_name = character_name.strip()

                            # Print the Model info.
                            print(f'Path: {root}')
                            print(f'\tSeries Name: {series_name}')
                            print(f'\tModel Name: {model_name}')
                            print(f'\tCategory: {category}')
                            print(f'\tCharacter Name: {character_name}')
                            print(f'\tTags: {tags}')

                            # Print the image file path
                            print(f'\tImage File: {os.path.join(root, file)}')

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

            # Write the filters to the html file
            for tag in all_tags:
                f.write(f'<div>'
                
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


            f.write(table)

            # Write the table rows to the html file
            for model in models:
                f.write(f'<tr>'
                        f'<td>{model["character_name"]}</td>'
                        f'<td>{model["model_name"]}</td>'
                        f'<td>{model["series_name"]}</td>'
                        f'<td>{model["category"]}</td>'
                        f'<td>{model["tags"]}</td>'
                        f'<td><img src="data:image/jpeg;base64,{model["image_base64_data"]}" /></td>'
                        f'</tr>')


            f.write('</tbody></table><script>')
            f.write(script)
            f.write('</script></body></html>')
            print('Done!')
            print(f'Total Models: {total_models}')
    except Exception as e:
        print(e)


# Run the main function
if __name__ == '__main__':
    main()
