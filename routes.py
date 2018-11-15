from flask import Flask, render_template, request
import argparse
from codimd import Codimd

app = Flask(__name__)


@app.route("/",  methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        codi = Codimd(url)
        codi.parse_url()
        data = codi.get_md()
        return render_template("index.html", data=data)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", required=False, default=False, action="store_true",
                        help="Enables the debug mode.")
    args = parser.parse_args()

    app.run(debug=args.debug)
