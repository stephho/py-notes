import math
from . import markdown_utils

class note:
    """
    A note in markdown

    Attributes:
        contents (list[str]): The entire contents of a note, comprised of the 
            frontmatter and the body. Each string in the list is a line in the 
            note, ending in `\\n`
        frontmatter (list[str]): The lines at the top of the note containing 
            the properties of a note, in YAML. The first and last lines of the
            frontmatter are always the frontmatter markers
        fontmatter_marker (str): Markdown notation that indicates the beginning
            and the end of the frontmatter: `'---\\n'`
        frontmatter_start (int): The index where the frontmatter starts in the 
            note's contents. This should always be `0`
        frontmatter_end (int): The index where the frontmatter ends in the 
            note's contents
        properties (dict[str, dict[str, any]]): Properties are structured data 
            found in the note's frontmatter. The keys of `properties` are the 
            property names, in kebab case. The values are dicts with the
            following keys:
                value (str | list[str]): The value of the property. Multi-line
                    property values are lists
                order (int): The order in which the property appears in the
                    frontmatter, starting from `1`
                index (int): The index of the first line of the property in the
                    frontmatter. The first property in the frontmatter always 
                    has an index of 1, because index `0` is always the 
                    frontmatter marker
            
            Example:
            ```
            properties = { 
                'date-created': { 
                    'value': '2024-09-01',
                    'order': 2,
                    'index': 3
                }
            }
            ```

        body (list[str]): All lines in the note's contents after the frontmatter
        h1 (str): The H1 level header in the body of the note, aka the title. 
            Text-only, no markdown characters
        list_marker (str): Character used as the bullpet point in unordered 
            lists in markdown notation. Default: `-`
        indentation (int): Number of spaces for one level of indentation used in
            lists. Default: `4`
    """

    def __init__(self, contents: list[str]):
        """
        Creates a note, given its contents

        Upon intitialization, the note will be parsed into its frontmatter and
        its body. If the note has no frontmatter, empty frontmatter (two lines
        of frontmatter markers with no lines in between) will be added

        Arguments:
            contents: The entire contents of a note, comprised of the 
                frontmatter and the body. Each string in the list is a line in 
                the note, ending in `\\n`
        """
        # markdown notation
        self.frontmatter_marker = '---\n' 
        self.list_marker = '-'
        self.indentation = 4

        self.contents = contents
        self.frontmatter_start = 0 # frontmatter is always at the start of the note
        self.frontmatter_end = 1 # default empty frontmatter, so 2 lines
        self.frontmatter = [self.frontmatter_marker, self.frontmatter_marker]
        self.properties = {}
        self.body = []
        self.h1 = ''

        # parse the note contents into frontmatter and body
        # check if the note has frontmatter
        if self.contents[0] == self.frontmatter_marker:
            # everything in between the first --- and second --- is frontmatter
            self.frontmatter_end = self.contents[1:].index(self.frontmatter_marker) + 1
            self.frontmatter = self.contents[self.frontmatter_start:self.frontmatter_end + 1]

            # there should be no empty lines in the frontmatter
            for line in self.frontmatter: 
                if len(line.strip()) == 0: 
                    self.frontmatter.remove(line)
        
        else:
            # there is no frontmatter in the note, add empty frontmatter
            self.contents = self.frontmatter + self.contents

        # the rest of the note contents after the frontmatter is the body
        self.body = self.contents[self.frontmatter_end + 1:]

        # there should be no empty lines in between the frontmatter and the body
        for line in self.body: 
            if len(line.strip()) == 0:
                self.body.remove(line)
            else:
                break

        # update attributes to account for removal of empty lines
        self.contents = self.frontmatter + self.body
        self.frontmatter_end = len(self.frontmatter) - 1


    def parse_properties(self):
        """
        Parse the lines in the frontmatter into a dictionary of properties

        Modifies attributes:
            properties (dict[str, dict[str, any]]): Keys are property names, in
                kebab case. The values are dicts with the following keys
                    value (str | list[str]): The value of the property. Multi-
                        line property values are lists
                    order (int): The order in which the property appears in the
                        frontmatter, starting from `1`
                    index (int): The index of the first line of the property in
                        the frontmatter. The first property in the frontmatter 
                        always has an index of 1, because index `0` is always 
                        the frontmatter marker
            frontmatter (list[str]): In the process of parsing properties, they 
                may be reformatted, affecting frontmatter
            frontmatter_end (int): If frontmatter is reformatted, the index of 
                where it ends may also be affected
            contents (list[str]): If frontmatter is reformatted, it is updated 
                in `contents` too
        
        Example:
            ```
            properties = { 
                'date-created': { 
                    'value': '2024-09-01',
                    'order': 2,
                    'index': 3
                }, 
                'tags': { 
                    'value': ['  - "#movie"\\n', '  - "#status/in-progress"\\n']
                    'order': 3
                    'index': 4
                }
            }
            ```
        """
        # first, get all the property keys and their indices in the frontmatter
        props = {}
        n = 0
        for line in self.frontmatter: 
            if line == self.frontmatter_marker: 
                pass 
            elif line[0] != ' ' and ':' in line:
                # this line has a property key
                # assumes there are no other ':' in the property name or value
                n += 1 # order of property
                i = self.frontmatter.index(line) # index of property
                prop_name = line.split(':')[0]
                props[n] = (i, prop_name)
            else: 
                continue
        
        # then, get the property values for each property key
        for n in props:
            i = props[n][0]
            prop_name = props[n][1]

            # get the index of the next property, in order
            # the property values are the lines in between the two indices
            try: 
                i2 = props[n+1][0]
            except KeyError: 
                # this is the last property
                i2 = -1
            
            prop_value = ''
            prop_value_lines = self.frontmatter[i+1:i2]

            if len(prop_value_lines) == 0: 
                # then the property value is in the same line as the property name
                try: 
                    prop_line = self.frontmatter[i]
                    prop_value = prop_line.lstrip('{}:'.format(prop_name)).strip()
                except IndexError: 
                    # the property has no value 
                    pass
            
            else: 
                # if property value is more than one item, it should be 
                # properly formatted as a YAML list
                if prop_name.lower().strip() == 'tags': 
                    is_tags = True 
                else: 
                    is_tags = False
                
                prop_value = markdown_utils.format_property_list(
                    prop_value=prop_value_lines, 
                    is_tags=is_tags)

            new_prop_name = markdown_utils.format_kebab_case(prop_name)

            self.properties[new_prop_name] = {
                'value': prop_value, 
                'order': n, 
                'index': i
            }
            
            # in case the property name and values have been reformatted, 
            # rewrite them to frontmatter
            new_prop_value_lines = markdown_utils.write_frontmatter(
                prop_name=new_prop_name, 
                prop_value=prop_value)
            self.frontmatter = (self.frontmatter[:i] + new_prop_value_lines 
                + self.frontmatter[i2:])
        
        # finally, we got all the properties 
        # update attributes to account for reformatted frontmatter
        self.contents = self.frontmatter + self.body
        self.frontmatter_end = len(self.frontmatter) - 1


    def add_property(self, prop_name: str, prop_order: int, prop_value: str | list[str]):
        """
        Add a new property and its value to the note
        
        Note: If the property already exists in the note, the property will not
        be added. Use `update_property()` method instead

        Arguments:
            prop_name (str): Name of the new property to add. This will be 
                changed to kebab case
            prop_order (int): The order in which the new property appears in
                the frontmatter. If prop_order = 1, then it will be the first
                property. If another property already exists in the frontmatter
                in the nth place, the new property will be inserted above it,
                and the rest of the properties below it move down in the order
            prop_value (str | list[str]): The value of the property. Multi-line
                property values are lists

        Modifies attributes:
            properties (dict[str, dict[str, any]])
            frontmatter (list[str]): The new property will also be added to the
                frontmatter
            frontmatter_end (int): Updating `frontmatter` also changes the 
                index where the frontmatter ends
            contents (list[str]): `frontmatter` is part of `contents`
        """
        prop_name = markdown_utils.format_kebab_case(prop_name)

        # check if properties have been parsed
        if len(self.properties) == 0: 
            self.parse_properties()

        # check if the property already exists, we don't want to overwrite it
        if prop_name in self.properties: 
            print('the property {} already exists, aborting'.format(prop_name))
            return

        # checks pass, let's add the new property to the frontmatter!
        prop_value_lines = []
        if type(prop_value) == list: 
            is_tags = True if prop_name == 'tags' else False 
            prop_value_list = markdown_utils.format_property_list(
                prop_value=prop_value, is_tags=is_tags)
            prop_value_lines = markdown_utils.write_frontmatter(
                prop_name=prop_name, prop_value=prop_value_list)
        else:
            prop_value_lines = markdown_utils.write_frontmatter(
                prop_name=prop_name, prop_value=prop_value)
        
        if prop_order > len(self.properties): 
            # add the property as the last property in the frontmatter
            new_prop_index = len(self.frontmatter) - 1

        elif prop_order == 1: 
            # add the property as the first property in the frontmatter 
            new_prop_index = 1

        else:
            # add the property in the line after the preceding property
            preceding_prop = prop_order - 1
            for prop in self.properties: 
                if self.properties[prop]['order'] == preceding_prop: 
                    new_prop_index = self.properties[prop]['index'] + 1

                    # if the preceding property is a list, it spans over 
                    # multiple lines; the new property needs to be added after
                    if type(self.properties[prop]['value']) == list: 
                        new_prop_index += len(self.properties[prop]['value'])

        self.frontmatter = (self.frontmatter[:new_prop_index] 
            + prop_value_lines 
            + self.frontmatter[new_prop_index:])
        print('the property has been added: {}'.format(str(prop_value_lines)))

        # update attributes affected by new frontmatter
        self.contents = self.frontmatter + self.body 
        self.frontmatter_end = len(self.frontmatter) - 1
        self.parse_properties() 


    def get_h1(self): 
        """
        Get the H1 heading, aka the title, of the note

        Note: If no H1 is found, use the `update_h1()` method to set one. There
        should only be one H1 per note, but if there are multiple H1
        headings, only the first H1 is set as `h1`

        Modifies attributes:
            h1 (str): This method will assign the title to `h1`
            body (list[str]): `h1` is part of the `body`. Some extra line breaks
                and spacing may be cleaned up in the process of getting `h1`
            contents (list[str]): `h1` is part of the `contents`
        """
        title = ''
        h1_index = 0
        for l in self.body: 
            if l.startswith('# '): 
                title = l 
                h1_index = self.body.index(l)
                break 
        
        if title != '': 
            title = title.lstrip('# ').strip()
            h1_line = '# {}\n'.format(title)
            self.body[h1_index] = h1_line
            
            # check if the line after h1 is a line break; if not, insert one
            if len(self.body[h1_index + 1].strip()) != 0: 
                self.body = (self.body[:h1_index + 1] 
                    + ['\n'] + self.body[h1_index + 1:])
            
            self.h1 = title
            self.contents = self.frontmatter + self.body


    def update_h1(self, title: str): 
        """
        Update the H1 heading, aka the title, of the note. If the note has no 
        H1 heading, it will be inserted into the note, as the first line of the
        body

        Arguments:
            title: The string to use as the new `h1`. Can be passed with or 
                without markdown notation

        Modifies attributes:
            h1 (str): This method will assign the new title to `h1`
            body (list[str]): `h1` is part of the `body`. Some extra line breaks
                and spacing may be cleaned up in the process of updating `h1`
            contents (list[str]): `h1` is part of the `contents`
        """
        # check if there is an h1 in the note
        if len(self.h1) == 0: 
            self.get_h1()

        h1_line = '# {}\n'.format(self.h1)

        cleaned_title = title.strip().lstrip('# ').strip()
        updated_h1 = '# {}\n'.format(cleaned_title)

        try: 
            h1_index = self.body.index(h1_line) 
            self.body[h1_index] = updated_h1

        except ValueError: 
            # no h1 exists in note, add it as the first line of the body
            updated_h1_lines = [updated_h1]
            
            # there should always be an empty line after the h1
            if len(self.body[0].strip()) != 0: 
                updated_h1_lines.append('\n')
            
            self.body = updated_h1_lines + self.body

        self.h1 = cleaned_title
        self.contents = self.frontmatter + self.body


    def change_list_indent(self, orig_indent: int=2):
        """
        Change the number of spaces used in list indentation in the note's body

        Note: The number of spaces to convert to is determined by the class 
        attribute `indentation` (default: `4`). This method does not affect 
        lists in frontmatter, which always use 2 spaces indentation

        Arguments:
            orig_indent (int): The number of spaces used in one level of 
                indentation in the original note's body

        Modifies attributes:
            body (list[str])
            content (list[str])
        """
        updated_lines = []

        if orig_indent == self.indentation: 
            print('no change in identation needed, aborting')
            return 

        for l in self.body:

            if l.startswith('{} '.format(self.list_marker)): 
                # this line is a 1st level list item, i.e. not indented
                updated_lines.append(l)

            elif l.strip().startswith('{} '.format(self.list_marker)): 
                # this line is a list item
                # get the number of spaces in front of the bullet
                bullet = l.index('{} '.format(self.list_marker)) 
                indent_chars = l[:bullet]
                
                if len(indent_chars.replace(' ', '')) == 0: 
                    # confirm there are only spaces in front of the bullet
                    # then calculate what is the indentation level
                    # in case n_spaces is not exactly equal to orig_indent, 
                    # round up to preserve some level of indentation 
                    n_spaces = len(indent_chars)
                    indentation_level = math.ceil(n_spaces / orig_indent)
                    
                    # insert the new number of spaces into the list line
                    new_indentation = indentation_level * self.indentation
                    new_indent_chars = ' ' * new_indentation
                    updated_l = new_indent_chars + l[bullet:]
                    updated_lines.append(updated_l)
                
                else:
                    print('this line may not be a list item, skipping:', l)
                    updated_lines.append(l)
            
            else: 
                # this line is not a list, do nothing
                updated_lines.append(l)
        
        self.body = updated_lines
        self.contents = self.frontmatter + self.body
