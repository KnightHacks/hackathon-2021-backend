from flask import Flask, render_template, request
import requests
import json
from flask_cors import CORS
app = Flask(__name__, static_url_path="/static")
CORS(app)

@app.route("/register/", methods=["POST", "GET"])
def phone_add():
    content = request.json
    print(content)
@app.route("/", methods = ["GET"])
def main():
    return "hello world!"
print("Flask server running on port 5002")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)