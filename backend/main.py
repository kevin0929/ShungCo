import os
import requests
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    session,
    abort,
)
from datetime import timedelta

from utils.user import User
from utils.auth import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)


@app.route("/")
def index():
    return {"message": "I am still living."}


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/student")
@login_required("student")
def student():
    return render_template("student.html")


@app.route("/teacher")
@login_required("teacher")
def teacher():
    return render_template("teacher.html")


@app.route("/verify", methods=["POST"])
def verify():
    # get input
    data = request.json
    username = data["username"]
    password = data["password"]

    # authenticate user information
    user = User(username, password)
    user_info_dict = user.login()
    passwd_is_correct = user_info_dict["flag"]
    role = user_info_dict["role"]

    if passwd_is_correct:
        # set session to store login user info
        session["username"] = username
        session["role"] = role
        session.permanent = True

        return redirect(url_for(f"{role}"))
    else:
        return jsonify({"error msg": "password is not correct."})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
