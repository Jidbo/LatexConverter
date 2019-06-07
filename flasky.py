import argparse
from app import create_app

# setup argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", required=False, default=False,
                    action="store_true", help="Enables the debug mode.")
parser.add_argument("--ip", required=False, default="0.0.0.0",
                    action="store", dest="ip",
                    help="set the ip the flask server binds to")
args = parser.parse_args()

if args.debug:
    app = create_app('debug')
else:
    app = create_app('production')

if __name__ == "__main__":
    # start flask app
    app.run(host=args.ip)
