from database.connection import get_connection, return_connection
from models.user import User
from psycopg2.extras import RealDictCursor


class UserRepository:

    def get_all_users(self):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users ORDER BY username")
                return [User.from_dict(dict(row)) for row in cur.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении пользователей: {e}")
            return []
        finally:
            if conn:
                return_connection(conn)

    def get_user_by_id(self, user_id):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM users WHERE id = %s",
                    (user_id,)
                )
                row = cur.fetchone()
                return User.from_dict(dict(row)) if row else None
        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            return None
        finally:
            if conn:
                return_connection(conn)

    def create_user(self, username):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username) VALUES (%s) RETURNING id",
                    (username,)
                )
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Ошибка при создании пользователя: {e}")
            return None
        finally:
            if conn:
                return_connection(conn)