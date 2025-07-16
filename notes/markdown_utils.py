"""
Helper functions for working with markdown text
"""

import re

def format_kebab_case(value: str) -> str: 
    """
    Formats a string into kebab case

    Kebab case uses hyphens `-` instead of spaces and is in all lowercase. 
    Kebab case is required for property names and tags.

    Arguments:
        value: The string to be formatted into kebab case

    Returns:
        A string in kebab case
    """
    formatted_value = str(value).strip().lower().replace(' ', '-')
    
    # ':' is an illegal character in property names and tags
    # it is often used in tags to create subtags or nested tags
    # in obsidian, the character used to create nested tags is '/'
    formatted_value = formatted_value.replace(':', '/')
    
    return formatted_value


def format_property_list_item(item: str, is_tags: bool=False) -> str: 
    """
    Formats a string as an individual item in a list type property in YAML 
    notation

    Arguments:
        item: The string to be formatted as a list item. The item can be passed
            with or without the list marker (`-`, a hyphen), double quotes, or
            hashtags (if a tag); all the YAML notation will be cleaned up
        is_tags: Set to `True` if the item is should be formatted as a tag

    Returns:
        A string formatted according to the following YAML rules
        - The basic format for a list item is: `'  - item\\n'` (line break, 2 
          spaces, 1 hyphen, 1 space, and then the item)
        - If the item is an internal link, it is wrapped in double quotes,
          `'  - "[[item]]"\\n'`
        - If the item is a tag, it is formatted with a hashtag wrapped in 
          double quotes and is changed to kebab case, `'  - "#item"\\n'`

    Examples:
        - `In progress` (a tag) --> `'  - "#in-progress"\\n'`
        - `[[Survivor US S48]]` --> `'  - "[[Survivor US S48]]"\\n'`
    """
    list_template = '  - {}\n'
    formatted_item = ''
    cleaned_item = str(item).strip().lstrip('-').strip().replace('"', '')
    
    if is_tags:
        formatted_item = format_kebab_case(cleaned_item)
        if formatted_item.startswith('#'): 
            formatted_item = '"{}"'.format(formatted_item)
        else: 
            formatted_item = '"#{}"'.format(formatted_item)

    else:
        # properties other than tags may contain internal links, which must be 
        # wrapped in double quotes
        if cleaned_item.startswith('[[') and cleaned_item.endswith(']]'): 
            formatted_item = '"{}"'.format(cleaned_item)
        else:
            formatted_item = cleaned_item

    formatted_item = list_template.format(formatted_item)

    return formatted_item


def format_property_list(prop_value: list[str], is_tags: bool=False) -> list[str]:
    """
    Formats the value of a list type property in YAML notation

    For more details on formatting rules, please see the function 
    `format_property_list_item()`

    Arguments:
        prop_value: The value to be formatted as a list in YAML
        is_tags: Set to `True` if the item is should be formatted as a tag

    Returns:
        A list of strings in the format of `['  - item 1\\n', '  - item 2\\n']`
    """
    formatted_prop_value = []
    
    for item in prop_value:
        formatted_item = format_property_list_item(item=item, is_tags=is_tags)
        formatted_prop_value.append(formatted_item)
    
    return formatted_prop_value


def format_property_string(prop_value: any) -> str:
    """
    Formats a single-line property value in YAML notation

    For all property data types besides list (text, list, number, checkbox 
    (boolean), and date), the property value will be converted to a string. 
    Internal links will be wrapped in double quotes as is required in YAML. 
    List type properties should use the `format_property_list()` function 
    instead

    Arguments:
        prop_value: The value to be formatted in YAML
    
    Returns:
        A string to be used as a property value
    
    Examples:
        - `[[Link]]` --> `'"[[Link]]"'`
        - `True` --> `'true'`
        - `2025-03-05 ` --> `'2025-03-05'`
        - `3` --> `'3'`
    """
    formatted_prop_value = str(prop_value).strip()

    # internal links must be wrapped in double quotes
    if (formatted_prop_value.startswith('[[') 
        and formatted_prop_value.endswith(']]')): 
        formatted_prop_value = '"{}"'.format(formatted_prop_value)

    # boolean aka checkbox property type
    elif formatted_prop_value == ('True' or 'False'):
        formatted_prop_value = formatted_prop_value.lower()
    
    return formatted_prop_value


