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
        r'\{empty\}'
    ]

    for regex in regular_exp_list:
        # Remove occurrences of the specified regular expression
        content = re.sub(regex, '', content)
    return content


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

    matches = {
        key: val for key,
        val in biblio_pattern.findall(bibliography_text)}

    for biblio_tag_num, biblio_tag_text in matches.items():
        anchor = f'[#bib{biblio_tag_num}]'
        modified_text = f'{anchor}\n[{biblio_tag_num}]{biblio_tag_text}'
        bibliography_text = bibliography_text.replace(
            f'[{biblio_tag_num}]{biblio_tag_text}', modified_text)

    content = content[:bibliography_pos] + bibliography_text
    return matches.keys(), content


def add_links_to_bibliography(content, keys):
    for key in keys:
        in_link_patterns = r'(?<!\[#bib{key}\]\n)\[{key}\]'
        in_link_patterns = in_link_patterns.format(key=key)
        content = re.sub(
            in_link_patterns,
            f'link:#bib{key}[[{key}\\]]',
            content)
    return content


def image_figure_and_table_fix(content):
    content = re.sub(r'\n.*{blank}\n', '\n', content)
    content = re.sub(r'\n\+\n', '\n', content)
    content = re.sub(r' \.anchor\]', ']', content)
    content = re.sub(r'image:\.', 'image::.', content)
    content = re.sub(r'###*( )*(Figure|Table) [0-9]* ', '\n.', content)
    return content


def remove_bib_numeration(content):
    if not re.search(r'\[[Bb]ibliography\]', content):
        content = re.sub(
            r'== [Bb]ibliography',
            "[bibliography]\n== Bibliography",
            content)
    return content


def fix_references(content):
    info = re.compile(r'^link:#[_a-zA-Z].*')
    misc_refs = re.compile(r'(Figure|Table|Annex) [#_a-zA-Z0-9].*')
    chapter_refs = re.compile(r'([0-9]*\.)*[0-9]* [#_a-zA-Z0-9].*')
    replacement_dict = {}
    for line in content.split('\n'):
        if info.match(line):
            replacement_dict['\n' + line + '\n'] = ""
            repl, val = line.split('[')[0:2:]
            if misc_refs.match(val):
                val = ' '.join(val.split()[0:2:])
                repl = f"<<{repl},{val}>>"
                replacement_dict[" " + val + " "] = repl
                replacement_dict[" " + val + ". "] = repl
                replacement_dict[" " + val + ") "] = repl
            elif chapter_refs.match(val):
                val = val.split()[0]
                repl = f"<<{repl},{val}>>"
                replacement_dict["Subclause " + val +
                                 " "] = "Subclause " + val + " "
                replacement_dict["subclause " + val +
                                 " "] = "subclause " + val + " "
                replacement_dict["clause " + val + " "] = "clause " + val + " "
                replacement_dict["Clause " + val + " "] = "Clause " + val + " "
                replacement_dict["Subclause " + val +
                                 ". "] = "Subclause " + val + ". "
                replacement_dict["subclause " + val +
                                 ". "] = "subclause " + val + ". "
                replacement_dict["clause " + val +
                                 ". "] = "clause " + val + ". "
                replacement_dict["Clause " + val +
                                 ". "] = "Clause " + val + ". "
                replacement_dict["Subclause " + val +
                                 ") "] = "Subclause " + val + ") "
                replacement_dict["subclause " + val +
                                 ") "] = "subclause " + val + ") "
                replacement_dict["clause " + val +
                                 ") "] = "clause " + val + ") "
                replacement_dict["Clause " + val +
                                 ") "] = "Clause " + val + ") "

    for word, replacement in replacement_dict.items():
        content = content.replace(word, replacement)

    def repl_1(match):
        text = match.group(0)
        text = [s.strip(' \n#+')
                for s in text.split('\n') if s.strip(' \n#+') != '']
        text = text[1:] + [text[0]]
        text[-1] = re.sub(r'\]', ']\n\n', text[-1])
        text = '\n'.join(text)

        return text

    def repl_2(match):
        text = match.group(0)
        text = [s.strip() for s in text.split('##')]
        text[0], text[-1] = text[-1], text[0]
        text = [re.sub(r'\]', ']\n', elem) for elem in text]
        text = [s.strip() for s in '\n'.join(text).split('\n')]
        text[1] = re.sub(r'.*(Figure|Table) [0-9]* ', '.', text[1])
        text[1], text[2] = text[2], text[1]
        text = '\n' + '\n'.join(text) + '\n'
        return text

    content = re.sub(r'\n(\[#_(Ref|Toc).*\])##image:(.*(\n))', repl_2, content)
    content = re.sub(
        r'\n(=)*( )*(image:.*\])(.*)(\n)+(\[#_(Ref|Toc).*\])(.*(\n))(.*(\n))',
        repl_1,
        content)
    return content


def fix_tables_with_appendices(content):
    def repl(match):
        text = match.group(0)
        text = re.sub(
            r'\[.*\](\n)+',
            '[.table-with-appendix-table]\n[cols=\"25%h,75%\"]',
            text)
        text = re.sub(
            r'\n\|Inherits from:.*\|\n',
            '\n\n{filler}\n\\g<0>|===\n[cols=\"25%,40%,25%,10%\",options=\"header\"]\n|===\n',
            text)
        return text
    content = re.sub(
        r'\[.*\](\n)+\|\===\n((\|.*\n)+?)\|Inherits from:.*\|\n',
        repl,
        content)
    return content


def remove_toc_and_add_doc_attr(content):
    content = re.sub(
        r'\nImprint((\|.*\n)+?)== Preamble',
        '== Preamble',
        content)
    content = ':toc: left\n:toc-title: Contents\n:sectlinks:\n:sectnums:\n:stylesheet: ../../style.css\n:favicon: ../../favicon.png\n:imagesdir: media/\n:nofooter:\n\ninclude::constraints.adoc[]\n\n' + content
    return content
