import re


def read_keywords_from_file(filename):
    keyword_names = []

    with open(filename, 'r') as file:
        for line in file:
            class_name = line.strip()
            keyword_names.append(class_name)

    return keyword_names


def replace_quotes_on_keyword(content):
    for keyword in KEYWORD_LIST:
        replacement = '`{}`'
        pattern = re.compile(r'\"' + re.escape(keyword) + r'\"', re.IGNORECASE)
        content = pattern.sub(replacement.format(keyword), content)

    return content


KEYWORD_LIST = read_keywords_from_file("keyword.txt")
