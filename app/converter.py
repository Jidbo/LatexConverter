import pypandoc
import os
from latex import build_pdf
from latex import LatexBuildError

TEMPLATE_FOLDER = "pandoc-templates/"

class Converter:

    def __init__(self, md, name, to="latex", in_format="md"):
        self.md = md
        self.to = to
        self.in_format = in_format
        self.name = name
        self.converted = None
        self.pdf = None
        self.arguments = ["-s"]

    def convert_to_text(self):
        self.converted = pypandoc.convert_text(self.md, self.to,
                                               format=self.in_format,
                                               extra_args=self.arguments)
        return self.converted

    def convert_to_pdf(self):
        if self.converted is None:
            self.convert_to_text()
        self.pdf = None
        generated = False

        try:
            self.pdf = bytes(build_pdf(self.converted, builder='latexmk'))
            generated = True
        except LatexBuildError:
            print('latexmk failed to build. Falling back to xelatex...')

        if not generated:
            try:
                self.pdf = bytes(build_pdf(self.converted, builder='xelatexmk'))
                generated = True
            except LatexBuildError:
                print('xelatex failed to build. Aborting...')

        return self.pdf

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
