import pytest
from unittest.mock import Mock, patch, MagicMock, call
from psycopg2.extras import RealDictCursor


class TestNoteRepositoryMocked:

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_get_all_notes(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_data = [
            {'id': 1, 'title': 'Заметка 1', 'content': 'Содержимое 1',
             'category_id': 1, 'user_id': 1, 'created_at': None,
             'category_name': 'Работа', 'username': 'user1'},
            {'id': 2, 'title': 'Заметка 2', 'content': 'Содержимое 2',
             'category_id': 1, 'user_id': 1, 'created_at': None,
             'category_name': 'Работа', 'username': 'user1'}
        ]
        mock_cursor.fetchall.return_value = db_data

        repo = NoteRepository()
        result = repo.get_all_notes()


        assert len(result) == 2
        assert result[0].title == "Заметка 1"
        assert result[0].content == "Содержимое 1"
        assert result[1].title == "Заметка 2"

        mock_get_connection.assert_called_once()
        mock_conn.cursor.assert_called_once_with(cursor_factory=RealDictCursor)
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_return_connection.assert_called_once_with(mock_conn)

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_get_all_notes_empty(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        repo = NoteRepository()
        result = repo.get_all_notes()

        assert result == []
        mock_cursor.execute.assert_called_once()

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_get_note_by_id(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_data = {'id': 1, 'title': 'Тестовая заметка', 'content': 'Содержимое',
                   'category_id': 1, 'user_id': 1, 'created_at': None}
        mock_cursor.fetchone.return_value = db_data

        repo = NoteRepository()
        result = repo.get_note_by_id(1)

        assert result is not None
        assert result.id == 1
        assert result.title == "Тестовая заметка"
        assert result.content == "Содержимое"

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM notes WHERE id = %s",
            (1,)
        )

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_get_note_by_id_not_found(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        repo = NoteRepository()
        result = repo.get_note_by_id(999)

        assert result is None
        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM notes WHERE id = %s",
            (999,)
        )

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_create_note(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (42,)

        repo = NoteRepository()
        result = repo.create_note("Новая заметка", "Новое содержимое", 1, 1)

        assert result == 42

        sql_call = mock_cursor.execute.call_args[0][0]
        assert "INSERT INTO notes" in sql_call
        assert "RETURNING id" in sql_call

        params = mock_cursor.execute.call_args[0][1]
        assert params[0] == "Новая заметка"
        assert params[1] == "Новое содержимое"
        assert params[2] == 1
        assert params[3] == 1

        mock_conn.commit.assert_called_once()
        mock_return_connection.assert_called_once_with(mock_conn)

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_create_note_exception(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.execute.side_effect = Exception("Database error")

        repo = NoteRepository()
        result = repo.create_note("Новая заметка", "Новое содержимое", 1, 1)

        assert result is None
        mock_conn.rollback.assert_called_once()

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_update_note(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1

        repo = NoteRepository()
        result = repo.update_note(1, "Обновленный заголовок", "Обновленное содержимое", 1)

        assert result is True

        sql_call = mock_cursor.execute.call_args[0][0]
        assert "UPDATE notes" in sql_call
        assert "SET title = %s, content = %s, category_id = %s" in sql_call
        assert "WHERE id = %s" in sql_call

        params = mock_cursor.execute.call_args[0][1]
        assert params[0] == "Обновленный заголовок"
        assert params[1] == "Обновленное содержимое"
        assert params[2] == 1
        assert params[3] == 1

        mock_conn.commit.assert_called_once()

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_update_note_not_found(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 0

        repo = NoteRepository()
        result = repo.update_note(999, "Новый заголовок", "Новое содержимое", 1)

        assert result is False

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_delete_note(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1

        repo = NoteRepository()
        result = repo.delete_note(1)

        assert result is True

        sql_call = mock_cursor.execute.call_args[0][0]
        assert "DELETE FROM notes" in sql_call
        assert "WHERE id = %s" in sql_call

        assert mock_cursor.execute.call_args[0][1] == (1,)
        mock_conn.commit.assert_called_once()

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_delete_note_not_found(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 0

        repo = NoteRepository()
        result = repo.delete_note(999)

        assert result is False

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_search_notes_by_title(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_data = [
            {'id': 1, 'title': 'Поисковая заметка 1', 'content': 'Содержимое 1',
             'category_id': 1, 'user_id': 1, 'created_at': None,
             'category_name': 'Работа', 'username': 'user1'}
        ]
        mock_cursor.fetchall.return_value = db_data

        repo = NoteRepository()
        result = repo.search_notes_by_title("поиск")

        assert len(result) == 1
        assert "поиск" in result[0].title.lower()

        sql_call = mock_cursor.execute.call_args[0][0]
        assert "ILIKE" in sql_call
        assert mock_cursor.execute.call_args[0][1] == ('%поиск%',)

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_filter_notes_by_category(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_data = [
            {'id': 1, 'title': 'Заметка 1', 'content': 'Содержимое 1',
             'category_id': 1, 'user_id': 1, 'created_at': None,
             'category_name': 'Работа', 'username': 'user1'},
            {'id': 2, 'title': 'Заметка 2', 'content': 'Содержимое 2',
             'category_id': 1, 'user_id': 1, 'created_at': None,
             'category_name': 'Работа', 'username': 'user1'}
        ]
        mock_cursor.fetchall.return_value = db_data

        repo = NoteRepository()
        result = repo.filter_notes_by_category(1)

        assert len(result) == 2
        assert result[0].category_id == 1
        assert result[1].category_id == 1

        assert mock_cursor.execute.call_args[0][1] == (1,)

    @patch('repositories.note_repository.get_connection')
    @patch('repositories.note_repository.return_connection')
    def test_filter_notes_by_category_empty(self, mock_return_connection, mock_get_connection):

        from repositories.note_repository import NoteRepository

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        repo = NoteRepository()
        result = repo.filter_notes_by_category(999)

        assert result == []