import re


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
