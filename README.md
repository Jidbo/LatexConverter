LatexConverter
===
A small webapp that converts your CodiMD documents to latexcode using pypandoc.

## Requirments
- Flask
- pypandoc
- requests

## Features
- Convert directly to tex file
- Use Templates

## Templates
Templates can be stored in the pandoc-templates folder and are automatically
added for selection. The templates have to
be in the [pandoc template format](https://pandoc.org/MANUAL.html#templates) for latex and have the `.tex` extension. 

Default templates:
- [Eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template)

## Commandline Arguements
- `-d` `--debug` Enables debug mode for flask server
- `--ip` set the ip the flask server binds to
- `-h` show help message
