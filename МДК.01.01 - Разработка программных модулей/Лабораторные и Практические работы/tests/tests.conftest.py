import pytest
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.note import Note
from models.category import Category
from models.user import User
from repositories.note_repository import NoteRepository
from repositories.category_repository import CategoryRepository
from repositories.user_repository import UserRepository
from services.note_service import NoteService



@pytest.fixture
def mock_note_repository():

    return Mock(spec=NoteRepository)


@pytest.fixture
def mock_category_repository():

    return Mock(spec=CategoryRepository)


@pytest.fixture
def mock_user_repository():

    return Mock(spec=UserRepository)


@pytest.fixture
def note_service():

    return NoteService()


@pytest.fixture
def note_service_with_mocks(mock_note_repository, mock_category_repository, mock_user_repository):

    service = NoteService()
    service.note_repo = mock_note_repository
    service.category_repo = mock_category_repository
    service.user_repo = mock_user_repository
    return service


@pytest.fixture
def sample_note():

    return Note(
        id=1,
        title="Тестовая заметка",
        content="Это содержимое тестовой заметки",
        category_id=1,
        user_id=1,
        created_at=None
    )


@pytest.fixture
def sample_category():

    return Category(id=1, name="Работа")


@pytest.fixture
def sample_user():

    return User(id=1, username="test_user")


@pytest.fixture
def list_of_notes():

    return [
        Note(id=1, title="Заметка 1", content="Содержимое 1", category_id=1, user_id=1),
        Note(id=2, title="Заметка 2", content="Содержимое 2", category_id=1, user_id=1),
        Note(id=3, title="Заметка 3", content="Содержимое 3", category_id=2, user_id=1)
    ]


@pytest.fixture
def list_of_categories():

    return [
        Category(id=1, name="Работа"),
        Category(id=2, name="Личное"),
        Category(id=3, name="Учеба")
    ]


@pytest.fixture
def list_of_users():

    return [
        User(id=1, username="user1"),
        User(id=2, username="user2")
    ]


@pytest.fixture
def mock_db_connection():

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor
