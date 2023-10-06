import re

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
