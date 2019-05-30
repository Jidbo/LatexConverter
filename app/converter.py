import pypandoc
import os

TEMPLATE_FOLDER = "pandoc-templates/"

class Converter:

    def __init__(self, md, name, to="latex", in_format="md"):
        self.md = md
        self.to = to
        self.in_format = in_format
        self.name = name
        self.filename = None
        self.to_convert = True
        self.arguments = ["-s"]

    def convert_to_text(self):
        self.converted = pypandoc.convert_text(self.md, self.to,
                                               format=self.in_format,
                                               extra_args=self.arguments)
        return self.converted


    def add_template(self, template):
        template_folder = get_template_folder()
        template = os.path.join(template_folder, f"{template}.tex")
        print(f"adding Template {template}")
        self.arguments.append("--template")
        self.arguments.append(template)


def get_available_templates():
    templatefolder = get_template_folder()
    files = os.listdir(templatefolder)
    templates = [tmp[:-4] for tmp in files if tmp.endswith(".tex")]

    return templates

def get_template_folder():
    filepath = os.path.realpath(__file__)
    mainfolder = os.path.dirname(filepath)
    return os.path.join(mainfolder, TEMPLATE_FOLDER)
