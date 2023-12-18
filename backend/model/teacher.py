import pandas as pd
from flask import Blueprint, render_template, url_for, request, jsonify

from utils.auth import login_required
from utils.list import StudentList

teacher_bp = Blueprint("teacher", __name__)


@teacher_bp.route("/index")
@login_required("teacher")
def index():
    return render_template("teacher/index.html")


@teacher_bp.route("/upload")
@login_required("teacher")
def upload():
    return render_template("teacher/upload.html")


@teacher_bp.route("/video")
@login_required("teacher")
def video():
    return render_template("teacher/video.html")


@teacher_bp.route("/list", methods=["POST"])
def upload_list():
    # receive csv file from frontend
    data = request.files["csvfile"]
    df = pd.read_csv(data)

    # upload student list
    stlist = StudentList(df)
    upload_info_dict = stlist.upload_list()

    if not upload_info_dict["flag"]:
        error_msg = upload_info_dict["msg"]
        return jsonify({"msg", f"{error_msg}"})
    else:
        upload_msg = upload_info_dict["msg"]

    return "OK"
