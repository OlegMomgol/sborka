from repositories.note_repository import NoteRepository
from repositories.category_repository import CategoryRepository
from repositories.user_repository import UserRepository


class NoteService:
    def __init__(self):
        self.note_repo = NoteRepository()
        self.category_repo = CategoryRepository()
        self.user_repo = UserRepository()

    def get_all_notes(self):
        return self.note_repo.get_all_notes()

    def get_note_by_id(self, note_id):
        return self.note_repo.get_note_by_id(note_id)

    def create_note(self, title, content, category_id, user_id):
        # Бизнес-логика: проверка данных
        if not title or not title.strip():
            raise ValueError("Заголовок не может быть пустым")

        if not category_id:
            raise ValueError("Не выбрана категория")

        if not user_id:
            raise ValueError("Не выбран пользователь")

        return self.note_repo.create_note(
            title.strip(),
            content.strip() if content else "",
            category_id,
            user_id
        )

    def update_note(self, note_id, title, content, category_id):
        if not title or not title.strip():
            raise ValueError("Заголовок не может быть пустым")

        if not category_id:
            raise ValueError("Не выбрана категория")

        return self.note_repo.update_note(
            note_id,
            title.strip(),
            content.strip() if content else "",
            category_id
        )

    def delete_note(self, note_id):
        return self.note_repo.delete_note(note_id)

    def search_notes(self, search_term):
        if not search_term or not search_term.strip():
            return self.get_all_notes()
        return self.note_repo.search_notes_by_title(search_term.strip())

    def filter_notes_by_category(self, category_id):
        if not category_id:
            return self.get_all_notes()
        return self.note_repo.filter_notes_by_category(category_id)

    def get_all_categories(self):
        return self.category_repo.get_all_categories()

    def get_all_users(self):
        return self.user_repo.get_all_users()