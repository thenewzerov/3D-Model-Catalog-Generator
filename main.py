import argparse
import os

from utils.file_utils import print_model_info, create_model_info, parse_model_info
from utils.html_utils import write_close, write_table, write_filters, write_header
from utils.image_utils import get_image_base64_data
from utils.search_utils import is_valid_image_file, contains_stl_folder


def extract_model_info_from_directory(path, folder_name):
    """
    Extracts model information from a directory structure.

    Args:
        path (str): The path to the model directory.
        folder_name (str): The name of the root folder.

    Returns:
        dict: A dictionary containing model information.
    """
    tokens = path.split('\\')
    category = ''

    for i in range(len(tokens)):
        if tokens[i] == folder_name:
            category = tokens[i + 1]
            break

    series_name = tokens[-2]
    model_name = tokens[-1]
    character_name = tokens[-1]
    tags = []

    if ' - ' in character_name:
        model_tags = character_name.split(' - ')[1].strip()
        character_name = character_name.split(' - ')[0].strip()
        model_name = character_name
        model_tags = model_tags.split(' ')
        tags.extend(model_tags)

    if character_name[-1].isdigit() and character_name[-2] == ' ':
        character_name = character_name[:-1]

    if '_' in character_name:
        model_name = character_name.split('_')[1].strip()
        character_name = character_name.split('_')[0].strip()
        model_name = character_name + ' - ' + model_name

    return {
        'file_path': path,
        'model_name': model_name,
        'character_name': character_name,
        'series': series_name,
        'tags': tags,
        'model_category': category
    }


def gen_from_directory_structure(path, create_model_info_files=False):
    total_models = 0
    models = []
    all_tags = []
    folder_name = os.path.basename(path)

    for root, dirs, files in os.walk(path):
        for file in files:
            if is_valid_image_file(os.path.join(root, file)) and contains_stl_folder(root):
                model_info = extract_model_info_from_directory(root, folder_name)
                image_base64_data = get_image_base64_data(os.path.join(root, file))

                for tag in model_info['tags']:
                    if tag not in all_tags:
                        all_tags.append(tag)

                if create_model_info_files:
                    print_model_info(**model_info)
                    create_model_info(
                        file_path=os.path.join(root, 'model-info.txt'),
                        model_name=model_info['model_name'],
                        character_name=model_info['character_name'],
                        series=model_info['series'],
                        tags=model_info['tags'],
                        model_category=model_info['model_category']
                    )

                model = {
                    'character_name': model_info['character_name'],
                    'model_name': model_info['model_name'],
                    'series_name': model_info['series'],
                    'category': model_info['model_category'],
                    'tags': ", ".join(model_info['tags']),
                    'image_base64_data': image_base64_data
                }
                models.append(model)
                total_models += 1
                break

    return total_models, models, all_tags


def gen_from_model_info_file(file_path):
    total_models = 0
    models = []
    all_tags = []

    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file == 'model-info.txt':
                model_info = parse_model_info(os.path.join(root, file))
                image_found = False

                for image_file in os.listdir(root):
                    if image_found:
                        continue
                    if not is_valid_image_file(os.path.join(root, image_file)):
                        continue

                    image_found = True
                    image_base64_data = get_image_base64_data(os.path.join(root, image_file))

                    for tag in model_info['Tags']:
                        if tag not in all_tags and tag != '':
                            all_tags.append(tag)

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


def main():
    try:
        parser = argparse.ArgumentParser(description="Model Info Program")
        parser.add_argument('path', type=str, help="Path to the root models directory")
        parser.add_argument('--custom-tags', type=str, help="Comma separated list of custom tags")
        parser.add_argument('--create-model-info', action='store_true',
                            help="Create model-info.txt files in each model directory")
        parser.add_argument('--use-model-info', action='store_true', help="Use model-info.txt file")

        args = parser.parse_args()
        path = args.path

        if not os.path.isdir(path):
            print('Invalid path')
            return

        custom_tags = args.custom_tags.split(',') if args.custom_tags else []

        with open('output.html', 'w') as f:
            if args.use_model_info:
                total_models, models, all_tags = gen_from_model_info_file(path)
            else:
                total_models, models, all_tags = gen_from_directory_structure(path,
                                                                               args.create_model_info)

            print('Total Models:', total_models)
            print('All Tags Found:', all_tags)
            print('Writing to html file...')

            write_header(f, total_models)

            if custom_tags:
                for tag in custom_tags:
                    if tag not in all_tags:
                        all_tags.append(tag)

            write_filters(f, all_tags)
            write_table(f, models, custom_tags)
            write_close(f)

            print('Done!')
            print(f'Total Models: {total_models}')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()