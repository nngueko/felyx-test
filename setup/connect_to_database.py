import psycopg2


class ConnectToDatabase:
    def __init__(self, db="felyx", user="postgres", pw="root"):
        self.conn = psycopg2.connect(dbname=db, user=user, password=pw)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)
        self.conn.commit()
        return self.cur

    def close(self):
        self.cur.close()
        self.conn.close()

