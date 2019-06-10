LatexConverter
===
A small webapp that converts your CodiMD documents to latexcode using pypandoc.

## Requirements
- [pandoc](https://pandoc.org/)
- [latex](https://www.latex-project.org)

## Features
- Directly download tex file
- Use Pandoc-Templates
- Edit Tex-File on page
- Convert generated tex to PDF

## Templates
Templates can be stored in the `pandoc-templates` folder and are automatically
added for selection. The templates have to be in the 
[pandoc template format](https://pandoc.org/MANUAL.html#templates) for latex 
and have the `.tex` extension. 

Default templates:
- [Eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template)

## Commandline Arguments
- `-d` `--debug` Enables debug mode for flask server (should be used while 
    developing, since talisman forwards all requests to https)
- `--ip` set the ip the flask server binds to
- `-h` show help message

## Docker
The docker container uses gunicorn as a WSGI-Server for the project.

Building: `sudo docker build -t latexconverter:latest .`
Running: `sudo docker run --name latexconv -d -e SECRET_KEY="<your-secret-key>" -p 5000:5000 latexconverter:latest`
