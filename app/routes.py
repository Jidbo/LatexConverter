from flask import render_template, request, flash
from requests.exceptions import ConnectionError
from app.codimd import Codimd, StatusCodeError
from app.converter import Converter, get_available_templates
from . import main
from base64 import b64encode
from . import form

NO_TEMPLATE_NAME = "None"


def parse_error(error):
    if isinstance(error, AttributeError):
        flash("Not a valid URL for a CodiMD note!", 'warning')
    elif isinstance(error, StatusCodeError):
        flash("Did not find a note with that id on the server!", 'warning')
    elif isinstance(error, ConnectionError):
        flash("Could not reach the CodiMD Server!", 'warning')


@main.route("/", methods=["GET"])
def home():
    values = {}
    main_form = form.MainForm(request.form)
    values["form"] = main_form
    values["url"] = ""

    return render_template("index.html", **values)


@main.route("/converted", methods=["POST"])
def converted():
    values = {}
    main_form = form.MainForm(request.form)
    values["form"] = main_form

    if main_form.validate():
        # get content from codi md
        codi = Codimd(main_form.url.data)
        codi.parse_url()
        try:
            data = codi.get_md()
        except (AttributeError, StatusCodeError, ConnectionError) as e:
            parse_error(e)
            return render_template("index.html", **values)

        conv = Converter(data, codi.note_id)

        # check if template is enabled
        temp_name = main_form.template.data

        if temp_name != NO_TEMPLATE_NAME and temp_name in get_available_templates():
            conv.add_template(temp_name)

        if main_form.file_type.data == "pdf":
            pdf_raw = conv.convert_to_pdf()
            if not pdf_raw:
                flash('Could not convert to PDF')
                return render_template("index.html", **values)

            pdf_data = b64encode(pdf_raw)
            values["data"] = pdf_data.decode('utf-8')
        else:
            values["data"] = conv.convert_to_text()

        return render_template("converted.html", **values)

    return render_template("index.html", **values)
