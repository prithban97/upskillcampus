from flask import Flask, render_template, request, redirect
import random
import string

app = Flask(__name__)

urls = {}




@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form["url"]
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        urls[code] = long_url
        short_url = request.host_url + code
        return render_template("index.html", short_url=short_url)

    return render_template("index.html")

@app.route("/<code>")
def redirect_url(code):
    if code in urls:
        return redirect(urls[code])
    return "URL Not Found!"

if __name__ == "__main__":
    app.run(debug=True)