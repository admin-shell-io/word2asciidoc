import re

REGULAR_EXP_LIST = [
    r'Table of Contents\n\n(.*?)(?=\n\n==)',
    r'\[#_Toc\d* \.anchor]####Table \d*\:?\s?',
    r'\[#_Ref\d* \.anchor]####Table \d*\:?\s?',
    r'\[\#_Ref\d* \.anchor\](?:\#{2,4})',
    r'\[\#_Toc\d* \.anchor\](?:\#{2,4})',
    r'\{empty\}'
]


def remove_text_matching_regex(content):
    for regex in REGULAR_EXP_LIST:
        # Remove occurrences of the specified regular expression
        content = re.sub(regex, '', content)
    return content
