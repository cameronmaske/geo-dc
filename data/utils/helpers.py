import re

def get_index(x, index):
    """
    Get the element at the index of the list or return None
    >>> example = [1, 2]
    >>> get_index(example, 1)
    1
    >>> get_index(example, 7)
    None
    """
    if len(x) > index:
        return x[index]

def clean_string(string):
    """
    Cleans up a string to strip out nasty things like newlines, excess spaces
    Far from prefect at the moment, but gets 80% of the way there.
    """
    # Replace all newlines with spaces.
    string = string.replace('\n', '')
    # Remove duplicate spaces.
    string = " ".join(string.split())
    # Remove leading and ending spaces.
    return string.strip().encode('utf-8')

def extract_digits(string):
    """
    Attempts to extract and returns numbers from a string.
    >>> example = "cost is $100"
    >>> extract_digits(example)
    100
    """
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

def data_attribute(soup, attr):
    """
    Used to find elements by data attributes in soups and return their value
    >>> html = <div data-value="key"></div>
    >>> soup = BeautifulSoup(html)
    >>> data_attribute(soup, "key")
    value
    """
    element = soup.find(attrs={attr: re.compile('')})
    if element:
        return element.get(attr)
    else:
        return None
