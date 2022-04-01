import psycopg2
import os


configs = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

conn = psycopg2.connect(**configs)


class DatabaseConnector:
    @classmethod
    def start_conn_cur(cls):
        cls.conn = psycopg2.connect(**configs)
        cls.cur = cls.conn.cursor()

    @classmethod
    def end_conn_cur(cls):
        cls.cur.close()
        cls.conn.close()
