import pandas as pd

from flask import Blueprint, render_template, session, jsonify
from collections import defaultdict

from utils.auth import login_required
from utils.database import database_init
from utils.config import CONFIG

student_bp = Blueprint("student", __name__)


@student_bp.route("/index")
@login_required("student")
def index():
    return render_template("student/index.html")


@student_bp.route("/video")
@login_required("student")
def video():
    # get username by session
    username = session.get("username")

    # connect to database
    try:
        conn = database_init()

        table_name = CONFIG["StudentVideoTable"]
        df = pd.read_sql(
            f"SELECT * FROM {table_name} WHERE student_name = '{username}'", conn
        )

        # get student have videos
        student_have_videos = []
        for idx, row in df.iterrows():
            student_have_videos.append(row["video_title"])

        # get have videos information
        video_table_name = CONFIG["VideoTable"]
        video_df = pd.read_sql(f"SELECT * FROM {video_table_name}", conn)

        videos = []
        for have_video in student_have_videos:
            sub_video_df = video_df.loc[video_df["video_title"] == have_video]

            for idx, row in sub_video_df.iterrows():
                video_dict = defaultdict()
                video_dict["title"] = row["video_title"]
                video_dict["url"] = row["video_url"].split("/")[-1]

                videos.append(video_dict)

    except Exception as err:
        return jsonify({"msg": f"{err}"})

    return render_template("student/video.html", videos=videos)
