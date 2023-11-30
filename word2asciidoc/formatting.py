import logging
import re


def escape_double_angle_brackets(content):
    pattern = r"<<(.*?)>>"
    return re.sub(pattern, r"\<<\1>>", content)


def recolor_notes(content):
    notes_patterns = [
        re.compile(r'(?<!foot)(?<!\[)Note:.*'),
        re.compile(r'Note\s+\d+.*'),
        re.compile(r'EXAMPLE\s+\d+:.*'),
        re.compile(r'Please note:.*')
    ]

    matches = set()
    for pattern in notes_patterns:
        matches.update(re.findall(pattern, content))

    # Iterate over the matches and modify the figure tags
    for match in matches:
        content = content.replace(match, f'\n====\n{match.strip()}\n====\n')

    return content


def remove_lines(content, start_line, end_line):
    lines = content.splitlines()
    lines_to_keep = lines[:start_line - 1] + lines[end_line:]
    return '\n'.join(lines_to_keep)


def remove_text_by_patterns(content):
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


def escape_source_square_brackets(content):
    pattern = r"\[(SOURCE:.*?)\]"
    return re.sub(pattern, r"&#91;\1&#93;", content)


def find_bibliography_section(content):
    # Find the position of "== Bibliography"
    bibliography_pos = content.find("== Bibliography")
    if bibliography_pos == -1:
        logging.warning("Bibliography section not found")
        return None
    return bibliography_pos


def add_anchors_to_bibliography(content):
    bibliography_pos = find_bibliography_section(content)
    if bibliography_pos is None:
        return {}, content

    # Extract the substring starting from the position of "== Bibliography"
    bibliography_text = content[bibliography_pos:]
    biblio_pattern = re.compile(r'^\[(\d+)\](.+)', re.MULTILINE)

    matches = {key: val for key, val in biblio_pattern.findall(bibliography_text)}

    for biblio_tag_num, biblio_tag_text in matches.items():
        anchor = f'[#bib{biblio_tag_num}]'
        modified_text = f'{anchor}\n[{biblio_tag_num}]{biblio_tag_text}'
        bibliography_text = bibliography_text.replace(f'[{biblio_tag_num}]{biblio_tag_text}', modified_text)

    content = content[:bibliography_pos] + bibliography_text
    return matches.keys(), content


def add_links_to_bibliography(content, keys):
    for key in keys:
        in_link_patterns = r'(?<!\[#bib{key}\]\n)\[{key}\]'
        in_link_patterns = in_link_patterns.format(key=key)
        content = re.sub(in_link_patterns, f'link:#bib{key}[[{key}\]]', content)
    return content
    
    
def image_inline_to_block(content):
    content = re.sub(r'image:.', r'image::.', content)
    return content
    
    
def remove_bib_numeration(content):
    if not re.search(r'\[[Bb]ibliography\]', content):
        content = re.sub(r'== [Bb]ibliography', "[bibliography]\n== Bibliography", content)
    return content
