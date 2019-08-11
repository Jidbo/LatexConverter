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


@main.route("/", methods=["GET", "POST"])
def home():
    values = {}
    main_form = form.MainForm(request.form)
    values["form"] = main_form
    print(dir(main_form.url))
    print(main_form.url.raw_data)
    print(main_form.url)
    # if request.method == "POST" and main_form.validate():
    if request.method == "POST":
        print("TEST TEST TEST TEST TEST TEST TEST")
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
            pdf_data = b64encode(conv.convert_to_pdf())
            values["data"] = pdf_data.decode('utf-8')
        else:
            values["data"] = conv.convert_to_text()
    else:
        # render default page
        values["url"] = ""

    return render_template("index.html", **values)
