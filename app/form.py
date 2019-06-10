from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, validators
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta
from . import config
from . import converter

FILE_TYPES = [('latex', 'Latex'), ('pdf', 'PDF')]

class MainForm(FlaskForm):

    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_time_limit = timedelta(minutes=20)
        csrf_secret = bytes(config.Config.SECRET_KEY, 'utf-8')

    url = StringField([validators.URL(message="Not a valid URL")], render_kw={
        "placeholder": "CodiMD URL",
        "class": "form-control"
    })
    template = RadioField(
        "Templates",
        [validators.InputRequired(message="Choose a Template")],
        choices=[(temp, temp) for temp in
                 converter.get_available_templates()] + [('none', 'None')]
    )
    file_type = RadioField("File", [validators.InputRequired(message="File Output required")], choices=FILE_TYPES)
    submit = SubmitField(
        render_kw={
            "class": "form-control btn btn-info"
        })



