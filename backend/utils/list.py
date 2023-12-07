import pandas as pd
import hashlib

from utils.database import database_init


class StudentList:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def hash_passwd(self, password: str) -> str:
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()[:16]

        return password

    def upload_list(self) -> dict:
        """
        read csv and insert into database
        """

        # connect to database
        conn = database_init()
        if not conn:
            return {"flag": False, "msg": "Connect to database failed."}
        else:
            cursor = conn.cursor()

        table_name = "loginID"

        msg_list = []
        for idx, row in self.df.iterrows():
            username = row["username"]
            password = row["password"]
            role = row["role"]

            password = self.hash_passwd(password)

            try:
                cursor.execute(
                    f"INSERT INTO {table_name} (username, password, role) VALUES (%s, %s, %s)",
                    (username, password, role),
                )

                # make msg ready to return back to frontend
                msg = f"user: {username}, role: {role} - added sucessfully!"
                msg_list.append(msg)
            except Exception as err:
                msg = f"user: {username}, role: {role} - {err}"
                msg_list.append(msg)

        conn.commit()
        cursor.close()

        return {"flag": True, "msg": msg_list}
