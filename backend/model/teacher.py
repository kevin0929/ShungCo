import pandas as pd

from psycopg2 import sql
from collections import defaultdict
from flask import Blueprint, render_template, url_for, request, jsonify, redirect

from utils.auth import login_required
from utils.config import CONFIG
from utils.list import StudentList
from utils.database import database_init

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


@teacher_bp.route("/course")
@login_required("teacher")
def course():
    # connect to database
    try:
        conn = database_init()

        # traverse database (course)
        table_name = CONFIG["CourseTable"]
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        courses = []
        for idx, row in df.iterrows():
            course_dict = defaultdict()
            course_dict["id"] = row["course_id"]
            course_dict["title"] = row["course_title"]
            course_dict["teacher"] = row["teacher_name"]
            course_dict["describe"] = row["course_describe"]

            courses.append(course_dict)
    except Exception as err:
        return jsonify({"msg": err})

    return render_template("teacher/course.html", courses=courses)


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

    return jsonify({"msg": upload_msg})


@teacher_bp.route("/upload_video", methods=["POST"])
@login_required("teacher")
def upload_video():
    data = request.files["video"]
    filename = data.filename

    # save video to video folder
    if data:
        data.save(f"../video/{filename}")
    else:
        return jsonify({"msg": "no file uploaded!"})

    return redirect(url_for("teacher.video"))


@teacher_bp.route("/change_title", methods=["POST"])
@login_required("teacher")
def change_title():
    data = request.json
    new_title = data["new_title"]
    course_id = data["course_id"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # change course title depend on course id
        table_name = CONFIG["CourseTable"]
        query_state = f"UPDATE {table_name} SET course_title = '{new_title}' WHERE course_id = {course_id}"
        cursor.execute(query_state)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("teacher.course"))


@teacher_bp.route("/change_teacher", methods=["POST"])
@login_required("teacher")
def change_teacher():
    data = request.json
    new_teacher = data["new_teacher"]
    course_id = data["course_id"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # change course title depend on course id
        table_name = CONFIG["CourseTable"]
        query_state = f"UPDATE {table_name} SET teacher_name = '{new_teacher}' WHERE course_id = {course_id}"
        cursor.execute(query_state)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("teacher.course"))


@teacher_bp.route("/change_describe", methods=["POST"])
@login_required("teacher")
def change_describe():
    data = request.json
    new_describe = data["new_describe"]
    course_id = data["course_id"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # change course title depend on course id
        table_name = CONFIG["CourseTable"]
        query_state = f"UPDATE {table_name} SET course_describe = '{new_describe}' WHERE course_id = {course_id}"
        cursor.execute(query_state)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("teacher.course"))


@teacher_bp.route("/delete_course", methods=["POST"])
@login_required("teacher")
def delete_course():
    data = request.json
    course_id = data["course_id"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # delete user from it's username
        table_name = CONFIG["CourseTable"]
        query_state = f"DELETE FROM {table_name} WHERE course_id = {course_id}"
        cursor.execute(query_state)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("teacher.course"))


@teacher_bp.route("/upload_course", methods=["POST"])
@login_required("teacher")
def upload_course():
    data = request.json
    course_title = data["course_title"]
    course_teacher = data["course_teacher"]
    course_describe = data["course_describe"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # insert data into database
        table_name = sql.Identifier(CONFIG["CourseTable"])
        column_name = sql.Identifier("course_id")

        # query course_id max value to set new course_id
        id_query_state = sql.SQL("SELECT MAX({}) FROM {}").format(
            column_name, table_name
        )
        cursor.execute(id_query_state)
        max_course_id = cursor.fetchone()[0]

        if max_course_id is None:
            max_course_id = 0
        else:
            max_course_id = int(max_course_id) + 1

        # insert data into database
        query_state = sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s)").format(
            table_name
        )
        insert_data = (max_course_id, course_title, course_teacher, course_describe)
        cursor.execute(query_state, insert_data)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("teacher.course"))
