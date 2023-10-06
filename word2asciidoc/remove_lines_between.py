def remove_lines_between(content, start_line, end_line):
    mod_content = ""
    for i, line in enumerate(content, start=1):
        if i < start_line or i > end_line:
            mod_content = mod_content+line
    return mod_content
