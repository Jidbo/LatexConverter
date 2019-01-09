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
        print(request.form)
        if "eisvogelTemplate" in request.form:
            conv.addTemplate("eisvogel")
            values["eisvogel"] = True
        if "convertToFile" in request.form:
            print("SAVE FILE")
            file_path = conv.convert_to_file("tex")
            values["file_path"] = conv.name
            return render_template("index.html", **values)
        else:
            values["data"] = conv.convert_to_text()
            return render_template("index.html", **values)
    else:
        return render_template("index.html", url="")


@app.route("/download/<id>", methods=["GET"])
def downlaod(id):
    file_path = f"tmp/{id}.md"
    return send_file(file_path, mimetype="text/plain", as_attachment=True,
                     attachment_filename="result.tex")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", required=False, default=False, action="store_true",
                        help="Enables the debug mode.")
    args = parser.parse_args()

    app.run(debug=args.debug, host="0.0.0.0")

