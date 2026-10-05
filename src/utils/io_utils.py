def add_line_to_file(file_path: str, line_content: str, flush=False):
    """
    Append a line of text to a file.
    Create the file if it does not exist.

    :param file_path: Full path to the target file.
    :param line_content: The text string to write.
    """
    with open(file_path, "a", encoding="utf-8") as file:
        if not line_content.endswith("\n"):         # ensure new line ends with '\n'
            line_content += "\n"
        file.write(line_content)
        if flush:
            file.flush()

def read_file_lines(file_path: str, encoding="utf-8"):
    with open(file_path, "r", encoding=encoding) as file:
        lines = file.readlines()
    return lines


def read_last_line(file_path, encoding="utf-8"):
    content = read_file_lines(file_path, encoding=encoding)
    return content[-1] if content else None

def count_file_lines(file_path, encoding="utf-8"):
    content = read_file_lines(file_path, encoding=encoding)
    lines_number = content.count("\n") + 1 if content else 0
    return lines_number