from typing import Optional, List
from psycopg2.extras import RealDictCursor
import psycopg2
from .repository import User, Order


class UserRepository:
    def __init__(self, conn):

        self.conn = conn
    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, email, status FROM users WHERE id = %s",
                (user_id,)
            )
            row = cur.fetchone()

        if row:
            return User(**row)
        return None

    def create(self, user: User) -> User:
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO users (name, email, status) 
                   VALUES (%s, %s, %s) RETURNING id""",
                (user.name, user.email, user.status)
            )
            user_id = cur.fetchone()['id']
            self.conn.commit()

        return User(id=user_id, name=user.name, email=user.email, status=user.status)

    def get_all(self) -> List[User]:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name, email, status FROM users")
            rows = cur.fetchall()

        return [User(**row) for row in rows]

    def delete(self, user_id: int) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            deleted = cur.rowcount > 0
            self.conn.commit()

        return deleted


class OrderRepository:

    def __init__(self, conn):
        self.conn = conn

    def create(self, order: Order) -> Order:
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO orders (user_id, product_name, quantity) 
                   VALUES (%s, %s, %s) RETURNING id""",
                (order.user_id, order.product_name, order.quantity)
            )
            order_id = cur.fetchone()['id']
            self.conn.commit()

        return Order(id=order_id, **order.__dict__)