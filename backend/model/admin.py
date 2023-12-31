import logging
import hashlib
import pandas as pd

from flask import Blueprint, render_template, url_for, redirect, request, jsonify
from collections import defaultdict

from utils.auth import login_required
from utils.database import database_init
from utils.config import CONFIG


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/index")
@login_required("admin")
def index():
    return render_template("admin/index.html")


@admin_bp.route("/manage")
@login_required("admin")
def manage():
    # connect to database
    try:
        conn = database_init()

        # read all table information
        table_name = "loginID"
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        # traverse dataframe and make dict return to front-end
        users = []
        for idx, row in df.iterrows():
            user_dict = defaultdict(str)
            user_dict["username"] = row["username"]
            user_dict["role"] = row["role"]

            users.append(user_dict)
    except Exception as err:
        logging.error(f"The error msg : {err}")

    return render_template("admin/manage.html", users=users)


@admin_bp.route("/change_personnel", methods=["PUT"])
@login_required("admin")
def change_personnel():
    data = request.json
    change_column = data["change_column"]
    new_data = data["new_data"]
    username = data["username"]

    # hash password if data type is password
    if change_column == "password":
        new_data = hashlib.sha256(new_data.encode("UTF-8")).hexdigest()[:16]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # change password
        table_name = CONFIG["UserTable"]

        query_state = f"UPDATE {table_name} SET {change_column} = '{new_data}' WHERE username = '{username}'"
        cursor.execute(query_state)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("admin.manage"))


@admin_bp.route("/delete_user", methods=["DELETE"])
@login_required("admin")
def delete_user():
    data = request.json
    username = data["username"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # delete user from it's username
        table_name = CONFIG["UserTable"]
        query_state = f"DELETE FROM {table_name} WHERE username = '{username}'"
        cursor.execute(query_state)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("admin.manage"))
