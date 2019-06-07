from flask import render_template, request
from requests.exceptions import ConnectionError
from app.codimd import Codimd, StatusCodeError
from app.converter import Converter, get_available_templates
from . import main
from base64 import b64encode

NO_TEMPLATE_NAME = "None"
FILE_TYPES = ['Latex', 'PDF']


def parse_error(error):
    values = {}
    if isinstance(error, AttributeError):
        values["error_display"] = "Not a valid URL for a CodiMD note!"
    elif isinstance(error, StatusCodeError):
        values["error_display"] = "Did not find a note with that id on" \
            " the server!"
    elif isinstance(error, ConnectionError):
        values["error_display"] = "Could not reach the CodiMD Server!"

    if "eisvogelTemplate" in request.form:
        values["eisvogel"] = True
    if "convertToFile" in request.form:
        values["convert_to_file"] = True

    return values


@main.route("/", methods=["GET", "POST"])
def home():
    values = {}
    # setup templates
    available_templates = get_available_templates()
    available_templates.append(NO_TEMPLATE_NAME)
    values["templates"] = available_templates
    values["cur_template"] = NO_TEMPLATE_NAME
    values["file_types"] = FILE_TYPES
    if request.method == "POST":
        url = request.form["url"]
        values["url"] = url

        # get content from codi md
        codi = Codimd(url)
        codi.parse_url()
        try:
            data = codi.get_md()
        except (AttributeError, StatusCodeError, ConnectionError) as e:
            values = {**values, **parse_error(e)}
            return render_template("index.html", **values)

        conv = Converter(data, codi.note_id)

        # check if template is enabled
        if "template" in request.form:
            temp_name = request.form["template"].strip()

            if temp_name != NO_TEMPLATE_NAME and temp_name in available_templates:
                conv.add_template(temp_name)
                values["cur_template"] = temp_name

        values["file_type"] = request.form["file_type"]

        if request.form["file_type"] == "PDF":
            pdf_data = b64encode(conv.convert_to_pdf())
            values["data"] = "data:application/pdf;base64," + pdf_data.decode('utf-8')
        else:
            values["data"] = conv.convert_to_text()
    else:
        # render default page
        values["url"] = ""

    return render_template("index.html", **values)
