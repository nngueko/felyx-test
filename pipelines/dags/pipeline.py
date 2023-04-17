from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import os
import psycopg2
import shutil


default_args = {
     'owner': 'mlngueko',
     'retries': 5,
     'retry_delay': timedelta(minutes=5)
}


with DAG(
        dag_id='postgres_ingestion_pipeline',
        default_args=default_args,
        start_date=datetime(2023, 4, 11),
        schedule_interval='*/5 * * * *'
) as dag:

    def get_files_dir():
        import os
        os.chdir("..")
        cwd = os.getcwd()
        only_files = [os.path.join(cwd, f) for f in os.listdir(cwd) if "files" in f]
        files = []
        for f_dir in only_files:
            files = [os.path.join(f_dir, f) for f in os.listdir(f_dir) if "incoming" in f][0]
        res = [os.path.join(files, f) for f in os.listdir(files) if "reservation" in f]
        return res


    def process_file():
        directories = get_files_dir()
        for file in directories:
            if 'reservation' in file:
                db = ConnectToDatabase()
                file_csv = open(file, 'r')
                db.cur.copy_from(file_csv, 'reservation', sep=',')
                db.conn.commit()
                db.close()
                file_csv.close()
                move_file(file)


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


    def move_file(filename):
        destination = filename.replace("incoming", "processed")
        os.rename(filename, destination)

    create_table = PostgresOperator (
        task_id='create_table',
        postgres_conn_id='postgres_local',
        sql=""" create table if not exists test_tab (
        id integer,
        name character,
        timestamp timestamp,
        primary key (id, name))
        """
     )

    process_file = PythonOperator(
        task_id='process_file',
        python_callable=process_file,
        dag=dag
    )

process_file
