# py-notes

> py-notes is a Python library to create, edit, and format markdown files, with a focus on YAML frontmatter (aka properties). This is meant for use with [Obsidian.md](https://obsidian.md)’s flavor of [markdown](https://help.obsidian.md/obsidian-flavored-markdown), [tags](https://help.obsidian.md/tags), and [properties](https://help.obsidian.md/properties), but will work with any markdown file. 

## Features
- **Properties**: add properties, update property values, ensure proper YAML formatting, reorder properties
- **Tags**: add tags, ensure proper tag formatting, convert a tag to a property
- **Change formatting of a note’s body**: indentation size, date format
- **Titles** (heading 1 level): update the title of a note, or extract it for further use

## Use cases
This project originated from a need for a way to migrate all of my notes from various note apps (Evernote, Notion, Bear, etc) to Obsidian, which uses plain markdown files as notes. Each app’s notes exported to markdown follow slightly different rules, such as using 2 or 4 spaces for indentation or which characters are allowed in tags — all of which needed to be standardized. In addition, I wanted to reorganize all of these notes to fit the current organization system I use with Obsidian, which namely uses properties. This library helps automate these processes. 

### Examples
- Add a tag to notes in bulk 
- Split one note into smaller notes, based on a heading
- Apply a new template (new sets of properties) to notes in bulk
