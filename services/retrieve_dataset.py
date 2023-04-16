import json
from flask import Flask

from setup import ConnectToDatabase

app = Flask(__name__)


@app.route('/get_data')
def index():
    sql = "SELECT * FROM tb_test"
    db = ConnectToDatabase()
    db.query(sql)
    rows = db.cur.fetchall()
    db.conn.commit()
    db.close()
    return json.dumps({"date": rows})

# app.run()