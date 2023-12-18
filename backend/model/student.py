from flask import Blueprint, render_template, url_for

from utils.auth import login_required


student_bp = Blueprint("student", __name__)


@student_bp.route("/index")
@login_required("student")
def index():
    return render_template("student/index.html")


@student_bp.route("/video")
@login_required("student")
def video():
    return render_template("student/video.html")


@student_bp.route("/reserve")
@login_required("student")
def student():
    return render_template("student/reserve.html")
