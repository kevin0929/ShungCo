from flask import Flask, jsonify, redirect, render_template, request, url_for

from utils.user import User

app = Flask(__name__)


@app.route("/")
def index():
    return {"message": "I am still living."}


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/student")
def student():
    return render_template("student.html")


@app.route("/verify", methods=["POST", "GET"])
def verify():
    # get user information
    data = request.json
    username = data["username"]
    password = data["password"]

    user = User(username, password)
    info_is_correct = user.Auth()

    if info_is_correct:
        return redirect(url_for("student"))
    else:
        return jsonify({"error msg": "password is not correct."})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
