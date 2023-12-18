import logging
import pandas as pd

from flask import Blueprint, render_template, url_for, redirect, request, jsonify
from collections import defaultdict

from utils.auth import login_required
from utils.database import database_init


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


@admin_bp.route("/change_password", methods=["POST"])
@login_required("admin")
def change_password():
    data = request.json
    old_password = data["old_password"]
    new_password = data["new_password"]
    username = data["username"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # check old password whether correct, if correct change password
        table_name = "loginID"

        correct_old_password_df = pd.read_sql(
            f"SELECT password FROM {table_name} WHERE username = '{username}'"
        )
        correct_old_password = correct_old_password_df["password"]

        if old_password == correct_old_password:
            query_state = f"UPDATE {table_name} SET password = '{new_password}' WHERE username = '{username}'"
            cursor.execute(query_state)
        else:
            return jsonify({"msg": "old password is wrong!"})
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("admin.manage"))


@admin_bp.route("/change_role", methods=["POST"])
@login_required("admin")
def change_role():
    # read post data from front-end
    data = request.json
    username = data["username"]
    new_role = data["newRole"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # update role change to database
        table_name = "loginID"
        query_state = (
            f"UPDATE {table_name} SET role = '{new_role}' WHERE username = '{username}'"
        )
        cursor.execute(query_state)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("admin.manage"))


@admin_bp.route("/delete_user", methods=["POST"])
@login_required("admin")
def delete_user():
    data = request.json
    username = data["username"]

    # connect to database
    try:
        conn = database_init()
        cursor = conn.cursor()

        # delete user from it's username
        table_name = "loginID"
        query_state = f"DELETE FROM {table_name} WHERE username = '{username}'"
        cursor.execute(query_state)
    except Exception as err:
        return jsonify({"msg": err})

    # commit
    conn.commit()
    cursor.close()

    return redirect(url_for("admin.manage"))
