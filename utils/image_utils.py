# Method to read an image, resize it, and convert it to base64 to embed in the html file
import base64
import os
from io import BytesIO

from PIL import Image


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
