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
                value (str or list[str]): The value of the property. Multi-line
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
                'date-created' { 
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