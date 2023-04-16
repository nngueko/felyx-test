import json
from flask import Flask
import psycopg2
from setup import ConnectToDatabase

app = Flask(__name__)


@app.route('/get_data')
def index():
    sql = "SELECT * FROM reservation"
    db = ConnectToDatabase()
    db.query(sql)
    rows = db.cur.fetchall()
    db.conn.commit()
    db.close()
    return json.dumps({"date": rows})


class DataManipulation:

    def __init__(self):
        self.res = None

    def retrieved_data(self):
        sql = f"SELECT COUNT(*) FROM reservation;"
        db = ConnectToDatabase()
        db.query(sql)
        rows = db.cur.fetchall()
        db.conn.commit()
        db.close()
        self.res = False
        if rows:
            self.res = True
        return self.res




# class ConnectToDatabase:
#     def __init__(self, db="felyx", user="postgres", pw="root"):
#         self.conn = psycopg2.connect(dbname=db, user=user, password=pw)
#         self.cur = self.conn.cursor()
#
#     def query(self, query):
#         self.cur.execute(query)
#         self.conn.commit()
#         return self.cur
#
#     def close(self):
#         self.cur.close()
#         self.conn.close()


# app.run()
