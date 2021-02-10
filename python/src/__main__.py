# -*- coding: utf-8 -*-
"""
    src.__main__
    ~~~~~~~~~~~~
    Handles arguments from the cli and runs the app.

    Functions:

        main()

"""
import argparse
from src import app

# Setup Parser
parser = argparse.ArgumentParser()

# Define the arguments
parser.add_argument("--host", type=str, help="The host to listen on (default: 0.0.0.0)", default="0.0.0.0")
parser.add_argument("--port", type=int, help="The port to listen on (default: 80)", default=80)
args = parser.parse_args()

def main():
    app.run(host=args.host, port=args.port)
    print(f"Listening on: {args.host}:{args.port}")

if __name__ == "__main__":
    main()
