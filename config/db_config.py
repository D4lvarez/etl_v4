import pymysql
from pymysql.cursors import DictCursor


def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="test_sap_b1",
        cursorclass=DictCursor,
    )
