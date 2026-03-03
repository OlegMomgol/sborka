import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv('HOST', 'localhost'),
        database=os.getenv('NAME', 'test_db'),
        user=os.getenv('USER', 'postgres'),
        password=os.getenv('PASSWORD', 'postgres'),
        cursor_factory=RealDictCursor
    )