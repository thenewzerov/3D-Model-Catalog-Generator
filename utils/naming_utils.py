def extract_tags(dirname):
    tags = []
    if 'chibi' in dirname.lower():
        tags.append('Chibi')
    if 'nsfw' in dirname.lower():
        tags.append('NSFW')
    return tags

def clean_name(name):
    return (name.replace('chibi', '').replace('nsfw', '')
                .replace('Chibi', '').replace('Nsfw', '')
                .replace('CHIBI', '').replace('NSFW', '').strip())

def split_character_and_version(dirname):
    if ' - ' in dirname:
        return dirname.split(' - ')
    return dirname, ''