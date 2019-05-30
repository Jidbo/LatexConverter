import argparse
from app import create_app

app = create_app()

if __name__ == "__main__":

    # setup argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", required=False, default=False,
                        action="store_true", help="Enables the debug mode.")
    parser.add_argument("--ip", required=False, default="0.0.0.0",
                        action="store", dest="ip",
                        help="set the ip the flask server binds to")
    args = parser.parse_args()

    # start flask app
    app.run(debug=args.debug, host=args.ip)
