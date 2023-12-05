import psycopg2
import logging
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def Auth(self) -> bool:
        # check if username and password are not empty
        if (self.username or self.password) is None:
            logging.info("Your username or password is empty")
            return False

        # Connect to database
        conn_info = ["127.0.0.1", "shenclass", "postgres", "tn78192712301158"]
        conn_string = "host={0} user={1} dbname={2} password={3}".format(
            conn_info[0], conn_info[2], conn_info[1], conn_info[3]
        )
        conn = psycopg2.connect(conn_string)

        logging.info(f"Successfully connected to {conn_info[1]}")

        table_name = "loginID"

        try:
            df = pd.read_sql(
                f"SELECT password FROM {table_name} WHERE username = '{self.username}'",
                conn,
            )
        except Exception as err:
            logging.info(f"Run into error when read database, error msg : {err}")
            return False

        correct_password = df["password"].values[0]

        # compare correct password and input password
        if self.password == correct_password:
            return True
        else:
            return False


if __name__ == "__main__":
    user = User("admin", "admin")
    flag = user.Auth()
    print(flag)
