import os
import requests
import pandas as pd
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

from model.admin import admin_bp
from model.teacher import teacher_bp
from model.student import student_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

# registy other route blueprint
api2prefix = [
    (admin_bp, "/admin"),
    (teacher_bp, "/teacher"),
    (student_bp, "/student"),
]
for api, prefix in api2prefix:
    app.register_blueprint(api, url_prefix=prefix)


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login")
def login():
    return render_template("login/login.html")


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

    # check whether connect to database
    if not passwd_is_correct:
        error_msg = user_info_dict["msg"]
        return jsonify({"msg": f"{error_msg}"})

    else:
        role = user_info_dict["role"]

        # set session to store login user info
        session["username"] = username
        session["role"] = role
        session.permanent = True

        return redirect(url_for(f"{role}.index"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
