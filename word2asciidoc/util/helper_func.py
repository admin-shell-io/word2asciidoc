def read_file(filename: str):
    with open(filename, 'r', encoding="utf-8") as file:
        content = file.readlines()
    return content


def write_file(filename: str, content):
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(content)
