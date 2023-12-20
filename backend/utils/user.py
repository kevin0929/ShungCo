import warnings
import hashlib

from utils.database import database_init

warnings.filterwarnings("ignore")


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def hash_passwd(self, password: str) -> str:
        password = hashlib.sha256(password.encode("UTF-8")).hexdigest()[:16]

        return password

    def login(self) -> dict:
        # check if username and password are not empty
        if (self.username or self.password) is None:
            return {"flag": False, "msg": "Username or password is empty."}

        # hash password
        self.password = self.hash_passwd(self.password)

        # Connect to database
        conn = database_init()
        if not conn:
            return {"flag": False, "msg": "Connect to database failed."}

        table_name = "loginID"

        try:
            # prevent SQL injection, we need to use parameter query
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password, role FROM {} WHERE username = %s".format(table_name),
                (self.username,),
            )
            row = cursor.fetchone()
            cursor.close()
        except Exception as err:
            return {"flag": False, "msg": f"{err}"}

        if row is None:
            return {"flag": False, "msg": "User not found."}

        correct_password, role = row

        # compare correct password and input password
        if self.password == correct_password:
            return {"flag": True, "role": role}
        else:
            return {"flag": False, "msg": "Password is incorrect."}
