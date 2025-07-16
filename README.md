# py-notes

> py-notes is a Python library to create, edit, and format markdown notes, with a focus on YAML frontmatter (aka properties). This is meant for use with [Obsidian.md](https://obsidian.md)’s flavor of [markdown](https://help.obsidian.md/obsidian-flavored-markdown), [tags](https://help.obsidian.md/tags), and [properties](https://help.obsidian.md/properties), but will work with any markdown file. 

## Features
- **Properties**: Add properties, update property values, ensure valid YAML formatting
- **Tags**: Add tags, ensure valid tag formatting, convert a tag to a property
- **Change formatting of a note’s body**: Indentation size, date format
- **Titles** (heading 1 level): Update the title of a note, or extract it for further use

## Use cases
This project originated from a need to migrate all of my notes from various note apps (Evernote, Notion, Bear, etc) to Obsidian, which uses plain markdown files as notes. Each app’s notes exported to markdown follow slightly different markdown syntax or rules, such as using 2 or 4 spaces for indentation or which characters are allowed in tags. All of these notes needed to be standardized. In addition, I wanted to reorganize the notes to fit the current organization system I use with Obsidian, which namely uses properties. This library helps automate these processes. 

### Examples
- Add a tag to notes in bulk 
- Split one note into smaller notes, based on a heading
- Apply a new set of properties to existing notes in bulk
