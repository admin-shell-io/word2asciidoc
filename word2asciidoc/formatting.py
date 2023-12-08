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
        r'\{empty\}',
        r'^.*{blank}$',
        r'^\+$',
    ]

    for regex in regular_exp_list:
        # Remove occurrences of the specified regular expression
        content = re.sub(regex, '', content, flags=re.MULTILINE)
    return content


def replace_text_by_patterns(content):
    content = re.sub(r'\]##.*\nTable', ']##Table', content)
    content = re.sub(r'\]##.*\nFigure', ']##Figure', content)
    content = re.sub(r'&#91;', '[', content)
    content = re.sub(r'&#93;', ']', content)
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


def remove_superfluous_attrs_image_figure_table(content):
    # Remove superfluous and badly named and placed identification
    content = re.sub(r' \.anchor\]', ']', content)

    # Remove superfluous prefixes from Table and Figure names
    # With the form 'Table xx', as these will be generated automatically
    # also split tile into new line with dot
    content = re.sub(r'###*( )*(Figure|Table) [0-9]* ', '\n.', content)
    content = re.sub(r'\](Figure|Table) [0-9]* ', '].', content)
    return content


def convert_image_inline_to_block(content):
    # Convert inline images to dedicated blocks
    content = re.sub(r'image:\.', 'image::.', content)
    return content


def remove_bib_numeration(content):
    if not re.search(r'\[[Bb]ibliography\]', content):
        content = re.sub(
            r'== [Bb]ibliography',
            "[bibliography]\n== Bibliography",
            content)
    return content


def fix_references(content):
    # Fixing references requires identifying them correctly first
    #
    # There are lines in the beginning that describe the cross-references
    # that were in the originating word document that are no longer present
    #
    # e.g. link:#preamble[1 Preamble link:#preamblelink:#bib11[[11\]]]
    #
    # We are to delete these lines for proper document formatting. But before doing so,
    # we need their content to restore the lost hyper references in the
    # document

    # First we want to match this informative lines
    info = re.compile(r'^link:#[_a-zA-Z].*')

    # Then we want to check if a given informative line describes a Figure,
    # Table or Annex reference
    misc_refs = re.compile(r'(Figure|Table|Annex) .*')

    # To check if a given informative line describes a chapter/section
    # reference
    chapter_refs = re.compile(r'([0-9]*\.)*[0-9]* .*')

    # We will modify a dictionary dynamically to store content to be replaced
    replacement_dict = {}

    # Separating the file into lines and loop over them
    # Might be done in other ways but they have the same space time complexity
    for line in content.split('\n'):

        # Check if a line is one of the aforementioned informative lines in the
        # beginning
        if info.match(line):

            # If yes, split using ']' and take the first two elements for
            # values
            repl, val = line.split('[')[0:2:]

            # If the informative line describes a reference for an image,
            # figure, table or annex
            if misc_refs.match(val):
                # The value to be replaced has to be brought in proper form
                val = ' '.join(val.split()[0:2:])
                val = val.strip(".")
                # Intuitively, the replacement value has form of an ascii-doc
                # reference
                repl = f"<<{repl},{val}>>"

                # Matching the value directly might result in problems
                # like matching Figure 45 for the 'Figure 4' part and having
                # a replacement such as the following
                # Figure 45 -> <<{reference_for_figure_4},Figure 4>>5
                #
                # So we have to match the following pattern to be sure the
                # expression has ended
                replacement_dict[val + " "] = repl + " "
                replacement_dict[val + "."] = repl + "."
                replacement_dict[val + ")"] = repl + ")"

            # If the informative line describes a reference for a chapter or
            # section
            elif chapter_refs.match(val):

                # Process is self explanatory analogously to the previous if statement
                # Only there are more possibilities so more entries
                val = val.split()[0]
                repl = f"<<{repl},{val}>>"

                possible_keys = [
                    "Subclause ",
                    "subclause ",
                    "clause ",
                    "Clause "]
                for word in possible_keys:
                    replacement_dict[word + val +
                                     " "] = "Subclause " + repl + " "

                    replacement_dict[word + val +
                                     ". "] = "Subclause " + repl + ". "

                    replacement_dict[word + val +
                                     ") "] = "Subclause " + repl + ") "

                    replacement_dict[word + val +
                                     ".\n"] = "Subclause " + repl + ".\n"

                    replacement_dict[word + val +
                                     ")\n"] = "Subclause " + repl + ")\n"

    # Replace the words with references using the dictionary we generated
    for word, replacement in replacement_dict.items():
        content = content.replace(word, replacement)

    def reference_ordering(match):
        text = match.group(0)
        text = [s.strip(' \n#+')
                for s in text.split('\n') if s.strip(' \n#+') != '']
        text = text[1:] + [text[0]]
        text[-1] = re.sub(r'\]', ']\n\n', text[-1])
        text = '\n' + '\n'.join(text) + '\n'
        return text

    def inline_refs(match):
        text = match.group(0)
        text = [s.strip() for s in text.split('##')]
        text[0], text[-1] = text[-1], text[0]
        text = [re.sub(r'\]', ']\n', elem) for elem in text]
        text = [s.strip() for s in '\n'.join(text).split('\n')]
        text[1] = re.sub(r'.*(Figure|Table) [0-9]* ', '.', text[1])
        text[1], text[2] = text[2], text[1]
        text = '\n' + '\n'.join(text) + '\n'
        return text

    # Some inline references are not even separated from the image description
    # with a new line. We split them, so all previously inline references have
    # a uniform structure. We will then transform them and set the ordering.
    content = re.sub(
        r'\]\[#_Ref',
        '\\]\n\\[#_Ref',
        content)

    content = re.sub(
        r'\]\[#_Toc',
        '\\]\n\\[#_Toc',
        content)

    # Match when '##image' follows the reference id
    # This is was originally an inline image
    # Use the dedicated function to split this line into two lines
    # Fix the unnecessary characters in the process
    # Make sure now the reference block follows the image
    # This may sound counter-intuitive, but everything else has this form
    # We aim to bring inline references into the same form
    # The ordering issue is fixed with the following match
    content = re.sub(
        r'\n(\[#_(Ref|Toc).*\])##image:(.*(\n))',
        inline_refs,
        content)

    # Match when Reference block follows the image itself
    # This is the case for everything by default, which is obviously false
    # After matching we fix the ordering in the dedicated function
    content = re.sub(
        r'\n(=)*( )*(image:.*\])(.*)(\n)+(\[#_(Ref|Toc).*\])(.*(\n))(.*(\n))',
        reference_ordering,
        content)
    return content


