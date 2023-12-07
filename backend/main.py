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
from utils.list import StudentList

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)


@app.route("/")
def index():
    return {"message": "I am still living."}


@app.route("/login")
def login():
    return render_template("login/login.html")


@app.route("/student")
@login_required("student")
def student():
    return render_template("student/student.html")


@app.route("/teacher")
@login_required("teacher")
def teacher():
    return render_template("teacher/list.html")


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

        return redirect(url_for(f"{role}"))


@app.route("/list", methods=["POST"])
def upload_list():
    # receive csv file from frontend
    data = request.files["csvfile"]
    df = pd.read_csv(data)

    # upload student list
    stlist = StudentList(df)
    upload_info_dict = stlist.upload_list()
    print(upload_info_dict["msg"])

    if not upload_info_dict["flag"]:
        error_msg = upload_info_dict["msg"]
        return jsonify({"msg", f"{error_msg}"})
    else:
        upload_msg = upload_info_dict["msg"]

    return "OK"


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
