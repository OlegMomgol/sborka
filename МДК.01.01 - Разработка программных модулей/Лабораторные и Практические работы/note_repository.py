from database.connection import get_connection, return_connection
from models.note import Note
from psycopg2.extras import RealDictCursor


class NoteRepository:
    def get_all_notes(self):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT n.*, c.name as category_name, u.username 
                    FROM notes n
                    LEFT JOIN categories c ON n.category_id = c.id
                    LEFT JOIN users u ON n.user_id = u.id
                    ORDER BY n.created_at DESC
                """)
                return [Note.from_dict(dict(row)) for row in cur.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении заметок: {e}")
            return []
        finally:
            if conn:
                return_connection(conn)

    def get_note_by_id(self, note_id):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM notes WHERE id = %s",
                    (note_id,)
                )
                row = cur.fetchone()
                return Note.from_dict(dict(row)) if row else None
        except Exception as e:
            print(f"Ошибка при получении заметки: {e}")
            return None
        finally:
            if conn:
                return_connection(conn)

    def create_note(self, title, content, category_id, user_id):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO notes (title, content, category_id, user_id, created_at)
                    VALUES (%s, %s, %s, %s, NOW())
                    RETURNING id
                    """,
                    (title, content, category_id, user_id)
                )
                note_id = cur.fetchone()[0]
                conn.commit()
                return note_id
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Ошибка при создании заметки: {e}")
            return None
        finally:
            if conn:
                return_connection(conn)

    def update_note(self, note_id, title, content, category_id):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE notes 
                    SET title = %s, content = %s, category_id = %s
                    WHERE id = %s
                    """,
                    (title, content, category_id, note_id)
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Ошибка при обновлении заметки: {e}")
            return False
        finally:
            if conn:
                return_connection(conn)

    def delete_note(self, note_id):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM notes WHERE id = %s",
                    (note_id,)
                )
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Ошибка при удалении заметки: {e}")
            return False
        finally:
            if conn:
                return_connection(conn)

    def search_notes_by_title(self, search_term):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT n.*, c.name as category_name, u.username 
                    FROM notes n
                    LEFT JOIN categories c ON n.category_id = c.id
                    LEFT JOIN users u ON n.user_id = u.id
                    WHERE n.title ILIKE %s
                    ORDER BY n.created_at DESC
                    """,
                    (f'%{search_term}%',)
                )
                return [Note.from_dict(dict(row)) for row in cur.fetchall()]
        except Exception as e:
            print(f"Ошибка при поиске заметок: {e}")
            return []
        finally:
            if conn:
                return_connection(conn)

    def filter_notes_by_category(self, category_id):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT n.*, c.name as category_name, u.username 
                    FROM notes n
                    LEFT JOIN categories c ON n.category_id = c.id
                    LEFT JOIN users u ON n.user_id = u.id
                    WHERE n.category_id = %s
                    ORDER BY n.created_at DESC
                    """,
                    (category_id,)
                )
                return [Note.from_dict(dict(row)) for row in cur.fetchall()]
        except Exception as e:
            print(f"Ошибка при фильтрации заметок: {e}")
            return []
        finally:
            if conn:
                return_connection(conn)