def write_frontmatter(prop_name: str, prop_value: str | list[str]) -> list[str]:
    """
    Write a property and its value to lines of frontmatter in YAML notation

    This function assumes the property names and values are already formatted 
    properly for YAML frontmatter. Use the `format_property_string()` and 
    `format_property_list()` (for property values), and `format_kebab_case()` 
    (for property names) functions first 
    
    Arguments:
        prop_name: Name of the property. Should be in kebab case
        prop_value: Value of the property. If str, the value is a single line; 
            if list, the value is multiple lines. Should be in YAML format

    Returns:
        A list of strings, where each string is a line of frontmatter

    Example:
        ```
        ['date-created: 2025-03-01\\n']
        ['media:\\n', '  - "[[Survivor US]]"\\n', '  - "[[Survivor US S48]]"\\n']
        ```
    """
    prop_single_line = '{prop_name}: {prop_value}\n'
    prop_multi_line = '{prop_name}:\n'

    if type(prop_value) == list: 
        frontmatter_lines = ([prop_multi_line.format(prop_name=prop_name)] 
                             + prop_value)
    else:
        frontmatter_lines = [prop_single_line.format(prop_name=prop_name, 
                                                     prop_value=prop_value)]
    
    return frontmatter_lines


def legalize_filename(filename: str) -> str: 
    """
    Convert a string into a valid filename by replacing characters not allowed
    in filenames in macOS
    
    Illegal characters are ... and converted to...: 
    - `\\` --> ` ` (space)
    - `/` --> ` ` (space)
    - `:` --> ` -` (space hyphen)

    Arguments:
        filename: The string that represents the name of a file
    
    Returns:
        A string with illegal characters replaced
    """
    orig_filename = filename.strip()
    legal_filename = (orig_filename.replace(':', ' -').replace('/', ' ')
        .replace('\\', ' '))
    
    return legal_filename


def convert_html_to_md(input: str | list[str]) -> str:
    """
    Convert basic HTML formatting into markdown

    This function will convert the following: 
    - Bold: `<b>abc</b>` --> `**abc**`
    - Italics: `<i>abc</i>` --> `*abc*`
    - Blockquotes: `<blockquote>abc</blockquote> --> `> abc`
    - Links: `<a href="https://abc.com">abc</a>` --> `[abc](https://abc.com)`

    Arguments:
        input: The string or list of strings containing HTML tags

    Returns:
        A string with the HTML tags replaced with markdown syntax. If the input
        was a list of strings, then a list of strings will be returned
    """
    is_list = False
    if type(input) == list: 
        input_str = ''.join(input)
        is_list = True
    elif type(input) == str: 
        input_str = input
    else: 
        print('aborting. input must be a string or list of strings')
        return 

    # BOLD, ITALICS
    input_str = (input_str.replace('<b>', '**').replace('</b>', '**')
                 .replace('<i>', '*').replace('</i>','*'))
    
    # BLOCKQUOTES
    blockquote_pattern = re.compile(r"<blockquote>(.*?)</blockquote>", 
                                    flags=re.DOTALL)
    while blockquote_pattern.search(input_str) != None: 
        blockquote_match = blockquote_pattern.search(input_str)
        if blockquote_match:
            blockquote_contents = blockquote_match.group(1)

            # blockquotes may span over multiple lines
            # each line must begin with `> `
            blockquote_lines = blockquote_contents.splitlines()
            blockquote_md = ['> {}\n'.format(x.strip()) for x in blockquote_lines]
            blockquote_md = ''.join(blockquote_md)
            
            input_str = (input_str[:blockquote_match.start(0)] + blockquote_md
                         + input_str[blockquote_match.end(0):])

    # LINKS
    # explanation of regex
    # - match must start with `<a href="` (single or double quotes)
    # - match must end with `</a>`
    # - group 1: everything between `<a href="` and the next single or double 
    #       quote. this is the url
    # - non-capturing group: everything after the url's closing quote and the 
    #       `<a href`'s closing bracket, `>`. these are extraneous html 
    #       attributes, e.g. `target="_blank"`
    # - group 2: everything after the closing bracket `>` and `</a>`. this is 
    #       the text of the link. may be empty
    ahref_pattern = re.compile(r"<a href=[\"'](.*?)[\"'](?:.*?)>(.*?)</a>", 
                               flags=re.DOTALL)
    while ahref_pattern.search(input_str) != None: 
        ahref_match = ahref_pattern.search(input_str)
        if ahref_match: 
            url = ahref_match.group(1)
            link_name = ahref_match.group(2).strip()
            link_md = '[{}]({})'.format(link_name, url)
            input_str = (input_str[:ahref_match.start(0)] + link_md 
                         + input_str[ahref_match.end(0):])
    
    if is_list: 
        result = input_str.splitlines()
    else: 
        result = input_str
    
    return result 