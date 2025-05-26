# Write the filters to the html file
from utils.file_utils import read_file

# Write the header of the html file
def write_header(f, total_models):
    # Read in all the template files
    css = read_file('./templates/style.css')
    header = read_file('./templates/htmlHeaderTemplate.html')

    # Replace the CSS data in the html template
    header = header.replace('{{style}}', css)
    header = header.replace('{{TotalModels}}', str(total_models))

    f.write(header)

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
    table = read_file('./templates/htmlTableTemplate.html')
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
    script = read_file('./templates/script.js')
    f.write('</tbody></table><script>')
    f.write(script)
    f.write('</script></body></html>')
