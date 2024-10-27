import sqlite3 as sql3


def db_conn():
    conn = sql3.connect('dbs/dbs.db')
    conn.row_factory = sql3.Row
    return conn

