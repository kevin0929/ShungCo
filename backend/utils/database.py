import psycopg2
import logging
import warnings

warnings.filterwarnings("ignore")


def database_init():
    """
    connect to database and return conn

    index
    0 : Host IP
    1 : db name
    2 : user
    3 : password
    """
    conn_info = ["127.0.0.1", "shenclass", "postgres", "tn78192712301158"]
    conn_string = "host={0} user={1} dbname={2} password={3}".format(
        conn_info[0], conn_info[2], conn_info[1], conn_info[3]
    )

    try:
        conn = psycopg2.connect(conn_string)
        logging.info(f"Successfully connected to {conn_info[1]}")

        return conn
    except Exception as err:
        logging.error(f"error msg : {err}")
        return None
