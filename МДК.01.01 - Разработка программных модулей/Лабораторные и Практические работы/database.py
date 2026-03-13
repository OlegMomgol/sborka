import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

connection_pool = None

def init_connection_pool():

    global connection_pool
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1,
        20,
        dbname="note_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    return connection_pool

def get_connection():
    if connection_pool is None:
        init_connection_pool()
    return connection_pool.getconn()

def return_connection(conn):
    if connection_pool:
        connection_pool.putconn(conn)

def get_connection_simple():
    return psycopg2.connect(
        dbname="note_manager",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )