from dotenv import find_dotenv, load_dotenv
from os import getenv
import psycopg2

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

db_conn = psycopg2.connect(host=getenv('HOST_DB'), database=getenv('NAME_DB'),
user=getenv('USER_DB'), password=getenv('PW_DB'), port=getenv('PORT_DB'))

# db_conn = psycopg2.connect(host="localhost", database="teste2",
# user="postgres", password="RootQWE123")
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