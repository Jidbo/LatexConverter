from flask import Flask, render_template, request, send_file, redirect
import argparse
from codimd import Codimd, StatusCodeError
from converter import Converter, get_available_templates
from requests.exceptions import ConnectionError

app = Flask(__name__)
NO_TEMPLATE_NAME = "None"

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

@app.route("/",  methods=["GET", "POST"])
def home():
    values = {}
    # setup templates
    available_templates = get_available_templates()
    available_templates.append(NO_TEMPLATE_NAME)
    values["templates"] = available_templates
    values["cur_template"] = NO_TEMPLATE_NAME
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

        # check if convert to file is enabled
        if "convertToFile" in request.form:
            values["convert_to_file"] = True
            conv.convert_to_file("tex")
            values["file_path"] = conv.name
        else:
            values["data"] = conv.convert_to_text()
    else:
        # render default page
        values["url"] = ""

    return render_template("index.html", **values)


@app.route("/download/<id>", methods=["GET"])
def downlaod(id):
    file_path = f"tmp/{id}.tex"
    return send_file(file_path, mimetype="text/plain", as_attachment=True,
                     attachment_filename="result.tex")


if __name__ == "__main__":
    # setup argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", required=False, default=False, action="store_true",
                        help="Enables the debug mode.")
    parser.add_argument("--ip", required=False, default="0.0.0.0",
                        action="store", dest="ip", help="set the ip the flask server binds to")
    args = parser.parse_args()

    # start flask app
    app.run(debug=args.debug, host=args.ip)

