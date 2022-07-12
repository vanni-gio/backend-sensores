import psycopg2
from os import getenv



db_conn = psycopg2.connect(host="localhost", database="teste2",
user="postgres", password="RootQWE123")
cursor = db_conn.cursor()

class HandleDB():
    def execute(self, sql):
        cursor.execute(sql)

    def commit(self,):
        db_conn.commit()

    def fetch_one(self):
        return cursor.fetchone()

    def fetch_many(self,size):
        return cursor.fetchmany(size)

    def fetch_all(self):
        return cursor.fetchall()

    def rollback(self):
        db_conn.rollback()