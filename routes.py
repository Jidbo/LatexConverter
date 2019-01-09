from flask import Flask, render_template, request, send_file, redirect
import argparse
from codimd import Codimd
from converter import Converter

app = Flask(__name__)


@app.route("/",  methods=["GET", "POST"])
def home():
    if request.method == "POST":
        values = {}
        values["url"] = request.form["url"]
        url = request.form["url"]
        # get content from codi md
        codi = Codimd(url)
        codi.parse_url()
        data = codi.get_md()
        conv = Converter(data, codi.note_id)

        # check if template is enabled
        if "eisvogelTemplate" in request.form:
            conv.add_template("eisvogel")
            values["eisvogel"] = True

        # check if convert to file is enabled
        if "convertToFile" in request.form:
            print("SAVE FILE")
            conv.convert_to_file("tex")
            values["file_path"] = conv.name
            return render_template("index.html", **values)
        else:
            values["data"] = conv.convert_to_text()
            return render_template("index.html", **values)
    else:
        # render default page
        return render_template("index.html", url="")


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

