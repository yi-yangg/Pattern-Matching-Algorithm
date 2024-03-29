def read_file(file_path: str) -> str:
    """
    Given a file path read the contents of a file

    Parameters:
    file_path (str): file path to read the files at

    Returns:
    str: Contents of the file
    """
    f = open(file_path, 'r')
    text = f.read()
    f.close()

    return text


def write_file(file_path: str, content: str) -> None:
    """
    Given file path and the content, write content to the file

    Parameters:
    file_path (str): file path to write the files to
    content (str): Content to write into the file
    """
    f = open(file_path, "w")
    f.write(content)
    f.close()
