import os
import json
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
    # connect to database
    try:
        conn = database_init()

        table_name = CONFIG["VideoTable"]
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        videos = []
        for idx, row in df.iterrows():
            video_dict = defaultdict()
            video_dict["id"] = row["video_id"]
            video_dict["title"] = row["video_title"]
            video_dict["describe"] = row["video_describe"]
            video_dict["course_id"] = row["course_id"]
            video_dict["teacher_name"] = row["teacher_name"]

            videos.append(video_dict)
    except Exception as err:
        return jsonify({"msg": err})

    return render_template("teacher/video.html", videos=videos)


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


@teacher_bp.route("/distribute")
@login_required("teacher")
def distribute():
    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        student_table = CONFIG["UserTable"]
        video_table = CONFIG["VideoTable"]

        # fetch student list
        student_df = pd.read_sql(f"SELECT * FROM {student_table}", conn)
        students = []
        for idx, row in student_df.iterrows():
            if row["role"] == "student":
                student_dict = defaultdict()
                student_dict["name"] = row["username"]

                students.append(student_dict)

        # fetch video list
        video_df = pd.read_sql(f"SELECT * FROM {video_table}", conn)
        videos = []
        for idx, row in video_df.iterrows():
            video_dict = defaultdict()
            video_dict["id"] = row["video_id"]
            video_dict["title"] = row["video_title"]

            videos.append(video_dict)
    except Exception as err:
        return jsonify({"msg": err})

    return render_template("teacher/distribute.html", students=students, videos=videos)


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


@teacher_bp.route("/change_video", methods=["PUT"])
@login_required("teacher")
def change_video():
    data = request.json
    change_column = data["change_column"]
    new_data = data["new_data"]
    video_id = data["video_id"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # change column value depend on course id
        table_name = sql.Identifier(CONFIG["VideoTable"])
        column_name = sql.Identifier(change_column)

        query_state = sql.SQL("UPDATE {} SET {} = %s WHERE video_id = %s").format(
            table_name, column_name
        )
        query_args = (new_data, video_id)
        cursor.execute(query_state, query_args)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("teacher.video"))


@teacher_bp.route("/delete_video", methods=["POST"])
@login_required("teacher")
def delete_video():
    data = request.json
    video_id = data["video_id"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # delete user from it's username
        table_name = sql.Identifier(CONFIG["VideoTable"])

        # delete video file
        query_state = sql.SQL("SELECT video_url FROM {} WHERE video_id = %s").format(
            table_name
        )
        cursor.execute(query_state, (video_id,))
        video_url = cursor.fetchone()[0]
        os.remove(video_url)

        query_state = sql.SQL("DELETE FROM {} WHERE video_id = %s").format(table_name)
        cursor.execute(query_state, (video_id,))
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("teacher.course"))


@teacher_bp.route("/upload_video", methods=["POST"])
@login_required("teacher")
def upload_video():
    # get video
    video = request.files["video"]
    video_name = video.filename

    json_data = request.form.get("data")
    if json_data:
        try:
            video_info = json.loads(json_data)
            video_title = video_info["video_title"]
            video_describe = video_info["video_describe"]
            course_id = video_info["course_id"]
        except json.JSONDecodeError:
            return jsonify({"msg": "Invalid JSON data!"}), 400
    else:
        return jsonify({"msg": "No video info provided!"}), 400

    # save video info to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # find teacher name by course id from course table
        video_table = sql.Identifier(CONFIG["VideoTable"])
        course_table = sql.Identifier(CONFIG["CourseTable"])

        query_state = sql.SQL(
            "SELECT teacher_name FROM {} WHERE course_id = %s"
        ).format(course_table)
        cursor.execute(query_state, (course_id,))
        teacher_name = cursor.fetchone()[0]

        # find max id in video table
        query_state = sql.SQL("SELECT MAX(video_id) FROM {}").format(video_table)
        cursor.execute(query_state)
        max_video_id = cursor.fetchone()[0]

        if max_video_id is None:
            max_video_id = 0
        else:
            max_video_id = int(max_video_id) + 1

        # add video url
        video_url = f"../video/{video_name}"

        # insert data into database
        query_state = sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s)").format(
            video_table
        )
        insert_data = (
            max_video_id,
            video_title,
            video_describe,
            course_id,
            teacher_name,
            video_url,
        )
        cursor.execute(query_state, insert_data)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    # save video to video folder
    if video:
        video.save(f"../video/{video_name}")
    else:
        return jsonify({"msg": "no file uploaded!"})

    return redirect(url_for("teacher.video"))


@teacher_bp.route("/change_course", methods=["PUT"])
@login_required("teacher")
def change_course():
    data = request.json
    change_column = data["change_column"]
    new_data = data["new_data"]
    course_id = data["course_id"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # change column value depend on course id
        table_name = sql.Identifier(CONFIG["CourseTable"])
        column_name = sql.Identifier(change_column)

        query_state = sql.SQL("UPDATE {} SET {} = %s WHERE course_id = %s").format(
            table_name, column_name
        )
        query_args = (new_data, course_id)
        cursor.execute(query_state, query_args)
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
        table_name = sql.Identifier(CONFIG["CourseTable"])

        query_state = sql.SQL("DELETE FROM {} WHERE course_id = %s").format(table_name)
        cursor.execute(query_state, (course_id,))
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
