import pytest
from datetime import datetime
from models.note import Note
from models.category import Category
from models.user import User


class TestNoteModel:


    def test_create_note(self):

        note = Note(
            id=1,
            title="Тестовая заметка",
            content="Это содержимое тестовой заметки",
            category_id=2,
            user_id=3,
            created_at=None
        )

        assert note.id == 1
        assert note.title == "Тестовая заметка"
        assert note.content == "Это содержимое тестовой заметки"
        assert note.category_id == 2
        assert note.user_id == 3
        assert note.created_at is None

    def test_create_note_with_created_at(self):

        created_at = datetime.now()
        note = Note(
            id=1,
            title="Заметка",
            content="Содержимое",
            category_id=1,
            user_id=1,
            created_at=created_at
        )

        assert note.created_at == created_at

    def test_note_repr(self):
        note = Note(id=1, title="Тестовая заметка", content="Содержимое", category_id=1, user_id=1)

        repr_str = repr(note)
        assert isinstance(repr_str, str)
        assert "Note(id=1, title='Тестовая заметка')" == repr_str

    def test_note_from_dict(self):
        data = {
            'id': 1,
            'title': 'Заметка из словаря',
            'content': 'Содержимое',
            'category_id': 2,
            'user_id': 3,
            'created_at': None
        }

        note = Note.from_dict(data)

        assert note.id == 1
        assert note.title == "Заметка из словаря"
        assert note.content == "Содержимое"
        assert note.category_id == 2
        assert note.user_id == 3

    def test_note_from_dict_without_id(self):
        data = {
            'title': 'Заметка без ID',
            'content': 'Содержимое',
            'category_id': 1,
            'user_id': 1
        }

        note = Note.from_dict(data)

        assert note.id is None
        assert note.title == "Заметка без ID"

    def test_note_to_dict(self):
        note = Note(
            id=1,
            title="Тестовая заметка",
            content="Содержимое",
            category_id=1,
            user_id=1,
            created_at=None
        )

        result = note.to_dict()
        assert isinstance(result, dict)
        assert result['id'] == 1
        assert result['title'] == "Тестовая заметка"
        assert result['content'] == "Содержимое"
        assert result['category_id'] == 1
        assert result['user_id'] == 1
        assert result['created_at'] is None


class TestCategoryModel:

    def test_create_category(self):
        category = Category(id=1, name="Работа")

        assert category.id == 1
        assert category.name == "Работа"

    def test_category_repr(self):
        category = Category(id=1, name="Работа")

        repr_str = repr(category)
        assert isinstance(repr_str, str)
        assert "Category(id=1, name='Работа')" == repr_str

    def test_category_from_dict(self):
        data = {'id': 1, 'name': 'Личное'}

        category = Category.from_dict(data)

        assert category.id == 1
        assert category.name == "Личное"

    def test_category_from_dict_without_id(self):

        data = {'name': 'Учеба'}

        category = Category.from_dict(data)

        assert category.id is None
        assert category.name == "Учеба"


class TestUserModel:

    def test_create_user(self):

        user = User(id=1, username="test_user")

        assert user.id == 1
        assert user.username == "test_user"

    def test_user_repr(self):

        user = User(id=1, username="test_user")

        repr_str = repr(user)
        assert isinstance(repr_str, str)
        assert "User(id=1, username='test_user')" == repr_str

    def test_user_from_dict(self):

        data = {'id': 1, 'username': 'new_user'}

        user = User.from_dict(data)

        assert user.id == 1
        assert user.username == "new_user"

    def test_user_from_dict_without_id(self):

        data = {'username': 'guest'}

        user = User.from_dict(data)

        assert user.id is None
        assert user.username == "guest"