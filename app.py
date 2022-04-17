from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods = ["POST", "GET"])
def search():
    nazwa_uzytkownika = request.form["nazwa_uzytkownika"]
    print(nazwa_uzytkownika)
    return nazwa_uzytkownika


if __name__ == "__main__":
    app.run(host="25.85.5.88", debug=True)
