from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import RadioField
from wtforms import SubmitField
from wtforms.widgets import Select
from . import converter

FILE_TYPES = [('latex', 'Latex'), ('pdf', 'PDF')]

class MainForm(FlaskForm):
    url = StringField(render_kw={
        "placeholder": "CodiMD URL",
        "class": "form-control"
    })
    template = RadioField(
        "Templates",
        choices=[(temp, temp) for temp in
                 converter.get_available_templates()] + [('none', 'None')]
    )
    file_type = RadioField("File", choices=FILE_TYPES)
    submit = SubmitField(render_kw={
        "class": "form-control btn btn-info"
    })



