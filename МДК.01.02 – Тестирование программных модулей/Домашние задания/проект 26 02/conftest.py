import pytest
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.database import get_db_connection
from src.repository import UserRepository, OrderRepository


@pytest.fixture(scope="session")
def setup_test_database():
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='postgres'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("DROP DATABASE IF EXISTS test_db")
    cur.execute("CREATE DATABASE test_db")
    cur.close()
    conn.close()

    test_conn = psycopg2.connect(
        host='localhost',
        database='test_db',
        user='postgres',
        password='postgres'
    )
    cur = test_conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            status VARCHAR(20) NOT NULL CHECK (status IN ('active', 'inactive', 'blocked'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            product_name VARCHAR(100) NOT NULL,
            quantity INTEGER CHECK (quantity > 0)
        )
    """)

    test_conn.commit()
    cur.close()
    test_conn.close()

    yield

    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='postgres'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS test_db")
    cur.close()
    conn.close()


@pytest.fixture
def db_connection(setup_test_database):
    conn = get_db_connection()
    conn.autocommit = False
    yield conn

    conn.rollback()
    conn.close()


@pytest.fixture
def user_repo(db_connection):
    return UserRepository(db_connection)


@pytest.fixture
def order_repo(db_connection):
    return OrderRepository(db_connection)


@pytest.fixture
def sample_user(db_connection):
    with db_connection.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, email, status) VALUES (%s, %s, %s) RETURNING id",
            ("Test User", "test@example.com", "active")
        )
        user_id = cur.fetchone()['id']
        db_connection.commit()

    return {"id": user_id, "name": "Test User", "email": "test@example.com", "status": "active"}