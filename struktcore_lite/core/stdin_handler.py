import sys

def read_piped_input():
    """
    Returns piped input from stdin, or None if nothing was piped.
    """
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        return data.strip() if data else None
    return None