import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import OperationalError


def get_connection():
    try:
        return pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="test_sap_b1",
            cursorclass=DictCursor,
        )
    except OperationalError:
        raise Exception("No se pudo conectar a base de datos")
