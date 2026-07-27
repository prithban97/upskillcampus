from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import random
import string

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["url_shortener"]
collection = db["urls"]

# Create Unique Index (Integrity)
collection.create_index("code", unique=True)


# Generate Short Code
def generate_code(length=3):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@app.route("/", methods=["GET", "POST"])
def home():

    short_url = None

    if request.method == "POST":

        long_url = request.form["url"]

        # Add https:// if missing
        if not long_url.startswith(("http://", "https://")):
            long_url = "https://" + long_url

        while True:
            code = generate_code()

            try:
                collection.insert_one({
                    "code": code,
                    "url": long_url
                })
                break

            except DuplicateKeyError:
                continue

        short_url = request.host_url + code

    return render_template("index.html", short_url=short_url)


@app.route("/<code>")
def redirect_url(code):

    data = collection.find_one({"code": code})

    if data:
        return redirect(data["url"])

    return "<h2>404 - URL Not Found</h2>"


if __name__ == "__main__":
    app.run(debug=True)