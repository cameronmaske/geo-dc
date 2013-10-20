import re
import logging

def get_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

def get_index(x, index):
    if len(x) > index:
        return x[index]

def clean_string(string):
    # Replace all newlines with spaces.
    string = string.replace('\n', '')
    # Remove duplicate spaces.
    string = " ".join(string.split())
    # Remove leading and ending spaces.
    return string.strip().encode('utf-8')

def extract_digits(string):
    string = string.replace(',', '')
    # Find the first digits in a string.
    matchs = re.findall('\d+', string)
    # Get the first or none.
    match = get_index(matchs, 0)
    if match:
        return int(match)

def truncate_string(string, length, end_text="..."):
    """
    Simple helper function to help truncate long strings
    >>> truncate_string("A long string", 6)
        "A l..."
    """
    if string and len(string) > length:
        return string[:length - len(end_text)] + end_text
    else:
        return string
