import pytest
from models.note import Note


class TestNoteServiceValidation:


    def test_create_note_empty_title(self, note_service_with_mocks):

        with pytest.raises(ValueError, match="Заголовок не может быть пустым"):
            note_service_with_mocks.create_note("", "content", 1, 1)

        note_service_with_mocks.note_repo.create.assert_not_called()

    def test_create_note_whitespace_title(self, note_service_with_mocks):

        with pytest.raises(ValueError, match="Заголовок не может быть пустым"):
            note_service_with_mocks.create_note("   ", "content", 1, 1)

        note_service_with_mocks.note_repo.create.assert_not_called()

    def test_create_note_without_category(self, note_service_with_mocks):

        with pytest.raises(ValueError, match="Не выбрана категория"):
            note_service_with_mocks.create_note("Title", "Content", None, 1)

        note_service_with_mocks.note_repo.create.assert_not_called()

    def test_create_note_without_user(self, note_service_with_mocks):

        with pytest.raises(ValueError, match="Не выбран пользователь"):
            note_service_with_mocks.create_note("Title", "Content", 1, None)

        note_service_with_mocks.note_repo.create.assert_not_called()

    def test_create_note_valid(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.create.return_value = 42

        note_id = note_service_with_mocks.create_note("Valid Title", "Valid Content", 1, 1)

        assert note_id == 42
        mock_note_repository.create.assert_called_once_with("Valid Title", "Valid Content", 1, 1)

    def test_create_note_trims_whitespace(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.create.return_value = 42

        note_id = note_service_with_mocks.create_note(
            "  Title with spaces  ",
            "  Content with spaces  ",
            1,
            1
        )

        assert note_id == 42

        mock_note_repository.create.assert_called_once_with(
            "Title with spaces",
            "Content with spaces",
            1,
            1
        )

    def test_create_note_empty_content(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.create.return_value = 42

        note_id = note_service_with_mocks.create_note("Title", "", 1, 1)

        assert note_id == 42
        mock_note_repository.create.assert_called_once_with("Title", "", 1, 1)


class TestNoteServiceUpdate:

    def test_update_note_empty_title(self, note_service_with_mocks):

        with pytest.raises(ValueError, match="Заголовок не может быть пустым"):
            note_service_with_mocks.update_note(1, "", "New Content", 1)

        note_service_with_mocks.note_repo.update.assert_not_called()

    def test_update_note_whitespace_title(self, note_service_with_mocks):
        with pytest.raises(ValueError, match="Заголовок не может быть пустым"):
            note_service_with_mocks.update_note(1, "   ", "New Content", 1)

        note_service_with_mocks.note_repo.update.assert_not_called()

    def test_update_note_without_category(self, note_service_with_mocks):

        with pytest.raises(ValueError, match="Не выбрана категория"):
            note_service_with_mocks.update_note(1, "New Title", "New Content", None)

        note_service_with_mocks.note_repo.update.assert_not_called()

    def test_update_note_valid(self, note_service_with_mocks, mock_note_repository):
        mock_note_repository.update.return_value = True

        result = note_service_with_mocks.update_note(1, "New Title", "New Content", 1)

        assert result is True
        mock_note_repository.update.assert_called_once_with(1, "New Title", "New Content", 1)

    def test_update_note_trim_whitespace(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.update.return_value = True

        result = note_service_with_mocks.update_note(
            1,
            "  New Title  ",
            "  New Content  ",
            1
        )

        assert result is True

        mock_note_repository.update.assert_called_once_with(1, "New Title", "New Content", 1)


class TestNoteServiceDelete:


    def test_delete_note_success(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.delete.return_value = True

        result = note_service_with_mocks.delete_note(1)

        assert result is True
        mock_note_repository.delete.assert_called_once_with(1)

    def test_delete_note_not_found(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.delete.return_value = False

        result = note_service_with_mocks.delete_note(999)

        assert result is False
        mock_note_repository.delete.assert_called_once_with(999)


class TestNoteServiceSearch:

    def test_search_notes_empty_query(self, note_service_with_mocks, mock_note_repository, list_of_notes):

        mock_note_repository.get_all_notes.return_value = list_of_notes

        result = note_service_with_mocks.search_notes("")

        assert len(result) == 3
        assert result == list_of_notes
        mock_note_repository.get_all_notes.assert_called_once()
        mock_note_repository.search_notes_by_title.assert_not_called()

    def test_search_notes_whitespace_query(self, note_service_with_mocks, mock_note_repository, list_of_notes):
        mock_note_repository.get_all_notes.return_value = list_of_notes

        result = note_service_with_mocks.search_notes("   ")

        assert len(result) == 3
        mock_note_repository.get_all_notes.assert_called_once()

    def test_search_notes_with_results(self, note_service_with_mocks, mock_note_repository):

        expected_notes = [
            Note(id=1, title="Заметка 1", content="Содержимое 1", category_id=1, user_id=1)
        ]
        mock_note_repository.search_notes_by_title.return_value = expected_notes

        result = note_service_with_mocks.search_notes("Заметка")

        assert len(result) == 1
        assert result[0].title == "Заметка 1"
        mock_note_repository.search_notes_by_title.assert_called_once_with("Заметка")

    def test_search_notes_no_results(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.search_notes_by_title.return_value = []

        result = note_service_with_mocks.search_notes("Несуществующий запрос")

        assert result == []
        mock_note_repository.search_notes_by_title.assert_called_once_with("Несуществующий запрос")


class TestNoteServiceFilterByCategory:

    def test_filter_by_category_none(self, note_service_with_mocks, mock_note_repository, list_of_notes):

        mock_note_repository.get_all_notes.return_value = list_of_notes

        result = note_service_with_mocks.filter_notes_by_category(None)

        assert len(result) == 3
        mock_note_repository.get_all_notes.assert_called_once()
        mock_note_repository.filter_notes_by_category.assert_not_called()

    def test_filter_by_category(self, note_service_with_mocks, mock_note_repository, list_of_notes):
        expected_notes = [list_of_notes[0], list_of_notes[1]]
        mock_note_repository.filter_notes_by_category.return_value = expected_notes

        result = note_service_with_mocks.filter_notes_by_category(1)

        assert len(result) == 2
        assert result[0].category_id == 1
        assert result[1].category_id == 1
        mock_note_repository.filter_notes_by_category.assert_called_once_with(1)

    def test_filter_by_category_no_notes(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.filter_notes_by_category.return_value = []

        result = note_service_with_mocks.filter_notes_by_category(999)

        assert result == []
        mock_note_repository.filter_notes_by_category.assert_called_once_with(999)


class TestNoteServiceGetAll:

    def test_get_all_notes(self, note_service_with_mocks, mock_note_repository, list_of_notes):

        mock_note_repository.get_all_notes.return_value = list_of_notes

        result = note_service_with_mocks.get_all_notes()

        assert len(result) == 3
        assert result == list_of_notes
        mock_note_repository.get_all_notes.assert_called_once()

    def test_get_all_notes_empty(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.get_all_notes.return_value = []

        result = note_service_with_mocks.get_all_notes()

        assert result == []
        mock_note_repository.get_all_notes.assert_called_once()


class TestNoteServiceGetById:

    def test_get_by_id_valid(self, note_service_with_mocks, mock_note_repository, sample_note):

        mock_note_repository.get_note_by_id.return_value = sample_note

        result = note_service_with_mocks.get_note_by_id(1)

        assert result == sample_note
        mock_note_repository.get_note_by_id.assert_called_once_with(1)

    def test_get_by_id_not_found(self, note_service_with_mocks, mock_note_repository):

        mock_note_repository.get_note_by_id.return_value = None

        result = note_service_with_mocks.get_note_by_id(999)

        assert result is None
        mock_note_repository.get_note_by_id.assert_called_once_with(999)


class TestNoteServiceCategoriesAndUsers:

    def test_get_all_categories(self, note_service_with_mocks, mock_category_repository, list_of_categories):
        mock_category_repository.get_all_categories.return_value = list_of_categories

        result = note_service_with_mocks.get_all_categories()

        assert len(result) == 3
        assert result == list_of_categories
        mock_category_repository.get_all_categories.assert_called_once()

    def test_get_all_users(self, note_service_with_mocks, mock_user_repository, list_of_users):
        mock_user_repository.get_all_users.return_value = list_of_users

        result = note_service_with_mocks.get_all_users()

        assert len(result) == 2
        assert result == list_of_users
        mock_user_repository.get_all_users.assert_called_once()