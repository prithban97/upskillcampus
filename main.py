from flask import Flask, request, redirect

import random, string

app = Flask(__name__)
urls = {}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        urls[code] = url
        return f'Short URL: <a href="/{code}">http://127.0.0.1:5000/{code}</a>'
    return '''
    <form method="post">
        <input type="text" name="url" placeholder="Enter URL">
        <button>Shorten</button>
    </form>
    '''

@app.route("/<code>")
def short(code):
    return redirect(urls.get(code, "/"))

app.run(debug=True)