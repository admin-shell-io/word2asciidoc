import re


def escape_double_angular_brackets(content):
    pattern = r"<<(.*?)>>"
    return re.sub(pattern, r"\<<\1>>", content)


def recolor_notes(content):
    matches = set()

    notes_patterns = [r'(?<!foot)(?<!\[)Note:.*', r'Note\s+\d+.*', r'EXAMPLE\s+\d+:.*', r'Please note:.*']

    for pattern in notes_patterns:
        matches.update(re.findall(pattern, content))

    # Iterate over the matches and modify the figure tags
    for match in matches:
        old_note = match
        # match = re.sub(r'Note:|Note\s+(\d+)(:*)', lambda m: '' if m.group(1) is None else m.group(1)+" :", match)
        match = match.strip()
        content = content.replace(old_note, f'\n====\n{match}\n====\n')

    return content


def remove_lines_between(content, start_line, end_line):
    mod_content = ""
    for i, line in enumerate(content, start=1):
        if i < start_line or i > end_line:
            mod_content = mod_content+line
    return mod_content


def remove_text_matching_regex(content):
    regular_exp_list = [
        r'Table of Contents\n\n(.*?)(?=\n\n==)',
        r'\[#_Toc\d* \.anchor]####Table \d*\:?\s?',
        r'\[#_Ref\d* \.anchor]####Table \d*\:?\s?',
        r'\[\#_Ref\d* \.anchor\](?:\#{2,4})',
        r'\[\#_Toc\d* \.anchor\](?:\#{2,4})',
        r'\{empty\}'
    ]

    for regex in regular_exp_list:
        # Remove occurrences of the specified regular expression
        content = re.sub(regex, '', content)
    return content


def use_block_tag_for_img_and_move_caption_ahead(content):
    # Define the callback function
    def replacement(match):
        # Use block figure tag
        figure_tag: str = match[1]
        figure_tag = figure_tag.replace("image:", "image::")

        # remove "Figure+num" as it will be automatically done in AsciiDoc
        caption: str = match[2]
        caption = re.sub(r'^Figure \d*:?', '', caption)

        # Move the caption to the beginning of the figure tag
        modified_figure_tag = f'.{caption.strip()}\n{figure_tag}\n'

        return modified_figure_tag

    # Define the regular expression pattern to match figure tags with specific captions
    pattern = r'(image:\S+\[.*?\])\s+?\n?\n?(Figure.*?\n)'

    # Replace the original figure tags with the modified ones
    new_content = re.sub(pattern, replacement, content)
    return new_content


def escape_square_brackets(content):
    pattern = r"\[(SOURCE:.*?)\]"
    return re.sub(pattern, r"&#91;\1&#93;", content)


def find_pos_of_bibliography(content):
    # Find the position of "== Bibliography"
    bibliography_pos = content.find("== Bibliography")
    if bibliography_pos == -1:
        print("Bibliography section not found")
    return bibliography_pos


def add_anchor_to_biblio(content):
    bibliography_pos = find_pos_of_bibliography(content)
    if bibliography_pos == -1:
        return content

    # Extract the substring starting from the position of "== Bibliography"
    bibliography_text = content[bibliography_pos:]

    matches = {}

    biblio_pattern = r'^\[(\d+)\](.+)'
    matches.update(re.findall(biblio_pattern, bibliography_text, re.MULTILINE))

    for key in matches.keys():
        biblio_tag = f'[{key}]'
        biblio_tag_mod = f'[{key}]'
        biblio_text = f'{matches.get(key)}'

        # Move the caption to the beginning of the figure tag
        modified_figure_tag = f'[#bib{key}]\n{biblio_tag_mod}{biblio_text}'
        old_figure_tag = f'{biblio_tag}{biblio_text}'

        bibliography_text = bibliography_text.replace(old_figure_tag, modified_figure_tag)

    content = content[:bibliography_pos] + bibliography_text
    return matches.keys(), content


def add_link_to_biblio(content, keys):
    for key in keys:
        in_link_patterns = r'(?<!\[#bib{key}\]\n)\[{key}\]'
        in_link_patterns = in_link_patterns.format(key=key)
        content = re.sub(in_link_patterns, f'link:#bib{key}[[{key}\]]', content)
    return content