def fix_tables_with_appendices(content):
    def split_and_mark(match):
        text = match.group(0)

        # Match the header block that defines the table cell widths and properties
        # e.g. [width="100%",cols="21%,17%,22%,40%",options="header",]
        #
        # We will use the same block to define the second table, that is the appendix
        # After having split the table into two
        table_props_def_block = re.match(r'\[.*\](\n)+', text).group(0)
        text = re.sub(
            r'\[.*\](\n)+',
            f'[.table-with-appendix-table]\n{table_props_def_block}',
            text)

        # Split from the line 'Inherits from'
        text = re.sub(
            r'\n\|Inherits from:.*\|\n',
            f'\n\n{{filler}}\n\\g<0>|===\n{table_props_def_block}\n|===\n',
            text)
        return text

    # Match tables to be split and do due work calling the function
    # split_and_mark
    content = re.sub(
        r'\[.*\](\n)+\|\===\n((\|.*\n)+?)\|Inherits from:.*\|\n',
        split_and_mark,
        content)
    return content


def remove_toc_and_var(content):
    # Remove table of contents, table of tables, table of figures, imprint
    # and similar content at the beginning that are badly formatted, non-necessary,
    # cause duplication and/or are error prone on another level.
    content = re.sub(
        r'\nImprint([\S\n\t\v ]+?)== Preamble',
        '\n== Preamble',
        content)
    return content


def add_doc_attr(content):
    content = ':toc: left\n:toc-title: Contents\n:sectlinks:\n:sectnums:\n:stylesheet: ../../style.css\n:favicon: ../../favicon.png\n:imagesdir: media/\n:nofooter:\n\ninclude::constraints.adoc[]\n\n' + content
    return content
