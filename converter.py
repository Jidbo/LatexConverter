import pypandoc
import os


class Converter:

    def __init__(self, md, name, to="latex", in_format="md"):
        self.md = md
        self.to = to
        self.in_format = in_format
        self.name = name
        self.filename = None
        self.converted = None
        self.to_convert = True

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
            self.converted = pypandoc.convert_text(self.md, self.to, format=self.in_format, extra_args=["-s"])

        return self.converted

