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
        self.converted = None
        self.to_convert = True
        self.arguments = ["-s"]

    def convert_to_text(self):
        return self._convert()

    def convert_to_file(self, ending):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        tmp_directory = os.path.join(current_directory, "tmp")
        if not os.path.isdir(tmp_directory):
            os.makedirs(tmp_directory)

        new_file = os.path.join(tmp_directory, f"{self.name}.{ending}")
        contents = self._convert()
        with open(new_file, "w") as file:
            file.write(contents)

        return new_file

    def _convert(self):
        if self.to_convert:
            self.to_convert = False
            self.converted = pypandoc.convert_text(self.md, self.to,
                                                   format=self.in_format,
                                                   extra_args=self.arguments)

        return self.converted

    def add_template(self, template):
        self.arguments.append("--template")
        templatedir = f"pandoc-templates/{template}.tex"
        print(f"adding Template {template}")
        self.arguments.append(templatedir)


def get_available_templates():
    filepath = os.path.realpath(__file__)
    mainfolder = os.path.dirname(filepath)
    templatefolder = os.path.join(mainfolder, TEMPLATE_FOLDER)
    files = os.listdir(templatefolder)
    templates = [tmp[:-4] for tmp in files if tmp.endswith(".tex")]

    return templates

