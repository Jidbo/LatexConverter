LatexConverter
===
A small webapp that converts your CodiMD documents to latexcode using pypandoc.

## Requirments
- [pandoc](https://pandoc.org/)

## Features
- Directly download tex file
- Use Pandoc-Templates
- Edit file on page

## Templates
Templates can be stored in the `pandoc-templates` folder and are automatically
added for selection. The templates have to be in the 
[pandoc template format](https://pandoc.org/MANUAL.html#templates) for latex 
and have the `.tex` extension. 

Default templates:
- [Eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template)

## Commandline Arguements
- `-d` `--debug` Enables debug mode for flask server (should be used while 
    developing, since talisman forwards all requests to https)
- `--ip` set the ip the flask server binds to
- `-h` show help message

## Docker
The docker container uses gunicorn as a WSGI-Server for the project.

Building: `sudo docker build -t latexconverter:latest .`
Running: `sudo docker run --name latexconv -d -p 5000:5000 latexconverter:latest`
