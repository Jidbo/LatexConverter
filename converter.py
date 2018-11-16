import pypandoc


class Converter:

    def __init__(self, md):
        self.md = md

    def convert_to_latex(self):
        latex = pypandoc.convert_text(self.md, "latex", format="md", extra_args=["-s"])
        return latex
