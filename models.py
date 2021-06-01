import sqlite3
from sqlite3 import Error

create_projects_sql = """
-- projects table
CREATE TABLE IF NOT EXISTS projects (
  id integer PRIMARY KEY,
  title text NOT NULL,
  description text,
  done boolean
);
"""


def create_connection(db_file):
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
       return conn
   except Error as e:
       print(e)


def create_connection_in_memory():
   conn = None
   try:
       conn = sqlite3.connect(":memory:")
       print(f"Connected, sqlite version: {sqlite3.version}")
       return conn
   except Error as e:
       print(e)
   finally:
       if conn:
           conn.close()


def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
       return c
   except Error as e:
       print(e)


def add_projects(conn, data):
   """
   Create a new projekt into the projects table
   :param conn:
   :param projekt:
   :return projekt id
   """
   sql = '''INSERT INTO projects( title, description, done)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, data)
   return cur.lastrowid


def update_projects(conn, data):
   """
    Update project
   :param conn:
   :param projekt:
   :return projekt id
   """
   sql = '''UPDATE projects
            SET title = ?,
                description = ?,
                done = ?
            WHERE
                id = ?;
   '''
   cur = conn.cursor()
   cur.execute(sql, data)
   cur.execute("SELECT * FROM projects")
   return cur.lastrowid


def save_and_close(conn):
    conn.commit()
    conn.close()


