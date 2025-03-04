"""
Helper functions for working with markdown text
"""

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

    Example:
        - `In progress` (a tag) --> `'  - "#in-progress"\\n'`
        - `[[Survivor US S48]]` --> `'  - "[[Survivor US S48]]"\\n'`
    """
    list_template = '  - {}\n'
    formatted_item = ''
    cleaned_item = str(item).strip().lstrip('- ').replace('"', '')
    
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


def write_frontmatter(prop_name: str, prop_value: str | list[str]): 
    """
    Write a property and its value to lines of frontmatter in YAML notation
    
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
        frontmatter_lines = [prop_multi_line.format(prop_name=prop_name)] + prop_value
    else:
        frontmatter_lines = [prop_single_line.format(prop_name=prop_name, prop_value=prop_value)]
    
    return frontmatter_lines