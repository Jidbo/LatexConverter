from flask import Flask, render_template, request, send_file, redirect
import argparse
from codimd import Codimd
from converter import Converter

app = Flask(__name__)


@app.route("/",  methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        codi = Codimd(url)
        codi.parse_url()
        data = codi.get_md()
        conv = Converter(data, codi.note_id)

        if "convertToFile" in request.form:
            print("SAVE FILE")
            file_path = conv.convert_to_file("md")
            return render_template("index.html", url=url, file_path=conv.name)
        else:
            latex = conv.convert_to_text()
            return render_template("index.html", data=latex, url=url)
    else:
        return render_template("index.html", url="")


@app.route("/download/<id>", methods=["GET"])
def downlaod(id):
    file_path = f"tmp/{id}.md"
    return send_file(file_path, mimetype="text/plain", as_attachment=True,
                     attachment_filename="result.md")
    # return redirect("/", code="302")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", required=False, default=False, action="store_true",
                        help="Enables the debug mode.")
    args = parser.parse_args()

    app.run(debug=args.debug, host="0.0.0.0")

